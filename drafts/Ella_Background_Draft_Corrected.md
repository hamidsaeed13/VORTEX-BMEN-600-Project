# Background and Research Question (Ella), corrected draft

Diabetes mellitus is a metabolic disorder characterized by persistently elevated blood glucose due to insufficient insulin production or action, and it can remain undiagnosed for years [1]. Worldwide, an estimated 589 million adults aged 20–79 years were living with diabetes in 2024, and approximately four in ten were unaware of their condition [1]. In the United States, data from the August 2021–August 2023 cycle of the National Health and Nutrition Examination Survey (NHANES) show that 15.8% of adults aged 20 years and older had diabetes: 11.3% diagnosed and 4.5% undiagnosed. In other words, slightly more than one in four adults with diabetes were undiagnosed [2]. Most adults with prediabetes do not know they have it [3]. Undiagnosed diabetes is most common among older adults and adults with obesity [2]. Early diagnosis allows timely lifestyle changes and treatment, which can prevent or delay complications affecting the eyes, kidneys, and cardiovascular system [1].

Part of the problem is that detection depends on a clinician ordering an appropriate glycemic test, such as hemoglobin A1c (HbA1c) or fasting plasma glucose. By contrast, the complete blood count (CBC) is among the most frequently ordered laboratory tests; in a comparison of five referral hospitals, it was the most common test by volume at four of them [4]. Several CBC-derived indices, including red cell distribution width [5] and the neutrophil-to-lymphocyte ratio [6], have been associated with dysglycemia. These associations may reflect chronic low-grade inflammation [6] and altered red blood cell turnover, since changes in red cell lifespan can shift HbA1c independently of blood glucose [7]. If routinely collected CBC values carry predictive information, they could support a decision-support tool that interprets CBC results alongside demographic information to guide subsequent glycemic testing. Such a tool could prioritize testing for patients at high predicted risk and potentially reduce unnecessary testing for those at very low risk. Because a missed case leaves disease undetected while a false positive leads to additional testing and follow-up, such a tool must reliably identify true cases while limiting unnecessary investigation.

This project therefore asks: In U.S. adults without a prior diabetes diagnosis, does adding CBC indices to age and sex improve the prediction of dysglycemia, defined as an HbA1c of 5.7% or higher (the prediabetes or diabetes range), in NHANES August 2021–August 2023?

NHANES provides CBC, HbA1c, demographic, and self-reported diagnosis data for the same participants, making the project feasible within the term. We will compare models using age and sex alone with models that also include CBC measurements, then evaluate their predictions on participants whose data were not used for training. The expected contribution is an estimate of how much CBC information improves these predictions, with emphasis on identifying true cases while limiting unnecessary follow-up, together with an openly shared, reproducible analysis pipeline. These findings could inform a proposed testing pathway, but demonstrating clinical benefit would require further validation.

## References

[1] International Diabetes Federation, *IDF Diabetes Atlas*, 11th ed. Brussels, Belgium: International Diabetes Federation, 2025. Accessed: Oct. 05, 2026. [Online]. Available: https://diabetesatlas.org

[2] J. A. Gwira, C. D. Fryar, and Q. Gu, "Prevalence of total, diagnosed, and undiagnosed diabetes in adults: United States, August 2021–August 2023," National Center for Health Statistics, Hyattsville, MD, NCHS Data Brief 516, Nov. 2024. doi: 10.15620/cdc/165794.

[3] CDC, "A U.S. Report Card," Diabetes. Accessed: Oct. 05, 2026. [Online]. Available: https://www.cdc.gov/diabetes/communication-resources/diabetes-statistics.html

[4] S. Horton et al., "The Top 25 Laboratory Tests by Volume and Revenue in Five Different Countries," *Am. J. Clin. Pathol.*, vol. 151, no. 5, pp. 446–451, Apr. 2019, doi: 10.1093/ajcp/aqy165.

[5] V. Veeranna, S. K. Zalawadiya, S. S. Panaich, K. Ramesh, and L. Afonso, "The Association of Red Cell Distribution Width with Glycated Hemoglobin among Healthy Adults without Diabetes Mellitus," *Cardiology*, vol. 122, no. 2, pp. 129–132, 2012, doi: 10.1159/000339225.

[6] C. Mertoglu and M. Gunay, "Neutrophil-Lymphocyte ratio and Platelet-Lymphocyte ratio as useful predictive markers of prediabetes and diabetes mellitus," *Diabetes Metab. Syndr.*, vol. 11 Suppl 1, pp. S127–S131, Nov. 2017, doi: 10.1016/j.dsx.2016.12.021.

[7] E. English, I. Idris, G. Smith, K. Dhatariya, E. S. Kilpatrick, and W. G. John, "The effect of anaemia and abnormalities of erythrocyte indices on HbA1c analysis: A systematic review," *Diabetologia*, vol. 58, no. 7, pp. 1409–1421, Jul. 2015, doi: 10.1007/s00125-015-3599-3.

---

## What changed from your version

1. **US prevalence sentence:** the citation was "[3], [4]" and is now **[2]** (NCHS Data Brief 516 is where 15.8% / 11.3% / 4.5% come from). The figures are merged into your existing NHANES sentence, so they are stated once.
2. **CBC volume claim:** the citation was **[1]** and is now **[4]** (Horton et al., p. 447). It moved into paragraph 2, where the CBC point is already made. The leftover phrase "motivates looking for a CBC-based signal.." was removed.
3. **Red cell turnover:** this was uncited. **[7] English et al. 2015** now supports it, the same source the team draft cites as [17]. It states that altered erythrocyte lifespan is a confounder of HbA1c (p. 1410) and that lifespan changes can affect HbA1c even with normal indices (p. 1419). [6] is also attached to the inflammation part.
4. **First sentence:** added [1]. IDF Atlas pp. 13 and 16 support both the definition and the "undiagnosed for years" point.
5. **Reference [2] authors:** now in IEEE initials format (J. A. Gwira, C. D. Fryar, Q. Gu), matching the other references.

**Optional, not applied:** Veeranna [5] shows red cell distribution width rising with HbA1c in adults *without* diabetes. "associated with higher HbA1c" would be slightly more precise than "associated with dysglycemia".

**Heads-up for the merged document:** in the team draft, English et al. is reference [17]. When your section is combined with the others, renumber [7] to match.
