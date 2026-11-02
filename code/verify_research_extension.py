"""Independently verify saved research-extension accounting and frozen inference."""
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
import nbformat
import joblib
from sklearn.metrics import roc_auc_score
from research_extension import ROOT,OUT,PRIMARY,load_cycle,logits

full,d=load_cycle('L');full_j,external=load_cycle('J')
assert len(d)==4612 and d.target.sum()==106
assert len(external)==3943 and external.target.sum()==132
assert not set(d.SEQN)&set(external.SEQN)
for entry in json.loads((ROOT/'data/extension_download_manifest.json').read_text()):
    payload=(ROOT/entry['path']).read_bytes()
    assert len(payload)==entry['bytes']
    assert hashlib.sha256(payload).hexdigest()==entry['sha256']
metadata=json.loads((OUT/'extension_metadata.json').read_text())
assert metadata['protocol_sha256']==hashlib.sha256((ROOT/'reports/extension_analysis_protocol.md').read_bytes()).hexdigest()
comparison=pd.read_csv(OUT/'extension_model_comparison.csv')
pred=pd.read_csv(OUT/'primary_extension_predictions.csv')
assert len(pred)==len(d)*7 and not pred.duplicated(['SEQN','model']).any()
assert pred.groupby(['model','SDMVSTRA','SDMVPSU']).fold.nunique().eq(1).all()
assert pred.groupby('SEQN').fold.nunique().eq(1).all()
assert pred.groupby('model').target.sum().eq(106).all()
assert pred._weight.gt(0).all()
expected_ids=set(d.SEQN)
for name,g in pred.groupby('model'):
    assert set(g.SEQN)==expected_ids
    point=comparison[comparison.analysis.eq('primary')&comparison.model.eq(name)&comparison.stage.eq('calibrated')].iloc[0]
    y=g.target.to_numpy();w=g._weight.to_numpy();p=g.calibrated.to_numpy();flag=g.flagged.to_numpy()
    assert np.isfinite(p).all() and ((p>=0)&(p<=1)).all()
    assert np.isclose(point.AUROC,roc_auc_score(y,p,sample_weight=w))
    assert np.isclose(point.Brier,np.sum(w*(p-y)**2)/w.sum())
    assert point.deferred_n==int((~flag).sum())
    assert point.missed_n==int(((y==1)&~flag).sum())
    assert np.isclose(point.sensitivity,w[(y==1)&flag].sum()/w[y==1].sum())
    assert g.groupby('fold').threshold.nunique().eq(1).all()

ha=pd.read_csv(OUT/'fasting_hba1c_predictions.csv')
fg=pd.read_csv(OUT/'fasting_glucose_predictions.csv')
assert len(ha)==len(fg)==2375*3
ha=ha.sort_values(['model','SEQN']).reset_index(drop=True)
fg=fg.sort_values(['model','SEQN']).reset_index(drop=True)
assert ha[['model','SEQN','fold']].equals(fg[['model','SEQN','fold']])
assert np.allclose(ha._weight,fg._weight)
for name,g in fg.groupby('model'):
    linked=g.merge(d[['SEQN','LBXGLU','WTSAF2YR']],on='SEQN',validate='one_to_one')
    assert linked.WTSAF2YR.gt(0).all() and linked.LBXGLU.notna().all()
    assert linked.target.eq(linked.LBXGLU.ge(126).astype(int)).all()
    assert linked.target.sum()==90
assert ha.groupby('model').target.sum().eq(60).all()

boot=pd.read_csv(OUT/'full_refit_bootstrap_replicates.csv')
assert len(boot)==300 and boot.replicate.nunique()==100
assert not boot.duplicated(['replicate','model']).any()
assert json.loads((OUT/'bootstrap_failures.json').read_text())==[]
interval=pd.read_csv(OUT/'full_refit_bootstrap_intervals.csv')
wide=boot.pivot(index='replicate',columns='model',values='AUROC')
delta=wide.demographics_bmi_cbc-wide.demographics_bmi
row=interval[interval.model.eq('CBC_minus_BMI_AUROC')].iloc[0]
assert np.isclose(row.lower,np.quantile(delta,.025)) and np.isclose(row.upper,np.quantile(delta,.975))

transport=pd.read_csv(OUT/'independent_cycle_predictions.csv')
for entry in json.loads((OUT/'frozen_model_manifest.json').read_text()):
    path=OUT/f'frozen_models/{entry["model"]}.joblib'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256']
    saved=joblib.load(path)
    # Reproduce independent inference solely from saved development artifacts.
    raw=saved['model'].predict_proba(external[saved['features']])[:,1]
    calibrated=saved['calibrator'].predict_proba(logits(raw))[:,1]
    got=transport[transport.model.eq(entry['model'])].set_index('SEQN').loc[external.SEQN]
    assert np.allclose(got.raw,raw) and np.allclose(got.calibrated,calibrated)
    assert np.allclose(got.threshold,entry['threshold'],rtol=1e-12,atol=1e-15)
    assert got.flagged.eq(calibrated>=entry['threshold']).all()
    assert got.target.sum()==132
    assert len(saved['features'])==len(set(saved['features']))
    assert not set(['LBXGH','target','DIQ010','DIQ050','DIQ070','LBXGLU','SDMVSTRA','SDMVPSU'])&set(saved['features'])

for name in ['05_bmi_and_biological_sensitivity.ipynb','06_resampling_and_independent_validation.ipynb']:
    nb=nbformat.read(ROOT/'code'/name,as_version=4);nbformat.validate(nb)
    assert all(c.execution_count for c in nb.cells if c.cell_type=='code')
    assert not any(o.output_type=='error' for c in nb.cells if c.cell_type=='code' for o in c.outputs)
evidence=pd.read_csv(ROOT/'literature_review/extension_evidence_matrix.csv')
assert len(evidence)==21 and evidence.source.notna().all()
result=dict(status='passed',current_participants=4612,current_positives=106,
    independent_participants=3943,independent_positives=132,fasting_participants=2375,
    bootstrap_successful=100,bootstrap_failures=0,evidence_sources=21,
    checks=['download hashes','protocol hash','matched participants and clusters',
            'weighted metrics and policy accounting','matched fasting endpoints and weights',
            'full-refit replicate counts and paired intervals','frozen model hashes and reproducible inference',
            'predictor leakage exclusions','notebook schemas and completed results cells'])
(ROOT/'reports/research_extension_validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
