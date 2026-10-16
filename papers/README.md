# Reference verification: Background and Research Question (Ella)

Each reference was checked against the source on 2026-10-16. Page numbers are the printed page numbers in the PDF. Quotes from U.S. government sources (refs 2, 3) are verbatim. For copyrighted sources, short excerpts are paired with page or section pointers so they can be checked in the PDF.

| Ref | Source file in this folder | Citation details | Supports the claim? |
|---|---|---|---|
| [1] IDF Atlas | `ref1_IDF_Diabetes_Atlas_11th_ed_2025.pdf` | Correct | Yes |
| [2] Gwira et al., NCHS DB 516 | `ref2_Gwira_NCHS_DataBrief516_2024.pdf` | Correct (full name is Jane **A.** Gwira) | Yes |
| [3] CDC "A U.S. Report Card" | Web page only (see below) | Correct | Yes |
| [4] Horton et al. 2019 | `ref4_Horton_Top25_Lab_Tests_AJCP2019.pdf` | Correct | Yes |
| [5] Veeranna et al. 2012 | Not included (paywalled, Karger). Abstract checked on PubMed, PMID 22813786 | Correct | Yes, with a wording caveat |
| [6] Mertoglu & Gunay 2017 | `ref6_Mertoglu_NLR_PLR_DiabetesMetabSyndr2017.pdf` | Correct | Yes, with a small-sample caveat |
| [7] English et al. 2015 (new, for red cell turnover) | `ref7_English_Anaemia_HbA1c_Diabetologia2015.pdf` | Correct | Yes |

**Status:** problems 1–4 below are fixed in `drafts/Ella_Background_Draft_Corrected.md`.

---

## Problems to fix in the text

1. **Wrong citation numbers in the sentence "US data from August 2021–August 2023 shows a similar pattern: 15.8% … [3], [4]."**
   Those figures come from **[2]** (NCHS Data Brief 516), not [3] (CDC page) or [4] (Horton).
2. **Wrong citation in "(it is the single most common test at four of five referral hospitals studied [1])".**
   That claim comes from **[4]** (Horton), not [1] (IDF Atlas).
3. **The sentences in problems 1 and 2 repeat the paragraph before them and the next paragraph.** They read like leftover draft notes: the US prevalence is already covered by [2], the CBC-volume point is made with [4] in paragraph 2, and the sentence ends with "signal..". You'll probably want to delete them or merge them into the surrounding text.
4. **"These associations may reflect chronic low-grade inflammation and altered red blood cell turnover."** This sentence has no citation. Mertoglu [6] supports the inflammation part. Neither [5] nor [6] discusses red cell turnover; Veeranna suggests chronic hyperglycemia as the link. Either add a citation for red cell turnover or drop that part. English et al. 2015 (Diabetologia) in `literature_review/papers` on `main` covers how anemia and red cell lifespan affect HbA1c.
5. **Minor wording:** "four in ten were unaware" is accurate. IDF says "just over four in ten (42.8%)" were undiagnosed. "Unaware" and "undiagnosed" are used interchangeably in the Atlas summary (p. 7).

---

## [1] IDF Diabetes Atlas, 11th ed., 2025

| Claim in text | Evidence | Location |
|---|---|---|
| Metabolic disorder with persistently high glucose due to insufficient insulin production or action | Defines diabetes as raised blood glucose because the body "cannot produce enough or any insulin or cannot effectively use the insulin it produces" | p. 13, Ch. 1 |
| 589 million adults aged 20–79 with diabetes in 2024 | "In 2024, it is estimated that 589 million adults aged 20-79 were living with diabetes." | p. 7, Foreword/Summary |
| About four in ten unaware | "just over four in ten (42.8%; 251.7 million)" adults with diabetes were undiagnosed | p. 50, §3.3 Undiagnosed diabetes |
| Can remain undiagnosed for years | Type 2 onset is often asymptomatic, so there is "often a long period before the diabetes is diagnosed" | p. 16, Ch. 1 |
| Early diagnosis can prevent or delay eye, kidney and CV complications | Lists CVD, nephropathy and retinopathy, and says these complications can be delayed or prevented. Section 3.3 says early diagnosis and timely treatment are crucial to prevent complications | p. 13; p. 50 |

## [2] Gwira, Fryar & Gu, NCHS Data Brief No. 516, Nov 2024, doi:10.15620/cdc/165794

Public domain (U.S. government).

| Claim in text | Verbatim evidence | Location |
|---|---|---|
| 15.8% total, 11.3% diagnosed, 4.5% undiagnosed | "The prevalence of total diabetes was 15.8% in all adults. The prevalence of diagnosed and undiagnosed diabetes was 11.3% and 4.5%, respectively" | p. 1–2 |
| "Slightly more than one in four" adults with diabetes undiagnosed | Derived: 4.5 / 15.8 = 28.5%. The brief does not state this ratio itself; it is your calculation, and it is correct | p. 2 |
| Undiagnosed most common in older adults | "The prevalence of undiagnosed diabetes increased from 1.3% in adults ages 20-39 to 5.6% for ages 40-59 and 6.8% for age 60 and older." | p. 2 |
| …and adults with obesity | "The prevalence of undiagnosed diabetes increased from 1.6% in adults in the underweight or normal weight category to 2.8% in those in the overweight category and 7.9% in adults with obesity." | p. 3 |

Note: NCHS defines undiagnosed diabetes as FPG ≥126 mg/dL or HbA1c ≥6.5% with no self-reported diagnosis. That is a stricter cutoff than our ≥5.7% dysglycemia outcome.

## [3] CDC, "A U.S. Report Card"

URL: https://www.cdc.gov/diabetes/communication-resources/diabetes-statistics.html. Page shows "Last updated: February 11, 2026". Checked 2026-10-16. Public domain.

| Claim in text | Verbatim evidence |
|---|---|
| Most adults with prediabetes don't know it | "8 in 10 adults with prediabetes don't know they have it." |
| (context) | "115.2 million American adults—more than 2 in 5—have prediabetes." "More than 1 in 4 adults with diabetes don't know they have it." |

Your citation says "Accessed: Oct. 05, 2026", so the page has not changed since you accessed it.

## [4] Horton et al., Am J Clin Pathol 151(5):446–451, 2019, doi:10.1093/ajcp/aqy165

| Claim in text | Evidence | Location |
|---|---|---|
| CBC is among the most frequently ordered tests | A CBC is the most common test in four of the five hospitals and second most common in the fifth | p. 447, Results ¶1 |

Caveat: the five hospitals are in Kenya, India, Nigeria, Malaysia and the USA (Denver Health). Only one of them is in the U.S.

## [5] Veeranna et al., Cardiology 122(2):129–132, 2012, doi:10.1159/000339225, PMID 22813786

Verified from the PubMed abstract only. The full text is paywalled and not saved here.

- Design: cross-sectional, 15,343 nondiabetic adults without CVD, **NHANES 1999–2008**.
- Finding: RDW correlated with HbA1c (r = 0.27, p < 0.001). Adjusted mean RDW rose from 12.59% (HbA1c ≤4.8%) to 12.92% (HbA1c >5.8%). RDW predicted HbA1c independent of fasting glucose (β = 0.034, 95% CI 0.026–0.042).
- **Supports the claim:** RDW is associated with HbA1c. Strictly, it shows an association with **higher HbA1c across the non-diabetic range**, not with "dysglycemia" as a category. "associated with higher HbA1c" would be the more precise wording. It is also a good fit for our project because it uses NHANES too.

## [6] Mertoglu & Gunay, Diabetes Metab Syndr 11 Suppl 1:S127–S131, Nov 2017, doi:10.1016/j.dsx.2016.12.021

| Claim in text | Evidence | Location |
|---|---|---|
| NLR associated with dysglycemia | Abstract conclusion: NLR is significantly higher in prediabetic and diabetic patients | p. S127, Abstract |
| Inflammation as mechanism | Intro says chronic inflammation plays a key role in the development of diabetes; NLR and PLR are described as markers of subclinical inflammation | p. S127, Abstract & §1 |

Caveats: this is a small, single-centre Turkish study (n = 110: 42 NGT, 25 IGT, 9 newly diagnosed, 34 known diabetes). Groups were defined by OGTT, not HbA1c. PLR moved in different directions at different stages, and MPV showed no difference.

## [7] English et al., Diabetologia 58(7):1409–1421, 2015, doi:10.1007/s00125-015-3599-3

This source was added for the red cell turnover sentence. It is the same paper the team draft cites as [17].

| Claim in text | Evidence | Location |
|---|---|---|
| Altered red cell turnover can shift HbA1c independently of glucose | Altered erythrocyte lifespan, particularly due to anaemia, is named as a key confounder of HbA1c. Haemolytic anaemia shortens lifespan and lowers HbA1c, while iron deficiency anaemia lengthens it and raises HbA1c | p. 1410, Introduction |
| (supporting) | Changes in erythrocyte lifespan can affect HbA1c even when haematological indices are normal | p. 1419, Discussion |
| (supporting) | Iron deficiency raised HbA1c with no matching rise in glucose | p. 1409, Abstract |

Caveat: this is a systematic review of 12 studies, mostly on iron deficiency anaemia. It describes an effect on how HbA1c is measured, not on true glycemia. That supports the argument for including red cell indices, but it also means part of any CBC–HbA1c link may be artifact.
