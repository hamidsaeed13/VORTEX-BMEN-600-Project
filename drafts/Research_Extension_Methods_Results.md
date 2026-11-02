# Draft Methods and Results insertion — requires team review

## Focused research question

Among adults without reported diabetes, does CBC improve identification of diabetes-range
HbA1c beyond demographics and BMI, and is its incremental value robust to blood-cell-related
measurement effects and independent-cycle evaluation?

## Methods

We linked NHANES August 2021–August 2023 demographics, CBC, HbA1c, diabetes questionnaire,
body measures and fasting-glucose components by unique participant identifier. The primary
cohort comprised 4,612 examined adults aged ≥20 years with positive phlebotomy weights,
explicitly reporting no prior diabetes diagnosis, no reported current diabetes medication,
observed HbA1c and complete selected CBC measures. Recorded pregnancy and indeterminate
pregnancy status in females aged 20–44 were excluded; public data could not establish
pregnancy status outside that reporting range. HbA1c ≥6.5% defined a laboratory outcome,
not confirmed diabetes. Original download dates for pre-existing inputs remain unverified;
new-file acquisition is documented in the manifest.

Three prespecified logistic models compared demographics, demographics plus BMI, and
demographics plus BMI plus CBC. Preprocessing, survey-weighted classifiers, calibration
and sensitivity-targeted thresholds were refitted within nested grouped validation. Five
outer folds and three inner folds kept masked survey PSUs together. We used 100 stratified
PSU resamples with refitting of the full pipeline for exploratory uncertainty, conditional
on fixed split assignments. Predictor-block, low-hemoglobin, age-restricted and fasting-endpoint
analyses examined robustness. Frozen current-cycle models were evaluated without updating
in a distinct 2017–2018 cohort using its examination weights. Methods and exceptions are
specified in reports/extension_analysis_protocol.md and reports/cycle_harmonization.md.

## Results

| Predictors | Current-cycle OOF AUROC | Independent-cycle AUROC | Current Brier | Independent Brier |
| --- | --- | --- | --- | --- |
| demographics | 0.693 | 0.664 | 0.01932 | 0.02004 |
| demographics_bmi | 0.799 | 0.762 | 0.01926 | 0.01987 |
| demographics_bmi_cbc | 0.823 | 0.799 | 0.01902 | 0.02059 |

The BMI-adjusted CBC AUROC gain was 0.023, with full-refit resampling percentile bounds
-0.030 to 0.069. The gain diminished with low-hemoglobin exclusion
and reversed in the restricted age-20–65, low-hemoglobin-excluded sensitivity cohort. In the
independent 2017–2018 sample (3,943 participants, 132 positive outcomes), CBC improved AUROC
but worsened Brier error and log loss. These mixed results limit an interpretation of uniform
clinical benefit. The main development-selected CBC policy missed three observed positives;
it did not establish safe deferral or economic savings.

## Discussion direction

Discuss the smaller gain beyond BMI, endpoint discordance and red-cell influences in relation
to the closest studies, not headline AUROCs from unlike endpoints. Frame the study as
incremental-value and robustness evaluation. Report independent calibration limitations and
resampling uncertainty. These draft paragraphs need integration with citations, figures,
the final manuscript's reference numbering, verified contributions and AI-use disclosure.
