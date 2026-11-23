# CBC Lasso selection

Phase 13 Step 2 evaluated the 14-feature candidate on the same 4,612 participants
and 106 diabetes-range HbA1c results as the full 21-feature model. The
[penalty rule](../methods/phase13_lasso_protocol.md) was specified before outer
evaluation. All five outer development sets independently selected C = 0.64.
The resulting outer fits retained 11, 10, 10, 12 and 8 CBC terms.

## Performance on matched held-out folds

| Fold | Full 21-feature logistic | Lasso | AUROC change |
|---|---:|---:|---:|
| Pooled | 0.8107 | 0.8158 | +0.0052 |
| 1 | 0.8495 | 0.8427 | −0.0068 |
| 2 | 0.6947 | 0.6974 | +0.0027 |
| 3 | 0.8569 | 0.8628 | +0.0059 |
| 4 | 0.8090 | 0.8129 | +0.0039 |
| 5 | 0.8182 | 0.8352 | +0.0170 |

These are survey-weighted AUROCs from calibrated predictions. The small pooled
gain is descriptive, and one fold favored the full model. The comparison
changes both the starting feature block and the type of regularization, which
also applies to demographics and BMI. It evaluates the selection procedure.
The team still needs to approve a fixed panel and evaluate it in Step 4.
The independent cycle was not used.

## Which CBC terms survived

| Measurement | NHANES variable | Outer fits / 5 | Inner fits / 15 |
|---|---|---:|---:|
| White blood cell count | LBXWBCSI | 5 | 15 |
| Mean corpuscular volume | LBXMCVSI | 5 | 15 |
| Lymphocyte % | LBXLYPCT | 5 | 15 |
| Monocyte % | LBXMOPCT | 5 | 14 |
| Red blood cell count | LBXRBCSI | 5 | 14 |
| Platelet count | LBXPLTSI | 5 | 13 |
| Mean platelet volume | LBXMPSI | 5 | 11 |
| Red cell distribution width | LBXRDW | 4 | 13 |
| Nucleated red blood cells | LBXNRBC | 4 | 13 |
| Eosinophil % | LBXEOPCT | 4 | 10 |
| Basophil % | LBXBAPCT | 3 | 11 |
| Hemoglobin | LBXHGB | 1 | 2 |
| Neutrophil % | LBXNEPCT | 0 | 1 |
| Hematocrit | LBXHCT | 0 | 0 |

Lymphocyte and monocyte percentages were stable across outer fits. Neutrophil
percentage was nearly always excluded. Eosinophil and basophil percentages
were less stable. The pattern shows a consistent preference among the most
collinear percentages, alongside variability in the other percentages.
The counts summarize overlapping training sets and should be read descriptively.

[VIF](../../results/cbc_diagnostics/cbc_vif.csv) was about 25,896 for neutrophil
percentage, 21,916 for lymphocyte percentage and 1,326 for monocyte percentage
in the 14-feature panel. Lasso retained some highly collinear terms while
setting others to zero. These results describe which terms this model used
under the chosen penalty. Correlated terms can provide similar information.

The [held-out permutation analysis](permutation_importance.md) on the full
logistic model showed a larger mean AUROC loss for shuffling white-cell and
platelet features jointly (0.0372) than for shuffling red-cell features jointly
(0.0100). This is consistent with frequent retention of several white-cell and
platelet terms. Several red-cell terms also survived, including red blood
cell count and mean corpuscular volume in every outer fit. The permutation
analysis is grouped and cannot rank individual measurements or estimate the
effect of dropping and retraining on specific terms.

## Reproduce and audit

Run `python scripts/analysis/cbc_lasso_selection.py` from the repository root.
The script checks the refitted baseline against the saved predictions,
thresholds, fold assignments and survey weights. It checks PSU separation
at both levels and exports participant membership, inner validation scores,
selected coefficients and held-out predictions in
[results/cbc_selection](../../results/cbc_selection).

## PCA sensitivity check on the 14-feature candidate

A parallel analysis compared raw CBC features and PCA at 95% retained variance
for both panels, using the same nested folds and L2 logistic regression. Age,
BMI and the other demographic inputs were held fixed. CBC scaling and PCA
were fitted on training data alone. The classifiers, calibrators and AUROC
used phlebotomy weights.

| CBC representation | Components | Pooled weighted AUROC |
|---|---:|---:|
| Full 21, raw | — | 0.8107 |
| Full 21, PCA | 11 | 0.8141 |
| Candidate 14, raw | — | 0.8137 |
| Candidate 14, PCA | 10 | 0.8150 |

PCA compressed the candidate from 14 measurements to 10 components in all
20 training fits. It raised pooled AUROC by 0.0012 versus the same raw panel.
This is a descriptive sensitivity comparison. The independent cycle was not
used, and approval of a fixed feature list remains Step 3.

Reproduce with `python scripts/analysis/cbc_candidate_pca.py`. The
[model comparison](../../results/cbc_selection/pca_model_comparison.csv),
[fit audit](../../results/cbc_selection/pca_fit_audit.csv), and
[held-out predictions](../../results/cbc_selection/pca_oof_predictions.csv)
record the matched evaluation.
