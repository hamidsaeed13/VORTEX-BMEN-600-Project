# Things only you (or the team) can do

Running list, updated as I keep working on the Midterm Research Plan. Nothing has been committed
or pushed anywhere — it's all local, on branch `Hamid-midTermProposal`.

## 0. Draft is ready — please eyeball it

Updated draft at **[drafts/Midterm_Research_Plan_Draft.docx](drafts/Midterm_Research_Plan_Draft.docx)**,
plus **[code/02_baseline_model_and_figures.ipynb](code/02_baseline_model_and_figures.ipynb)** with
a real, executed baseline model (not a mockup) feeding Section 5.

This pass added a second, independent, adversarial fact-check on top of the first (both documented
in [literature_review/README.md](literature_review/README.md)), plus a code-review pass on both
notebooks specifically for edge cases. What actually got fixed:

**Citations (second verification pass found 8 concrete errors the first pass missed):**
- Wrong volume/year for the Mansoori et al. reference (cited as vol. 12/2022; the PDF's own footer
  says vol. 13, article 663, **2023**) — the most serious one.
- Horton et al.'s publication month was wrong (Apr. → May 2019).
- Dropped the IDF Atlas's own "aged 20–79" qualifier on the 589-million figure — restored.
- A citation ([4], the CDC webpage) was being used but never logged as checked anywhere — logged.
- "A Chinese tertiary hospital" was an invented descriptor for the Guo et al. study — the paper
  never says "tertiary"; corrected to name the actual hospital.
- The word "directly" was added to the Veeranna citation beyond what its title supports — removed.
- The Lorenzo et al. (IRAS) paragraph omitted that paper's actual headline finding (lymphocyte
  count OR 1.96) while only reporting its null results — added back for balance.
- The McDermott et al. arXiv ID wasn't visible in the PDF text, so I independently confirmed it
  directly against arxiv.org (title/authors/date match exactly).

**Code (edge cases found and fixed, not just cosmetic):**
- `code/01_eda_cbc_glucose_demographics.ipynb` had 3 real bugs: a boolean compared with `.notna()`
  that silently always returned the full sample size instead of the valid-response count; a
  `pd.cut` boundary that put participants exactly at the clinical cutoffs (HbA1c 5.7 and 6.5) into
  the wrong category; and a markdown claim ("median X, Y, Z") with no cell actually computing a
  median. All three fixed and the notebook re-executed against the real data — one write-up number
  changed slightly as a result (median WBC by group: 6.5/6.8/7.4, was 6.5/6.9/7.4).
- `code/02_baseline_model_and_figures.ipynb`: NHANES "refused"/"don't know" education codes (7, 9)
  were being fed into the model as if they were real education levels — recoded to missing. Also
  hardened `confusion_matrix` against a label-dropping edge case. This shifted the threshold table
  very slightly (e.g., at the 0.3 threshold: sensitivity 67.6%→68.7%, NPV 95.2%→95.4%) — the Word
  doc's numbers were updated to match exactly.

**Additional graphs — my recommendation: don't add one.** The notebook also produces a correlation
heatmap and a feature-importance bar chart; I did not embed either in the Word doc. Reasoning: body
content is already ~3,240 words plus a table and a figure, and I can't render this machine's output
to confirm the exact page count (no LibreOffice/pandoc installed here) — adding a second image is
the kind of change that could push it over the 6-page cap without me being able to see the result.
Both figures are in the notebook if you want them pulled in — the feature-importance chart would be
the stronger addition since it directly backs an existing sentence in Section 5.

- [ ] **Open the .docx in Word and check the actual page count** (same caveat as before — still
  can't render it here). Tell me if it's over 6 pages and I'll trim, or if there's room and you
  want the feature-importance figure added.
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
