# Project Plan — Lab Test Recommendation System

Start-to-end research/technical plan for predicting diabetes-range HbA1c from CBC + demographics.
Course logistics (assignments, grading, submission, peer evaluation, presentations) are
intentionally excluded — this tracks the research project itself.

Checkboxes were reconciled against this checkout on 2026-11-16; see [evidence and teammate contributions](CHECKLIST_AUDIT.md). Completion refers to implementation here, not team approval or merge into main.

Checkboxes reflect status as of this writing. `[x]` = done, `[~]` = in progress / partially done,
`[ ]` = not started. Re-check this list as work lands rather than trusting it blindly — it's a
snapshot.

**Extension progress (2026-11-02):** Notebooks 05–06 implement matched BMI/block comparisons,
low-hemoglobin and fasting-endpoint sensitivity, full-refit survey resampling and frozen-model
independent-cycle evaluation. See [results](../findings/research_extension_results.md) and
[publication readiness](../findings/publication_readiness.md). These are research findings,
including negative results; original tasks and team decisions below remain for review.

---

## Phase 1 — Data acquisition & merging

- [x] Identify and download NHANES 2021–2023 cycle files: `DEMO_L`, `CBC_L`, `GLU_L`, `GHB_L`,
      `DIQ_L` (`data/raw/`)
- [x] Merge all five on `SEQN` (`notebooks/01_eda_cbc_glucose_demographics.ipynb`)
- [ ] Record the real dataset access/download date
- [x] Fix `pd.read_sas` SAS-zero bug (zeros read as ~5.4e-79) — use `pyreadstat` or explicitly
      snap near-zero values before any weight-based filtering

## Phase 2 — Exploratory data analysis

- [x] Coverage analysis: how much usable data under each candidate label (fasting glucose vs.
      HbA1c vs. self-report)
- [x] Demographic distributions, CBC predictor distributions, glycemic outcome distributions
- [x] Exploratory comparison of the three candidate label definitions
- [x] CBC vs. glycemic-status first look (boxplots, group means/medians)
- [x] Missingness summary

## Phase 3 — Cohort / eligibility definition (blocking item)

**Progress:** Notebook 03 implements a recommended adults-20+ cohort and recomputes counts;
team population/endpoint decisions remain open. See [cohort analysis](../findings/cohort_definition_analysis.md).

- [ ] Decide and document the intended population: age range (12+? adults only?), known-diagnosis
      policy (include/exclude/stratify), pregnancy exclusion
- [x] Apply `WTSAF2YR > 0` eligibility filter for fasting-glucose analysis
      (`research_extension.py`; matched fasting-endpoint results)
- [x] Recompute cohort counts, class balance, and the "78.8% already diagnosed" caveat once
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
- [~] Missing-data strategy is implemented (observed outcome/complete CBC eligibility; fold-specific imputation for remaining predictors). Reconcile documentation and selection assumptions with PR 15.
- [~] Add merge-validation assertions: unique `SEQN`, one-to-one joins, unchanged merged row
      count and primary cohort/event counts are checked; complete source/category auditing
      remains to reconcile with PR 15

## Phase 5 — Missing data handling

**Progress:** Notebooks 03–04 refit imputers inside each training fold.

- [x] Baseline: median-impute numeric CBC/age/income; most-frequent-impute categorical
      demographics
- [x] Move imputers inside the `ColumnTransformer`/pipeline so they refit per CV fold (not fit
      once on the full sample)
- [~] Numeric missingness indicators, including income, are implemented in the extension.
      Education is mode-imputed (two missing values in the adult cohort); no separate
      education indicator. Adult eligibility removes the under-20 structural category.

## Phase 6 — Encoding categorical variables

**Progress (updated 2026-11-23):** The canonical encoding — one-hot for sex/race-ethnicity
(nominal), ordinal for education (`DMDEDUC2` has a natural order) — is now centralized in
`scripts/analysis/study_config.py` (`categorical_transformer_entries()`) and used by every
official script (`cohort_analysis.py`, `weighted_calibration_analysis.py`,
`research_extension.py`) and notebooks 03–04. Notebook 02 still uses its own, separate
exploratory encoding (one-hot sex only; it doesn't model race/education/income at all) as a
historical baseline, not the final pipeline. Ordinal vs. one-hot education gave no measurable
AUROC difference in the original Phase 6 exploration (`notebooks/Phase 6.ipynb`); ordinal was
adopted since it adds one feature instead of several sparse indicator columns.

- [x] `sex` (`RIAGENDR`): one-hot encode inside folds; retain all levels with penalized logistic regression rather than require a dropped binary level
- [x] `race_eth` (`RIDRETH3`): `OneHotEncoder(handle_unknown="ignore")` — nominal, nothing ordinal
      about it
- [x] `education` (`DMDEDUC2`): ordinal-encode via `study_config.py` (team decision) to allow a
      natural-order effect with one feature instead of several sparse indicator columns.
- [x] Fit every encoder inside the training fold only, with `handle_unknown="ignore"` so an unseen
      category in held-out data doesn't break the pipeline

## Phase 7 — Collinearity check / PCA (diagnostic, not a replacement for raw features)

**2026-11-16, updated 2026-11-23:** Implemented in [cbc_diagnostics.py](../../scripts/analysis/cbc_diagnostics.py), with [findings](../findings/cbc_diagnostics.md), VIF/correlation tables, descriptive scree/PC1–PC2 figure, and a matched nested 95%-variance PCA comparison. All preprocessing is fitted inside each training fold. The CBC block now keeps all 21 variables (team decision 2026-11-23; see Phase 15), including basophil percentage, MCH, MCHC, MPV, NRBC and the five absolute differential counts, superseding the earlier 11-feature block this section originally described. VIF is now severe (up to ~26,000 for `LBXNEPCT`) versus ~808 under the legacy 11-feature block — driven by the differential percentages summing to ~100% plus the new near-exact identity `absolute count ≈ WBC total × percentage`. The raw-vs-PCA matched comparison still shows no meaningful AUROC difference (0.8107 vs 0.8141), reinforcing that PCA is a robustness check here, not a selection mechanism — see Phase 15 for the actual reduction plan.

- [x] Compute correlation matrix + VIF on the numeric CBC block before deciding anything further
      (already have a correlation heatmap; extend to VIF)
- [x] Address the WBC 5-part differential being compositional data (`lymph_pct + neut_pct +
      mono_pct + eos_pct + baso_pct ≈ 100%`) — drop one category or use a log-ratio transform
      before PCA/linear models
- [x] Note the algebraic relationships among `hemoglobin`/`hematocrit`/`mcv`/`mch`/`mchc`
- [x] Run PCA (after scaling, after resolving the compositional issue) as:
  - [x] a 2D/3D PC1-vs-PC2 scatter colored by HbA1c status
  - [x] an optional secondary model arm (compressed CBC representation vs. raw features) as a
        robustness check — not the primary/headline model, to preserve interpretability for the
        eventual order/skip policy
  - [x] choose `n_components` via scree-plot elbow or ~90–95% explained variance; fit only inside
        the training fold of each CV split

## Phase 8 — Survey design (NHANES-specific)

**Progress:** Notebook 04 uses WTPH2YR in classifiers, calibration and evaluation, with
SDMVSTRA/SDMVPSU for grouped validation and conditional variance estimates. Fasting-glucose
eligibility and weighting are implemented in notebook 05. See [weighted analysis](../findings/weighted_calibration_analysis.md).

**Resolved (2026-11-20 team meeting):** the primary-outcome/cohort disagreement tracked in
[checklist audit](CHECKLIST_AUDIT.md) and [team review](../reviews/TEAM_REVIEW.md) across PRs
13-15 is settled. HbA1c >= 6.5% is the primary outcome, on an examined-adults-20+ cohort with
an explicit "no" prior-diabetes diagnosis (borderline excluded), no insulin/diabetic-pill use,
and pregnancy-clear status. These values now live in one place,
`scripts/analysis/study_config.py`, which `research_extension.py`, `cohort_analysis.py`,
`weighted_calibration_analysis.py`, `02_baseline_model_and_figures.ipynb` and
`03_survey_design.ipynb` all read from, instead of each redefining its own copy. See
[survey design decisions](../survey_design.md) for the resulting cohort (4,636/106 in notebook
03; 4,619/106 in notebook 02; 4,612/106 in the official pipeline -- the small remaining gaps are
a separate, still-open complete-CBC-panel modeling choice, not a disagreement over eligibility).

- [x] Apply `WTPH2YR` for CBC/HbA1c analyses, `WTSAF2YR` (with eligibility) for fasting glucose
- [x] Preserve `SDMVSTRA`/`SDMVPSU` for design-aware uncertainty
- [x] State explicitly whether reported performance targets the analytic sample or a
      population-level estimate; keep class-balancing weights conceptually separate from survey
      weights

## Phase 9 — Explore other relevant factors (feature expansion)

The original baseline only used the CBC panel + 5 demographic variables (`age_years`, `sex`,
`race_eth`, `education`, `income_pir`). Several other NHANES-measured factors are plausible
predictors of diabetes-range HbA1c and are either already sitting unused in this repo or are a
cheap additional download. Each one needs its own task: pull the variable(s), check coverage/
eligibility overlap with the existing modeling cohort, and test whether it adds incremental value
over the current CBC+demographics model (same ablation approach already used for CBC vs.
demographics-only).

### Already downloaded in `data/raw/2021_2023/laboratory/`, not yet used

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

- [x] **Body Measures** (`BMX_L`, Examination component) — **BMI, waist circumference, weight,
      height.** This is the single biggest gap: the closest published precedent (Guo et al.,
      already cited) uses age, BMI, sex, NLR, and PLR as predictors, and BMI is now included in the matched extension models
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

- [~] BMI and CBC blocks are evaluated on matched participants/folds. For each further new variable group, repeat the existing ablation pattern: fit CBC+demographics
      alone vs. CBC+demographics+[new variables], same split/settings, compare AUROC and the
      sensitivity/NPV threshold table — don't just add everything into one giant model at once
- [ ] Track coverage overlap with the current modeling cohort — several of these (`FERTIN_L`,
      `TFR_L`) are only eligible for a narrow age/sex subsample and would shrink `n` substantially
- [ ] Re-run the collinearity/VIF check (Phase 7) whenever new numeric features are added — e.g.
      lipids and liver enzymes may correlate with each other and with existing CBC indices

## Phase 10 — Modeling

**Progress:** Age-only comparisons are in notebooks 02–04. Notebook 04 adds nested
cluster-grouped validation with development-only calibration/threshold selection; further
model comparisons remain open; notebook 06 adds frozen older-cycle evaluation.

- [x] Baseline logistic regression (demographics-only and CBC+demographics)
- [x] Baseline random forest (CBC+demographics), `class_weight="balanced"`
- [x] Single stratified train/test split, ROC curves, AUROC comparison (historical baseline; nested validation supersedes it)
- [x] Add a simple age-only baseline for comparison
- [ ] Add a matched demographics-only random forest (same split/settings) alongside the existing
      logistic-regression ablation
- [ ] Add gradient boosting
- [x] Replace the single train/test split with stratified k-fold (or repeated stratified k-fold)
      cross-validation, with the full pipeline (impute → encode → scale → [PCA] → classifier)
      refit per fold
- [x] Development-only threshold/model selection; reserve an untouched holdout (or nested CV) for
      final reporting — the current test set has already been inspected across models/thresholds

## Phase 11 — Evaluation

**Progress:** Notebooks 02–04 report deferred/flagged/missed counts. Notebook 04 adds weighted
calibration diagnostics and conditional design intervals, which exclude training variability;
notebooks 05–06 add 100 full refits and matched HbA1c/fasting-glucose sensitivity.

- [x] First-pass threshold table (sensitivity/specificity/NPV/PPV across thresholds)
- [x] Report tests flagged, tests deferred, and positive labels missed together at every
      threshold — never NPV alone (a predict-all-negative rule already gets 89.3% NPV)
- [x] Add calibration checks: reliability plot, proper scoring rule (Brier score vs. constant
      baseline is not sufficient on its own); fit any calibrator within development data only
- [x] Add confidence intervals / design-aware uncertainty (plain bootstrap on a fixed split
      ignores NHANES clustering/stratification)
- [x] Use held-out permutation importance instead of impurity-based importance for predictor
      interpretation: [analysis and limitations](../findings/permutation_importance.md).
      Two existing models, nine blocks, 20 within-PSU permutations; frozen development-only
      preprocessing/calibration and weighted evaluation. Permutation SD is not a confidence interval.
- [x] Subgroup/sensitivity analysis: compare HbA1c-based and fasting-glucose-based results to
      check sensitivity to HbA1c-related measurement effects (e.g. anemia)
- [ ] Add `savefig` calls in the notebooks so `results/baseline/*.png` regenerate automatically instead
      of relying on manual export

## Phase 12 — Translate into a recommendation policy

- [~] Development-only 95%-sensitivity thresholds and exploratory policy counts are implemented; team justification remains open. Define the decision policy itself (order / consider / skip) at a chosen high-sensitivity
      operating point, justified as a research objective, not an approved clinical safety standard
- [x] Frame the cost-benefit explicitly as a hypothesis (NHANES has no cost or ordering-policy
      data) rather than an established economic claim
- [x] State clearly that cross-sectional NHANES cannot validate the counterfactual harm of
      withholding a test

## Phase 13 — Literature review

- [x] 18 sources collected, 3 rounds of fact-checking completed, 15/18 verified against full text
- [ ] Resolve the 3 remaining sources (Veeranna, Engström, Bang) — full text blocked by
      Cloudflare/WAF; currently cited at abstract/title level only
- [~] BMI and red-cell literature are covered in the extension evidence matrix. If further new feature groups from Phase 9 are added (lipids, insulin/HOMA-IR, inflammation,
      BMI), add matching literature coverage for each

## Phase 14 — Technical cleanup

- [x] Add a dependency/environment file (Python 3.9.6, pandas 2.3.3, NumPy 2.0.2,
      scikit-learn 1.6.1, SciPy 1.13.1 were used successfully)
- [ ] Update stale statements in notebook 01 ("modeling packages not installed", "future notebook
      02") now that notebook 02 exists

## Phase 15 — CBC feature reduction (blocking item before final model comparison)

**Status (2026-11-23):** Not started. The team decided (cohort-summary table, same meeting as
the 21-feature CBC decision) that feature reduction happens as its own dedicated stage, not
folded into the current 21-feature baseline. This phase exists to track that work explicitly so
it isn't lost. Trigger/evidence: Phase 7's VIF check on the full 21-feature block found VIF up to
~25,983 (`LBXNEPCT`) and ~22,006 (`LBXLYPCT`) — roughly 30x worse than the legacy 11-feature
block's worst case (~808) — driven by (a) the 5-part differential summing to ~100% and (b) the
five absolute differential counts (`LBDLYMNO`, `LBDNENO`, `LBDMONO`, `LBDEONO`, `LBDBANO`) each
being near-exactly `WBC total × percentage / 100` (correlation 0.78–0.9998 depending on cell
type). MCH (`LBXMCHSI`) and MCHC (`LBXMC`) are also algebraically close to functions of
hemoglobin/RBC/hematocrit already in the model. PCA was evaluated as a possible shortcut and
rejected: the matched raw-vs-95%-PCA comparison in `cbc_diagnostics.py` shows no AUROC
difference (0.8107 vs 0.8141), so compressing to components buys nothing and would also make
the resulting panel non-actionable (a lab can't "order less of" a PCA component). Reduction
needs a supervised, name-preserving method instead.

- [ ] **Step 1 — drop the algebraically-redundant columns first**, as a documented default pass,
      before any data-driven selection: MCH, MCHC (implied by HGB/RBC/HCT already kept) and the
      five absolute differential counts (implied by WBC × percentage already kept). Re-run VIF
      (`cbc_diagnostics.py`) on the resulting ~14-feature set to confirm this brings VIF back down
      toward the legacy-block range.
- [ ] **Step 2 — supervised selection on what's left.** Run an L1 (Lasso) logistic-regression
      regularization path (nested CV, development data only, matching the existing
      `weighted_calibration_analysis.py`/`research_extension.py` fold structure) to see which CBC
      coefficients survive at an AUROC-preserving penalty. Cross-check against the existing
      held-out permutation-importance results (`docs/findings/permutation_importance.md`) and VIF
      — a feature that's both low-importance and high-VIF is a strong drop candidate; a
      low-VIF/low-importance feature is a weaker one (drop for parsimony, not collinearity).
- [ ] **Step 3 — team decision and lock the reduced set.** Document the resulting feature list as
      a new canonical block in `study_config.py` (same pattern as `CBC_FEATURES`), with the
      rationale (which columns were dropped and why), the same way the 11→21 and 21→reduced
      decisions are now tracked here.
- [ ] **Step 4 — head-to-head model comparison on the locked set.** Re-run the full pipeline
      (`cohort_analysis.py`, `weighted_calibration_analysis.py`, `research_extension.py` and their
      notebooks) with the reduced block, producing one comparison table across: age-only,
      demographics, demographics+BMI, demographics+BMI+full-21-CBC (current baseline),
      demographics+BMI+reduced-CBC — same folds/weights/calibration throughout so the comparison
      is apples-to-apples. This directly answers whether reduction recovers some of the AUROC gain
      lost to collinearity noise between the 11- and 21-feature stages (0.023→0.010 CBC-over-BMI
      gain; see `docs/findings/research_extension_results.md`).
- [ ] **Step 5 — expand the model comparison itself**, now that the feature set is settled: add
      gradient boosting (already an open Phase 10 item) alongside the existing logistic/forest
      pair, using the same matched folds/weights/calibration so it's comparable, not a new
      one-off evaluation.
- [ ] **Step 6 — final locked evaluation.** Once a model + feature set is chosen from Step 4/5,
      reserve a genuinely untouched holdout (or confirm the nested-CV design already satisfies
      this) for the final reported numbers — the folds used during Steps 1–5 have already been
      inspected across many specs and cannot be relabelled an untouched test set.

**2026-11-16 reconciliation:** Phase 4 cleaning is also addressed in Setayesh PR 15; Phase 8 and selected Phase 9 blocks in Ella PRs 13–14. Those branches use different eligibility/outcomes and are pending integration, so their tasks are not automatically marked complete here. See CHECKLIST_AUDIT.md. Phase 12 has an exploratory threshold procedure, but team justification and a final policy remain open. Phase 9 is a candidate menu, not a requirement to add every measured biomarker.
