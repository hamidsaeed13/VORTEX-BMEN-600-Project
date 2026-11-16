# CBC diagnostic and PCA supplement — 2026-11-16

Specified before running this supplement. Existing extension outcomes have already been
inspected; this is exploratory follow-up, not a new preregistered primary analysis.

- Preserve the primary 4,612-person cohort, eligibility, outcome, weights and PSU-grouped
  five outer/three inner folds from `research_extension.py`. Do not use the older cycle
  again to choose features or models.
- Report ordinary Pearson correlations and ordinary and survey-weighted VIF for the 12
  CBC variables and the 11-variable block with basophil percentage removed. VIF uses an
  intercept; singular auxiliary regressions return infinity. These are descriptive
  diagnostics, not significance tests or automatic variable-selection rules.
- Quantify the five differential percentages' sum. Dropping basophil percentage removes
  the fixed-sum dependency; rounding may make that dependency approximate in released data.
  RBC, hematocrit and MCV have an approximate multiplicative relationship. HGB, HCT, MCH
  and MCHC are related, but MCH/MCHC are not predictors in this project's CBC block.
- Preserve the existing penalized raw-CBC logistic model. Compare it with a secondary
  demographics+BMI+PCA(CBC) logistic model using the same 11 CBC variables. Use standardized
  CBC, full-SVD PCA retaining 95% variance, fitted separately within every inner and outer
  training fold. Demographics/BMI processing stays identical. PCA/scaling are unweighted,
  as is existing preprocessing; fitting, calibration and evaluation use survey weights.
- Use the existing development-only sigmoid calibration and 95% weighted sensitivity
  target. Report AUROC, AP, Brier, log loss and observed deferred/missed counts. No new
  model-selection or clinical policy claim follows from this comparison.
- Whole-cohort scree and PC1/PC2 plots are descriptive only. They never enter evaluation.
  Export loadings and fold-specific component counts. Conditional survey-design intervals
  hold predictions fixed and do not capture model-fitting or split uncertainty.
- Verify matching participants/folds, PSU separation, training-only PCA sample counts,
  finite predictions, accounting, and reproduction of the saved raw-CBC predictions.
