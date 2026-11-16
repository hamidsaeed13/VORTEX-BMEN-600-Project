"""Independently reconstruct metric changes and check held-out donor accounting."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score, log_loss

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'results/permutation_importance'


def main():
    pred = pd.read_csv(OUT/'baseline_oof_predictions.csv')
    repeats = pd.read_csv(OUT/'permutation_repeat_metrics.csv')
    summary = pd.read_csv(OUT/'permutation_importance_summary.csv')
    donors = pd.read_csv(OUT/'heldout_donors.csv')
    splits = pd.read_csv(OUT/'split_audit.csv')
    saved = pd.read_csv(ROOT/'results/research_extension/primary_extension_predictions.csv')
    assert len(splits) == 20 and splits.group_overlap.eq(0).all()
    assert not pred.duplicated(['model', 'SEQN']).any()
    models = sorted(pred.model.unique())
    assert len(models) == 2 and len(pred) == 9224
    reference = pred.loc[pred.model.eq(models[0])].set_index('SEQN')
    assert len(reference) == 4612 and reference.target.sum() == 106
    for name, g in pred.groupby('model'):
        a = g.set_index('SEQN').sort_index()
        b = saved.loc[saved.model.eq(name)].set_index('SEQN').sort_index()
        assert a.index.equals(b.index)
        for col in ['target', '_weight', 'fold', 'calibrated']:
            np.testing.assert_allclose(a[col], b[col], rtol=1e-8, atol=1e-10)
    assert len(donors) == 4612*20
    assert not donors.duplicated(['repeat', 'SEQN']).any()
    assert donors.groupby('repeat').size().eq(4612).all()
    for (fold, repeat, group), g in donors.groupby(['fold', 'repeat', 'group']):
        assert set(g.SEQN) == set(g.donor_SEQN)
        assert reference.loc[g.SEQN, 'fold'].eq(fold).all()
        actual_group = (reference.loc[g.SEQN, 'SDMVSTRA'].astype(int).astype(str) + ':' +
                        reference.loc[g.SEQN, 'SDMVPSU'].astype(int).astype(str))
        assert actual_group.eq(group).all()
        assert g.seed.eq(20261116+1000*fold+repeat).all()
    assert len(repeats) == 2*9*20*4
    assert not repeats.duplicated(['model', 'block', 'repeat', 'metric']).any()
    with np.load(OUT/'perturbed_probabilities.npz', allow_pickle=False) as archive:
        ids = archive['SEQN']
        assert len(set(ids)) == 4612 and set(ids) == set(reference.index)
        assert len(archive.files) == 2*9*20+1
        for (model, block, repeat), rows in repeats.groupby(['model', 'block', 'repeat']):
            g = pred.loc[pred.model.eq(model)].set_index('SEQN').loc[ids]
            y = g.target.to_numpy(); w = g._weight.to_numpy()
            p = archive[f'{model}__{block}__r{repeat}']
            assert np.isfinite(p).all() and ((p >= 0) & (p <= 1)).all()
            def score(prob):
                return dict(AUROC=roc_auc_score(y, prob, sample_weight=w),
                            AP=average_precision_score(y, prob, sample_weight=w),
                            Brier=np.sum(w*(y-prob)**2)/w.sum(),
                            log_loss=log_loss(y, prob, sample_weight=w, labels=[0, 1]))
            original, shuffled = score(g.calibrated.to_numpy()), score(p)
            assert set(rows.metric) == set(original)
            for row in rows.itertuples():
                sign = -1 if row.metric in ['AUROC', 'AP'] else 1
                expected = sign*(shuffled[row.metric]-original[row.metric])
                np.testing.assert_allclose([row.baseline, row.permuted, row.importance],
                                           [original[row.metric], shuffled[row.metric], expected], atol=1e-12)
    for (model, block, metric), rows in repeats.groupby(['model', 'block', 'metric']):
        row = summary.loc[summary.model.eq(model) & summary.block.eq(block) & summary.metric.eq(metric)]
        assert len(row) == 1 and len(rows) == 20 and row.iloc[0].repeats == 20
        np.testing.assert_allclose([row.iloc[0]['mean'], row.iloc[0].permutation_sd],
                                   [rows.importance.mean(), rows.importance.std(ddof=1)], atol=1e-12)
    status_path = ROOT/'docs/verification/permutation_importance_validation.json'
    status = json.loads(status_path.read_text())
    protocol = ROOT/'docs/methods/permutation_importance_protocol.md'
    assert status['protocol_sha256'] == hashlib.sha256(protocol.read_bytes()).hexdigest()
    status['independent_checks'] = ['saved baseline predictions and weights', 'within-PSU donor membership and bijections',
                                    'all 360 probability vectors and 1440 metric differences',
                                    'all 72 importance summaries', 'protocol hash']
    status_path.write_text(json.dumps(status, indent=2)+'\n')
    print(json.dumps(status, indent=2))


if __name__ == '__main__':
    main()
