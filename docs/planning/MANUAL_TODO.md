# Things only you (or the team) can do

Running list, updated as I keep working on the Midterm Research Plan. Nothing has been pushed —
there is a local commit (`347c1b1`) from earlier, plus further uncommitted changes from this pass,
all still on branch `Hamid-midTermProposal`.

## 0. Major revision just applied — please read this one carefully

You supplied an independent, external verification report
([docs/verification/Midterm_Research_Plan_Verification_Report.md](../verification/Midterm_Research_Plan_Verification_Report.md))
that rendered the actual draft (something I can't do on this machine — no LibreOffice/pandoc here)
and found real problems. I independently re-checked its highest-stakes claims against primary
sources myself before acting on them — all of them held up. I then rewrote the draft to fix
everything in it. This was a substantial revision, not a polish pass:

- **Page count**: the audit found the previous draft rendered to **7 body pages against a 6-page
  limit**. The new draft cuts body length from ~3,340 words to ~2,580 — well under the ~472
  words/page the audit measured, so it should now fit with real margin. I still can't render it
  myself to triple-check — **please confirm the actual page count once you open it in Word.**
- **The research question didn't match the model**: the title and question promised blood-glucose
  prediction, but the actual model predicts diabetes-range HbA1c. Rather than ask you to pick
  between the audit's two suggested fixes, I went with the lower-risk one given the deadline:
  **renamed the title/question around HbA1c**, keeping fasting glucose as a secondary check. If the
  team would rather make glucose the primary target and demote the current HbA1c model to
  "preliminary feasibility work," that's a bigger change (different cohort, different numbers) —
  tell me and I'll redo it, but it's a real scope decision, not something I should decide alone.
- **The model mostly detects people who already know they have diabetes**: 565 of 717 "positive"
  cases (78.8%) already report a prior diagnosis. This is now stated explicitly in Sections 4 and
  5, since it directly undercuts an "undiagnosed screening" framing.
- **Two real literature errors, found by rereading the actual papers**: the Guo et al. study (our
  closest precedent) was described as using "CBC data alone" — it actually also uses age, BMI, sex,
  and two inflammatory ratios. And the Horton et al. citation was being used to claim glucose costs
  more than CBC — the paper's own pricing table shows the opposite (CBC costs 1.33–6.67× more).
  Both fixed. Full list of what changed in
  [literature/README.md](../../literature/README.md).
- **Kamkar et al. [7] is no longer "not obtained"** — PMC's bot-block turned out to be intermittent;
  a retry got the full text, with real numbers (sensitivity 61.8%/NPV 88.9% at one threshold) now
  cited as a genuine precedent instead of a vague, hedged mention.
- **NPV was being presented as proof of safe test deferral.** It isn't, on its own — a model that
  flags nobody still gets 89.3% NPV. The draft now reports tests flagged, tests deferred, *and*
  positive cases missed together at each threshold, not NPV in isolation.
- **IEEE citation order was wrong** (ref [20] was used before ref [10]) — fixed by renumbering; the
  PDF files in `literature/papers/` were renamed to match.
- Smaller fixes: NHANES dataset description restored (multistage/cross-sectional/noninstitutionalized
  language), the main `README.md`'s overly broad "NHANES has no other glucose measurement" claim
  softened (a serum glucose variable does exist in `BIOPRO_L`, just not yet used), setup/run
  instructions added to `README.md` since there weren't any, and several other citation-detail
  corrections logged in `literature/README.md`.

- [ ] **Confirm the actual page count in Word** — this is the one thing I most need verified.
- [ ] **Confirm the HbA1c-as-primary-endpoint call above** — or tell me to redo it around glucose.
- [ ] Read through for tone — still a draft, not a final copy-edit.

## 1. Papers still not fully obtained (3 of 18 — down from 10)

- [ ] Veeranna et al., *Cardiology* (2012) — doi: 10.1159/000339225
- [ ] Engström et al., *J. Intern. Med.* (2014) — doi: 10.1111/joim.12188 (abstract obtained)
- [ ] Bang et al., *Ann. Intern. Med.* (2009) — doi: 10.7326/0003-4819-151-11-200912010-00005

All blocked by a Cloudflare/WAF challenge; two also need library access. The draft only claims what
each source's title or abstract directly supports.

## 2. Decisions and confirmations only the team can make

- [ ] **Author Contributions** — Review and update all five members' contributions for the
  final submission, then have each member confirm their entry.
- [ ] **AI-Assisted Work statement** — confirm the described tools/checks match what the team
  actually did, beyond what I can see in this repo.
- [ ] **Intended screening population** — the current exploratory model includes participants as
  young as 12 and both diagnosed and undiagnosed people. Decide the real intended population
  (e.g., adults only, no prior diagnosis) before the final report; the current numbers will change
  once that's applied.
  **Progress note:** Notebook 03 implements a recommended adults-20+ cohort with explicit
  no prior diagnosis (4,612 participants, 106 positive HbA1c results); team agreement on
  the intended population remains open. See [cohort analysis](../findings/cohort_definition_analysis.md).
- [ ] **Real dataset access date** — Section 3 currently says "to be confirmed." I don't have the
  team's actual download date and didn't want to guess one.
- [ ] **Team size vs. course template** — the template mentions teams of 3–4; the signed Team
  Contract lists 5. If the instructor already approved 5, no action needed — just flagging it per
  the audit so nobody is surprised.
- [ ] **Design Critique lead** — still TBD in the workstream plan; assign when known.

## 3. Submission logistics (can't be done by me)

- [ ] Export the finished Research Plan to PDF and submit to D2L by **Fri, Oct 16, 11:59 PM**.
- [ ] Include the GitHub repo link: `https://github.com/hamidsaeed13/VORTEX-BMEN-600-Project` —
  and confirm the grader can actually see the branch/commit you intend to submit (I can't check
  remote visibility from here).
- [ ] Decide whether/when to commit, merge `Hamid-midTermProposal` into `main`, and push — I'm not
  doing any of that without you telling me to.

## 4. Real next-step work (correctly scoped as post-midterm, not blocking submission)

Per the audit's own recommended sequence, these are improvements for the final project, not fixes
required before tomorrow: one-hot encoding for race/education instead of raw numeric codes, NHANES
survey weights and design variables in the actual model fit, calibration checks (the current models'
mean predicted risk doesn't match the true prevalence), stratified k-fold cross-validation with
the pipeline refit per fold, and further model comparisons. The age-only baseline is now implemented in notebook 02,
using the same cohort/split as the other models, with matched threshold comparisons and
exported AUROC/threshold tables in `results/baseline/`. The remaining improvements are listed in
the notebook's own "Next steps" section.

**Progress note (notebooks 03–04):** One-hot encoding, preprocessing refitted per fold,
survey-weighted fitting/evaluation, and development-only calibration are implemented.
Notebook 04 adds nested cluster-grouped validation and conditional survey-design intervals;
those intervals exclude model-training variability. Independent validation, further model
comparisons and clinical-policy justification remain open. See the
[weighted analysis report](../findings/weighted_calibration_analysis.md) for details.

---
*I'll keep this file updated as I continue refining the Research Plan.*

**Progress note (2026-11-02):** Notebooks 05–06 add the matched BMI comparison,
red-cell/fasting-glucose sensitivity checks, 100 full-refit survey resamples and frozen-model
2017–2018 evaluation. See [results](../findings/research_extension_results.md), the
[literature update](../../literature/extension_evidence_matrix.md) and
[publication-readiness assessment](../findings/publication_readiness.md). Team review, three
full-text gaps and independent clinical/statistical verification remain open; no clinical
deferral policy or publication readiness is established. Original checklist wording is preserved.
