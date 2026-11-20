"""Reproducible exploratory cohort analysis; run from the root or notebooks directory."""
# %%
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from scipy.sparse import csr_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, average_precision_score, confusion_matrix, roc_curve

ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / 'CODEX.md').is_file())
RAW = ROOT / 'data/raw/2021_2023'
OUT = ROOT / 'results/cohort'
OUT.mkdir(parents=True, exist_ok=True)
cbc_vars = ['LBXWBCSI', 'LBXRBCSI', 'LBXHGB', 'LBXHCT', 'LBXMCVSI', 'LBXRDW',
            'LBXPLTSI', 'LBXLYPCT', 'LBXNEPCT', 'LBXMOPCT', 'LBXEOPCT', 'LBXBAPCT']
numeric = ['RIDAGEYR', 'INDFMPIR']
categorical = ['RIAGENDR', 'RIDRETH3', 'DMDEDUC2']

def load(name):
    frame = pd.read_sas(RAW / (name + '_L.xpt'), format='xport')
    assert frame.SEQN.is_unique, name
    # pandas XPORT can decode SAS zero as a tiny positive number.
    for col in frame.select_dtypes(include='number'):
        frame.loc[frame[col].abs().lt(1e-70), col] = 0.0
    return frame

demo, cbc, ghb, diq = [load(name) for name in ['DEMO', 'CBC', 'GHB', 'DIQ']]
df = demo.merge(cbc[['SEQN'] + cbc_vars], on='SEQN', how='left', validate='one_to_one')
df = df.merge(ghb[['SEQN', 'LBXGH', 'WTPH2YR']], on='SEQN', how='left', validate='one_to_one')
df = df.merge(diq[['SEQN', 'DIQ010', 'DIQ050', 'DIQ070']], on='SEQN', how='left', validate='one_to_one')
assert len(df) == len(demo)
df['DMDEDUC2'] = df.DMDEDUC2.replace({7: np.nan, 9: np.nan})
df['diagnosis_status'] = df.DIQ010.map({1: 'yes', 2: 'no', 3: 'borderline', 7: 'refused', 9: 'unknown'}).fillna('missing')
df['target'] = (df.LBXGH >= 6.5).astype(int)
complete = df[['LBXGH'] + cbc_vars].notna().all(axis=1)
adult = df.RIDAGEYR >= 20
no_dx = df.DIQ010.eq(2)
no_meds = ~df.DIQ050.eq(1) & ~df.DIQ070.eq(1)
# Missing medication answers are skips/unknown, not proof of no medication.
# Pregnancy data are public only for females aged 20–44. Outside that band,
# absence of a pregnancy record must not be described as confirmed nonpregnant.
preg_band = df.RIAGENDR.eq(2) & df.RIDAGEYR.between(20, 44)
preg_ok = ~df.RIDEXPRG.eq(1) & (~preg_band | df.RIDEXPRG.eq(2))
eligible = df.RIDSTATR.eq(2) & df.WTPH2YR.gt(0)

flow = []
mask = pd.Series(True, index=df.index)
for label, condition in [
    ('All interviewed participants', mask.copy()),
    ('Examined, positive phlebotomy weight', eligible),
    ('Age 20+', adult),
    ('Explicit no prior diagnosis (DIQ010=2)', no_dx),
    ('No reported current insulin/diabetes pills', no_meds),
    ('Exclude recorded pregnancy and indeterminate pregnancy in females 20–44', preg_ok),
    ('Observed HbA1c and complete 12-variable CBC', complete),
]:
    before = int(mask.sum())
    mask &= condition
    flow.append(dict(step=label, n=int(mask.sum()), excluded=before-int(mask.sum()),
                     positives=int(df.loc[mask & df.LBXGH.notna(), 'target'].sum())))
primary = mask.copy()
pd.DataFrame(flow).to_csv(OUT / 'cohort_flow.csv', index=False)

cohorts = {
    'reference_all_ages': complete,
    'adults20_all_diagnoses': complete & adult & eligible & preg_ok,
    'primary_adults20_no_diagnosis': primary,
    'sensitivity_age18_no_diagnosis': complete & (df.RIDAGEYR >= 18) & eligible & no_dx & no_meds & preg_ok,
    'sensitivity_age35_70_no_diagnosis': primary & df.RIDAGEYR.between(35, 70),
    'sensitivity_age65plus_no_diagnosis': primary & (df.RIDAGEYR >= 65),
    'sensitivity_include_borderline': complete & adult & eligible & preg_ok & no_meds & df.DIQ010.isin([2, 3]),
}
summary = []
for name, keep in cohorts.items():
    d = df.loc[keep]
    pos = d.target.eq(1)
    summary.append(dict(cohort=name, n=len(d), positives=int(pos.sum()), prevalence=d.target.mean(),
                        known_diagnosis_positives=int((pos & d.DIQ010.eq(1)).sum()),
                        fraction_positives_known=(pos & d.DIQ010.eq(1)).sum()/pos.sum() if pos.sum() else np.nan,
                        females_pregnancy_status_not_public=int((d.RIAGENDR.eq(2) & ~d.RIDAGEYR.between(20,44)).sum()),
                        weighted_prevalence=np.average(d.target, weights=d.WTPH2YR) if d.WTPH2YR.gt(0).all() else np.nan))
summary = pd.DataFrame(summary)
summary.to_csv(OUT / 'cohort_summary.csv', index=False)
diagnosis_table = pd.crosstab(df.loc[complete & adult, 'diagnosis_status'], df.loc[complete & adult, 'target'])
diagnosis_table.to_csv(OUT / 'adult_diagnosis_counts.csv')
assert (df.loc[primary, 'DIQ010'] == 2).all()
assert not df.loc[primary, 'RIDEXPRG'].eq(1).any()
print(pd.DataFrame(flow).to_string(index=False))
print(summary.round(4).to_string(index=False))
print('Adult diagnosis strata (columns: HbA1c below/at least 6.5%):\n', diagnosis_table)

# %%
# Identical folds across models within each cohort; folds differ across cohorts.
# All preprocessing is refitted inside each training fold. Diagnosis, medication,
# pregnancy, weight, and HbA1c variables never enter the predictor matrix.
def make_model(nums, cats, forest=False):
    transforms = [('numeric', Pipeline([('impute', SimpleImputer(strategy='median')),
                                        ('scale', StandardScaler())]), nums)]
    if cats:
        transforms.append(('categorical', Pipeline([
            ('impute', SimpleImputer(strategy='most_frequent')),
            ('encode', OneHotEncoder(handle_unknown='ignore', sparse_output=False))]), cats))
    clf = (RandomForestClassifier(n_estimators=300, min_samples_leaf=5,
                                  class_weight='balanced', random_state=42, n_jobs=1)
           if forest else LogisticRegression(class_weight='balanced', solver='liblinear', max_iter=2000))
    # Sparse logistic input avoids dense BLAS matmul warnings on this macOS/NumPy
    # environment. This changes storage, not features or their numeric values.
    steps = [('preprocess', ColumnTransformer(transforms))]
    if not forest:
        steps.append(('sparse_storage', FunctionTransformer(csr_matrix, accept_sparse=True)))
    return Pipeline(steps + [('classifier', clf)])

specs = {'age_logistic': (['RIDAGEYR'], [], False),
         'demographics_logistic': (numeric, categorical, False),
         'cbc_demographics_logistic': (numeric + cbc_vars, categorical, False),
         'cbc_demographics_forest': (numeric + cbc_vars, categorical, True)}
metrics, thresholds, predictions, fold_metrics = [], [], [], []
primary_curves = {}
for name, keep in cohorts.items():
    d = df.loc[keep].reset_index(drop=True)
    y = d.target.to_numpy()
    assert min(np.bincount(y, minlength=2)) >= 5, name
    folds = list(StratifiedKFold(n_splits=5, shuffle=True, random_state=42).split(d, y))
    for model_name, (nums, cats, forest) in specs.items():
        scores = np.full(len(d), np.nan)
        fold_ids = np.zeros(len(d), dtype=int)
        for fold_id, (train, test) in enumerate(folds, 1):
            model = make_model(nums, cats, forest)
            model.fit(d.iloc[train][nums + cats], y[train])
            scores[test] = model.predict_proba(d.iloc[test][nums + cats])[:, 1]
            fold_ids[test] = fold_id
            fold_metrics.append(dict(cohort=name, model=model_name, fold=fold_id,
                                     n=len(test), positives=int(y[test].sum()), AUROC=roc_auc_score(y[test], scores[test])))
        assert np.isfinite(scores).all() and (fold_ids > 0).all()
        metrics.append(dict(cohort=name, model=model_name, n=len(d), positives=int(y.sum()),
                            AUROC=roc_auc_score(y, scores), average_precision=average_precision_score(y, scores),
                            prevalence=y.mean()))
        predictions.append(pd.DataFrame(dict(cohort=name, model=model_name, SEQN=d.SEQN.astype(int),
                                             target=y, fold=fold_ids, score=scores)))
        for threshold in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
            tn, fp, fn, tp = confusion_matrix(y, scores >= threshold, labels=[0, 1]).ravel()
            assert tn + fp + fn + tp == len(d) and tp + fn == y.sum()
            thresholds.append(dict(cohort=name, model=model_name, threshold=threshold,
                sensitivity=tp/(tp+fn), specificity=tn/(tn+fp),
                NPV=tn/(tn+fn) if tn+fn else np.nan, PPV=tp/(tp+fp) if tp+fp else np.nan,
                n_flagged=int(tp+fp), n_deferred=int(tn+fn), positives_missed=int(fn)))
        if name == 'primary_adults20_no_diagnosis':
            primary_curves[model_name] = (y, scores)
    print('Completed:', name, flush=True)
metrics = pd.DataFrame(metrics)
metrics.to_csv(OUT / 'cohort_model_comparison.csv', index=False)
pd.DataFrame(fold_metrics).to_csv(OUT / 'cohort_fold_metrics.csv', index=False)
pd.DataFrame(thresholds).to_csv(OUT / 'cohort_threshold_comparison.csv', index=False)
pd.concat(predictions, ignore_index=True).to_csv(OUT / 'cohort_oof_predictions.csv', index=False)
print(metrics.round(4).to_string(index=False))

# %%
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(summary.cohort, summary.prevalence * 100)
ax.set_xlabel('Observed diabetes-range HbA1c (%) — unweighted')
fig.tight_layout()
fig.savefig(OUT / 'cohort_prevalence.png', dpi=160)
plt.close(fig)
fig, ax = plt.subplots(figsize=(7, 6))
for name, (y, scores) in primary_curves.items():
    fpr, tpr, _ = roc_curve(y, scores)
    ax.plot(fpr, tpr, label=f'{name}: {roc_auc_score(y, scores):.3f}')
ax.plot([0, 1], [0, 1], 'k--')
ax.set(xlabel='False positive rate', ylabel='Sensitivity', title='Primary cohort: exploratory out-of-fold ROC')
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT / 'primary_cohort_roc.png', dpi=160)
plt.close(fig)
print('Exports:', OUT)
