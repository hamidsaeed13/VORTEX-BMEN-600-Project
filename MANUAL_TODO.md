# Things only you (or the team) can do

Running list, updated as I keep working on the Midterm Research Plan. Nothing has been committed
or pushed anywhere — it's all local, on branch `Hamid-midTermProposal`.

## 0. Draft is ready — please eyeball it

Updated draft at **[drafts/Midterm_Research_Plan_Draft.docx](drafts/Midterm_Research_Plan_Draft.docx)**,
plus a new **[code/02_baseline_model_and_figures.ipynb](code/02_baseline_model_and_figures.ipynb)**
with a real, executed baseline model (not a mockup) feeding Section 5.

What changed in this pass:
- **Fact-checked every citation against its actual PDF**, not just an abstract snippet — several
  numbers/claims were corrected or sharpened as a result (e.g., the Lorenzo and Gkrania-Klotsas
  papers were previously lumped together as uniformly confirmatory; the Lorenzo cohort's own
  finding was actually null after adjustment, which the draft now says explicitly). Full list of
  what was checked and what changed: [literature_review/README.md](literature_review/README.md).
- **Added a real baseline model** (logistic regression + random forest on the actual NHANES data):
  AUROC improves from 0.743 (demographics only) to 0.811 (CBC + demographics, random forest), with
  a full sensitivity/specificity/NPV table across thresholds. This is now in Section 5, and is a
  genuine, reproducible run — all numbers in the Word doc match the notebook's own printed output.
- **Removed all team-member names** from the document (title page, Section 6, AI-Assisted Work,
  Author Contributions) per your instruction — those sections now speak by role (Project Manager,
  Coordinator, Editor, Reviewer, Presentation Lead) instead of by name. Published-author names in
  the References list were kept (required for valid citations).
- **`Sugar Predictor/`** (the old project you added) is now in `.gitignore` — it won't be tracked
  or pushed. I used it only to confirm standard technique choices (SMOTE/class-weighting for
  imbalance, stratified splits, correlation heatmaps) — none of its own data or any mention of it
  appears anywhere in the report.

- [ ] **Open the .docx in Word and check the actual page count.** Body content is ~3,140 words
  plus one table and one figure; I can't render it here (no LibreOffice/pandoc on this machine) to
  confirm it's under the 6-page cap. If it's over, tell me and I'll cut further — Section 2 is the
  easiest place to trim without losing the new verified numbers.
- [ ] Read through for tone — this is still a draft, not a final copy-edit.

## 1. Papers still not obtained (4 of 18 — down from 10)

You got most of them. These four remain blocked by a Cloudflare/WAF bot challenge or PMC's JS
proof-of-work challenge, which need a real logged-in browser (three also need library access).
The draft only cites these at the level of their title (no specific stat quoted from any of them),
so they're not blocking, just incomplete:

- [ ] Kamkar et al., *Am. Heart J. Plus* (2026) — doi: 10.1016/j.ahjo.2026.100854
- [ ] Veeranna et al., *Cardiology* (2012) — doi: 10.1159/000339225
- [ ] Engström et al., *J. Intern. Med.* (2014) — doi: 10.1111/joim.12188
- [ ] Bang et al., *Ann. Intern. Med.* (2009) — doi: 10.7326/0003-4819-151-11-200912010-00005

## 2. Decisions and confirmations only the team can make

- [ ] **Author Contributions** — currently role-based with no names, per your instruction. Before
  final submission the rubric wants named contributions, so someone will need to add names back in
  (or confirm the team wants to submit it anonymized, which may not satisfy that rubric line).
- [ ] **AI-Assisted Work statement** — confirm which AI tools team members actually used beyond
  what I can see in this repo.
- [ ] **Target glucose/diabetes label definition** — still presented as *open* (three candidates).
  Section 5's baseline model uses HbA1c ≥ 6.5% only because it has the largest paired sample with
  CBC, explicitly flagged in the text as exploratory, not a decision.
- [ ] **Final proofread + page-limit check** (see above).

## 3. Submission logistics (can't be done by me)

- [ ] Export the finished Research Plan to PDF and submit to D2L by **Fri, Oct 16, 11:59 PM**.
- [ ] Include the GitHub repo link: `https://github.com/hamidsaeed13/VORTEX-BMEN-600-Project`
- [ ] Decide whether/when to commit, merge `Hamid-midTermProposal` into `main`, and push — I'm not
  doing any of that without you telling me to.

---
*I'll keep this file updated as I continue refining the Research Plan.*
