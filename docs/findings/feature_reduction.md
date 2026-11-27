# CBC feature reduction — Phase 15, Steps 1–2 (2026-11-23)

Exploratory, development-only selection pass on the fixed 4,612-adult, 106-positive primary
cohort. **Nothing here is locked** — `study_config.py`'s `CBC_FEATURES` is untouched. This
produces candidates and evidence for the team to review at Step 3, not a final decision.

## What drives the VIF, precisely

Two separate redundancy sources were tested independently, because conflating them gave a
misleading first read:

| Step | CBC block | n | Worst VIF (`LBXNEPCT`) | 2nd worst (`LBXLYPCT`) |
| --- | --- | --- | ---: | ---: |
| (baseline) full panel | all 21 | 21 | 25,983 | 22,006 |
| drop only the algebraically-redundant 7 (MCH, MCHC, 5 absolute counts) | `candidate_14` | 14 | 25,896 | 21,916 |
| **also** drop one differential percentage (basophil %) | `candidate_13` | 13 | **809** | **688** |

Dropping the algebraically-redundant columns alone (MCH/MCHC, implied by HGB/RBC/HCT; the 5
absolute differential counts, implied by WBC total × percentage) barely touches the two worst
VIF offenders — it does fix the **red-cell cluster** dramatically (`LBXHGB` 723→22, `LBXMCVSI`
657→56, `LBXHCT` 897→146), just not the differential percentages. The 5-part differential sums
to ~100% by construction, so any 4 of the 5 percentages determine the 5th — that compositional
constraint, not the algebraic one, is what inflates `LBXNEPCT`/`LBXLYPCT` into the tens of
thousands. Dropping exactly one percentage (basophil %, the rarest category — matching the
team's earlier 11-feature precedent) resolves it: VIF drops back to ~809/688, essentially the
same level as the pre-2026-11-23 11-feature block (~808/686).

**Takeaway: both fixes are needed together.** `candidate_13` (13 features) is the first
evidence-backed reduction candidate: drop MCH, MCHC, the 5 absolute differential counts, and
basophil %.

## L1 (Lasso) path: naive full-21 vs. the de-redundanced 13

A development-only L1 logistic-regression path (`C` from 0.001 to 10, 5-fold PSU-grouped,
survey-weighted AUROC, same splits as `research_extension.py`) was run twice — once on the raw
21-feature block, once on `candidate_13` — to see what a supervised method does with vs. without
the known redundancy already removed.

| | Best weighted AUROC | Features kept at best `C` | Knee-point AUROC (≥99% of best, most regularized) | Features kept at knee |
| --- | ---: | ---: | ---: | ---: |
| full 21 (naive) | 0.8091 | up to 21 | 0.8077 | 10 |
| `candidate_13` (de-redundanced first) | **0.8108** | up to 13 | 0.8096 | **8** |

De-redundancing first gives a **higher** best AUROC with **fewer** candidate features and a
cleaner selection path — evidence that the extra 8 dropped columns were adding collinear noise,
not signal, consistent with the VIF story above.

**Knee-point candidate set (8 features, `candidate_13` run):** `LBXRBCSI`, `LBXMCVSI`,
`LBXWBCSI`, `LBXPLTSI`, `LBXLYPCT`, `LBXMOPCT`, `LBXEOPCT`, `LBXMPSI` (kept in ≥3/5 outer folds).

**Dropped at the knee:** `LBXHGB`, `LBXHCT`, `LBXNEPCT`, `LBXRDW`, `LBXNRBC`.

## Stability check: is the 8-feature knee set robust, or a one-split artifact?

The single 5-fold knee selection above was re-run at the same `C` across 5 different PSU-grouped
fold seeds (25 folds total) to see which of the 8 "knee" features are *reliably* selected versus
which just happened to survive one particular split.

| Feature | Selection rate (of 25 folds) |
| --- | ---: |
| `LBXRBCSI`, `LBXMCVSI`, `LBXWBCSI`, `LBXLYPCT`, `LBXMOPCT` | 100% |
| `LBXPLTSI` | 88% |
| `LBXEOPCT` | 64% |
| `LBXRDW` | 44% |
| `LBXNRBC` | 40% |
| `LBXMPSI` | 36% |
| `LBXHGB` | 4% |
| `LBXHCT`, `LBXNEPCT` | 0% |

**`LBXMPSI` (MPV), which the single-split knee set kept, is actually unstable (36%)** — a clean
example of why the one-split result alone shouldn't be locked in. The genuinely stable core
(≥60% selection rate) is **7 features**: RBC, MCV, WBC, lymphocyte %, monocyte %, platelet count,
eosinophil %.

## Open question resolved: HGB/HCT face validity costs ~nothing

L1 consistently drops **hemoglobin and hematocrit** (statistically defensible — `HCT ≈ RBC ×
MCV / 10`, so once RBC and MCV are kept they add little new predictive information) — but they
are the most clinically standard CBC values, and the project's own anemia-sensitivity check in
`research_extension.py` is built on `LBXHGB`. A direct (unpenalized, same convention as the rest
of the pipeline) comparison answers whether adding them back costs anything:

| Feature set | # CBC features | Weighted AUROC (5-fold mean ± SD) |
| --- | ---: | ---: |
| 8-feature knee set | 8 | 0.8211 ± 0.0604 |
| knee set + HGB + HCT | 10 | 0.8210 ± 0.0605 |
| full `candidate_13` (all 13, no L1) | 13 | 0.8077 ± 0.0591 |

Adding HGB and HCT back costs essentially nothing (0.8211 → 0.8210, within noise) — so there is
no statistical reason not to keep them for clinical face validity. Notably, the full 13-feature
de-redundanced set *underperforms* the smaller sets here (unpenalized logistic regression still
struggles with the residual `LBXNEPCT` VIF of ~809), reinforcing that fewer, cleaner features is
the right direction, not a compromise.

## Recommended candidate for Step 3 review

**9 features:** `LBXRBCSI`, `LBXHGB`, `LBXHCT`, `LBXMCVSI`, `LBXWBCSI`, `LBXPLTSI`, `LBXLYPCT`,
`LBXMOPCT`, `LBXEOPCT` — the 7 stably-selected features plus HGB/HCT restored for face validity
at no measured AUROC cost. This drops 12 of the original 21: MCH, MCHC, all 5 absolute
differential counts, basophil %, **neutrophil %**, RDW, NRBC, and MPV.

The neutrophil % drop was initially flagged as a concern: it's one of only 3 of the 5
differential percentages kept, so unlike the algebraically-redundant 7 (MCH/MCHC/absolute
counts, each exactly implied by features already kept), the remaining 2 dropped percentages
(neutrophil %, basophil %) are **not** individually determined by the 3 that stayed — only their
*sum* is, via the ~100% compositional constraint. That meant the L1/knee selection could have
arbitrarily dropped a feature carrying real, distinct information just because it lost a
collinear tie-break against lymphocyte %, not because it was truly redundant.

## Direct validation: does any dropped feature matter even a little?

Per team instruction — these features are cheap to measure, so the bar for excluding one should
be "contributes nothing," not "didn't survive a parsimony penalty." Every one of the 12 CBC
features dropped from the 21-feature panel was tested directly: add it back to the 9-feature
base *alone*, via the same repeated (25-fold) PSU-grouped weighted-AUROC evaluation, and measure
the gain.

| Feature added back | AUROC gain | Gain ÷ its own SD |
| --- | ---: | ---: |
| `LBDMONO` (monocyte #) | +0.0003 | 0.006 |
| `LBDLYMNO` (lymphocyte #) | +0.0002 | 0.004 |
| `LBXNEPCT` (neutrophil %) | -0.0001 | -0.001 |
| `LBDNENO` (neutrophil #) | -0.0002 | -0.005 |
| `LBXMCHSI` (MCH) | -0.0003 | -0.007 |
| `LBXMC` (MCHC) | -0.0006 | -0.012 |
| `LBDEONO` (eosinophil #) | -0.0010 | -0.020 |
| `LBXRDW` (RDW) | -0.0016 | -0.033 |
| `LBXMPSI` (MPV) | -0.0018 | -0.036 |
| `LBXBAPCT` (basophil %) | -0.0019 | -0.037 |
| `LBDBANO` (basophil #) | -0.0020 | -0.039 |
| `LBXNRBC` (NRBC) | -0.0041 | -0.083 |

**None of the 12 dropped features show a real gain** — every gain is a tiny fraction (at most
8%) of its own fold-to-fold standard deviation, indistinguishable from noise, and most are
slightly negative. Critically, **neutrophil % itself gains essentially nothing (-0.0001,
gain/SD ratio -0.001)** when added back — the concern above was reasonable to raise, but the
direct test resolves it: for this linear logistic model, the 3 kept percentages (lymphocyte,
monocyte, eosinophil) already span nearly all the usable linear signal in the 5-part
differential for this outcome; the remaining compositional degree of freedom that distinguishes
neutrophil % from basophil % (given the other 3) carries no additional predictive value here.
This is an empirical finding about this specific outcome/model, not a logical necessity, but it
is now directly tested rather than inferred from VIF/L1 behavior alone.

**The 9-feature CBC candidate is confirmed to not be discarding any feature that matters, even a
little**, by direct test rather than by proxy (VIF, L1 path, or stability-selection alone, any of
which could in principle hide a real individual effect behind collinearity).

**Update (2026-11-23): locked.** This 9-feature candidate (plus dropping income from the
demographics) is now `study_config.py`'s default (`CBC_FEATURES`, `NUMERIC_DEMOGRAPHICS`) —
Phase 15 Step 3. The original 21-feature/income block is retained explicitly as `*_INITIAL`.
Step 4 (full official-pipeline re-run under the locked set) is also done — see
`docs/findings/phase2_feature_variant_comparison.md` and the refreshed `cbc_diagnostics.md`
(worst VIF now ~144, a >180x improvement on the 21-feature stage's ~26,000). The
neutrophil-%/HGB/HCT domain-vs-statistics concerns raised above are resolved by the direct test
rather than left open — HGB/HCT were restored (no cost to keeping them), and neutrophil % was
confirmed to genuinely add nothing (not just arbitrarily dropped).

## Full-model ablation: are all demographics worth keeping too?

Reduction so far only touched the CBC block — demographics (age, sex, race/ethnicity,
education, income) and BMI were held fixed as the established baseline. To do a genuine
*final* feature selection, each of those was tested for removal too, using the same
leave-one-block-out approach: fit the full model (demographics + BMI + the 9-feature reduced
CBC candidate), then refit with exactly one block removed, and compare weighted AUROC on the
same PSU-grouped folds. Repeated across 5 fold seeds (25 fit/evaluate pairs per block) after a
single-split run first suggested something worth double-checking.

| Block removed | Mean AUROC cost (repeated, 25 folds) | SD |
| --- | ---: | ---: |
| age | **0.0962** | 0.0063 |
| BMI | **0.0361** | 0.0037 |
| CBC (reduced 9) | **0.0227** | 0.0054 |
| race/ethnicity | **0.0171** | 0.0022 |
| sex | 0.0030 | 0.0021 |
| income | 0.0007 | 0.0038 |
| education | -0.0002 | 0.0014 |

Full model (all blocks): weighted AUROC 0.8364 ± 0.0103.

Age, BMI, the reduced CBC block, and race/ethnicity all show a clear, low-noise positive
contribution (cost well above its own SD) and should be kept without question. **Income and
education show essentially zero marginal AUROC contribution** — their cost estimates are smaller
than their own SD, i.e. indistinguishable from removing a useless feature. Sex is small but
likely genuine (cost roughly 1.5× its SD).

This mostly lines up with the project's existing [held-out permutation importance](permutation_importance.md)
(computed independently, different method, on the old 11-feature CBC block): there, age
(0.1525), BMI (0.0752) and race/ethnicity (0.0348) were also the top block scores, and income
(0.0016) was also the weakest. **One real disagreement: education scored a modest 0.0114 there,
not ~0 as here.** The two methods ask slightly different questions — permutation importance
measures how much a *trained* model's performance degrades when a feature's values are shuffled
(reliance on the fitted coefficient), while this ablation measures whether a model *refit without
the feature at all* loses anything (a correlated feature like income or CBC-derived health
status could compensate once education is gone). Both are legitimate, and the disagreement means
education's status is genuinely borderline, not that one method is wrong.

**Updated final-candidate recommendation:**

- **Drop:** income (near-zero/negative in both methods — the most convergent "safe to drop" case here).
- **Keep:** age, BMI, race/ethnicity, sex, the 9-feature reduced CBC block.
- **Team call:** education — ablation says ~0, permutation importance says modest-positive.
  Dropping it has no measured statistical downside here, but keeping it may still matter for
  non-AUROC reasons (e.g. a socioeconomic-disparity angle on the test-recommendation policy).
  Recommend keeping it unless the team has a specific reason to simplify further.

## Completeness check: income and education's "substitution" problem, and the real bottom line

Two things the analysis above didn't yet answer, checked directly:

**(1) Are income and education actually redundant with each other, not just individually
useless?** They're moderately correlated (Spearman ρ=0.50 — expected in survey data). If each
one's ~0 marginal cost is because the *other* one is substituting for it, dropping both at once
should cost more than the sum of dropping each alone. Tested directly (CBC held at the full 21
to isolate the demographic effect):

| Spec | Weighted AUROC | Cost vs. full (27-feature) baseline |
| --- | ---: | ---: |
| full baseline (27 features) | 0.8241 | — |
| drop income only | 0.8237 | 0.0004 |
| drop education only | 0.8238 | 0.0003 |
| **drop both income and education** | **0.8186** | **0.0055** |

Confirmed: dropping both costs ~8x more than the sum of dropping each alone (0.0055 vs.
0.0004+0.0003=0.0007). They partially substitute for each other — so while either one alone looks
safe to drop, **dropping both at once is not** the same as "dropping two useless features." At
least one of the two should stay if either is being removed.

**(2) The actual bottom line: how does the full proposed reduced model compare to the current
27-feature baseline, not just block-by-block costs?**

| Model | # features | Weighted AUROC (25-fold repeated) |
| --- | ---: | ---: |
| current full baseline (all demographics + BMI + 21 CBC) | 27 | 0.8241 ± 0.0510 |
| **proposed: age+BMI+sex+race+education + 9-feature CBC (drop income only)** | **14** | **0.8357 ± 0.0440** |
| age+BMI+sex+race + 9-feature CBC (drop income **and** education) | 13 | 0.8313 ± 0.0464 |

**The 14-feature reduced model (dropping only income) scores *higher* than the current
27-feature baseline** (+0.0116 AUROC) with roughly half the features — consistent with the
earlier CBC-only finding that the extra, redundant columns were adding noise, not signal, not
just "costing nothing." Given the substitution result above, **the recommendation is now: drop
income, keep education** — the 13-feature all-dropped version is still better than baseline but
measurably worse than keeping education (-0.0044).

## What this does *not* yet cover

- **Not yet tested against the independent 2017-2018 cycle.** Everything above is development-only,
  single-cohort (current cycle) exploration, same as Steps 1-2. Whether this reduced/14-feature
  model holds up on the frozen independent-cycle evaluation (the way `research_extension.py`
  already checks for the current 21-feature model) is Step 4 work, not done here.
- **This is a different question from fairness/equity.** Income (and, if dropped, education)
  showing ~0 *marginal predictive* value in this model does not mean income- or education-linked
  health disparities are irrelevant to the project — `docs/findings/permutation_importance.md`
  already makes the same point about sex/education scores. Dropping a demographic variable from
  the model is a modeling decision about this AUROC objective, not a claim about its real-world
  relevance to diabetes risk or to the project's equity framing.
- **Scope stayed inside the current model's features.** `docs/planning/PROJECT_PLAN.md` Phase 9
  lists several NHANES variables never brought into the model at all (lipids, insulin, hs-CRP,
  liver/kidney markers, smoking, blood pressure, family history, etc.). None of those were
  touched here — this was reduction of what's already in the model, not expansion. Worth
  confirming with the team whether "final feature selection" is meant to stay scoped to the
  current feature set, or should also screen some Phase 9 candidates before being called final.

## Reproduction

Run `python scripts/analysis/feature_reduction.py` from the repository root. Outputs:
`results/feature_reduction/reduction_vif.csv`, `lasso_path.csv` (both `full_21` and
`candidate_13` runs), `lasso_path.png`, `stability_check.csv` (25-fold repeated selection
frequencies), `hgb_hct_comparison.csv`, `all_feature_ablation.csv` (single-split),
`all_feature_ablation_repeated.csv` (25-fold repeated, demographics + BMI + CBC),
`final_candidates_comparison.csv` (bottom-line model comparisons), and
`reduction_summary.json`. See
[`docs/planning/PROJECT_PLAN.md`](../planning/PROJECT_PLAN.md) Phase 15 for the full reduction
plan this feeds into.
