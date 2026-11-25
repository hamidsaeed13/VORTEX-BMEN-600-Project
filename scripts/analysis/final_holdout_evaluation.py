"""Phase 15 Step 6: final locked evaluation on a genuinely untouched holdout.

Every number elsewhere in this pipeline comes from nested CV over the same 4,612
participants, reused across dozens of specs by now (11->21->9 CBC features, 6+
model families, 2 class-balancing schemes). This script reserves a fresh, single
PSU-grouped development/holdout split -- using a random seed (99912601) that has
never been used anywhere else in this codebase -- fits the three models the team
has actually been comparing (logistic, AdaBoost, and their soft-voting ensemble,
all on demographics+BMI+the locked 9-feature CBC block) on the development
portion only, with its own internal 3-fold calibration/threshold selection
(matching the inner-fold convention used everywhere else in research_extension.py),
then evaluates ONCE on the holdout.

THIS HOLDOUT IS NOW SPENT. Do not rerun this script with a different model spec
or feature set and report the result as confirmatory -- that defeats the purpose
of reserving it. If the locked model/feature set changes meaningfully later, a
new holdout (a new seed, documented as such) would be needed for a genuine final
check.

Run: python scripts/analysis/final_holdout_evaluation.py
"""
from pathlib import Path
import sys
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import roc_curve, roc_auc_score

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/analysis'))
import research_extension as ext

OUT = ROOT / 'results/final_holdout'
OUT.mkdir(parents=True, exist_ok=True)

HOLDOUT_SEED = 99912601  # used nowhere else in this codebase -- see module docstring


def main():
    full, d = ext.load_cycle('L')
    assert len(d) == 4612 and d.target.sum() == 106

    splits = list(StratifiedGroupKFold(n_splits=4, shuffle=True, random_state=HOLDOUT_SEED).split(d, d.target, d.group))
    dev_idx, holdout_idx = splits[0]  # ~75% development, ~25% holdout
    assert not set(d.iloc[dev_idx].group) & set(d.iloc[holdout_idx].group)
    assert d.iloc[dev_idx].target.nunique() == 2 and d.iloc[holdout_idx].target.nunique() == 2
    print(f'Development: n={len(dev_idx)}, positives={int(d.iloc[dev_idx].target.sum())}', flush=True)
    print(f'Holdout: n={len(holdout_idx)}, positives={int(d.iloc[holdout_idx].target.sum())}', flush=True)

    multiplicity = np.ones(len(d), dtype=int)
    inner = ext.folds_for(d.iloc[dev_idx], n=3, seed=HOLDOUT_SEED + 1)

    locked_models = {
        'demographics_bmi_cbc': ext.PRIMARY['demographics_bmi_cbc'],
        'demographics_bmi_cbc_adaboost': (ext.NUM + ['BMXBMI'] + ext.RED + ext.WHITE, 'adaboost'),
        'demographics_bmi_cbc_ensemble': (ext.NUM + ['BMXBMI'] + ext.RED + ext.WHITE, 'ensemble_la'),
    }
    dev_prevalence = np.average(d.iloc[dev_idx].target, weights=d.iloc[dev_idx]._weight)

    records = []
    for name, spec in locked_models.items():
        model, cal, cut = ext.development_fit(d, dev_idx, spec, multiplicity, inner)
        raw = model.predict_proba(d.iloc[holdout_idx][spec[0] + ext.CAT])[:, 1]
        calibrated = cal.predict_proba(ext.logits(raw))[:, 1]
        g = d.iloc[holdout_idx][['SEQN', 'target', '_weight', 'SDMVSTRA', 'SDMVPSU']].copy()
        g['model'] = name; g['raw'] = raw; g['calibrated'] = calibrated
        g['threshold'] = cut; g['flagged'] = calibrated >= cut; g['constant'] = dev_prevalence
        records.append(g)
        print(f'[{name}] development threshold (95% target): {cut:.4f}', flush=True)
    pred = pd.concat(records, ignore_index=True)
    assert not pred.duplicated(['model', 'SEQN']).any()
    assert np.isfinite(pred[['raw', 'calibrated', 'threshold']]).all().all()
    pred.to_csv(OUT / 'final_holdout_predictions.csv', index=False)

    summary = ext.summarise(pred, 'final_holdout')
    summary.to_csv(OUT / 'final_holdout_summary.csv', index=False)
    calibrated_summary = summary.loc[summary.stage.eq('calibrated')]
    print(calibrated_summary[['model', 'n', 'positives', 'AUROC', 'AP', 'Brier', 'sensitivity',
                              'deferred_fraction', 'deferred_n', 'missed_n']].to_string(index=False), flush=True)

    fig, ax = plt.subplots(figsize=(7, 6))
    for name, g in pred.groupby('model'):
        fpr, tpr, _ = roc_curve(g.target, g.calibrated, sample_weight=g._weight)
        auc = roc_auc_score(g.target, g.calibrated, sample_weight=g._weight)
        ax.plot(fpr, tpr, label=f'{name}: {auc:.3f}')
    ax.plot([0, 1], [0, 1], 'k--', label='Chance')
    ax.set(xlabel='False positive rate (weighted)', ylabel='Sensitivity (weighted)',
           title='Final holdout (spent, single evaluation) — ROC')
    ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(OUT / 'final_holdout_roc.png', dpi=170); plt.close(fig)

    metadata = dict(
        status='SPENT -- do not reuse this holdout for further model selection',
        holdout_seed=HOLDOUT_SEED, n_development=len(dev_idx), n_holdout=len(holdout_idx),
        positives_development=int(d.iloc[dev_idx].target.sum()), positives_holdout=int(d.iloc[holdout_idx].target.sum()),
        development_weighted_prevalence=float(dev_prevalence),
        models_evaluated=list(locked_models),
        note='Development-only 3-fold inner calibration/threshold selection (95% weighted-sensitivity '
             'target), matching the inner-fold convention used throughout research_extension.py. '
             'The holdout itself was never touched during fitting, calibration or threshold selection.')
    (OUT / 'final_holdout_metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(f'\nOutputs: {OUT}', flush=True)


if __name__ == '__main__':
    main()
