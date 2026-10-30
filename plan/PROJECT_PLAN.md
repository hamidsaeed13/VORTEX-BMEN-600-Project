# Project Plan — Lab Test Recommendation System

Start-to-end research/technical plan for predicting diabetes-range HbA1c from CBC + demographics.
Course logistics (assignments, grading, submission, peer evaluation, presentations) are
intentionally excluded — this tracks the research project itself.

Checkboxes reflect status as of this writing. `[x]` = done, `[~]` = in progress / partially done,
`[ ]` = not started. Re-check this list as work lands rather than trusting it blindly — it's a
snapshot.

---

## Phase 1 — Data acquisition & merging

- [x] Identify and download NHANES 2021–2023 cycle files: `DEMO_L`, `CBC_L`, `GLU_L`, `GHB_L`,
      `DIQ_L` (`data/raw/`)
- [x] Merge all five on `SEQN` (`code/01_eda_cbc_glucose_demographics.ipynb`)
- [ ] Record the real dataset access/download date
- [ ] Fix `pd.read_sas` SAS-zero bug (zeros read as ~5.4e-79) — use `pyreadstat` or explicitly
      snap near-zero values before any weight-based filtering

## Phase 2 — Exploratory data analysis

- [x] Coverage analysis: how much usable data under each candidate label (fasting glucose vs.
      HbA1c vs. self-report)
- [x] Demographic distributions, CBC predictor distributions, glycemic outcome distributions
- [x] Exploratory comparison of the three candidate label definitions
- [x] CBC vs. glycemic-status first look (boxplots, group means/medians)
- [x] Missingness summary

## Phase 3 — Cohort / eligibility definition (blocking item)

- [ ] Decide and document the intended population: age range (12+? adults only?), known-diagnosis
      policy (include/exclude/stratify), pregnancy exclusion
- [ ] Apply `WTSAF2YR > 0` eligibility filter for any fasting-glucose analysis (not currently
      applied — current "measured" counts include ineligible zero-weight records)
- [ ] Recompute cohort counts, class balance, and the "78.8% already diagnosed" caveat once
      eligibility is applied — do not reuse the current exploratory numbers unchanged
- [ ] Finalize the primary target label (currently HbA1c ≥6.5%, exploratory) and document the
      clinical justification; keep fasting glucose as the secondary check

## Phase 4 — Data processing / cleaning pipeline

- [x] Narrow raw files to the variables actually used, with renamed columns
- [x] Recode sentinel codes to missing for `DMDEDUC2` (7/9 → NaN)
- [ ] Extend sentinel recoding to every other categorical/self-report column kept (e.g. `DIQ010`
      7/9)
- [ ] Add a short cohort-flow description distinguishing interview-only (`n=3,073`) vs. examined
      (`n=8,860`) participants, and age-ineligibility vs. true item nonresponse
- [ ] Decide missing-data strategy per variable type (see Phase 5) and justify it
- [ ] Add merge-validation assertions (unique `SEQN`, expected row counts, expected label
      availability) so a broken merge fails loudly instead of silently

## Phase 5 — Missing data handling

- [x] Baseline: median-impute numeric CBC/age/income; most-frequent-impute categorical
      demographics
- [ ] Move imputers inside the `ColumnTransformer`/pipeline so they refit per CV fold (not fit
      once on the full sample)
- [ ] Consider a missingness indicator for `education`/`income_pir`, since missingness there is
      structural (e.g. adult education is undefined under age 20), not random

## Phase 6 — Encoding categorical variables

- [ ] `sex` (`RIAGENDR`): explicit `OneHotEncoder(drop="if_binary")` instead of raw int
- [ ] `race_eth` (`RIDRETH3`): `OneHotEncoder(handle_unknown="ignore")` — nominal, nothing ordinal
      about it
- [ ] `education` (`DMDEDUC2`): decide ordinal (`OrdinalEncoder` with an explicit category order)
      vs. one-hot, and justify the choice — currently passed as raw numeric codes to both logistic
      regression and random forest, which is a real correctness bug
- [ ] Fit every encoder inside the training fold only, with `handle_unknown="ignore"` so an unseen
      category in held-out data doesn't break the pipeline

## Phase 7 — Collinearity check / PCA (diagnostic, not a replacement for raw features)

- [ ] Compute correlation matrix + VIF on the numeric CBC block before deciding anything further
      (already have a correlation heatmap; extend to VIF)
- [ ] Address the WBC 5-part differential being compositional data (`lymph_pct + neut_pct +
      mono_pct + eos_pct + baso_pct ≈ 100%`) — drop one category or use a log-ratio transform
      before PCA/linear models
- [ ] Note the algebraic relationships among `hemoglobin`/`hematocrit`/`mcv`/`mch`/`mchc`
- [ ] Run PCA (after scaling, after resolving the compositional issue) as:
  - [ ] a 2D/3D PC1-vs-PC2 scatter colored by HbA1c status
  - [ ] an optional secondary model arm (compressed CBC representation vs. raw features) as a
        robustness check — not the primary/headline model, to preserve interpretability for the
        eventual order/skip policy
  - [ ] choose `n_components` via scree-plot elbow or ~90–95% explained variance; fit only inside
        the training fold of each CV split

## Phase 8 — Survey design (NHANES-specific)

- [ ] Apply `WTPH2YR` for CBC/HbA1c analyses, `WTSAF2YR` (with eligibility) for fasting glucose
- [ ] Preserve `SDMVSTRA`/`SDMVPSU` for design-aware uncertainty
- [ ] State explicitly whether reported performance targets the analytic sample or a
      population-level estimate; keep class-balancing weights conceptually separate from survey
      weights

## Phase 9 — Explore other relevant factors (feature expansion)

The current model only uses the CBC panel + 5 demographic variables (`age_years`, `sex`,
`race_eth`, `education`, `income_pir`). Several other NHANES-measured factors are plausible
predictors of diabetes-range HbA1c and are either already sitting unused in this repo or are a
cheap additional download. Each one needs its own task: pull the variable(s), check coverage/
eligibility overlap with the existing modeling cohort, and test whether it adds incremental value
over the current CBC+demographics model (same ablation approach already used for CBC vs.
demographics-only).

### Already downloaded in `data/raw/laboratory/`, not yet used

- [ ] **Fasting/refrigerated serum glucose** (`BIOPRO_L`, `LBXSGL`) — an alternate glucose
      measurement already flagged in the README as not yet incorporated; check how it relates to
      the fasting (`GLU_L`) and HbA1c labels before treating it as a feature vs. an outcome
- [ ] **Liver enzymes** (`BIOPRO_L`: `LBXSATSI` ALT, `LBXSASSI` AST, `LBXSGTSI` GGT, `LBXSAPSI`
      ALP) — nonalcoholic fatty liver disease is strongly associated with insulin resistance/T2D
- [ ] **Kidney function** (`BIOPRO_L`: `LBXSCR` creatinine, `LBXSBU` BUN, `LBXSUA` uric acid) —
      renal markers correlate with metabolic syndrome and diabetic nephropathy
- [ ] **Insulin** (`INS_L`, `LBXIN`) — paired with fasting glucose, enables a HOMA-IR insulin-
      resistance score, a clinically standard predictor the current model doesn't have access to
- [ ] **hs-CRP** (`HSCRP_L`, `LBXHSCRP`) — systemic inflammation marker; directly relevant to the
      NLR/PLR inflammation literature already cited (Mertoglu, Lorenzo) but not yet tested as a
      feature itself
- [ ] **Lipid panel** (`TCHOL_L` total cholesterol, `HDL_L` HDL, `TRIGLY_L` LDL + triglycerides) —
      classic metabolic-syndrome components, commonly included alongside CBC in comparable studies
- [ ] **Iron/anemia status** (`FERTIN_L` ferritin, `TFR_L` transferrin receptor, `FOLATE_L`/
      `FFMR_L`/`FOLFMS_L` folate) — directly relevant to the known HbA1c-anemia confound (English
      et al., already in the literature review) — useful both as candidate features and as a way
      to test whether the CBC→HbA1c signal is partly an anemia artifact
- [ ] **Smoking biomarker** (`COT_L`, serum cotinine) — smoking is an established diabetes risk
      factor and a more objective measure than self-report
- [ ] **Vitamin D** (`VID_L`) — some literature links low vitamin D to diabetes risk
- [ ] **Urine albumin-creatinine ratio** (`ALB_CR_L`) — likely more useful as a downstream
      complication/validity check than as a predictor (it reflects existing kidney damage), but
      worth considering for a "known-diabetes" sensitivity analysis

### Not yet downloaded — worth acquiring

- [ ] **Body Measures** (`BMX_L`, Examination component) — **BMI, waist circumference, weight,
      height.** This is the single biggest gap: the closest published precedent (Guo et al.,
      already cited) uses age, BMI, sex, NLR, and PLR as predictors, and BMI is missing entirely
      from the current feature set
- [ ] **Blood Pressure** (`BPXO_L`, Examination component) — hypertension correlates strongly with
      diabetes/metabolic syndrome risk
- [ ] **Smoking Questionnaire** (`SMQ_L`) — self-reported smoking status/pack-years, complementary
      to the cotinine biomarker above
- [ ] **Alcohol Use Questionnaire** (`ALQ_L`)
- [ ] **Physical Activity Questionnaire** (`PAQ_L`)
- [ ] **Medical Conditions Questionnaire** (`MCQ_L`) — includes family history of diabetes, a
      well-established risk factor not currently captured at all
- [ ] **Prescription Medications** (`RXQ_RX_L`) — identifies metformin/insulin/other diabetes
      medication use, useful for distinguishing treated-known-diabetic participants more precisely
      than the blunt `DIQ010` self-report currently used
- [ ] **Dietary recall** (Dietary component, e.g. `DR1TOT_L`) — higher effort to process, lower
      priority than the above, but a plausible confounder/predictor (sugar/carbohydrate intake)

### How to evaluate each addition

- [ ] For each new variable group, repeat the existing ablation pattern: fit CBC+demographics
      alone vs. CBC+demographics+[new variables], same split/settings, compare AUROC and the
      sensitivity/NPV threshold table — don't just add everything into one giant model at once
- [ ] Track coverage overlap with the current modeling cohort — several of these (`FERTIN_L`,
      `TFR_L`) are only eligible for a narrow age/sex subsample and would shrink `n` substantially
- [ ] Re-run the collinearity/VIF check (Phase 7) whenever new numeric features are added — e.g.
      lipids and liver enzymes may correlate with each other and with existing CBC indices

## Phase 10 — Modeling

- [x] Baseline logistic regression (demographics-only and CBC+demographics)
- [x] Baseline random forest (CBC+demographics), `class_weight="balanced"`
- [x] Single stratified train/test split, ROC curves, AUROC comparison
- [ ] Add a simple age-only baseline for comparison
- [ ] Add a matched demographics-only random forest (same split/settings) alongside the existing
      logistic-regression ablation
- [ ] Add gradient boosting
- [ ] Replace the single train/test split with stratified k-fold (or repeated stratified k-fold)
      cross-validation, with the full pipeline (impute → encode → scale → [PCA] → classifier)
      refit per fold
- [ ] Development-only threshold/model selection; reserve an untouched holdout (or nested CV) for
      final reporting — the current test set has already been inspected across models/thresholds

## Phase 11 — Evaluation

- [x] First-pass threshold table (sensitivity/specificity/NPV/PPV across thresholds)
- [ ] Report tests flagged, tests deferred, and positive labels missed together at every
      threshold — never NPV alone (a predict-all-negative rule already gets 89.3% NPV)
- [ ] Add calibration checks: reliability plot, proper scoring rule (Brier score vs. constant
      baseline is not sufficient on its own); fit any calibrator within development data only
- [ ] Add confidence intervals / design-aware uncertainty (plain bootstrap on a fixed split
      ignores NHANES clustering/stratification)
- [ ] Use held-out permutation importance instead of impurity-based importance if feature
      interpretation claims are made
- [ ] Subgroup/sensitivity analysis: compare HbA1c-based and fasting-glucose-based results to
      check sensitivity to HbA1c-related measurement effects (e.g. anemia)
- [ ] Add `savefig` calls in the notebooks so `code/assets/*.png` regenerate automatically instead
      of relying on manual export

## Phase 12 — Translate into a recommendation policy

- [ ] Define the decision policy itself (order / consider / skip) at a chosen high-sensitivity
      operating point, justified as a research objective, not an approved clinical safety standard
- [ ] Frame the cost-benefit explicitly as a hypothesis (NHANES has no cost or ordering-policy
      data) rather than an established economic claim
- [ ] State clearly that cross-sectional NHANES cannot validate the counterfactual harm of
      withholding a test

## Phase 13 — Literature review

- [x] 18 sources collected, 3 rounds of fact-checking completed, 15/18 verified against full text
- [ ] Resolve the 3 remaining sources (Veeranna, Engström, Bang) — full text blocked by
      Cloudflare/WAF; currently cited at abstract/title level only
- [ ] If any new feature groups from Phase 9 are added (lipids, insulin/HOMA-IR, inflammation,
      BMI), add matching literature coverage for each

## Phase 14 — Technical cleanup

- [ ] Add a dependency/environment file (Python 3.9.6, pandas 2.3.3, NumPy 2.0.2,
      scikit-learn 1.6.1, SciPy 1.13.1 were used successfully)
- [ ] Update stale statements in notebook 01 ("modeling packages not installed", "future notebook
      02") now that notebook 02 exists
