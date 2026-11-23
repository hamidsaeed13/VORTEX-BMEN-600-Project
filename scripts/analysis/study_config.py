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

# ---- CBC feature block (team decision: the stricter 11-feature set) ----
# Excludes MCH, MCHC, MPV and basophil % relative to the full panel -- the
# looser 15-feature set some notebooks used is NOT the canonical one.
RED_CELL_FEATURES = ["LBXRBCSI", "LBXHGB", "LBXHCT", "LBXMCVSI", "LBXRDW"]
WHITE_CELL_PLATELET_FEATURES = ["LBXWBCSI", "LBXPLTSI", "LBXLYPCT", "LBXNEPCT", "LBXMOPCT", "LBXEOPCT"]
CBC_FEATURES = RED_CELL_FEATURES + WHITE_CELL_PLATELET_FEATURES  # 11 features total
BASOPHIL_COL = "LBXBAPCT"  # required for a *complete panel* check, but not used as a model feature
                           # (dropped from modeling: the 5-part differential is compositional data)
COMPLETE_PANEL_FEATURES = CBC_FEATURES + [BASOPHIL_COL]  # 12: what "drew a full CBC panel" means

# ---- Demographic baseline ----
NUMERIC_DEMOGRAPHICS = [AGE_COL, INCOME_COL]
NOMINAL_DEMOGRAPHICS = [SEX_COL, RACE_ETH_COL]      # one-hot encoded: no natural order
ORDINAL_DEMOGRAPHICS = [EDUCATION_COL]              # ordinal encoded (team decision, below)
CATEGORICAL_DEMOGRAPHICS = NOMINAL_DEMOGRAPHICS + ORDINAL_DEMOGRAPHICS  # kept for descriptive/legacy use

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
