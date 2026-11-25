# Executable scripts

Install `requirements.txt` at the project root. From that root:

| Purpose | Command | Outputs |
|---|---|---|
| Acquire missing public BMI/older-cycle inputs | `python scripts/data/acquire_extension_data.py` | `data/raw/`, `data/manifests/` |
| Compare cohorts | `python scripts/analysis/cohort_analysis.py` | `results/cohort/` |
| Weighted validation and calibration | `python scripts/analysis/weighted_calibration_analysis.py` | `results/weighted_calibration/` |
| CBC collinearity and nested PCA supplement | `python scripts/analysis/cbc_diagnostics.py` | `results/cbc_diagnostics/`, diagnostic report and validation JSON |
| Held-out grouped predictor importance | `python scripts/analysis/heldout_permutation_importance.py` | `results/permutation_importance/`, findings and validation JSON |
| Independently verify permutation importance | `python scripts/verification/verify_permutation_importance.py` | Reconstructs exported metric differences and checks donor accounting |
| Final-cohort description figure | `python scripts/figures/plot_final_cohort.py` | `results/cohort/` |
| BMI/robustness/independent-cycle analysis | `python scripts/analysis/research_extension.py --bootstrap 100` | `results/research_extension/` |
| Generate extension reports and results notebooks | `python scripts/reporting/report_research_extension.py` | findings, draft text, notebooks 05–06 |
| Verify weighted outputs | `python scripts/verification/verify_weighted_outputs.py` | `docs/verification/weighted_validation.json` |
| Verify research extension | `python scripts/verification/verify_research_extension.py` | `docs/verification/research_extension_validation.json` |
| Verify organization-only changes against the research commit | `python scripts/verification/verify_organization.py` | `docs/verification/organization_validation.json` |
| Render contributor review tabs | `python scripts/reporting/render_team_review.py` | `docs/reviews/TEAM_REVIEW.html` from the Markdown review |
| CBC/demographic feature-reduction exploration (Phase 15) | `python scripts/analysis/feature_reduction.py` | `results/feature_reduction/`, [findings](../docs/findings/feature_reduction.md) |
| Biomarker expansion screen (Phase 9, exploratory) | `python scripts/analysis/biomarker_expansion.py` | `results/biomarker_expansion/`, [findings](../docs/findings/biomarker_expansion.md) |
| Final locked holdout evaluation (Phase 15 Step 6 — **spent, do not rerun with new specs and call it confirmatory**) | `python scripts/analysis/final_holdout_evaluation.py` | `results/final_holdout/`, [findings](../docs/findings/final_holdout_evaluation.md) |
| Secondary (prediabetes, HbA1c≥5.7%) threshold sensitivity, exploratory | `python scripts/analysis/secondary_threshold_cohort.py --bootstrap 100` | `results/secondary_threshold/`, [findings](../docs/findings/secondary_threshold_cohort.md) |

The report generator writes only notebooks 05–06. The other scripts do not rewrite notebooks.
Analysis scripts regenerate their own outputs; they do not select new cohort/model choices.
The full extension includes 100 refitted survey resamples and takes longer than reading the
saved-results notebooks. Notebooks 05–06 default to displaying those saved results.

## Phase 2: initial-vs-reduced feature-set comparison

`scripts/phase-2/` holds copies of the three core modeling scripts above
(`cohort_analysis.py`, `weighted_calibration_analysis.py`, `research_extension.py`),
parameterized to run under both the `initial` (21 CBC features + income) and `reduced` (9 CBC
features, no income) variants now defined in `scripts/analysis/study_config.py`
(`FEATURE_SET_VARIANTS`). The originals above are untouched and still run the `initial` variant
only.

| Command | Outputs |
|---|---|
| `python scripts/phase-2/cohort_analysis.py` | `results/phase-2/cohort_analysis/{initial,reduced,comparison}/` |
| `python scripts/phase-2/weighted_calibration_analysis.py` | `results/phase-2/weighted_calibration/{initial,reduced,comparison}/` |
| `python scripts/phase-2/research_extension.py --bootstrap 100` | `results/phase-2/research_extension/{initial,reduced,comparison}/` |

Each `comparison/` folder has merged CSVs and labeled-legend bar charts. See
[the full writeup](../docs/findings/phase2_feature_variant_comparison.md). `cbc_diagnostics.py`
and `heldout_permutation_importance.py` were not duplicated here — they're diagnostic tools for
a *given* feature set (collinearity, held-out importance), not part of the initial-vs-reduced
performance comparison.

Raw 2021–2023 files are under `data/raw/2021_2023/`; the downloaded laboratory reference
collection remains in its `laboratory/` subfolder. Independent-cycle inputs are under
`data/raw/2017_2018/`. Existing duplicate reference files are retained for provenance.
