"""Phase 2: cohort_analysis.py, run under both the INITIAL (21 CBC + income) and
REDUCED (9 CBC, no income) feature-set variants from study_config.py, so we can
see where the project started and where the Phase 15 reduction work landed.

This is a copy of scripts/analysis/cohort_analysis.py (kept byte-for-byte
equivalent in its modeling logic -- same folds, same preprocessing, same
cohorts) parameterized by `variant`. The original script is untouched and
still represents the INITIAL variant alone for the rest of the pipeline.

Run: python scripts/phase-2/cohort_analysis.py
Outputs:
  results/phase-2/cohort_analysis/initial/   -- same contents as results/cohort/
  results/phase-2/cohort_analysis/reduced/   -- same analysis, REDUCED feature set
  results/phase-2/cohort_analysis/comparison/ -- merged tables + labeled figures
"""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from scipy.sparse import csr_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, average_precision_score, confusion_matrix, roc_curve

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/analysis'))
import study_config as cfg

RAW = ROOT / 'data/raw/2021_2023'
BASE_OUT = ROOT / 'results/phase-2/cohort_analysis'


def load(name):
    frame = pd.read_sas(RAW / (name + '_L.xpt'), format='xport')
    assert frame.SEQN.is_unique, name
    for col in frame.select_dtypes(include='number'):
        frame.loc[frame[col].abs().lt(1e-70), col] = 0.0
    return frame


def make_model(nums, cats, forest=False):
    transforms = [('numeric', Pipeline([('impute', SimpleImputer(strategy='median')),
                                        ('scale', StandardScaler())]), nums)]
    if cats:
        transforms += cfg.categorical_transformer_entries()
    clf = (RandomForestClassifier(n_estimators=300, min_samples_leaf=5,
                                  class_weight='balanced', random_state=42, n_jobs=1)
           if forest else LogisticRegression(class_weight='balanced', solver='liblinear', max_iter=2000))
    steps = [('preprocess', ColumnTransformer(transforms))]
    if not forest:
        steps.append(('sparse_storage', FunctionTransformer(csr_matrix, accept_sparse=True)))
    return Pipeline(steps + [('classifier', clf)])


def run_variant(variant):
    spec = cfg.FEATURE_SET_VARIANTS[variant]
    cbc_vars = spec['cbc_features']
    numeric = spec['numeric_demographics']
    categorical = cfg.CATEGORICAL_DEMOGRAPHICS
    out = BASE_OUT / variant
    out.mkdir(parents=True, exist_ok=True)

    demo, cbc, ghb, diq = [load(name) for name in ['DEMO', 'CBC', 'GHB', 'DIQ']]
    df = demo.merge(cbc[['SEQN'] + cbc_vars], on='SEQN', how='left', validate='one_to_one')
    df = df.merge(ghb[['SEQN', 'LBXGH', 'WTPH2YR']], on='SEQN', how='left', validate='one_to_one')
    df = df.merge(diq[['SEQN', 'DIQ010', 'DIQ050', 'DIQ070']], on='SEQN', how='left', validate='one_to_one')
    assert len(df) == len(demo)
    df['DMDEDUC2'] = df.DMDEDUC2.replace({7: np.nan, 9: np.nan})
    df['diagnosis_status'] = df.DIQ010.map({1: 'yes', 2: 'no', 3: 'borderline', 7: 'refused', 9: 'unknown'}).fillna('missing')
    df['target'] = (df.LBXGH >= cfg.PRIMARY_CUT).astype(int)
    complete = df[['LBXGH'] + cbc_vars].notna().all(axis=1)
    adult = df.RIDAGEYR >= cfg.MIN_AGE
    no_dx = df.DIQ010.eq(cfg.NO_PRIOR_DIAGNOSIS_CODE)
    no_meds = ~df.DIQ050.eq(1) & ~df.DIQ070.eq(1)
    preg_band = df.RIAGENDR.eq(cfg.PREGNANCY_BAND_SEX) & df.RIDAGEYR.between(*cfg.PREGNANCY_BAND_AGE)
    preg_ok = ~df.RIDEXPRG.eq(1) & (~preg_band | df.RIDEXPRG.eq(2))
    eligible = df.RIDSTATR.eq(cfg.REQUIRE_EXAM_STATUS) & df.WTPH2YR.gt(0)

    flow = []
    mask = pd.Series(True, index=df.index)
    for label, condition in [
        ('All interviewed participants', mask.copy()),
        ('Examined, positive phlebotomy weight', eligible),
        ('Age 20+', adult),
        ('Explicit no prior diagnosis (DIQ010=2)', no_dx),
        ('No reported current insulin/diabetes pills', no_meds),
        ('Exclude recorded pregnancy and indeterminate pregnancy in females 20–44', preg_ok),
        (f'Observed HbA1c and complete {len(cbc_vars)}-variable CBC ({variant})', complete),
    ]:
        before = int(mask.sum())
        mask &= condition
        flow.append(dict(step=label, n=int(mask.sum()), excluded=before - int(mask.sum()),
                         positives=int(df.loc[mask & df.LBXGH.notna(), 'target'].sum())))
    primary = mask.copy()
    pd.DataFrame(flow).to_csv(out / 'cohort_flow.csv', index=False)

    cohorts = {
        'reference_all_ages': complete,
        'adults20_all_diagnoses': complete & adult & eligible & preg_ok,
        'primary_adults20_no_diagnosis': primary,
        'sensitivity_age18_no_diagnosis': complete & (df.RIDAGEYR >= 18) & eligible & no_dx & no_meds & preg_ok,
        'sensitivity_age35_70_no_diagnosis': primary & df.RIDAGEYR.between(35, 70),
        'sensitivity_age65plus_no_diagnosis': primary & (df.RIDAGEYR >= 65),
        'sensitivity_include_borderline': complete & adult & eligible & preg_ok & no_meds
            & df.DIQ010.isin([cfg.NO_PRIOR_DIAGNOSIS_CODE, cfg.BORDERLINE_DIAGNOSIS_CODE]),
    }
    summary = []
    for name, keep in cohorts.items():
        d = df.loc[keep]
        pos = d.target.eq(1)
        summary.append(dict(cohort=name, n=len(d), positives=int(pos.sum()), prevalence=d.target.mean(),
                            known_diagnosis_positives=int((pos & d.DIQ010.eq(1)).sum()),
                            fraction_positives_known=(pos & d.DIQ010.eq(1)).sum() / pos.sum() if pos.sum() else np.nan,
                            females_pregnancy_status_not_public=int((d.RIAGENDR.eq(2) & ~d.RIDAGEYR.between(20, 44)).sum()),
                            weighted_prevalence=np.average(d.target, weights=d.WTPH2YR) if d.WTPH2YR.gt(0).all() else np.nan))
    summary = pd.DataFrame(summary)
    summary.to_csv(out / 'cohort_summary.csv', index=False)
    diagnosis_table = pd.crosstab(df.loc[complete & adult, 'diagnosis_status'], df.loc[complete & adult, 'target'])
    diagnosis_table.to_csv(out / 'adult_diagnosis_counts.csv')
    assert (df.loc[primary, 'DIQ010'] == 2).all()
    assert not df.loc[primary, 'RIDEXPRG'].eq(1).any()
    print(f'[{variant}]', pd.DataFrame(flow).to_string(index=False))
    print(f'[{variant}]', summary.round(4).to_string(index=False))

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
                    sensitivity=tp / (tp + fn), specificity=tn / (tn + fp),
                    NPV=tn / (tn + fn) if tn + fn else np.nan, PPV=tp / (tp + fp) if tp + fp else np.nan,
                    n_flagged=int(tp + fp), n_deferred=int(tn + fn), positives_missed=int(fn)))
            if name == 'primary_adults20_no_diagnosis':
                primary_curves[model_name] = (y, scores)
        print(f'[{variant}] Completed:', name, flush=True)
    metrics = pd.DataFrame(metrics)
    metrics.to_csv(out / 'cohort_model_comparison.csv', index=False)
    pd.DataFrame(fold_metrics).to_csv(out / 'cohort_fold_metrics.csv', index=False)
    pd.DataFrame(thresholds).to_csv(out / 'cohort_threshold_comparison.csv', index=False)
    pd.concat(predictions, ignore_index=True).to_csv(out / 'cohort_oof_predictions.csv', index=False)
    print(f'[{variant}]', metrics.round(4).to_string(index=False))

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(summary.cohort, summary.prevalence * 100)
    ax.set_xlabel('Observed diabetes-range HbA1c (%) — unweighted')
    ax.set_title(f'{spec["label"]}: cohort prevalence')
    fig.tight_layout()
    fig.savefig(out / 'cohort_prevalence.png', dpi=160)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 6))
    for name, (y, scores) in primary_curves.items():
        fpr, tpr, _ = roc_curve(y, scores)
        ax.plot(fpr, tpr, label=f'{name}: {roc_auc_score(y, scores):.3f}')
    ax.plot([0, 1], [0, 1], 'k--', label='Chance')
    ax.set(xlabel='False positive rate', ylabel='Sensitivity',
           title=f'{spec["label"]}: primary cohort out-of-fold ROC')
    ax.legend(fontsize=8, title=spec['label'])
    fig.tight_layout()
    fig.savefig(out / 'primary_cohort_roc.png', dpi=160)
    plt.close(fig)
    return dict(flow=pd.DataFrame(flow), summary=summary, metrics=metrics, n_cbc_features=len(cbc_vars))


def compare(results):
    out = BASE_OUT / 'comparison'
    out.mkdir(parents=True, exist_ok=True)
    labels = {v: cfg.FEATURE_SET_VARIANTS[v]['label'] for v in results}

    merged = pd.concat([results[v]['metrics'].assign(variant=v, variant_label=labels[v]) for v in results], ignore_index=True)
    merged.to_csv(out / 'model_comparison_both_variants.csv', index=False)

    primary = merged[merged.cohort.eq('primary_adults20_no_diagnosis')]
    pivot = primary.pivot(index='model', columns='variant_label', values='AUROC')
    pivot['AUROC_delta_reduced_minus_initial'] = pivot[labels['reduced']] - pivot[labels['initial']]
    pivot.to_csv(out / 'primary_cohort_auroc_comparison.csv')

    fig, ax = plt.subplots(figsize=(9, 5))
    models = pivot.index.tolist()
    x = np.arange(len(models))
    width = 0.35
    ax.bar(x - width / 2, pivot[labels['initial']], width, label=labels['initial'], color='#3478a6')
    ax.bar(x + width / 2, pivot[labels['reduced']], width, label=labels['reduced'], color='#d55e00')
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=20, ha='right', fontsize=8)
    ax.set_ylabel('AUROC (primary cohort, unweighted 5-fold OOF)')
    ax.set_title('cohort_analysis.py: initial vs. reduced feature set')
    ax.legend(title='Feature set', fontsize=8)
    fig.tight_layout()
    fig.savefig(out / 'primary_cohort_auroc_comparison.png', dpi=160)
    plt.close(fig)

    print('\n=== Comparison: primary cohort AUROC, initial vs. reduced ===')
    print(pivot.round(4).to_string())
    return pivot


def main():
    BASE_OUT.mkdir(parents=True, exist_ok=True)
    results = {variant: run_variant(variant) for variant in cfg.FEATURE_SET_VARIANTS}
    compare(results)
    print('\nOutputs:')
    for variant in results:
        print(f'  {variant}: {BASE_OUT / variant}')
    print(f'  comparison: {BASE_OUT / "comparison"}')


if __name__ == '__main__':
    main()
