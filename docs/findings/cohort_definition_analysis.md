# Cohort definition and analysis

## Recommendation

Use **adults aged 20+ who explicitly report no prior diabetes diagnosis** as the primary research cohort. The question is whether CBC adds discrimination for a diabetes-range HbA1c result among people without a reported diagnosis. Keep ages 35–70 and 65+ as sensitivity analyses, rather than selecting an older cohort because of its score. No replacement dataset is necessary for this next phase.

Age 20 aligns with availability of adult education information and excludes adolescents; it is an analytic choice, not a clinical threshold. The age-18 sensitivity adds 230 participants but no positive labels. The age-65+ subgroup retains only 46 positive labels and addresses a narrower population. The USPSTF screening recommendation includes ages 35–70 with overweight/obesity and no symptoms; this analysis has not established BMI or symptom eligibility, so its age subgroup is not guideline eligible by definition.

## Explicit eligibility

One participant is one case, identified by SEQN. Require RIDSTATR=2, WTPH2YR>0 after repairing tiny XPORT pseudo-zeros, age ≥20, DIQ010=2, no DIQ050=1 or DIQ070=1, observed HbA1c and all 12 CBC predictors. Outcome: HbA1c ≥6.5%, not a confirmed clinical diagnosis. Diagnosis, medication use, HbA1c, pregnancy and survey weights are excluded from model features.

DIQ010=1 is known diabetes, 3 is borderline, and 7/9/missing are not treated as a negative response. Borderline responses enter only the labelled sensitivity cohort. Forty-one adults who answered no diagnosis reported insulin or diabetes pills; excluding them removes nine positive HbA1c labels. Missing medication responses are not recoded as confirmed nonuse.

Exclude RIDEXPRG=1. Among females aged 20–44, require RIDEXPRG=2, excluding indeterminate/missing records. Pregnancy is not publicly released outside that band. There are 1,612 females outside that reporting band in the primary cohort; this cannot be described as a fully confirmed nonpregnant cohort. The age-18 sensitivity has the same public-data limitation for ages 18–19.

The flow is 11,933 interviewed → 6,750 examined with positive phlebotomy weight → 5,792 age 20+ → 4,756 explicit no diagnosis → 4,715 without reported diabetes medication → 4,657 after pregnancy rules → **4,612 complete CBC/HbA1c**. These sequential counts are not interchangeable with notebook 02's complete-case-first counts.

## Table 1. Cohort sizes and observed outcomes

| Cohort | N | Positive HbA1c | Positive (%) |
| --- | --- | --- | --- |
| reference_all_ages | 6678 | 717 | 10.74 |
| adults20_all_diagnoses | 5677 | 716 | 12.61 |
| primary_adults20_no_diagnosis | 4612 | 106 | 2.30 |
| sensitivity_age18_no_diagnosis | 4842 | 106 | 2.19 |
| sensitivity_age35_70_no_diagnosis | 2879 | 72 | 2.50 |
| sensitivity_age65plus_no_diagnosis | 1375 | 46 | 3.35 |
| sensitivity_include_borderline | 4779 | 127 | 2.66 |

The original reference has 565/717 positives with a reported diagnosis (78.8%). Primary cohort prevalence is 106/4,612 = 2.30%; released-weight descriptive prevalence is 1.99%. The latter has no design-aware interval or extra complete-case nonresponse adjustment. All predictive results below are unweighted.

## Table 2. Primary-cohort model comparison

| Model | Pooled OOF AUROC | Average precision | Fold AUROC mean ± SD |
| --- | --- | --- | --- |
| age_logistic | 0.630 | 0.034 | 0.634 ± 0.045 |
| demographics_logistic | 0.711 | 0.048 | 0.716 ± 0.056 |
| cbc_demographics_logistic | 0.765 | 0.069 | 0.768 ± 0.035 |
| cbc_demographics_forest | 0.733 | 0.074 | 0.734 ± 0.043 |

All four models use identical five-fold stratified assignments within a cohort (seed 42), training-fold imputation/scaling, and one-hot categorical encoding. Logistic regression uses balanced classes, liblinear, and max_iter=2000; the forest uses 300 trees, balanced classes, min_samples_leaf=5 and seed 42. Logistic inputs use sparse storage to avoid dense BLAS warnings in the execution environment. Age, sex, race/ethnicity, education and income form the demographic baseline; the full model adds the 12 CBC variables listed in the script.

CBC adds **0.054 AUROC** over demographics in the matched logistic comparison. This estimates discrimination on these exploratory folds; it does not establish a statistically significant gain or safe test deferral. The no-skill average-precision reference is 0.023. Fold SD describes variation across five overlapping training sets, not a confidence interval. Do not compare these AUROCs directly with notebook 02's single split and ordinal category preprocessing as if only the cohort changed.

At score threshold 0.2, primary CBC logistic sensitivity is 0.943, NPV 0.996, with 1647 tests deferred and **6 of 106 positive labels missed** across pooled out-of-fold predictions. This is a descriptive fixed-grid example, not a threshold selected or validated for use. Balanced-class scores are uncalibrated; an equal numeric threshold does not mean equal clinical risk. An always-negative rule already has 97.70% NPV here.

## Figures and reproducibility

Figure 1 (`results/cohort/cohort_prevalence.png`) shows observed positive prevalence across the seven cohorts. Figure 2 (`results/cohort/primary_cohort_roc.png`) shows the primary cohort's out-of-fold ROC curves. The complete results, individual fold AUROCs, all fixed thresholds and participant-level out-of-fold scores are exported beside the figures.

Install `requirements.txt` and run `python scripts/analysis/cohort_analysis.py` from the root, or execute `notebooks/03_cohort_definition_and_filtering.ipynb`. Both contain the same analysis. This pass was executed with numerical RuntimeWarnings treated as errors, notebook schema validation, unique-ID merge checks, finite-score checks, one prediction per model/participant, and confusion-matrix accounting checks.

## What to do next

Keep this cohort fixed for the next phase. Implement survey-weighted fitting/evaluation and survey-design uncertainty using SDMVSTRA/SDMVPSU, then development-only calibration and threshold selection with separate final evaluation. These folds are already inspected and cannot be relabelled an untouched final test set. Assess anemia-related HbA1c sensitivity and missing-data selection before clinical interpretation. Adding BMI is useful if the team wants a guideline-specific research question; restricting to older adults to improve a score is not justified.

This analysis supports the final-project rubric's explicit sample definition, meaningful baseline comparison, reproducibility, variability and sensitivity analysis requirements. Design-aware uncertainty, the final paper's numbered/captioned integrated figures, and team scope review remain outstanding. The original download date is still unknown.

## Sources

- [NHANES demographics: age, examination status and public pregnancy limitations](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DEMO_L.htm).
- [NHANES diabetes questionnaire: diagnosis/medication coding and skip patterns](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DIQ_L.htm).
- [NHANES HbA1c: phlebotomy weighting and measurement](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/GHB_L.htm).
- [USPSTF screening recommendation](https://www.uspreventiveservicestaskforce.org/uspstf/recommendation/prediabetes-and-type-2-diabetes-screening).
- Local `docs/course/BMEN600 Final Project.pdf`, Dataset and Methods, Results, and GitHub requirements.
