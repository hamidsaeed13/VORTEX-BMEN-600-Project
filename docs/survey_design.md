# Phase 8: Survey design decisions

**Notebook:** `code/03_survey_design.ipynb`

## Weights and design variables
- **CBC/HbA1c analyses:** `WTPH2YR` (phlebotomy weight), found in `CBC_L` and `GHB_L`. Participants with weight = 0 are excluded.
- **Fasting-glucose analyses:** `WTSAF2YR` (from `GLU_L`), fasting subsample only.
- **Design variables kept:** `SDMVSTRA` (strata) and `SDMVPSU` (clusters), found in `DEMO_L`, for design-aware confidence intervals.
- SAS near-zero values (e.g., 5.4e-79) were set to 0 before any weight filtering.

## Analytic cohort
Adults ≥18 years, no prior diabetes diagnosis (DIQ010 not 1/7/9), not pregnant, WTPH2YR > 0, HbA1c available.
Merged participants: 7,199 → analytic cohort: **5,144**.

## Unweighted vs weighted prevalence

| Outcome | Cases (n) | Unweighted % | Weighted % |
|---|---|---|---|
| HbA1c ≥5.7% | 1,552 | 30.2 | 26.4 |
| HbA1c ≥6.5% | 152 | 3.0 | 2.5 |

## Interpretation
- The unweighted sample overstates prevalence because NHANES oversamples higher-risk groups. Population-level estimates must use WTPH2YR.
- Only 152 undiagnosed participants reach HbA1c ≥6.5%, which supports HbA1c ≥5.7% as the primary outcome, with ≥6.5% as secondary.

## What our numbers mean
- Model training and case counts describe the **NHANES sample**.
- Prevalence and performance reported with WTPH2YR estimate the **U.S. adult population** without diagnosed diabetes.
- Class-balancing weights (e.g., `class_weight="balanced"`) are a modelling choice and are kept separate from survey weights.

## Still to do
- Design-aware 95% confidence intervals using SDMVSTRA/SDMVPSU (links to the uncertainty plan).