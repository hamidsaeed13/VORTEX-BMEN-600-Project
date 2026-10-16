# Lab Test Recommendation System — Predicting Diabetes-Range HbA1c from CBC Panels

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
   demographics) via `SEQN`. *(Done — see `code/01_eda_cbc_glucose_demographics.ipynb`.)*
2. Define the target label(s) and document the clinical justification for the
   chosen glycemic cutoffs, including the intended age/prior-diagnosis
   eligibility. *(In progress — current exploratory work uses HbA1c ≥6.5% on
   all ages/diagnosis statuses; see Known Uncertainties above.)*
3. Exploratory data analysis and handling of class imbalance. *(Done — see
   notebook 01; class weighting used in the baseline models below.)*
4. Train and compare classification models (logistic regression, random
   forest, gradient boosting) for predicting diabetes-range HbA1c from CBC +
   demographics. *(First pass done — see `code/02_baseline_model_and_figures.ipynb`;
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
├── data/                # raw NHANES extracts and codebooks
├── code/                # notebooks and reusable data processing / modeling code
├── literature_review/   # source papers for Section 2, with a README documenting
│                         # exactly what was verified against each one
├── drafts/               # the Midterm Research Plan draft
└── reports/              # independent verification / audit reports
```

## Setup and Running the Notebooks

- Requires Python 3.9+ with `pandas`, `numpy`, `matplotlib`, and `scikit-learn`.
- The notebooks use relative data paths (`../data/raw`), so **run them from
  inside the `code/` directory** (or open them in Jupyter with `code/` as the
  working directory) — running from the repository root will fail to find the
  data files.
- `code/01_eda_cbc_glucose_demographics.ipynb` loads and merges the raw NHANES
  files and produces the descriptive statistics and figures used in Section 5.
- `code/02_baseline_model_and_figures.ipynb` depends on nothing from notebook
  01 being run first (it reloads the raw files itself) and produces the
  baseline model, ROC curves, and threshold table used in Section 5.

## Status

First exploratory baseline model complete (AUROC 0.743 demographics-only →
0.811 CBC+demographics, random forest); target-label finalization, survey
weighting, categorical encoding, and cross-validation are the next steps
before the final report. See `MANUAL_TODO.md` and
`reports/Midterm_Research_Plan_Verification_Report.md` for the current list of
open items.
