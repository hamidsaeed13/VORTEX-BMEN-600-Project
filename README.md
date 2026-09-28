# Lab Test Recommendation System — Predicting Test Necessity from CBC Panels

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

This project investigates whether a cheap, near-universally-ordered baseline test
— the Complete Blood Count (CBC), combined with basic demographics — can predict
the likely outcome of an additional, costlier test (blood glucose), so that
downstream ordering decisions can be risk-stratified: prioritize testing for
patients likely to have an abnormal result, and avoid unnecessary testing for
patients who are very likely to be normal.

## Research Question

> Using only CBC parameters and demographics, can we predict the probability
> that a patient's blood glucose result would be abnormal — at a confidence
> level high enough to responsibly inform test-ordering decisions, without
> materially increasing the risk of a missed diabetes diagnosis?

## Why This Matters

- **Cost asymmetry:** an unnecessary glucose test costs a few dollars; a missed
  diabetes diagnosis (from skipping a needed test) can lead to delayed
  treatment and downstream complications. Any recommendation policy must be
  built around this asymmetry, not overall accuracy alone.
- **Opportunistic screening:** CBC is already collected for many patients for
  unrelated reasons, so there is no additional collection cost to using it as
  a predictor.

## Dataset

**NHANES (National Health and Nutrition Examination Survey), CDC/NCHS**

- Publicly available at [wwwn.cdc.gov/nchs/nhanes](https://wwwn.cdc.gov/nchs/nhanes/)
- CBC laboratory component (`CBC_*`): WBC, RBC, hemoglobin, hematocrit, MCV,
  MCH, MCHC, platelet count, and 5-part WBC differential (neutrophils,
  lymphocytes, monocytes, eosinophils, basophils)
- Glycemic outcome components (`GLU_*`, `GHB_*`, `DIQ_*`): fasting plasma
  glucose, HbA1c, and self-reported diabetes diagnosis
- Demographics component (`DEMO_*`): age, sex, and other covariates
- Records are linked across components via the shared participant identifier
  `SEQN`

## Known Uncertainties / Open Risks

1. **Target definition:** NHANES has no "random glucose" measurement — outcome
   labels will be defined from fasting glucose, HbA1c, and/or self-reported
   diagnosis, which reflect chronic glycemic control rather than a single
   opportunistic draw. This choice materially affects what the model is
   actually predicting.
2. **Decision threshold, not just accuracy:** because of the cost asymmetry
   between an unnecessary test and a missed diagnosis, the model must be
   evaluated on sensitivity/NPV at clinically defensible thresholds, not
   overall accuracy or AUROC alone.
3. **No cost or ordering-policy data in NHANES:** NHANES gives every
   participant the full standardized battery, so it can validate the
   *predictive* signal (does CBC correlate with glucose abnormality) but not
   the economic impact of a skip/order policy. Cost assumptions and the
   harm-of-a-missed-diagnosis will need to be defined separately by the team.

## Planned Approach

1. Acquire and merge relevant NHANES cycles (CBC + glucose/HbA1c/DIQ +
   demographics) via `SEQN`.
2. Define the target label(s) and document the clinical justification for the
   chosen glycemic cutoffs.
3. Exploratory data analysis and handling of class imbalance.
4. Train and compare classification models (e.g., logistic regression, random
   forest, gradient boosting) for predicting abnormal glycemic status from
   CBC + demographics.
5. Evaluate at multiple decision thresholds, reporting sensitivity/specificity/
   NPV trade-offs rather than a single accuracy figure.
6. Translate model output into a test-recommendation policy (order / consider /
   skip) with an explicit cost-benefit framing.

## Repository Structure

```
.
├── README.md
├── data/            # raw and processed NHANES extracts
├── notebooks/        # EDA and modeling notebooks
└── src/               # reusable data processing / modeling code
```

## Status

Project scoping stage — dataset acquisition and target-label definition in
progress.
