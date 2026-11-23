"""Survey-weighted, held-out, within-PSU grouped permutation importance.

Run from repository root. Existing research artifacts are read, never overwritten.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, average_precision_score, log_loss
import research_extension as ext

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'results/permutation_importance'
REPEATS = 20
SEED = 20261116
# Income (INDFMPIR) is deliberately absent: Phase 15 dropped it from the model (near-zero/
# negative marginal AUROC in both ablation and this script's own earlier permutation-importance
# finding -- see docs/findings/feature_reduction.md). Permuting a column the fitted model never
# reads is a no-op (always exactly zero importance, not a finding), so it's not a block here.
BLOCKS = {'age': ['RIDAGEYR'], 'sex': ['RIAGENDR'], 'race_ethnicity': ['RIDRETH3'],
          'education': ['DMDEDUC2'], 'BMI': ['BMXBMI'],
          'red_cells': ext.RED, 'white_cells_platelets': ext.WHITE,
          'all_CBC': ext.RED + ext.WHITE}
SPECS = {'demographics_bmi_cbc': ext.PRIMARY['demographics_bmi_cbc'],
         'demographics_bmi_cbc_forest': ext.FORESTS['demographics_bmi_cbc_forest']}


def metrics(y, p, w):
    return {'AUROC': roc_auc_score(y, p, sample_weight=w),
            'AP': average_precision_score(y, p, sample_weight=w),
            'Brier': np.average((y-p)**2, weights=w),
            'log_loss': log_loss(y, p, sample_weight=w, labels=[0, 1])}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    _, d = ext.load_cycle('L')
    assert len(d) == 4612 and d.target.sum() == 106
    outer = ext.folds_for(d)
    base = {name: np.full(len(d), np.nan) for name in SPECS}
    perturbed = {(name, block): np.full((REPEATS, len(d)), np.nan)
                 for name in SPECS for block in BLOCKS}
    baseline_records, donor_records, splits = [], [], []
    for fold, (train, test) in enumerate(outer, 1):
        inner = ext.folds_for(d.iloc[train], n=3, seed=420+fold)
        for stage, a, b in [('outer', train, test)] + [
                (f'inner_{i}', train[a], train[b]) for i, (a, b) in enumerate(inner, 1)]:
            overlap = set(d.iloc[a].group) & set(d.iloc[b].group)
            assert not overlap
            splits.append(dict(fold=fold, stage=stage, train_n=len(a), test_n=len(b), group_overlap=0))
        fitted = {}
        for name, spec in SPECS.items():
            model, cal, _ = ext.development_fit(d, train, spec, np.ones(len(d), dtype=int), inner)
            fitted[name] = model, cal
            raw = model.predict_proba(d.iloc[test][spec[0]+ext.CAT])[:, 1]
            p = cal.predict_proba(ext.logits(raw))[:, 1]
            base[name][test] = p
            g = d.iloc[test][['SEQN', 'target', '_weight', 'SDMVSTRA', 'SDMVPSU']].copy()
            g['model'] = name; g['fold'] = fold; g['calibrated'] = p
            baseline_records.append(g)
        z = d.iloc[test].reset_index(drop=True)
        for repeat in range(REPEATS):
            seed = SEED + 1000*fold + repeat
            rng = np.random.default_rng(seed)
            donors = np.arange(len(z))
            for positions in z.groupby('group', sort=True).indices.values():
                donors[positions] = rng.permutation(positions)
                assert set(donors[positions]) == set(positions)
            assert np.array_equal(z.group.to_numpy(), z.iloc[donors].group.to_numpy())
            donor_records.append(pd.DataFrame(dict(fold=fold, repeat=repeat, seed=seed,
                                                   SEQN=z.SEQN, donor_SEQN=z.iloc[donors].SEQN.to_numpy(),
                                                   group=z.group)))
            for block, columns in BLOCKS.items():
                x = z.copy()
                x[columns] = z.iloc[donors][columns].to_numpy()
                assert x[['SEQN', 'target', '_weight', 'group']].equals(z[['SEQN', 'target', '_weight', 'group']])
                for name, (model, cal) in fitted.items():
                    nums, _ = SPECS[name]
                    p = model.predict_proba(x[nums+ext.CAT])[:, 1]
                    perturbed[name, block][repeat, test] = cal.predict_proba(ext.logits(p))[:, 1]
        print(f'Permutation evaluation: outer fold {fold}/5 complete', flush=True)
    baseline = pd.concat(baseline_records, ignore_index=True)
    saved = pd.read_csv(ROOT/'results/research_extension/primary_extension_predictions.csv')
    for name in SPECS:
        ref = saved.loc[saved.model.eq(name)].set_index('SEQN').sort_index()
        actual = baseline.loc[baseline.model.eq(name)].set_index('SEQN').sort_index()
        assert ref.index.equals(actual.index)
        np.testing.assert_allclose(actual.calibrated, ref.calibrated, rtol=1e-8, atol=1e-10)
        assert np.array_equal(actual.fold, ref.fold)
    y = d.target.to_numpy(); w = d._weight.to_numpy()
    records, score_records = [], []
    for (name, block), predictions in perturbed.items():
        assert np.isfinite(predictions).all() and ((predictions >= 0) & (predictions <= 1)).all()
        original = metrics(y, base[name], w)
        for repeat, p in enumerate(predictions):
            shuffled = metrics(y, p, w)
            for metric, value in original.items():
                delta = value-shuffled[metric] if metric in ['AUROC', 'AP'] else shuffled[metric]-value
                records.append(dict(model=name, block=block, repeat=repeat, metric=metric,
                                    baseline=value, permuted=shuffled[metric], importance=delta))
            # Export enough probabilities to independently recompute pooled metric changes.
            # Wide columns keep the shared participants and donor map compact.
            score_records.append((f'{name}__{block}__r{repeat}', p))
    repeated = pd.DataFrame(records)
    summary = repeated.groupby(['model', 'block', 'metric']).importance.agg(
        mean='mean', permutation_sd='std', minimum='min', maximum='max', repeats='size').reset_index()
    baseline.to_csv(OUT/'baseline_oof_predictions.csv', index=False)
    pd.concat(donor_records, ignore_index=True).to_csv(OUT/'heldout_donors.csv', index=False)
    pd.DataFrame(splits).to_csv(OUT/'split_audit.csv', index=False)
    repeated.to_csv(OUT/'permutation_repeat_metrics.csv', index=False)
    summary.to_csv(OUT/'permutation_importance_summary.csv', index=False)
    # Compressed arrays avoid a large text prediction table; allow_pickle=False on reading.
    np.savez_compressed(OUT/'perturbed_probabilities.npz', SEQN=d.SEQN.to_numpy(),
                        **dict(score_records))
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharex=True)
    for ax, name in zip(axes, SPECS):
        table = summary.loc[summary.model.eq(name) & summary.metric.eq('AUROC')].sort_values('mean')
        ax.barh(table.block, table['mean'], xerr=table.permutation_sd, color='#3478a6', capsize=3)
        ax.axvline(0, color='gray', linewidth=1)
        ax.set(title='Logistic regression' if name == 'demographics_bmi_cbc' else 'Random forest',
               xlabel='Weighted AUROC loss (mean ± permutation SD)')
    fig.suptitle('Held-out within-PSU permutation; overlapping blocks are not additive')
    fig.tight_layout(); fig.savefig(OUT/'heldout_permutation_importance.png', dpi=180); plt.close(fig)
    status = dict(status='passed', participants=len(d), positives=int(y.sum()), models=2,
                  blocks=len(BLOCKS), repeats=REPEATS, outer_folds=5, seed=SEED,
                  checks=['saved calibrated prediction and fold reproduction', 'inner/outer PSU separation',
                          'donor bijections within held-out PSU', 'labels and weights unchanged',
                          'complete finite perturbed probabilities'],
                  protocol_sha256=hashlib.sha256((ROOT/'docs/methods/permutation_importance_protocol.md').read_bytes()).hexdigest())
    (ROOT/'docs/verification/permutation_importance_validation.json').write_text(json.dumps(status, indent=2)+'\n')
    lines = ['| Model | Block | Mean AUROC loss | Permutation SD |', '|---|---|---:|---:|']
    for name in SPECS:
        table = summary.loc[summary.model.eq(name) & summary.metric.eq('AUROC')].sort_values('mean', ascending=False)
        for r in table.itertuples():
            lines.append(f'| {"Logistic" if name == "demographics_bmi_cbc" else "Forest"} | {r.block} | {r.mean:.4f} | {r.permutation_sd:.4f} |')
    report = '''# Held-out grouped permutation importance — 2026-11-16

This completes the Phase 11 held-out interpretation task for the primary 4,612-person,
106-positive cohort. It evaluates the existing logistic and forest procedures, without
changing their features or selecting a model. Unperturbed calibrated predictions and
folds reproduce the saved extension results.

## What was measured

Each predictor block was jointly shuffled within each held-out PSU, using 20 reproducible
permutations and the same donors across models/blocks. No training records were shuffled;
preprocessing, classifiers and development-only calibrators stayed frozen. Joint CBC
shuffling preserves within-block relationships. Labels, weights and design membership stay
fixed. The five out-of-fold vectors are pooled per repeat for weighted evaluation.
Donor assignments are uniform within each PSU; weights remain attached to recipients.
This preserves the unweighted block values, not their survey-weighted marginal distribution.

The scores measure fitted-model reliance under this within-PSU perturbation. They exclude
between-PSU dependence and are not independent or causal contributions. Overlapping all-CBC,
red-cell and white-cell/platelet scores must not be added. Correlated predictors may
substitute for each other; cross-block shuffling can create unusual combinations.
Small sex/education scores, including negative values, do not establish absence of
biomedical relevance or fairness across groups. This is not a subgroup fairness test.

## Results

''' + '\n'.join(lines) + '''

Positive AUROC/AP loss or Brier/log-loss increase means worse performance after shuffling.
Negative values are retained. The reported SD describes random-permutation variation;
it is not a confidence interval, design-based uncertainty or model-refitting variability.
Do not use overlapping error bars to infer significance or rank small differences reliably.
All four metrics and per-repeat values are exported.

![Held-out permutation importance](../../results/permutation_importance/heldout_permutation_importance.png)

These descriptive results replace reliance on forest impurity importance for interpretation.
They do not establish test-removal value: removing a predictor and retraining is a different
experiment. They do not show clinical benefit or resolve the team's endpoint/cohort decisions.
The older cycle was not reused.

## Reproduction and checks

Run `python scripts/analysis/heldout_permutation_importance.py`, then
`python scripts/verification/verify_permutation_importance.py`. The donor table, split
audit, baseline predictions, repeat metrics and compressed perturbed probabilities support
independent metric reconstruction. Read the NPZ with `allow_pickle=False`.
See the [specification](../methods/permutation_importance_protocol.md) and
[validation](../verification/permutation_importance_validation.json).
'''
    (ROOT/'docs/findings/permutation_importance.md').write_text(report)
    print(summary.loc[summary.metric.eq('AUROC')].to_string(index=False))


if __name__ == '__main__':
    main()
