# Literature Review Summary

This file summarizes the literature supporting our research question. Full text is in Sections 1–2 of the Midterm Research Plan.

## Research question
In U.S. adults without a prior diabetes diagnosis, does adding CBC indices to age and sex improve the prediction of dysglycemia (HbA1c ≥ 5.7%) in NHANES August 2021–August 2023?

## Key evidence

| Theme | Source | Main finding | DOI |
|---|---|---|---|
| Burden | IDF Diabetes Atlas (2025) | ~589 million adults with diabetes; ~4 in 10 unaware | — |
| Burden | Gwira et al. (2024) | >1 in 4 U.S. adults with diabetes undiagnosed (NHANES 2021–2023) | 10.15620/cdc/165794 |
| CBC use | Horton et al. (2019) | CBC is among the most frequently ordered lab tests | 10.1093/ajcp/aqy165 |
| Risk scores | Bang et al. (2009) | NHANES questionnaire score identifies adults to screen | 10.7326/0003-4819-151-11-200912010-00005 |
| ML detection | Liu et al. (2025) | AutoML detected undiagnosed diabetes (AUROC 0.909) using mainly self-reported data | 10.2196/68260 |
| White cells | Gkrania-Klotsas et al. (2010) | Higher white-cell counts associated with type 2 diabetes | 10.1371/journal.pone.0013405 |
| NLR | Mertoglu & Gunay (2017) | NLR elevated in prediabetes and diabetes (cross-sectional) | 10.1016/j.dsx.2016.12.021 |
| NLR | Lorenzo et al. (2014) | NLR not associated with incident diabetes (prospective) | 10.1007/s00125-013-3080-0 |
| RDW | Veeranna et al. (2012) | RDW positively associated with HbA1c in nondiabetic NHANES adults | 10.1159/000339225 |
| RDW | Engström et al. (2014) | RDW linked to higher HbA1c but lower glucose and lower future diabetes risk | 10.1111/joim.12188 |
| CBC prediction | Guo et al. (2026) | CBC-based model predicted HbA1c ≥ 5.7% (AUROC 0.791) | 10.1038/s41598-026-59213-3 |
| HbA1c validity | English et al. (2015) | Anemia and erythrocyte abnormalities affect HbA1c independently of glucose | 10.1007/s00125-015-3599-3 |

## Research gap
Prior work shows CBC indices relate to glycemic status, but it remains unclear:
1. whether CBC-based prediction generalizes to a nationally representative population,
2. how much the CBC adds beyond age and sex alone, and
3. how such a model performs at the high sensitivity needed for safe use in undiagnosed adults.

## Planned checks
- Exclude anemic participants (sensitivity analysis)
- Repeat analysis at HbA1c ≥ 6.5% (diabetes only)
