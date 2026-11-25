# Phase 9: biomarker expansion beyond CBC (exploratory, 2026-11-23)

Tests whether liver, kidney, inflammation, lipid and insulin-resistance biomarkers — already
downloaded in `data/raw/2021_2023/laboratory/`, never used in this project until now — add
value beyond the locked demographics + BMI + 9-feature CBC baseline. **This does not change
`study_config.py`'s locked feature set** — it's a separate research question (what's the best
predictor achievable with all available NHANES data) from Phase 15's (how much can CBC alone be
trimmed). No hyperparameter/threshold selection was done from these results.

## Coverage

| Group | Weight | n with complete group (of 4,612) |
| --- | --- | ---: |
| Liver (ALT, AST, GGT, ALP) | WTPH2YR (same as primary cohort) | 4,351 |
| Kidney (creatinine, BUN, uric acid) | WTPH2YR | 4,363 |
| Inflammation (hs-CRP) | WTPH2YR | 4,481 |
| Lipids, non-fasting (total cholesterol, HDL) | WTPH2YR | 4,408 |
| Lipids, fasting (triglycerides, Friedewald LDL) | WTSAF2YR (fasting subsample) | 2,434 |
| Insulin | WTSAF2YR | 2,450 |
| HOMA-IR (derived) | WTSAF2YR | 2,436 |

Four of seven groups use the same `WTPH2YR` weight as the primary cohort, so they're tested on
essentially the full 4,612 (minus item-level missingness) — no subsample restriction. Insulin,
triglycerides/LDL and HOMA-IR require the fasting subsample, the same restriction already
applied to fasting glucose elsewhere in this pipeline (`research_extension.py`'s
`fasting_hba1c`/`fasting_glucose` scenarios).

## Results

Each group is tested against its own matched baseline (same subsample, same folds) — gains are
**not directly comparable across groups** since sample sizes differ.

| Group | n | Positives | Baseline AUROC | Baseline+group AUROC | Gain |
| --- | ---: | ---: | ---: | ---: | ---: |
| HOMA-IR | 2,265 | 60 | 0.819 | 0.901 | **+0.082** |
| Lipids (fasting) | 2,263 | 57 | 0.799 | 0.829 | +0.030 |
| Insulin | 2,265 | 60 | 0.819 | 0.845 | +0.026 |
| Liver | 4,351 | 104 | 0.837 | 0.859 | +0.022 |
| Lipids (non-fasting) | 4,408 | 104 | 0.819 | 0.833 | +0.014 |
| Kidney | 4,363 | 104 | 0.836 | 0.846 | +0.010 |
| Inflammation (hs-CRP) | 4,481 | 105 | 0.823 | 0.824 | +0.002 |

## Critical caveat: HOMA-IR and insulin are not "opportunistic" predictors the way CBC is

**HOMA-IR's gain should not be read as evidence it's a good additional screening test.** It's
computed as `fasting glucose × insulin / 405` — the formula directly embeds fasting glucose,
which is mechanistically and near-definitionally linked to HbA1c (both reflect the same
glycemic status; HbA1c is literally a time-averaged measure of blood glucose). This is close to
predicting a glucose-defined outcome from glucose itself, not discovering new information from
an unrelated test drawn for other reasons — the opposite of this project's actual research
question (does a test ordered for unrelated reasons, like CBC, opportunistically predict
diabetes-range HbA1c). The same logic applies, more weakly, to insulin alone: insulin resistance
is a direct causal driver of elevated glucose/HbA1c, not an incidental correlate the way most
CBC components are. **Neither should be treated as validating a "measure HOMA-IR/insulin
instead of HbA1c" screening strategy** — that would require a test that's cheaper or more often
already drawn than HbA1c itself, which fasting insulin is not (it requires its own fasting blood
draw, same burden as the HbA1c/glucose tests it would be replacing).

**Liver enzymes, lipids and kidney markers are more defensible as genuinely opportunistic
screening candidates**, same framing as CBC: they're often drawn for unrelated reasons (general
metabolic panels), don't mechanistically embed the outcome, and show real (if more modest)
biologically plausible gains — liver enzymes via the established NAFLD/insulin-resistance link
already cited in this project's literature review, lipids via the metabolic-syndrome
association. Inflammation (hs-CRP) shows essentially no incremental value here.

## Status

Exploratory screen only. No feature-coverage/VIF recheck, no survey-weighted calibration, no
independent-cycle validation, and no combination of multiple new groups together has been done
— each group was tested in isolation against the baseline. If the team wants to pursue this
further, liver enzymes and the lipid panel are the most defensible next candidates to formally
add to the model (matching this project's "opportunistic test" framing); HOMA-IR/insulin would
need a much more careful circularity discussion before being treated as a predictive-value
finding rather than a methodological artifact.

## Reproduction

Run `python scripts/analysis/biomarker_expansion.py` from the repository root. Outputs:
`results/biomarker_expansion/biomarker_coverage.csv`, `biomarker_ablation_summary.csv`,
`biomarker_ablation_gains.png`, per-group prediction/summary CSVs, and
`biomarker_expansion_metadata.json`.
