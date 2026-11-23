"""Single source of truth for the cohort/endpoint/feature decisions every
analysis script and notebook should share.

Before this file existed, the same eligibility rule was copy-pasted into
research_extension.py, cohort_analysis.py and weighted_calibration_analysis.py
(all three agreed), while notebooks/02_baseline_model_and_figures.ipynb and
notebooks/03_survey_design.ipynb each used a looser, different rule. Edit the
values below to change the study definition everywhere at once; every
consumer imports from here instead of redefining its own copy.

Team decision (2026-11-20 meeting, adopted here as canonical): adopt the
stricter values already used by research_extension.py, rather than the looser
ones in notebooks 02/03 -- those notebooks are the ones that need to change
to match this file, not the other way around.
"""

# ---- NHANES raw column names, grouped by what they mean ----
AGE_COL = "RIDAGEYR"
SEX_COL = "RIAGENDR"              # 1 = male, 2 = female
RACE_ETH_COL = "RIDRETH3"
EDUCATION_COL = "DMDEDUC2"        # 7/9 (refused/don't know) must be recoded to NaN before use
INCOME_COL = "INDFMPIR"
EXAM_STATUS_COL = "RIDSTATR"      # 2 = also attended the Mobile Examination Center (MEC)
DIAGNOSIS_COL = "DIQ010"          # 1=yes, 2=no, 3=borderline, 7=refused, 9=don't know
INSULIN_COL = "DIQ050"            # 1 = currently taking insulin
PILLS_COL = "DIQ070"              # 1 = currently taking diabetic pills
PREGNANCY_COL = "RIDEXPRG"        # 1 = positive pregnancy test, 2 = not pregnant (public for women 20-44 only)
HBA1C_COL = "LBXGH"
PHLEBOTOMY_WEIGHT_COL = "WTPH2YR"
FASTING_WEIGHT_COL = "WTSAF2YR"
STRATUM_COL = "SDMVSTRA"
PSU_COL = "SDMVPSU"

# ---- Cohort eligibility (team decision) ----
MIN_AGE = 20
REQUIRE_EXAM_STATUS = 2           # must be MEC-examined, not interview-only
NO_PRIOR_DIAGNOSIS_CODE = 2       # DIQ010 must equal exactly this (borderline/code 3 is EXCLUDED)
BORDERLINE_DIAGNOSIS_CODE = 3     # DIQ010 "borderline/prediabetes" -- excluded by default, used only
                                  # in explicit sensitivity analyses that test including it
EXCLUDE_INSULIN_USERS = True      # DIQ050 == 1 excluded
EXCLUDE_DIABETES_PILL_USERS = True  # DIQ070 == 1 excluded
EXCLUDE_CONFIRMED_PREGNANT = True   # RIDEXPRG == 1 excluded
# Pregnancy status is only publicly reported for women aged 20-44 ("the band").
# Inside that band we require a CONFIRMED not-pregnant result (code 2), not just
# "not a confirmed positive" -- a missing/unascertainable result inside the band
# is excluded too. Outside the band, pregnancy status doesn't apply.
PREGNANCY_BAND_SEX = 2            # female
PREGNANCY_BAND_AGE = (20, 44)
REQUIRE_CONFIRMED_NONPREGNANT_IN_BAND = True

# ---- Outcome ----
PRIMARY_CUT = 6.5   # HbA1c >= 6.5%: the primary, prespecified diabetes-range label
SECONDARY_CUT = 5.7  # HbA1c >= 5.7%: secondary/exploratory only, never the primary label

# ---- CBC feature block: INITIAL (where we started) vs REDUCED (where Phase 15 got to) ----
#
# INITIAL (team decision, 2026-11-23 cohort-summary table): keep all 21 CBC variables --
# supersedes the earlier stricter 11-feature set that excluded MCH, MCHC, MPV, basophil %
# and the five LBD*NO absolute counts. This is the block every already-published result in
# this repo (docs/findings/*, results/*) was computed with.
RED_CELL_FEATURES_INITIAL = ["LBXRBCSI", "LBXHGB", "LBXHCT", "LBXMCVSI", "LBXMCHSI", "LBXMC",
                             "LBXRDW", "LBXNRBC"]  # RBC count, Hgb, Hct, MCV, MCH, MCHC, RDW, NRBC
WHITE_CELL_PLATELET_FEATURES_INITIAL = ["LBXWBCSI", "LBXPLTSI", "LBXMPSI",
                                        "LBXLYPCT", "LBXNEPCT", "LBXMOPCT", "LBXEOPCT", "LBXBAPCT",
                                        "LBDLYMNO", "LBDNENO", "LBDMONO", "LBDEONO", "LBDBANO"]
                                        # WBC, platelets, MPV, 5-part differential (% and absolute)
CBC_FEATURES_INITIAL = RED_CELL_FEATURES_INITIAL + WHITE_CELL_PLATELET_FEATURES_INITIAL  # 21 features

# REDUCED (Phase 15 feature-reduction candidate, 2026-11-23; see docs/findings/feature_reduction.md
# and scripts/analysis/feature_reduction.py). Not yet locked as the project's canonical block --
# kept alongside INITIAL so scripts/phase-2/ can run and compare both. Every one of the 12
# dropped columns was tested by direct marginal-addition (add it back alone, measure AUROC
# over 25 repeated PSU-grouped folds) and showed no measurable gain (all within +/-8% of their
# own fold-to-fold SD -- noise level), so this is not just a parsimony trade-off.
RED_CELL_FEATURES_REDUCED = ["LBXRBCSI", "LBXHGB", "LBXHCT", "LBXMCVSI"]
WHITE_CELL_PLATELET_FEATURES_REDUCED = ["LBXWBCSI", "LBXPLTSI", "LBXLYPCT", "LBXMOPCT", "LBXEOPCT"]
CBC_FEATURES_REDUCED = RED_CELL_FEATURES_REDUCED + WHITE_CELL_PLATELET_FEATURES_REDUCED  # 9 features

# ---- LOCKED (2026-11-23 team decision, Phase 15 Step 3): the unqualified names every script
# reads now resolve to REDUCED, not INITIAL. Validated via scripts/phase-2/'s full pipeline
# re-run (bootstrap, independent-cycle transport) in docs/findings/phase2_feature_variant_comparison.md --
# the reduced set won on every logistic model and every scenario tested. INITIAL is kept above,
# unchanged, as the historical starting point and is still what scripts/phase-2/ compares against. ----
RED_CELL_FEATURES = RED_CELL_FEATURES_REDUCED
WHITE_CELL_PLATELET_FEATURES = WHITE_CELL_PLATELET_FEATURES_REDUCED
CBC_FEATURES = CBC_FEATURES_REDUCED  # 9 features total
COMPLETE_PANEL_FEATURES = CBC_FEATURES  # kept as an alias: "complete panel" now equals the model feature set

# ---- Demographic baseline: INITIAL vs REDUCED ----
#
# INITIAL: age + income (where every already-published result was computed).
# REDUCED (Phase 15): income dropped -- near-zero/negative marginal AUROC contribution in both
# the direct ablation and the pre-existing permutation-importance findings (convergent evidence
# across two methods; see docs/findings/feature_reduction.md). Education is NOT dropped here:
# ablation and permutation importance disagreed on it, and dropping it together with income
# costs ~8x more than the sum of dropping each alone (they're correlated, rho=0.50) -- so
# education stays in both INITIAL and REDUCED.
NUMERIC_DEMOGRAPHICS_INITIAL = [AGE_COL, INCOME_COL]
NUMERIC_DEMOGRAPHICS_REDUCED = [AGE_COL]
NUMERIC_DEMOGRAPHICS = NUMERIC_DEMOGRAPHICS_REDUCED  # locked default (2026-11-23, Phase 15 Step 3): income dropped

NOMINAL_DEMOGRAPHICS = [SEX_COL, RACE_ETH_COL]      # one-hot encoded: no natural order; same in both variants
ORDINAL_DEMOGRAPHICS = [EDUCATION_COL]              # ordinal encoded (team decision, below); same in both variants
CATEGORICAL_DEMOGRAPHICS = NOMINAL_DEMOGRAPHICS + ORDINAL_DEMOGRAPHICS  # kept for descriptive/legacy use

# ---- Named variants for scripts/phase-2/ to run/compare both "where we started" and "where we
# are now" without each one re-deriving the same lists. Legend labels are for figures/tables. ----
FEATURE_SET_VARIANTS = {
    "initial": dict(
        label="Initial (21 CBC features + income)",
        cbc_features=CBC_FEATURES_INITIAL,
        red_cell_features=RED_CELL_FEATURES_INITIAL,
        white_cell_platelet_features=WHITE_CELL_PLATELET_FEATURES_INITIAL,
        numeric_demographics=NUMERIC_DEMOGRAPHICS_INITIAL,
    ),
    "reduced": dict(
        label="Reduced (9 CBC features, no income)",
        cbc_features=CBC_FEATURES_REDUCED,
        red_cell_features=RED_CELL_FEATURES_REDUCED,
        white_cell_platelet_features=WHITE_CELL_PLATELET_FEATURES_REDUCED,
        numeric_demographics=NUMERIC_DEMOGRAPHICS_REDUCED,
    ),
}

# ---- Education encoding (team decision, notebooks/Phase 6.ipynb) ----
# Ordinal vs one-hot gave no measurable AUROC difference (0.727 vs 0.727 logistic,
# 0.733 vs 0.732 forest, on that notebook's own exploratory cohort). Ordinal was chosen
# because education has a natural order, it adds one feature instead of five, and it
# avoids sparse indicator columns for small categories. Revisit only if a later analysis
# needs to report education effects in detail (ordinal assumes equal gaps between levels).
EDUCATION_ENCODING = "ordinal"
EDUCATION_LEVELS = [1, 2, 3, 4, 5]  # DMDEDUC2, <9th grade (1) to college graduate+ (5); 7/9 -> NaN upstream

# ---- Evaluation ----
RANDOM_SEED = 42


def categorical_transformer_entries(impute_strategy="most_frequent", impute_fill_value=None):
    """ColumnTransformer entries for the team's demographic categorical encoding:
    sex/race one-hot (nominal), education ordinal (team decision, Phase 6).

    Returns [("nominal", Pipeline, NOMINAL_DEMOGRAPHICS), ("ordinal", Pipeline, ORDINAL_DEMOGRAPHICS)]
    ready to splice into a ColumnTransformer's transformer list. Pass `impute_fill_value` to use
    a constant-fill imputer (e.g. -1) instead of most-frequent, matching a caller's own convention.
    """
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

    def _imputer():
        if impute_fill_value is not None:
            return SimpleImputer(strategy="constant", fill_value=impute_fill_value)
        return SimpleImputer(strategy=impute_strategy)

    nominal = Pipeline([("impute", _imputer()),
                        ("encode", OneHotEncoder(handle_unknown="ignore", sparse_output=False))])
    ordinal = Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                        ("encode", OrdinalEncoder(categories=[EDUCATION_LEVELS],
                                                   handle_unknown="use_encoded_value", unknown_value=-1))])
    return [("nominal", nominal, NOMINAL_DEMOGRAPHICS), ("ordinal", ordinal, ORDINAL_DEMOGRAPHICS)]


def eligibility_mask(df, weight_col=PHLEBOTOMY_WEIGHT_COL):
    """The team-agreed eligibility rule, built from the columns above.

    `df` must already have SDMVSTRA/SDMVPSU/RIDSTATR/DIQ010/DIQ050/DIQ070/
    RIDEXPRG/RIDAGEYR/RIAGENDR and a positive-weight column loaded. Pass
    `weight_col` for a cycle that doesn't carry WTPH2YR (e.g. an older
    independent-validation cycle using WTMEC2YR instead).
    """
    in_band = (df[SEX_COL].eq(PREGNANCY_BAND_SEX)
               & df[AGE_COL].between(*PREGNANCY_BAND_AGE))
    pregnancy_ok = ~df[PREGNANCY_COL].eq(1) if EXCLUDE_CONFIRMED_PREGNANT else True
    if REQUIRE_CONFIRMED_NONPREGNANT_IN_BAND:
        pregnancy_ok = pregnancy_ok & (~in_band | df[PREGNANCY_COL].eq(2))

    mask = (df[EXAM_STATUS_COL].eq(REQUIRE_EXAM_STATUS)
            & df[weight_col].gt(0)
            & df[AGE_COL].ge(MIN_AGE)
            & df[DIAGNOSIS_COL].eq(NO_PRIOR_DIAGNOSIS_CODE)
            & pregnancy_ok)
    if EXCLUDE_INSULIN_USERS:
        mask = mask & ~df[INSULIN_COL].eq(1)
    if EXCLUDE_DIABETES_PILL_USERS:
        mask = mask & ~df[PILLS_COL].eq(1)
    return mask
