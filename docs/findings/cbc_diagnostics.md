# CBC collinearity and PCA supplement — 2026-11-23 (updated for the Phase 15 locked 9-feature set)

Exploratory Phase 7 supplement on the fixed 4,612 adults / 106 positive HbA1c labels.
The original primary analysis and independent-cycle results are preserved.

## Collinearity: three stages of this project's CBC feature-block history

1. **legacy_11** (pre-2026-11-23): excluded MCH, MCHC, MPV, NRBC, basophil % and the five
   absolute differential counts. Worst survey-weighted VIF was ~808 (`LBXNEPCT`).
2. **historical_21** (2026-11-23 cohort-summary decision): briefly kept all 21 CBC variables.
   Differential percentages sum to 100.0–100.2%
   (mean 100.125%) by construction, so any 4 of the 5 determine the 5th;
   combined with MCH/MCHC/absolute-count redundancy this drove worst VIF to ~26,000
   (`LBXNEPCT`).
3. **current** (locked default as of Phase 15 Step 3, this report): the 9-feature set below,
   after every one of the 12 dropped `historical_21` columns was confirmed by direct
   marginal-addition testing (add it back alone, measure AUROC over 25 repeated PSU-grouped
   folds) to add no measurable gain -- see `docs/findings/feature_reduction.md`.

Largest survey-weighted VIFs in the **current 9-predictor block**:

- LBXHCT: weighted VIF 144.4.
- LBXRBCSI: weighted VIF 135.1.
- LBXMCVSI: weighted VIF 55.5.
- LBXHGB: weighted VIF 18.9.

This is a >180x reduction from `historical_21`'s worst VIF (~26,000) and still an improvement
on `legacy_11`'s (~808) — the remaining collinearity is just the expected, mild
RBC/MCV/HCT/HGB red-cell-index relationship (hematocrit approximately equals RBC × MCV / 10;
median absolute residual 0.0334
hematocrit percentage points). MCH and MCHC are no longer predictors in the current block (they
were dropped as algebraically redundant with HGB/RBC/HCT, confirmed by direct test, not just
VIF), so those near-identities are reported here only as historical context: MCH ≈ HGB × 10 / RBC
(median absolute residual 0.0578 pg)
and MCHC ≈ HGB × 100 / HCT (median absolute residual
0.0667 g/dL). The white-cell/platelet/
differential features in the current block (WBC, platelets, lymphocyte/monocyte/eosinophil %)
now show essentially no collinearity (VIF ≈ 1) — the two differential percentages dropped
(neutrophil %, basophil %) were exactly what drove the `historical_21` compositional blow-up.

## Matched nested comparison

Both models use demographics and BMI. Only the CBC representation changes. PCA
retains 95% variance with component counts [7] across inner/outer training fits.
Scaling/PCA are unweighted; classifiers, calibration and evaluation use WTPH2YR.
Five outer / three inner PSU-grouped folds match the extension. Calibration and
95%-weighted-sensitivity thresholds use development data only.

| Model | AUROC | AP | Brier | Log loss | Deferred | Missed / 106 |
|---|---:|---:|---:|---:|---:|---:|
| demographics_bmi_cbc | 0.8347 | 0.0865 | 0.01897 | 0.08364 | 1601 | 2 |
| demographics_bmi_cbc_pca95 | 0.8349 | 0.0877 | 0.01897 | 0.08355 | 1613 | 3 |

Deferred and missed are observed counts; the development sensitivity target does
not guarantee held-out sensitivity. Conditional design intervals are exported,
but exclude refitting/split uncertainty; no superiority or clinical-safety claim
is established by this exploratory comparison. The older cycle was not reused.

## Figures and verification

![Descriptive scree and PC1/PC2](../../results/cbc_diagnostics/cbc_pca_diagnostics.png)

The whole-cohort figure and loadings are descriptive and never enter validation.
PCA maximizes predictor variance, not outcome separation. Components/loadings are
not causal effects. Re-run `python scripts/analysis/cbc_diagnostics.py` from the root.

Checks passed for saved raw-CBC prediction reproduction, matched subjects/folds,
all 40 inner/outer fit audits, PSU separation, PCA training sample counts, and
finite unique predictions. See [validation](../verification/cbc_diagnostics_validation.json)
and [analysis specification](../methods/phase7_analysis_protocol.md).
PCA projections are checked against independent non-BLAS contractions. The local
NumPy/Apple BLAS build emitted matmul floating-point warnings despite finite,
matching results; these warnings are accepted only after that numerical check.

This supplies additional reproducible methods, a meaningful matched baseline,
variability estimates and explicit limitations for the final-project rubric.
Team review and integration with the other cohort/endpoint proposals remain open.
