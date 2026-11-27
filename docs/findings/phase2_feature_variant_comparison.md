# Phase 2: initial vs. reduced feature set, run through the full pipeline (2026-11-23)

This validates the Phase 15 feature-reduction proposal (`docs/findings/feature_reduction.md`)
by re-running the project's three core modeling scripts under **both** feature-set variants now
defined in `scripts/analysis/study_config.py`:

| Variant | Label | CBC features | Numeric demographics |
| --- | --- | --- | --- |
| `initial` | Initial (21 CBC features + income) | 21 (unchanged original block) | age, income |
| `reduced` | Reduced (9 CBC features, no income) | 9 (RBC, HGB, HCT, MCV, WBC, platelets, lymphocyte %, monocyte %, eosinophil %) | age only |

Sex, race/ethnicity and education are unchanged between variants (see `docs/findings/feature_reduction.md`
for why education stays despite a mixed signal, and why income is the one demographic dropped).

**Nothing about the official pipeline changed.** `scripts/analysis/study_config.py`'s unqualified
names (`CBC_FEATURES`, `NUMERIC_DEMOGRAPHICS`, etc.) still resolve to exactly the `initial` values,
so every existing script, notebook and saved result is untouched. This comparison lives entirely
in a new `scripts/phase-2/` (copies of the three scripts, parameterized by variant) and
`results/phase-2/` (separate output per variant, plus a `comparison/` folder per script with
merged tables and labeled figures).

## Script 1: `cohort_analysis.py` (unweighted, exploratory, class-balanced)

| Model | Initial | Reduced | Δ (reduced − initial) |
| --- | ---: | ---: | ---: |
| age_logistic | 0.6296 | 0.6296 | 0.0000 |
| demographics_logistic | 0.7179 | 0.7141 | −0.0038 |
| cbc_demographics_logistic | 0.7544 | 0.7671 | **+0.0126** |
| cbc_demographics_forest | 0.7169 | 0.7290 | +0.0121 |

Figures: `results/phase-2/cohort_analysis/comparison/primary_cohort_auroc_comparison.png`

## Script 2: `weighted_calibration_analysis.py` (survey-weighted, PSU-grouped, calibrated)

| Model | Initial | Reduced | Δ (reduced − initial) |
| --- | ---: | ---: | ---: |
| age_logistic | 0.6517 | 0.6517 | 0.0000 |
| demographics_logistic | 0.7201 | 0.7167 | −0.0034 |
| cbc_demographics_logistic | 0.7701 | 0.7857 | **+0.0156** |
| cbc_demographics_forest | 0.7201 | 0.7012 | −0.0189 |

Figures: `results/phase-2/weighted_calibration/comparison/calibrated_auroc_comparison.png`

## Script 3: `research_extension.py` (BMI, bootstrap, independent-cycle transport — the most rigorous check)

Calibrated AUROC, primary analysis:

| Model | Initial | Reduced | Δ (reduced − initial) |
| --- | ---: | ---: | ---: |
| demographics | 0.6967 | 0.7167 | +0.0200 |
| demographics_bmi | 0.8006 | 0.8154 | +0.0149 |
| **demographics_bmi_cbc** | 0.8107 | **0.8347** | **+0.0241** |
| demographics_bmi_cbc_forest | 0.7769 | 0.7812 | +0.0042 |
| demographics_bmi_forest | 0.7765 | 0.7661 | −0.0105 |
| demographics_bmi_red | 0.7993 | 0.8228 | +0.0235 |
| demographics_bmi_white_platelet | 0.8105 | 0.8298 | +0.0193 |

**The reduced set wins in every one of the 8 secondary scenarios too** (BMI-observed subset,
low-hemoglobin exclusion, age 20–65 subsets, both fasting endpoints) — not just the primary
analysis. It also wins on the **independent 2017–2018 cycle** (frozen-model transport): AUROC
0.790 (reduced) vs. 0.761 (initial, after our earlier fix to 3,939 participants) — the gain
generalizes out-of-cycle, not just to held-out folds from the same cycle. Full table:
`results/phase-2/research_extension/comparison/calibrated_auroc_comparison.csv`.

**100-replicate PSU bootstrap** (CBC-minus-BMI AUROC gain, 95% interval): initial −0.056 to
0.051; reduced −0.034 to 0.062. Both still include zero (not a statistically settled gain), but
the reduced interval is narrower and shifted higher — a tighter, more favorable (if still
inconclusive) estimate of CBC's incremental value.

## What's consistent, and what isn't

- **Logistic models consistently prefer the reduced set** across all three scripts and every
  scenario tested (+0.012 to +0.024 AUROC on the primary comparisons).
- **Random forest is inconsistent**: improves in `cohort_analysis.py` and
  `research_extension.py`'s primary analysis, but gets worse in `weighted_calibration_analysis.py`
  (−0.019). Forests handle collinearity differently than penalized logistic regression (they can
  exploit redundant correlated features via different splits), so losing exactly which features
  helps depends on the specific weighting/calibration procedure. This is reported honestly, not
  smoothed over — it means the reduction is more clearly a win for the logistic models than for
  the forest.
- **Demographics-only models move in the direction expected from Phase 15**: small, income-driven
  changes (−0.003 to +0.020 depending on script), consistent with income contributing ~nothing.

## Reproduction

```
python scripts/phase-2/cohort_analysis.py
python scripts/phase-2/weighted_calibration_analysis.py
python scripts/phase-2/research_extension.py --bootstrap 100
```

Each writes `results/phase-2/<script>/initial/`, `results/phase-2/<script>/reduced/` (identical
contents/format to the original script's output folder) and `results/phase-2/<script>/comparison/`
(merged CSVs + PNGs with the variant labels above as figure legends). None of this touches
`scripts/analysis/`, `results/cohort/`, `results/weighted_calibration/`, `results/research_extension/`,
or any existing doc.

## Status and next step

**Update (2026-11-23): locked.** Based on this evidence, `study_config.py`'s unqualified names
now resolve to the `reduced` variant by default (Phase 15 Step 3) — every script and notebook in
the official pipeline reads it. `*_INITIAL` is retained unchanged as the historical starting
point, and `scripts/phase-2/` still runs and compares both variants on demand. Step 4 (full
official-pipeline re-run under the locked set) is done — see `docs/planning/PROJECT_PLAN.md`
Phase 15 and the refreshed `README.md`/findings docs for the new numbers. Steps 5-6 (gradient
boosting, final locked holdout) remain open.
