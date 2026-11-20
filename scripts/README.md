# Executable scripts

Install `requirements.txt` at the project root. From that root:

| Purpose | Command | Outputs |
|---|---|---|
| Acquire missing public BMI/older-cycle inputs | `python scripts/data/acquire_extension_data.py` | `data/raw/`, `data/manifests/` |
| Compare cohorts | `python scripts/analysis/cohort_analysis.py` | `results/cohort/` |
| Weighted validation and calibration | `python scripts/analysis/weighted_calibration_analysis.py` | `results/weighted_calibration/` |
| Final-cohort description figure | `python scripts/figures/plot_final_cohort.py` | `results/cohort/` |
| BMI/robustness/independent-cycle analysis | `python scripts/analysis/research_extension.py --bootstrap 100` | `results/research_extension/` |
| Generate extension reports and results notebooks | `python scripts/reporting/report_research_extension.py` | findings, draft text, notebooks 05–06 |
| Verify weighted outputs | `python scripts/verification/verify_weighted_outputs.py` | `docs/verification/weighted_validation.json` |
| Verify research extension | `python scripts/verification/verify_research_extension.py` | `docs/verification/research_extension_validation.json` |
| Verify organization-only changes against the research commit | `python scripts/verification/verify_organization.py` | `docs/verification/organization_validation.json` |

The report generator writes only notebooks 05–06. The other scripts do not rewrite notebooks.
Analysis scripts regenerate their own outputs; they do not select new cohort/model choices.
The full extension includes 100 refitted survey resamples and takes longer than reading the
saved-results notebooks. Notebooks 05–06 default to displaying those saved results.

Raw 2021–2023 files are under `data/raw/2021_2023/`; the downloaded laboratory reference
collection remains in its `laboratory/` subfolder. Independent-cycle inputs are under
`data/raw/2017_2018/`. Existing duplicate reference files are retained for provenance.
