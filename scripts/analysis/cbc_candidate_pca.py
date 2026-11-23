"""Compare raw and PCA representations of the Phase 13 candidate panel."""

import numpy as np
import pandas as pd

import research_extension as ext
from cbc_diagnostics import CBC, CANDIDATE_14, matched_pca
from cbc_lasso_selection import BASELINE, OUT, compare


def main():
    _, data = ext.load_cycle('L')
    assert len(CANDIDATE_14) == 14
    predictions, audit_rows = matched_pca(data, [
        (BASELINE, False, CBC),
        ('full_21_pca95', True, CBC),
        ('candidate_14_raw', False, CANDIDATE_14),
        ('candidate_14_pca95', True, CANDIDATE_14),
    ])
    baseline = predictions.loc[predictions.model.eq(BASELINE)]
    saved = pd.read_csv(ext.OUT / 'primary_extension_predictions.csv').query('model == @BASELINE')
    compare(saved, baseline)
    reference = saved.set_index('SEQN').loc[baseline.SEQN]
    np.testing.assert_allclose(reference[['raw', 'calibrated', 'threshold']],
                               baseline[['raw', 'calibrated', 'threshold']], rtol=1e-8, atol=1e-10)
    for _, group in predictions.groupby('model'):
        compare(baseline, group)
    assert np.isfinite(predictions[['raw', 'calibrated', 'threshold']]).all().all()
    audit = pd.DataFrame(audit_rows)
    pca = audit.loc[audit.model.str.endswith('pca95')]
    assert len(pca) == 40 and pca.pca_fit_n.eq(pca.train_n).all()
    assert pca.retained_variance.ge(.95).all() and audit.group_overlap.eq(0).all()
    summary = ext.summarise(predictions, 'phase13_pca_sensitivity')

    OUT.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(OUT / 'pca_oof_predictions.csv', index=False)
    audit.to_csv(OUT / 'pca_fit_audit.csv', index=False)
    summary.to_csv(OUT / 'pca_model_comparison.csv', index=False)
    print(summary.loc[summary.stage.eq('calibrated'), ['model', 'AUROC', 'AP', 'Brier']].to_string(index=False))
    print(pca.groupby('model').components.agg(['min', 'max']).to_string())


if __name__ == '__main__':
    main()
