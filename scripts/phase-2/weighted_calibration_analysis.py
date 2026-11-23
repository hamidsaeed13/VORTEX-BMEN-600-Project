"""Phase 2: weighted_calibration_analysis.py, run under both the INITIAL
(21 CBC + income) and REDUCED (9 CBC, no income) feature-set variants from
study_config.py.

Same nested PSU-grouped validation, development-only sigmoid calibration and
conditional jackknife as scripts/analysis/weighted_calibration_analysis.py --
that script is untouched and still represents the INITIAL variant alone for
the rest of the pipeline.

Run: python scripts/phase-2/weighted_calibration_analysis.py
Outputs:
  results/phase-2/weighted_calibration/initial/   -- same contents as results/weighted_calibration/
  results/phase-2/weighted_calibration/reduced/   -- same analysis, REDUCED feature set
  results/phase-2/weighted_calibration/comparison/ -- merged tables + labeled figures
"""
from pathlib import Path
import sys
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from scipy.special import logit
from scipy.stats import t as student_t
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import roc_auc_score, average_precision_score, confusion_matrix, log_loss

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/analysis'))
import study_config as cfg

RAW = ROOT / 'data/raw/2021_2023'
BASE_OUT = ROOT / 'results/phase-2/weighted_calibration'


def read(name):
    d = pd.read_sas(RAW / f'{name}_L.xpt', format='xport')
    assert d.SEQN.is_unique
    for c in d.select_dtypes(include='number'):
        d.loc[d[c].abs().lt(1e-70), c] = 0.
    return d


def make_model(nums, cats, forest):
    transform = [('num', Pipeline([('impute', SimpleImputer(strategy='median')),
                                  ('scale', StandardScaler())]), nums)]
    if cats:
        transform += cfg.categorical_transformer_entries()
    steps = [('pre', ColumnTransformer(transform))]
    if not forest:
        steps.append(('sparse', FunctionTransformer(csr_matrix, accept_sparse=True)))
    clf = (RandomForestClassifier(n_estimators=300, min_samples_leaf=5, random_state=42, n_jobs=1)
           if forest else LogisticRegression(solver='liblinear', max_iter=2000))
    return Pipeline(steps + [('clf', clf)])


def logits(scores):
    return csr_matrix(logit(np.clip(scores, 1e-6, 1 - 1e-6)).reshape(-1, 1))


def choose_threshold(labels, scores, weights, sensitivity_goal=.95):
    positive_scores = scores[labels == 1]
    positive_weights = weights[labels == 1]
    order = np.argsort(-positive_scores, kind='stable')
    cumulative = np.cumsum(positive_weights[order]) / positive_weights.sum()
    return float(positive_scores[order][np.flatnonzero(cumulative >= sensitivity_goal)[0]])


def evaluate(g, weights, stage):
    labels = g.target.to_numpy()
    scores = g[stage].to_numpy()
    average = lambda a: np.average(a, weights=weights)
    return dict(AUROC=roc_auc_score(labels, scores, sample_weight=weights),
        average_precision=average_precision_score(labels, scores, sample_weight=weights),
        Brier=average((labels - scores) ** 2), log_loss=log_loss(labels, scores, sample_weight=weights, labels=[0, 1]),
        mean_prediction=average(scores), prevalence=average(labels))


def policy(g, weights):
    labels, flag = g.target.to_numpy(), g.flagged.to_numpy()
    tn, fp, fn, tp = confusion_matrix(labels, flag, sample_weight=weights, labels=[0, 1]).ravel()
    return dict(sensitivity=tp / (tp + fn), specificity=tn / (tn + fp),
                NPV=tn / (tn + fn) if tn + fn else np.nan,
                PPV=tp / (tp + fp) if tp + fp else np.nan,
                deferred_fraction=(tn + fn) / (tn + fp + fn + tp))


def run_variant(variant):
    spec = cfg.FEATURE_SET_VARIANTS[variant]
    CBC, NUM, CAT = spec['cbc_features'], spec['numeric_demographics'], cfg.CATEGORICAL_DEMOGRAPHICS
    out = BASE_OUT / variant
    out.mkdir(parents=True, exist_ok=True)

    demo, cbc, ghb, diq = [read(n) for n in ['DEMO', 'CBC', 'GHB', 'DIQ']]
    full = demo.merge(ghb[['SEQN', 'WTPH2YR', 'LBXGH']], on='SEQN', how='left', validate='one_to_one')
    full = full.merge(cbc[['SEQN'] + CBC], on='SEQN', how='left', validate='one_to_one')
    full = full.merge(diq[['SEQN', 'DIQ010', 'DIQ050', 'DIQ070']], on='SEQN', how='left', validate='one_to_one')
    assert len(full) == len(demo)
    full['DMDEDUC2'] = full.DMDEDUC2.replace({7: np.nan, 9: np.nan})
    keep = cfg.eligibility_mask(full) & full[['LBXGH'] + CBC].notna().all(axis=1)
    d = full.loc[keep].reset_index(drop=True)
    y = d.LBXGH.ge(cfg.PRIMARY_CUT).astype(int).to_numpy()
    w = d.WTPH2YR.to_numpy()
    if variant == 'initial':
        assert len(d) == 4612 and y.sum() == 106  # must exactly match the official pipeline
        previous = ROOT / 'results/cohort/cohort_oof_predictions.csv'
        if previous.exists():
            old = pd.read_csv(previous)
            assert set(old.loc[old.cohort.eq('primary_adults20_no_diagnosis'), 'SEQN']) == set(d.SEQN)
    # Cross-check against this same Phase 2 run's own cohort_analysis.py output, for both
    # variants (the official pipeline only has an 'initial' cohort file to check against above).
    phase2_cohort = ROOT / f'results/phase-2/cohort_analysis/{variant}/cohort_oof_predictions.csv'
    if phase2_cohort.exists():
        other = pd.read_csv(phase2_cohort)
        assert set(other.loc[other.cohort.eq('primary_adults20_no_diagnosis'), 'SEQN']) == set(d.SEQN)
    assert np.isfinite(w).all() and (w > 0).all()
    assert d[['SDMVSTRA', 'SDMVPSU']].notna().all().all()
    groups = (d.SDMVSTRA.astype(int).astype(str) + ':' + d.SDMVPSU.astype(int).astype(str)).to_numpy()
    design = full.loc[full.WTPH2YR.gt(0), ['SDMVSTRA', 'SDMVPSU']].drop_duplicates()
    assert design.notna().all().all()
    strata = {int(h): sorted(g.SDMVPSU.astype(int).tolist()) for h, g in design.groupby('SDMVSTRA')}
    assert all(len(psus) >= 2 for psus in strata.values())
    design.to_csv(out / 'full_design_psus.csv', index=False)
    print(f'[{variant}] Fixed cohort: {len(d)} participants, {y.sum()} positives; '
          f'{len(strata)} strata, {len(design)} PSUs, {len(CBC)} CBC features', flush=True)

    def fit_model(train, nums, cats, forest):
        model = make_model(nums, cats, forest)
        train_w = w[train] / w[train].mean()
        model.fit(d.iloc[train][nums + cats], y[train], clf__sample_weight=train_w)
        return model

    specs = {'age_logistic': (['RIDAGEYR'], [], False),
             'demographics_logistic': (NUM, CAT, False),
             'cbc_demographics_logistic': (NUM + CBC, CAT, False),
             'cbc_demographics_forest': (NUM + CBC, CAT, True)}
    outer = list(StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42).split(d, y, groups))
    records, fold_records, audits = [], [], []
    for fold, (train, test) in enumerate(outer, 1):
        assert not set(groups[train]) & set(groups[test])
        assert len(np.unique(y[train])) == len(np.unique(y[test])) == 2
        inner = list(StratifiedGroupKFold(n_splits=3, shuffle=True, random_state=420 + fold).split(d.iloc[train], y[train], groups[train]))
        for name, (nums, cats, forest) in specs.items():
            development_scores = np.full(len(train), np.nan)
            for inner_fold, (a, b) in enumerate(inner, 1):
                a, b = train[a], train[b]
                assert not set(groups[a]) & (set(groups[b]) | set(groups[test]))
                assert len(np.unique(y[a])) == len(np.unique(y[b])) == 2
                model = fit_model(a, nums, cats, forest)
                locations = pd.Index(train).get_indexer(b)
                development_scores[locations] = model.predict_proba(d.iloc[b][nums + cats])[:, 1]
                audits.append(dict(model=name, outer_fold=fold, inner_fold=inner_fold,
                                   train_n=len(a), validation_n=len(b), train_positive=int(y[a].sum()),
                                   validation_positive=int(y[b].sum()), cluster_overlap=0))
            assert np.isfinite(development_scores).all()
            calibrator = LogisticRegression(solver='liblinear', C=1e6, max_iter=2000)
            calibrator.fit(logits(development_scores), y[train], sample_weight=w[train] / w[train].mean())
            calibrated_development = calibrator.predict_proba(logits(development_scores))[:, 1]
            threshold = choose_threshold(y[train], calibrated_development, w[train])
            model = fit_model(train, nums, cats, forest)
            raw = model.predict_proba(d.iloc[test][nums + cats])[:, 1]
            calibrated = calibrator.predict_proba(logits(raw))[:, 1]
            baseline = np.average(y[train], weights=w[train])
            records.append(pd.DataFrame(dict(SEQN=d.iloc[test].SEQN.astype(int), model=name, fold=fold,
                target=y[test], weight=w[test], stratum=d.iloc[test].SDMVSTRA.astype(int),
                psu=d.iloc[test].SDMVPSU.astype(int), raw=raw, calibrated=calibrated,
                train_prevalence=baseline, development_threshold=threshold, flagged=calibrated >= threshold)))
            fold_records.append(dict(model=name, fold=fold, train_n=len(train), test_n=len(test),
                test_positives=int(y[test].sum()), train_prevalence=baseline,
                threshold=threshold, sigmoid_slope=float(calibrator.coef_[0, 0]),
                sigmoid_intercept=float(calibrator.intercept_[0]),
                weighted_auroc=roc_auc_score(y[test], calibrated, sample_weight=w[test])))
        print(f'[{variant}] Finished outer fold {fold}', flush=True)
    pred = pd.concat(records, ignore_index=True)
    assert not pred.duplicated(['SEQN', 'model']).any()
    assert pred.groupby('model').size().eq(len(d)).all()
    assert np.isfinite(pred[['raw', 'calibrated', 'development_threshold']]).all().all()
    pred.to_csv(out / 'weighted_oof_predictions.csv', index=False)
    pd.DataFrame(fold_records).to_csv(out / 'weighted_fold_metrics.csv', index=False)
    pd.DataFrame(audits).to_csv(out / 'split_audit.csv', index=False)

    def replicate_weights(g):
        base = g.weight.to_numpy()
        for h, psus in strata.items():
            m = len(psus)
            for psu in psus:
                rw = base.copy()
                in_h = g.stratum.eq(h).to_numpy()
                dropped = in_h & g.psu.eq(psu).to_numpy()
                rw[in_h] *= m / (m - 1)
                rw[dropped] = 0
                yield h, psu, rw

    point_rows, replicate_rows, policy_rows, calibration_rows = [], [], [], []
    for name, group in pred.groupby('model'):
        g = group.sort_values('SEQN').reset_index(drop=True)
        for stage in ['raw', 'calibrated', 'train_prevalence']:
            values = evaluate(g, g.weight.to_numpy(), stage)
            point_rows.extend(dict(model=name, stage=stage, metric=k, estimate=v) for k, v in values.items())
            for h, psu, rw in replicate_weights(g):
                replicate_rows.extend(dict(model=name, stage=stage, stratum=h, deleted_psu=psu, metric=k, estimate=v)
                                      for k, v in evaluate(g, rw, stage).items())
        pv = policy(g, g.weight.to_numpy())
        policy_rows.append(dict(model=name, **pv, n_flagged=int(g.flagged.sum()),
            n_deferred=int((~g.flagged).sum()), positives_missed=int((g.target.eq(1) & ~g.flagged).sum()),
            total_positives=int(g.target.sum()), n=len(g)))
        point_rows.extend(dict(model=name, stage='development_policy', metric=k, estimate=v) for k, v in pv.items())
        for h, psu, rw in replicate_weights(g):
            replicate_rows.extend(dict(model=name, stage='development_policy', stratum=h, deleted_psu=psu, metric=k, estimate=v)
                                  for k, v in policy(g, rw).items())
        for stage in ['raw', 'calibrated']:
            ordered = g.sort_values(stage).copy()
            midpoint = (ordered.weight.cumsum() - ordered.weight / 2) / ordered.weight.sum()
            ordered['bin'] = np.minimum((midpoint * 5).astype(int), 4)
            for bin_id, b in ordered.groupby('bin'):
                calibration_rows.append(dict(model=name, stage=stage, bin=int(bin_id), n=len(b),
                    positives=int(b.target.sum()), weight_sum=b.weight.sum(),
                    mean_prediction=np.average(b[stage], weights=b.weight),
                    observed_fraction=np.average(b.target, weights=b.weight)))
    points, reps = pd.DataFrame(point_rows), pd.DataFrame(replicate_rows)
    degrees_freedom = len(design) - len(strata)
    critical = student_t.ppf(.975, degrees_freedom)

    def jackknife_se(rows):
        variance = 0.
        for h, z in rows.groupby('stratum'):
            m = len(strata[int(h)])
            assert len(z) == m
            variance += (m - 1) / m * ((z.estimate - z.estimate.mean()) ** 2).sum()
        return np.sqrt(variance)

    for i, r in points.iterrows():
        rr = reps[reps.model.eq(r.model) & reps.stage.eq(r.stage) & reps.metric.eq(r.metric)]
        se = jackknife_se(rr)
        points.loc[i, 'conditional_design_SE'] = se
        points.loc[i, 'lower_95'] = max(0, r.estimate - critical * se)
        points.loc[i, 'upper_95'] = min(1, r.estimate + critical * se) if r.metric != 'log_loss' else r.estimate + critical * se
        points.loc[i, 'design_df'] = degrees_freedom
    paired = []
    for stage in ['raw', 'calibrated']:
        for metric in ['AUROC', 'average_precision', 'Brier']:
            a = reps[reps.model.eq('cbc_demographics_logistic') & reps.stage.eq(stage) & reps.metric.eq(metric)]
            b = reps[reps.model.eq('demographics_logistic') & reps.stage.eq(stage) & reps.metric.eq(metric)]
            delta = a.merge(b, on=['stratum', 'deleted_psu'], suffixes=('_a', '_b'))
            delta['estimate'] = delta.estimate_a - delta.estimate_b
            pa = points[points.model.eq('cbc_demographics_logistic') & points.stage.eq(stage) & points.metric.eq(metric)].estimate.iloc[0]
            pb = points[points.model.eq('demographics_logistic') & points.stage.eq(stage) & points.metric.eq(metric)].estimate.iloc[0]
            se = jackknife_se(delta)
            paired.append(dict(stage=stage, metric=metric, CBC_minus_demographics=pa - pb,
                               conditional_design_SE=se, lower_95=pa - pb - critical * se, upper_95=pa - pb + critical * se))
    points.to_csv(out / 'weighted_metrics_intervals.csv', index=False)
    reps.to_csv(out / 'conditional_jackknife_replicates.csv', index=False)
    pd.DataFrame(paired).to_csv(out / 'paired_cbc_gain.csv', index=False)
    pd.DataFrame(policy_rows).to_csv(out / 'development_policy_evaluation.csv', index=False)
    calibration = pd.DataFrame(calibration_rows)
    calibration.to_csv(out / 'weighted_calibration_bins.csv', index=False)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, stage in zip(axes, ['raw', 'calibrated']):
        for name, g in calibration[calibration.stage.eq(stage)].groupby('model'):
            ax.plot(g.mean_prediction, g.observed_fraction, 'o-', label=name)
        ax.plot([0, .15], [0, .15], 'k--', label='Perfect calibration')
        ax.set(xlabel='Weighted mean predicted risk', ylabel='Weighted observed fraction', title=stage)
        ax.legend(fontsize=7, title='Model')
    fig.suptitle(f'{spec["label"]}: outer held-out calibration (five weighted equal-mass bins)')
    fig.tight_layout()
    fig.savefig(out / 'weighted_calibration.png', dpi=160)
    plt.close(fig)

    metadata = dict(variant=variant, label=spec['label'], n=len(d), positives=int(y.sum()),
        n_cbc_features=len(CBC), weighted_prevalence=float(np.average(y, weights=w)),
        strata=len(strata), psus=len(design), design_df=degrees_freedom, outer_folds=5, inner_folds=3, seed=42)
    (out / 'analysis_metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
    cal_points = points[points.stage.eq('calibrated')].copy()
    cal_points['variant'] = variant
    return dict(cal_points=cal_points, policy=pd.DataFrame(policy_rows).assign(variant=variant), metadata=metadata)


def compare(results):
    out = BASE_OUT / 'comparison'
    out.mkdir(parents=True, exist_ok=True)
    labels = {v: cfg.FEATURE_SET_VARIANTS[v]['label'] for v in results}

    auroc = pd.concat([results[v]['cal_points'][results[v]['cal_points'].metric.eq('AUROC')] for v in results], ignore_index=True)
    auroc['variant_label'] = auroc.variant.map(labels)
    pivot = auroc.pivot(index='model', columns='variant_label', values='estimate')
    pivot['AUROC_delta_reduced_minus_initial'] = pivot[labels['reduced']] - pivot[labels['initial']]
    pivot.to_csv(out / 'calibrated_auroc_comparison.csv')

    policy = pd.concat([results[v]['policy'] for v in results], ignore_index=True)
    policy['variant_label'] = policy.variant.map(labels)
    policy.to_csv(out / 'development_policy_comparison.csv', index=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    models = pivot.index.tolist()
    x = np.arange(len(models))
    width = 0.35
    ax.bar(x - width / 2, pivot[labels['initial']], width, label=labels['initial'], color='#3478a6')
    ax.bar(x + width / 2, pivot[labels['reduced']], width, label=labels['reduced'], color='#d55e00')
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=20, ha='right', fontsize=8)
    ax.set_ylabel('Calibrated weighted AUROC (5 outer PSU-grouped folds)')
    ax.set_title('weighted_calibration_analysis.py: initial vs. reduced feature set')
    ax.legend(title='Feature set', fontsize=8)
    fig.tight_layout()
    fig.savefig(out / 'calibrated_auroc_comparison.png', dpi=160)
    plt.close(fig)

    metadata_both = {v: results[v]['metadata'] for v in results}
    (out / 'comparison_metadata.json').write_text(json.dumps(metadata_both, indent=2) + '\n')

    print('\n=== Comparison: calibrated weighted AUROC, initial vs. reduced ===')
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
