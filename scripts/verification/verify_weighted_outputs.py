"""Independent accounting checks for saved weighted analysis outputs."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import nbformat

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'results/weighted_calibration'
p = pd.read_csv(OUT/'weighted_oof_predictions.csv')
m = pd.read_csv(OUT/'weighted_metrics_intervals.csv')
r = pd.read_csv(OUT/'conditional_jackknife_replicates.csv')
policy = pd.read_csv(OUT/'development_policy_evaluation.csv').set_index('model')
audit = pd.read_csv(OUT/'split_audit.csv')
design = pd.read_csv(OUT/'full_design_psus.csv')
assert len(p)==4612*4 and not p.duplicated(['model','SEQN']).any()
assert len(audit)==60 and audit.cluster_overlap.eq(0).all()
assert audit[['train_positive','validation_positive']].gt(0).all().all()
assert p.groupby(['model','stratum','psu']).fold.nunique().eq(1).all()
assert p.groupby(['SEQN']).fold.nunique().eq(1).all()  # Same splits across models
assert p.groupby('model').target.sum().eq(106).all()
for name, g in p.groupby('model'):
    weight, y = g.weight.to_numpy(), g.target.to_numpy()
    assert len(g)==4612 and (weight>0).all()
    for stage in ['raw','calibrated','train_prevalence']:
        q=g[stage].to_numpy()
        assert np.isfinite(q).all() and ((q>=0)&(q<=1)).all()
        expected={'prevalence': np.sum(weight*y)/sum(weight),
                  'mean_prediction': np.sum(weight*q)/sum(weight),
                  'Brier': np.sum(weight*(y-q)**2)/sum(weight)}
        for metric,value in expected.items():
            actual=m[m.model.eq(name)&m.stage.eq(stage)&m.metric.eq(metric)].estimate.item()
            assert np.isclose(value,actual,rtol=1e-10,atol=1e-12)
    flag=g.flagged.astype(bool).to_numpy()
    # Check integer counts and weighted sensitivity/NPV independently.
    assert policy.loc[name,'n_deferred']==int((~flag).sum())
    assert policy.loc[name,'positives_missed']==int(((y==1)&~flag).sum())
    assert np.isclose(policy.loc[name,'sensitivity'],weight[(y==1)&flag].sum()/weight[y==1].sum())
    assert np.isclose(policy.loc[name,'NPV'],weight[(y==0)&~flag].sum()/weight[~flag].sum())
    assert g.groupby('fold').development_threshold.nunique().eq(1).all()
    # Independently calculate jackknife prevalence from PSU-level totals, rather
    # than reusing the analysis's record-level replicate-weight function.
    total_num=np.dot(weight,y)
    total_den=weight.sum()
    for h, hg in design.groupby('SDMVSTRA'):
        inside=g.stratum.eq(h)
        n_psu=len(hg)
        hn=np.dot(weight[inside],y[inside]); hd=weight[inside].sum()
        for psu in hg.SDMVPSU:
            deleted=inside & g.psu.eq(psu)
            dn=np.dot(weight[deleted],y[deleted]); dd=weight[deleted].sum()
            value=(total_num-hn+(hn-dn)*n_psu/(n_psu-1))/(total_den-hd+(hd-dd)*n_psu/(n_psu-1))
            actual=r[r.model.eq(name)&r.stage.eq('raw')&r.metric.eq('prevalence')&r.stratum.eq(h)&r.deleted_psu.eq(psu)].estimate.item()
            assert np.isclose(value,actual,rtol=1e-10)
nb=nbformat.read(ROOT/'notebooks/04_survey_weighted_calibration.ipynb',as_version=4)
nbformat.validate(nb)
assert all(c.execution_count for c in nb.cells if c.cell_type=='code')
assert not any(o.output_type=='error' for c in nb.cells if c.cell_type=='code' for o in c.outputs)
result=dict(status='passed',participants=4612,positive_labels=106,models=4,
            outer_folds=5,inner_fit_audits=60,design_strata=15,design_psus=30,
            checks=['unique predictions','PSU separation','matched model folds','positive weights',
                    'weighted Brier/prevalence/mean risk','weighted sensitivity/NPV',
                    'integer deferred/missed counts','PSU-total jackknife prevalence',
                    'executed notebook schema'])
(ROOT/'docs/verification/weighted_validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
