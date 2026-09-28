# NHANES August 2021-August 2023 — Laboratory Component

All files in this folder are from the CDC/NCHS NHANES continuous survey, cycle
**August 2021 - August 2023** (file suffix `_L`), Laboratory component:

<https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Laboratory&Cycle=2021-2023>

Each dataset is provided as a SAS transport file (`CODE_L.xpt`) with its matching
CDC documentation/codebook page (`CODE_L.htm`, saved locally, also viewable online at
`https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/CODE_L.htm`).

Every file shares the respondent identifier **`SEQN`**, which is the key used to
merge across files and across other NHANES components (Demographics, Questionnaire,
Examination, Dietary). Row counts differ between files because each lab test was only
run on a specific eligible subsample (age range, sex, fasting status, or a random
subsample), not the full ~8,860-person cycle — see "Eligible sample" per file below.

## Summary table

| File | Rows | Cols | Description |
|---|---|---|---|
| [`AGP_L`](#agp_l) | 2564 | 3 | alpha-1-Acid Glycoprotein |
| [`ALB_CR_L`](#alb_cr_l) | 8493 | 8 | Albumin & Creatinine - Urine |
| [`BCHE_L`](#bche_l) | 8068 | 5 | Butyrylcholinesterase Activity & Concentration |
| [`BIOPRO_L`](#biopro_l) | 7199 | 42 | Standard Biochemistry Profile |
| [`CBC_L`](#cbc_l) | 8727 | 23 | Complete Blood Count with 5-Part Differential in Whole Blood |
| [`COT_L`](#cot_l) | 8493 | 5 | Cotinine and Hydroxycotinine - Serum |
| [`FAR_L`](#far_l) | 8068 | 44 | Fatty Acids - Washed RBCs |
| [`FASTQX_L`](#fastqx_l) | 8727 | 19 | Fasting Questionnaire |
| [`FERTIN_L`](#fertin_l) | 2564 | 4 | Ferritin |
| [`FFMR_L`](#ffmr_l) | 8068 | 15 | Folate Forms - Total & Individual – Washed RBCs |
| [`FOLATE_L`](#folate_l) | 8727 | 4 | Folate - RBC |
| [`FOLFMS_L`](#folfms_l) | 8727 | 16 | Serum Folate Forms - Total & Individual - Serum |
| [`GHB_L`](#ghb_l) | 7199 | 3 | Glycohemoglobin |
| [`GLU_L`](#glu_l) | 3996 | 4 | Plasma Fasting Glucose |
| [`HDL_L`](#hdl_l) | 8068 | 4 | Cholesterol – High-Density Lipoprotein |
| [`HEPA_L`](#hepa_l) | 8611 | 3 | Hepatitis A |
| [`HEPBD_L`](#hepbd_l) | 8068 | 5 | Hepatitis B: Core antibody, Surface antigen, and Hepatitis D: antibody |
| [`HEPB_S_L`](#hepb_s_l) | 8611 | 3 | Hepatitis B Surface Antibody |
| [`HEPC_L`](#hepc_l) | 8068 | 5 | Hepatitis C: RNA (HCV-RNA), Confirmed Antibody (INNO-LIA), & Genotype |
| [`HEPE_L`](#hepe_l) | 8068 | 4 | Hepatitis E: IgG & IgM Antibodies |
| [`HSCRP_L`](#hscrp_l) | 8727 | 4 | High-Sensitivity C-Reactive Protein |
| [`IHGEM_L`](#ihgem_l) | 8727 | 11 | Mercury:  Inorganic, Ethyl, and Methyl - Blood |
| [`INS_L`](#ins_l) | 3996 | 5 | Insulin |
| [`PBCD_L`](#pbcd_l) | 8727 | 17 | Lead, Cadmium, Total Mercury, Selenium, & Manganese – Blood |
| [`PFAS_L`](#pfas_l) | 3618 | 20 | Perfluoroalkyl and Polyfluoroalkyl Substances |
| [`TCHOL_L`](#tchol_l) | 8068 | 4 | Cholesterol - Total |
| [`TFR_L`](#tfr_l) | 2564 | 4 | Transferrin Receptor |
| [`TRIGLY_L`](#trigly_l) | 3996 | 10 | Cholesterol - Low-Density Lipoproteins (LDL) & Triglycerides |
| [`TST_L`](#tst_l) | 8493 | 35 | Sex Steroid Hormone Panel - Serum |
| [`UCPREG_L`](#ucpreg_l) | 1134 | 2 | Urine Pregnancy Test |
| [`VID_L`](#vid_l) | 8727 | 10 | Vitamin D |
| [`VOCWB_L`](#vocwb_l) | 3618 | 78 | Volatile Organic Compounds and Trihalomethanes/MTBE - Blood |

---

## AGP_L

**alpha-1-Acid Glycoprotein**

- Data file: `AGP_L.xpt` (2564 rows x 3 columns)
- Doc/codebook: `AGP_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/AGP_L.htm

Alpha-1-Acid Glycoprotein (AGP) is synthesized in the liver and structurally belongs to the lipocalin superfamily of secretory proteins, such as retinol-binding protein and alpha-1-microglobulin (Schmid, 1975). AGP is a sensitive acute phase reactant whose concentration can increase by a factor of 3 within 24-48 hours when inflammation occurs (Tietz, 1995). It can also be used to differentiate between acute phase reactions (elevated serum level) and estrogen effects (normal or decreased serum level); whereas, the serum level of other positive reactants, such as ceruloplasmin and haptoglobin, increases during such reactions (Ganrot, 1974). Moderate and isolated increases occur when glomerular filtration is inhibited in the early stages of uremia. The determination is used in the assessment of the activity of acute and recurring inflammations as well as of tumors with cell necrosis (Ganrot, 1974).

**Eligible sample:** Examined participants 1-5 years old and 12-49 years old females were eligible.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `WTPH2YR` | Phlebotomy 2 Year Weight |
| `LBXAGP` | alpha-1-acid glycoprotein (g/L) |

---

## ALB_CR_L

**Albumin & Creatinine - Urine**

- Data file: `ALB_CR_L.xpt` (8493 rows x 8 columns)
- Doc/codebook: `ALB_CR_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/ALB_CR_L.htm

Albumin is the most abundant plasma protein in healthy individuals. Human serum albumin is synthesized by the liver and serves many important roles in human physiology such as, maintaining oncotic pressure, and transport of various hormones, vitamins, and drugs throughout the body. Kidney elimination of serum albumin may be observed in severe kidney disease. Following the urinary albumin excretion has been shown to be a diagnostic and prognostic marker for kidney and cardiovascular events. Unfortunately, this marker displays variable correlation between diagnostic vendors. The correlation deviations are attributed to calibration and assay differences between platforms.

**Eligible sample:** Examined participants aged 3 years and older were eligible.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `URXUMA` | Albumin, urine (ug/mL) |
| `URXUMS` | Albumin, urine (mg/L) |
| `URDUMALC` | Albumin, urine comment code |
| `URXUCR` | Creatinine, urine (mg/dL) |
| `URXCRS` | Creatinine, urine (umol/L) |
| `URDUCRLC` | Creatinine, urine comment code |
| `URDACT` | Albumin creatinine ratio (mg/g) |

---

## BCHE_L

**Butyrylcholinesterase Activity & Concentration**

- Data file: `BCHE_L.xpt` (8068 rows x 5 columns)
- Doc/codebook: `BCHE_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BCHE_L.htm

Butyrylcholinesterase (BChE) is an enzyme primarily synthesized in the liver and found in high concentrations in blood plasma. BChE can be used as an indicator of reduced cholinesterase (ChE). Due to its higher concentrations in blood plasma, because it is freely circulating in blood, and can be obtained directly from either serum or plasma, BChE activity is often a better indicator for acute ChE inhibition (Bartels et. al., 2000). While BChE is naturally produced, its activity can be affected by environmental exposures. BChE activity measurements can be used to indicate various health and exposure conditions including liver dysfunction, drug sensitivity, and exposure to organophosphate (OP) pesticides and nerve agents (Perez et. al. 2015).

**Eligible sample:** Examined participants aged 6 years and older were eligible.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `LBXBA` | Butyrylcholinesterase Activity (U/mL) |
| `LBDBALC` | Butyrylcholinesterase Act comt code |
| `LBXCH` | Butyrylcholinesterase Con (ng/mL) |
| `LBDCHLC` | Butyrylcholinesterase Conc comt code |

---

## BIOPRO_L

**Standard Biochemistry Profile**

- Data file: `BIOPRO_L.xpt` (7199 rows x 42 columns)
- Doc/codebook: `BIOPRO_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BIOPRO_L.htm

These series of measurements are used in the diagnosis and treatment of certain liver, heart, and kidney diseases; acid-base imbalance in the respiratory and metabolic systems; other diseases involving lipid metabolism; various endocrine disorders; as well as other metabolic or nutritional disorders.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent Sequence Number |
| `WTPH2YR` | Phlebotomy 2 Year Weight |
| `LBXSATSI` | Alanine Aminotransferase (ALT) (IU/L) |
| `LBXSAL` | Albumin, refrigerated serum (g/dL) |
| `LBDSALSI` | Albumin, refrigerated serum (g/L) |
| `LBXSAPSI` | Alkaline Phosphatase (ALP) (IU/L) |
| `LBXSASSI` | Aspartate Aminotransferase (AST) (IU/L) |
| `LBXSC3SI` | Bicarbonate (mmol/L) |
| `LBXSBU` | Blood Urea Nitrogen (mg/dL) |
| `LBDSBUSI` | Blood Urea Nitrogen (mmol/L) |
| `LBXSCLSI` | Chloride (mmol/L) |
| `LBXSCK` | Creatine Phosphokinase (CPK) (U/L) |
| `LBXSCR` | Creatinine, refrigerated serum (mg/dL) |
| `LBDSCRSI` | Creatinine, refrigerated serum (umol/L) |
| `LBXSGB` | Globulin (g/dL) |
| `LBDSGBSI` | Globulin (g/L) |
| `LBXSGL` | Glucose, refrigerated serum (mg/dL) |
| `LBDSGLSI` | Glucose, refrigerated serum (mmol/L) |
| `LBXSGTSI` | Gamma Glutamyl Transferase (GGT) (IU/L) |
| `LBDSGTLC` | GGT Comment Code |
| `LBXSIR` | Iron, refrigerated serum (µg/dL) |
| `LBDSIRSI` | Iron, refrigerated serum (umol/L) |
| `LBXSLDSI` | Lactate Dehydrogenase (LDH) (U/L) |
| `LBXMAGN` | Magnesium (mg/dL) |
| `LBXSOSSI` | Osmolality (mmol/Kg) |
| `LBXSPH` | Phosphorus (mg/dL) |
| `LBDSPHSI` | Phosphorus (mmol/L) |
| `LBXSKSI` | Potassium (mmol/L) |
| `LBXSNASI` | Sodium (mmol/L) |
| `LBXSTB` | Total Bilirubin (mg/dL) |
| `LBDSTBSI` | Total Bilirubin (umol/L) |
| `LBDSTBLC` | Total Bilirubin Comment Code |
| `LBXSCA` | Total Calcium (mg/dL) |
| `LBDSCASI` | Total Calcium (mmol/L) |
| `LBXSCH` | Cholesterol, refrigerated serum (mg/dL) |
| `LBDSCHSI` | Cholesterol, refrigerated serum (mmol/L) |
| `LBXSTP` | Total Protein (g/dL) |
| `LBDSTPSI` | Total Protein (g/L) |
| `LBXSTR` | Triglycerides, refrig serum (mg/dL) |
| `LBDSTRSI` | Triglycerides, refrig serum (mmol/L) |
| `LBXSUA` | Uric acid (mg/dL) |
| `LBDSUASI` | Uric acid (umol/L) |

---

## CBC_L

**Complete Blood Count with 5-Part Differential in Whole Blood**

- Data file: `CBC_L.xpt` (8727 rows x 23 columns)
- Doc/codebook: `CBC_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/CBC_L.htm

The complete blood count (CBC) with 5-part differential counts red blood cells (RBCs), white blood cells (WBCs), and platelets, measures hemoglobin; estimates the red cells’ volume; and sorts the WBCs into subtypes. A CBC is a routine blood test used to evaluate your overall health and detect a wide range of disorders, including anemia, infection, and leukemia.

**Eligible sample:** Examined participants aged 1 year and over were eligible.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `WTPH2YR` | Phlebotomy 2 Year Weight |
| `LBXWBCSI` | White blood cell count (1000 cells/uL) |
| `LBXLYPCT` | Lymphocyte percent (%) |
| `LBXMOPCT` | Monocyte percent (%) |
| `LBXNEPCT` | Segmented neutrophils percent (%) |
| `LBXEOPCT` | Eosinophils percent (%) |
| `LBXBAPCT` | Basophils percent (%) |
| `LBDLYMNO` | Lymphocyte number (1000 cells/uL) |
| `LBDMONO` | Monocyte number (1000 cells/uL) |
| `LBDNENO` | Segmented neutrophils num (1000 cell/uL) |
| `LBDEONO` | Eosinophils number (1000 cells/uL) |
| `LBDBANO` | Basophils number (1000 cells/uL) |
| `LBXRBCSI` | Red blood cell count (million cells/uL) |
| `LBXHGB` | Hemoglobin (g/dL) |
| `LBXHCT` | Hematocrit (%) |
| `LBXMCVSI` | Mean cell volume (fL) |
| `LBXMC` | Mean Cell Hgb Conc. (g/dL) |
| `LBXMCHSI` | Mean cell hemoglobin (pg) |
| `LBXRDW` | Red cell distribution width (%) |
| `LBXPLTSI` | Platelet count (1000 cells/uL) |
| `LBXMPSI` | Mean platelet volume (fL) |
| `LBXNRBC` | Nucleated red blood cells (/100 WBC) |

---

## COT_L

**Cotinine and Hydroxycotinine - Serum**

- Data file: `COT_L.xpt` (8493 rows x 5 columns)
- Doc/codebook: `COT_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/COT_L.htm

The specific aims of the component are: 1) to measure the prevalence and extent of tobacco use; 2) to estimate the extent of exposure to environmental tobacco smoke (ETS), and determine trends in exposure to ETS; and 3) to describe the relationship between tobacco use (as well as exposure to ETS) and chronic health conditions, including respiratory and cardiovascular diseases.

**Eligible sample:** Examined participants aged 3 years and older were eligible

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent Sequence Number |
| `LBXCOT` | Cotinine, Serum (ng/mL) |
| `LBDCOTLC` | Cotinine, Serum Comment Code |
| `LBXHCOT` | Hydroxycotinine, Serum (ng/mL) |
| `LBDHCOLC` | Hydroxycotinine, Serum Comment Code |

---

## FAR_L

**Fatty Acids - Washed RBCs**

- Data file: `FAR_L.xpt` (8068 rows x 44 columns)
- Doc/codebook: `FAR_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/FAR_L.htm

The analysis of red blood cell (RBC) fatty acids (FA) is an indicator of long term (4 months) FA status. Evaluation of RBC fatty acid content has become increasingly favored as a measure of n-3 polyunsaturated fatty acids (PUFA) intake. PUFA alter membrane physical characteristics and the activity of membrane-bound proteins. In membranes, they interact with ion channels and can be converted into bioactive eicosanoid (Harris, et al., 2008).

**Eligible sample:** Examined participants aged 6 years and older were eligible.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `WTPH2YR` | Phlebotomy 2 Year Weight |
| `LBXPAN` | alpha-Linolenic acid (C18:3n-3) (%) |
| `LBDPANLC` | alpha-Linolenic acid (C18:3n-3) cmt code |
| `LBXP1A` | Arachidic acid (C20:0) (%) |
| `LBDP1ALC` | Arachidic acid (C20:0) comment code |
| `LBXPRA` | Arachidonic acid (C20:4n-6) (%) |
| `LBDPRALC` | Arachidonic acid (C20:4n-6) comment code |
| `LBXPDA` | Docosanoic acid (C22:0) (%) |
| `LBDPDALC` | Docosanoic acid (C22:0) comment code |
| `LBXPHA` | Docosahexaenoic acid (C22:6n-3) (%) |
| `LBDPHALC` | Docosahexaenoic acid (C22:6n-3) cmt code |
| `LBXPD3` | Docosapentaenoic acid 3 (C22:5n-3) (%) |
| `LBDPD3LC` | Docosapentaenoic acid 3 (C22:5n-3) cmt |
| `LBXPD6` | Docosapentaenoic acid (C22:5n-6) (%) |
| `LBDPD6LC` | Docosapentaenoic acid (C22:5n-6) cmt cd |
| `LBXPTA` | Docosatetraenoic acid (C22:4n-6) (%) |
| `LBDPTALC` | Docosatetraenoic acid (C22:4n-6) cmt cd |
| `LBXPED` | 11,14-Eicosadienoic acid (C20:2n6) (%) |
| `LBDPEDLC` | 11,14-Eicosadienoic acid(C20:2n6) cmt cd |
| `LBXP1E` | 11-Eicosenoic acid (C20:1n-9) (%) |
| `LBDP1ELC` | 11-Eicosenoic acid (C20:1n-9) cmt code |
| `LBXPPE` | Eicosapentaenoic acid (C20:5n-3) (%) |
| `LBDPPELC` | Eicosapentaenoic acid (C20:5n-3) cmt cd |
| `LBXPLG` | gamma-Linolenic acid (C18:3n-6) (%) |
| `LBDPLGLC` | gamma-Linolenic acid (C18:3n-6) cmt code |
| `LBXPGH` | homo-gamma-Linolenic acid(C20:3n-6) (%) |
| `LBDPGHLC` | homo-gamma-Linolenic acd (C20:3n-6) cmt |
| `LBXP1G` | Tetracosanoic acid (C24:0) (%) |
| `LBDP1GLC` | Tetracosanoic acid (C24:0) comment code |
| `LBXPNL` | Linoleic acid (C18:2n-6) (%) |
| `LBDPNLLC` | Linoleic acid (C18:2n-6) comment code |
| `LBXPMR` | Myristic acid (C14:0) (%) |
| `LBDPMRLC` | Myristic acid (C14:0) comment code |
| `LBXPNR` | 15-Tetracosenoic acid (C24:1n9) (%) |
| `LBDPNRLC` | 15-Tetracosenoic acid(C24:1n9) comt code |
| `LBXPOL` | Oleic acid (C18:1n-9) (%) |
| `LBDPOLLC` | Oleic acid (C18:1n-9) comment code |
| `LBXPPL` | Palmitoleic acid (16:1n-7) (%) |
| `LBDPPLLC` | Palmitoleic acid (16:1n-7) comment code |
| `LBXPPM` | Palmitic acid (C16:0) (%) |
| `LBDPPMLC` | Palmitic acid (C16:0) comment code |
| `LBXPST` | Stearic acid (C18:0) (%) |
| `LBDPSTLC` | Stearic acid (C18:0) comment code |

---

## FASTQX_L

**Fasting Questionnaire**

- Data file: `FASTQX_L.xpt` (8727 rows x 19 columns)
- Doc/codebook: `FASTQX_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/FASTQX_L.htm

The fasting questionnaire is administered to determine the fasting status of the survey participant. Questions include but are not limited to: length of “food” fast, whether the participant had gum or mints, coffee or tea, or alcohol or dietary supplements prior to their laboratory examination.

**Eligible sample:** Examined participants aged 1 year and older were eligible.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `PHQ020` | Coffee or tea with cream or sugar? |
| `PHACOFHR` | Coffee/tea fast time (hours) |
| `PHACOFMN` | Coffee/tea fast time (minutes) |
| `PHQ030` | Alcohol, such as beer, wine, or liquor? |
| `PHAALCHR` | Alcohol fast time (hours) |
| `PHAALCMN` | Alcohol fast time (minutes) |
| `PHQ040` | Gum, mints, lozenges or cough drops |
| `PHAGUMHR` | Gum, mints cough drops fast time (hours) |
| `PHAGUMMN` | Gum, mints, cough fast time (minutes) |
| `PHQ050` | Antacids, laxatives, or anti-diarrheals? |
| `PHAANTHR` | Antacids, laxatives fast time (hours) |
| `PHAANTMN` | Antacids, laxatives fast time (minutes) |
| `PHQ060` | Dietary supplements? |
| `PHASUPHR` | Dietary supplements fast time (hours) |
| `PHASUPMN` | Dietary supplements fast time (minutes) |
| `PHAFSTHR` | Total length of 'food fast' (hours) |
| `PHAFSTMN` | Total length of 'food fast' (minutes) |
| `PHDSESNZ` | Session in which SP was examined |

---

## FERTIN_L

**Ferritin**

- Data file: `FERTIN_L.xpt` (2564 rows x 4 columns)
- Doc/codebook: `FERTIN_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/FERTIN_L.htm

Ferritin is a protein that contains iron and is found in red blood cells. Ferritin levels are used primarily in evaluating the body’s iron metabolism and levels of iron storage or reserves, which can be too low or too high. Low storage of iron can lead to iron deficiency anemia. High levels of iron storage, also called iron overload, occurs when excess iron is accumulated in the body, primarily the liver.

**Eligible sample:** Examined participants 1-5 years old and 12-49 years old females were eligible.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `WTPH2YR` | Phlebotomy 2 Year Weight |
| `LBXFER` | Ferritin(ng/mL) |
| `LBDFERSI` | Ferritin(µg/L) |

---

## FFMR_L

**Folate Forms - Total & Individual – Washed RBCs**

- Data file: `FFMR_L.xpt` (8068 rows x 15 columns)
- Doc/codebook: `FFMR_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/FFMR_L.htm

Folate belongs to the group of water-soluble B vitamins that occur naturally in food. Prolonged folate deficiency leads to megaloblastic anemia. Low folate status has been causally linked to an increased risk in women of reproductive age to have an offspring with neural tube defects. Low folate status also increases plasma homocysteine levels, a potential risk factor for chronic diseases, such as cardiovascular disease or cognitive function. Potential roles of folate and other B vitamins in modulating the risk for diseases (e.g., heart disease, cancer, and cognitive impairment) are under investigation. While serum folate is an indicator of recent intake, red blood cell (RBC) folate is an indicator of long-term status.

**Eligible sample:** Examined participants aged 6 years and older were eligible.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `WTPH2YR` | Phlebotomy 2 Year Weight |
| `LBDRF7SI` | Total Folate, RBC (nmol/L) |
| `LBXRF1SI` | 5-Methyl-tetrahydrofolate, RBC (nmol/L) |
| `LBDRF1LC` | 5-Methyl-tetrahydrofolate, RBC cmt |
| `LBXRF2SI` | Folic acid, RBC (nmol/L) |
| `LBDRF2LC` | Folic acid, RBC cmt |
| `LBXRF3SI` | 5-Formyl-tetrahydrofolate, RBC (nmol/L) |
| `LBDRF3LC` | 5-Formyl-tetrahydrofolate, RBC cmt |
| `LBXRF4SI` | Tetrahydrofolate, RBC (nmol/L) |
| `LBDRF4LC` | Tetrahydrofolate, RBC cmt |
| `LBXRF5SI` | 5,10-Methenyl-tetrahydrofolate (nmol/L) |
| `LBDRF5LC` | 5,10-Methenyl-tetrahydrofolate, RBC cmt |
| `LBXRF6SI` | MeFox oxidation product, RBC (nmol/L) |
| `LBDRF6LC` | MeFox oxidation product, RBC cmt |

---

## FOLATE_L

**Folate - RBC**

- Data file: `FOLATE_L.xpt` (8727 rows x 4 columns)
- Doc/codebook: `FOLATE_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/FOLATE_L.htm

Folate belongs to the group of water-soluble B vitamins that occur naturally in food. It is required in cellular one carbon metabolism and hematopoiesis. Prolonged folate deficiency leads to megaloblastic anemia (Bailey, 2015). Low folate status has been shown to increase the risk of women of childbearing age to have an offspring with neural tube defects. Low folate status also increases plasma homocysteine levels, a potential risk factor for cardiovascular disease, in the general population. Potential roles of folate and other B vitamins in modulating the risk for diseases (e.g., heart disease, cancer, and cognitive impairment) are currently being studied.

**Eligible sample:** All examined participants aged 1 year and older were eligible.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `WTPH2YR` | Phlebotomy 2 Year Weight |
| `LBDRFO` | RBC folate (ng/mL) |
| `LBDRFOSI` | RBC folate (nmol/L) |

---

## FOLFMS_L

**Serum Folate Forms - Total & Individual - Serum**

- Data file: `FOLFMS_L.xpt` (8727 rows x 16 columns)
- Doc/codebook: `FOLFMS_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/FOLFMS_L.htm

Folate belongs to the group of water-soluble B vitamins that occur naturally in food. It is required in cellular one carbon metabolism and hematopoiesis (Bailey, 2015). Prolonged folate deficiency leads to megaloblastic anemia. Low folate status has been shown to increase the risk of women of childbearing age to have an offspring with neural tube defects. Low folate status also increases plasma homocysteine levels, a potential risk factor for cardiovascular disease, in the general population. Potential roles of folate and other B vitamins in modulating the risk for diseases (e.g., heart disease, cancer, and cognitive impairment) are currently being studied.

**Eligible sample:** Examined participants aged 1 year and older were eligible.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `LBDFOTSI` | Serum total folate (nmol/L) |
| `LBDFOT` | Serum total folate (ng/mL) |
| `LBXSF1SI` | 5-Methyl-tetrahydrofolate (nmol/L) |
| `LBDSF1LC` | 5-Methyl-tetrahydrofolate cmt |
| `LBXSF2SI` | Folic acid (nmol/L) |
| `LBDSF2LC` | Folic acid cmt |
| `LBXSF3SI` | 5-Formyl-tetrahydrofolate (nmol/L) |
| `LBDSF3LC` | 5-Formyl-tetrahydrofolate cmt |
| `LBXSF4SI` | Tetrahydrofolate (nmol/L) |
| `LBDSF4LC` | Tetrahydrofolate cmt |
| `LBXSF5SI` | 5,10-Methenyl-tetrahydrofolate (nmol/L) |
| `LBDSF5LC` | 5,10-Methenyl-tetrahydrofolate cmt |
| `LBXSF6SI` | Mefox oxidation product (nmol/L) |
| `LBDSF6LC` | Mefox oxidation product cmt |

---

## GHB_L

**Glycohemoglobin**

- Data file: `GHB_L.xpt` (7199 rows x 3 columns)
- Doc/codebook: `GHB_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/GHB_L.htm

According to the National Diabetes Statistics Report, in 2021, diabetes was the eighth leading cause of death in the United States (Centers for Disease Control and Prevention, 2024). More than 38 million Americans are living with diabetes, where almost 30 million were diagnosed and nearly 9 million were undiagnosed (American Diabetes Association, 2023). Also, more than 97 million are living with prediabetes, which is a serious health condition that increases a person’s risk of type-2 diabetes and other chronic diseases (American Diabetes Association, 2023). The prevalence of diabetes and overweight, one of the major risk factors for diabetes, continues to increase. Recognized and accredited programs are available for people to prevent or manage diabetes, including the National Diabetes Prevention Program (Centers for Disease Control and Prevention, 2024) and diabetes self-management education and support services (Centers for Disease Control and Prevention, 2024).

**Eligible sample:** Examined participants aged 12 years and older were eligible.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Sequence number |
| `WTPH2YR` | Phlebotomy 2 Year Weight |
| `LBXGH` | Glycohemoglobin (%) |

---

## GLU_L

**Plasma Fasting Glucose**

- Data file: `GLU_L.xpt` (3996 rows x 4 columns)
- Doc/codebook: `GLU_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/GLU_L.htm

According to the National Diabetes Statistics Report, in 2021, diabetes was the eighth leading cause of death in the United States (Centers for Disease Control and Prevention2024). More than 38 million Americans are living with diabetes, where almost 30 million were diagnosed and nearly 9 million were undiagnosed (American Diabetes Association, 2023). Also, more than 97 million are living with prediabetes, which is a serious health condition that increases a person’s risk of type-2 diabetes and other chronic diseases (American Diabetes Association, 2023). The prevalence of diabetes and overweight, one of the major risk factors for diabetes, continues to increase. Recognized and accredited programs are available for people to prevent or manage diabetes, including the National Diabetes Prevention Program (Centers for Disease Control and Prevention, 2024) and diabetes self-management education and support services (Centers for Disease Control and Prevention, 2024).

**Eligible sample:** All examined participants 12 years and older were eligible.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `WTSAF2YR` | Fasting Subsample 2 Year MEC Weight |
| `LBXGLU` | Fasting Glucose (mg/dL) |
| `LBDGLUSI` | Fasting Glucose (mmol/L) |

---

## HDL_L

**Cholesterol – High-Density Lipoprotein**

- Data file: `HDL_L.xpt` (8068 rows x 4 columns)
- Doc/codebook: `HDL_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/HDL_L.htm

Heart disease is the leading cause of death in the United States (Murphy, et. al., 2018). Blood lipid levels are fundamental measures included in NHANES that can be used for cardiovascular risk assessment. The goals of the NHANES blood lipids measurements include: 1) monitoring the prevalence and trends in major cardiovascular conditions and overall risk factors in the U.S.; 2) evaluating prevention and treatment programs targeting cardiovascular disease in the U.S.; and 3) monitoring the status of hyperlipidemia.

**Eligible sample:** Examined participants aged 6 years and older were eligible.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent Sequence Number |
| `WTPH2YR` | Phlebotomy 2 Year Weight |
| `LBDHDD` | Direct HDL-Cholesterol (mg/dL) |
| `LBDHDDSI` | Direct HDL-Cholesterol (mmol/L) |

---

## HEPA_L

**Hepatitis A**

- Data file: `HEPA_L.xpt` (8611 rows x 3 columns)
- Doc/codebook: `HEPA_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/HEPA_L.htm

Hepatitis viruses constitute a major public health problem because of the morbidity and mortality associated with the acute and chronic consequences of these infections. Because of the high rate of asymptomatic infection with these viruses, information about the prevalence of these diseases is needed to monitor prevention efforts. By testing a nationally representative sample of the U.S. population, NHANES provides the most reliable estimates of age-specific prevalence needed to evaluate the effectiveness of the strategies to prevent these infections. In addition, NHANES provides the means to better define the epidemiology of other hepatitis viruses. NHANES testing for markers of infection with hepatitis viruses is used to determine secular trends in infection rates across most age and racial/ethnic groups and provides a national picture of the epidemiologic determinants of these infections.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `WTPH2YR` | Phlebotomy 2 Year Weight |
| `LBXHA` | Hepatitis A antibody |

---

## HEPBD_L

**Hepatitis B: Core antibody, Surface antigen, and Hepatitis D: antibody**

- Data file: `HEPBD_L.xpt` (8068 rows x 5 columns)
- Doc/codebook: `HEPBD_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/HEPBD_L.htm

Hepatitis viruses constitute a major public health problem because of the morbidity and mortality associated with the acute and chronic consequences of these infections. Because of the high rate of asymptomatic infection with these viruses, information about the prevalence of these diseases is needed to monitor prevention efforts. By testing a nationally representative sample of the U.S. population, NHANES will provide the most reliable estimates of age-specific prevalence needed to evaluate the effectiveness of the strategies to prevent these infections. In addition, NHANES provides the means to better define the epidemiology of other hepatitis viruses. NHANES testing for markers of infection with hepatitis viruses has been used to determine secular trends in infection rates across most age and racial/ethnic groups and has provided a national picture of the epidemiologic determinants of these infections.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `WTPH2YR` | Phlebotomy 2 Year Weight |
| `LBXHBC` | Hepatitis B core antibody |
| `LBDHBG` | Hepatitis B surface antigen |
| `LBDHD` | Hepatitis D antibody (anti-HDV) |

---

## HEPB_S_L

**Hepatitis B Surface Antibody**

- Data file: `HEPB_S_L.xpt` (8611 rows x 3 columns)
- Doc/codebook: `HEPB_S_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/HEPB_S_L.htm

Hepatitis viruses constitute a major public health problem because of the morbidity and mortality associated with the acute and chronic consequences of these infections. Because of the high rate of asymptomatic infection with these viruses, information about the prevalence of these diseases is needed to monitor prevention efforts. By testing a nationally representative sample of the U.S. population, NHANES provides the most reliable estimates of age-specific prevalence needed to evaluate the effectiveness of the strategies to prevent these infections. NHANES testing for markers of infection with hepatitis viruses is used to determine secular trends in infection rates across most age and racial/ethnic groups, and provides a national picture of the epidemiologic determinants of these infections.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `WTPH2YR` | Phlebotomy 2 Year Weight |
| `LBXHBS` | Hepatitis B Surface Antibody |

---

## HEPC_L

**Hepatitis C: RNA (HCV-RNA), Confirmed Antibody (INNO-LIA), & Genotype**

- Data file: `HEPC_L.xpt` (8068 rows x 5 columns)
- Doc/codebook: `HEPC_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/HEPC_L.htm

Hepatitis viruses constitute a major public health problem because of the morbidity and mortality associated with the acute and chronic consequences of these infections. Because of the high rate of asymptomatic infection with these viruses, information about the prevalence of these diseases is needed to monitor prevention efforts. By testing a nationally representative sample of the U.S. population, NHANES provides the most reliable estimates of age-specific prevalence needed to evaluate the effectiveness of the strategies to prevent these infections. NHANES testing for markers of infection with hepatitis viruses is used to determine secular trends in infection rates across most age and racial/ethnic groups, and provides a national picture of the epidemiologic determinants of these infections.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `WTPH2YR` | Phlebotomy 2 Year Weight |
| `LBXHCR` | Hepatitis C RNA |
| `LBDHCI` | Hepatitis C Antibody (confirmed) |
| `LBXHCG` | Hepatitis C Genotype |

---

## HEPE_L

**Hepatitis E: IgG & IgM Antibodies**

- Data file: `HEPE_L.xpt` (8068 rows x 4 columns)
- Doc/codebook: `HEPE_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/HEPE_L.htm

Hepatitis viruses constitute a major public health problem because of the morbidity and mortality associated with the acute and chronic consequences of these infections. Because of the high rate of asymptomatic infection with these viruses, information about the prevalence of these diseases is needed to monitor prevention efforts. By testing a nationally representative sample of the U.S. population, NHANES provides the most reliable estimates of age-specific prevalence needed to evaluate the effectiveness of the strategies to prevent these infections. NHANES testing for markers of infection with hepatitis viruses is used to determine secular trends in infection rates across most age and racial/ethnic groups, and provides a national picture of the epidemiologic determinants of these infections. In addition, NHANES provides the means to better define the epidemiology of other hepatitis viruses.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `WTPH2YR` | Phlebotomy 2 Year Weight |
| `LBDHEG` | Hepatitis E IgG (anti-HEV) |
| `LBDHEM` | Hepatitis E IgM (anti-HEV) |

---

## HSCRP_L

**High-Sensitivity C-Reactive Protein**

- Data file: `HSCRP_L.xpt` (8727 rows x 4 columns)
- Doc/codebook: `HSCRP_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/HSCRP_L.htm

C-reactive protein (CRP) is an acute phase protein synthesized in the liver. It is involved in the activation of complement, enhancement of phagocytosis, and detoxification of substances released from damaged tissue. It is one of the most sensitive, though nonspecific, indicators of inflammation. CRP levels may rise within six hours of an inflammatory stimulus. Measurement of CRP concentrations by this highly sensitive method is performed primarily to ascertain the level of cardiovascular disease risk in individuals who have no existing inflammatory conditions. Increases in CRP concentration are non-specific and should be used in conjunction with traditional clinical laboratory evaluation of acute coronary syndromes.

**Eligible sample:** Examined participants aged 1 year and older were eligible.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent Sequence Number |
| `WTPH2YR` | Phlebotomy 2 Year Weight |
| `LBXHSCRP` | HS C-Reactive Protein (mg/L) |
| `LBDHRPLC` | HS C-Reactive Protein Comment Code |

---

## IHGEM_L

**Mercury:  Inorganic, Ethyl, and Methyl - Blood**

- Data file: `IHGEM_L.xpt` (8727 rows x 11 columns)
- Doc/codebook: `IHGEM_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/IHGEM_L.htm

Inorganic, Ethyl and Methyl Mercury

**Eligible sample:** All examined participants aged 1 year and older were eligible.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `WTPH2YR` | Phlebotomy 2 Year Weight |
| `LBXIHG` | Mercury, inorganic (ug/L) |
| `LBDIHGSI` | Mercury, inorganic (nmol/L) |
| `LBDIHGLC` | Mercury, inorganic comment code |
| `LBXBGE` | Mercury, ethyl (ug/L) |
| `LBDBGESI` | Mercury, ethyl (nmol/L) |
| `LBDBGELC` | Mercury, ethyl comment code |
| `LBXBGM` | Mercury, methyl (ug/L) |
| `LBDBGMSI` | Mercury, methyl (nmol/L) |
| `LBDBGMLC` | Mercury, methyl comment code |

---

## INS_L

**Insulin**

- Data file: `INS_L.xpt` (3996 rows x 5 columns)
- Doc/codebook: `INS_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/INS_L.htm

Insulin is the primary hormone responsible for controlling glucose metabolism, and its secretion is determined by plasma glucose concentration. The insulin molecule is synthesized in the pancreas as pro-insulin and is later cleaved to form C-peptide and insulin. The principal function of insulin is to control the uptake and utilization of glucose in the peripheral tissues. Insulin concentrations are severely reduced in insulin-dependent diabetes mellitus (IDDM) and some other conditions, while insulin concentrations are raised in non-insulin-dependent diabetes mellitus (NIDDM), obesity, and some endocrine disorders.

**Eligible sample:** All examined participants 12 years and older, in the NHANES August 2021 – August 2023 sample, were eligible.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `WTSAF2YR` | Fasting Subsample 2 Year MEC Weight |
| `LBXIN` | Insulin (uU/mL) |
| `LBDINSI` | Insulin (pmol/L) |
| `LBDINLC` | Insulin Comment Code |

---

## PBCD_L

**Lead, Cadmium, Total Mercury, Selenium, & Manganese – Blood**

- Data file: `PBCD_L.xpt` (8727 rows x 17 columns)
- Doc/codebook: `PBCD_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/PBCD_L.htm

Lead

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `WTPH2YR` | Phlebotomy 2 Year Weight |
| `LBXBPB` | Blood lead (ug/dL) |
| `LBDBPBSI` | Blood lead (umol/L) |
| `LBDBPBLC` | Blood lead comment code |
| `LBXBCD` | Blood cadmium (ug/L) |
| `LBDBCDSI` | Blood cadmium (nmol/L) |
| `LBDBCDLC` | Blood cadmium comment code |
| `LBXTHG` | Blood mercury, total (ug/L) |
| `LBDTHGSI` | Blood mercury, total (nmol/L) |
| `LBDTHGLC` | Blood mercury, total comment code |
| `LBXBSE` | Blood selenium (ug/L) |
| `LBDBSESI` | Blood selenium (umol/L) |
| `LBDBSELC` | Blood selenium comment code |
| `LBXBMN` | Blood manganese (ug/L) |
| `LBDBMNSI` | Blood manganese (nmol/L) |
| `LBDBMNLC` | Blood manganese comment code |

---

## PFAS_L

**Perfluoroalkyl and Polyfluoroalkyl Substances**

- Data file: `PFAS_L.xpt` (3618 rows x 20 columns)
- Doc/codebook: `PFAS_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/PFAS_L.htm

Perfluoroalkyl and polyfluoroalkyl substances (PFAS) are used in multiple commercial applications, including surfactants, lubricants, paints, polishes, food packaging, and fire-retarding foams. Certain PFAS are used in the manufacture of polymers used in many industrial and consumer products, including soil, stain, grease, and water-resistant coatings on textiles and carpet; uses in the automotive, mechanical, aerospace, chemical, electrical, medical, and building/construction industries; personal care products; and non-stick coatings on cookware. Some PFAS are ubiquitous contaminants found in humans and animals worldwide.

**Eligible sample:** Examined participants aged 12 years and older were eligible.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `WTSPF2YR` | PFAS subsample weight |
| `LBXPFDE` | Perfluorodecanoic acid (ng/mL) |
| `LBDPFDEL` | Perfluorodecanoic acid Comment Code |
| `LBXPFHS` | Perfluorohexane sulfonic acid (ng/mL) |
| `LBDPFHSL` | Perfluorohexane sulfonic acid Comt Code |
| `LBXMPAH` | 2-(N-methyl-PFOSA)acetic acid (ng/mL) |
| `LBDMPAHL` | 2-(N-methyl-PFOSA) acetic acid Comt Code |
| `LBXPFNA` | Perfluorononanoic acid (ng/mL) |
| `LBDPFNAL` | Perfluorononanoic acid Comment Code |
| `LBXPFUA` | Perfluoroundecanoic acid (ng/mL) |
| `LBDPFUAL` | Perfluoroundecanoic acid Comment Code |
| `LBXNFOA` | n-perfluorooctanoic acid (ng/mL) |
| `LBDNFOAL` | n-perfluorooctanoic acid Comment Code |
| `LBXBFOA` | Br. perfluorooctanoic acid iso (ng/mL) |
| `LBDBFOAL` | Br. perfluorooctanoic acid iso Comt Code |
| `LBXNFOS` | n-perfluorooctane sulfonic acid (ng/mL) |
| `LBDNFOSL` | n-perfluorooctane sulfonic Comt Code |
| `LBXMFOS` | Sm-PFOS (ng/mL) |
| `LBDMFOSL` | Sm-PFOS Comment Code |

---

## TCHOL_L

**Cholesterol - Total**

- Data file: `TCHOL_L.xpt` (8068 rows x 4 columns)
- Doc/codebook: `TCHOL_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/TCHOL_L.htm

Heart disease is the leading cause of death in the United States (Murphy, et. al., 2018). Blood lipid levels are fundamental measures included in NHANES that can be used for cardiovascular risk assessment. The goals the NHANES blood lipids measurements include: 1) monitoring the prevalence and trends in major cardiovascular conditions and overall risk factors in the U.S.; 2) evaluating prevention and treatment programs targeting cardiovascular disease in the U.S.; and 3) monitoring the status of hyperlipidemia.

**Eligible sample:** Examined participants aged 6 years and older were eligible.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent Sequence Number |
| `WTPH2YR` | Phlebotomy 2 Year Weight |
| `LBXTC` | Total Cholesterol (mg/dL) |
| `LBDTCSI` | Total Cholesterol (mmol/L) |

---

## TFR_L

**Transferrin Receptor**

- Data file: `TFR_L.xpt` (2564 rows x 4 columns)
- Doc/codebook: `TFR_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/TFR_L.htm

Soluble transferrin receptor (sTfR) is a measure of iron deficiency and is particularly useful in persons with inflammation, infection, or chronic disease, where ferritin levels do not correlate with true iron levels. Low storage of iron can lead to iron deficiency anemia. High levels of iron storage, also called iron overload, occurs when excess iron is accumulated in the body, primarily the liver.

**Eligible sample:** Examined participants aged 1 to 5 years and females aged 12-49 years were eligible.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `WTPH2YR` | Phlebotomy 2 Year Weight |
| `LBXTFR` | Transferrin receptor (mg/L) |
| `LBDTFRSI` | Transferrin receptor (nmol/L) |

---

## TRIGLY_L

**Cholesterol - Low-Density Lipoproteins (LDL) & Triglycerides**

- Data file: `TRIGLY_L.xpt` (3996 rows x 10 columns)
- Doc/codebook: `TRIGLY_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/TRIGLY_L.htm

Heart disease is the leading cause of death in the United States (Murphy, et. al., 2024). Blood lipid levels are fundamental measures included in NHANES that can be used for cardiovascular risk assessment. The goals of NHANES blood lipid measurements include: 1) monitoring the prevalence and trends in major cardiovascular conditions and overall risk factors in the U.S.; 2) evaluating prevention and treatment programs targeting cardiovascular disease in the U.S.; and 3) monitoring the status of hyperlipidemia.

**Eligible sample:** Participants aged 12 years and older who were examined in the morning sessions were eligible.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `WTSAF2YR` | Fasting Subsample 2 Year MEC Weight |
| `LBXTLG` | Triglyceride (mg/dL) |
| `LBDTRSI` | Triglyceride (mmol/L) |
| `LBDLDL` | LDL-Cholesterol, Friedewald (mg/dL) |
| `LBDLDLSI` | LDL-Cholesterol, Friedewald (mmol/L) |
| `LBDLDLM` | LDL-Cholesterol, Martin-Hopkins (mg/dL) |
| `LBDLDMSI` | LDL-Cholesterol, Martin-Hopkins (mmol/L) |
| `LBDLDLN` | LDL-Cholesterol, NIH equation 2 (mg/dL) |
| `LBDLDNSI` | LDL-Cholesterol, NIH equation 2 (mmol/L) |

---

## TST_L

**Sex Steroid Hormone Panel - Serum**

- Data file: `TST_L.xpt` (8493 rows x 35 columns)
- Doc/codebook: `TST_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/TST_L.htm

The sex steroid hormone panel – Serum (TST) consists of 17α-hydroxyprogesterone, androstenedione, anti-Müllerian hormone, dehydroepiandrosterone sulfate (DHEAS), estradiol, estrone, estrone sulfate, follicle-stimulating hormone, luteinizing hormone, progesterone, sex hormone binding globulin, and total testosterone. This data will allow for analysis of the selected steroid hormones and related binding protein that can be used to assist in disease diagnosis, treatment, and prevention of diseases, such as Polycystic Ovary Syndrome (PCOS), androgen deficiency, certain cancers, and hormone imbalances. An estimated 5 to 7 million women in the United States (U.S.) suffer with the effects of PCOS; and PCOS can occur in girls as young as 11 years old. PCOS is the most common hormonal disorder among women of reproductive age and is the leading cause of infertility. Androgen deficiency, such as hypogonadism, is associated with a range of chronic diseases. The prevalence of symptomatic androgen deficiency in men between 30 and 79 years of age is estimated to be 5.6% (Araujo et. al., 2007). Androgen deficiency in men and excess in women and the associated chronic diseases are a public health concern. Estradiol is the key biomarker for assessing reproductive function in females, including amenorrhea, infertility, and menopausal status. Estradiol levels decline greatly with age, and this decrease is associated with increased risk for cardiovascular disease, cognitive impairment, and bone fractures in older women. Estrogen hormone therapy, or use of estradiol as a supplement, raises health concerns related to estradiol concentration in blood, such as elevated levels in postmenopausal women increasing the risk of breast cancer.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `WTPH2YR` | Phlebotomy 2 Year Weight |
| `LBX17H` | 17α-hydroxyprogesterone (ng/dL) |
| `LBD17HSI` | 17α-hydroxyprogesterone (nmol/L) |
| `LBD17HLC` | 17α-hydroxyprogesterone Comment Code |
| `LBXAND` | Androstenedione (ng/dL) |
| `LBDANDSI` | Androstenedione (nmol/L) |
| `LBDANDLC` | Androstenedione Comment Code |
| `LBXAMH` | Anti-Mullerian hormone (ng/mL) |
| `LBDAMHSI` | Anti-Mullerian hormone (pmol/L) |
| `LBDAMHLC` | Anti-Mullerian hormone Comment Code |
| `LBXDHE` | DHEAS (µg/dL) |
| `LBDDHESI` | DHEAS (µmol/L) |
| `LBDDHELC` | DHEAS Comment Code |
| `LBXEST` | Estradiol (pg/mL) |
| `LBDESTSI` | Estradiol (pmol/L) |
| `LBDESTLC` | Estradiol Comment Code |
| `LBXESO` | Estrone (ng/dL) |
| `LBDESOSI` | Estrone (pmol/L) |
| `LBDESOLC` | Estrone Comment Code |
| `LBXES1` | Estrone Sulfate (pg/mL) |
| `LBDES1SI` | Estrone Sulfate (pmol/L) |
| `LBDES1LC` | Estrone Sulfate Comment Code |
| `LBXFSH` | Follicle Stimulating Hormone (mIU/mL) |
| `LBDFSHLC` | FSH Comment Code |
| `LBXLUH` | Luteinizing Hormone (mIU/mL) |
| `LBDLUHLC` | Luteinizing Hormone Comment Code |
| `LBXPG4` | Progesterone (ng/dL) |
| `LBDPG4SI` | Progesterone (nmol/L) |
| `LBDPG4LC` | Progesterone Comment Code |
| `LBXSHBG` | SHBG (nmol/L) |
| `LBDSHGLC` | SHBG Comment Code |
| `LBXTST` | Testosterone, total (ng/dL) |
| `LBDTSTSI` | Testosterone, total (nmol/L) |
| `LBDTSTLC` | Testosterone comment code |

---

## UCPREG_L

**Urine Pregnancy Test**

- Data file: `UCPREG_L.xpt` (1134 rows x 2 columns)
- Doc/codebook: `UCPREG_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/UCPREG_L.htm

A urine pregnancy test was performed in the mobile examination center (MEC) on menstruating female survey participants 8 years and older. All positive test results excluded pregnant women from the DXA component at the MEC.

**Eligible sample:** Examined female participants aged 12–59 years, and menstruating females aged 8–11 years were eligible. However, due to disclosure risks, only females 20-44 years of age have urine pregnancy results in this file.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `URXPREG` | Urine Pregnancy Result |

---

## VID_L

**Vitamin D**

- Data file: `VID_L.xpt` (8727 rows x 10 columns)
- Doc/codebook: `VID_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/VID_L.htm

Vitamin D is functionally a hormone rather than a vitamin, and in conjunction with parathyroid hormone and calcitonin, it is one of the most important biological regulators of calcium metabolism. Vitamin D and its main metabolites may be categorized into two families of secosteroids: cholecalciferol (vitamin D3) and ergocalciferol (vitamin D2). Both vitamins D3 and D2 are enzymatically hydroxylated in the liver to 25-hydroxy forms and then further metabolized in the kidney to the bioactive 1,25-dihydroxy forms. Although 25-hydroxyvitamin D (25OHD) is not the bioactive form, it is the predominant circulating form of vitamin D, and thus, it is considered to be the most reliable index of vitamin D status (Olkowski, 2003; Saenger, 2006). Vitamin D3 is a naturally occurring form of vitamin D that is produced in the skin after 7-dehydrocholesterol is exposed to UV-B radiation. Commercially, vitamin D2 is produced by UV irradiation of plant-derived ergosterol. The two forms differ in the structures of their side chains, but they are metabolized identically. Good sources of vitamin D3 are fatty fish, while mushrooms provide a good source of vitamin D2. Both forms are used for fortification of a limited selection of foods including milk, juice, margarines, cheese and nutrition bars. Because these two parent compounds provide various contributions to vitamin D status, it is informative when both forms are measured separately (Olkowski, 2003; Saenger, 2006).

**Eligible sample:** Examined participants aged 1 year and older were eligible.

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `WTPH2YR` | Phlebotomy 2 Year Weight |
| `LBXVIDMS` | 25OHD2+25OHD3 (nmol/L) |
| `LBDVIDLC` | 25OHD2+25OHD3 comment code |
| `LBXVD2MS` | 25OHD2 (nmol/L) |
| `LBDVD2LC` | 25OHD2 comment code |
| `LBXVD3MS` | 25OHD3 (nmol/L) |
| `LBDVD3LC` | 25OHD3 comment code |
| `LBXVE3MS` | epi-25OHD3 (nmol/L) |
| `LBDVE3LC` | epi-25OHD3 comment code |

---

## VOCWB_L

**Volatile Organic Compounds and Trihalomethanes/MTBE - Blood**

- Data file: `VOCWB_L.xpt` (3618 rows x 78 columns)
- Doc/codebook: `VOCWB_L.htm`
- Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/VOCWB_L.htm

Volatile Organic Compounds and Trihalomethanes/MTBE (Whole Blood)

**Variables:**

| Column | Description |
|---|---|
| `SEQN` | Respondent sequence number |
| `WTSVOC2Y` | VOC Subsample Weight |
| `LBX2DF` | Blood 2,5-Dimethylfuran (ng/mL) |
| `LBD2DFLC` | Blood 2,5-Dimethylfuran Comment Code |
| `LBXV06` | Blood Hexane (ng/mL) |
| `LBDV06LC` | Blood Hexane Comment Code |
| `LBXV07N` | Blood Heptane (ng/mL) |
| `LBDV07LC` | Blood Heptane Comment Code |
| `LBXV08N` | Blood Octane (ng/mL) |
| `LBDV08LC` | Blood Octane Comment Code |
| `LBXV1D` | Blood 1,2-Dichlorobenzene (ng/mL) |
| `LBDV1DLC` | Blood 1,2-Dichlorobenzene Comment Code |
| `LBXV2A` | Blood 1,2-Dichloroethane (ng/mL) |
| `LBDV2ALC` | Blood 1,2-Dichloroethane Comment Code |
| `LBXV3B` | Blood 1,3-Dichlorobenzene (ng/mL) |
| `LBDV3BLC` | Blood 1,3-Dichlorobenzene Comment Code |
| `LBXV4C` | Blood Tetrachloroethene (ng/mL) |
| `LBDV4CLC` | Blood Tetrachloroethene Comment Code |
| `LBXVAPN` | Blood a-pinene (ng/mL) |
| `LBDVAPLC` | Blood a-pinene Comment Code |
| `LBXVBF` | Blood Bromoform (ng/mL) |
| `LBDVBFLC` | Blood Bromoform Comment Code |
| `LBXVBM` | Blood Bromodichloromethane (ng/mL) |
| `LBDVBMLC` | Blood Bromodichloromethane Comment Code |
| `LBXVBZ` | Blood Benzene (ng/mL) |
| `LBDVBZLC` | Blood Benzene Comment Code |
| `LBXVBZN` | Blood Benzonitrile (ng/mL) |
| `LBDVZBLC` | Blood Benzonitrile Comment Code |
| `LBXVC6` | Blood Cyclohexane (ng/mL) |
| `LBDVC6LC` | Blood Cyclohexane Comment Code |
| `LBXVCB` | Blood Chlorobenzene (ng/mL) |
| `LBDVCBLC` | Blood Chlorobenzene Comment Code |
| `LBXVCF` | Blood Chloroform (ng/mL) |
| `LBDVCFLC` | Blood Chloroform Comment Code |
| `LBXVCM` | Blood Dibromochloromethane (ng/mL) |
| `LBDVCMLC` | Blood Dibromochloromethane Comment Code |
| `LBXVCT` | Blood Carbon Tetrachloride (ng/mL) |
| `LBDVCTLC` | Blood Carbon Tetrachloride Comment Code |
| `LBXVDB` | Blood 1,4-Dichlorobenzene (ng/mL) |
| `LBDVDBLC` | Blood 1,4-Dichlorobenzene Comment Code |
| `LBXVDEE` | Blood Diethyl Ether (ng/mL) |
| `LBDVEELC` | Blood Diethyl Ether Comment Code |
| `LBXVEA` | Blood Ethyl Acetate (ng/mL) |
| `LBDVEALC` | Blood Ethyl Acetate Comment Code |
| `LBXVEB` | Blood Ethylbenzene (ng/mL) |
| `LBDVEBLC` | Blood Ethylbenzene Comment Code |
| `LBXVEC` | Blood Chloroethane (ng/mL) |
| `LBDVECLC` | Blood Chloroethane Comment Code |
| `LBXVFN` | Blood Furan (ng/mL) |
| `LBDVFNLC` | Blood Furan Comment Code |
| `LBXVIBN` | Blood Isobutyronitrile (ng/mL) |
| `LBDVIBLC` | Blood Isobutyronitrile Comment Code |
| `LBXVIPB` | Blood Isopropylbenzene (ng/mL) |
| `LBDVIPLC` | Blood Isopropylbenzene Comment Code |
| `LBXVMC` | Blood Methylene Chloride (ng/mL) |
| `LBDVMCLC` | Blood Methylene Chloride Comment Code |
| `LBXVMCP` | Blood Methylcyclopentane (ng/mL) |
| `LBDVMPLC` | Blood Methylcyclopentane Comment Code |
| `LBXVME` | Blood MTBE (ng/mL) |
| `LBDVMELC` | Blood MTBE Comment Code |
| `LBXVMIK` | Blood Methyl Isobutyl Ketone (ng/mL) |
| `LBDVMKLC` | Blood Methyl Isobutyl Ketone Comt Code |
| `LBXVOX` | Blood o-Xylene (ng/mL) |
| `LBDVOXLC` | Blood o-Xylene Comment Code |
| `LBXVST` | Blood Styrene (ng/mL) |
| `LBDVSTLC` | Blood Styrene Comment Code |
| `LBXVTC` | Blood Trichloroethene (ng/mL) |
| `LBDVTCLC` | Blood Trichloroethene Comment Code |
| `LBXVTE` | Blood 1,1,1-Trichloroethane (ng/mL) |
| `LBDVTELC` | Blood 1,1,1-Trichloroethane Comment Code |
| `LBXVTHF` | Blood Tetrahydrofuran (ng/mL) |
| `LBDVHTLC` | Blood Tetrahydrofuran Comment Code |
| `LBXVTO` | Blood Toluene (ng/mL) |
| `LBDVTOLC` | Blood Toluene Comment Code |
| `LBXVTP` | Blood 1,2,3-Trichloropropane (ng/mL) |
| `LBDVTPLC` | Blood 1,2,3-Trichloropropane Comt Code |
| `LBXVXY` | Blood m-/p-Xylene (ng/mL) |
| `LBDVXYLC` | Blood m-/p-Xylene Comment Code |

---
