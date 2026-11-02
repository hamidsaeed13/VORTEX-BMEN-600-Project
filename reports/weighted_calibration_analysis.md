# Weighted evaluation and calibration — fixed primary cohort

## Main result

The primary cohort remains 4,612 adults aged 20+ with 106 observed diabetes-range HbA1c results.
Phlebotomy-weighted prevalence is 1.99%.
Table 1 compares calibrated outer-fold predictions from four prespecified models.

| Model | Weighted AUROC | Conditional 95% interval | Average precision | Brier | Mean risk |
| --- | --- | --- | --- | --- | --- |
| age_logistic | 0.652 | 0.601–0.702 | 0.033 | 0.01939 | 1.97% |
| demographics_logistic | 0.715 | 0.650–0.779 | 0.046 | 0.01929 | 1.99% |
| cbc_demographics_logistic | 0.781 | 0.714–0.848 | 0.073 | 0.01904 | 1.99% |
| cbc_demographics_forest | 0.735 | 0.691–0.779 | 0.047 | 0.01925 | 2.01% |

CBC logistic minus demographics logistic weighted AUROC is 0.066,
with a paired conditional design interval of -0.001 to 0.134.
The interval includes zero: these results suggest incremental discrimination but do not clearly
resolve the gain at this uncertainty level. Average precision should be read against the
weighted prevalence of about 0.020; high overall accuracy or NPV alone is uninformative here.

## Fitting and evaluation

The cohort eligibility and public-pregnancy limitations are unchanged from notebook 03.
Unique SEQN merges are checked; when notebook 03's prediction file exists, membership is
verified against it. CBC/demographic predictors exclude outcome, diagnosis, medication,
pregnancy and design variables. Classifiers receive WTPH2YR normalized to mean one within
each training fold. Class balancing is removed to target population risk. This normalization
keeps logistic regularization on a participant-scale rather than a population-total scale.
Imputation, standardization and one-hot encoding are fitted within training folds; imputation
and scaling are unweighted. These weights cannot correct every source of complete-case bias.

Five outer StratifiedGroupKFold splits keep each unique SDMVSTRA:SDMVPSU together.
Within each outer development sample, three grouped inner folds generate out-of-fold scores.
A survey-weighted sigmoid calibrator is fitted to those inner predictions only. The base
classifier is refitted on all outer development records, then raw and calibrated predictions
are generated for the outer held-out clusters. The sigmoid uses logit-clipped probabilities
(1e-6 to 1-1e-6), C=1e6, liblinear, max_iter=2000. Logistic base models use C=1, liblinear,
max_iter=2000. The forest uses 300 trees, min_samples_leaf=5 and seed 42.
No hyperparameters or model winner are selected from the outer results.

The training-fold weighted prevalence predictor is included as a constant-risk baseline.
Raw and calibrated Brier score, log loss, mean prediction, prevalence, AUROC and average
precision are in weighted_metrics_intervals.csv. A mean prediction near prevalence does not
prove calibration across the risk range. Figure 1 (weighted_calibration.png) plots weighted
observed fractions against weighted predicted means in five equal-weight bins. Bin counts
and positive counts are exported; the small number of events limits their precision.
Calibration is not guaranteed to improve every held-out metric. Raw/calibrated curves and
proper scoring rules must be read together.

## Survey uncertainty

The full positive-phlebotomy-weight sample defines 15 variance strata and
30 nested PSUs before the primary analytic domain is selected. For each stratum,
delete one PSU and multiply its sibling PSU weights by m/(m-1). All other strata retain
their weights. PSUs with zero analytic-domain members remain in the design frame.
The stratified jackknife variance is the sum over strata of (m-1)/m times the sum of
squared deviations of replicate estimates from their within-stratum replicate mean.
Intervals use t with 15 design degrees of freedom; bounded metrics are clipped
to [0,1]. CBC-minus-demographics differences use the same replicate weights for pairing.

These are **approximate conditional survey-design intervals for fixed out-of-fold scores
and learned thresholds**. They do not refit models/calibrators in survey replicates, include
training instability, establish external validity, or constitute definitive population inference
for a learned policy. The script exports every replicate for audit. Resampling the full
learning procedure or independent validation remains needed for stronger uncertainty claims.
Strata/PSUs guide validation and variance estimation; they are not predictive covariates.

## Development-selected threshold evaluation

Within each outer development sample, choose the largest calibrated inner-score threshold
achieving at least 95% survey-weighted sensitivity, then apply that frozen threshold to the
outer held-out sample. The 95% goal is a prespecified exploratory research target, not a
clinical safety standard. Thresholds differ by outer fold; this is an evaluation of the
learning procedure, not a single deployable cutoff.

| Model | Weighted sensitivity | Weighted NPV | Weighted deferred % | Observed deferred N | Observed positives missed |
| --- | --- | --- | --- | --- | --- |
| age_logistic | 0.935 | 0.9949 | 25.1 | 788 | 4 |
| cbc_demographics_forest | 0.963 | 0.9973 | 27.7 | 1105 | 6 |
| cbc_demographics_logistic | 0.958 | 0.9969 | 27.2 | 1013 | 3 |
| demographics_logistic | 0.940 | 0.9953 | 25.3 | 860 | 4 |

All observed miss counts use the same 106 positive participants. Weighted sensitivity and
weighted deferred percentages do not equal raw count ratios. The policy CSV includes raw
flagged/deferred counts; the interval CSV includes weighted policy estimates and conditional
intervals. A high NPV with missed cases still cannot justify withholding an HbA1c test.

## Reproduction, validation and next work

Install code/requirements-cohort.txt, then run python code/weighted_calibration_analysis.py
from any directory, or execute notebook 04. Outputs are in code/assets/weighted/.
Numerical RuntimeWarnings were treated as errors during execution. Assertions check cohort
membership, positive weights, unique IDs, binary classes in every split, disjoint clusters,
complete inner predictions, finite outer scores, and one outer score per model/participant.
The split audit records all 60 inner fits and the fold table records 20 outer fits.

These are exploratory internal validation results. Notebook 03's participant-stratified,
class-balanced and unweighted AUROCs differ in several design choices, so changes cannot
be attributed to weighting alone. The outer folds are now inspected and are not an untouched
final test set. No further cohort or threshold optimization should use them as a final test.
Next work is full-procedure uncertainty/independent validation, HbA1c/anemia sensitivity,
and a justified cost/missed-case research policy. Gradient boosting remains optional future
comparison work, not completed here. The final paper must integrate the generated figures,
limitations and AI verification record per the course rubric.

## Sources

- [CDC NHANES variance estimation and domain analysis](https://wwwn.cdc.gov/nchs/nhanes/tutorials/varianceestimation.aspx).
- [CDC NHANES phlebotomy weights](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/GHB_L.htm).
- [scikit-learn calibration guidance](https://scikit-learn.org/stable/modules/calibration.html).
- Local BMEN600 Final Project.pdf, Dataset and Methods, Results and reproducibility requirements.
