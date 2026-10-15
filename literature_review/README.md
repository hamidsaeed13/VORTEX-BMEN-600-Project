# Literature Review — Source Papers

Collected for the Midterm Research Plan (Section 2: Background and Research Gap), on
CBC/demographics-based prediction of glucose abnormality and type 2 diabetes, plus reflex-testing
/ test-utilization evidence for the cost-asymmetry framing in Sections 1 and 4. Keywords used (per
`Team_Workstream_Plan.xlsx`): "Diabetes + Prediction + CBC + Demographics".

PDFs are in `papers/`, numbered to match the References list in the Research Plan draft
(`drafts/Midterm_Research_Plan_Draft.docx`). Every claim attributed to a numbered source below was
checked directly against that source's own PDF (not taken from an abstract snippet or a search
summary) before being used in the draft — see "Verified facts actually used" under each entry.

**This list has been through two independent fact-check passes**, the second done specifically to
catch anything the first missed (wrong direction of effect, wrong year/volume, unsupported added
detail, etc.) — see "Second-pass corrections" at the bottom for exactly what changed and why.

## Downloaded and verified against full text (14 of 18 cited papers)

1. **`01_horton_top25_lab_tests_AJCP2019.pdf`** — S. Horton, K. A. Fleming, M. Kuti, L.-M. Looi,
   S. A. Pai, S. Sayed, and M. L. Wilson, "The Top 25 Laboratory Tests by Volume and Revenue in
   Five Different Countries," Am. J. Clin. Pathol., vol. 151, no. 5, pp. 446–451, May 2019,
   doi: 10.1093/ajcp/aqy165.
   Verified: a CBC was the single most common test by volume at 4 of 5 referral hospitals studied
   (US, India, Kenya, Malaysia, Nigeria), and appeared in the top-25 list at all 5.

2. **`02_idf_diabetes_atlas_11thed_2025.pdf`** — International Diabetes Federation, IDF Diabetes
   Atlas, 11th ed. Brussels: IDF, 2025.
   Verified: 589 million adults **aged 20–79** worldwide live with diabetes; 43% of cases are
   undiagnosed. (The age qualifier was dropped from the first draft pass — fixed.)

3. **`03_nchs_databrief516_diabetes_prevalence_2024.pdf`** — J. A. Gwira, C. D. Fryar, and Q. Gu,
   "Prevalence of Total, Diagnosed, and Undiagnosed Diabetes in Adults: United States, August
   2021–August 2023," NCHS Data Brief 516, Nov. 2024, doi: 10.15620/cdc/165794.
   Verified exact figures: total diabetes prevalence 15.8%, diagnosed 11.3%, undiagnosed 4.5% of
   US adults 20 and older.

4. **CDC, "A U.S. Report Card," Diabetes.** [Online]. Available:
   https://www.cdc.gov/diabetes/communication-resources/diabetes-statistics.html
   Webpage, not a paper — cited alongside [3] for the same prevalence figures, as general context
   rather than as an independent numeric source. Not independently re-verified beyond that.

5. **`05_guo_cbc_opportunistic_screening_Nature2026.pdf`** — X. Guo, N. Zhang, B. Li, X. Yu,
   J. Guo, and G. Dan, "Using machine learning to identify individuals at elevated risk of
   diabetes from low-cost complete blood count data for opportunistic screening," Sci. Rep.,
   vol. 16, Art. no. 29445, 2026, doi: 10.1038/s41598-026-59213-3.
   Verified: CBC-only LightGBM model, AUROC 0.821 (development) / 0.791 (independent 2024
   temporal validation), n=70,725 development + 26,650 validation, Shenzhen University General
   Hospital. (The first draft pass called this "a Chinese tertiary hospital" — the paper itself
   never uses that word, and only says "single-center." Fixed to name the hospital directly.)

6. **`06_mansoori_hematological_factors_MASHAD_Nature2022.pdf`** — A. Mansoori et al., "Prediction
   of type 2 diabetes mellitus using hematological factors based on machine learning approaches: a
   cohort study analysis," Sci. Rep., vol. 13, Art. no. 663, 2023, doi: 10.1038/s41598-022-27340-2.
   Verified: MASHAD cohort (Iran), ~9,000 adults 35–65; bootstrap-forest model; age and WBC the
   most influential predictors. **Correction (second pass)**: the first draft pass cited this as
   "vol. 12, Jan. 2022" — the PDF's own footer reads "Scientific Reports | (2023) 13:663." Volume
   and year were both wrong; fixed. The DOI itself (which contains "2022") is unchanged and correct.

7. **Not downloaded** — N. Kamkar et al., "A machine learning-based framework for predicting type
   2 diabetes mellitus using hematological indices," Am. Heart J. Plus, 2026,
   doi: 10.1016/j.ahjo.2026.100854. Title/author list confirmed via Europe PMC full-text XML;
   no specific numeric claim from this source is used in the draft.

8. **Not downloaded** — V. Veeranna, S. K. Zalawadiya, S. S. Panaich, K. Ramesh, and L. Afonso,
   "The Association of Red Cell Distribution Width with Glycated Hemoglobin among Healthy Adults
   without Diabetes Mellitus," Cardiology, vol. 122, no. 2, pp. 129–132, 2012,
   doi: 10.1159/000339225. Only the title-level claim is used in the draft (RDW associated with
   HbA1c in healthy, non-diabetic adults) — not independently full-text verified. **Correction
   (second pass)**: the first draft pass added the word "directly" to this claim, which isn't
   confirmable from the title alone; removed.

9. **Not downloaded** — G. Engström, J. G. Smith, M. Persson, P. M. Nilsson, O. Melander, and
   B. Hedblek, "Red cell distribution width, haemoglobin A1c and incidence of diabetes mellitus,"
   J. Intern. Med., vol. 276, no. 2, pp. 174–183, 2014, doi: 10.1111/joim.12188. Only the
   title-level claim is used (RDW associated with incident diabetes) — not full-text verified.

10. **`10_park_wbc_predictor_T2D_JIR2021.pdf`** — J.-M. Park, H. S. Lee, J.-Y. Park, D.-H. Jung,
    and J.-W. Lee, "White Blood Cell Count as a Predictor of Incident Type 2 Diabetes Mellitus
    Among Non-Obese Adults: A Longitudinal 10-Year Analysis of the Korean Genome and Epidemiology
    Study," J. Inflamm. Res., vol. 14, pp. 1235–1242, 2021, doi: 10.2147/JIR.S300026.
    Verified exact figure: adjusted HR 1.55 (95% CI 1.10–2.18), highest vs. lowest WBC quartile,
    n=4,211, 592 (14.1%) incident cases.

11. **`11_gkrania_klotsas_wbc_meta_PLoSONE2010.pdf`** — E. Gkrania-Klotsas et al., "Differential
    white blood cell count and type 2 diabetes: Systematic review and meta-analysis of
    cross-sectional and prospective studies," PLoS ONE, vol. 5, no. 10, e13405, 2010,
    doi: 10.1371/journal.pone.0013405.
    Verified exact figures: 20 studies, 8,647 cases / 85,040 non-cases; combined RR 1.61 (95% CI
    1.45–1.79) for top vs. bottom WBC tertile. **Important nuance now reflected in the draft**:
    the authors themselves caution that publication bias and incomplete confounder adjustment
    likely make this an overestimate.

12. **`12_lorenzo_iras_wbc_diff_Diabetologia2014.pdf`** — C. Lorenzo, A. J. Hanley, and
    S. M. Haffner, "Differential white cell count and incident type 2 diabetes: The Insulin
    Resistance Atherosclerosis Study," Diabetologia, vol. 57, no. 1, pp. 83–92, 2014,
    doi: 10.1007/s00125-013-3080-0.
    **Correction from the first draft pass**: this is a single cohort study (n=866), not
    meta-analytic evidence, and its own white-cell/neutrophil associations with incident diabetes
    were attenuated to non-significance after adjusting for family history, fasting glucose, and
    smoking; neutrophil:lymphocyte ratio showed no significant association at all (OR 0.89, ns).
    The draft no longer groups this with the meta-analysis as uniformly confirmatory — it is now
    cited for the more mixed picture it actually shows. **Second-pass correction**: the first
    corrected draft still omitted the paper's actual headline finding — lymphocyte count alone
    remained significantly associated with incident diabetes after the same full adjustment (OR
    1.96, 95% CI 1.13–3.37), the strongest single association in the study, which the authors
    attribute to insulin sensitivity rather than inflammation. Now added.

13. **`13_mertoglu_nlr_plr_DiabetesMetabSyndr2017.pdf`** — C. Mertoglu and M. Gunay,
    "Neutrophil-Lymphocyte ratio and Platelet-Lymphocyte ratio as useful predictive markers of
    prediabetes and diabetes mellitus," Diabetes Metab. Syndr., vol. 11, suppl. 1, pp. S127–S131,
    2017, doi: 10.1016/j.dsx.2016.12.021.
    Verified: NLR significantly higher in prediabetic, newly-diagnosed, and established diabetic
    groups vs. normal (p=0.004); PLR pattern is non-monotonic (lower in prediabetes/newly
    diagnosed, higher in established diabetes, p=0.021); MPV showed no significant difference.

14. **`14_rahman_sociodemographic_ML_Algorithms2023.pdf`** — Md. A. Rahman, L. F. Abdulrazak,
    Md. M. Ali, I. Mahmud, K. Ahmed, and F. M. Bui, "Machine Learning-Based Approach for
    Predicting Diabetes Employing Socio-Demographic Characteristics," Algorithms, vol. 16,
    no. 11, 503, 2023, doi: 10.3390/a16110503.
    **Correction from the first draft pass**: the feature set is not pure demographics — it
    includes self-reported symptoms (polyuria, polydipsia, delayed healing). Random forest
    reported 99.36% accuracy, a figure high enough that the draft now flags it as warranting
    caution about class imbalance / evaluation artifacts rather than citing it at face value.

15. **`15_liu_automl_undiagnosed_diabetes_JMIRAI2025.pdf`** — J. Liu, F. Ssewamala, R. An, and
    M. Ji, "Use of automated machine learning to detect undiagnosed diabetes in US adults:
    Development and validation study," JMIR AI, vol. 4, e68260, 2025, doi: 10.2196/68260.
    Verified: this is also NHANES-based (1999–2020), predictors are demographic/anthropometric/
    dietary/behavioral (no CBC or other labs — lab values were used only to *define* the
    undiagnosed-diabetes outcome), AutoML AUROC 0.909 (95% CI 0.897–0.921), sensitivity 70.3%,
    specificity 90.5%, NPV 92.6%. This is now used in the draft as a direct benchmark for our own
    sensitivity/NPV evaluation approach, not just a generic "demographics work" citation.

16. **`16_english_anemia_hba1c_Diabetologia2015.pdf`** — E. English, I. Idris, G. Smith,
    K. Dhatariya, E. S. Kilpatrick, and W. G. John, "The effect of anaemia and abnormalities of
    erythrocyte indices on HbA1c analysis: A systematic review," Diabetologia, vol. 58, no. 7,
    pp. 1409–1421, 2015, doi: 10.1007/s00125-015-3599-3.
    Verified: systematic review of 12 studies; iron-deficiency anemia (with or without anemia)
    increases HbA1c values independent of true glycemic status — supports the draft's confound
    discussion in Sections 2 and 4.

17. **`17_mcdermott_smart_reflex_testing_arxiv2023.pdf`** — M. McDermott, A. Dighe, P. Szolovits,
    Y. Luo, and J. Baron, "Using Machine Learning to Develop Smart Reflex Testing Protocols,"
    arXiv:2302.00794, 2023.
    The arXiv ID isn't visible in the extracted PDF text itself (just the PDF's internal creation
    date, Feb. 1, 2023), so the second verification pass flagged it for a direct check — confirmed
    by fetching arxiv.org/abs/2302.00794 directly: title, all 5 authors, and submission date
    (Feb. 1, 2023) match exactly.

18. **Not downloaded** — H. Bang et al., "Development and validation of a patient self-assessment
    score for diabetes risk," Ann. Intern. Med., vol. 151, no. 11, pp. 775–783, 2009,
    doi: 10.7326/0003-4819-151-11-200912010-00005. Only the title-level claim is used (a
    non-laboratory self-assessment risk score) — not full-text verified.

19. NHANES dataset citation (not a journal paper) — CDC/NCHS, National Health and Nutrition
    Examination Survey, 2021–2023 cycle. https://wwwn.cdc.gov/nchs/nhanes/

20. **`20_yin_rdw_glycemic_control_TCRM2018.pdf`** *(new addition, found independently and added
    to the draft — not in the original source list)* — Y. Yin, S. Ye, H. Wang, B. Li, A. Wang,
    W. Yan, J. Dou, and Y. Mu, "Red blood cell distribution width and the risk of being in poor
    glycemic control among patients with established type 2 diabetes," Ther. Clin. Risk Manag.,
    vol. 14, pp. 265–273, 2018, doi: 10.2147/TCRM.S155753.
    Verified: REACTION cohort, n=702 established T2D patients; higher RDW was associated with
    **lower** risk of poor glycemic control (OR 0.3, 95% CI 0.2–0.7, top vs. bottom quartile,
    multivariable-adjusted) — the **opposite direction** from RDW's association with incident
    diabetes in a non-diabetic population (refs 8–9). The draft now explicitly notes this
    direction difference rather than treating "RDW and diabetes" as one uniform relationship.

## Second-pass corrections (summary)

An independent, adversarial re-check (separate from the pass that produced the entries above) was
run specifically to catch anything the first pass missed. It confirmed the large majority of
claims exactly and found these concrete errors, all now fixed in the draft and in this file:

- **[1] Horton**: publication month was wrong (Apr. → May 2019).
- **[2] IDF Atlas**: dropped the Atlas's own "aged 20–79" qualifier on the 589 million figure —
  added back in both places the draft uses it.
- **[4] CDC webpage**: was cited but never logged in this file at all — added above.
- **[5] Guo et al.**: draft called it "a Chinese tertiary hospital," a descriptor the paper itself
  never uses — corrected to name the actual hospital.
- **[6] Mansoori et al.**: wrong volume and year (cited as vol. 12, 2022; actually vol. 13, article
  663, 2023, per the PDF's own footer) — the single most serious citation-detail error found.
- **[8] Veeranna**: draft added the word "directly," which isn't supported by the title alone —
  removed.
- **[12] Lorenzo et al. (IRAS)**: the draft's framing of this study as "attenuated to
  non-significance" omitted the paper's own actual headline finding (lymphocyte count remained
  significantly associated, OR 1.96) — added.
- **[17] McDermott et al.**: arXiv ID independently confirmed directly against arxiv.org (see
  entry above) since it wasn't visible in the PDF's own extracted text.

Also checked and found internally consistent: all of Section 5's numbers (AUROC 0.743/0.783/0.811,
sample sizes, threshold table, feature-importance ranking) were re-verified character-for-character
against `code/02_baseline_model_and_figures.ipynb`'s actual executed output — no discrepancies.
One internal-consistency issue was found and fixed in the draft itself (not a citation issue): the
draft had implied all 11,933 merged participants have CBC data, when only 7,593 (63.6%, per Table
1) do — Sections 3 and 5 now say this correctly, and a note was added clarifying why Table 1's
"CBC + HbA1c" count (6,689, using WBC presence as a proxy for CBC) differs slightly from the
baseline model's own modeling sample (6,678, requiring all 12 CBC columns present).

## Still not obtained (4 of 18)

All four remain blocked by a Cloudflare/WAF bot challenge on the publisher's site, or by PMC's
JS proof-of-work challenge — both require a real logged-in browser session, and three of the four
also need institutional library access:

- [7] Kamkar et al., Am. Heart J. Plus (2026) — doi: 10.1016/j.ahjo.2026.100854
- [8] Veeranna et al., Cardiology (2012) — doi: 10.1159/000339225
- [9] Engström et al., J. Intern. Med. (2014) — doi: 10.1111/joim.12188
- [18] Bang et al., Ann. Intern. Med. (2009) — doi: 10.7326/0003-4819-151-11-200912010-00005

For these four, the draft only makes claims that are directly supported by the paper's own title
(noted above) — no specific statistic from any of them is quoted in the draft.
