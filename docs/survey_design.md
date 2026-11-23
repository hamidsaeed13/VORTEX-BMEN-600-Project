# Phase 8: Survey design and analytic cohort (team-agreed rules)

**Notebook:** `notebooks/03_survey_design.ipynb` (cell 1)

## Eligibility rules (set at the top of the notebook)
- Age 20 years or older
- Pregnant participants excluded (RIDEXPRG = 1)
- Prior diabetes diagnosis excluded: DIQ010 = 1 (yes), 7 (refused), 9 (don't know) or missing. DIQ010 = 3 (borderline) is kept, pending team confirmation.
- Valid phlebotomy weight (WTPH2YR > 0) and HbA1c available

## Cohort flow

| Step | Participants |
|---|---|
| Has CBC and HbA1c records | 7,199 |
| Age 20+ | 6,064 |
| Not pregnant | 6,023 |
| No prior diabetes diagnosis | 5,155 |
| Valid weight and HbA1c (analytic cohort) | **4,911** |

## Prevalence

| Outcome | Cases (n) | Unweighted % | Weighted % |
|---|---|---|---|
| Primary: HbA1c ≥6.5% | 152 | 3.1 | 2.6 |
| Secondary: HbA1c ≥5.7% | 1,541 | 31.4 | 27.3 |

## Weights and design variables
- WTPH2YR (CBC_L, GHB_L) is used for all CBC/HbA1c estimates and for survey-weighted AUROC.
- SDMVSTRA and SDMVPSU (DEMO_L) are kept for design-based confidence intervals.
- WTSAF2YR (GLU_L) applies only to fasting-glucose analyses.
- SAS near-zero values (e.g., 5.4e-79) are set to 0 before weight filtering.
- Unweighted numbers describe the NHANES sample; weighted numbers estimate U.S. adults without diagnosed diabetes.