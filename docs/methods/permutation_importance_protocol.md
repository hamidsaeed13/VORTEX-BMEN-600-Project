# Held-out grouped permutation importance — 2026-11-16

Exploratory follow-up specified before running this supplement, after inspecting the
existing model results. The final-project rubric calls for proportionate interpretation,
meaningful comparisons, reproducible analysis and appropriate variability reporting.

1. Preserve the primary 4,612 participants, HbA1c ≥6.5% outcome, existing predictors,
   WTPH2YR, five outer/three inner PSU-grouped folds, and logistic/forest specifications
   from `research_extension.py`. Reproduce both saved calibrated out-of-fold predictions.
   Do not reuse the older cycle for exploratory interpretation or choose a new model.
2. Fit each procedure using development records only, including imputation, encoding,
   scaling and calibration. Freeze the fitted model/calibrator before perturbation.
3. Perturb only the held-out predictors, independently within each held-out PSU. Keep
   labels, IDs, weights and design membership fixed. For a block, use the same donor row
   for all columns so its joint values and missingness patterns remain intact. Use the
   same donor assignments for both models and all blocks within a repeat. Export donors
   and seeds. This conditions on PSU membership; between-PSU dependence is not assessed.
4. Use 20 reproducible permutations per fold. Prespecify age, sex, race/ethnicity,
   education, income, BMI, red-cell, white-cell/platelet and all-CBC blocks. All-CBC is
   a separate overlapping experiment, not the sum of its two sub-blocks. Do not normalize
   or interpret the scores as additive shares of contribution.
5. Pool each repeat's five out-of-fold prediction vectors and report survey-weighted
   AUROC/AP losses and Brier/log-loss increases relative to the unperturbed predictions.
   Positive values indicate worse performance after perturbation. Preserve negative
   values. Report mean and SD across permutations as Monte Carlo perturbation variation,
   not confidence intervals, survey sampling uncertainty or model-refitting variability.
6. Correlated blocks can substitute for one another, and shuffling can create unusual
   cross-block combinations. Scores measure reliance of these fitted procedures under
   this perturbation, not causal effects, independent biomarker value or the value of
   removing a test and retraining. No clinical-policy or feature-selection claim follows.
7. Check saved prediction reproduction, outer/inner PSU separation, donor bijections
   within each held-out PSU, complete repeat coverage, fixed targets/weights and finite
   probabilities. Independently recompute metric differences from exported scores.
