# Literature Review — Source Papers

Collected for the Midterm Research Plan (Section 2: Background and Research Gap), on
CBC/demographics-based prediction of diabetes-range HbA1c, plus reflex-testing evidence for
Sections 1 and 4. Keywords used (per `Team_Workstream_Plan.xlsx`): "Diabetes + Prediction + CBC +
Demographics".

PDFs are in `papers/`, numbered to match the References list in the current Research Plan draft
(`drafts/Midterm_Research_Plan_Draft.docx`). **This numbering changed from an earlier draft** — an
independent outside audit (`reports/Midterm_Research_Plan_Verification_Report.md`) found the
references were cited out of IEEE first-use order (ref [20], Yin et al., was used before ref
[10]). Fixed by renumbering: Yin moved from 20 → 10, and everything that was 10–19 shifted up by
one to 11–20. File names in `papers/` were renamed to match.

This list has now been through **three rounds of fact-checking**: an initial pass, an independent
adversarial re-check, and a third external audit (the report above) that re-derived several claims
from scratch and caught real errors the first two missed. All three rounds' corrections are
reflected below.

## Downloaded and verified against full text (15 of 18 cited papers)

1. **`01_horton_top25_lab_tests_AJCP2019.pdf`** — S. Horton et al., "The Top 25 Laboratory Tests by
   Volume and Revenue in Five Different Countries," Am. J. Clin. Pathol., vol. 151, no. 5,
   pp. 446–451, May 2019, doi: 10.1093/ajcp/aqy165.
   Verified: CBC is the single most common test by volume at 4 of 5 referral hospitals studied,
   and appears in the top-25 list at all 5. **Third-pass correction**: the draft previously called
   blood glucose "a costlier add-on test" than CBC, citing this paper. That is backwards — this
   paper's own Table 3 shows CBC (hematology) costs 1.33–6.67× *more* than glucose (biochemistry)
   across its five hospitals. The draft no longer makes a cost-direction claim from this source.

2. **`02_idf_diabetes_atlas_11thed_2025.pdf`** — International Diabetes Federation, IDF Diabetes
   Atlas, 11th ed. Brussels: IDF, 2025.
   Verified: 589 million adults aged 20–79 worldwide live with diabetes; 43% of cases undiagnosed.

3. **`03_nchs_databrief516_diabetes_prevalence_2024.pdf`** — J. A. Gwira, C. D. Fryar, and Q. Gu,
   NCHS Data Brief 516, Nov. 2024, doi: 10.15620/cdc/165794.
   Verified: total diabetes prevalence 15.8%, diagnosed 11.3%, undiagnosed 4.5%, US adults 20+.

4. **CDC, "A U.S. Report Card," Diabetes** (webpage, not a paper). Cited alongside [3] for the
   same prevalence figures as general context; not an independent numeric source.

5. **`05_guo_cbc_opportunistic_screening_Nature2026.pdf`** — X. Guo, N. Zhang, B. Li, X. Yu,
   J. Guo, and G. Dan, Sci. Rep., vol. 16, Art. no. 29445, 2026, doi: 10.1038/s41598-026-59213-3.
   Verified: AUROC 0.821 (development) / 0.791 (temporal validation), n=70,725 / 26,650, Shenzhen
   University General Hospital. **Third-pass correction (significant)**: the draft previously said
   this model used "CBC parameters alone." It did not — per the paper's own "Predictor set"
   section: "Age, BMI, sex, NLR, and PLR were included as key predictors" alongside CBC. The label
   is HbA1c ≥5.7% (including prediabetes), not ≥6.5%. Both are now stated correctly.

6. **`06_mansoori_hematological_factors_MASHAD_Nature2022.pdf`** — A. Mansoori et al., Sci. Rep.,
   vol. 13, Art. no. 663, 2023, doi: 10.1038/s41598-022-27340-2 (footer confirms vol. 13/2023, not
   the vol. 12/2022 in an earlier draft pass). Bootstrap-forest model; age and WBC most influential.
   **Note**: the abstract's "~9,000 adults" is an approximation — the paper's methods state 9,704
   were actually enrolled.

7. **`07_kamkar_hematological_framework_AmHeartJPlus2026_fulltext.txt`** — N. Kamkar, S. Behzadi,
   V. Mahdavizadeh, M. Maali Tafti, A. Mansoori, M. Poudineh, H. Esmaily, and M. Ghayour-Mobarhan,
   Am. Heart J. Plus, 2026, doi: 10.1016/j.ahjo.2026.100854.
   **Status change**: previously listed as "not obtained" — PMC's bot challenge is intermittent,
   not permanent, and full text was retrieved on a retry. Verified: Random Forest best model,
   ROC-AUC 0.73, 223/347 incident T2DM cases identified; at a 0.20 probability threshold,
   sensitivity 61.8%, specificity 70.7%, PPV 32.7%, NPV 88.9%, in adults free of diabetes at
   baseline (incident-disease prediction, not our mixed known/unknown cohort). Predictors include
   RBC, WBC, RDW, NLR plus clinical variables (metabolic syndrome, BMI, uric acid, age) — not CBC
   indices alone. This is now cited in the draft as a real precedent for a sensitivity/NPV
   operating point, correcting an earlier overstatement that no cited study reported one.

8. **Not downloaded** — V. Veeranna et al., Cardiology, vol. 122, no. 2, pp. 129–132, 2012,
   doi: 10.1159/000339225. Only the title-level claim is used (RDW associated with HbA1c in
   healthy, non-diabetic adults) — not independently full-text verified.

9. **Not downloaded** (abstract-level only) — G. Engström, J. G. Smith, M. Persson, P. M. Nilsson,
   O. Melander, and B. Hedblad, J. Intern. Med., vol. 276, no. 2, pp. 174–183, 2014,
   doi: 10.1111/joim.12188. **Third-pass correction (significant)**: an earlier draft pass assumed
   this paper showed *higher* RDW predicting incident diabetes — the opposite of the true finding.
   Checked against the paper's PubMed abstract: RDW is positively associated with HbA1c, but it is
   *lower* RDW that predicts incident diabetes in this cohort. (Also: a co-author's name was
   misspelled "Hedblek" in an earlier version of this file — corrected to Hedblad, matching the
   Word-doc reference list, which had it right.)

10. **`10_yin_rdw_glycemic_control_TCRM2018.pdf`** — Y. Yin, S. Ye, H. Wang, B. Li, A. Wang,
    W. Yan, J. Dou, and Y. Mu, Ther. Clin. Risk Manag., vol. 14, pp. 265–273, 2018,
    doi: 10.2147/TCRM.S155753. REACTION cohort, n=702 established T2D patients; higher RDW
    associated with *lower* risk of poor glycemic control (OR 0.3, 95% CI 0.2–0.7, Model 2; the
    most-adjusted model gives CI 0.2–0.6). Renumbered from [20] to [10] (see note above).

11. **`11_park_wbc_predictor_T2D_JIR2021.pdf`** — J.-M. Park et al., J. Inflamm. Res., vol. 14,
    pp. 1235–1242, 2021, doi: 10.2147/JIR.S300026. Verified: adjusted HR 1.55 (95% CI 1.10–2.18),
    highest vs. lowest WBC quartile, n=4,211, 592 (14.1%) incident cases.

12. **`12_gkrania_klotsas_wbc_meta_PLoSONE2010.pdf`** — E. Gkrania-Klotsas et al., PLoS ONE,
    vol. 5, no. 10, e13405, 2010, doi: 10.1371/journal.pone.0013405. Verified: 20 studies, 8,647
    cases / 85,040 non-cases, combined RR 1.61 (95% CI 1.45–1.79), top vs. bottom WBC tertile,
    pooling cross-sectional and prospective evidence (the prospective-only estimate alone is 1.48,
    95% CI 1.22–1.79 — the draft does not claim this is incident-only). Authors' own caution about
    publication bias is reflected in the draft.

13. **`13_lorenzo_iras_wbc_diff_Diabetologia2014.pdf`** — C. Lorenzo, A. J. Hanley, and
    S. M. Haffner, Diabetologia, vol. 57, no. 1, pp. 83–92, 2014, doi: 10.1007/s00125-013-3080-0.
    n=866; white-cell and neutrophil associations attenuated to non-significance after full
    adjustment; neutrophil:lymphocyte ratio not significant (OR 0.89, ns); lymphocyte count alone
    stayed significant (OR 1.96, 95% CI 1.13–3.37) — described as a possible partial explanation
    via insulin sensitivity, not an established causal mechanism.

14. **`14_mertoglu_nlr_plr_DiabetesMetabSyndr2017.pdf`** — C. Mertoglu and M. Gunay, Diabetes
    Metab. Syndr., vol. 11, suppl. 1, pp. S127–S131, 2017, doi: 10.1016/j.dsx.2016.12.021.
    Verified: NLR significantly higher across prediabetes/diabetes (p=0.004); PLR non-monotonic
    (p=0.021); MPV not significant. This is a small cross-sectional comparison, not prospective
    validation of a screening policy.

15. **`15_rahman_sociodemographic_ML_Algorithms2023.pdf`** — Md. A. Rahman et al., Algorithms,
    vol. 16, no. 11, 503, 2023, doi: 10.3390/a16110503. Feature set is socio-demographic plus
    self-reported symptoms (polyuria, polydipsia, delayed healing, etc.), not pure demographics.
    Abstract reports 99.36% accuracy (a table elsewhere in the paper reports 99.37%; cross-validated
    accuracies are lower) — the draft flags this headline number as warranting caution rather than
    citing it at face value.

16. **`16_liu_automl_undiagnosed_diabetes_JMIRAI2025.pdf`** — J. Liu, F. Ssewamala, R. An, and
    M. Ji, JMIR AI, vol. 4, e68260, 2025, doi: 10.2196/68260. NHANES-based (1999–2020), predictors
    demographic/anthropometric/dietary/behavioral (no CBC — labs only defined the outcome), AUROC
    0.909, sensitivity 70.3%, NPV 92.6%. **Third-pass correction**: this is useful context, not a
    strict benchmark — it uses an earlier NHANES cycle, adults with no prior diabetes, a combined
    HbA1c/fasting-glucose/OGTT endpoint, and a 19.1% analytic prevalence vs. our 10.7%, and it
    selects its threshold by test-set F1 (not a practice to copy). The draft now says this
    explicitly instead of presenting it as directly comparable.

17. **`17_english_anemia_hba1c_Diabetologia2015.pdf`** — E. English et al., Diabetologia, vol. 58,
    no. 7, pp. 1409–1421, 2015, doi: 10.1007/s00125-015-3599-3. 12-study review: iron-deficiency
    anemia raises HbA1c independent of true glycemic status. (Also found, not yet in the draft: a
    different anemia type is associated with a *decrease* in HbA1c — the effect is not one-directional
    across all anemia types.)

18. **`18_mcdermott_smart_reflex_testing_arxiv2023.pdf`** — M. McDermott et al., arXiv:2302.00794,
    2023. Confirmed directly against arxiv.org (title/authors/date match exactly). **Third-pass
    correction**: this is a feasibility preprint specifically about ferritin test ordering, and it
    discusses its own limitations; the draft no longer cites it as establishing clinical safety for
    reflex testing generally, only feasibility.

19. **Not downloaded** — H. Bang et al., Ann. Intern. Med., vol. 151, no. 11, pp. 775–783, 2009,
    doi: 10.7326/0003-4819-151-11-200912010-00005. Metadata and abstract verified; full text
    blocked by a Cloudflare challenge on ACP's site. This is a risk-score development/validation
    study, not a trial proving safe test reduction — the draft's language reflects that.

20. NHANES dataset citation (not a journal paper) — CDC/NCHS, 2021–2023 cycle.
    https://wwwn.cdc.gov/nchs/nhanes/

## Still not obtained in full text (3 of 18)

- [8] Veeranna et al., *Cardiology* (2012) — doi: 10.1159/000339225
- [9] Engström et al., *J. Intern. Med.* (2014) — doi: 10.1111/joim.12188 (abstract obtained, full
  text not)
- [19] Bang et al., *Ann. Intern. Med.* (2009) — doi: 10.7326/0003-4819-151-11-200912010-00005

All blocked by a Cloudflare/WAF challenge on the publisher's site; [8] and [19] also need
institutional library access. The draft only makes claims these sources' titles or abstracts
directly support.

## What the third-pass audit changed beyond citations

The external audit in `reports/Midterm_Research_Plan_Verification_Report.md` also found and the
draft now reflects: the modeling cohort mixes known and undiagnosed diabetes (565 of 717 positive
labels, 78.8%, already have a prior diagnosis); the title/question previously promised blood
glucose prediction while the implemented model actually predicts HbA1c (the title and question are
now about diabetes-range HbA1c, with glucose as a secondary check); high NPV was being presented
as evidence of safe test deferral without reporting how many true positives are missed at the same
threshold (now reported together); and some "measured" counts in Table 1 include NHANES records
with a zero fasting-sample weight that are not actually eligible for the fasting-glucose analysis
(now flagged with a note). See the audit report itself for the complete technical findings,
including several items correctly scoped as final-project work rather than midterm blockers
(survey weighting, categorical encoding, calibration, cross-validation).
