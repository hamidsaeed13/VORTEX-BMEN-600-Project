# Phase 15 Step 6: final locked holdout evaluation (2026-11-23) — SPENT

**This holdout has been used and should not be reused for further model selection.** Every
other number in this project comes from nested cross-validation over the same 4,612
participants, inspected across dozens of specs (11→21→9 CBC features, 6+ model families, 2
class-balancing schemes) — technically no longer an untouched test of generalization. This
evaluation reserves a single, fresh PSU-grouped development/holdout split, using a random seed
(`99912601`) that appears nowhere else in this codebase, and evaluates the three models the
team has actually been comparing exactly once.

## Setup

- **Development**: 3,407 participants, 77 positive labels (~74% of the primary cohort).
- **Holdout**: 1,205 participants, 29 positive labels (~26%) — a PSU-grouped split (no survey
  cluster appears in both), never touched during fitting, calibration or threshold selection.
- Each model was fit on development only, with its own internal 3-fold grouped calibration and
  a 95%-weighted-sensitivity development-selected threshold — the same convention used for every
  outer fold everywhere else in `research_extension.py`. The holdout was touched exactly once,
  for evaluation.

## Result

| Model | AUROC | AP | Brier | Weighted sensitivity | Deferred | Missed / 29 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Logistic (`demographics_bmi_cbc`) | 0.766 | 0.083 | 0.0157 | 90.2% | 399 | 1 |
| AdaBoost | **0.829** | 0.116 | 0.0152 | **100.0%** | 257 | **0** |
| Ensemble (logistic + AdaBoost) | 0.821 | 0.090 | 0.0159 | 95.5% | 618 | 2 |

**On this genuinely untouched sample, AdaBoost outperforms logistic regression** — the reverse
of the nested-CV ranking used throughout the rest of this project (where logistic edges out
AdaBoost, 0.835 vs 0.821, averaged over many reused folds). AdaBoost also achieves perfect
weighted sensitivity here (misses 0 of 29 positive labels) while deferring fewer tests than
either alternative.

## Why this should not be over-interpreted as "AdaBoost wins"

- **29 positive events is a very small holdout.** A single-split AUROC estimate at this event
  count has wide sampling variability — this result is consistent with the repeated nested-CV
  finding that the gap between logistic and AdaBoost is not reliably distinguishable from noise
  (paired bootstrap interval for `Logistic_minus_AdaBoost_AUROC`, see
  `docs/findings/research_extension_results.md`), not necessarily evidence that the ranking
  genuinely flipped.
- **This is one realization of the random holdout split, not a repeated estimate.** Unlike the
  100-replicate PSU bootstrap used elsewhere, this holdout is deliberately evaluated only once —
  that's the entire point of reserving it — so there's no distribution to characterize its own
  uncertainty from, beyond noting the small event count.
- **The honest reading:** both logistic and AdaBoost (and the ensemble) generalize reasonably to
  genuinely unseen data (none collapsed or showed a dramatically different operating
  characteristic than development suggested), and the three models remain close enough that
  this project does not have enough data to confidently declare one one the single best model.
  That is itself a legitimate, reportable finding — not a failure of the holdout.

## Status and reproduction

Run `python scripts/analysis/final_holdout_evaluation.py` from the repository root. Running it
again reproduces the identical split and result (fixed seed) — it does not draw a new holdout.
If the locked model or feature set changes meaningfully in the future, a genuinely new holdout
(a new, documented seed) would be needed for another one-time final check; re-running this
script with modified models and reporting it as confirmatory would defeat its purpose.

Outputs: `results/final_holdout/final_holdout_predictions.csv`,
`final_holdout_summary.csv`, `final_holdout_roc.png`, `final_holdout_metadata.json`.
