"""Exploratory: relabel the SAME locked cohort using the secondary/prediabetes HbA1c
threshold (LBXGH >= 5.7%, study_config.SECONDARY_CUT) instead of the primary diabetes
threshold (>=6.5%, PRIMARY_CUT), to see how many more "positive" cases this produces and
how it changes the headline comparison.

Team request (2026-11-24): "is it possible to increase the population based on [a lower
HbA1c] threshold" -- confirmed via follow-up to mean the HbA1c cutoff specifically. Note this
does NOT change cohort membership (eligibility doesn't depend on HbA1c; same 4,612 people):
it only relabels which of them count as positive, shifting the clinical question from
"detect diabetes (HbA1c>=6.5%)" to "detect diabetes-or-prediabetes (HbA1c>=5.7%)" -- SECONDARY_CUT
is already flagged in study_config.py as "secondary/exploratory only, never the primary label"
for exactly this reason: it is a materially different, less severe condition, not just "the
same thing with more data."

Does not touch study_config.py, the locked eligibility/outcome definition, or
results/research_extension/. Reuses research_extension.py's already-fitted machinery
(ext.load_cycle, ext.nested, ext.summarise, ext.jackknife, ext.folds_for) with the target
column overwritten.

Run: python scripts/analysis/secondary_threshold_cohort.py [--bootstrap 100]
Outputs: results/secondary_threshold/
"""
from pathlib import Path
import sys
import argparse
import json
import time
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/analysis'))
import research_extension as ext
import study_config as cfg

OUT = ROOT / 'results/secondary_threshold'
OUT.mkdir(parents=True, exist_ok=True)

HEADLINE = {**ext.PRIMARY,
            'demographics_bmi_cbc_adaboost': ext.OTHERS['demographics_bmi_cbc_adaboost'],
            'demographics_bmi_cbc_ensemble': ext.ENSEMBLE['demographics_bmi_cbc_ensemble']}


def relabel(d, cut):
    d = d.copy()
    d['target'] = d.LBXGH.ge(cut).astype(int)
    return d


def bootstrap(d, full, count, specs):
    outer = ext.folds_for(d); rng = np.random.default_rng(20261102)
    design = full.loc[full._weight.gt(0), ['SDMVSTRA', 'SDMVPSU']].drop_duplicates()
    assert design.groupby('SDMVSTRA').size().eq(2).all()
    rows = []; failures = []
    for rep in range(count):
        mult = np.zeros(len(d), dtype=int)
        for h, hg in design.groupby('SDMVSTRA'):
            chosen = rng.choice(hg.SDMVPSU.to_numpy())
            mult[d.SDMVSTRA.eq(h) & d.SDMVPSU.eq(chosen)] = 2
        try:
            predictions = ext.nested(d, specs=specs, outer=outer, multiplicity=mult)
            for name, g in predictions.groupby('model'):
                rows.append(dict(replicate=rep, model=name, **ext.metrics(g)))
        except ValueError as e:
            failures.append(dict(replicate=rep, error=str(e)))
        if (rep + 1) % 5 == 0:
            pd.DataFrame(rows).to_csv(OUT / 'bootstrap_replicates.csv', index=False)
            print(f'Secondary-threshold bootstrap: {rep + 1}/{count}; failures={len(failures)}', flush=True)
    (OUT / 'bootstrap_failures.json').write_text(json.dumps(failures, indent=2) + '\n')
    b = pd.DataFrame(rows); b.to_csv(OUT / 'bootstrap_replicates.csv', index=False)
    summaries = []
    for name, g in b.groupby('model'):
        for metric in ['AUROC', 'AP', 'Brier', 'sensitivity', 'deferred_fraction']:
            summaries.append(dict(model=name, metric=metric, successful_replicates=len(g),
                lower=g[metric].quantile(.025), upper=g[metric].quantile(.975)))
    wide = b.pivot(index='replicate', columns='model', values='AUROC')
    for a, b_name, label in [('demographics_bmi_cbc', 'demographics_bmi_cbc_adaboost', 'Logistic_minus_AdaBoost_AUROC'),
                             ('demographics_bmi_cbc_ensemble', 'demographics_bmi_cbc', 'Ensemble_minus_Logistic_AUROC'),
                             ('demographics_bmi_cbc_ensemble', 'demographics_bmi_cbc_adaboost', 'Ensemble_minus_AdaBoost_AUROC'),
                             ('demographics_bmi_cbc', 'demographics_bmi', 'CBC_minus_BMI_AUROC')]:
        if a in wide.columns and b_name in wide.columns:
            delta = wide[a] - wide[b_name]
            summaries.append(dict(model=label, metric='AUROC_gain', successful_replicates=len(delta.dropna()),
                lower=delta.quantile(.025), upper=delta.quantile(.975)))
    pd.DataFrame(summaries).to_csv(OUT / 'bootstrap_intervals.csv', index=False)
    return len(failures)


def main(count=100):
    started = time.time()
    full, d_primary = ext.load_cycle('L')
    d = relabel(d_primary, cfg.SECONDARY_CUT)
    full_j, d_j_primary = ext.load_cycle('J')
    d_j = relabel(d_j_primary, cfg.SECONDARY_CUT)

    counts = pd.DataFrame([
        dict(cohort='2021_2023_primary_6.5', n=len(d_primary), positives=int(d_primary.target.sum())),
        dict(cohort='2021_2023_secondary_5.7', n=len(d), positives=int(d.target.sum())),
        dict(cohort='2017_2018_primary_6.5', n=len(d_j_primary), positives=int(d_j_primary.target.sum())),
        dict(cohort='2017_2018_secondary_5.7', n=len(d_j), positives=int(d_j.target.sum())),
    ])
    counts.to_csv(OUT / 'cohort_counts.csv', index=False)
    print(counts.to_string(index=False))
    print(f'\nSame {len(d)} people as the locked cohort -- only the label changed. '
          f'{int(d.target.sum()) - int(d_primary.target.sum())} participants flip from negative to '
          f'positive at the 5.7% cut who were negative at 6.5%.')

    print('\nFitting headline models at the secondary (5.7%) threshold...')
    pred = ext.nested(d, specs=HEADLINE, verbose=True)
    pred.to_csv(OUT / 'secondary_predictions.csv', index=False)
    secondary_results = ext.summarise(pred, 'secondary_5.7')
    secondary_results.to_csv(OUT / 'secondary_model_comparison.csv', index=False)
    ext.jackknife(pred, full).to_csv(OUT / 'secondary_conditional_intervals.csv', index=False)

    print('\nFor comparison, refitting at the locked primary (6.5%) threshold...')
    pred_primary = ext.nested(d_primary, specs=HEADLINE, verbose=False)
    primary_results = ext.summarise(pred_primary, 'primary_6.5')

    both = pd.concat([secondary_results, primary_results], ignore_index=True)
    both.to_csv(OUT / 'secondary_vs_primary_comparison.csv', index=False)
    calibrated = both[both.stage.eq('calibrated')]
    pivot = calibrated.pivot(index='model', columns='analysis', values='AUROC')
    pivot['AUROC_delta_secondary_minus_primary'] = pivot['secondary_5.7'] - pivot['primary_6.5']
    pivot.to_csv(OUT / 'auroc_comparison.csv')
    print('\n=== AUROC: secondary (5.7%, diabetes-or-prediabetes) vs. primary (6.5%, locked) threshold ===')
    print(pivot.round(4).to_string())

    failures = bootstrap(d, full, count, HEADLINE) if count else None
    metadata = dict(n=len(d), positives_primary=int(d_primary.target.sum()),
        positives_secondary=int(d.target.sum()), secondary_cut=cfg.SECONDARY_CUT,
        primary_cut=cfg.PRIMARY_CUT, bootstrap_requested=count, bootstrap_failures=failures,
        elapsed_seconds=time.time() - started)
    (OUT / 'secondary_threshold_metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(f'\nOutputs written to {OUT}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--bootstrap', type=int, default=100)
    main(parser.parse_args().bootstrap)
