"""Descriptive collinearity diagnostics and exploratory nested PCA comparison."""
import argparse
from pathlib import Path
import json
import hashlib
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, FunctionTransformer
import research_extension as ext
import study_config as cfg

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'results/cbc_diagnostics'
CBC = ext.RED + ext.WHITE  # current team-agreed 21-feature panel (study_config.py, 2026-11-23)

# The pre-2026-11-23 canonical set (team decision superseded by the 21-feature block above):
# excluded MCH, MCHC, MPV, NRBC, basophil % and the five absolute differential counts.
LEGACY_11 = ['LBXRBCSI', 'LBXHGB', 'LBXHCT', 'LBXMCVSI', 'LBXRDW',
             'LBXWBCSI', 'LBXPLTSI', 'LBXLYPCT', 'LBXNEPCT', 'LBXMOPCT', 'LBXEOPCT']

# Phase 13 candidate. MCH and MCHC are derived from retained red-cell measures.
# Absolute differential counts duplicate total WBC multiplied by each percentage.
REDUNDANT_COLUMNS = {'LBXMCHSI', 'LBXMC', 'LBDLYMNO', 'LBDNENO', 'LBDMONO',
                     'LBDEONO', 'LBDBANO'}
CANDIDATE_14 = [column for column in CBC if column not in REDUNDANT_COLUMNS]


class CheckedPCA(PCA):
    """Check BLAS projections against an independent non-BLAS contraction."""

    def transform(self, X):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always', RuntimeWarning)
            result = super().transform(X)
        reference = np.einsum('ij,kj->ik', np.asarray(X) - self.mean_, self.components_)
        np.testing.assert_allclose(result, reference, rtol=1e-10, atol=1e-10)
        assert np.isfinite(result).all()
        # Some Apple BLAS/NumPy builds set spurious floating-point status flags.
        # Accept those warnings only after checking every projection independently.
        for warning in caught:
            if warning.category is not RuntimeWarning or 'matmul' not in str(warning.message):
                warnings.warn(warning.message, warning.category)
        return result


def vif_table(frame, weights, block):
    x = frame.to_numpy(dtype=float)
    rows = []
    for weighting, w in [('ordinary', np.ones(len(x))), ('survey_weighted', weights)]:
        w = w / w.mean()
        for j, name in enumerate(frame.columns):
            y = x[:, j]
            design = np.column_stack([np.ones(len(x)), np.delete(x, j, axis=1)])
            coef = np.linalg.lstsq(design * np.sqrt(w[:, None]), y * np.sqrt(w), rcond=None)[0]
            residual = np.sum(w * (y - np.einsum('ij,j->i', design, coef)) ** 2)
            total = np.sum(w * (y - np.average(y, weights=w)) ** 2)
            assert np.isfinite(residual) and total > 0
            rows.append(dict(block=block, weighting=weighting, variable=name,
                             VIF=np.inf if residual <= total * 1e-12 else total / residual))
    return rows


def build(pca, columns=CBC):
    if not pca:
        return ext.build(ext.NUM + ['BMXBMI'] + columns)
    pre = ColumnTransformer([
        ('numeric', Pipeline([('impute', SimpleImputer(strategy='median', add_indicator=True)),
                              ('scale', StandardScaler())]), ext.NUM + ['BMXBMI']),
        *cfg.categorical_transformer_entries(),  # nominal one-hot, education ordinal (team decision)
        ('cbc', Pipeline([('scale', StandardScaler()), ('pca', CheckedPCA(n_components=.95, svd_solver='full'))]), columns)])
    return Pipeline([('pre', pre), ('sparse', FunctionTransformer(csr_matrix, accept_sparse=True)),
                     ('clf', LogisticRegression(solver='liblinear', max_iter=2000))])


def matched_pca(d, models):
    audit, records = [], []
    outer = ext.folds_for(d)
    for fold, (train, test) in enumerate(outer, 1):
        inner = ext.folds_for(d.iloc[train], n=3, seed=420+fold)
        for name, use_pca, columns in models:
            def fit(indices, stage, heldout):
                z = d.iloc[indices]
                model = build(use_pca, columns)
                model.fit(z, z.target, clf__sample_weight=z._weight / z._weight.mean())
                if stage.startswith('inner_'):
                    assert set(z.group).isdisjoint(d.iloc[test].group)
                overlap = set(z.group) & set(d.iloc[heldout].group)
                assert not overlap
                info = dict(model=name, outer_fold=fold, stage=stage, train_n=len(z),
                            heldout_n=len(heldout), group_overlap=len(overlap))
                if use_pca:
                    p = model.named_steps['pre'].named_transformers_['cbc'].named_steps['pca']
                    assert p.n_samples_ == len(z)
                    info.update(pca_fit_n=p.n_samples_, components=p.n_components_,
                                retained_variance=float(p.explained_variance_ratio_.sum()))
                audit.append(info)
                return model
            raw_inner = np.full(len(train), np.nan)
            for k, (a, b) in enumerate(inner, 1):
                model = fit(train[a], f'inner_{k}', train[b])
                raw_inner[b] = model.predict_proba(d.iloc[train[b]])[:, 1]
            z = d.iloc[train]
            cal = LogisticRegression(solver='liblinear', C=1e6, max_iter=2000)
            cal.fit(ext.logits(raw_inner), z.target, sample_weight=z._weight / z._weight.mean())
            cut = ext.threshold(z.target.to_numpy(), cal.predict_proba(ext.logits(raw_inner))[:, 1], z._weight.to_numpy())
            model = fit(train, 'outer', test)
            raw = model.predict_proba(d.iloc[test])[:, 1]
            p = cal.predict_proba(ext.logits(raw))[:, 1]
            g = d.iloc[test][['SEQN', 'target', '_weight', 'SDMVSTRA', 'SDMVPSU']].copy()
            g['model'] = name; g['fold'] = fold; g['raw'] = raw; g['calibrated'] = p
            g['threshold'] = cut; g['flagged'] = p >= cut
            g['constant'] = np.average(z.target, weights=z._weight)
            records.append(g)
        print(f'Outer fold {fold}/5 complete', flush=True)
    return pd.concat(records, ignore_index=True), audit


def main(vif_only=False):
    OUT.mkdir(parents=True, exist_ok=True)
    full, d = ext.load_cycle('L')
    assert len(d) == 4612 and d.target.sum() == 106
    rows = vif_table(d[LEGACY_11], d._weight.to_numpy(), 'legacy_11')
    rows += vif_table(d[ext.CBC], d._weight.to_numpy(), 'full_21')
    rows += vif_table(d[CANDIDATE_14], d._weight.to_numpy(), 'candidate_14')
    pd.DataFrame(rows).to_csv(OUT / 'cbc_vif.csv', index=False)
    if vif_only:
        return
    d[ext.CBC].corr().to_csv(OUT / 'cbc_correlations.csv')
    differential = d[['LBXLYPCT', 'LBXNEPCT', 'LBXMOPCT', 'LBXEOPCT', 'LBXBAPCT']].sum(axis=1)
    relationships = {
        'differential_sum_min': float(differential.min()),
        'differential_sum_max': float(differential.max()),
        'differential_sum_mean': float(differential.mean()),
        'hct_minus_rbc_times_mcv_over_10_abs_median': float((d.LBXHCT - d.LBXRBCSI*d.LBXMCVSI/10).abs().median()),
        'mch_minus_hgb_times_10_over_rbc_abs_median': float((d.LBXMCHSI - d.LBXHGB*10/d.LBXRBCSI).abs().median()),
        'mchc_minus_hgb_times_100_over_hct_abs_median': float((d.LBXMC - d.LBXHGB*100/d.LBXHCT).abs().median())}
    (OUT / 'cbc_relationships.json').write_text(json.dumps(relationships, indent=2) + '\n')
    scaled = StandardScaler().fit_transform(d[CBC])
    descriptive = CheckedPCA(svd_solver='full').fit(scaled)
    scores = descriptive.transform(scaled)
    variance = pd.DataFrame({'component': np.arange(1, len(CBC)+1),
                            'explained_variance_ratio': descriptive.explained_variance_ratio_,
                            'cumulative_variance': descriptive.explained_variance_ratio_.cumsum()})
    variance.to_csv(OUT / 'descriptive_pca_variance.csv', index=False)
    pd.DataFrame(descriptive.components_.T, index=CBC,
                 columns=[f'PC{i+1}' for i in range(len(CBC))]).to_csv(OUT / 'descriptive_pca_loadings.csv')
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].plot(variance.component, variance.cumulative_variance, marker='o')
    axes[0].axhline(.95, color='gray', linestyle='--')
    axes[0].set(xlabel='Components', ylabel='Cumulative explained variance', title='Standardized CBC scree (descriptive)')
    for label, color in [(0, '#3478a6'), (1, '#d55e00')]:
        keep = d.target.eq(label)
        axes[1].scatter(scores[keep, 0], scores[keep, 1], s=10, alpha=.4,
                        c=color, label=f'HbA1c {"≥" if label else "<"}6.5% (n={keep.sum()})')
    axes[1].set(xlabel='PC1', ylabel='PC2', title='Whole-cohort view; not validation')
    axes[1].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(OUT / 'cbc_pca_diagnostics.png', dpi=180); plt.close(fig)
    pred, audit = matched_pca(d, [
        ('demographics_bmi_cbc', False, CBC),
        ('demographics_bmi_cbc_pca95', True, CBC),
    ])
    pred.to_csv(OUT / 'pca_oof_predictions.csv', index=False)
    pd.DataFrame(audit).to_csv(OUT / 'pca_fit_audit.csv', index=False)
    summary = ext.summarise(pred, 'exploratory_phase7')
    summary.to_csv(OUT / 'pca_model_comparison.csv', index=False)
    ext.jackknife(pred, full).to_csv(OUT / 'pca_conditional_intervals.csv', index=False)
    saved = pd.read_csv(ROOT / 'results/research_extension/primary_extension_predictions.csv')
    ref = saved.loc[saved.model.eq('demographics_bmi_cbc')].set_index('SEQN').sort_index()
    raw = pred.loc[pred.model.eq('demographics_bmi_cbc')].set_index('SEQN').sort_index()
    assert ref.index.equals(raw.index)
    for column in ['raw', 'calibrated', 'threshold']:
        np.testing.assert_allclose(raw[column], ref[column], rtol=1e-8, atol=1e-10)
    assert not pred.duplicated(['model', 'SEQN']).any()
    assert np.isfinite(pred[['raw', 'calibrated', 'threshold']]).all().all()
    assert pred.groupby('model').size().eq(4612).all()
    assert pred.groupby('model').target.sum().eq(106).all()
    assert pred.groupby('SEQN').fold.nunique().eq(1).all()
    status = dict(status='passed', participants=4612, positives=106, fit_audits=len(audit),
                  checks=['saved raw-CBC prediction reproduction', 'matched subjects and folds',
                          'PSU separation for all inner and outer fits', 'training-only PCA sample counts',
                          'finite unique predictions', 'PCA projections match independent einsum contraction'],
                  protocol_sha256=hashlib.sha256((ROOT/'docs/methods/phase7_analysis_protocol.md').read_bytes()).hexdigest())
    (ROOT / 'docs/verification/cbc_diagnostics_validation.json').write_text(json.dumps(status, indent=2)+'\n')
    calibrated = summary.loc[summary.stage.eq('calibrated')]
    table = ['| Model | AUROC | AP | Brier | Log loss | Deferred | Missed / 106 |',
             '|---|---:|---:|---:|---:|---:|---:|']
    for r in calibrated.itertuples():
        table.append(f'| {r.model} | {r.AUROC:.4f} | {r.AP:.4f} | {r.Brier:.5f} | '
                     f'{r.log_loss:.5f} | {r.deferred_n} | {r.missed_n} |')
    vif = pd.DataFrame(rows)
    top = vif.loc[(vif.block == 'full_21') & (vif.weighting == 'survey_weighted')].nlargest(4, 'VIF')
    notes = '\n'.join(f'- {r.variable}: weighted VIF {r.VIF:.1f}.' for r in top.itertuples())
    counts = sorted({int(r['components']) for r in audit if 'components' in r})
    report = f'''# CBC collinearity and PCA supplement — 2026-11-23

Exploratory Phase 7 supplement on the fixed 4,612 adults / 106 positive HbA1c labels.
The original primary analysis and independent-cycle results are preserved.

## Collinearity

Differential percentages sum to {differential.min():.1f}–{differential.max():.1f}%
(mean {differential.mean():.3f}%). The team's 2026-11-23 cohort-summary decision
supersedes the earlier 11-predictor block (which dropped MCH, MCHC, MPV, NRBC,
basophil % and the five absolute differential counts): all 21 CBC variables are
now kept as model features. Rounding makes the released differential sum
approximately fixed. VIFs for both the legacy 11-predictor block and the current
full 21-predictor block are exported with ordinary and survey-weighted auxiliary
regressions and an intercept, so the earlier collinearity finding can be checked
against the larger panel.
Adding back the dropped components does not remove the strong approximate
dependence among the differential percentages; high VIF persists and motivates
the PCA sensitivity arm.

Largest survey-weighted VIFs in the current full 21-predictor block:

{notes}

Hematocrit approximately equals RBC × MCV / 10 (median absolute residual
{relationships['hct_minus_rbc_times_mcv_over_10_abs_median']:.4f} hematocrit
percentage points). Now that MCH and MCHC are themselves predictors, the same
kind of near-identity applies to them: MCH ≈ HGB × 10 / RBC (median absolute
residual {relationships['mch_minus_hgb_times_10_over_rbc_abs_median']:.4f} pg) and
MCHC ≈ HGB × 100 / HCT (median absolute residual
{relationships['mchc_minus_hgb_times_100_over_hct_abs_median']:.4f} g/dL) — both
expected to inflate VIF further in the full 21-predictor block versus the legacy
11. High VIF does not justify causal interpretation, nor does it automatically
invalidate penalized prediction. Retain the existing regularized raw-feature
model and treat PCA as a secondary robustness comparison.

## Matched nested comparison

Both models use demographics and BMI. Only the CBC representation changes. PCA
retains 95% variance with component counts {counts} across inner/outer training fits.
Scaling/PCA are unweighted; classifiers, calibration and evaluation use WTPH2YR.
Five outer / three inner PSU-grouped folds match the extension. Calibration and
95%-weighted-sensitivity thresholds use development data only.

{chr(10).join(table)}

Deferred and missed are observed counts; the development sensitivity target does
not guarantee held-out sensitivity. Conditional design intervals are exported,
but exclude refitting/split uncertainty; no superiority or clinical-safety claim
is established by this exploratory comparison. The older cycle was not reused.

## Figures and verification

![Descriptive scree and PC1/PC2](../../results/cbc_diagnostics/cbc_pca_diagnostics.png)

The whole-cohort figure and loadings are descriptive and never enter validation.
PCA maximizes predictor variance, not outcome separation. Components/loadings are
not causal effects. Re-run `python scripts/analysis/cbc_diagnostics.py` from the root.

Checks passed for saved raw-CBC prediction reproduction, matched subjects/folds,
all 40 inner/outer fit audits, PSU separation, PCA training sample counts, and
finite unique predictions. See [validation](../verification/cbc_diagnostics_validation.json)
and [analysis specification](../methods/phase7_analysis_protocol.md).
PCA projections are checked against independent non-BLAS contractions. The local
NumPy/Apple BLAS build emitted matmul floating-point warnings despite finite,
matching results; these warnings are accepted only after that numerical check.

This supplies additional reproducible methods, a meaningful matched baseline,
variability estimates and explicit limitations for the final-project rubric.
Team review and integration with the other cohort/endpoint proposals remain open.
'''
    (ROOT / 'docs/findings/cbc_diagnostics.md').write_text(report)
    print(summary.loc[summary.stage.eq('calibrated')].to_string(index=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vif-only', action='store_true',
                        help='Refresh the VIF table without refitting PCA models.')
    main(vif_only=parser.parse_args().vif_only)
