# Phase 9: Feature expansion (team-agreed rules, survey-weighted)

**Notebook:** `notebooks/03_survey_design.ipynb` (cells 2–5). Supersedes the earlier `04_feature_expansion.ipynb`.

## Method
- Cohort: 4,911 adults from Phase 8.
- Primary outcome HbA1c ≥6.5% (152 cases); secondary HbA1c ≥5.7% (1,541 cases).
- Baseline: age, sex and BMI.
- CBC block: the team's 15 features (same as `cbc_vars` in `02_baseline`): WBC, RBC, hemoglobin, hematocrit, MCV, MCH, MCHC, RDW, platelets, MPV, and lymphocyte, neutrophil, monocyte, eosinophil and basophil %.
- Logistic regression with median imputation and scaling inside the pipeline; 5-fold stratified CV repeated 5 times (25 splits, random_state=42).
- AUROC is survey-weighted (WTPH2YR) in each test fold; mean and SD across the 25 splits.
- Serum glucose and insulin excluded as predictors because they measure the outcome. hs-CRP log-transformed.

## Results: primary outcome (HbA1c ≥6.5%)

| Model | Features | Weighted AUROC | SD | Change vs age + sex + BMI |
|---|---|---|---|---|
| A: age + sex | 2 | 0.686 | 0.060 | −0.098 |
| A2: age + sex + BMI | 3 | 0.784 | 0.042 | 0.000 |
| B: A2 + CBC | 18 | 0.805 | 0.045 | +0.021 |
| C: A2 + CBC without red-cell | 11 | 0.800 | 0.041 | +0.016 |
| D: B + waist | 19 | 0.807 | 0.044 | +0.023 |
| E: B + hs-CRP | 19 | 0.822 | 0.050 | +0.038 |

Anemia check (451 anemic and 18 missing hemoglobin excluded; n = 4,442; 136 cases): A2 0.789, B 0.804 (+0.014).

Iron subgroup (ferritin/TfR measured only in women of reproductive age): 1,130 people, 19 cases at ≥6.5%, too few to model.

## Results: secondary outcome (HbA1c ≥5.7%)

| Model | Features | Weighted AUROC | SD | Change vs age + sex + BMI |
|---|---|---|---|---|
| A: age + sex | 2 | 0.705 | 0.017 | −0.032 |
| A2: age + sex + BMI | 3 | 0.736 | 0.015 | 0.000 |
| B: A2 + CBC | 18 | 0.787 | 0.012 | +0.051 |
| C: A2 + CBC without red-cell | 11 | 0.754 | 0.016 | +0.018 |
| D: B + waist | 19 | 0.787 | 0.012 | +0.050 |
| E: B + hs-CRP | 19 | 0.792 | 0.012 | +0.056 |

## Interpretation
- BMI is the largest single contributor beyond age and sex.
- At ≥6.5%, the CBC adds a small gain (+0.021) that is smaller than the split-to-split variation (SD ≈ 0.045) with only 152 cases, so the added value is uncertain. Most of it comes from white-cell and platelet measures, and it persists after excluding anemic participants (+0.014).
- At ≥5.7%, the CBC gain is clear (+0.051), but most of it comes from red-cell measures. This may partly reflect erythrocyte effects on HbA1c rather than glycemia (English et al.), so it should be interpreted cautiously.
- Waist and hs-CRP add little beyond the CBC.

## Changes from the earlier version
- Primary outcome changed to ≥6.5%; age 20+; BMI added to the baseline.
- CBC aligned to the team's 15 features: 5 absolute white-cell counts and nucleated RBC (LBXNRBC) removed.
- Anemia check now excludes participants with missing hemoglobin.
- AUROC is now survey-weighted and averaged over 25 splits.

## Limitations and next steps
- Cross-validation only; no held-out test set yet.
- Design-based (PSU/strata) confidence intervals not yet computed.
- "Borderline" diagnosis rule pending team confirmation; change `DIAGNOSED_CODES` and rerun if needed.