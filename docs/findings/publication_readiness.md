# Publication-readiness assessment — 2026-11-02

**Assessment:** a substantially developed exploratory secondary-data study, not a submission-ready
clinical decision tool. A journal paper is plausible in principle, with an incremental-value and
robustness focus. Acceptance, novelty and clinical benefit have not been established. The mixed
results, including negative sensitivity findings and worse independent probability error, belong
in the manuscript rather than being optimized away.

This is a preliminary project self-audit informed by
[TRIPOD+AI](https://pmc.ncbi.nlm.nih.gov/articles/PMC11019967/) and
[PROBAST+AI](https://pmc.ncbi.nlm.nih.gov/articles/PMC11931409/).
It is not an independent formal PROBAST+AI assessment or a completed item-by-item TRIPOD checklist.

| Area | Available evidence | What remains before submission |
|---|---|---|
| Focused contribution | Matched BMI incremental comparison, red/white-cell ablations, fasting-endpoint comparison, independent-cycle evaluation | Broader novelty search and supervisor/clinical agreement on intended use; no claim of a first-ever method |
| Participants | Explicit recommended eligibility and flows; current n=4,612/106 positives; independent n=3,943/132 | Team acceptance of research scope; limitations of diagnosis self-report and unavailable pregnancy status |
| Data provenance | Codebooks, new-download URLs/timestamps/hashes, cycle harmonization | Original pre-existing download date remains unknown; final journal data/ethics wording needs institutional verification |
| Predictors | Training-fold imputation/scaling/one-hot encoding; BMI and CBC blocks; coefficients and frozen pipelines | Independent review of variable coding, collinearity and intended clinical availability; no causal interpretation of coefficients |
| Outcome | HbA1c≥6.5%; separate fasting endpoint and discordance analysis | Single-test laboratory outcome cannot establish confirmed diabetes; anemia flag does not exhaust HbA1c interference |
| Missingness | Predictor missingness, otherwise-eligible excluded-record audit and BMI-observed sensitivity | Stronger missing-data assumptions/selection assessment; no claim that released weights solve every nonresponse mechanism |
| Modelling | Prespecified matched logistic and forest comparisons; grouped nested validation; weighted calibration | Rare events relative to flexible models remain a concern; sample-size/model-complexity review by a statistician |
| Uncertainty | Conditional design jackknife and 100 full-pipeline PSU resamples | More replicates for tail stability before publication; independent review of rare-event resampling and fixed-split conditioning |
| Independent evaluation | Frozen 2021–2023 models evaluated without updating in 2017–2018 | Backwards-in-time transport is not prospective or independent health-system validation; performance in clinical encounters unknown |
| Calibration/utility | Brier/log loss, independent reliability bins, policy miss counts, assumed-harm decision curves | Clinical harm/cost assumptions not agreed; independent probability error worsens after CBC; no actual economic/impact evaluation |
| Subgroups | Sex/age/race descriptive tables with event counts and suppression below 10 positives | Adequate precision and independent fairness assessment; do not interpret nonsignificant differences as equal performance |
| Literature | 21-source extraction CSV, synthesis and dated search log | Three original full-text gaps; second-reader checking; comprehensive search before strong novelty claims |
| Reproducibility | Requirements, input hashes, exported predictions/models, scripts, results notebooks and independent accounting checks | Clean environment reproduction by a teammate; versioned submitted commit and accessible repository; untrusted pickle/joblib files must not be loaded |
| Manuscript | Draft Introduction and Methods/Results inserts with generated evidence | Integrated Abstract/Discussion/Conclusion, numbered captioned figures and journal formatting; provisional interpretation is not a final conclusion |
| Transparency | AI-assisted analysis is evident in code/history; no fictional contributor assignments | Confirm all five actual author contributions, human verification and AI-use disclosure; conflicts/funding and institutional publication decisions |

Suggested paper framing: **Incremental value and robustness of CBC for detecting diabetes-range
HbA1c beyond demographics and BMI in adults without reported diabetes: a survey-weighted NHANES
analysis with independent-cycle evaluation.** This is a working framing, not an approved title.

The most useful remaining scientific work is independent clinical/statistical review of the
outcome and sampling assumptions, replication with more resamples, and evaluation in a dataset
representing the intended clinical workflow. More algorithms alone will not resolve those gaps.
No ethics exemption, consent waiver or permission to publish has been asserted on the team's behalf.
