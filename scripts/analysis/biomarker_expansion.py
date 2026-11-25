"""Phase 9: test the incremental value of liver, kidney, inflammation, lipid and
insulin-resistance biomarkers beyond demographics + BMI + the locked 9-feature CBC
block. Exploratory -- this does not change the Phase 15 locked feature set in
study_config.py, and no hyperparameter/threshold selection is done from results.

All but the fasting group (insulin, triglycerides, LDL) use WTPH2YR -- the same
weight as the primary cohort -- so they're tested on the full 4,612/106 primary
cohort (no subsample loss beyond item-level missingness). The fasting group uses
WTSAF2YR, the same restriction already applied to fasting glucose elsewhere in
this pipeline, so it's tested on a smaller, separately-matched subsample.

Run: python scripts/analysis/biomarker_expansion.py
"""
from pathlib import Path
import sys
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/analysis'))
import study_config as cfg
import research_extension as ext

OUT = ROOT / 'results/biomarker_expansion'
OUT.mkdir(parents=True, exist_ok=True)
LAB = ROOT / 'data/raw/2021_2023/laboratory'

NUM = cfg.NUMERIC_DEMOGRAPHICS
CAT = cfg.CATEGORICAL_DEMOGRAPHICS
CBC = cfg.CBC_FEATURES  # current locked 9-feature block (Phase 15 Step 3)
BASELINE = NUM + ['BMXBMI'] + CBC

# WTPH2YR groups (full primary cohort, no subsample restriction beyond item missingness)
WTPH_GROUPS = {
    'liver': ['LBXSATSI', 'LBXSASSI', 'LBXSGTSI', 'LBXSAPSI'],         # ALT, AST, GGT, ALP
    'kidney': ['LBXSCR', 'LBXSBU', 'LBXSUA'],                          # creatinine, BUN, uric acid
    'inflammation': ['LBXHSCRP'],                                      # hs-CRP
    'lipids_nonfasting': ['LBXTC', 'LBDHDD'],                          # total cholesterol, HDL
}
# WTSAF2YR groups (fasting subsample only, same restriction as existing fasting-glucose work)
FASTING_GROUPS = {
    'lipids_fasting': ['LBXTLG', 'LBDLDL'],                            # triglycerides, Friedewald LDL
    'insulin': ['LBXIN'],
    'homa_ir': ['HOMA_IR'],                                            # derived: glucose x insulin / 405
}


def main():
    full, d = ext.load_cycle('L')
    assert len(d) == 4612 and d.target.sum() == 106

    bio = ext.read(LAB / 'BIOPRO_L.xpt')
    crp = ext.read(LAB / 'HSCRP_L.xpt')
    tchol = ext.read(LAB / 'TCHOL_L.xpt')
    hdl = ext.read(LAB / 'HDL_L.xpt')
    trigly = ext.read(LAB / 'TRIGLY_L.xpt')
    ins = ext.read(LAB / 'INS_L.xpt')

    d = d.merge(bio[['SEQN'] + WTPH_GROUPS['liver'] + WTPH_GROUPS['kidney']], on='SEQN', how='left', validate='one_to_one')
    d = d.merge(crp[['SEQN'] + WTPH_GROUPS['inflammation']], on='SEQN', how='left', validate='one_to_one')
    d = d.merge(tchol[['SEQN', 'LBXTC']], on='SEQN', how='left', validate='one_to_one')
    d = d.merge(hdl[['SEQN', 'LBDHDD']], on='SEQN', how='left', validate='one_to_one')
    d = d.merge(trigly[['SEQN', 'LBXTLG', 'LBDLDL']], on='SEQN', how='left', validate='one_to_one')
    d = d.merge(ins[['SEQN', 'LBXIN']], on='SEQN', how='left', validate='one_to_one')  # WTSAF2YR already in d via ext.load_cycle
    d['HOMA_IR'] = d.LBXGLU * d.LBXIN / 405  # standard formula; LBXGLU (fasting glucose) already in d via GLU_L

    coverage = {}
    for name, cols in {**WTPH_GROUPS, **FASTING_GROUPS}.items():
        coverage[name] = int(d[cols].notna().all(axis=1).sum())
    pd.Series(coverage, name='n_with_complete_group').to_csv(OUT / 'biomarker_coverage.csv')
    print('Coverage (of 4,612 primary-cohort participants):', flush=True)
    print(pd.Series(coverage).to_string(), flush=True)

    rows, aurocs = [], {}
    for name, cols in {**WTPH_GROUPS, **FASTING_GROUPS}.items():
        mask = d[cols].notna().all(axis=1)
        if name in FASTING_GROUPS:
            mask = mask & d.WTSAF2YR.gt(0)
        z = d.loc[mask].reset_index(drop=True)
        if z.target.sum() < 10:
            print(f'[{name}] skipped: fewer than 10 positive labels (n={len(z)}, positives={int(z.target.sum())})', flush=True)
            continue
        if name in FASTING_GROUPS:
            z['_weight'] = z.WTSAF2YR  # fasting weight, matching existing fasting-endpoint convention
        specs = {'baseline': (BASELINE, 'logistic'), f'baseline_plus_{name}': (BASELINE + cols, 'logistic')}
        pred = ext.nested(z, specs=specs, verbose=False)
        summary = ext.summarise(pred, name)
        summary.to_csv(OUT / f'{name}_predictions_summary.csv', index=False)
        pred.to_csv(OUT / f'{name}_predictions.csv', index=False)
        cal = summary.loc[summary.stage.eq('calibrated')].set_index('model')
        gain = cal.loc[f'baseline_plus_{name}', 'AUROC'] - cal.loc['baseline', 'AUROC']
        rows.append(dict(group=name, variables=','.join(cols), n=len(z), positives=int(z.target.sum()),
                         baseline_AUROC=cal.loc['baseline', 'AUROC'],
                         baseline_plus_group_AUROC=cal.loc[f'baseline_plus_{name}', 'AUROC'],
                         AUROC_gain=gain))
        aurocs[name] = (cal.loc['baseline', 'AUROC'], cal.loc[f'baseline_plus_{name}', 'AUROC'])
        print(f'[{name}] n={len(z)} positives={int(z.target.sum())}: baseline {cal.loc["baseline","AUROC"]:.4f} '
              f'-> +group {cal.loc[f"baseline_plus_{name}","AUROC"]:.4f} (gain {gain:+.4f})', flush=True)

    results = pd.DataFrame(rows).sort_values('AUROC_gain', ascending=False)
    results.to_csv(OUT / 'biomarker_ablation_summary.csv', index=False)
    print(results.round(4).to_string(index=False), flush=True)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(results.group, results.AUROC_gain, color=['#59a14f' if v >= 0 else '#e15759' for v in results.AUROC_gain])
    ax.axvline(0, color='black', lw=.8)
    ax.set(xlabel='Weighted AUROC gain over demographics+BMI+CBC baseline',
           title='Phase 9: biomarker groups, matched per-group subsample (not directly comparable to each other -- different n)')
    fig.tight_layout(); fig.savefig(OUT / 'biomarker_ablation_gains.png', dpi=160); plt.close(fig)

    metadata = dict(baseline_features=BASELINE, coverage=coverage,
                    note='Exploratory Phase 9 screen. Each group uses its own matched subsample '
                         '(different n per row) because missingness/fasting-eligibility differs by '
                         'group -- gains are not directly comparable across groups, only each group '
                         'to its own baseline. Does not change study_config.py.')
    (OUT / 'biomarker_expansion_metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(f'\nOutputs: {OUT}', flush=True)


if __name__ == '__main__':
    main()
