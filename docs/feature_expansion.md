# Phase 9: Feature expansion (team-agreed rules, survey-weighted)

**Notebook:** `notebooks/03_survey_design.ipynb` (cells 2–5). Supersedes the earlier `04_feature_expansion.ipynb`.
Cohort and feature-block values come from the single shared `scripts/analysis/study_config.py`,
not from constants local to this notebook.

## Method

- Cohort: 4,636 adults from Phase 8 (`docs/survey_design.md`).
- Primary outcome HbA1c ≥6.5% (106 cases); secondary HbA1c ≥5.7% (1,356 cases).
- Baseline: age, sex and BMI.
- CBC block: the team's full 21-feature panel (`scripts/analysis/study_config.py`, team decision
  2026-11-23, same as `cbc_vars` in `02_baseline`): WBC, RBC, hemoglobin, hematocrit, MCV, MCH,
  MCHC, RDW, NRBC, platelets, MPV, and the 5-part differential as both percentages and absolute
  counts (lymphocyte, neutrophil, monocyte, eosinophil, basophil). Supersedes the earlier
  11-feature block, which excluded MCH, MCHC, MPV, NRBC, basophil % and the absolute counts.
- Logistic regression with median imputation and scaling inside the pipeline; 5-fold stratified CV repeated 5 times (25 splits, random_state=42).
- AUROC is survey-weighted (WTPH2YR) in each test fold; mean and SD across the 25 splits.
- Serum glucose and insulin excluded as predictors because they measure the outcome. hs-CRP log-transformed.

## Results: primary outcome (HbA1c ≥6.5%)

| Model | Features | Weighted AUROC | SD | Change vs age + sex + BMI |
|---|---|---|---|---|
| A: age + sex | 2 | 0.667 | 0.067 | −0.113 |
| A2: age + sex + BMI | 3 | 0.779 | 0.053 | 0.000 |
| B: A2 + CBC | 24 | 0.803 | 0.039 | +0.023 |
| C: A2 + CBC without red-cell | 16 | 0.795 | 0.050 | +0.015 |
| D: B + waist | 25 | 0.802 | 0.042 | +0.022 |
| E: B + hs-CRP | 25 | 0.827 | 0.041 | +0.048 |

Anemia check (421 anemic and 17 missing hemoglobin excluded; n = 4,198; 95 cases): A2 0.793, B 0.804 (+0.011).

Iron subgroup (ferritin/TfR measured only in women of reproductive age): 1,076 people, 15 cases at ≥6.5%, too few to model.

## Results: secondary outcome (HbA1c ≥5.7%)

| Model | Features | Weighted AUROC | SD | Change vs age + sex + BMI |
|---|---|---|---|---|
| A: age + sex | 2 | 0.699 | 0.020 | −0.031 |
| A2: age + sex + BMI | 3 | 0.730 | 0.019 | 0.000 |
| B: A2 + CBC | 24 | 0.783 | 0.018 | +0.053 |
| C: A2 + CBC without red-cell | 16 | 0.749 | 0.019 | +0.018 |
| D: B + waist | 25 | 0.782 | 0.018 | +0.052 |
| E: B + hs-CRP | 25 | 0.789 | 0.017 | +0.058 |

## Interpretation
- BMI is the largest single contributor beyond age and sex.
- At ≥6.5%, the CBC adds a gain (+0.023) smaller than the split-to-split variation (SD ≈ 0.039) with only 106 cases, so the added value remains uncertain. Most of it comes from white-cell and platelet measures (+0.015 of the +0.023 total), and it persists after excluding anemic participants (+0.011).
- At ≥5.7%, the CBC gain is clearer (+0.053) and still mostly comes from red-cell measures (the non-red-cell arm alone gains only +0.018). This may partly reflect erythrocyte effects on HbA1c rather than glycemia (English et al.), so it should be interpreted cautiously.
- Waist and hs-CRP add little beyond the CBC.

## Changes from the earlier version

- Eligibility, outcome and feature-block values now come from `scripts/analysis/study_config.py`
  instead of this notebook's own local constants, so they stay in sync with `02_baseline` and the
  official `research_extension.py` pipeline.
- Prior-diagnosis handling tightened to an explicit "no" only (DIQ010 = 2): borderline/prediabetes
  is now excluded, resolving the "pending team confirmation" item from the previous version.
- Added insulin/diabetic-pill exclusion (not present before).
- Tightened the pregnancy rule: women aged 20-44 now need a confirmed not-pregnant result, not
  just the absence of a confirmed-positive one.
- CBC block narrowed from 15 to 11 features (drops MCH, MCHC, MPV and basophil %), then widened
  again to the full 21-feature panel on 2026-11-23 (adds back MCH, MCHC, MPV, NRBC, basophil %
  and the five absolute differential counts), matching the official pipeline's feature block
  exactly at each point.
- Cohort shrank from 4,911 to 4,636 and primary-outcome cases from 152 to 106 as a result of the
  eligibility tightening above; the later 11→21 feature-block change did not change this cohort's
  size (this notebook does not require a complete CBC panel at eligibility — see
  `docs/survey_design.md`). AUROC numbers in this file are all from the current 4,636/106 cohort
  and the current 21-feature block; they are not comparable to the pre-2026-11-20 version's
  numbers.

## Limitations and next steps
- Cross-validation only; no held-out test set yet.
- Design-based (PSU/strata) confidence intervals not yet computed.
- This cohort (4,636/106) is close to but not identical to the official pipeline's 4,612/106 --
  see the note in `docs/survey_design.md` on the remaining complete-CBC-panel difference.
