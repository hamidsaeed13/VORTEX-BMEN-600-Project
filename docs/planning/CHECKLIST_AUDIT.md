# Checklist reconciliation — 2026-11-16

This audit distinguishes implementation in the current `organize-project` checkout from
open contributions and team decisions. A checked implementation does not mean that it
has been independently scientifically reviewed or merged into `main`.

## Why unchecked tasks already have implementations

The original plan was retained while notebooks 03–06 and their executable scripts were
added. Progress paragraphs were appended, but most individual checkboxes were never
updated. `MANUAL_TODO.md` also retained historical midterm branch/submission statements.
The local research commits `3558e76` and `9fd7466` already contain much of that work.

| Phase | Evidence in this checkout | Remaining work |
|---|---|---|
| 1 | `load_cycle` corrects SAS near-zero values and validates unique IDs | Actual original download date |
| 3 | `cohort_analysis.py`, cohort-flow/summary CSVs, fasting eligibility in extension | Team agreement on population and HbA1c endpoint |
| 4 | One-to-one merges and row-count assertions; explicit diagnosis eligibility | Full categorical allowed-value audit, explicit sentinel normalization, interview/examination/nonresponse breakdown |
| 5–6 | Fold-fitted pipelines, one-hot nominal variables; numeric missingness indicators in extension | Final missing-data justification and independent review |
| 7 | Basophil percentage already removed in extension; new diagnostic/PCA supplement | Review findings; avoid causal coefficient interpretations |
| 8 | WTPH2YR/WTSAF2YR; PSU-grouped folds; conditional design intervals | Independent statistical review |
| 9 | Matched BMI comparisons, red/white-cell ablations, low-HGB checks | Other candidate blocks remain candidates; integration with Ella's contribution |
| 10 | Age baseline, logistic/forest models, nested development-only procedures | Original demographics-only forest and gradient boosting tasks |
| 11 | Calibration, AP/proper scores, policy accounting, subgroup/fasting checks, 100 full refits, older-cycle transport | Permutation importance if making importance claims; stronger uncertainty/reproduction |
| 12 | Exploratory 95%-sensitivity development thresholds and decision curves | Team-justified operating point; no established clinical or economic benefit |
| 13 | Extension evidence matrix and BMI literature | Three original full-text gaps and second-reader review |
| 14 | Pinned `requirements.txt`, runnable scripts | Review old notebook narrative/setup statements |

## Teammates' pending contributions

Read from GitHub's open-PR descriptions on 2026-11-16. These descriptions are evidence of
submitted work, not independent execution or approval. No contribution was merged by this audit.

**Subsequent source review:** [Team contribution review](../reviews/TEAM_REVIEW.md)
now examines the actual source and reproduces cohort/model results. It identifies a
matched age/sex-only forest in PR 15, explicit fixes in both contributions and eligibility
differences. That forest fulfills a comparison within Setayesh's exploratory specification;
integration with the current population and demographic baseline remains open.

| Contribution | Submitted by | Reported scope | Integration issue |
|---|---|---|---|
| [PR 13](https://github.com/hamidsaeed13/VORTEX-BMEN-600-Project/pull/13) | ProbablyElla | Phase 8: weight choice, design variables, weighted prevalence; 5,144 adults 18+ | Proposes HbA1c ≥5.7% as primary; differs from current ≥6.5%/age 20+ study |
| [PR 14](https://github.com/hamidsaeed13/VORTEX-BMEN-600-Project/pull/14) | ProbablyElla | Phase 9: BMI/waist, hs-CRP, iron, anemia checks; exploratory unweighted 5-fold logistic CV | Uses PR 13's cohort and ≥5.7% endpoint; cannot pool its metrics with current results; attenuation checks cannot prove anemia is irrelevant |
| [PR 15](https://github.com/hamidsaeed13/VORTEX-BMEN-600-Project/pull/15) | Setayeshafshar-code | Phase 4: cleaning, sentinel/category checks, merge assertions, cohort flow, missingness, precision–recall | Reports 4,930 participants/152 positives and permits incomplete CBC; validation boxes are unchecked |

Current primary analysis: adults 20+, explicit no prior diagnosis, no reported current
diabetes medication, pregnancy restrictions, positive phlebotomy weights, observed HbA1c
and all 12 CBC values; 4,612 participants/106 HbA1c ≥6.5% labels. Different counts need
eligibility reconciliation, not a decision that one teammate's result is automatically wrong.

## Recommended order

1. Review the Phase 7 diagnostic/PCA supplement and its validation output.
2. Agree as a team whether the primary endpoint is ≥6.5% or ≥5.7%, and fix eligibility.
3. Reconcile PRs 13–15 against that agreed specification, retaining useful cleaning and
   feature-expansion work and rerunning comparisons on matched participants/folds.
4. Complete justified model/evaluation gaps; keep optional feature/model experiments explicit.
5. Independently reproduce, agree policy tradeoffs, and integrate the final report.

## Course requirements checked

The local `docs/course/BMEN600 Final Project.pdf` requires a cohesive paper of at most
10 body pages, an organized reproducible repository with a submitted commit identifier,
and a five-minute group presentation. Its deadline is Friday, December 4 at 11:59 p.m.
It requires a meaningful comparison, uncertainty, data/sample and primary-result
figures/tables, limitations, AI-use verification and contributions. It does not require
testing every candidate biomarker or inventing an algorithm. The plan's broad feature
menu should therefore be prioritized by the agreed question and feasible coverage.

The dated extension protocol remains unchanged. Checklist status reflects current
implementation; original historical instructions in the manual TODO remain below a dated notice.
