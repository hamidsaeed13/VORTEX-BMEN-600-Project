# CBC collinearity and PCA supplement — 2026-11-16

Exploratory Phase 7 supplement on the fixed 4,612 adults / 106 positive HbA1c labels.
The original primary analysis and independent-cycle results are preserved.

## Collinearity

Differential percentages sum to 100.0–100.2%
(mean 100.125%). Basophil percentage was already removed in the
extension; this supplement uses the same 11 predictors. Rounding makes the released
sum approximately fixed. All-12 and drop-basophil VIFs are exported with ordinary
and survey-weighted auxiliary regressions and an intercept.
Dropping a rare component does not remove the strong approximate dependence among
the remaining percentages; high VIF persists and motivates the PCA sensitivity arm.

Largest survey-weighted VIFs after dropping basophil percentage:

- LBXNEPCT: weighted VIF 808.1.
- LBXLYPCT: weighted VIF 686.5.
- LBXHCT: weighted VIF 145.8.
- LBXRBCSI: weighted VIF 135.1.

Hematocrit approximately equals RBC × MCV / 10; the median absolute residual is
0.0334 hematocrit percentage points.
HGB/HCT-derived MCH/MCHC relationships are relevant background, but MCH/MCHC are
not among this study's predictors. High VIF does not justify causal interpretation,
nor does it automatically invalidate penalized prediction. Retain the existing
regularized raw-feature model and treat PCA as a secondary robustness comparison.

## Matched nested comparison

Both models use demographics and BMI. Only the CBC representation changes. PCA
retains 95% variance with component counts [7] across inner/outer training fits.
Scaling/PCA are unweighted; classifiers, calibration and evaluation use WTPH2YR.
Five outer / three inner PSU-grouped folds match the extension. Calibration and
95%-weighted-sensitivity thresholds use development data only.

| Model | AUROC | AP | Brier | Log loss | Deferred | Missed / 106 |
|---|---:|---:|---:|---:|---:|---:|
| demographics_bmi_cbc | 0.8226 | 0.0812 | 0.01902 | 0.08465 | 1474 | 3 |
| demographics_bmi_cbc_pca95 | 0.8237 | 0.0832 | 0.01902 | 0.08444 | 1586 | 3 |

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
