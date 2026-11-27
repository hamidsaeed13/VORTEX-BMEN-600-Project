# Secondary (prediabetes) HbA1c threshold sensitivity (2026-11-24)

Team request: "is it possible to increase the population based upon [a lower HbA1c]
threshold" -- confirmed to mean relabeling the locked cohort using `study_config.SECONDARY_CUT`
(HbA1c >= 5.7%, the prediabetes/borderline range) instead of `PRIMARY_CUT` (HbA1c >= 6.5%,
frank diabetes). **This does not change who is in the cohort** -- eligibility doesn't depend on
HbA1c, so it's the same 4,612 people -- it only relabels which of them count as positive,
shifting the clinical question from "detect diabetes" to "detect diabetes-or-prediabetes."
`study_config.py` already flags `SECONDARY_CUT` as "secondary/exploratory only, never the
primary label" for exactly this reason.

Does not touch `study_config.py`, the locked outcome definition, or
`results/research_extension/`.

## Population: a real 12.7x increase in positive cases

| Threshold | n | positives | prevalence |
| --- | ---: | ---: | ---: |
| Primary (HbA1c >= 6.5%, locked) | 4,612 | 106 | 2.3% |
| Secondary (HbA1c >= 5.7%) | 4,612 | **1,348** | 29.2% |

1,242 participants flip from negative to positive. Same pattern holds in the 2017-2018 cycle
(132 -> 1,366 positives).

## AUROC drops for every BMI/CBC-based model

| Model | Primary (6.5%) | Secondary (5.7%) | Δ |
| --- | ---: | ---: | ---: |
| demographics only | 0.717 | 0.741 | +0.024 |
| demographics+BMI | 0.815 | 0.763 | -0.053 |
| demographics+BMI+CBC | 0.835 | 0.798 | -0.037 |
| + AdaBoost | 0.821 | 0.772 | -0.049 |
| + ensemble | 0.846 | 0.796 | -0.050 |

Prediabetes involves much subtler physiological change than frank diabetes, so the same CBC/BMI
signal that separates diabetics from healthy people is weaker for this broader, milder
condition. More events bought lower absolute performance, not higher.

## But the extra power resolves every previously-ambiguous model comparison

100 full-pipeline PSU-bootstrap replicates, paired AUROC-gain 95% intervals:

| Comparison | Primary (106 events) | Secondary (1,348 events) |
| --- | --- | --- |
| CBC - BMI | [-0.034, 0.062] (includes 0) | **[0.023, 0.045]** (excludes 0 -- CBC genuinely helps) |
| Logistic - AdaBoost | [-0.042, 0.101] (includes 0) | **[0.015, 0.042]** (excludes 0 -- logistic genuinely wins) |
| Ensemble - Logistic | [-0.058, 0.046] (includes 0) | [-0.005, 0.004] (tiny interval, essentially tied) |
| Ensemble - AdaBoost | [0.003, 0.065] (barely excludes 0) | **[0.016, 0.038]** (excludes 0 -- ensemble genuinely beats AdaBoost) |

This is the first time in this project that the CBC-vs-BMI-alone comparison has cleanly excluded
zero. With ~12.7x more events, three of the four paired comparisons resolve cleanly (two of them
newly significant), and the fourth (ensemble vs. logistic) tightens into a near-exact tie rather
than staying ambiguous. This directly confirms the standing diagnosis for this whole project
(`docs/findings/research_extension_results.md`, `docs/findings/final_holdout_evaluation.md`):
model-ranking ambiguity in the primary analysis is a sample-size artifact of having only 106
diabetic events, not evidence the models are genuinely indistinguishable. Give the same
procedure enough events and it does distinguish them.

## Reading

- **Not a free win.** The secondary cut answers a different, milder clinical question
  (diabetes-or-prediabetes) at a lower absolute AUROC. It should not be reported as "the
  model got better."
- **Is a genuine methodological finding.** It's direct evidence that this project's event count
  (106) is the binding constraint on statistical resolution, exactly as the final-holdout and
  paired-bootstrap analyses on the primary cohort already suggested from the other direction.
- Logistic beating AdaBoost here, with the ensemble essentially tied with logistic, is a
  different ranking than the inconclusive primary-cohort comparison -- plausible, since
  AdaBoost's extra flexibility may show its cost (or lack of benefit) more clearly with more
  events, but this is evidence about the *prediabetes* task, not a corrected verdict on the
  primary diabetes task.

## Status and reproduction

Exploratory; does not change the locked feature set, outcome definition, or any published
headline number. Run `python scripts/analysis/secondary_threshold_cohort.py [--bootstrap 100]`.
Outputs: `results/secondary_threshold/cohort_counts.csv`, `secondary_predictions.csv`,
`secondary_model_comparison.csv`, `secondary_conditional_intervals.csv`,
`secondary_vs_primary_comparison.csv`, `auroc_comparison.csv`, `bootstrap_replicates.csv`,
`bootstrap_intervals.csv`, `secondary_threshold_metadata.json`.
