"""Matched BMI, biological sensitivity and independent-cycle analyses.

Run: python code/research_extension.py [--bootstrap 100]
The saved protocol defines choices before results; no temporal outcome is used
for fitting, calibration, threshold selection or hyperparameter selection.
"""
from pathlib import Path
import argparse
import hashlib
import json
import time
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from scipy.special import logit
from scipy.stats import t
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import roc_auc_score, average_precision_score, log_loss
import joblib

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'code/assets/extension'
CBC=['LBXWBCSI','LBXRBCSI','LBXHGB','LBXHCT','LBXMCVSI','LBXRDW','LBXPLTSI',
     'LBXLYPCT','LBXNEPCT','LBXMOPCT','LBXEOPCT','LBXBAPCT']
RED=['LBXRBCSI','LBXHGB','LBXHCT','LBXMCVSI','LBXRDW']
WHITE=['LBXWBCSI','LBXPLTSI','LBXLYPCT','LBXNEPCT','LBXMOPCT','LBXEOPCT']
NUM=['RIDAGEYR','INDFMPIR']
CAT=['RIAGENDR','RIDRETH3','DMDEDUC2']
PRIMARY={'demographics':(NUM,False),'demographics_bmi':(NUM+['BMXBMI'],False),
         'demographics_bmi_cbc':(NUM+['BMXBMI']+RED+WHITE,False)}
BLOCKS={'demographics_bmi_red':(NUM+['BMXBMI']+RED,False),
        'demographics_bmi_white_platelet':(NUM+['BMXBMI']+WHITE,False)}
FORESTS={'demographics_bmi_forest':(NUM+['BMXBMI'],True),
         'demographics_bmi_cbc_forest':(NUM+['BMXBMI']+RED+WHITE,True)}

def read(path):
    x=pd.read_sas(path,format='xport')
    assert x.SEQN.is_unique
    for c in x.select_dtypes(include='number'):
        x.loc[x[c].abs().lt(1e-70),c]=0.
    return x

def load_cycle(cycle):
    folder=ROOT/'data/raw' if cycle=='L' else ROOT/'data/raw/2017_2018'
    tables={n:read(folder/f'{n}_{cycle}.xpt') for n in ['DEMO','CBC','GHB','DIQ','BMX','GLU']}
    x=tables['DEMO'].copy()
    selections={'CBC':CBC,'GHB':['LBXGH']+(['WTPH2YR'] if cycle=='L' else []),
                'DIQ':['DIQ010','DIQ050','DIQ070'],'BMX':['BMXBMI'],
                'GLU':['LBXGLU','WTSAF2YR']}
    for n,cols in selections.items():
        x=x.merge(tables[n][['SEQN']+cols],on='SEQN',how='left',validate='one_to_one')
    assert len(x)==len(tables['DEMO'])
    x['DMDEDUC2']=x.DMDEDUC2.replace({7:np.nan,9:np.nan})
    x['_weight']=x['WTPH2YR' if cycle=='L' else 'WTMEC2YR']
    x['group']=x.SDMVSTRA.astype(int).astype(str)+':'+x.SDMVPSU.astype(int).astype(str)
    x['target']=x.LBXGH.ge(6.5).astype(int)
    band=x.RIAGENDR.eq(2)&x.RIDAGEYR.between(20,44)
    x['eligible_before_labs']=(x.RIDSTATR.eq(2)&x._weight.gt(0)&x.RIDAGEYR.ge(20)
        &x.DIQ010.eq(2)&~x.DIQ050.eq(1)&~x.DIQ070.eq(1)&~x.RIDEXPRG.eq(1)
        &(~band|x.RIDEXPRG.eq(2)))
    keep=x.eligible_before_labs&x[['LBXGH']+CBC].notna().all(axis=1)
    d=x.loc[keep].reset_index(drop=True)
    d['low_hgb']=(d.RIAGENDR.eq(2)&d.LBXHGB.lt(12))|(d.RIAGENDR.eq(1)&d.LBXHGB.lt(13))
    assert d._weight.gt(0).all() and d[['SDMVSTRA','SDMVPSU']].notna().all().all()
    return x,d

def folds_for(d,n=5,seed=42):
    splits=list(StratifiedGroupKFold(n_splits=n,shuffle=True,random_state=seed).split(d,d.target,d.group))
    for a,b in splits:
        assert not set(d.iloc[a].group)&set(d.iloc[b].group)
        assert d.iloc[a].target.nunique()==d.iloc[b].target.nunique()==2
    return splits

def build(nums,forest=False):
    pre=ColumnTransformer([
        ('numeric',Pipeline([('impute',SimpleImputer(strategy='median',add_indicator=True)),('scale',StandardScaler())]),nums),
        ('categorical',Pipeline([('impute',SimpleImputer(strategy='most_frequent')),
            ('encode',OneHotEncoder(handle_unknown='ignore',sparse_output=False))]),CAT)])
    clf=(RandomForestClassifier(n_estimators=300,min_samples_leaf=5,random_state=42,n_jobs=1)
         if forest else LogisticRegression(solver='liblinear',max_iter=2000))
    steps=[('pre',pre)]
    if not forest: steps.append(('sparse',FunctionTransformer(csr_matrix,accept_sparse=True)))
    return Pipeline(steps+[('clf',clf)])

def fit(d,indices,spec,multiplicity):
    # Expanding sampled PSU multiplicities refits even preprocessing under resampling.
    expanded=np.repeat(indices,multiplicity[indices])
    z=d.iloc[expanded]
    if z.target.nunique()!=2: raise ValueError('resampled training set has one class')
    model=build(*spec)
    weights=z._weight.to_numpy()
    model.fit(z[spec[0]+CAT],z.target,clf__sample_weight=weights/weights.mean())
    return model

def logits(s): return csr_matrix(logit(np.clip(s,1e-6,1-1e-6)).reshape(-1,1))

def threshold(y,p,w,goal=.95):
    keep=(y==1)&(w>0)
    order=np.argsort(-p[keep],kind='stable')
    levels=p[keep][order]
    fraction=np.cumsum(w[keep][order])/w[keep].sum()
    return float(levels[np.flatnonzero(fraction>=goal)[0]])

def development_fit(d,train,spec,multiplicity,inner):
    scores=np.full(len(train),np.nan)
    for a,b in inner:
        model=fit(d,train[a],spec,multiplicity)
        scores[b]=model.predict_proba(d.iloc[train[b]][spec[0]+CAT])[:,1]
    assert np.isfinite(scores).all()
    ww=d.iloc[train]._weight.to_numpy()*multiplicity[train]
    active=ww>0
    if d.iloc[train].target.to_numpy()[active].max()==0: raise ValueError('calibration has no positives')
    cal=LogisticRegression(solver='liblinear',C=1e6,max_iter=2000)
    cal.fit(logits(scores[active]),d.iloc[train].target.to_numpy()[active],sample_weight=ww[active]/ww[active].mean())
    calibrated=cal.predict_proba(logits(scores))[:,1]
    cut=threshold(d.iloc[train].target.to_numpy(),calibrated,ww)
    return fit(d,train,spec,multiplicity),cal,cut

def nested(d,specs=PRIMARY,outer=None,multiplicity=None,verbose=False):
    if outer is None: outer=folds_for(d)
    if multiplicity is None: multiplicity=np.ones(len(d),dtype=int)
    records=[]
    for fold,(train,test) in enumerate(outer,1):
        inner=folds_for(d.iloc[train],n=3,seed=420+fold)
        for name,spec in specs.items():
            model,cal,cut=development_fit(d,train,spec,multiplicity,inner)
            raw=model.predict_proba(d.iloc[test][spec[0]+CAT])[:,1]
            proba=cal.predict_proba(logits(raw))[:,1]
            g=d.iloc[test][['SEQN','target','_weight','SDMVSTRA','SDMVPSU','RIAGENDR','RIDAGEYR','RIDRETH3']].copy()
            g['model']=name; g['fold']=fold; g['raw']=raw; g['calibrated']=proba
            g['threshold']=cut; g['flagged']=proba>=cut
            g['_weight']=g._weight.to_numpy()*multiplicity[test]
            active=multiplicity[train]>0
            g['constant']=np.average(d.iloc[train].target.to_numpy()[active],
                weights=d.iloc[train]._weight.to_numpy()[active]*multiplicity[train][active])
            records.append(g)
        if verbose: print(f'  outer fold {fold} complete',flush=True)
    result=pd.concat(records,ignore_index=True)
    assert not result.duplicated(['SEQN','model']).any()
    assert result[['raw','calibrated','threshold']].notna().all().all()
    return result

def metrics(g,stage='calibrated'):
    g=g.loc[g._weight.gt(0)]
    y=g.target.to_numpy(); w=g._weight.to_numpy(); p=g[stage].to_numpy()
    if len(np.unique(y))!=2: raise ValueError('evaluation has one class')
    flag=g.flagged.to_numpy().astype(bool)
    avg=lambda a:np.average(a,weights=w)
    tp=w[(y==1)&flag].sum(); fn=w[(y==1)&~flag].sum()
    tn=w[(y==0)&~flag].sum(); fp=w[(y==0)&flag].sum()
    return dict(AUROC=roc_auc_score(y,p,sample_weight=w),AP=average_precision_score(y,p,sample_weight=w),
        Brier=avg((y-p)**2),log_loss=log_loss(y,p,sample_weight=w,labels=[0,1]),mean_risk=avg(p),
        prevalence=avg(y),sensitivity=tp/(tp+fn),specificity=tn/(tn+fp),
        NPV=tn/(tn+fn) if tn+fn else np.nan,deferred_fraction=avg(~flag))

def summarise(pred,label):
    rows=[]
    for model,g in pred.groupby('model'):
        for stage in ['raw','calibrated','constant']:
            # Policy metrics refer to the development-selected calibrated policy in every row.
            rows.append(dict(analysis=label,model=model,stage=stage,n=len(g),positives=int(g.target.sum()),
                deferred_n=int((~g.flagged).sum()),missed_n=int((g.target.eq(1)&~g.flagged).sum()),**metrics(g,stage)))
    return pd.DataFrame(rows)

def jackknife(pred,full):
    design=full.loc[full._weight.gt(0),['SDMVSTRA','SDMVPSU']].drop_duplicates()
    sizes=design.groupby('SDMVSTRA').size()
    assert sizes.ge(2).all()
    rows=[]
    for name,g in pred.groupby('model'):
        point=metrics(g)
        rep={k:[] for k in point}
        for h,hg in design.groupby('SDMVSTRA'):
            m=len(hg); values=[]
            for psu in hg.SDMVPSU:
                z=g.copy(); inside=z.SDMVSTRA.eq(h)
                z.loc[inside,'_weight']*=m/(m-1)
                z.loc[inside&z.SDMVPSU.eq(psu),'_weight']=0
                values.append(metrics(z))
            for key in point:
                estimates=np.array([v[key] for v in values])
                rep[key].append((m-1)/m*np.sum((estimates-estimates.mean())**2))
        dfree=len(design)-len(sizes)
        for key,value in point.items():
            se=np.sqrt(sum(rep[key])); critical=t.ppf(.975,dfree)
            rows.append(dict(model=name,metric=key,estimate=value,SE=se,lower=max(0,value-critical*se),
                upper=min(1,value+critical*se) if key!='log_loss' else value+critical*se,design_df=dfree))
    return pd.DataFrame(rows)

def bootstrap(d,full,count):
    outer=folds_for(d); rng=np.random.default_rng(20261102)
    design=full.loc[full._weight.gt(0),['SDMVSTRA','SDMVPSU']].drop_duplicates()
    assert design.groupby('SDMVSTRA').size().eq(2).all()
    rows=[]; failures=[]
    for rep in range(count):
        mult=np.zeros(len(d),dtype=int)
        for h,hg in design.groupby('SDMVSTRA'):
            chosen=rng.choice(hg.SDMVPSU.to_numpy())
            mult[d.SDMVSTRA.eq(h)&d.SDMVPSU.eq(chosen)]=2
        try:
            predictions=nested(d,outer=outer,multiplicity=mult)
            for name,g in predictions.groupby('model'):
                rows.append(dict(replicate=rep,model=name,**metrics(g)))
        except ValueError as e:
            failures.append(dict(replicate=rep,error=str(e)))
        if (rep+1)%5==0:
            pd.DataFrame(rows).to_csv(OUT/'full_refit_bootstrap_replicates.csv',index=False)
            print(f'Full refit PSU bootstrap: {rep+1}/{count}; failures={len(failures)}',flush=True)
    (OUT/'bootstrap_failures.json').write_text(json.dumps(failures,indent=2)+'\n')
    b=pd.DataFrame(rows); b.to_csv(OUT/'full_refit_bootstrap_replicates.csv',index=False)
    summaries=[]
    for name,g in b.groupby('model'):
        for metric in ['AUROC','AP','Brier','sensitivity','deferred_fraction']:
            summaries.append(dict(model=name,metric=metric,successful_replicates=len(g),
                lower=g[metric].quantile(.025),upper=g[metric].quantile(.975)))
    wide=b.pivot(index='replicate',columns='model',values='AUROC')
    delta=wide.demographics_bmi_cbc-wide.demographics_bmi
    summaries.append(dict(model='CBC_minus_BMI_AUROC',metric='AUROC_gain',successful_replicates=len(delta),
                          lower=delta.quantile(.025),upper=delta.quantile(.975)))
    pd.DataFrame(summaries).to_csv(OUT/'full_refit_bootstrap_intervals.csv',index=False)
    return len(failures)

def transport(d,external,full_external):
    train=np.arange(len(d)); inner=folds_for(d,n=5)
    multiplicity=np.ones(len(d),dtype=int)
    records=[]
    modeldir=OUT/'frozen_models'; modeldir.mkdir(exist_ok=True)
    frozen=[]
    for name,spec in PRIMARY.items():
        model,cal,cut=development_fit(d,train,spec,multiplicity,inner)
        payload=dict(model=model,calibrator=cal,threshold=cut,features=spec[0]+CAT,
                     development_cycle='2021–2023',evaluation_cycle='2017–2018')
        path=modeldir/f'{name}.joblib'; joblib.dump(payload,path)
        frozen.append(dict(model=name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),threshold=cut))
    # Freeze all fitted payloads and hashes before evaluating any external outcome.
    (OUT/'frozen_model_manifest.json').write_text(json.dumps(frozen,indent=2)+'\n')
    for name,spec in PRIMARY.items():
        saved=joblib.load(modeldir/f'{name}.joblib')
        raw=saved['model'].predict_proba(external[spec[0]+CAT])[:,1]
        p=saved['calibrator'].predict_proba(logits(raw))[:,1]
        g=external[['SEQN','target','_weight','SDMVSTRA','SDMVPSU']].copy()
        g['raw']=raw; g['calibrated']=p; g['model']=name; g['threshold']=saved['threshold']
        g['flagged']=p>=saved['threshold']; g['constant']=np.average(d.target,weights=d._weight)
        records.append(g)
    pred=pd.concat(records,ignore_index=True)
    pred.to_csv(OUT/'independent_cycle_predictions.csv',index=False)
    jackknife(pred,full_external).to_csv(OUT/'independent_cycle_conditional_intervals.csv',index=False)
    return summarise(pred,'transport_2017_2018')

def utility(pred):
    curves=[]; matched=[]
    for name,g in pred.groupby('model'):
        y=g.target.to_numpy(); w=g._weight.to_numpy(); p=g.calibrated.to_numpy()
        prevalence=np.average(y,weights=w)
        for cut in np.linspace(.005,.10,40):
            flag=p>=cut; tp=w[(y==1)&flag].sum()/w.sum(); fp=w[(y==0)&flag].sum()/w.sum()
            curves.append(dict(model=name,threshold=cut,net_benefit=tp-fp*cut/(1-cut),
                test_all=prevalence-(1-prevalence)*cut/(1-cut),test_none=0))
        # Descriptive matched burden on held-out scores; not selected deployable thresholds.
        order=np.argsort(-p,kind='stable')
        for fraction in [.50,.75,.90]:
            end=np.searchsorted(np.cumsum(w[order])/w.sum(),fraction,side='left')+1
            cut=p[order[min(end-1,len(order)-1)]]
            flag=p>=cut
            matched.append(dict(model=name,target_flag_fraction=fraction,
                actual_weighted_flag_fraction=np.average(flag,weights=w),
                weighted_sensitivity=w[(y==1)&flag].sum()/w[y==1].sum(),
                missed_n=int(((y==1)&~flag).sum()),deferred_n=int((~flag).sum())))
    curves=pd.DataFrame(curves);curves.to_csv(OUT/'decision_curves.csv',index=False)
    pd.DataFrame(matched).to_csv(OUT/'descriptive_matched_testing_burden.csv',index=False)
    fig,ax=plt.subplots(figsize=(8,5))
    for name,g in curves.groupby('model'): ax.plot(g.threshold,g.net_benefit,label=name)
    g=next(iter(curves.groupby('model')))[1]
    ax.plot(g.threshold,g.test_all,'k--',label='Test all');ax.axhline(0,color='gray',label='Test none')
    ax.set(xlabel='Risk threshold (assumed harm exchange rate)',ylabel='Weighted net benefit',
           title='Exploratory decision curves — no measured costs or safety claim',ylim=(-.025,.03))
    ax.legend(fontsize=8);fig.tight_layout();fig.savefig(OUT/'decision_curves.png',dpi=160);plt.close(fig)

def main(count=100):
    OUT.mkdir(parents=True,exist_ok=True);started=time.time()
    full,d=load_cycle('L');full_j,external=load_cycle('J')
    assert len(d)==4612 and d.target.sum()==106
    assert not set(d.SEQN)&set(external.SEQN)
    counts=[]
    for cycle,f,z in [('2021_2023',full,d),('2017_2018',full_j,external)]:
        counts.append(dict(cycle=cycle,n=len(z),positives=int(z.target.sum()),
            bmi_missing=int(z.BMXBMI.isna().sum()),weighted_prevalence=np.average(z.target,weights=z._weight),
            eligible_before_labs=int(f.eligible_before_labs.sum()),low_hgb=int(z.low_hgb.sum())))
    pd.DataFrame(counts).to_csv(OUT/'cycle_counts.csv',index=False)
    # Selection audit within eligibility, separating observed outcomes from missing labels.
    selection=full.loc[full.eligible_before_labs].copy()
    selection['complete_labs']=selection.SEQN.isin(d.SEQN)
    selection['positive_observed']=selection.LBXGH.ge(6.5).where(selection.LBXGH.notna())
    selection.groupby('complete_labs').agg(n=('SEQN','size'),age_mean=('RIDAGEYR','mean'),
        female_fraction=('RIAGENDR',lambda x:x.eq(2).mean()),hba1c_observed=('LBXGH','count'),
        observed_positive=('positive_observed','sum'),BMI_observed=('BMXBMI','count')).to_csv(OUT/'selection_audit.csv')
    missing=d[NUM+CAT+['BMXBMI']+CBC].isna().mean().rename('missing_fraction')
    missing.to_csv(OUT/'primary_predictor_missingness.csv')
    results=[]
    print('Primary BMI/block/forest comparison',flush=True)
    pred=nested(d,{**PRIMARY,**BLOCKS,**FORESTS},verbose=True)
    pred.to_csv(OUT/'primary_extension_predictions.csv',index=False)
    results.append(summarise(pred,'primary'))
    jackknife(pred,full).to_csv(OUT/'primary_conditional_intervals.csv',index=False)
    utility(pred[pred.model.isin(PRIMARY)])
    subgroups=[]
    for variable,bins in [('sex',d.RIAGENDR.map({1:'male',2:'female'})),
                          ('age',pd.Series(np.where(d.RIDAGEYR.lt(65),'20–64','65+'))),
                          ('race_ethnicity',d.RIDRETH3.astype(int).astype(str))]:
        membership=dict(zip(d.SEQN,bins))
        for name,g in pred[pred.model.isin(PRIMARY)].groupby('model'):
            for label,z in g.groupby(g.SEQN.map(membership)):
                row=dict(variable=variable,subgroup=label,model=name,n=len(z),positives=int(z.target.sum()))
                if z.target.sum()>=10 and z.target.nunique()==2: row.update(metrics(z))
                else: row['note']='Performance suppressed: fewer than 10 positive labels; no fairness claim'
                subgroups.append(row)
    pd.DataFrame(subgroups).to_csv(OUT/'subgroup_descriptive_metrics.csv',index=False)
    scenarios={'bmi_observed':d.BMXBMI.notna(),'exclude_low_hgb_all_ages':~d.low_hgb,
               'age20_65_all':d.RIDAGEYR.le(65),
               'age20_65_exclude_low_hgb':d.RIDAGEYR.le(65)&~d.low_hgb}
    for name,mask in scenarios.items():
        z=d.loc[mask].reset_index(drop=True)
        print(f'Sensitivity {name}: n={len(z)}, positives={z.target.sum()}',flush=True)
        pp=nested(z);results.append(summarise(pp,name))
        pp.to_csv(OUT/f'{name}_predictions.csv',index=False)
    fasting=d.loc[d.WTSAF2YR.gt(0)&d.LBXGLU.notna()].reset_index(drop=True)
    fasting['_weight']=fasting.WTSAF2YR
    agreement=pd.crosstab(fasting.target,fasting.LBXGLU.ge(126).astype(int),dropna=False)
    agreement.to_csv(OUT/'fasting_hba1c_agreement_counts.csv')
    aa=[]
    for h in [0,1]:
        for g in [0,1]: aa.append(dict(hba1c=h,glucose=g,n=int((fasting.target.eq(h)&fasting.LBXGLU.ge(126).eq(bool(g))).sum()),
            weighted_fraction=fasting.loc[fasting.target.eq(h)&fasting.LBXGLU.ge(126).eq(bool(g)),'_weight'].sum()/fasting._weight.sum()))
    pd.DataFrame(aa).to_csv(OUT/'fasting_hba1c_agreement_weighted.csv',index=False)
    shared_folds=folds_for(fasting)
    for endpoint in ['hba1c','glucose']:
        z=fasting.copy()
        if endpoint=='glucose':z['target']=z.LBXGLU.ge(126).astype(int)
        print(f'Fasting endpoint {endpoint}: n={len(z)}, positives={z.target.sum()}',flush=True)
        pp=nested(z,outer=shared_folds);pp.to_csv(OUT/f'fasting_{endpoint}_predictions.csv',index=False)
        results.append(summarise(pp,f'fasting_{endpoint}'))
    print('Frozen independent-cycle transport',flush=True)
    results.append(transport(d,external,full_j))
    all_results=pd.concat(results,ignore_index=True);all_results.to_csv(OUT/'extension_model_comparison.csv',index=False)
    print(all_results[all_results.stage.eq('calibrated')][['analysis','model','n','positives','AUROC','Brier']].to_string(index=False),flush=True)
    failures=bootstrap(d,full,count) if count else None
    metadata=dict(protocol_sha256=hashlib.sha256((ROOT/'reports/extension_analysis_protocol.md').read_bytes()).hexdigest(),
        bootstrap_requested=count,bootstrap_failures=failures,elapsed_seconds=time.time()-started,
        cycle_counts=counts,primary_specs={k:v[0] for k,v in PRIMARY.items()},drop_basophil_percentage=True,
        limits=['Internal/independent-cycle cross-sectional evidence, not clinical safety',
                'Bootstrap fixes original split assignment; finite replicate tail precision',
                'Operational low-hemoglobin flag is not etiologic anemia diagnosis',
                '2017–2018 uses MEC weights; 2021–2023 uses phlebotomy weights'])
    (OUT/'extension_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print('Extension finished',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--bootstrap',type=int,default=100)
    main(parser.parse_args().bootstrap)
