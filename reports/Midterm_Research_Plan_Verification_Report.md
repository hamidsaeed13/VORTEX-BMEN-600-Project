# Midterm Research Plan Verification Report

**Project:** Team Vortex 600, BMEN 600  
**Review date:** October 15, 2026  
**Reviewed revision:** `347c1b1` on `Hamid-midTermProposal`, including the subsequent working-tree draft and TODO edits present at final verification  
**Submission deadline in the course template:** Friday, October 16, 11:59 p.m.

**The project is feasible, and the preliminary numerical results reproduce, but the current draft needs correction before submission.** The main problems are a seven-page body against a six-page limit, inaccurate descriptions of several important papers, a mismatch between the screening question and the modeled population, misleading interpretation of NPV, and incomplete contributions and milestone ownership.

This report reviews the draft, assignment template and rubric, both notebooks, relevant NHANES files and codebooks, the literature notes and cited sources, and the team contract/workstream plan. It distinguishes confirmed errors from methodological improvements and matters requiring team confirmation. This review changed only files in `reports/`; concurrent edits to the draft and TODO were reread and preserved. Numerical evidence, source hashes, and verification metadata are retained in [the audit evidence file](midterm_verification_evidence.json).

## What passed verification

- **Both notebooks execute successfully.** Their code cells were run sequentially in fresh namespaces using the existing raw files, with plotting directed to a noninteractive backend. This checks computation; it is not a clean-environment installation test or a saved Jupyter-kernel rerun.
- **The reported coverage counts, modeling sample, split, AUROCs, and threshold table reproduce.** The important qualification is that some counts describe measurement availability, not final clinical eligibility.
- **The five core source files have unique, nonmissing `SEQN` identifiers.** There is no observed multiplication of participants in the current merges. Preprocessing is fitted on training data through pipelines; no direct inclusion of HbA1c in the predictor matrix was found.
- **The embedded ROC image exactly matches `code/assets/fig_roc_curves.png` by SHA-256.** Its displayed AUROCs agree with the notebook at the figure's rounding precision.
- **All required report sections are present**, including data/code availability, AI use, author contributions, and references. More than six scholarly sources are cited. The contribution section is present but unfinished.
- **The exploratory limitations are acknowledged.** Lack of survey weighting, final target selection, cross-validation, and confidence intervals is disclosed. The midterm does not require a finished clinical model or all final-project analyses.
- Previously reported fixes to HbA1c category boundaries and education refusal/unknown codes are present. The categorical-encoding problem discussed below remains a separate issue.

## Priority actions before submission

| Priority | Issue | Required action |
|---|---|---|
| Critical | Seven body pages, maximum six | Condense the body and rerender the final PDF. |
| High | Incorrect study descriptions and research-gap claims | Correct Guo, Kamkar, RDW synthesis, comparator framing, and clinical-safety claims. |
| High | Screening question and current cohort do not match | Specify the primary outcome, age range, prior-diabetes policy, and intended use. |
| High | High NPV is presented as reassuring despite many missed positive results | Report missed positives and tests deferred together; remove claims of demonstrated safe deferral. |
| High | Fasting-glucose availability is called a usable sample | Distinguish measured results from eligible fasting results; correct counts for the intended analysis. |
| High | Contributions and milestone owners are incomplete | Complete actual contributions and resolve the remaining research-task owners and Design Critique lead. |
| Medium | Data acquisition date and reproduction instructions are missing | Add the real access date, exact component links, environment, and run instructions. |
| Medium | IEEE citation order is incorrect | Renumber after editing; reference [20] currently appears before [10]. |

## Submission requirements and presentation

### Page count is a confirmed problem

The current [draft](../drafts/Midterm_Research_Plan_Draft.docx) was rendered with bundled LibreOffice 25.2 and every rendered page was inspected. The result is **10 total pages: title page 1, body pages 2–8, and references pages 9–10**. The body is therefore **one page over** the limit in the [course template](../BMEN%20600%20Midterm%20Research%20Plan.dotx). Only the title and references are explicitly excluded from the limit; the availability, AI, and contribution statements need body-page space.

Table 1 now fits together on page 5, and the ROC plot and caption fit together on page 6. No obvious clipping or missing glyphs was found. The earlier snapshot rendered to eight body pages with a split table; those observations were superseded by this final check. Page numbers in this report refer to the latest audit render; Word pagination can differ, so check the actual submission PDF after revision.

The body contains approximately 3,302 whitespace-delimited words including table text. Remove the repeated prevalence/CBC-frequency material at the start of Section 2, shorten the long paper-by-paper account, consolidate repeated limitations, and compress the availability and AI statements. Resize the ROC plot if needed while retaining legibility. Do not add another figure before fixing the page budget.

Suggested six-page allocation: introduction 0.5; background 1.0; dataset 0.8; methods 1.2; preliminary results 1.2; team plan 0.5; availability, AI, and contributions together 0.8. These are planning targets, not additional rubric rules.

### Requirements matrix

| Requirement | Status | Evidence or correction |
|---|---|---|
| Maximum six body pages | Not met | Current render has seven. |
| One final PDF with repository link | Partly met | Draft includes a working hyperlink object; no final submission PDF was found among project deliverables. Live repository visibility remains unverified. |
| Six main sections and required statements | Met for structure | All exist. |
| At least six scholarly sources | Met for quantity | Accuracy and interpretation need the corrections below. |
| Dataset name, source, access date, relevant documentation | Partly met | Name/source present; actual acquisition/access date absent. Generic portal citation is insufficient for component-specific eligibility and weighting. |
| Appropriate analysis and uncertainty plan | Partly met | Models and fold-refitted preprocessing are described; endpoint, threshold selection, survey design, and uncertainty method need specificity. |
| Team-created preliminary table or figure | Met | Table 1 and ROC Figure 1 are present and interpretable, subject to count qualifications. |
| Milestones with responsible team members | Partly met | Assignment and final-deliverable leads are named. Research-task ownership is not explicit, and Design Critique still says lead TBD. |
| Named actual author contributions | Partly met | All names are present, but two contributions remain future work and Emmanuella's contribution is still to be added. |
| AI tools, purposes, and verification | Partly met | Tools and reference checks are described; actual human checks of code, outputs, and final prose need to be stated accurately. |
| README setup and run instructions | Not met | Current README does not explain environment setup or notebook working directory/run steps. |
| IEEE referencing | Needs correction | First-use order is wrong; online sources also need consistent access details. |

The template states a team size of three to four; the signed contract lists five. **Check whether existing instructor permission resolves this discrepancy.** It is not evidence that the team is unauthorized, and no member should be removed from truthful authorship to match the template.

## Research question and interpretation

### The endpoint needs to match the question

**Locations:** title, Section 1 research question, Section 4 “Variables and groups,” and Section 5 model interpretation.

The title promises blood-glucose prediction, but the implemented target is HbA1c ≥6.5%. Section 4 also offers prior self-reported diagnosis as an interchangeable candidate. These represent different outcomes: a fasting measurement, a longer-term glycemic marker, and a history of disease. Prior diagnosis cannot stand in for whether an additional glucose measurement would be abnormal.

Moreover, diabetes-range thresholds do not identify all abnormal glycemia: prediabetes is below HbA1c 6.5% and fasting glucose 126 mg/dL. A single threshold-positive test should be described as a **diabetes-range result**, not automatically a confirmed diagnosis or incident type 2 diabetes. The NIDDK describes different prediabetes thresholds and usual confirmatory testing. [NIDDK tests and diagnosis](https://www.niddk.nih.gov/health-information/diabetes/overview/tests-diagnosis).

Choose one primary planned endpoint before submission and explain secondary analyses. Two coherent options are:

| Choice | What the plan must say |
|---|---|
| Retain the current HbA1c model | Rename the primary question around diabetes-range HbA1c; make eligible fasting glucose a secondary check for an association caused partly by red-cell effects. |
| Retain the blood-glucose question | Make valid fasting plasma glucose the primary endpoint; retain the HbA1c model as preliminary feasibility work and a secondary analysis. |

Use self-reported diagnosis primarily to define eligibility or stratify results. Decide explicitly how borderline, unknown, and treated diabetes are handled. These are proposed research choices, not changes made by this review.

### The current model mostly detects elevated HbA1c in people already diagnosed

**Locations:** notebook 02, cells 4–6; Sections 3–5. Notebook cell numbers in this report are one-based and include Markdown cells.

The modeling cohort has 6,678 participants and 717 positive labels. **565 of the 717 positives, or 78.8%, already report a diabetes diagnosis.** There are 816 participants with a prior diagnosis in total; 251 have HbA1c below 6.5%. The current model is not an undiagnosed-diabetes screening model, and a negative label in a treated person cannot establish that glucose monitoring is unnecessary.

The cohort also includes **709 participants younger than 18, none of whom has a positive label**, and **943 younger than 20**. All 943 have structurally missing adult education, which is mode-imputed. Thirty-seven participants have recorded pregnancy status indicating pregnancy. These inclusions are not automatically invalid for a broad feasibility analysis, but they conflict with an unspecified adult opportunistic-screening interpretation and affect the comparability of reported metrics.

Specify the intended age range and known-diabetes/pregnancy policy. If the intended application is screening previously undiagnosed adults, rerun that cohort and report its new counts and uncertainty. Do not reuse the current sample size and metrics after changing eligibility. Distinguish missing pregnancy data outside NHANES public-release age ranges from confirmed absence of pregnancy.

### High NPV does not demonstrate safe testing deferral

**Locations:** Section 5 “NPV stayed high,” notebook 02 cells 15 and 18, and Section 1 “could safely skip it.”

The test set contains 179 positive and 1,491 negative labels. A rule predicting every participant negative has **89.3% NPV and zero sensitivity**. Thus, the lower end of the draft's “89–99%” NPV range is compatible with missing nearly every positive case.

The following counts were recomputed from the current random-forest predictions. “Deferred” assumes, solely for illustration, that every participant below the threshold would not receive the target test. These are label-based simulations, not observed clinical decisions.

| Threshold | Tests flagged | Tests deferred | Positive labels missed | Sensitivity | NPV |
|---|---:|---:|---:|---:|---:|
| 0.10 | 1,020 | 650 / 1,670, 38.9% | 10 / 179, 5.6% | 94.4% | 98.5% |
| 0.30 | 450 | 1,220 / 1,670, 73.1% | 56 / 179, 31.3% | 68.7% | 95.4% |
| 0.70 | 3 | 1,667 / 1,670, 99.8% | 178 / 179, 99.4% | 0.6% | 89.3% |

The highlighted 0.30 example in the draft misses **56 of 179 positive labels**. Its 1,220 deferred tests comprise 1,164 target-negative participants and 56 target-positive participants; calling all 1,220 tests “unnecessary” would be wrong. Even a target-negative result can have a clinical reason for testing that this dataset does not capture.

Replace the reassuring NPV wording with the explicit trade-off. Specify a high-sensitivity operating objective and choose the threshold inside training/validation data. Any numerical sensitivity target must be justified as a research operating point; it is not automatically a clinically approved safety standard. Allow the possibility that the data support little or no deferral at the required sensitivity.

### Cost and clinical benefit are hypotheses

**Locations:** Section 2 final reflex-testing paragraph and README motivation, which still describes blood glucose as a costlier test.

The cited Horton paper's Table 3 expresses test prices relative to glucose. CBC costs **1.33–6.67 times glucose** across its five hospitals. It supports the frequency of CBC ordering, but not the premise that glucose costs more than CBC or that the listed bundled orders are routinely inappropriate. [Horton et al.](https://doi.org/10.1093/ajcp/aqy165).

Frame the application as using an **already available CBC** to study the marginal value of an additional glycemic test. Section 2's claim that CBC must justify “drawing extra blood” contradicts that premise. Define the clinical setting and intended user, and keep cost estimates as explicit scenarios until local prices and workflow evidence exist. Cross-sectional NHANES does not observe the counterfactual harm of withholding a test or establish prospective diagnostic safety.

## Data and code issues

### Correct the participant and missingness descriptions

**Locations:** Section 3 dataset paragraph; notebook 01 cell 7; README “No cost or ordering-policy data.”

`DEMO_L` includes **11,933 interviewed participants: 8,860 examined and 3,073 interviewed only**. It is not the full examined sample. CBC eligibility starts at age one; HbA1c and the fasting component start at age 12. HbA1c is therefore not measured on every examined participant. [DEMO documentation](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DEMO_L.htm), [CBC documentation](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/CBC_L.htm), [HbA1c documentation](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/GHB_L.htm).

Missing values combine interview-only participation, age ineligibility, subsampling, specimen availability, and item nonresponse. The statement that this is “not missing data in the usual sense” is too broad. Add a short cohort-flow description and distinguish the full interview denominator from the eligible analysis denominator. Restore the cross-sectional design and noninstitutionalized population qualifiers omitted from the current shortened dataset description. The source survey uses a multistage, stratified, clustered design.

### Fasting eligibility changes the usable sample

**Locations:** Section 4 candidate sample sizes, Table 1, notebook 01 cells 10–11 and 20.

The values 3,672 measured glucose results and 3,657 with WBC are arithmetically correct. However, **311 measured glucose results have a true zero fasting-subsample weight**; 307 of these also have WBC. The component codebook assigns zero weights to results without the required fasting eligibility or without a laboratory result. For the measured subset, the issue is fasting eligibility. [GLU documentation](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/GLU_L.htm).

Using the positive fasting-weight subset yields:

| Count | Current availability count | Eligible fasting-weight subset |
|---|---:|---:|
| Measured glucose | 3,672 | 3,361 |
| Measured glucose plus WBC | 3,657 | 3,350 |
| Glucose ≥126 mg/dL, without a CBC restriction | 430 | 384 |

These revised counts still precede any adult-only, prior-diagnosis, pregnancy, or complete-predictor restriction. Either relabel Table 1 as raw measurement availability and add this qualification, or report the properly restricted analytic counts. Do not apply a fasting diagnostic threshold indiscriminately to the excluded results.

### The current pandas reader does not preserve exact SAS zeros

**Locations:** both notebooks' `pd.read_sas` calls; future weight filtering.

In the audited environment, pandas 2.3.3 reads certain SAS transport zeros as approximately `5.397605346934028e-79`. A second reader, `pyreadstat` 1.2.6 with Latin-1 decoding, reads them as exact zero. This was verified on the same local binaries and agrees with the codebook frequencies. For example, all 635 zero fasting weights become tiny positive values through the current pandas reader.

This makes a future `WTSAF2YR > 0` filter unsafe unless import handling is corrected first. It also affects some age, income, and CBC zeros. The tiny values do not invalidate the reproduction of the current scores, but they matter for equality checks and eligibility.

Use a reader that preserves these values, or explicitly normalize the verified zero representation after checking the affected variables. Add meaningful checks against codebook counts: 635 zero fasting weights and 3,361 eligible measured glucose results. Avoid an arbitrary broad near-zero rule applied blindly to every scientific measurement.

### Specify the appropriate survey design

**Locations:** notebook 01 cell 6, notebook 02 cell 4, Sections 3–4, and the October 19–23 milestone.

Both notebooks currently discard weights and survey design variables. “Apply NHANES survey weights” is too vague for the next phase. CBC/HbA1c analyses in this cycle use the **phlebotomy weight `WTPH2YR`**; fasting analyses use **`WTSAF2YR`** with appropriate eligibility. Preserve **`SDMVSTRA` and `SDMVPSU`** for design-aware uncertainty. [CBC analytic notes](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/CBC_L.htm), [GLU analytic notes](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/GLU_L.htm).

State whether the target is performance in this analytic sample or a population-level quantity. Separate weighted evaluation from the choice to weight model fitting. Class-balancing weights are not survey weights. Ordinary participant bootstrap intervals do not account for NHANES clustering and stratification, and variation across CV folds should not automatically be called a confidence interval. A unique `SEQN` prevents duplicate-person leakage but does not make survey participants statistically independent in every sense.

### Encode demographic categories appropriately

**Locations:** notebook 02 cells 9–12 and its “Next steps.”

Race/ethnicity codes are currently passed as numbers to logistic regression, imposing an arbitrary numeric ordering and equal-distance relationship. Education is also treated as a single numeric effect without justification. The notebook acknowledges one-hot encoding as future work; it is a material preprocessing correction for the final comparison. Scikit-learn trees also split numeric codes by numeric thresholds, so they do not automatically interpret nominal categories as unordered. [OneHotEncoder documentation](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html).

Use one-hot encoding for nominal variables, handle unseen categories, and justify any ordinal education effect. Fit the encoder and imputer inside each training fold. Restrict or explicitly handle structurally unavailable adult education rather than imputing an adult education category for all adolescents.

### Calibrate scores before calling them individual probabilities

**Locations:** Section 1 probability/confidence language; notebook 02 cell 12.

All three models use balanced class weights. In the existing test set, positive-label prevalence is **10.7%**, but mean predicted scores are **41.3%** for demographics-only logistic regression, **37.8%** for full logistic regression, and **19.7%** for the random forest. These values reveal a substantial calibration-in-the-large mismatch on this sample. They should not be read as validated patient-level probabilities.

Add reliability plots and a proper scoring rule, then fit any calibrator within the development data. The random forest's audited Brier score is 0.0941, versus 0.0957 for a constant training-prevalence prediction; that comparison alone does not isolate calibration. [Scikit-learn calibration guidance](https://scikit-learn.org/stable/modules/calibration.html).

### Strengthen the comparison without overstating current defects

**Locations:** notebook 02 cell 12; Section 5 “CBC adds real value.”

The existing logistic-regression comparison is already a useful same-family ablation: **0.74295 without CBC versus 0.78304 with CBC** on the same split. Do not dismiss that evidence merely because the random forest has no matching demographics-only version in the notebook.

An additional audit-only demographics random forest, with the same split and forest settings, gave **0.73295**, versus **0.81126** with CBC. This supports preliminary incremental discrimination in the current cohort. It does not establish transportability, calibrated risk, or the safety of skipping tests. Add this matched comparison to the planned evaluation, address encoding, and report uncertainty in paired model differences.

The existing feature-importance chart is based on impurity reduction. It cannot establish the claim that “we need a model that uses several variables together” or that age is a causal driver. Compare an age-only/simple-rule baseline and use held-out permutation importance if interpretation is important. Correlated blood indices also complicate individual importance attribution. [Scikit-learn forest importance example](https://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html).

### Improve reproducibility and documentation

**Locations:** README, both notebook setup cells, notebook 01 “Next steps,” MANUAL_TODO, and Data and Code Availability.

- Both notebooks assume the working directory is `code/` because `DATA_DIR = Path("..") / "data" / "raw"`. Document this or make root discovery robust. A repository-root execution can fail despite the notebooks working in the audited directory.
- Add installation instructions and a dependency/environment file. The successful computation used Python 3.9.6, pandas 2.3.3, NumPy 2.0.2, scikit-learn 1.6.1, and SciPy 1.13.1. Record the actual intended supported environment rather than treating this audit environment as a universal requirement.
- Save tables and figure assets explicitly from the analysis. Notebook 02 currently displays plots but has no `savefig` calls that regenerate the committed `code/assets` files. The current embedded figure matches its asset, but future updates need an automated path to keep them synchronized.
- Add merge validation and assertions for cohort counts, label availability, and key eligibility conditions. Remove blanket warning suppression or restrict it to known harmless warnings so convergence problems remain visible.
- The README still describes project scoping and dataset acquisition as underway. Notebook 01 says modeling packages are not installed and proposes a future notebook 02 despite the existing model. Update these stale statements.
- MANUAL_TODO says nothing has been committed. At review start, the tree was clean and commit `347c1b1` already contained the draft, both notebooks, and literature material. It also says rendering is unavailable; this audit successfully rendered the draft. Replace those stale status claims when applying revisions.
- The local cached `origin/main` contains notebook 01 but not the draft or notebook 02. The current proposal branch has no displayed upstream. These facts do **not** prove the current remote is missing work. Live repository visibility could not be established through the available web retrieval; verify the exact submitted link and reviewer access before submission.

### Correct the statement that NHANES has no other glucose measurement

**Location:** README “Target definition.”

The repository already contains `BIOPRO_L.xpt`, whose `LBXSGL` variable is serum glucose. There are **6,357 measured serum-glucose values**, including **2,857 participants without a value in the fasting-glucose component**. Thus, the blanket assertion that NHANES has no relevant glucose measurement outside the fasting component is too broad. [BIOPRO codebook](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BIOPRO_L.htm).

This does not make serum glucose interchangeable with fasting plasma glucose or a diagnostic random-plasma-glucose test. Review specimen, method, fasting-status, and clinical-definition differences before considering it as a separate outcome. The current three-candidate framing should acknowledge the distinction rather than exclude it by an inaccurate dataset claim.

## Literature and claim corrections

The following checks use the draft's current reference numbering. Renumber only after revising the text. Fourteen local full texts were inspected, with targeted primary-source checks for unavailable papers and current webpages. Abstract-only verification is identified below; it must not be represented as full-text review.

### Highest priority corrections

1. **Guo [5], Section 2: incorrect predictors and omitted endpoint distinction.** The paper's predictor set includes age, BMI, sex, NLR, PLR, and CBC features; the draft's “using only CBC data” description is incorrect. Its label is **HbA1c ≥5.7%**, including prediabetes, not the draft's ≥6.5% label. The stated AUROCs 0.821/0.791 and cohort sizes 70,725/26,650 match the local final PDF. Correct both the draft and literature README. [Guo et al.](https://www.nature.com/articles/s41598-026-59213-3).

2. **Research gap, Section 2: the claim that none test the needed sensitivity/NPV trade-off is overstated.** Kamkar [7] explicitly reports a 0.20 threshold with sensitivity 0.618, specificity 0.707, and NPV 0.889. It studies incident diabetes in initially diabetes-free adults and includes non-CBC clinical/metabolic/renal predictors. Recast the contribution as a specific NHANES replication, matched incremental-value comparison, and high-sensitivity deferral analysis; specify how that policy analysis differs from already reported threshold metrics. Its full text was accessible during this review, so its “blocked” status in the notes is stale. [Kamkar et al. full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC13475539/).

3. **RDW synthesis, Section 2: the alleged opposite direction is incorrect.** Engström [9] reports that lower RDW predicts incident diabetes, while RDW is positively associated with HbA1c. Higher RDW is therefore inversely associated with both incident diabetes in [9] and poor control in Yin [20]. The relevant contrast is HbA1c association versus incident disease, not the claimed onset/control reversal. Engström was checked through its primary abstract, not full text. [Engström et al.](https://pubmed.ncbi.nlm.nih.gov/24471821/). Yin's OR 0.3, CI 0.2–0.7 is supported by its Model 2; the most adjusted model has CI 0.2–0.6. [Yin et al.](https://doi.org/10.2147/TCRM.S155753).

4. **Liu [15], Sections 2, 4, and 5: not a directly comparable numerical benchmark.** The quoted AUROC 0.909, sensitivity 70.3%, and NPV 92.6% are accurate. However, the study uses earlier NHANES cycles, nonpregnant adults aged at least 20 without prior diabetes, a combined HbA1c/fasting-glucose/OGTT endpoint, and a much broader nonlaboratory feature set. Its analytic prevalence is 19.1%, versus 10.7% here. It also selects a threshold by test-set F1, which should not be copied as a validation practice. Treat it as contextual evidence and fit a matched baseline within the project's own cohort. NPV especially cannot be compared without considering prevalence. [Liu et al.](https://ai.jmir.org/2025/1/e68260).

5. **Reflex-testing evidence [17–18], Section 2: clinical safety is overstated.** McDermott is a feasibility preprint about ferritin ordering and explicitly describes limitations of replacing manual ordering. Predicting historical ordering is not the same as validating medical necessity or outcomes after deferral. Bang is a risk-score development/validation study, not a trial establishing safe test reduction. Replace the safety claim with feasibility language. [McDermott et al.](https://arxiv.org/abs/2302.00794), [Bang et al. abstract](https://pubmed.ncbi.nlm.nih.gov/19949143/).

### Further corrections and verification ledger

| Reference | Verification and action |
|---|---|
| [1] Horton | Local full text supports CBC being most common at four of five sites. Does not establish inappropriate bundling. Prices contradict “glucose costlier than CBC.” |
| [2] IDF Atlas | 589 million adults aged 20–79 and 43% undiagnosed are supported. Identify the estimate as 2024, published in the 2025 edition. |
| [3] NCHS Data Brief 516 | 15.8% total, 11.3% diagnosed, and 4.5% undiagnosed match. Specify adults aged at least 20 and crude estimates for August 2021–August 2023. |
| [4] CDC webpage | Current title matches, but current figures differ from the historical NCHS percentages. Use [3] for those exact historical figures and give webpage access dates. |
| [5] Guo | Numerical findings supported; feature set and label need the correction above. |
| [6] Mansoori | 2023, volume 13, article 663 is correct despite the local filename containing 2022. The roughly 9,000 observations refer to a balanced analytic dataset after SMOTE, not simply 9,000 original independent participants; the initial cohort is 9,704. Clarify the sample description. |
| [7] Kamkar | Primary full text available and inspected. Add complete publication details and correct the gap claim. |
| [8] Veeranna | Metadata and primary abstract support an RDW–HbA1c association; full text not reviewed. Do not imply clinical prediction is established by association. |
| [9] Engström | Abstract confirms the synthesis error. The DOCX author name B. Hedblad is correct; the literature README incorrectly says Hedblek. |
| [10] Park | Local full text supports HR 1.55, CI 1.10–2.18, n=4,211, and 592 events. Preserve the non-obese Korean adult cohort context. |
| [11] Gkrania-Klotsas | RR 1.61, CI 1.45–1.79 pools cross-sectional and prospective evidence. Do not describe it as incident-only; the prospective-only estimate is 1.48, CI 1.22–1.79. Existing bias caveat is useful. |
| [12] Lorenzo | n=866, lymphocyte OR 1.96, CI 1.13–3.37, and NLR null findings are supported. Describe insulin sensitivity as a possible partial explanation, not an established causal mechanism. |
| [13] Mertoglu | NLR/PLR directional summary is supported. This is a small cross-sectional comparison, not prospective validation of a screening policy. |
| [14] Rahman | Abstract reports 99.36%, while a table reports 99.37%; reported CV accuracies are lower. Summarize cautiously as high internal performance in a small symptoms dataset, without inventing the cause of the high headline result. |
| [15] Liu | Quoted metrics match; direct-comparison framing does not. |
| [16] English | Twelve-study review and possible HbA1c distortion are supported. Replace deterministic “raises ... regardless” wording with possible spurious elevation; effects depend on anemia type and context. |
| [17] McDermott | Author/title/arXiv details match. Identify it as a preprint and avoid claims of established clinical safety. |
| [18] Bang | Metadata and abstract verified. Full text remains unreviewed because direct retrieval encountered a challenge; an indexed full-text link is not proof of successful full-text review. |
| [19] NHANES | Add component-specific codebooks and the relevant survey operations documentation instead of relying only on a generic portal citation. |
| [20] Yin | Local full text supports the quoted Model 2 estimate; cross-study directional interpretation and reference order need correction. |

**Additional unsupported sentence:** Section 3 asserts that clinical cutoffs were developed primarily in non-Hispanic white populations. The draft provides no supporting citation, and the International Expert Committee report describes evidence from multiple populations. Remove the historical assertion while retaining the justified plan to check subgroup performance and calibration. [International Expert Committee report](https://diabetesjournals.org/care/article/32/7/1327/26886/International-Expert-Committee-Report-on-the-Role).

**Verification statement:** the AI paragraph and literature README overstate the completeness of earlier fact-checking. After these corrections, describe the actual verification scope and distinguish full text from abstracts. Do not use a paper title as sufficient evidence for a direction of association, predictor set, or safety conclusion.

## Team plan and responsible reporting

**Author Contributions:** all five names are now present, and the earlier bracketed editing note is gone. However, Jacob Kraft and Ahenkan Yeboah are still described as doing future review, and Emmanuella Osifo's contribution is explicitly still to be added. Confirm completed contributions and fill the remaining gap. Standing roles do not prove that specific work has been completed; do not convert planned reviewing into completed reviewing.

**Section 6:** the current draft names assignment leads and Emmanuella as final-report/presentation lead. Design Critique still says “lead TBD,” while ownership of the endpoint/cohort decision, weighting, model validation, and threshold/uncertainty analysis is not explicit. Add owners for these research tasks and make review responsibility clear. The workbook schedules stakeholder work October 5–23, whereas the draft says it begins October 19; reconcile that timing.

**AI-Assisted Work:** retain the tools actually used and their substantive purposes, then briefly state the checks the team actually performed on references, code, outputs, and writing. An automated audit should not be described as a named team member's independent review. Full chat histories are not required by the template.

**Access and use statements:** add the real acquisition/access date from the team's records; do not substitute the audit date or infer it solely from file timestamps. Qualify Section 3's blanket statement that no “approval” is needed by distinguishing public data access from the team's institution/course requirements. Cite the applicable public-use terms. No new approval requirement is inferred by this review.

**Internal literature workflow:** the workstream plan advises excluding papers with zero or few citations. Replace that rule with appraisal of methods, relevance, validation, and bias; citation counts would systematically exclude recent work the draft itself uses. This is an improvement, not a midterm submission requirement.

## Suggested revision language

### Research contribution

> This project will estimate the incremental value of CBC features over a matched demographic baseline in NHANES August 2021–August 2023. We will quantify the trade-off between tests deferred and missed diabetes-range results at prespecified high-sensitivity operating points. The study is a retrospective feasibility analysis; clinical safety and economic benefit require additional validation.

Add the chosen endpoint and age/prior-diagnosis eligibility directly to this statement. If HbA1c remains primary, use that term in the title and question instead of implying that the present results predict fasting glucose.

### Preliminary result interpretation

> In the current exploratory cohort, adding CBC features increased held-out logistic-regression AUROC from 0.743 to 0.783; the CBC-plus-demographics random forest achieved 0.811. At a score threshold of 0.30, the forest flagged 450 of 1,670 participants but missed 56 of 179 positive HbA1c labels. At 0.10 it missed 10 of 179 while flagging 1,020 participants. These results support further evaluation of predictive signal but do not establish that withholding testing is safe.

These sentences refer to the existing cohort and must be updated if cohort definitions or preprocessing change.

### Evaluation plan

> Preprocessing, model selection, calibration, and threshold selection will use development data only. We will evaluate matched demographic and CBC-plus-demographic models on the same participants, reporting discrimination, calibration, sensitivity, NPV, tests deferred, and missed positive results. Survey-weighted estimates and uncertainty will use the appropriate component weights and sampling-design variables. We will examine subgroup performance and compare the primary result with an alternative glycemic endpoint to assess sensitivity to HbA1c-related measurement effects.

Choose a concrete implementation for this plan. The existing test set has already been inspected across models and thresholds; treat it as exploratory. For final evaluation, use nested validation or an independent holdout that has not influenced the model/policy choices, rather than describing the current inspected split as untouched.

## Recommended sequence of work

1. **Correct the draft's factual and interpretive errors first.** Update the literature descriptions, cost premise, NPV discussion, participant description, and fasting-eligibility qualification. Remove unsupported safety and necessity claims.
2. **Nominate the primary endpoint and cohort.** Record the main analysis and secondary checks, with a defensible threshold-selection objective. A clear plan is required now; a fully validated final model is not.
3. **Complete the mandatory reporting details.** Named actual contributions, milestone owners, data access date, reproducible setup/run instructions, and accurate AI verification scope.
4. **Reduce and render.** Fit the body into six pages, keep Table 1 together, preserve a readable figure, renumber citations, and inspect the actual final PDF.
5. **Verify submission materials.** Confirm the repository URL exposes the intended revision to the grader and submit the PDF through D2L. This review has not committed, pushed, or submitted anything.
6. **For the final project, implement the stronger analysis.** Correct imports/eligibility and categorical encoding; preserve survey variables; use matched baselines, development-only threshold/calibration selection, appropriate uncertainty, and HbA1c-versus-glucose sensitivity analyses. Do these before adding more complex model families.

## Verification boundaries

The audit establishes reproducibility of the current calculations and identifies specific source, design, and submission problems. It does not verify team members' personal contributions, institutional determinations, instructor permission for team size, the original download date, live remote repository permissions, or D2L submission. Those remain factual confirmations for the team, not assumptions to fill in.

The numerical evidence includes additional diagnostic calculations on the existing split. Its optional 2,000-draw bootstrap results resample fixed held-out predictions as independent observations; they do not refit the models or account for the NHANES survey design and must not be presented as final population-level uncertainty. This review did not edit the plan or notebooks; it incorporated the concurrent draft changes so the team can apply the remaining corrections deliberately.
