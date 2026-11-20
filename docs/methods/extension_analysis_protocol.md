# Analysis extension specification — 2026-11-02

Written before inspecting the extension's model results. This is a prospective specification
for this extension, not retrospective preregistration of the existing project. Notebook 04's
results and cohort have already been inspected. No winning model or cohort will be selected
by the new holdout results.

1. Preserve the 4,612-person 2021–2023 primary cohort. Merge BMI one-to-one; median-impute BMI
   within training folds and compare demographics, demographics+BMI, and demographics+BMI+CBC
   on the same participants and the same five outer/three inner PSU-grouped folds as notebook 04.
   Additional matched BMI-only versus BMI+CBC forests are descriptive comparisons, not tuning.
2. Use WTPH2YR in classifiers, calibrators and evaluation; retain development-only sigmoid
   calibration and 95% sensitivity thresholds. Age/sex/race/education/income remain the baseline.
   Sensitivity comparisons include BMI-observed participants and predictor-block ablations:
   red-cell indices versus white-cell/platelet indices. Drop basophil percentage in the new
   CBC models to remove the exact differential-composition dependency; do not compare changes
   against notebook 04 as if only BMI changed. All 12 CBC measurements still define eligibility.
3. Assess exclusion of low hemoglobin (<12 g/dL recorded female; <13 recorded male) as an
   operational sensitivity flag, not a complete anemia diagnosis. Repeat among ages 20–65,
   consistent with WHO 2024 cutoff age coverage; no altitude/smoking adjustment is available.
   Public pregnancy information remains incomplete. Do not automatically apply an iron marker
   available only in a selected subsample to the whole cohort.
4. On the eligible fasting subsample (WTSAF2YR>0, measured LBXGLU), compare HbA1c>=6.5% and
   fasting glucose>=126 mg/dL using identical participants, folds and fasting weights.
   Report endpoint agreement; never treat these single measurements as confirmed diabetes.
5. Refit the three primary logistic procedures in 100 stratified PSU-resampling replicates.
   Within each stratum with two PSUs, draw one PSU and give it multiplicity two (Rao–Wu
   rescaled bootstrap). Duplicate training records by that integer multiplicity, refit all
   preprocessing, inner calibration, threshold selection and classifiers, then evaluate
   held-out original records using corresponding replicate weights. Keep original fold
   membership so duplicate records cannot leak across training/evaluation. Record failed
   replicates, paired gains and exploratory percentile intervals. This includes fitting
   variability under these fixed splits, not all split/hyperparameter uncertainty. One hundred
   replicates have limited tail precision; this is a practical first full-procedure analysis.
6. Freeze the three logistic specifications, fit/calibrate using only 2021–2023, and evaluate
   once in the independent 2017–2018 NHANES cycle. It is backwards-in-time transportability,
   not prospective validation or independent health-system validation. Use that cycle's
   WTMEC2YR; do not invent a WTPH2YR variable. No temporal-sample recalibration or threshold
   selection. Check units, variables, specimen methods, age top-coding and exclusions against
   both cycles' codebooks. Evaluate conditional design uncertainty in that independent sample.
7. Describe missingness/selection, measured demographic subgroup performance with event counts,
   matched sensitivity/testing burden, and exploratory decision curves at risk thresholds
   0.005–0.10. Decision curves assume the chosen harm exchange rate; they cannot select the
   clinically acceptable threshold or prove cost savings. No new cost values will be invented.
8. Update a narrative literature evidence matrix (not a systematic review), source/search log,
   closest-study comparisons and publication-readiness assessment. Use TRIPOD+AI for reporting
   and PROBAST+AI for risk-of-bias review. Leave author contributions, clinical tolerances and
   publication decisions for team verification. Preserve existing plans; append only status notes.

Sources: [BMI L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BMX_L.htm),
[CBC J](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/CBC_J.htm),
[GHB J](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/GHB_J.htm),
[WHO cutoffs](https://www.ncbi.nlm.nih.gov/books/NBK602183/table/fm-ch1.tab2/),
[CDC domain variance](https://wwwn.cdc.gov/nchs/nhanes/tutorials/varianceestimation.aspx),
[decision analysis](https://www.bmj.com/content/384/bmj-2023-074820).
