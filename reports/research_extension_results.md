# Research extension: BMI, biological sensitivity and independent evaluation

## What changed scientifically

The original cohort was retained (4,612 adults; 106 positive HbA1c labels). BMI is observed in
4,560 participants; the 52 missing values are training-fold median-imputed, with missingness
indicators. The independent 2017–2018 cohort has 3,943 participants and 132 positive labels.
All primary comparisons within a sample use identical participants and splits.

### Table 1. Weighted, calibrated discrimination and probability error

| Predictors | Current-cycle OOF AUROC | Independent-cycle AUROC | Current Brier | Independent Brier |
| --- | --- | --- | --- | --- |
| demographics | 0.693 | 0.664 | 0.01932 | 0.02004 |
| demographics_bmi | 0.799 | 0.762 | 0.01926 | 0.01987 |
| demographics_bmi_cbc | 0.823 | 0.799 | 0.01902 | 0.02059 |

The incremental CBC AUROC gain after BMI is **0.023**. This is smaller than the earlier
comparison against demographics without BMI. It is not a direct update of notebook 04's
numbers: the new specification also adds numeric missingness indicators and removes basophil
percentage from predictors to remove the differential-composition dependency. Models are
regularized, not interpreted as causal effects; other red-cell collinearity remains.

One hundred stratified PSU resamples refitted preprocessing, all inner and outer models,
calibration and development-selected thresholds. All 100 completed. The exploratory 95%
percentile interval for CBC-minus-BMI AUROC is **-0.030 to 0.069**.
It includes zero. This is stronger than holding fitted scores fixed but not definitive:
the outer/inner splits and hyperparameters are fixed, there are only 15 variance strata,
and 100 resamples give limited tail precision. The code supports increasing --bootstrap
for a higher-precision follow-up; coverage is not validated for this rare-event learning
procedure. Duplicate sampled records retain their original fold assignment to prevent leakage.

### Table 2. Sensitivity and endpoint comparisons

| Analysis | N | Positives | BMI baseline AUROC | BMI+CBC AUROC | CBC gain |
| --- | --- | --- | --- | --- | --- |
| primary | 4612 | 106 | 0.799 | 0.823 | +0.023 |
| bmi_observed | 4560 | 105 | 0.803 | 0.832 | +0.029 |
| exclude_low_hgb_all_ages | 4191 | 95 | 0.795 | 0.808 | +0.012 |
| age20_65_all | 3343 | 63 | 0.792 | 0.798 | +0.007 |
| age20_65_exclude_low_hgb | 3061 | 55 | 0.790 | 0.781 | -0.009 |
| fasting_hba1c | 2375 | 60 | 0.795 | 0.805 | +0.010 |
| fasting_glucose | 2375 | 90 | 0.766 | 0.778 | +0.012 |
| transport_2017_2018 | 3943 | 132 | 0.762 | 0.799 | +0.037 |

The CBC gain is smaller after excluding low hemoglobin and reverses among the age-20–65
low-hemoglobin-excluded participants. Those comparisons have fewer events and different
case mix/folds; they cannot prove anemia causes the original signal. Red-cell-only and
white-cell/platelet-only models, included in the full CSV, separate predictor blocks rather
than establish mechanisms. The low-Hgb flag (<12 g/dL female, <13 male) is operational:
it omits altitude/smoking corrections, iron deficiency without anemia and hemoglobin variants.
The 20–65 restriction respects the age coverage of the WHO cutoff table; the all-age flag
is an explicit extrapolation sensitivity, not a validated geriatric anemia definition.

Fasting analyses use the same 2,375 positive-WTSAF2YR participants for both endpoints.
There are 60 HbA1c positives and 90 FPG positives: 41 meet both, 19 HbA1c only, and 49 FPG
only. Thus 68 people have discordant single-test labels. The glucose and HbA1c comparisons
use the same folds and fasting weights; neither endpoint is a confirmed clinical diagnosis.
Their modest CBC gains do not establish that all HbA1c signal is glucose-specific.

## Independent-cycle evaluation

All three model pipelines, calibrators and thresholds were fitted in 2021–2023, saved and
hashed before evaluating the 2017–2018 outcomes. No independent-sample recalibration, feature
selection or threshold search was performed. AUROC improves from 0.762 to 0.799 after CBC,
but **Brier error worsens** from 0.01987 to 0.02059, and log loss also worsens. Mean CBC-model
risk is 2.29% against 2.06% weighted observed prevalence. Better ranking therefore does not
mean uniformly better probability estimates or clinical utility.

This is independent earlier-cycle transport, not prospective or hospital-system validation.
The older cycle uses WTMEC2YR while the current cycle uses WTPH2YR; both have appropriate
cycle-specific design variables. CBC units/coding were aligned. CDC documents a current-cycle
HbA1c instrument transition and reports no adjustment needed after bridging, but assay and
population shifts remain limitations. See cycle_harmonization.md. Independent-sample
conditional jackknife intervals and paired gains are exported separately; these condition
on models developed in the current cycle.

## Exploratory policy value

### Table 3. Outer-fold policies targeting 95% sensitivity during development

| Model | Weighted sensitivity | Weighted deferred % | Observed deferred N | Observed missed positives |
| --- | --- | --- | --- | --- |
| demographics | 0.933 | 21.7 | 729 | 4 |
| demographics_bmi | 0.937 | 38.1 | 1416 | 4 |
| demographics_bmi_cbc | 0.945 | 38.1 | 1474 | 3 |

The primary CBC model achieves 94.5% weighted
sensitivity, below the development target. Weighted deferral is almost identical between
BMI and BMI+CBC models (about 38.1%); raw observed deferred counts differ because weights
vary. This is an important limitation of interpreting the AUROC increase as a large reduction
in testing. The saved matched-burden table fixes weighted testing fractions descriptively;
those held-out descriptive thresholds are not selected deployable cutoffs.

Decision curves compare models with test-all/test-none over assumed risk thresholds
0.005–0.10. The assumed harm ratio is threshold/(1-threshold); no measured cost data or
clinician-approved harm ratio is available. Curves show hypothetical preferences, not
actual savings, safety, or a clinically endorsed cutoff. No model should be used to withhold
testing on this evidence alone.

## Selection, missingness and subgroup checks

Forty-five otherwise eligible participants lack complete labs: only 24 have observed HbA1c,
and the other 21 must not be labelled negative. selection_audit.csv contrasts their available
characteristics with included records; a descriptive audit cannot remove selection bias.
Income-to-poverty ratio is missing in about 12.8% of the included cohort; adult education has
two missing records, BMI 52. Median/mode imputation and numeric missingness indicators are
fitted only in training samples. The BMI-observed sensitivity retains 4,560/105 participants/
positive labels and shows the finding does not solely depend on BMI imputation.

Subgroup metrics by recorded sex, age and race/ethnicity are descriptive, with positive
counts; groups with fewer than 10 events have performance suppressed. This is not a formal
fairness assessment, and small-group uncertainty cannot support claims of equal performance.
Race/ethnicity categories reflect recorded survey categories, not causal biology.

## Reproducibility and figures

Install code/requirements-cohort.txt. Acquire missing public inputs with
python code/acquire_extension_data.py. Run python code/research_extension.py --bootstrap 100,
then python code/report_research_extension.py and python code/verify_research_extension.py.
The acquisition manifest records URLs, retrieval times and hashes; frozen-model hashes and
coefficients accompany the predictions. Requirements include joblib for model artifacts.
Models are trusted project artifacts; do not load untrusted joblib files.

Notebook 05 summarizes BMI and sensitivity results; notebook 06 summarizes resampling and
independent-cycle evaluation. By default they read verified saved outputs; setting RUN_ANALYSIS
in notebook 05 reruns the full extension. Figure 1 is the matched BMI/transport comparison;
Figure 2 displays all sensitivity gains including the negative result; Figure 3 shows independent
calibration. decision_curves.png is an exploratory supplementary figure.

## Interpretation for a paper

CBC contains additional ranking information beyond demographics and BMI in these samples,
but its gain is modest, uncertain under full-procedure resampling, and not consistent across
all biological sensitivity analyses. Independent-cycle probability error worsens despite
better discrimination. This supports a cautious incremental-value/robustness paper, not a
claim that CBC safely replaces HbA1c screening.

The literature synthesis and 21-source evidence matrix are in literature_review/extension_*.
The publication-readiness assessment distinguishes work completed here from clinical,
institutional and independent-review decisions that remain. Negative findings should be part
of the paper's contribution, not removed to obtain a stronger headline.
