# Phase 13 Step 2 Lasso protocol

Use the primary NHANES cohort and the 14-feature Step 1 candidate. Keep the
research extension's five outer PSU folds and three inner PSU folds per outer
development set, demographic encoders, age, BMI, weight normalization and
development-only logistic calibration. Use L1 logistic regression with the
same column preprocessing as the extension. All model coefficients are
penalized, including demographic and BMI terms. Report selection for CBC
terms only. A CBC coefficient with absolute magnitude above 1e-8 counts as
retained.

## Penalty rule specified before outer evaluation

Use C values 0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 1.28,
2.56 and 5.12. For each C, score raw inner-validation predictions by weighted
AUROC within each fold and average the three AUROCs equally. Choose the
smallest C (strongest penalty) whose mean is within 0.005 AUROC of the best
mean on that outer development set. This tolerance guides selection relative
to the candidate path. It is not a noninferiority margin against the full model.

Fit preprocessing and L1 coefficients separately inside every inner training
fold. After choosing C, use its inner out-of-fold predictions to fit the weighted
calibrator and development threshold, then refit the pipeline on the whole outer
development set. Score the outer test fold once. Use the same outer weights and
report pooled calibrated AUROC and paired per-fold differences against the
full 21-feature logistic baseline.

Report nonzero terms by outer fit and by inner fit at the selected C. This
evaluates a selection procedure and leaves the final panel for team approval.
VIF and prior group permutation results are interpretation aids after evaluation.
