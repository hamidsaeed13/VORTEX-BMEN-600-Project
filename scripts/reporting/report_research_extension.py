"""Generate interpretation tables, figures, draft text and results notebooks."""
from pathlib import Path
import base64
import io
import contextlib
import numpy as np
import pandas as pd
import nbformat
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import t
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts/analysis'))
from research_extension import ROOT,OUT,PRIMARY,load_cycle,metrics

def md(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+
                     ['| '+' | '.join(map(str,row))+' |' for row in rows])

def paired_interval(pred,full,label):
    design=full.loc[full._weight.gt(0),['SDMVSTRA','SDMVPSU']].drop_duplicates()
    a=pred[pred.model.eq('demographics_bmi_cbc')].sort_values('SEQN').reset_index(drop=True)
    b=pred[pred.model.eq('demographics_bmi')].sort_values('SEQN').reset_index(drop=True)
    assert a.SEQN.equals(b.SEQN)
    result=[]
    for metric in ['AUROC','AP','Brier']:
        gain=metrics(a)[metric]-metrics(b)[metric];variance=0
        for h,hg in design.groupby('SDMVSTRA'):
            estimates=[];m=len(hg)
            for psu in hg.SDMVPSU:
                zs=[]
                for g in [a,b]:
                    z=g.copy();inside=z.SDMVSTRA.eq(h)
                    z.loc[inside,'_weight']*=m/(m-1)
                    z.loc[inside&z.SDMVPSU.eq(psu),'_weight']=0
                    zs.append(metrics(z)[metric])
                estimates.append(zs[0]-zs[1])
            variance+=(m-1)/m*np.sum((np.array(estimates)-np.mean(estimates))**2)
        se=np.sqrt(variance);critical=t.ppf(.975,len(design)-design.SDMVSTRA.nunique())
        result.append(dict(analysis=label,metric=metric,gain=gain,SE=se,lower=gain-critical*se,upper=gain+critical*se))
    return result

def main():
    all_results=pd.read_csv(OUT/'extension_model_comparison.csv')
    results=all_results[all_results.stage.eq('calibrated')]
    counts=pd.read_csv(OUT/'cycle_counts.csv')
    intervals=pd.read_csv(OUT/'full_refit_bootstrap_intervals.csv')
    full,d=load_cycle('L');full_j,external=load_cycle('J')
    pred=pd.read_csv(OUT/'primary_extension_predictions.csv')
    transport=pd.read_csv(OUT/'independent_cycle_predictions.csv')
    paired=pd.DataFrame(paired_interval(pred,full,'primary')+paired_interval(transport,full_j,'independent_cycle'))
    paired.to_csv(OUT/'paired_conditional_design_gains.csv',index=False)
    primary=results[results.analysis.eq('primary')&results.model.isin(PRIMARY)]
    ext=results[results.analysis.eq('transport_2017_2018')]
    table=md(['Predictors','Current-cycle OOF AUROC','Independent-cycle AUROC','Current Brier','Independent Brier'],
        [[name,f'{primary.set_index("model").loc[name,"AUROC"]:.3f}',
          f'{ext.set_index("model").loc[name,"AUROC"]:.3f}',
          f'{primary.set_index("model").loc[name,"Brier"]:.5f}',
          f'{ext.set_index("model").loc[name,"Brier"]:.5f}'] for name in PRIMARY])
    gains=[]
    for analysis,g in results[results.model.isin(PRIMARY)].groupby('analysis',sort=False):
        z=g.set_index('model');gain=z.loc['demographics_bmi_cbc','AUROC']-z.loc['demographics_bmi','AUROC']
        gains.append([analysis,int(z.loc['demographics_bmi','n']),int(z.loc['demographics_bmi','positives']),
                      f'{z.loc["demographics_bmi","AUROC"]:.3f}',f'{z.loc["demographics_bmi_cbc","AUROC"]:.3f}',f'{gain:+.3f}'])
    sensitivity_table=md(['Analysis','N','Positives','BMI baseline AUROC','BMI+CBC AUROC','CBC gain'],gains)
    boot_gain=intervals[intervals.model.eq('CBC_minus_BMI_AUROC')].iloc[0]
    pi=primary.set_index('model');ei=ext.set_index('model')
    gain=pi.loc['demographics_bmi_cbc','AUROC']-pi.loc['demographics_bmi','AUROC']
    policy=md(['Model','Weighted sensitivity','Weighted deferred %','Observed deferred N','Observed missed positives'],
        [[r.model,f'{r.sensitivity:.3f}',f'{100*r.deferred_fraction:.1f}',r.deferred_n,r.missed_n] for r in primary.itertuples()])
    # Main comparison figure.
    fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    names=list(PRIMARY);labels=['Demographics','+ BMI','+ BMI + CBC']
    for ax,frame,title in [(axes[0],primary,'2021–2023: nested grouped CV'),(axes[1],ext,'2017–2018: frozen models')]:
        ax.bar(labels,[frame.set_index('model').loc[n,'AUROC'] for n in names],color=['#999999','#4c78a8','#59a14f'])
        ax.set(ylim=(0,1),ylabel='Survey-weighted AUROC',title=title)
        for i,name in enumerate(names):ax.text(i,frame.set_index('model').loc[name,'AUROC']+.015,f'{frame.set_index("model").loc[name,"AUROC"]:.3f}',ha='center')
    fig.suptitle('Figure 1. Matched BMI comparison and independent-cycle transport')
    fig.tight_layout();fig.savefig(OUT/'bmi_transport_comparison.png',dpi=170);plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,5))
    labels2=[row[0] for row in gains];values=[float(row[-1]) for row in gains]
    ax.barh(labels2,values,color=['#59a14f' if v>=0 else '#e15759' for v in values])
    ax.axvline(0,color='black',lw=.8);ax.set(xlabel='Weighted AUROC: BMI+CBC minus BMI baseline',title='Figure 2. CBC gain is not consistent across sensitivity analyses')
    fig.tight_layout();fig.savefig(OUT/'sensitivity_gains.png',dpi=170);plt.close(fig)
    # Independent probability calibration, no recalibration using evaluation labels.
    bins=[]
    fig,ax=plt.subplots(figsize=(7,5))
    for name,g in transport.groupby('model'):
        g=g.sort_values('calibrated').copy();g['bin']=np.minimum(((g._weight.cumsum()-g._weight/2)/g._weight.sum()*5).astype(int),4)
        rows=[]
        for binid,z in g.groupby('bin'):
            row=dict(model=name,bin=binid,n=len(z),positives=int(z.target.sum()),
                predicted=np.average(z.calibrated,weights=z._weight),observed=np.average(z.target,weights=z._weight))
            rows.append(row);bins.append(row)
        ax.plot([r['predicted'] for r in rows],[r['observed'] for r in rows],'o-',label=name)
    ax.plot([0,.10],[0,.10],'k--');ax.set(xlabel='Weighted predicted risk',ylabel='Weighted observed fraction',title='Figure 3. Independent-cycle calibration (five equal-weight bins)')
    ax.legend(fontsize=8);fig.tight_layout();fig.savefig(OUT/'independent_cycle_calibration.png',dpi=170);plt.close(fig)
    pd.DataFrame(bins).to_csv(OUT/'independent_cycle_calibration_bins.csv',index=False)
    # Expose the fitted specification and reproducible coefficients for the frozen models.
    import joblib
    coefficients=[]
    for name in PRIMARY:
        saved=joblib.load(OUT/f'frozen_models/{name}.joblib')
        model=saved['model']
        for feature,value in zip(model.named_steps['pre'].get_feature_names_out(),model.named_steps['clf'].coef_[0]):
            coefficients.append(dict(model=name,feature=feature,coefficient=value))
    pd.DataFrame(coefficients).to_csv(OUT/'frozen_logistic_coefficients.csv',index=False)
    report=f'''# Research extension: BMI, biological sensitivity and independent evaluation

## What changed scientifically

The original cohort was retained (4,612 adults; 106 positive HbA1c labels). BMI is observed in
4,560 participants; the 52 missing values are training-fold median-imputed, with missingness
indicators. The independent 2017–2018 cohort has 3,943 participants and 132 positive labels.
All primary comparisons within a sample use identical participants and splits.

### Table 1. Weighted, calibrated discrimination and probability error

{table}

The incremental CBC AUROC gain after BMI is **{gain:.3f}**. This is smaller than the earlier
comparison against demographics without BMI. It is not a direct update of notebook 04's
numbers: the new specification also adds numeric missingness indicators and removes basophil
percentage from predictors to remove the differential-composition dependency. Models are
regularized, not interpreted as causal effects; other red-cell collinearity remains.

One hundred stratified PSU resamples refitted preprocessing, all inner and outer models,
calibration and development-selected thresholds. All 100 completed. The exploratory 95%
percentile interval for CBC-minus-BMI AUROC is **{boot_gain.lower:.3f} to {boot_gain.upper:.3f}**.
It includes zero. This is stronger than holding fitted scores fixed but not definitive:
the outer/inner splits and hyperparameters are fixed, there are only 15 variance strata,
and 100 resamples give limited tail precision. The code supports increasing --bootstrap
for a higher-precision follow-up; coverage is not validated for this rare-event learning
procedure. Duplicate sampled records retain their original fold assignment to prevent leakage.

### Table 2. Sensitivity and endpoint comparisons

{sensitivity_table}

The CBC gain is smaller after excluding low hemoglobin and reverses among the age-20–65
low-hemoglobin-excluded participants. Those comparisons have fewer events and different
case mix/folds; they cannot prove anemia causes the original signal. Red-cell-only and
white-cell/platelet-only models, included in the full CSV, separate predictor blocks rather
than establish mechanisms. The low-Hgb flag (<12 g/dL female, <13 male) is operational:
it omits altitude/smoking corrections, iron deficiency without anemia and hemoglobin variants.
The 20–65 restriction respects the age coverage of the WHO cutoff table; the all-age flag
is an explicit extrapolation sensitivity, not a validated geriatric anemia definition.

Fasting analyses use the same 2,375 positive-WTSAF2YR participants for both endpoints.
There are 60 HbA1c positives and 90 FPG positives: 41 meet both, 19 HbA1c only, and 49 FPG
only. Thus 68 people have discordant single-test labels. The glucose and HbA1c comparisons
use the same folds and fasting weights; neither endpoint is a confirmed clinical diagnosis.
Their modest CBC gains do not establish that all HbA1c signal is glucose-specific.

## Independent-cycle evaluation

All three model pipelines, calibrators and thresholds were fitted in 2021–2023, saved and
hashed before evaluating the 2017–2018 outcomes. No independent-sample recalibration, feature
selection or threshold search was performed. AUROC improves from 0.762 to 0.799 after CBC,
but **Brier error worsens** from 0.01987 to 0.02059, and log loss also worsens. Mean CBC-model
risk is 2.29% against 2.06% weighted observed prevalence. Better ranking therefore does not
mean uniformly better probability estimates or clinical utility.

This is independent earlier-cycle transport, not prospective or hospital-system validation.
The older cycle uses WTMEC2YR while the current cycle uses WTPH2YR; both have appropriate
cycle-specific design variables. CBC units/coding were aligned. CDC documents a current-cycle
HbA1c instrument transition and reports no adjustment needed after bridging, but assay and
population shifts remain limitations. See cycle_harmonization.md. Independent-sample
conditional jackknife intervals and paired gains are exported separately; these condition
on models developed in the current cycle.

## Exploratory policy value

### Table 3. Outer-fold policies targeting 95% sensitivity during development

{policy}

The primary CBC model achieves {100*pi.loc['demographics_bmi_cbc','sensitivity']:.1f}% weighted
sensitivity, below the development target. Weighted deferral is almost identical between
BMI and BMI+CBC models (about 38.1%); raw observed deferred counts differ because weights
vary. This is an important limitation of interpreting the AUROC increase as a large reduction
in testing. The saved matched-burden table fixes weighted testing fractions descriptively;
those held-out descriptive thresholds are not selected deployable cutoffs.

Decision curves compare models with test-all/test-none over assumed risk thresholds
0.005–0.10. The assumed harm ratio is threshold/(1-threshold); no measured cost data or
clinician-approved harm ratio is available. Curves show hypothetical preferences, not
actual savings, safety, or a clinically endorsed cutoff. No model should be used to withhold
testing on this evidence alone.

## Selection, missingness and subgroup checks

Forty-five otherwise eligible participants lack complete labs: only 24 have observed HbA1c,
and the other 21 must not be labelled negative. selection_audit.csv contrasts their available
characteristics with included records; a descriptive audit cannot remove selection bias.
Income-to-poverty ratio is missing in about 12.8% of the included cohort; adult education has
two missing records, BMI 52. Median/mode imputation and numeric missingness indicators are
fitted only in training samples. The BMI-observed sensitivity retains 4,560/105 participants/
positive labels and shows the finding does not solely depend on BMI imputation.

Subgroup metrics by recorded sex, age and race/ethnicity are descriptive, with positive
counts; groups with fewer than 10 events have performance suppressed. This is not a formal
fairness assessment, and small-group uncertainty cannot support claims of equal performance.
Race/ethnicity categories reflect recorded survey categories, not causal biology.

## Reproducibility and figures

Install requirements.txt. Acquire missing public inputs with
python scripts/data/acquire_extension_data.py. Run python scripts/analysis/research_extension.py --bootstrap 100,
then python scripts/reporting/report_research_extension.py and python scripts/verification/verify_research_extension.py.
The acquisition manifest records URLs, retrieval times and hashes; frozen-model hashes and
coefficients accompany the predictions. Requirements include joblib for model artifacts.
Models are trusted project artifacts; do not load untrusted joblib files.

Notebook 05 summarizes BMI and sensitivity results; notebook 06 summarizes resampling and
independent-cycle evaluation. By default they read verified saved outputs; setting RUN_ANALYSIS
in notebook 05 reruns the full extension. Figure 1 is the matched BMI/transport comparison;
Figure 2 displays all sensitivity gains including the negative result; Figure 3 shows independent
calibration. decision_curves.png is an exploratory supplementary figure.

## Interpretation for a paper

CBC contains additional ranking information beyond demographics and BMI in these samples,
but its gain is modest, uncertain under full-procedure resampling, and not consistent across
all biological sensitivity analyses. Independent-cycle probability error worsens despite
better discrimination. This supports a cautious incremental-value/robustness paper, not a
claim that CBC safely replaces HbA1c screening.

The literature synthesis and 21-source evidence matrix are in literature/extension_*.
The publication-readiness assessment distinguishes work completed here from clinical,
institutional and independent-review decisions that remain. Negative findings should be part
of the paper's contribution, not removed to obtain a stronger headline.
'''
    (ROOT/'docs/findings/research_extension_results.md').write_text(report)
    draft=f'''# Draft Methods and Results insertion — requires team review

## Focused research question

Among adults without reported diabetes, does CBC improve identification of diabetes-range
HbA1c beyond demographics and BMI, and is its incremental value robust to blood-cell-related
measurement effects and independent-cycle evaluation?

## Methods

We linked NHANES August 2021–August 2023 demographics, CBC, HbA1c, diabetes questionnaire,
body measures and fasting-glucose components by unique participant identifier. The primary
cohort comprised 4,612 examined adults aged ≥20 years with positive phlebotomy weights,
explicitly reporting no prior diabetes diagnosis, no reported current diabetes medication,
observed HbA1c and complete selected CBC measures. Recorded pregnancy and indeterminate
pregnancy status in females aged 20–44 were excluded; public data could not establish
pregnancy status outside that reporting range. HbA1c ≥6.5% defined a laboratory outcome,
not confirmed diabetes. Original download dates for pre-existing inputs remain unverified;
new-file acquisition is documented in the manifest.

Three prespecified logistic models compared demographics, demographics plus BMI, and
demographics plus BMI plus CBC. Preprocessing, survey-weighted classifiers, calibration
and sensitivity-targeted thresholds were refitted within nested grouped validation. Five
outer folds and three inner folds kept masked survey PSUs together. We used 100 stratified
PSU resamples with refitting of the full pipeline for exploratory uncertainty, conditional
on fixed split assignments. Predictor-block, low-hemoglobin, age-restricted and fasting-endpoint
analyses examined robustness. Frozen current-cycle models were evaluated without updating
in a distinct 2017–2018 cohort using its examination weights. Methods and exceptions are
specified in docs/methods/extension_analysis_protocol.md and docs/methods/cycle_harmonization.md.

## Results

{table}

The BMI-adjusted CBC AUROC gain was {gain:.3f}, with full-refit resampling percentile bounds
{boot_gain.lower:.3f} to {boot_gain.upper:.3f}. The gain diminished with low-hemoglobin exclusion
and reversed in the restricted age-20–65, low-hemoglobin-excluded sensitivity cohort. In the
independent 2017–2018 sample (3,943 participants, 132 positive outcomes), CBC improved AUROC
but worsened Brier error and log loss. These mixed results limit an interpretation of uniform
clinical benefit. The main development-selected CBC policy missed three observed positives;
it did not establish safe deferral or economic savings.

## Discussion direction

Discuss the smaller gain beyond BMI, endpoint discordance and red-cell influences in relation
to the closest studies, not headline AUROCs from unlike endpoints. Frame the study as
incremental-value and robustness evaluation. Report independent calibration limitations and
resampling uncertainty. These draft paragraphs need integration with citations, figures,
the final manuscript's reference numbering, verified contributions and AI-use disclosure.
'''
    (ROOT/'writing/drafts/Research_Extension_Methods_Results.md').write_text(draft)
    make_notebooks(table,sensitivity_table)
    print(table)
    print('Full refit CBC gain bounds:',boot_gain.lower,boot_gain.upper)

def make_notebooks(table,sensitivity_table):
    for number,title,figures in [
        (5,'BMI comparison and biological sensitivity',['bmi_transport_comparison.png','sensitivity_gains.png']),
        (6,'Full-refit uncertainty and independent-cycle evaluation',['independent_cycle_calibration.png','decision_curves.png'])]:
        n=nbformat.v4.new_notebook()
        n.metadata['kernelspec']=dict(name='python3',language='python',display_name='Python 3')
        n.metadata['language_info']=dict(name='python',version='3.9.6')
        n.cells.append(nbformat.v4.new_markdown_cell(f'''# {number:02d} — {title}

This results notebook reads the completed extension outputs. The executable analysis lives
in `research_extension.py`; the analysis protocol predates extension results. Original notebooks
01–04 remain separate. Run from the root or notebooks directory after installing requirements.txt.
Notebook 05 can rerun all analyses and 100 full-refit replicates by setting RUN_ANALYSIS=True.

See [full interpretation](../docs/findings/research_extension_results.md),
[harmonization](../docs/methods/cycle_harmonization.md), and
[literature matrix](../literature/extension_evidence_matrix.md).
This is exploratory research; no safe clinical deferral policy is established.'''))
        setup='''from pathlib import Path
import sys
import pandas as pd
ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / 'CODEX.md').is_file())
sys.path.insert(0, str(ROOT / 'scripts/analysis'))
OUT = ROOT / 'results/research_extension'
'''
        if number==5:
            setup+='''RUN_ANALYSIS = False
if RUN_ANALYSIS:
    import research_extension
    research_extension.main(count=100)
'''
        n.cells.append(nbformat.v4.new_code_cell(setup))
        n.cells.append(nbformat.v4.new_markdown_cell(table+'\n\n'+(sensitivity_table if number==5 else
            'The 100-replicate CBC gain interval includes zero. Independent-cycle AUROC improves while Brier/log-loss worsen. Bootstrap intervals fix splits; independent jackknife intervals fix developed models.')))
        files=(['extension_model_comparison.csv','selection_audit.csv'] if number==5 else
               ['full_refit_bootstrap_intervals.csv','paired_conditional_design_gains.csv','cycle_counts.csv'])
        code='\n'.join(f"print('\\n{f}')\nprint(pd.read_csv(OUT / '{f}').to_string(index=False))" for f in files)
        n.cells.append(nbformat.v4.new_code_cell(code))
        namespace={}
        counter=0
        for cell in n.cells:
            if cell.cell_type=='code':
                counter+=1;buf=io.StringIO()
                with contextlib.redirect_stdout(buf):exec(cell.source,namespace)
                cell.execution_count=counter;cell.outputs=[nbformat.v4.new_output('stream',name='stdout',text=buf.getvalue())]
        for file in figures:
            n.cells.append(nbformat.v4.new_markdown_cell(f'Generated figure: `{file}`. Interpret alongside the report; subgroup changes and assumed utility trade-offs do not establish causation or safety.'))
            c=nbformat.v4.new_code_cell(f"from IPython.display import Image, display\ndisplay(Image(filename=str(OUT / '{file}')))")
            counter+=1;c.execution_count=counter
            c.outputs=[nbformat.v4.new_output('display_data',data={'image/png':base64.b64encode((OUT/file).read_bytes()).decode()},metadata={})]
            n.cells.append(c)
        nbformat.validate(n)
        name='05_bmi_and_biological_sensitivity.ipynb' if number==5 else '06_resampling_and_independent_validation.ipynb'
        nbformat.write(n,ROOT/'notebooks'/name)

if __name__=='__main__':main()
