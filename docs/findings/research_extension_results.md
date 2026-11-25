# Research extension: BMI, biological sensitivity and independent evaluation

## What changed scientifically

The original cohort was retained (4,612 adults; 106 positive HbA1c labels). BMI is observed in
4,560 participants; the 52 missing values are training-fold median-imputed, with missingness
indicators. The independent 2017–2018 cohort has 3,943 participants and 132 positive labels.
All primary comparisons within a sample use identical participants and splits.

### Table 1. Weighted, calibrated discrimination and probability error

| Predictors | Current-cycle OOF AUROC | Independent-cycle AUROC | Current Brier | Independent Brier |
| --- | --- | --- | --- | --- |
| demographics | 0.717 | 0.674 | 0.01928 | 0.02003 |
| demographics_bmi | 0.815 | 0.766 | 0.01917 | 0.01994 |
| demographics_bmi_cbc | 0.835 | 0.799 | 0.01897 | 0.02065 |

The incremental CBC AUROC gain after BMI is **0.019**. This is smaller than the earlier
comparison against demographics without BMI. It is not a direct update of notebook 04's
numbers: the new specification also adds numeric missingness indicators and removes basophil
percentage from predictors to remove the differential-composition dependency. Models are
regularized, not interpreted as causal effects; other red-cell collinearity remains.

One hundred stratified PSU resamples refitted preprocessing, all inner and outer models,
calibration and development-selected thresholds. All 100 completed. The exploratory 95%
percentile interval for CBC-minus-BMI AUROC is **-0.034 to 0.062**.
It includes zero. This is stronger than holding fitted scores fixed but not definitive:
the outer/inner splits and hyperparameters are fixed, there are only 15 variance strata,
and 100 resamples give limited tail precision. The code supports increasing --bootstrap
for a higher-precision follow-up; coverage is not validated for this rare-event learning
procedure. Duplicate sampled records retain their original fold assignment to prevent leakage.

### Table 1b. Model family comparison (current cycle only, Phase 15 Step 5)

| Model | AUROC | AP | Brier |
| --- | --- | --- | --- |
| demographics | 0.717 | 0.047 | 0.01928 |
| demographics_bmi | 0.815 | 0.064 | 0.01917 |
| demographics_bmi_cbc | 0.835 | 0.087 | 0.01897 |
| demographics_bmi_red | 0.823 | 0.069 | 0.01907 |
| demographics_bmi_white_platelet | 0.830 | 0.082 | 0.01901 |
| demographics_bmi_forest | 0.766 | 0.044 | 0.01930 |
| demographics_bmi_cbc_forest | 0.781 | 0.059 | 0.01909 |
| demographics_bmi_gbm | 0.784 | 0.061 | 0.01921 |
| demographics_bmi_cbc_gbm | 0.801 | 0.065 | 0.01923 |
| demographics_bmi_adaboost | 0.799 | 0.060 | 0.01904 |
| demographics_bmi_cbc_adaboost | 0.821 | 0.080 | 0.01895 |
| demographics_bmi_svm | 0.568 | 0.024 | 0.01957 |
| demographics_bmi_cbc_svm | 0.692 | 0.054 | 0.01947 |
| demographics_bmi_nb | 0.646 | 0.064 | 0.01941 |
| demographics_bmi_cbc_nb | 0.681 | 0.047 | 0.01937 |
| demographics_bmi_cbc_ensemble | 0.846 | 0.089 | 0.01958 |

Six additional model families (scikit-learn `GradientBoostingClassifier`, `AdaBoostClassifier`,
`SVC` with an RBF kernel, and `GaussianNB`, each fit on both the BMI-only and BMI+CBC feature
sets) were added alongside the existing logistic/forest pair, through the same matched folds,
survey weights and development-only calibration as every other model here. All must support
`sample_weight` in `fit()` to match this project's population-risk (no class-balancing)
convention; `KNeighborsClassifier` does not and was excluded for that reason rather than fit
unweighted and left incomparable.

On this cohort, **properly regularized logistic regression outperforms every other model
family tested.** AdaBoost is the strongest alternative (0.821 AUROC with CBC, versus logistic's
0.835) and clearly beats both gradient boosting (0.801) and random forest (0.781) — a genuinely
informative result, since AdaBoost's reweighting-based boosting is mechanically different from
gradient boosting's residual-fitting approach. RBF-kernel SVM and Naive Bayes perform
substantially worse (0.692 and 0.681 with CBC; SVM alone drops to 0.568 without it) — both used
scikit-learn defaults, with no hyperparameter tuning, matching this file's stated discipline of
not selecting hyperparameters from results; SVM in particular is known to need tuned
regularization/kernel-width for imbalanced tabular data like this ~2.3%-prevalence cohort, so
this reflects untuned defaults, not a ceiling on what RBF SVM could achieve here.

This overall pattern — simpler, regularized linear models matching or beating every more
flexible alternative — is consistent with the signal here being close to linear and already
well-captured by the CBC feature-reduction work (Phase 15): added model flexibility does not
recover additional discrimination on ~4,600 rows with 106 events. None of these additional
model families are frozen/transported to the independent 2017–2018 cycle (Table 1 above is
logistic-only, `demographics`/`demographics_bmi`/`demographics_bmi_cbc`, for that reason) or
included in the 100-replicate bootstrap.

### Table 1c. SVM hyperparameter sensitivity (exploratory; not part of the headline comparison)

| Configuration | AUROC | AP | Brier |
| --- | --- | --- | --- |
| demographics_bmi_cbc_svm | 0.692 | 0.054 | 0.01947 |
| demographics_bmi_cbc_svm_balanced | 0.769 | 0.064 | 0.01910 |
| demographics_bmi_cbc_svm_c10 | 0.702 | 0.064 | 0.01918 |
| demographics_bmi_cbc_svm_c100_g1 | 0.445 | 0.017 | 0.01951 |

Default RBF SVM (`C=1`, `gamma='scale'`, no class weighting) underperformed every other model
family in Table 1b. A prior, unrelated project's notebook (not part of this pipeline) found
`class_weight='balanced'` plus grid-searched `C=100, gamma=1` dramatically improved its own SVM.
To check whether the same levers help here, without grid-searching this project's own data (which
would violate this file's stated no-hyperparameter-selection-from-results discipline), a small,
pre-specified set of configurations was run through the identical matched folds/weights/
calibration and reported in full rather than searched-and-selected:

- **Class balancing alone helps substantially** (0.692 → 0.769 AUROC) — the untuned default's
  poor performance was partly a class-imbalance artifact fixable without touching the kernel.
- **Mildly increasing `C` without changing `gamma`** (`C=10`, `gamma='scale'`, class-balanced)
  barely moves the needle (0.702) — far short of `class_weight='balanced'` alone.
- **Directly porting the other project's winning configuration** (`C=100`, `gamma=1`,
  class-balanced) is actively harmful here (AUROC 0.445, worse than chance) — that
  hyperparameter pair was tuned for a different dataset's scale and dimensionality, and a
  `gamma=1` RBF kernel badly overfits this feature space. This is exactly the failure mode the
  no-grid-search discipline guards against: a hyperparameter pair that looks like a clear win
  elsewhere can be actively destructive on different data, so it is reported as a cautionary
  data point here, not adopted. None of these four configurations replace
  `demographics_bmi_cbc_svm`'s default hyperparameters in Table 1b or anywhere else in this
  pipeline; this table is exploratory evidence, not a selected best model.

### Table 1d. Class-balancing sensitivity, all model families (exploratory; not part of the headline comparison)

| Model | Unbalanced AUROC | Class-balanced AUROC | Delta |
| --- | --- | --- | --- |
| Logistic | 0.835 | 0.835 | +0.000 |
| Forest | 0.781 | 0.801 | +0.019 |
| Gradient boosting | 0.801 | 0.806 | +0.005 |
| AdaBoost | 0.821 | 0.820 | -0.001 |
| SVM | 0.692 | 0.766 | +0.074 |
| Naive Bayes | 0.681 | 0.684 | +0.003 |

Every model family in Table 1b was refit with a class-balance sample weight (sklearn's
`'balanced'` formula, `n_samples / (n_classes * class_count)`) multiplied into the existing
survey weight — the same single mechanism applied identically across all six, so it works even
for model types with no native `class_weight` parameter (gradient boosting, AdaBoost, Naive
Bayes). This directly answers "does class balancing help" for the whole comparison, not just
SVM. The effect is highly model-dependent: **SVM improves dramatically** (+0.074 AUROC,
consistent with the native-`class_weight='balanced'` result in Table 1c above — two different
implementations of the same idea agree) and **random forest improves meaningfully** (+0.019);
gradient boosting improves modestly (+0.005); logistic regression, AdaBoost and Naive Bayes are
essentially unchanged (within ±0.003, i.e. noise). A plausible explanation: margin- and
distance-based methods (SVM) and models that partition the training sample empirically (forest)
are more sensitive to a skewed training prevalence than models already built around resampling-
based reweighting (AdaBoost's native update rule) or explicit likelihood/prior estimation
(logistic's MLE, Naive Bayes' own class-prior modeling) — but this is a plausible interpretation
of these six numbers, not a mechanism verified here. As with Table 1c, none of these
balanced variants replace any model's default fitting in Table 1b or elsewhere in this pipeline.

### Logistic vs. AdaBoost vs. their ensemble: is the ranking in Table 1b real?

A soft-voting ensemble of logistic regression and AdaBoost (`demographics_bmi_cbc_ensemble`,
same matched folds/weights/calibration) was added to Table 1b and to the 100-replicate PSU
bootstrap alongside the three `PRIMARY` models. Point estimates suggest a ranking — ensemble
(0.846) > logistic (0.835) > AdaBoost (0.821) — but paired bootstrap intervals for the gaps
tell a more cautious story:

| Comparison | 95% interval |
| --- | --- |
| Logistic − AdaBoost | −0.042 to 0.101 (includes zero) |
| Ensemble − Logistic | −0.058 to 0.046 (includes zero) |
| Ensemble − AdaBoost | **0.003 to 0.065** (excludes zero, barely) |

**Only the ensemble-vs-AdaBoost gap is distinguishable from resampling noise, and only just** (the
lower bound is 0.003). Logistic and AdaBoost are not reliably separable from each other, nor is
the ensemble reliably separable from logistic alone. This is reinforced by the Phase 15 Step 6
final locked holdout (`docs/findings/final_holdout_evaluation.md`): on a single genuinely
untouched split (1,205 participants, 29 positive events, never used in any fold decision
before), **AdaBoost actually outperformed logistic** (0.829 vs. 0.766 AUROC, 100% vs. 90.2%
weighted sensitivity) — the reverse of the nested-CV point estimate. Taken together, the honest
conclusion is that logistic, AdaBoost and their ensemble perform comparably on this cohort size,
and this project does not have enough events (106 in the primary cohort) to confidently declare
a single best model among them.

### Table 2. Sensitivity and endpoint comparisons

| Analysis | N | Positives | BMI baseline AUROC | BMI+CBC AUROC | CBC gain |
| --- | --- | --- | --- | --- | --- |
| primary | 4612 | 106 | 0.815 | 0.835 | +0.019 |
| bmi_observed | 4560 | 105 | 0.817 | 0.838 | +0.021 |
| exclude_low_hgb_all_ages | 4191 | 95 | 0.795 | 0.810 | +0.015 |
| age20_65_all | 3343 | 63 | 0.802 | 0.815 | +0.013 |
| age20_65_exclude_low_hgb | 3061 | 55 | 0.816 | 0.802 | -0.014 |
| fasting_hba1c | 2375 | 60 | 0.819 | 0.823 | +0.004 |
| fasting_glucose | 2375 | 90 | 0.774 | 0.794 | +0.020 |
| transport_2017_2018 | 3943 | 132 | 0.766 | 0.799 | +0.034 |

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
| demographics | 0.990 | 20.1 | 716 | 1 |
| demographics_bmi | 0.967 | 39.9 | 1539 | 4 |
| demographics_bmi_cbc | 0.976 | 40.4 | 1601 | 2 |

The primary CBC model achieves 97.6% weighted
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

Install requirements.txt. Acquire missing public inputs with
python scripts/data/acquire_extension_data.py. Run python scripts/analysis/research_extension.py --bootstrap 100,
then python scripts/reporting/report_research_extension.py and python scripts/verification/verify_research_extension.py.
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

The literature synthesis and 21-source evidence matrix are in literature/extension_*.
The publication-readiness assessment distinguishes work completed here from clinical,
institutional and independent-review decisions that remain. Negative findings should be part
of the paper's contribution, not removed to obtain a stronger headline.
