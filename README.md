# Lab Test Recommendation System — Predicting Diabetes-Range HbA1c from CBC Panels

## Project navigation

Expand a stage to find its notebook, executable analysis, interpretation and saved outputs.
The numbered filenames retain the research sequence. See the [file map](docs/file-map.csv)
for previous locations and the [script guide](scripts/README.md) for commands.

<details>
<summary>01 — Explore the source dataset</summary>

- [Notebook](notebooks/01_eda_cbc_glucose_demographics.ipynb)
- [Final-cohort figure script](scripts/figures/plot_final_cohort.py)
- [Final-cohort figure](results/cohort/final_cohort_description.png)

</details>

<details>
<summary>02 — Original baseline and age-only comparison</summary>

- [Notebook](notebooks/02_baseline_model_and_figures.ipynb)
- [AUROC table](results/baseline/baseline_auroc_comparison.csv)
- [Threshold table](results/baseline/baseline_threshold_comparison.csv)

</details>

<details>
<summary>03 — Define and compare cohorts</summary>

- [Notebook](notebooks/03_cohort_definition_and_filtering.ipynb)
- [Analysis script](scripts/analysis/cohort_analysis.py)
- [Interpretation](docs/findings/cohort_definition_analysis.md)
- [Outputs](results/cohort/)

</details>

<details>
<summary>04 — Survey weighting and calibration</summary>

- [Notebook](notebooks/04_survey_weighted_calibration.ipynb)
- [Analysis script](scripts/analysis/weighted_calibration_analysis.py)
- [Interpretation](docs/findings/weighted_calibration_analysis.md)
- [Outputs](results/weighted_calibration/)

</details>

<details>
<summary>05–06 — BMI, robustness and independent validation</summary>

- [BMI/sensitivity notebook](notebooks/05_bmi_and_biological_sensitivity.ipynb)
- [Independent-validation notebook](notebooks/06_resampling_and_independent_validation.ipynb)
- [Analysis script](scripts/analysis/research_extension.py)
- [Results and interpretation](docs/findings/research_extension_results.md)
- [Outputs and frozen models](results/research_extension/)

</details>

<details>
<summary>Literature, writing and project management</summary>

- [Literature evidence and source notes](literature/README.md)
- [Draft writing](writing/drafts/)
- [Presentations](writing/presentations/)
- [Project plan](docs/planning/PROJECT_PLAN.md)
- [Manual TODO](docs/planning/MANUAL_TODO.md)
- [Methods, findings, verification and course documents](docs/README.md)
- [Publication readiness](docs/findings/publication_readiness.md)

</details>

## Team

- Afshar, Setayesh
- Kraft, Jacob
- Osifo, Emmanuella
- Saeed, Hamid
- Yeboah, Ahenkan

## Problem Statement

Clinical labs frequently order bundled test panels reflexively (e.g., CBC + Blood
Group + HbsAg + Anti-HCV + Blood Sugar, all at once) regardless of whether each
individual test is likely to be informative for a given patient. This drives up
patient cost, phlebotomy burden, and lab turnaround time without a proportional
diagnostic benefit.

This project investigates whether a CBC — already drawn so often that it is the
single most commonly ordered lab test in a five-country hospital comparison —
combined with basic demographics, can predict a diabetes-range HbA1c result, so
that downstream ordering decisions (e.g., whether a confirmatory glucose test is
warranted) can be risk-stratified rather than applied uniformly.

## Research Question

> Using only CBC parameters and demographics, how well can we identify a
> diabetes-range HbA1c result — and does that signal come from genuinely new
> information, or mostly from flagging people who already know they have
> diabetes?

Fasting plasma glucose is tracked as a secondary check on this association (see
Known Uncertainties), not as an interchangeable primary outcome.

## Why This Matters

- **Cost asymmetry:** an unnecessary glucose test is cheap relative to the harm
  of a missed diabetes diagnosis. Any recommendation policy must be built
  around that asymmetry, evaluated by sensitivity/NPV at a chosen threshold,
  not overall accuracy alone. (We are not claiming CBC itself is cheaper than
  glucose to run — a five-country cost comparison actually shows CBC priced
  *higher* than glucose at every site studied — only that CBC is already
  drawn for unrelated reasons far more often, so using it adds no new blood
  draw.)
- **Opportunistic screening:** CBC is already collected for many patients for
  unrelated reasons, so there is no additional collection cost to using it as
  a predictor.

## Dataset

**NHANES (National Health and Nutrition Examination Survey), CDC/NCHS, 2021–2023 cycle**

- Publicly available at [wwwn.cdc.gov/nchs/nhanes](https://wwwn.cdc.gov/nchs/nhanes/)
- A multistage, stratified, cross-sectional survey of the noninstitutionalized
  US civilian population
- CBC laboratory component (`CBC_*`): WBC, RBC, hemoglobin, hematocrit, MCV,
  MCH, MCHC, platelet count, and 5-part WBC differential (neutrophils,
  lymphocytes, monocytes, eosinophils, basophils)
- Glycemic outcome components (`GLU_*`, `GHB_*`, `DIQ_*`): fasting plasma
  glucose, HbA1c, and self-reported diabetes diagnosis
- Demographics component (`DEMO_*`): age, sex, and other covariates
- Records are linked across components via the shared participant identifier
  `SEQN`

## Known Uncertainties / Open Risks

1. **Target definition:** our primary outcome is diabetes-range HbA1c
   (≥6.5%). Fasting glucose (≥126 mg/dL) is tracked as a secondary check —
   note that NHANES also has a biochemistry-panel serum glucose value
   (`BIOPRO_L`, variable `LBXSGL`, ~6,357 measurements, non-fasting), which we
   have not yet incorporated; it is not interchangeable with the fasting or
   diagnostic definitions without reviewing specimen/fasting-status
   differences first. Self-reported diagnosis is used to define eligibility
   and stratify results, not as a third interchangeable outcome — in our
   current exploratory cohort, 78.8% of participants with a diabetes-range
   HbA1c already report a prior diagnosis, so the present model mostly
   distinguishes known from unknown cases rather than screening for new ones.
   We will restrict to an explicit intended population (e.g., adults only, no
   prior diagnosis) for the next phase.
2. **Decision threshold, not just accuracy:** because of the cost asymmetry
   between an unnecessary test and a missed diagnosis, the model must be
   evaluated on sensitivity/NPV at clinically defensible thresholds, not
   overall accuracy or AUROC alone — and a high NPV must always be reported
   together with how many true positives are missed at that same threshold,
   since NPV alone is not evidence that deferring a test is safe.
3. **Survey design not yet applied:** our current preliminary numbers do not
   yet apply NHANES survey weights (`WTPH2YR` for CBC/HbA1c, `WTSAF2YR` with
   proper eligibility for fasting glucose) or design variables (`SDMVSTRA`,
   `SDMVPSU`), so they describe our analytic sample, not the US population.
4. **No cost or ordering-policy data in NHANES:** NHANES gives every
   participant the full standardized battery, so it can validate the
   *predictive* signal (does CBC correlate with HbA1c status) but not the
   economic impact of a skip/order policy. Cost assumptions and the
   harm-of-a-missed-diagnosis will need to be defined separately by the team.

## Planned Approach

1. Acquire and merge relevant NHANES cycles (CBC + glucose/HbA1c/DIQ +
   demographics) via `SEQN`. *(Done — see `notebooks/01_eda_cbc_glucose_demographics.ipynb`.)*
2. Define the target label(s) and document the clinical justification for the
   chosen glycemic cutoffs, including the intended age/prior-diagnosis
   eligibility. *(In progress — current exploratory work uses HbA1c ≥6.5% on
   all ages/diagnosis statuses; see Known Uncertainties above.)*
3. Exploratory data analysis and handling of class imbalance. *(Done — see
   notebook 01; class weighting used in the baseline models below.)*
4. Train and compare classification models (logistic regression, random
   forest, gradient boosting) for predicting diabetes-range HbA1c from CBC +
   demographics. *(First pass done — see `notebooks/02_baseline_model_and_figures.ipynb`;
   gradient boosting and proper categorical encoding still to add.)*
5. Evaluate at multiple decision thresholds, reporting sensitivity/specificity/
   NPV trade-offs — together with tests flagged and positives missed — rather
   than a single accuracy figure. *(First pass done; cross-validation,
   confidence intervals, and calibration checks still to add.)*
6. Translate model output into a test-recommendation policy (order / consider /
   skip) with an explicit cost-benefit framing. *(Not started.)*

## Repository Structure

```
.
├── README.md
├── requirements.txt
├── notebooks/           # numbered research storyline, 01–06
├── scripts/             # data, analysis, figures, reporting, verification
├── data/                # raw inputs by cycle; download manifests
├── results/             # baseline, cohort, weighted calibration, research extension
├── literature/          # papers, evidence matrix and search log
├── writing/             # drafts, presentations and final submission materials
└── docs/                # planning, methods, findings, verification and course materials
```

## Setup and Running the Notebooks

- Requires Python 3.9+ with `pandas`, `numpy`, `matplotlib`, and `scikit-learn`.
- Install dependencies with `python -m pip install -r requirements.txt`.
- Open notebooks from the repository root or `notebooks/`; data paths resolve from
  the project root identified by `CODEX.md`. Script locations and output folders
  are listed in the collapsible navigation below.
- `notebooks/01_eda_cbc_glucose_demographics.ipynb` loads and merges the raw NHANES
  files and produces the descriptive statistics and figures used in Section 5.
- `notebooks/02_baseline_model_and_figures.ipynb` depends on nothing from notebook
  01 being run first (it reloads the raw files itself) and produces the
  baseline models, ROC curves, and threshold comparisons. It now includes an age-only
  logistic baseline on the same cohort/split and exports comparison CSVs plus the ROC figure
  to `results/baseline/`.

## Status

First exploratory baseline model complete (AUROC 0.743 demographics-only →
0.811 CBC+demographics, random forest); target-label finalization, survey
weighting, categorical encoding, and cross-validation are the next steps
before the final report. See `docs/planning/MANUAL_TODO.md` and
`docs/verification/Midterm_Research_Plan_Verification_Report.md` for the current list of
open items.

### Age-only baseline comparison

Notebook 02 now compares age-only logistic regression (held-out AUROC **0.689**),
demographics-only logistic regression (**0.743**), CBC + demographics logistic regression
(**0.783**), and CBC + demographics random forest (**0.811**). The matched logistic comparison
suggests CBC adds discrimination beyond demographics on this split (AUROC gain **0.040**).
These remain unweighted exploratory results; the threshold table reports deferred tests and
positive cases missed alongside sensitivity/NPV, and no safe deferral threshold is established.

### Cohort definition and filtering (notebook 03)

The recommended primary research population is **adults aged 20+ who explicitly report no
prior diabetes diagnosis**, with no reported current insulin/diabetes pills, an observed HbA1c,
and a complete CBC. Require an examination and positive phlebotomy weight. Exclude recorded
pregnancy and indeterminate pregnancy status among females aged 20–44. Pregnancy information
outside that public reporting band is unavailable; this is not a confirmed nonpregnant cohort.
Borderline diagnosis responses are separate and included only in a sensitivity analysis.
Age 20 is an analytic choice, not a clinical screening cutoff; age 18+ is also compared.

Run `python -m pip install -r requirements.txt`, then
`python scripts/analysis/cohort_analysis.py` from the repository root, or run
`notebooks/03_cohort_definition_and_filtering.ipynb` from the root or `notebooks/` directory.
The notebook is self-contained and does not depend on earlier notebook state.
Outputs in `results/cohort/` include cohort flow/counts, diagnosis strata, model/fold
comparisons, out-of-fold predictions, threshold tables, and prevalence/ROC figures.
See `docs/findings/cohort_definition_analysis.md` for the recommendation and interpretation.

The seven comparisons retain the original all-age reference and include adults of all diagnosis
statuses, the primary cohort, ages 18+, ages 35–70, ages 65+, and inclusion of borderline
responses. Cohort choice is based on the question, not the highest AUROC. Ages 35–70 alone do
not implement the USPSTF population: BMI and symptom eligibility are not established here.
All four models use matched five-fold splits within each cohort, training-fold preprocessing,
and one-hot categorical encoding. These are new exploratory cross-validation results, not a
replication of notebook 02's single split. Survey-weighted modelling, design-aware uncertainty,
calibration and separate final evaluation remain outstanding. Weighted prevalence is descriptive
only; models and predictive metrics remain unweighted.

### Survey-weighted calibration (notebook 04)

`notebooks/04_survey_weighted_calibration.ipynb` and `scripts/analysis/weighted_calibration_analysis.py`
extend the fixed primary cohort with WTPH2YR-weighted fitting, calibration and evaluation.
Run `python scripts/analysis/weighted_calibration_analysis.py` after installing
`requirements.txt`. Outputs and the regenerated interpretation report are
`results/weighted_calibration/` and `docs/findings/weighted_calibration_analysis.md`.

Five outer folds hold out entire survey PSUs; three inner grouped folds fit development-only
sigmoid calibration and select exploratory thresholds targeting 95% weighted sensitivity.
SDMVSTRA/SDMVPSU guide splitting and conditional jackknife variance, not prediction.
Class balancing is removed; imputation/scaling remain unweighted within training folds.
The full survey design is retained before selecting the analytic domain.

Calibrated weighted AUROC is 0.715 for demographics and 0.781 for CBC + demographics logistic
regression. The paired conditional interval for the gain includes zero. Mean calibrated CBC
logistic risk is 1.99%, close to weighted prevalence; this alone does not establish calibration.
Its outer-fold policy evaluation defers 1,013 observed tests and misses 3/106 positive labels
(95.8% weighted sensitivity). This does not establish safe clinical deferral. Intervals condition
on fitted scores/thresholds and exclude training variability; independent validation remains.

### Research extension: BMI, robustness and independent evaluation (notebooks 05–06)

The new extension preserves notebooks 01–04. Install `requirements.txt`, then run:

```sh
python scripts/data/acquire_extension_data.py
python scripts/analysis/research_extension.py --bootstrap 100
python scripts/reporting/report_research_extension.py
python scripts/verification/verify_research_extension.py
```

The acquisition step downloads public CDC BMI and 2017–2018 inputs if missing, with a hash
manifest. The analysis adds matched BMI baselines, red/white-cell ablations, low-hemoglobin
and fasting-endpoint sensitivities, 100 full-pipeline PSU resamples, frozen independent-cycle
evaluation, subgroup/selection audits and hypothetical decision curves. Outputs and frozen
models are in `results/research_extension/`; these joblib files are trusted project outputs, not
files to load from unknown sources. Notebooks 05–06 display completed results; notebook 05
can rerun the full analysis by changing `RUN_ANALYSIS`.

CBC adds 0.023 AUROC beyond demographics+BMI in the current cohort, with an exploratory
full-refit interval spanning zero. Ranking improves in the independent earlier cycle while
probability error worsens. See [results](docs/findings/research_extension_results.md),
[literature matrix](literature/extension_evidence_matrix.md),
[draft text](writing/drafts/Research_Extension_Methods_Results.md) and
[publication assessment](docs/findings/publication_readiness.md). These results do not establish
clinical safety, cost savings or readiness for journal submission.
