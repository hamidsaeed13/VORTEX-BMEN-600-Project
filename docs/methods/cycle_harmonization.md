# Cycle harmonization and eligibility audit

The extension develops in August 2021–August 2023 and evaluates in 2017–2018. These are
nonoverlapping participants, checked by SEQN. This is backwards-in-time independent-cycle
transport, not prospective clinical validation. No model/threshold is changed after evaluation.

| Item | Handling and evidence |
|---|---|
| Linkage | Unique SEQN in every input; left one-to-one merges into demographics. |
| Age/sex/race/education | Same variable names and coding families; age 80 represents 80+ in both cycles. Education 7/9 becomes missing. Codes are one-hot encoded within training folds. |
| BMI | BMXBMI in kg/m² in both cycles; no cross-cycle unit conversion. Missing BMI imputed only from development training records; a missingness indicator is included when learned. |
| CBC | Same selected variable names and units: WBC 10³/µL, RBC 10⁶/µL, hemoglobin g/dL, hematocrit %, MCV fL, RDW %, platelets 10³/µL, differential %. Both codebooks identify Beckman Coulter DxH 800. |
| HbA1c | LBXGH in percent, threshold ≥6.5. The 2021–2023 documentation reports a Tosoh G8 to Bio-Rad D-100 change; the CDC bridging study concluded no adjustment was needed. The 2017–2018 codebook describes G8 and secondary Premier methods. No invented conversion is applied; assay/cycle shift remains a limitation. |
| Diagnosis | DIQ010=2 only; yes, borderline, refused/unknown/missing excluded. No reported current insulin or diabetes pills (DIQ050/DIQ070=1 excluded). Questionnaire skips do not prove medication nonuse. |
| Pregnancy | Exclude recorded pregnant and require confirmed nonpregnant among females 20–44. Public status outside that band unavailable in both cycles. |
| Eligibility | Examined, age ≥20, observed HbA1c and all 12 CBC values, positive appropriate weight. |
| Weights | 2021–2023 WTPH2YR for blood-analyte analyses; 2017–2018 WTMEC2YR, as specified by its demographics codebook. Their differing nonresponse adjustments are a limitation. Do not pool these weights or invent an older phlebotomy weight. |
| Fasting analysis | Only current-cycle WTSAF2YR>0 and observed LBXGLU. GLU_L documentation assigns zero weights to records outside the 8-to-<24-hour fasting criteria. HbA1c and FPG models use this same subsample and fasting weights. |
| Variance | Define strata and nested PSU frame from all positive-weight records before the analytic domain. Units are masked variance clusters, not hospitals. |

Downloaded BMI and independent-cycle files have URLs, retrieval times, byte counts and SHA256
hashes in `data/manifests/extension_download_manifest.json`. Older pre-existing files retain unknown
original download dates; this manifest does not retroactively supply those dates.

Sources: locally saved `DEMO_J.htm`, `CBC_J.htm`, `GHB_J.htm`, `BMX_J.htm`, `DIQ_J.htm`,
and current `DEMO_L.htm`, `CBC_L.htm`, `GHB_L.htm`, `BMX_L.htm`, `GLU_L.htm`.
Online [2017 demographics](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/DEMO_J.htm),
[2021 HbA1c](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/GHB_L.htm),
[2021 glucose](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/GLU_L.htm).
