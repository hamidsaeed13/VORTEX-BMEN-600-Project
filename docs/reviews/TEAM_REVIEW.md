# Team contribution review — 2026-11-16

[Ella](#ella-prs-13-and-14) · [Setayesh](#setayesh-pr-15) · [Shared decisions](#shared-decisions-before-integration) · [Proposed patches](#proposed-patches-and-validation)

[Open the standalone report with contributor tabs](TEAM_REVIEW.html).

Review of the actual PR source snapshots, with local reproduction against this repository's
NHANES files. **The reported principal counts and Ella's main AUROCs reproduced.**
This review identifies specific fixes and integration differences, rather than treating
all differences from our branch as mistakes. Nothing has been posted to GitHub or applied
to the contributors' branches.

## Ella — PRs 13 and 14

Reviewed snapshots: [PR 13 source](https://github.com/hamidsaeed13/VORTEX-BMEN-600-Project/tree/1336565f01623f9177cafd41e3b77b711b84d2ea)
and [PR 14 source](https://github.com/hamidsaeed13/VORTEX-BMEN-600-Project/tree/01d07d229287f2d0b3c61ebca9c040aa93c2b3c0).
Cell numbers below count all notebook cells from one.

| ID / priority | Location | Finding and evidence | Proposed fix |
|---|---|---|---|
| E1 — fix | PR 14, `code/04_feature_expansion.ipynb`, cell 7 | `na = data[~data["anemic"]]` retains **19 missing-HGB participants** because comparisons with NaN are false. The resulting 4,671-person group is not entirely observed as above the HGB cutoffs. | Require observed HGB before taking the complement. Corrected subgroup is **4,652**. Use an operational low-HGB label and regenerate its results. Included in the proposed patch. |
| E2 — fix | PR 14, cell 7 `rbc` / `no_rbc`; `docs/feature_expansion.md`, limitations | The “without red-cell features” model retains **`LBXNRBC`**, a nucleated-red-cell variable, while the write-up calls all retained features white-cell/platelet features. The code excludes seven other red-cell measures. | Add `LBXNRBC` to the removed block, or rename the experiment to specify exactly which red-cell indices were removed. Patch proposes removing it and rerunning. |
| E3 — correct wording | PR 13, `docs/survey_design.md`, “Analytic cohort”; PR 14, `docs/feature_expansion.md`, “Method” | “Not pregnant” overstates `RIDEXPRG != 1`. The 5,144-person cohort includes **21 indeterminate values and 4,151 missing values**; missing values include men and participants outside public reporting ages, not 4,151 pregnancy-risk cases. | Say “recorded pregnancy excluded; public pregnancy status is incomplete.” If adopting our stricter rule, require code 2 within the publicly reported female age band and rerun. Never describe unavailable status as confirmed nonpregnancy. |
| E4 — clarify cohort / decision | PR 13 cell 2 and PR 14 cell 1, `~DIQ010.isin([1, 7, 9])` | The cohort contains **215 borderline responses (code 3)** and 4,929 explicit “no” responses. The expression would also admit NaN, although **no missing DIQ010 responses were observed in the reproduced final cohort**. Inclusion of borderline responses can be a study choice. | If eligibility means explicit “no,” use `.eq(2)`. Otherwise label the cohort as including borderline responses and explicitly exclude missing values. Do not change the rule without documenting the scope decision. |
| E5 — revise inference | PR 14, `docs/feature_expansion.md`, “Interpretation” | “Not explained by anemia,” “clear value,” and comparing changes to fold SD are stronger than this analysis supports. Fold SD is not an interval for the paired model difference. Removing low-HGB records does not rule out all red-cell effects on HbA1c. | Use the replacement wording below. Report matched out-of-fold differences with suitable design-aware/refitting uncertainty before making superiority claims. |
| E6 — reproducibility | PR 14, cell 8 | The summary is manually populated with AUROCs, SDs and subgroup sizes. **The original values reproduced**, but the summary will become stale when E1/E2 change the experiment. | Build it from current frames and computed scores. Patch removes the typed-in result table and clears saved outputs. |
| E7 — integration safeguard | PR 13 cell 1; PR 14 cells 1, 3–6 | First-match recursive loading and unvalidated joins can select a different duplicate file or multiply rows. The BMI download also runs unconditionally. No duplication was demonstrated in the reproduced cohort. | Resolve explicit cycle-specific paths; fail on missing/ambiguous inputs; check unique SEQN and use `validate="one_to_one"`. Cache and hash downloads. Patch only prevents unconditional redownload; full loader harmonization remains open. |

Suggested correction for E1:

```python
observed_hgb = data["LBXHGB"].notna()
na = data.loc[observed_hgb & ~data["anemic"]].copy()
```

Suggested replacement interpretation for PR 14:

> In the exploratory unweighted cross-validation, CBC increased mean AUROC beyond age
> and sex. The observed gain persisted in a sensitivity analysis excluding participants
> below operational hemoglobin cutoffs; this does not establish that anemia or other
> red-cell effects are absent. The red-cell ablation must be rerun after clarifying its
> feature block. BMI/waist, hs-CRP and iron-marker additions produced small observed
> differences, whose paired uncertainty has not yet been estimated. These findings do
> not establish clinical utility or population-level performance.

Additional wording: glucose is a direct glycemic measurement; insulin is a related
biomarker, not literally the HbA1c outcome. Explain exclusions in terms of the intended
available tests and information leakage, rather than calling both the outcome itself.

What is already useful: correct phlebotomy-weight identification, transparent exploratory
unweighted reporting, fold-fitted imputation/scaling, matched comparisons within the
iron subgroup, and explicit reporting of limited iron-marker coverage.

## Setayesh — PR 15

Reviewed [source snapshot](https://github.com/hamidsaeed13/VORTEX-BMEN-600-Project/tree/8500a82a12ebe95a6f6a50b3ed422b3bba3323ac),
`code/02_baseline_model_and_figures.ipynb`.

| ID / priority | Location | Finding and evidence | Proposed fix |
|---|---|---|---|
| S1 — validation weakness | Cell 4, `allowed_codes` loop | Casting to integer **before** validation can accept invalid fractional codes: 1.5 becomes 1 and passes `{1, 2}`. No such invalid values were found in this dataset. | Compare the original nonmissing numeric values directly with allowed codes. Patch removes `.astype(int)`. |
| S2 — integration fix | Cell 2, `DATA_DIR` | `../data/raw` assumes the old directory layout and notebook working directory. Inputs now live under `data/raw/2021_2023`. | Resolve repository root and the cycle-specific directory, with an explicit legacy fallback. Included in patch; tested from repository root. |
| S3 — inherited safeguard gap | Cells 2 and 4 | Blanket warning suppression remains in the notebook, and SAS tiny-positive representations of zero are not normalized. The blanket suppression was already in the baseline; it is **not newly attributed to Setayesh**. Her current eligibility does not filter weights, so this did not cause the reproduced cohort count. | Restore visible warnings; normalize SAS near-zero values immediately after loading, before future weight-based filtering. Both are proposed in the patch. |
| S4 — scope decision | Cells 6–8 | Her cohort includes **212 borderline diagnosis responses**, **37 recorded pregnancies**, and **85 reported diabetes-medication users**. These categories can overlap. Her notebook explicitly allows borderline responses and incomplete CBC; it does not claim pregnancy/medication exclusions. | Document these choices and agree the primary cohort before replacing our analysis. For an explicit-no-diagnosis screening cohort, use the agreed diagnosis, medication, pregnancy and CBC-completeness rules together. Do not simply replace 4,930 with 4,612 in text. |
| S5 — interpretation boundary | Cells 14, 16–17 | The class-balanced model's scores and descriptive threshold table are not calibrated population risks or evidence of safe test deferral. This is an acknowledged preliminary baseline, not a demonstrated coding failure. | Retain the exploratory label. Use development-only calibration/threshold selection and report held-out weighted missed/deferred counts before discussing a recommendation policy. |
| S6 — reporting improvement | Cell 20 | Impurity-based forest importance can favor correlated/continuous features; it does not establish independent biomedical contribution. | Treat as descriptive, or replace interpretation claims with held-out permutation importance and uncertainty, preferably including correlated-feature blocks. Importance cell not rerun in this review. |

Minimal fix for S1:

```python
observed = set(df[column].dropna().unique())
assert observed.issubset(allowed)
```

What is already useful: source record-count and SEQN checks, one-to-one joins, categorical
sentinel handling, interview/examination flow, structural missingness discussion, fold-safe
pipeline construction, a matched age/sex-only forest, and explicit flagged/missed counts.
The matched forest task is therefore implemented in this pending contribution, even though
its population and predictor baseline differ from our extension's models.

## Shared decisions before integration

| Question | Current branch | Ella | Setayesh | Action |
|---|---|---|---|---|
| Age | 20+ | 18+ | 20+ | Agree primary population; keep other ages as labelled sensitivity analyses |
| HbA1c endpoint | ≥6.5% | ≥5.7% primary proposal | ≥6.5% | Different scientific questions; event count alone cannot choose the question |
| Diagnosis | Explicit code 2 | Codes 2/3 in observed cohort | Codes 2/3 | Agree handling of borderline responses |
| Pregnancy / medications | Explicit restrictions, with public-data limitations | Recorded pregnancy excluded; no medication restriction | No such restrictions | Reconcile eligibility and qualify pregnancy claims |
| CBC block | Eligibility: complete 12; extension prediction: 11 after basophil drop | 21 predictors | 15 predictors, incomplete allowed | Document exact block and missingness; these are not interchangeable ablations |
| Demographic baseline | Age, sex, race, education, income; BMI extension | Age/sex | Age/sex | Attribute CBC gains to the actual comparator |
| Evaluation | Weighted nested PSU-grouped procedures | Unweighted row-stratified CV | Unweighted single split | Preserve exploratory results; use common design-aware evaluation for final comparisons |

Ella's ordinary CV is explicitly exploratory; lack of a separate holdout is not by itself
data leakage. Preprocessing is inside her pipeline. For our final NHANES comparisons,
coordinate matched PSU-grouped folds and weights. Neither her fold SD nor Setayesh's
single split substitutes for design-aware uncertainty.

Do not select a new HbA1c cutoff merely to increase the event count. Team agreement on
the question comes first; follow with reconciled cohort-flow counts, matched model
comparisons and regenerated tables. Our 4,612-person cohort is itself still a team proposal.

## Proposed patches and validation

- [PR 14 proposed patch](proposed_fixes/pr14_proposed.patch): observed-HGB restriction,
  remove NRBC from the red-cell ablation, compute the summary dynamically, avoid an
  unconditional BMI redownload, clear old code outputs.
- [PR 15 proposed patch](proposed_fixes/pr15_proposed.patch): resolve paths, normalize
  SAS zeros, validate original category values, restore warnings, document cohort mismatch,
  clear old code outputs.
- [Machine-readable evidence](../verification/teammate_review_evidence.json): reviewed
  heads, source/patch hashes, reproduced cohort composition and proposed-fix checks.

Patches target the contributors' original `code/` paths and reviewed snapshots. They are
**proposals, not applied changes**; inspect them on those branch versions before applying.
If notebooks move into `notebooks/`, map paths during integration. Patches clear saved
outputs deliberately: rerun and regenerate the associated Markdown reports before merging.
No claim is made that these limited patches resolve every review item.

The cohort checks reproduced Ella's 5,144/1,552 (≥5.7%) and 152 (≥6.5%) counts and
Setayesh's 4,930/152 counts. Ella's original age/sex, CBC and BMI AUROCs reproduced
to the three decimals reported. Proposed notebook cells were compiled and schema-checked;
the sensitivity/model/threshold execution results and limits are recorded in the evidence
JSON. The network download, full plot rerendering and PR 15 importance cell were not rerun.
The local NumPy/BLAS environment emits floating-point matmul warnings; they are recorded,
not treated as evidence that a contributor's code is wrong. Check convergence and finite
predictions separately.

The corrected observed-HGB subgroup has 4,652 participants: age/sex AUROC 0.704,
CBC AUROC 0.779. Removing NRBC leaves the ablation AUROC at 0.730 to three decimals.
Proposed PR 15 fixes preserve all four reported AUROCs (0.673, 0.772, 0.574, 0.747)
to three decimals and pass threshold-count accounting. No convergence warnings were
recorded in either proposed notebook execution. These are reproduction checks, not
independent scientific approval.

This review supports the course rubric's requirements for justified inclusion criteria,
reproducible methods, meaningful comparisons, uncertainty, limitations and verified AI work.
