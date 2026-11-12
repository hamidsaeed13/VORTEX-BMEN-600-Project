# Phase 9: Feature expansion (exploratory)

**Notebook:** `code/04_feature_expansion.ipynb`

## Method
- Cohort: same 5,144 adults as Phase 8 (≥18, no prior diabetes diagnosis, not pregnant, valid WTPH2YR and HbA1c).
- Outcome: HbA1c ≥5.7%.
- Model: logistic regression with median imputation and scaling inside a pipeline; 5-fold stratified cross-validation (random_state=42); metric AUROC (mean and SD across folds).
- Added `BMX_L` (body measures) to `data/raw/examination/`.
- Serum glucose and insulin/HOMA-IR were **not** used as predictors because they directly measure the outcome.
- hs-CRP and ferritin log-transformed (log1p) due to skew.

## Results (unweighted, exploratory)

| Population | Model | AUROC (mean) | AUROC (SD) |
|---|---|---|---|
| Whole cohort | A: age + sex | 0.697 | 0.012 |
| Whole cohort | B: + CBC | 0.770 | 0.018 |
| Whole cohort | C: B + BMI + waist | 0.780 | 0.014 |
| Whole cohort | D: B + hs-CRP | 0.781 | 0.018 |
| Whole cohort | B without red-cell features | 0.730 | 0.014 |
| Non-anemic (n=4,671) | A: age + sex | 0.703 | 0.019 |
| Non-anemic (n=4,671) | B: + CBC | 0.779 | 0.017 |
| Iron subgroup, women 18–49 (n=1,240; 181 cases) | B: age + sex + CBC | 0.766 | 0.021 |
| Iron subgroup, women 18–49 (n=1,240; 181 cases) | E: B + ferritin + TfR | 0.770 | 0.012 |

## Interpretation
- **CBC adds clear value beyond age and sex** (+0.073 AUROC), well above fold-to-fold variation.
- **Not explained by anemia:** after excluding 473 anemic participants (WHO Hb <13 g/dL men, <12 g/dL women), the CBC gain was +0.076.
- **Red-cell and white-cell/platelet measures each contribute.** Removing red-cell measures lowered AUROC to 0.730, still above age + sex. Part of the red-cell contribution may reflect erythrocyte effects on HbA1c rather than glycemia, which should be acknowledged.
- **BMI/waist (+0.010), hs-CRP (+0.011) and iron markers (+0.004) add little beyond CBC**; these differences are within fold-to-fold variation.
- Ferritin and TfR were measured only in women aged 18–49 (NHANES design), so iron findings apply only to that group.

## Limitations
- Unweighted cross-validated estimates describe the NHANES sample, not the U.S. population (see Phase 8).
- No confidence intervals or held-out test set yet; differences of ~0.01 should not be over-interpreted.
- Missing BMI (66 participants) and hs-CRP filled by median imputation within each fold.
- The "without red-cell features" model removed RBC, Hb, Hct, MCV, MCH, MCHC and RDW; it kept 14 white-cell and platelet features, including nucleated RBC (LBXNRBC), which is usually near zero in adults.

## Not tested
Blood pressure, smoking, alcohol, physical activity, family history, medications, diet, liver/kidney markers, lipids.