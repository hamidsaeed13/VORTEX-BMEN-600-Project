"""Run Phase 13 CBC selection with nested, survey-weighted L1 logistic regression."""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

import research_extension as ext
from cbc_diagnostics import CANDIDATE_14

OUT = ext.ROOT / 'results/cbc_selection'
C_GRID = (0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 1.28, 2.56, 5.12)
TOLERANCE = 0.005
COEF_THRESHOLD = 1e-8
NUMERIC = ext.NUM + ['BMXBMI'] + CANDIDATE_14
COLUMNS = NUMERIC + ext.CAT
BASELINE = 'demographics_bmi_cbc'
LASSO = 'demographics_bmi_cbc_lasso'


def fit_lasso(train, penalty_c):
    model = ext.build(NUMERIC)
    model.set_params(clf__penalty='l1', clf__C=penalty_c, clf__random_state=42)
    weights = train._weight.to_numpy()
    model.fit(train[COLUMNS], train.target, clf__sample_weight=weights / weights.mean())
    assert model['clf'].n_iter_.max() < model['clf'].max_iter
    return model


def coefficients(model, fold, stage, penalty_c):
    names = model['pre'].get_feature_names_out()
    values = pd.Series(model['clf'].coef_[0], index=names)
    return [dict(fold=fold, stage=stage, C=penalty_c, variable=column,
                 coefficient=values[f'numeric__{column}'],
                 retained=abs(values[f'numeric__{column}']) > COEF_THRESHOLD)
            for column in CANDIDATE_14]


def run_nested(data, outer):
    path, selected, assignments, predictions = [], [], [], []
    for fold, (train_idx, test_idx) in enumerate(outer, 1):
        dev, test = data.iloc[train_idx], data.iloc[test_idx]
        assert set(dev.group).isdisjoint(test.group)
        inner = ext.folds_for(dev, n=3, seed=420 + fold)
        for stage, (fit_idx, valid_idx) in enumerate(inner, 1):
            assert set(dev.iloc[fit_idx].group).isdisjoint(dev.iloc[valid_idx].group)
            assert set(dev.iloc[fit_idx].group).isdisjoint(test.group)
            assignments.append(dev.iloc[valid_idx][['SEQN', 'group']].assign(
                outer_fold=fold, inner_validation_fold=stage))

        scores_by_c, coefficients_by_c, means = {}, {}, {}
        for penalty_c in C_GRID:
            scores = np.full(len(dev), np.nan)
            fold_aucs, rows = [], []
            for stage, (fit_idx, valid_idx) in enumerate(inner, 1):
                model = fit_lasso(dev.iloc[fit_idx], penalty_c)
                valid = dev.iloc[valid_idx]
                assert np.isnan(scores[valid_idx]).all()
                scores[valid_idx] = model.predict_proba(valid[COLUMNS])[:, 1]
                auc = roc_auc_score(valid.target, scores[valid_idx], sample_weight=valid._weight)
                fold_aucs.append(auc)
                rows.extend(coefficients(model, fold, f'inner_{stage}', penalty_c))
                path.append(dict(fold=fold, inner_fold=stage, C=penalty_c, weighted_AUROC=auc))
            assert np.isfinite(scores).all()
            scores_by_c[penalty_c], coefficients_by_c[penalty_c] = scores, rows
            means[penalty_c] = np.mean(fold_aucs)

        chosen_c = min(c for c in C_GRID if means[c] >= max(means.values()) - TOLERANCE)
        selected.extend(coefficients_by_c[chosen_c])
        weights = dev._weight.to_numpy()
        cal = LogisticRegression(solver='liblinear', C=1e6, max_iter=2000)
        dev_logits = ext.logits(scores_by_c[chosen_c])
        cal.fit(dev_logits, dev.target, sample_weight=weights / weights.mean())
        threshold = ext.threshold(dev.target.to_numpy(), cal.predict_proba(dev_logits)[:, 1], weights)

        model = fit_lasso(dev, chosen_c)
        selected.extend(coefficients(model, fold, 'outer', chosen_c))
        raw = model.predict_proba(test[COLUMNS])[:, 1]
        calibrated = cal.predict_proba(ext.logits(raw))[:, 1]
        predictions.append(test[['SEQN', 'target', '_weight', 'SDMVSTRA', 'SDMVPSU']].assign(
            fold=fold, model=LASSO, raw=raw, calibrated=calibrated, threshold=threshold,
            flagged=calibrated >= threshold, constant=np.average(dev.target, weights=weights)))
    return (pd.DataFrame(path), pd.DataFrame(selected), pd.concat(assignments, ignore_index=True),
            pd.concat(predictions, ignore_index=True))


def compare(baseline, candidate):
    keys = ['SEQN', 'fold', 'target', 'SDMVSTRA', 'SDMVPSU']
    paired = baseline.merge(candidate, on=keys, validate='one_to_one', suffixes=('_full', '_lasso'))
    assert len(paired) == len(baseline) == len(candidate)
    np.testing.assert_allclose(paired._weight_full, paired._weight_lasso, rtol=1e-12, atol=0)
    rows = []
    for fold, block in [('pooled', paired), *paired.groupby('fold')]:
        full_auc = roc_auc_score(block.target, block.calibrated_full, sample_weight=block._weight_full)
        lasso_auc = roc_auc_score(block.target, block.calibrated_lasso, sample_weight=block._weight_full)
        rows.append(dict(fold=fold, n=len(block), positives=int(block.target.sum()),
                         full_21_AUROC=full_auc, lasso_AUROC=lasso_auc, delta=lasso_auc - full_auc))
    return pd.DataFrame(rows)


def main():
    _, data = ext.load_cycle('L')
    assert len(data) == 4612 and data.target.sum() == 106 and len(CANDIDATE_14) == 14
    outer = ext.folds_for(data)
    saved = pd.read_csv(ext.OUT / 'primary_extension_predictions.csv').query('model == @BASELINE')
    refit = ext.nested(data, specs={BASELINE: ext.PRIMARY[BASELINE]}, outer=outer)
    compare(saved, refit)
    aligned = saved.set_index('SEQN').loc[refit.SEQN]
    np.testing.assert_allclose(aligned[['raw', 'calibrated', 'threshold']],
                               refit[['raw', 'calibrated', 'threshold']], rtol=1e-8, atol=1e-10)
    path, selection, splits, candidate = run_nested(data, outer)
    assert splits.groupby(['outer_fold', 'group']).inner_validation_fold.nunique().eq(1).all()
    assigned = splits.merge(candidate[['SEQN', 'fold']], on='SEQN', validate='many_to_one')
    assert assigned.outer_fold.ne(assigned.fold).all()
    assert assigned.groupby('SEQN').size().eq(len(outer) - 1).all()
    comparison = compare(saved, candidate)

    OUT.mkdir(parents=True, exist_ok=True)
    for name, frame in [('inner_penalty_path', path), ('selected_coefficients', selection),
                        ('inner_validation_membership', splits), ('oof_predictions', candidate),
                        ('weighted_auroc', comparison)]:
        frame.to_csv(OUT / f'{name}.csv', index=False)
    print(comparison.to_string(index=False))


if __name__ == '__main__':
    main()
