# Evidence matrix and literature synthesis — 2026-11-02

This is a targeted narrative update to the existing midterm review, not a systematic review.
It preserves the original source notes and distinguishes directly checked full text from
abstract-only evidence. A high AUROC from a different population/endpoint is not a benchmark
our model is expected to beat. The companion CSV provides an editable extraction table.

## Closest prediction studies

| Study | Population / endpoint | Predictors and validation | Use in this project |
|---|---|---|---|
| [Guo 2026](https://www.nature.com/articles/s41598-026-59213-3) | Chinese hospital examinations; HbA1c ≥5.7%, including prediabetes and established diabetes | CBC, age, sex, BMI, NLR/PLR; development and later-year evaluation; calibration assessed | Closest CBC precedent; motivates BMI comparator, but not the same outcome or diagnosis exclusions. Full text rechecked. |
| [Liu 2025](https://ai.jmir.org/2025/1/e68260/) | NHANES adults without reported diagnosis; combined HbA1c/FPG/OGTT endpoint | Anthropometric, demographic, dietary and behavioral information; AutoML, random holdout; AUROC 0.909 | Establishes existing NHANES undiagnosed-screening work. No CBC incremental comparison; test-set F1 threshold choice should not be copied. Full text rechecked. |
| [Kamkar 2026](https://doi.org/10.1016/j.ahjo.2026.100854) | Adults free of diabetes at baseline; incident diabetes | Hematological and clinical/metabolic predictors; forest AUROC 0.73 | Longitudinal prediction differs from detecting a contemporaneous laboratory result; not evidence of safe omission. Existing local full text. |
| [Mansoori 2023](https://doi.org/10.1038/s41598-022-27340-2) | MASHAD cohort; diabetes-related classification | Hematological/clinical variables; bootstrap forest | Association/model precedent; does not isolate the value of CBC beyond a matched BMI baseline. Existing local full text. |
| [Bang 2009](https://pubmed.ncbi.nlm.nih.gov/19949143/) | Adults 20+ without known diabetes; FPG ≥126 | Age, sex, obesity, family history, hypertension and activity; NHANES development and separate cohorts | Established nonlaboratory screening comparator. PMC record exists but full-text retrieval remained bot-blocked this pass; detailed extraction remains incomplete. |

Survey weighting in a hospital cohort is not applicable in the same way as NHANES weighting.
For papers where design weighting/calibration details were not explicitly verified, the CSV
says so; absence of a checked detail is not proof that the authors omitted it.

## Biological interpretation and endpoint validity

[English 2015](https://pubmed.ncbi.nlm.nih.gov/25994072/) supports the concern that red-cell
abnormalities can affect HbA1c independently of glucose. Excluding low hemoglobin does not
remove all iron deficiency, altered red-cell survival or hemoglobin variants. The new red-cell
versus white-cell/platelet ablations and matched fasting-glucose analysis address different
parts of that concern, but neither proves a mechanism.

[Engström 2014](https://pubmed.ncbi.nlm.nih.gov/24471821/) is important because an HbA1c
association need not have the same direction as future diabetes risk. The abstract reports
lower RDW associated with incident diabetes while RDW is positively associated with HbA1c.
The remaining full-text gap must be resolved before extracting more detail.

Park, Gkrania-Klotsas and Lorenzo provide inflammatory-marker context; Mertoglu provides
small-sample ratio associations. They do not validate a test-deferral policy. Yin concerns
glycemic control among established diabetes patients, so it should not be presented as an
undiagnosed-screening study. Veeranna remains an abstract/metadata-level source, not a newly
verified full-text study. The correct primary-study PMID is 22813786; avoid confusing it with
the similarly indexed RDW commentary (PMID 22890371).

## Methods and clinical utility references to add

- [TRIPOD+AI, Collins et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11019967/): reporting
  guidance for regression and machine-learning prediction research; not a quality certification.
- [PROBAST+AI, Moons et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11931409/): development
  quality and evaluation risk-of-bias/applicability framework. An independent assessment is
  still needed; the project self-audit is not a completed formal rating.
- [Riley et al., external evaluation guidance](https://www.bmj.com/content/384/bmj-2023-074820):
  discrimination, calibration and utility should be examined together.
- [Rao and Wu 1988](https://doi.org/10.1080/01621459.1988.10478591) and
  [Rao, Wu and Yue 1992](https://www150.statcan.gc.ca/n1/en/pub/12-001-x/1992002/article/14486-eng.pdf):
  complex-survey resampling; the extension uses the two-PSU-per-stratum rescaled case.
- [WHO 2024 cutoff table](https://www.ncbi.nlm.nih.gov/books/NBK602183/table/fm-ch1.tab2/): supports
  operational hemoglobin thresholds within its stated adult age range; older ages require caution.
- [CDC variance/domain tutorial](https://wwwn.cdc.gov/nchs/nhanes/tutorials/varianceestimation.aspx):
  retain the full design when estimating domain uncertainty.

## What belongs in the final Introduction and Discussion

The Introduction should move from opportunistic screening to the specific unresolved
comparison: whether CBC adds to demographics plus BMI among people without reported diagnosis.
Explain why HbA1c-related red-cell effects make that comparison scientifically nontrivial.
Discuss Guo and Liu as closest precedents, rather than listing unrelated model accuracies.

The Discussion must compare incremental gains, endpoint definitions, calibration and evaluation
design. A smaller gain after BMI, a negative sensitivity result, or weaker transport calibration
is substantive evidence. Do not claim a new algorithm, a first-ever CBC screening approach,
confirmed undiagnosed diabetes, proven cost savings or a safe rule for withholding tests.
This limited search cannot establish novelty; a broader database/citation search is needed
before making an originality claim in a journal submission.

## Still requiring team/library work

Obtain and verify the three existing full-text gaps (Veeranna, Engström, Bang), have a second
reader check the closest-study extraction, choose a target journal, and format the final
references in first-citation IEEE order. The existing 18 papers are not all equally relevant
to the final question; inclusion should follow the argument rather than a reference-count goal.
