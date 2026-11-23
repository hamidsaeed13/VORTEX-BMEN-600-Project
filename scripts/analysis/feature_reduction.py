"""Phase 15 (CBC feature reduction), Steps 1-2: drop redundant CBC columns, then
run an L1 (Lasso) path to see which of the rest survive.

This is an exploratory/development-only selection pass, not a final evaluation.
It does not touch study_config.py: no feature set here is "locked" until the
team reviews these results (Step 3). Development data only; no outer held-out
set is spent on model/hyperparameter selection here, matching the existing
nested-CV convention in weighted_calibration_analysis.py/research_extension.py.

Two sources of redundancy, found separately by VIF (see docs/findings/
feature_reduction.md for the full story):
  (a) algebraic: MCH/MCHC are functions of HGB/RBC/HCT already kept; the five
      absolute differential counts are ~= WBC total x percentage already kept.
      Dropping these 7 fixes the red-cell VIF cluster (e.g. HGB 723 -> 22) but
      does almost nothing for the two worst offenders (LBXNEPCT, LBXLYPCT).
  (b) compositional: the 5-part differential sums to ~100%, so any 4 of the 5
      percentages determine the 5th. This is what actually drives LBXNEPCT/
      LBXLYPCT's VIF into the tens of thousands. Fixing it requires dropping
      exactly one percentage (basophil %, the rarest category and the team's
      earlier precedent) -- this alone brings VIF back to the pre-21-feature
      legacy range (~809 vs ~808 originally).

Run: python scripts/analysis/feature_reduction.py
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.metrics import roc_auc_score
import study_config as cfg
import research_extension as ext
from cbc_diagnostics import vif_table

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'results/feature_reduction'
OUT.mkdir(parents=True, exist_ok=True)

# This script explores reduction FROM the historical starting point, so it always anchors to
# _INITIAL explicitly -- not the unqualified cfg.CBC_FEATURES/NUMERIC_DEMOGRAPHICS, which now
# resolve to the locked REDUCED result of this exploration (Phase 15 Step 3, 2026-11-23).
NUM = cfg.NUMERIC_DEMOGRAPHICS_INITIAL
CAT = cfg.CATEGORICAL_DEMOGRAPHICS
CBC = cfg.CBC_FEATURES_INITIAL

ALGEBRAICALLY_REDUNDANT = ['LBXMCHSI', 'LBXMC', 'LBDLYMNO', 'LBDNENO', 'LBDMONO', 'LBDEONO', 'LBDBANO']
CANDIDATE_14 = [c for c in CBC if c not in ALGEBRAICALLY_REDUNDANT]
assert len(CANDIDATE_14) == 14

COMPOSITIONALLY_REDUNDANT = ['LBXBAPCT']  # drop one of the 5-part differential percentages
CANDIDATE_13 = [c for c in CANDIDATE_14 if c not in COMPOSITIONALLY_REDUNDANT]
assert len(CANDIDATE_13) == 13

# Recommended CBC candidate from Steps 1-2 (docs/findings/feature_reduction.md): the 7
# stably-selected features (>=60% selection rate across 25 repeated-CV folds) plus HGB/HCT
# restored for clinical face validity at ~zero measured AUROC cost. Not yet locked in
# study_config.py -- this is still a proposal pending team review.
CBC_REDUCED_9 = ['LBXRBCSI', 'LBXHGB', 'LBXHCT', 'LBXMCVSI', 'LBXWBCSI',
                 'LBXPLTSI', 'LBXLYPCT', 'LBXMOPCT', 'LBXEOPCT']
assert len(CBC_REDUCED_9) == 9


def build(nums, cats, C):
    transforms = [('numeric', Pipeline([('impute', SimpleImputer(strategy='median', add_indicator=True)),
                                        ('scale', StandardScaler())]), nums)]
    if cats:
        transforms += cfg.categorical_transformer_entries()
    pre = ColumnTransformer(transforms)
    clf = LogisticRegression(penalty='l1', solver='liblinear', C=C, max_iter=5000)
    return Pipeline([('pre', pre), ('sparse', FunctionTransformer(csr_matrix, accept_sparse=True)),
                     ('clf', clf)])


def cbc_coefficients(model, nums, cbc_cols):
    """Map fitted L1 coefficients back to their original CBC column names.

    The 'numeric' ColumnTransformer branch outputs its input columns in the same
    order as `nums` first, then appends any missing-value indicator columns --
    so coef_[:len(nums)] lines up positionally with `nums`.
    """
    coefs = model.named_steps['clf'].coef_[0]
    return {c: float(coefs[nums.index(c)]) for c in cbc_cols}


def l1_path(d, outer, cbc_cols, label, Cs):
    nums = NUM + ['BMXBMI'] + cbc_cols
    rows = []
    for C in Cs:
        fold_auc, nonzero = [], {c: 0 for c in cbc_cols}
        for train, test in outer:
            z = d.iloc[train]
            model = build(nums, CAT, C)
            w = z._weight.to_numpy()
            model.fit(z[nums + CAT], z.target, clf__sample_weight=w / w.mean())
            p = model.predict_proba(d.iloc[test][nums + CAT])[:, 1]
            wt = d.iloc[test]._weight.to_numpy()
            fold_auc.append(roc_auc_score(d.iloc[test].target, p, sample_weight=wt))
            for c, v in cbc_coefficients(model, nums, cbc_cols).items():
                if abs(v) > 1e-8:
                    nonzero[c] += 1
        rows.append(dict(set=label, C=C, mean_weighted_AUROC=np.mean(fold_auc), sd_weighted_AUROC=np.std(fold_auc),
                         n_cbc_selected_mean=np.mean(list(nonzero.values())),
                         **{f'folds_selected__{c}': n for c, n in nonzero.items()}))
        print(f'[{label}] C={C:.4f}: weighted AUROC {np.mean(fold_auc):.4f} +/- {np.std(fold_auc):.4f}, '
              f'avg folds-selected per CBC feature = {np.mean(list(nonzero.values())):.2f}/5', flush=True)
    return pd.DataFrame(rows)


def knee_row(path_for_set):
    best = path_for_set.mean_weighted_AUROC.max()
    near_best = path_for_set.loc[path_for_set.mean_weighted_AUROC >= 0.99 * best]
    return near_best.loc[near_best.C.idxmin()], best


def selection_at(row, threshold=3):
    selected = {c.replace('folds_selected__', ''): int(row[c]) for c in row.index if c.startswith('folds_selected__')}
    kept = sorted([c for c, n in selected.items() if n >= threshold], key=lambda c: -selected[c])
    dropped = sorted([c for c, n in selected.items() if n < threshold], key=lambda c: selected[c])
    return kept, dropped


def stability_check(d, cbc_cols, C, label, seeds):
    """Repeated PSU-grouped CV at a fixed C: how often is each feature selected
    across many more folds than the single 5-fold split used for the main path?
    Answers whether a knee-point selection is robust or a one-split artifact."""
    nums = NUM + ['BMXBMI'] + cbc_cols
    nonzero, total_folds = {c: 0 for c in cbc_cols}, 0
    aucs = []
    for seed in seeds:
        for train, test in ext.folds_for(d, seed=seed):
            z = d.iloc[train]
            model = build(nums, CAT, C)
            w = z._weight.to_numpy()
            model.fit(z[nums + CAT], z.target, clf__sample_weight=w / w.mean())
            p = model.predict_proba(d.iloc[test][nums + CAT])[:, 1]
            wt = d.iloc[test]._weight.to_numpy()
            aucs.append(roc_auc_score(d.iloc[test].target, p, sample_weight=wt))
            for c, v in cbc_coefficients(model, nums, cbc_cols).items():
                if abs(v) > 1e-8:
                    nonzero[c] += 1
            total_folds += 1
    freq = pd.DataFrame([dict(set=label, variable=c, folds_selected=n, total_folds=total_folds,
                              selection_rate=n / total_folds) for c, n in nonzero.items()]
                        ).sort_values('selection_rate', ascending=False)
    print(f'[{label}] stability over {total_folds} folds ({len(seeds)} seeds): '
          f'weighted AUROC {np.mean(aucs):.4f} +/- {np.std(aucs):.4f}', flush=True)
    return freq, float(np.mean(aucs)), float(np.std(aucs))


def categorical_entries_for(nominal_cols, ordinal_cols):
    """Like cfg.categorical_transformer_entries(), but for an arbitrary subset of
    nominal/ordinal columns (that function is hardcoded to the project's full
    NOMINAL_DEMOGRAPHICS/ORDINAL_DEMOGRAPHICS -- needed here to ablate one
    demographic variable at a time, including categorical ones)."""
    entries = []
    if nominal_cols:
        nominal = Pipeline([('impute', SimpleImputer(strategy='most_frequent')),
                            ('encode', OneHotEncoder(handle_unknown='ignore', sparse_output=False))])
        entries.append(('nominal', nominal, nominal_cols))
    if ordinal_cols:
        assert ordinal_cols == cfg.ORDINAL_DEMOGRAPHICS, 'only education is ordinal in this project'
        ordinal = Pipeline([('impute', SimpleImputer(strategy='most_frequent')),
                            ('encode', OrdinalEncoder(categories=[cfg.EDUCATION_LEVELS],
                                                      handle_unknown='use_encoded_value', unknown_value=-1))])
        entries.append(('ordinal', ordinal, ordinal_cols))
    return entries


def fit_eval_auroc(d, outer, nums, nominal_cols, ordinal_cols):
    """Plain (no L1) PSU-grouped weighted AUROC for an arbitrary numeric/nominal/
    ordinal feature combination -- the project's default modeling convention,
    used here for leave-one-block-out ablation across ALL features, not just CBC."""
    cats = nominal_cols + ordinal_cols
    aucs = []
    for train, test in outer:
        z = d.iloc[train]
        transforms = [('numeric', Pipeline([('impute', SimpleImputer(strategy='median', add_indicator=True)),
                                            ('scale', StandardScaler())]), nums)] if nums else []
        transforms += categorical_entries_for(nominal_cols, ordinal_cols)
        model = Pipeline([('pre', ColumnTransformer(transforms)),
                          ('sparse', FunctionTransformer(csr_matrix, accept_sparse=True)),
                          ('clf', LogisticRegression(solver='liblinear', max_iter=2000))])
        w = z._weight.to_numpy()
        model.fit(z[nums + cats], z.target, clf__sample_weight=w / w.mean())
        p = model.predict_proba(d.iloc[test][nums + cats])[:, 1]
        wt = d.iloc[test]._weight.to_numpy()
        aucs.append(roc_auc_score(d.iloc[test].target, p, sample_weight=wt))
    return np.mean(aucs), np.std(aucs)


def ablate_all_blocks(d, outer, cbc_cols):
    """Leave-one-block-out ablation across every feature currently in the model
    -- age, income, sex, race/ethnicity, education, BMI, and the reduced CBC
    block -- not just CBC. Each row removes exactly one block from the full set
    and reports the weighted-AUROC cost of removing it."""
    full_nums = NUM + ['BMXBMI'] + cbc_cols
    full_nominal, full_ordinal = cfg.NOMINAL_DEMOGRAPHICS, cfg.ORDINAL_DEMOGRAPHICS
    blocks = {
        'age': ('num', 'RIDAGEYR'), 'income': ('num', 'INDFMPIR'), 'BMI': ('num', 'BMXBMI'),
        'sex': ('nominal', 'RIAGENDR'), 'race_ethnicity': ('nominal', 'RIDRETH3'),
        'education': ('ordinal', 'DMDEDUC2'), 'CBC_reduced': ('cbc', None),
    }
    full_auc, full_sd = fit_eval_auroc(d, outer, full_nums, full_nominal, full_ordinal)
    rows = [dict(block_removed='none (full model)', mean_weighted_AUROC=full_auc, sd_weighted_AUROC=full_sd, auroc_cost=0.0)]
    for block, (kind, col) in blocks.items():
        nums = [c for c in full_nums if c != col] if kind in ('num',) else \
               [c for c in full_nums if c not in cbc_cols] if kind == 'cbc' else full_nums
        nominal = [c for c in full_nominal if c != col] if kind == 'nominal' else full_nominal
        ordinal = [c for c in full_ordinal if c != col] if kind == 'ordinal' else full_ordinal
        auc, sd = fit_eval_auroc(d, outer, nums, nominal, ordinal)
        rows.append(dict(block_removed=block, mean_weighted_AUROC=auc, sd_weighted_AUROC=sd, auroc_cost=full_auc - auc))
        print(f'without {block}: weighted AUROC {auc:.4f} (cost {full_auc - auc:+.4f})', flush=True)
    return pd.DataFrame(rows).sort_values('auroc_cost', ascending=False)


def repeated_ablation(d, cbc_cols, seeds):
    """Same leave-one-block-out ablation as ablate_all_blocks, but repeated across
    multiple PSU-grouped fold seeds, to avoid trusting a single split's noise --
    the same lesson the CBC stability_check already surfaced (one split flagged
    MPV as selected when it wasn't reliably so)."""
    full_nums = NUM + ['BMXBMI'] + cbc_cols
    full_nominal, full_ordinal = cfg.NOMINAL_DEMOGRAPHICS, cfg.ORDINAL_DEMOGRAPHICS
    blocks = {
        'age': ('num', 'RIDAGEYR'), 'income': ('num', 'INDFMPIR'), 'BMI': ('num', 'BMXBMI'),
        'sex': ('nominal', 'RIAGENDR'), 'race_ethnicity': ('nominal', 'RIDRETH3'),
        'education': ('ordinal', 'DMDEDUC2'), 'CBC_reduced': ('cbc', None),
    }
    costs = {b: [] for b in blocks}
    costs['none (full model)'] = []
    for seed in seeds:
        outer = ext.folds_for(d, seed=seed)
        full_auc, _ = fit_eval_auroc(d, outer, full_nums, full_nominal, full_ordinal)
        costs['none (full model)'].append(full_auc)
        for block, (kind, col) in blocks.items():
            nums = [c for c in full_nums if c != col] if kind == 'num' else \
                   [c for c in full_nums if c not in cbc_cols] if kind == 'cbc' else full_nums
            nominal = [c for c in full_nominal if c != col] if kind == 'nominal' else full_nominal
            ordinal = [c for c in full_ordinal if c != col] if kind == 'ordinal' else full_ordinal
            auc, _ = fit_eval_auroc(d, outer, nums, nominal, ordinal)
            costs[block].append(full_auc - auc)
        print(f'repeated ablation: seed {seed} complete', flush=True)
    rows = [dict(block_removed=b, mean_auroc_cost=np.mean(v), sd_auroc_cost=np.std(v), n_folds=len(v))
            for b, v in costs.items() if b != 'none (full model)']
    rows.append(dict(block_removed='none (full model)', mean_auroc_cost=0.0, sd_auroc_cost=0.0,
                     n_folds=len(costs['none (full model)'])))
    rows_df = pd.DataFrame(rows).sort_values('mean_auroc_cost', ascending=False)
    rows_df['full_model_mean_weighted_AUROC'] = np.mean(costs['none (full model)'])
    rows_df['full_model_sd_weighted_AUROC'] = np.std(costs['none (full model)'])
    return rows_df


def repeated_fit_eval(d, nums, nominal, ordinal, seeds):
    aucs = []
    for seed in seeds:
        outer = ext.folds_for(d, seed=seed)
        for train, test in outer:
            z = d.iloc[train]
            cats = nominal + ordinal
            transforms = [('numeric', Pipeline([('impute', SimpleImputer(strategy='median', add_indicator=True)),
                                                ('scale', StandardScaler())]), nums)] if nums else []
            transforms += categorical_entries_for(nominal, ordinal)
            model = Pipeline([('pre', ColumnTransformer(transforms)),
                              ('sparse', FunctionTransformer(csr_matrix, accept_sparse=True)),
                              ('clf', LogisticRegression(solver='liblinear', max_iter=2000))])
            w = z._weight.to_numpy()
            model.fit(z[nums + cats], z.target, clf__sample_weight=w / w.mean())
            p = model.predict_proba(d.iloc[test][nums + cats])[:, 1]
            wt = d.iloc[test]._weight.to_numpy()
            aucs.append(roc_auc_score(d.iloc[test].target, p, sample_weight=wt))
    return np.mean(aucs), np.std(aucs), len(aucs)


def marginal_addition_test(d, base_cbc, candidates, seeds):
    """For each currently-dropped CBC feature, test adding it back to the base
    set alone and measure the weighted-AUROC delta via repeated PSU-grouped CV.

    This exists because an L1/knee selection can arbitrarily drop one feature
    from a severely collinear pair even when that feature carries real,
    non-redundant information -- e.g. with only 3 of the 5 differential
    percentages kept, the other 2 are NOT algebraically determined by the 3
    (only their *sum* is, via the ~100% compositional constraint), so dropping
    one of them is a real information loss, not a safe redundancy removal like
    MCH/MCHC/the absolute counts. Per team instruction: keep anything that
    shows even a small, real gain -- these features are cheap to keep.
    """
    nominal, ordinal = cfg.NOMINAL_DEMOGRAPHICS, cfg.ORDINAL_DEMOGRAPHICS
    base_nums = NUM + ['BMXBMI'] + base_cbc
    base_auc, base_sd, n = repeated_fit_eval(d, base_nums, nominal, ordinal, seeds)
    rows = [dict(feature='(base only)', mean_weighted_AUROC=base_auc, sd_weighted_AUROC=base_sd,
                auroc_gain=0.0, gain_sd_ratio=0.0)]
    for feat in candidates:
        nums = base_nums + [feat]
        auc, sd, _ = repeated_fit_eval(d, nums, nominal, ordinal, seeds)
        gain = auc - base_auc
        rows.append(dict(feature=feat, mean_weighted_AUROC=auc, sd_weighted_AUROC=sd,
                         auroc_gain=gain, gain_sd_ratio=gain / sd if sd else np.nan))
        print(f'[marginal add] +{feat}: weighted AUROC {auc:.4f} (gain {gain:+.4f}, {n} folds)', flush=True)
    return pd.DataFrame(rows).sort_values('auroc_gain', ascending=False)


def final_candidates_comparison(d, cbc_reduced, seeds):
    """Two completeness checks in one pass:
    (1) the actual bottom line -- proposed final model(s) vs. the current full
        27-feature baseline (demographics_bmi_cbc as used everywhere else in
        the pipeline) -- not just per-block costs.
    (2) whether income and education's ~0 individual ablation cost is because
        they substitute for each other (Spearman rho=0.50 between them): drop
        each alone vs. drop both together and compare the combined cost to the
        sum of the individual costs.
    """
    nominal = cfg.NOMINAL_DEMOGRAPHICS
    specs = {
        'original_full_27feat': (NUM + ['BMXBMI'] + CBC, nominal, cfg.ORDINAL_DEMOGRAPHICS),
        'reduced_keep_education': (['RIDAGEYR', 'BMXBMI'] + cbc_reduced, nominal, cfg.ORDINAL_DEMOGRAPHICS),
        'reduced_drop_education': (['RIDAGEYR', 'BMXBMI'] + cbc_reduced, nominal, []),
        'income_only_dropped_cbc21': (['RIDAGEYR', 'BMXBMI'] + CBC, nominal, cfg.ORDINAL_DEMOGRAPHICS),
        'education_only_dropped_cbc21': (NUM + ['BMXBMI'] + CBC, nominal, []),
        'both_income_and_education_dropped_cbc21': (['RIDAGEYR', 'BMXBMI'] + CBC, nominal, []),
    }
    rows = []
    for name, (nums, nom, ordi) in specs.items():
        mean_auc, sd_auc, n = repeated_fit_eval(d, nums, nom, ordi, seeds)
        rows.append(dict(spec=name, n_features=len(nums) + len(nom) + len(ordi),
                         mean_weighted_AUROC=mean_auc, sd_weighted_AUROC=sd_auc, n_folds=n))
        print(f'[final_candidates] {name}: weighted AUROC {mean_auc:.4f} +/- {sd_auc:.4f}', flush=True)
    return pd.DataFrame(rows)


def compare_feature_sets(d, sets, label):
    """Plain (unpenalized-equivalent, L2) PSU-grouped 5-fold weighted AUROC for
    a handful of named CBC feature sets, matching the rest of the pipeline's
    modeling convention (no L1), to quantify the cost of adding features back."""
    outer = ext.folds_for(d)
    rows = []
    for name, cbc_cols in sets.items():
        nums = NUM + ['BMXBMI'] + cbc_cols
        aucs = []
        for train, test in outer:
            z = d.iloc[train]
            pre = [('numeric', Pipeline([('impute', SimpleImputer(strategy='median', add_indicator=True)),
                                        ('scale', StandardScaler())]), nums)] + cfg.categorical_transformer_entries()
            model = Pipeline([('pre', ColumnTransformer(pre)),
                              ('sparse', FunctionTransformer(csr_matrix, accept_sparse=True)),
                              ('clf', LogisticRegression(solver='liblinear', max_iter=2000))])
            w = z._weight.to_numpy()
            model.fit(z[nums + CAT], z.target, clf__sample_weight=w / w.mean())
            p = model.predict_proba(d.iloc[test][nums + CAT])[:, 1]
            wt = d.iloc[test]._weight.to_numpy()
            aucs.append(roc_auc_score(d.iloc[test].target, p, sample_weight=wt))
        rows.append(dict(comparison=label, feature_set=name, n_cbc_features=len(cbc_cols),
                         mean_weighted_AUROC=np.mean(aucs), sd_weighted_AUROC=np.std(aucs)))
        print(f'[{label}] {name} ({len(cbc_cols)} CBC features): weighted AUROC '
              f'{np.mean(aucs):.4f} +/- {np.std(aucs):.4f}', flush=True)
    return pd.DataFrame(rows)


def main():
    full, d = ext.load_cycle('L')
    assert len(d) == 4612 and d.target.sum() == 106
    # ext.load_cycle merges only cfg.COMPLETE_PANEL_FEATURES (now the locked 9-feature REDUCED
    # block) -- this script needs the full INITIAL 21-column panel to explore reduction *from*,
    # so merge in whatever INITIAL columns aren't already present. CBC completeness is all-or-
    # nothing in this data (verified independently), so this adds columns, not rows or NaNs.
    missing_cols = [c for c in CBC if c not in d.columns]
    if missing_cols:
        cbc_raw = ext.read(ROOT / 'data/raw/2021_2023/CBC_L.xpt')
        d = d.merge(cbc_raw[['SEQN'] + missing_cols], on='SEQN', how='left', validate='one_to_one')
        assert d[missing_cols].notna().all().all()

    # --- VIF across all three candidate CBC blocks ---
    rows = vif_table(d[CBC], d._weight.to_numpy(), 'full_21')
    rows += vif_table(d[CANDIDATE_14], d._weight.to_numpy(), 'candidate_14_drop_algebraic')
    rows += vif_table(d[CANDIDATE_13], d._weight.to_numpy(), 'candidate_13_drop_algebraic_and_baso')
    vif = pd.DataFrame(rows)
    vif.to_csv(OUT / 'reduction_vif.csv', index=False)
    top = {b: vif.loc[(vif.block == b) & (vif.weighting == 'survey_weighted')].nlargest(4, 'VIF')[['variable', 'VIF']].to_dict('records')
           for b in ['full_21', 'candidate_14_drop_algebraic', 'candidate_13_drop_algebraic_and_baso']}

    # --- L1 path on the naive full 21 vs. the properly de-redundanced 13 ---
    outer = ext.folds_for(d)
    Cs = np.logspace(-3, 1, 25)
    path_21 = l1_path(d, outer, CBC, 'full_21', Cs)
    path_13 = l1_path(d, outer, CANDIDATE_13, 'candidate_13', Cs)
    path = pd.concat([path_21, path_13], ignore_index=True)
    path.to_csv(OUT / 'lasso_path.csv', index=False)

    knee21, best21 = knee_row(path_21)
    knee13, best13 = knee_row(path_13)
    kept21, dropped21 = selection_at(knee21)
    kept13, dropped13 = selection_at(knee13)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for label, p, knee in [('full_21', path_21, knee21), ('candidate_13', path_13, knee13)]:
        axes[0].errorbar(p.C, p.mean_weighted_AUROC, yerr=p.sd_weighted_AUROC, marker='o', ms=3, label=label)
        axes[1].plot(p.C, p.n_cbc_selected_mean, marker='o', ms=3, label=label)
    axes[0].set_xscale('log'); axes[0].legend(fontsize=8)
    axes[0].set(xlabel='C (inverse L1 penalty, log scale)', ylabel='Weighted AUROC (5-fold mean)',
                title='Development-only L1 path: AUROC vs. regularization')
    axes[1].set_xscale('log'); axes[1].legend(fontsize=8)
    axes[1].set(xlabel='C (inverse L1 penalty, log scale)', ylabel='Mean CBC features with nonzero coef (across 5 folds)',
                title='CBC features retained vs. regularization')
    fig.tight_layout()
    fig.savefig(OUT / 'lasso_path.png', dpi=160)
    plt.close(fig)

    # --- Stability check: is the knee-point selection a one-split artifact? ---
    seeds = [42, 1, 2, 3, 4]
    stability, stab_auc_mean, stab_auc_sd = stability_check(d, CANDIDATE_13, float(knee13.C), 'candidate_13_knee', seeds)
    stability.to_csv(OUT / 'stability_check.csv', index=False)
    stable_kept = stability.loc[stability.selection_rate >= 0.6, 'variable'].tolist()
    unstable = stability.loc[(stability.selection_rate > 0.2) & (stability.selection_rate < 0.6), 'variable'].tolist()

    # --- Cost of restoring HGB/HCT for clinical face validity ---
    knee8 = kept13  # the 8 features L1 kept at the candidate_13 knee
    comparison = compare_feature_sets(d, {
        'knee_8': knee8,
        'knee_8_plus_hgb_hct': knee8 + ['LBXHGB', 'LBXHCT'],
        'candidate_13_full': CANDIDATE_13,
    }, 'hgb_hct_face_validity')
    comparison.to_csv(OUT / 'hgb_hct_comparison.csv', index=False)

    # --- All-feature ablation: age, income, sex, race, education, BMI, and the
    # reduced CBC block -- not just CBC -- each tested for removal in turn. ---
    ablation = ablate_all_blocks(d, outer, CBC_REDUCED_9)
    ablation.to_csv(OUT / 'all_feature_ablation.csv', index=False)

    repeated = repeated_ablation(d, CBC_REDUCED_9, seeds)
    repeated.to_csv(OUT / 'all_feature_ablation_repeated.csv', index=False)

    finals = final_candidates_comparison(d, CBC_REDUCED_9, seeds)
    finals.to_csv(OUT / 'final_candidates_comparison.csv', index=False)

    # --- Marginal addition test: does any currently-dropped CBC feature matter
    # even a little, individually, when added back to the 9-feature base? ---
    dropped_from_9 = [c for c in CBC if c not in CBC_REDUCED_9]
    assert len(dropped_from_9) == 12
    marginal = marginal_addition_test(d, CBC_REDUCED_9, dropped_from_9, seeds)
    marginal.to_csv(OUT / 'marginal_addition_test.csv', index=False)

    summary = dict(
        candidate_14_drop_algebraic=CANDIDATE_14, algebraically_redundant_dropped=ALGEBRAICALLY_REDUNDANT,
        candidate_13_drop_algebraic_and_baso=CANDIDATE_13, compositionally_redundant_dropped=COMPOSITIONALLY_REDUNDANT,
        vif_top4=top,
        l1_full_21=dict(knee_C=float(knee21.C), knee_weighted_AUROC=float(knee21.mean_weighted_AUROC),
                        best_weighted_AUROC=float(best21), kept_in_ge3_of_5_folds=kept21, dropped_in_lt3_of_5_folds=dropped21),
        l1_candidate_13=dict(knee_C=float(knee13.C), knee_weighted_AUROC=float(knee13.mean_weighted_AUROC),
                             best_weighted_AUROC=float(best13), kept_in_ge3_of_5_folds=kept13, dropped_in_lt3_of_5_folds=dropped13),
        stability_check=dict(seeds=seeds, total_folds=len(seeds) * 5, weighted_AUROC_mean=stab_auc_mean,
                             weighted_AUROC_sd=stab_auc_sd, stably_kept_rate_ge_60pct=stable_kept,
                             unstable_20_to_60pct=unstable),
        hgb_hct_face_validity=comparison.to_dict('records'),
        cbc_reduced_9=CBC_REDUCED_9,
        all_feature_ablation=ablation.to_dict('records'),
        all_feature_ablation_repeated=repeated.to_dict('records'),
        final_candidates_comparison=finals.to_dict('records'),
        marginal_addition_test=marginal.to_dict('records'))
    (OUT / 'reduction_summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
