"""Plot the fixed primary cohort using saved, verified analysis membership."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'code/assets/cohort'
pred = pd.read_csv(ROOT / 'code/assets/weighted/weighted_oof_predictions.csv')
members = pred.loc[pred.model.eq('cbc_demographics_logistic'), ['SEQN', 'target']]
assert members.SEQN.is_unique and len(members) == 4612
demo = pd.read_sas(ROOT/'data/raw/DEMO_L.xpt', format='xport')
d = members.merge(demo[['SEQN','RIDAGEYR','RIAGENDR']], on='SEQN', validate='one_to_one')
assert len(d) == 4612 and d.target.sum() == 106
assert d.RIDAGEYR.ge(20).all() and d[['RIDAGEYR','RIAGENDR']].notna().all().all()
assert d.RIAGENDR.isin([1,2]).all()
fig, axes = plt.subplots(1,3,figsize=(14,4.8))
axes[0].hist(d.RIDAGEYR, bins=np.arange(20,86,5), color='#4c78a8', edgecolor='white')
axes[0].set(title='Age (years)', xlabel='Age (80 = 80 or older)', ylabel='Participants', xlim=(19,85))
axes[0].set_xticks([20,30,40,50,60,70,80])
sex = d.RIAGENDR.value_counts().reindex([2,1],fill_value=0)
outcome = d.target.value_counts().reindex([0,1],fill_value=0)
for ax, labels, counts, title, colors in [
    (axes[1], ['Female','Male'], sex.to_numpy(), 'Recorded sex', ['#72b7b2']*2),
    (axes[2], ['Below 6.5%','At least 6.5%'], outcome.to_numpy(), 'Observed HbA1c', ['#4c78a8','#e45756']),
]:
    bars=ax.bar(labels,counts,color=colors,width=.65)
    ax.set(title=title,ylabel='Participants',ylim=(0,max(counts)*1.2))
    for bar,count in zip(bars,counts):
        ax.text(bar.get_x()+bar.get_width()/2, count+max(counts)*.025,
                f'{count:,}\n({100*count/len(d):.1f}%)',ha='center',va='bottom',fontsize=10)
fig.suptitle('Final analytic cohort: adults aged 20+ with no reported diabetes diagnosis (N = 4,612)',fontsize=13)
fig.text(.5,.025,'Unweighted sample counts. Additional medication, pregnancy and laboratory eligibility filters apply.\n'
         'HbA1c ≥6.5% is a laboratory outcome, not a confirmed diagnosis; pregnancy status is not public for all ages.',
         ha='center',fontsize=9)
fig.tight_layout(rect=(0,.13,1,.92))
OUT.mkdir(parents=True,exist_ok=True)
fig.savefig(OUT/'final_cohort_description.png',dpi=180)
plt.close(fig)
pd.DataFrame({'panel':['sex']*2+['hba1c']*2,
              'category':['Female','Male','Below 6.5%','At least 6.5%'],
              'n':list(sex)+list(outcome)}).assign(percent=lambda x:100*x.n/len(d)).to_csv(
                  OUT/'final_cohort_description_counts.csv',index=False)
print(OUT/'final_cohort_description.png')
