# Phase 8: Survey design and analytic cohort (team-agreed rules)

**Notebook:** `notebooks/03_survey_design.ipynb` (cell 1). Eligibility values come from the
single shared `scripts/analysis/study_config.py`, not from constants local to this notebook.

## Eligibility rules (from `scripts/analysis/study_config.py`)

- Examined (MEC), age 20 years or older
- Explicit "no" prior diabetes diagnosis (DIQ010 = 2 only): diagnosed (1), borderline/prediabetes
  (3), refused (7), don't know (9), and missing responses are all excluded
- No reported current insulin or diabetic-pill use (DIQ050/DIQ070 = 1 excluded)
- Pregnancy-clear: confirmed-positive pregnancy test excluded (RIDEXPRG = 1); for women aged
  20-44, an unascertained result is also excluded (RIDEXPRG must equal 2, not just "not 1")
- Valid phlebotomy weight (WTPH2YR > 0) and HbA1c available

## Cohort flow

| Step | Participants |
|---|---|
| Has CBC and HbA1c records | 7,199 |
| Examined (MEC), age 20+ | 6,064 |
| No prior diabetes diagnosis (explicit "no"; borderline/refused/missing excluded) | 4,975 |
| No insulin or diabetic-pill use | 4,934 |
| Pregnancy-clear (confirmed not pregnant for women 20-44) | 4,865 |
| Valid weight and HbA1c (analytic cohort) | **4,636** |

## Prevalence

| Outcome | Cases (n) | Unweighted % | Weighted % |
|---|---|---|---|
| Primary: HbA1c ≥6.5% | 106 | 2.3 | 2.0 |
| Secondary: HbA1c ≥5.7% | 1,356 | 29.2 | 25.6 |

## Weights and design variables

- WTPH2YR (CBC_L, GHB_L) is used for all CBC/HbA1c estimates and for survey-weighted AUROC.
- SDMVSTRA and SDMVPSU (DEMO_L) are kept for design-based confidence intervals.
- WTSAF2YR (GLU_L) applies only to fasting-glucose analyses.
- SAS near-zero values (e.g., 5.4e-79) are set to 0 before weight filtering.
- Unweighted numbers describe the NHANES sample; weighted numbers estimate U.S. adults without diagnosed diabetes.

## Note on the 2026-11-20 team decision

This cohort (4,636 participants, 106 positives) is close to but not identical to the 4,612/106
used by the official `scripts/analysis/research_extension.py` pipeline, even though both now
read the same eligibility rule from `study_config.py`. The remaining 24-participant gap is a
separate, still-open modeling choice: this notebook allows a participant with a partially
missing CBC panel (imputed later), while `research_extension.py` requires a fully complete
21-feature panel at eligibility time. That difference is not part of the shared config and
should be reconciled separately if an exact match is needed.