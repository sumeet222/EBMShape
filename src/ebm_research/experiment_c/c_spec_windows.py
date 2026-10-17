"""Separate supplementary C-spec window review after the completed P0 screen.

Reuses the same daily arrays, state labels and previously verified block intervals.
No acquisition, model fitting, threshold changes or duplicate minute data.
"""
import datetime as dt
import math
import time

import numpy as np
import pandas as pd

from .preliminary import ROOT, OUT as P0, CONFIG, read_json, write_json, sha, COLORS, NAMES
from .reporting import table

OUT=ROOT/'artifacts/C/C_spec_window_preliminary_v1'
WINDOWS={'OPEN':(0,6),'C_SPEC_MID':(24,48),'C_SPEC_CLOSE':(66,78)}
LABELS=['OPEN\n09:30–10:00','C-spec MID\n11:30–13:30','C-spec CLOSE\n15:00–16:00']


def verify_preservation():
    """Verify every original P0 output/code/source hash, plus the old B snapshot."""
    manifest=read_json(P0/'outputs_manifest.json')
    for ref in manifest['files']:
        if sha(ROOT/ref['path'])!=ref['sha256']:raise ValueError('Prior P0 file changed: '+ref['path'])
    snapshot=read_json(P0/'start_snapshot.json')
    from .preliminary import data_root
    for ref in snapshot['files']:
        path=(ROOT if ref['base']=='repo' else data_root())/ref['path']
        if sha(path)!=ref['sha256']:raise ValueError('Prior B/shared file changed: '+ref['path'])
    return len(manifest['files']),len(snapshot['files'])


def reconcile(z,w):
    """Independently recover all C-spec means, SDs, counts and robust contrasts."""
    checks=0
    for branch,key in [('OPEN','open_labels'),('PREV','prev_labels')]:
        labels=z[key];valid=np.flatnonzero(labels>=0);dates=z['dates']
        ranked=sorted(valid,key=lambda i:(-z['RV_day'][i],dates[i]));removed=set(ranked[:math.ceil(.01*len(valid))])
        for mode,key,offset in [('whole','q',0),('remaining','remaining',6)]:
            # Prefix differences provide a separate summation path to P0 slice sums.
            cumulative=np.c_[np.zeros(len(dates)),np.cumsum(z[key],axis=1)]
            for window,(a,b) in WINDOWS.items():
                if mode=='remaining' and window=='OPEN':continue
                values=cumulative[:,b-offset]-cumulative[:,a-offset]
                for variant in ['FULL','DROP_TOP1','MEDIAN']:
                    reducer=np.median if variant=='MEDIAN' else np.mean;group=[]
                    for g,state in enumerate(NAMES):
                        ix=[i for i in valid if labels[i]==g and (variant!='DROP_TOP1' or i not in removed)]
                        value=float(reducer(values[ix]));sd=float(np.std(values[ix],ddof=1));group.append((value,sd,len(ix)))
                        row=w[(w.branch==branch)&(w['mode']==mode)&(w.window==window)&(w.variant==variant)&(w.state==state)].iloc[0]
                        np.testing.assert_allclose([row.summary,row.sd],[value,sd],atol=1e-10,rtol=0)
                        assert row.n==len(ix);checks+=1
                    row=w[(w.branch==branch)&(w['mode']==mode)&(w.window==window)&(w.variant==variant)&(w.state=='high-minus-low')].iloc[0]
                    np.testing.assert_allclose(row.summary,group[2][0]-group[0][0],atol=1e-10,rtol=0)
                    np.testing.assert_allclose(row.sd,np.sqrt((group[2][1]**2+group[0][1]**2)/2),atol=1e-10,rtol=0)
                    assert row.n==group[2][2]+group[0][2];checks+=1
    return checks


def plots(z,w):
    """Seven supplementary figures; fixed P0 cohorts and comparable branch axes."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from PIL import Image,ImageOps,ImageDraw
    plt.rcParams.update({'font.size':12,'axes.titlesize':13,'legend.fontsize':10})
    folder=OUT/'figures';folder.mkdir(parents=True,exist_ok=True);files=[]
    primary=w[(w.variant=='FULL')&(w['mode']=='whole')&(w.state!='high-minus-low')]
    ymax=float(primary.hi_5.max()*1.15)
    contrasts=w[(w.variant=='FULL')&(w.state=='high-minus-low')]
    lim=float(np.abs(contrasts[['lo_5','hi_5','lo_10','hi_10']].to_numpy()).max()*100*1.15)
    def finish(fig,name,title):
        fig.suptitle('C-SPEC SUPPLEMENTARY · '+title,fontsize=15)
        fig.text(.5,.012,'SPY 2016–2021 · same P0 source/cohorts · exploratory pointwise intervals · P0 primary verdict unchanged',ha='center',fontsize=10)
        fig.tight_layout(rect=[0,.04,1,.94]);file=folder/name;fig.savefig(file,dpi=160);plt.close(fig);files.append(file)
    for i,branch in enumerate(['OPEN','PREV']):
        fig,ax=plt.subplots(figsize=(12,6));x=np.arange(3)
        for g,color in zip(NAMES,COLORS):
            d=primary[(primary.branch==branch)&(primary.state==g)].set_index('window').loc[list(WINDOWS)]
            ax.errorbar(x+(NAMES.index(g)-1)*.22,d.summary,yerr=[d.summary-d.lo_5,d.hi_5-d.summary],fmt='o',capsize=5,color=color,label=f'{g} (n={int(d.n.iloc[0])})')
        ax.set_xticks(x,LABELS);ax.set_ylim(0,ymax);ax.set_ylabel('Mean fraction of whole-day realized variance');ax.grid(alpha=.2);ax.legend()
        note='retrospective state; opening numerator overlap' if branch=='OPEN' else 'state from immediate prior scheduled session'
        finish(fig,f'0{i+1}_{branch.lower()}_C_spec_group_shares.png',f'{branch} terciles · {note}\nGroup means and 95% pointwise intervals · block 5')
        fig,axs=plt.subplots(1,2,figsize=(13,6),sharey=True)
        for ax,mode in zip(axs,['whole','remaining']):
            windows=list(WINDOWS) if mode=='whole' else list(WINDOWS)[1:]
            d=contrasts[(contrasts.branch==branch)&(contrasts['mode']==mode)].set_index('window').loc[windows]
            for length,color,offset in [(5,COLORS[0],-.07),(10,COLORS[2],.07)]:
                value=d.summary.to_numpy()*100;lo=d[f'lo_{length}'].to_numpy()*100;hi=d[f'hi_{length}'].to_numpy()*100
                ax.errorbar(np.arange(len(d))+offset,value,yerr=[value-lo,hi-value],fmt='o',capsize=5,color=color,label=f'block {length}')
            ax.axhline(0,color='black',lw=.8);ax.set_ylim(-lim,lim);ax.set_xticks(np.arange(len(d)),[LABELS[list(WINDOWS).index(k)] for k in windows]);ax.set_title('Whole-day denominator' if mode=='whole' else 'Post-10:00 denominator');ax.grid(alpha=.2);ax.legend()
        axs[0].set_ylabel('High − low allocation difference (percentage points)')
        finish(fig,f'0{i+3}_{branch.lower()}_C_spec_HL_blocks.png',f'{branch} · wider-window contrasts · fixed original states')
    fig,axs=plt.subplots(2,3,figsize=(14,9),sharey=True)
    for row,(branch,key) in enumerate([('OPEN','open_labels'),('PREV','prev_labels')]):
        label=z[key]
        for col,(name,(a,b)) in enumerate(WINDOWS.items()):
            ax=axs[row,col];values=z['q'][:,a:b].sum(axis=1)
            boxes=ax.boxplot([values[label==g] for g in range(3)],tick_labels=NAMES,showfliers=True,patch_artist=True,flierprops=dict(marker='.',markersize=3,alpha=.4))
            for box,color in zip(boxes['boxes'],COLORS):box.set_facecolor(color);box.set_alpha(.4)
            ax.set_title(branch+' · '+LABELS[col].replace('\n',' '));ax.set_ylim(0,1);ax.grid(alpha=.2)
            if col==0:ax.set_ylabel('Daily whole-day RV fraction\nAll outliers retained')
    finish(fig,'05_C_spec_daily_distributions.png','Daily wider-window distributions · n OPEN1491 / PREV 1472')
    fig,axs=plt.subplots(2,2,figsize=(13,9),sharey=True)
    for row,branch in enumerate(['OPEN','PREV']):
        for col,mode in enumerate(['whole','remaining']):
            ax=axs[row,col]
            for variant,marker in [('FULL','o'),('DROP_TOP1','s'),('MEDIAN','^')]:
                d=w[(w.branch==branch)&(w['mode']==mode)&(w.variant==variant)&(w.state=='high-minus-low')].set_index('window').loc[['C_SPEC_MID','C_SPEC_CLOSE']]
                ax.plot([0,1],100*d.summary,marker=marker,label=f'{variant} H+L n={int(d.n.iloc[0])}')
            ax.set_xticks([0,1],['MID 11:30–13:30','CLOSE 15:00–16:00']);ax.axhline(0,color='black',lw=.8);ax.grid(alpha=.2);ax.legend();ax.set_title(branch+' · '+mode+' denominator')
            if col==0:ax.set_ylabel('H−L allocation difference (pp)')
    finish(fig,'06_C_spec_outlier_median_fragility.png','Wider-window robustness · FULL primary within supplementary review')
    fig,axs=plt.subplots(1,2,figsize=(13,6),sharey=True)
    for ax,branch,key in zip(axs,['OPEN','PREV'],['open_labels','prev_labels']):
        for g,color in enumerate(COLORS):ax.plot(np.arange(78),z['q'][z[key]==g].mean(axis=0),color=color,label=f'{NAMES[g]} n={int((z[key]==g).sum())}')
        ax.axvspan(24,47.95,color='gray',alpha=.13,label='C-spec MID');ax.axvspan(66,77,color='gold',alpha=.15,label='C-spec CLOSE')
        ax.set_xticks([0,6,24,48,66,77],['09:30','10:00','11:30','13:30','15:00','15:55']);ax.set_xlim(0,77);ax.set_xlabel('ET five-minute bin start');ax.set_title(branch);ax.grid(alpha=.2);ax.legend()
    axs[0].set_ylabel('Mean daily RV fraction per five-minute bin')
    finish(fig,'07_C_spec_windows_on_full_profiles.png','Window locations on unchanged P0 mean profiles\nOPEN state remains retrospective; shaded wider windows are supplementary')
    records=[]
    for file in sorted(files):
        with Image.open(file) as im:
            im.load();assert im.width>=1600 and np.asarray(im).std()>5
            records.append(dict(path=file.relative_to(ROOT).as_posix(),width=im.width,height=im.height,sha256=sha(file)))
    sheet=Image.new('RGB',(2100,1500),'white')
    for i,file in enumerate(sorted(files)):
        with Image.open(file) as im:thumb=ImageOps.contain(im.convert('RGB'),(680,455))
        tile=Image.new('RGB',(700,500),'white');tile.paste(thumb,((700-thumb.width)//2,30));ImageDraw.Draw(tile).text((5,5),file.name,fill='black');sheet.paste(tile,((i%3)*700,(i//3)*500))
    sheet.save(folder/'contact_sheet.png')
    return records


def report(w,qa):
    """Separate window-specific feasibility judgments, not a revised P0 verdict."""
    stats=w[(w.state=='high-minus-low')&(w.variant=='FULL')].copy();stats['daily_SD_units']=stats.summary/stats.sd
    columns=['branch','mode','window','summary','lo_5','hi_5','lo_10','hi_10','daily_SD_units']
    frag=w[w.state=='high-minus-low'][['branch','mode','window','variant','summary','sd','n']]
    matched=pd.read_csv(P0/'matched_date_comparison.csv');matched=matched[matched.window.isin(WINDOWS)]
    decision=[dict(branch='OPEN',window='C_SPEC_MID',verdict='WEAK'),dict(branch='OPEN',window='C_SPEC_CLOSE',verdict='WEAK'),dict(branch='PREV',window='C_SPEC_MID',verdict='WEAK'),dict(branch='PREV',window='C_SPEC_CLOSE',verdict='GO/PROMISING (descriptive feasibility only)')]
    narrative='C-spec supplementary review: promising narrowly for PREV-state closing-hour allocation; OPEN-state wider windows and both midday comparisons remain weak/inconclusive. P0 primary remains WEAK/INCONCLUSIVE.'
    prefix='../../artifacts/C/C_spec_window_preliminary_v1/'
    images='\n\n'.join(f'![C-spec supplementary: {r["path"].split("/")[-1]}]({prefix}figures/{r["path"].split("/")[-1]})' for r in qa['figures'])
    text=f'''# Experiment C — C-spec windows: separate supplementary feasibility review

**Implementation/QA PASS. {narrative}**

This is the explicitly requested follow-on to the completed [P0 review](C_preliminary_RV_profile_visual_gallery.md). It does not replace that review's primary 12:00–13:00 midday / 15:30–16:00 closing windows, source, sample, states or verdict. The C-spec windows were specified before P0; supplementary numerical results were already visible there. This review adds the separately labeled visualization/feasibility assessment requested afterward; it is not a fresh blind test or new confirmatory evidence.

## Definitions and shared source

- C-spec OPEN 09:30–10:00, bins 0:6 (shared with P0).
- C-spec MID 11:30–13:30, bins 24:48 (24 five-minute bins).
- C-spec CLOSE 15:00–16:00, bins 66:78 (12 bins).
- Each mean is the mean of daily window shares, not the ratio of group variance totals. Window durations differ; displayed values are fractions of whole-day RV, not per-minute rates. They do not exhaust the day and are dependent.
- Same Alpaca SIP split-adjusted SPY bars, exact 390-minute full sessions, first log(close09:30/open09:30), then 389 close ratios, no overnight/fill. Main 2016-01-05–2021-12-31; OPEN 1491 days (497/497/497), PREV 1472 (491/491/490); matched 1472. Same independent fixed terciles, source hashes and strict preceding scheduled-session rule. No new source request, raw copy, model, state search, VIX or 2022–2026 scientific values.
- `whole` uses the full-day denominator. `remaining` retains original states and renormalizes only 10:00–16:00 RV, removing direct opening numerator overlap without removing all dependence. OPEN is retrospective/descriptive.

## Separate feasibility judgments

{table(pd.DataFrame(decision))}

PREV closing-hour H−L whole-day allocation is **+2.005pp**, with block 5 interval **+0.927 to +3.080pp** and block 10 **+0.839 to +3.206pp**. Remaining-day H−L is **+1.737pp**, with block 10 **+0.459 to +3.068pp**. Whole-day drop-top1 and median contrasts are **+1.839pp** and **+2.416pp**; remaining-day counterparts **+1.553pp** and **+2.197pp**. The original full-sample primary mean is retained. Standardized whole/remaining effects are about **0.257/0.200 pooled daily SD**, a modest but interpretable descriptive shift.

The C-spec 2pp closing-hour materiality reference lies inside the observed confidence interval: the estimate is near that reference, but the interval does **not** establish a shift larger than 2pp. Nor do other intervals containing zero prove invariance. Broader C RQ1/RQ2, source-paper replication, continuous-state models, temporal stability and forecasting are untested. The favorable PREV result supports considering a later reviewed stage, not automatic approval or full-C scientific success.

OPEN C-spec closing-hour H−L is **−0.415pp** (block 10 **−1.731 to +0.963pp**) and remaining **−0.099pp**; both uncertain. OPEN/PREV wider-midday contrasts are **−0.075/+0.349pp**, with both block intervals crossing zero. Thus this is a window- and branch-specific preliminary signal, not a uniform state effect.

## Numerical effects and both block lengths

Values in the table are fractions; multiply by100 for percentage points. All 95% intervals are exploratory **pointwise**, conditional on fixed original state labels and 1,000 joint date-block resamples per branch/length. P0 already independently replayed these intervals; this review verifies those saved input hashes and independently reconstructs all 120 C-spec summary/SD/count/contrast rows from the shared daily arrays to 1e-10. No new independent tests or simultaneous inference are claimed.

{table(stats[columns])}

## C-spec visual gallery

Every chart is explicitly labeled C-SPEC SUPPLEMENTARY. Comparable branch panels share scales; window distributions retain all outliers. FULL, drop-top1 and median summaries are shown separately. The full normalized curves and underlying state groups are unchanged from P0; the last figure only locates the wider windows on those curves.

{images}

## Robustness and matched dates

{table(frag)}

Top1% removes 15 largest RV_day dates per branch without refitting state labels. Those dates account for 22.49% of OPEN-cohort raw RV and 18.11% of PREV-cohort raw RV. Median contrasts are differences of medians of daily window shares, not sums of per-bin medians. This robustness does not recover excluded incomplete sessions.

{table(matched)}

The matched cohort uses the same 1472 outcome dates with original branch labels. Its OPEN closing-hour whole/remaining contrasts are −0.333/+0.003pp, still a weak wider-hour result; PREV contrasts equal the full PREV cohort. OPEN/PREV state-group membership differs even on common dates; no causal paired interpretation follows.

## QA, selection and limitations

{qa['prior_P0_files']}prior P0 files and{qa['prior_B_shared_files']}earlier B/shared snapshot files remain hash-unchanged. Numerical reconciliation 120 rows passed to 1e-10; interval provenance is the preserved P0 QA and matching window table, not a newly estimated uncertainty distribution. All 7 main PNGs decode, are nonblank and≥1600px wide; the contact sheet permits manual review. No download bytes were added; original cumulative response-body total remains 119,675,359/1,000,000,000.

The source's complete-session selection omits 12 early closes and 7 ordinary days with 100 missing minutes, including four 2020 March crisis dates. Those omissions are not random; causes of missing bars were not established and no bars were fabricated. Same SPY asset/2016–2021 era, full-sample terciles, fixed-label conditional intervals, two block lengths and no global multiplicity correction limit generalization. This is an RV proxy, not the original VIX/futures periodicity estimator or evidence of trading value.

## Reproduce and next step

```sh
.venv/bin/python -B scripts/c_spec_window_review.py
```

The command reads existing compact P0 products and verifies their hashes, then replaces only this supplement's own outputs. It never calls a source API or alters P0 data/config/reports. Output folder: `artifacts/C/C_spec_window_preliminary_v1/`; independent review CSV, decision/QA JSON, seven figures and contact sheet; no duplicated daily array or raw-minute table. Read [P0's full source/method report](C_preliminary_RV_profile_results.md) for original math/eligibility/bootstrap checks. Next safe action: design-thread review of the promising PREV closing-hour finding, keeping this C-spec supplement distinct from P0 and from any future full C analysis.
'''
    (ROOT/'reports/C/C_spec_window_preliminary_visual_review.md').write_text(text)
    write_json(OUT/'feasibility_verdict.json',dict(scope='C_SPEC_SUPPLEMENTARY',summary=narrative,by_branch_window=decision,
        P0_primary_verdict='WEAK (unchanged)',not_a_new_blind_test=True,no_full_C_claim=True))


def main():
    """Reconcile and visualize wider C-spec windows without touching P0 outputs."""
    start=time.perf_counter();OUT.mkdir(parents=True,exist_ok=True)
    counts=verify_preservation();p=read_json(CONFIG)
    if p['supplementary_windows']!={k:list(v) for k,v in WINDOWS.items() if k!='OPEN'}:raise ValueError('C-spec window mapping differs from approved P0 config')
    assert sha(ROOT/p['spec_path'])==p['spec_sha256']
    z=np.load(P0/'daily_profiles.npz');all_w=pd.read_csv(P0/'window_shares_by_state.csv');w=all_w[all_w.window.isin(WINDOWS)].copy()
    checks=reconcile(z,w);w['review_role']='C_SPEC_SUPPLEMENTARY';w.to_csv(OUT/'C_spec_window_summaries.csv',index=False,float_format='%.17g')
    qa=dict(status='PASS',scope='C_SPEC_SUPPLEMENTARY',prior_P0_files=counts[0],prior_B_shared_files=counts[1],
        reconciled_summary_rows=checks,tolerance=1e-10,windows=WINDOWS,primary_P0_unchanged=True,
        source_P0_qa_sha256=sha(P0/'qa_results.json'),source_window_table_sha256=sha(P0/'window_shares_by_state.csv'),
        source_daily_arrays_sha256=sha(P0/'daily_profiles.npz'),source_manifest_sha256=sha(P0/'source_manifest.json'),
        protocol_sha256=sha(CONFIG),P0_outputs_manifest_sha256=sha(P0/'outputs_manifest.json'),
        additional_download_bytes=0,bootstrap='Reuse verified P0 fixed-label 1000-draw 5/10-session intervals; no new independent sample',figures=plots(z,w))
    report(w,qa);verify_preservation()
    qa.update(wall_seconds=time.perf_counter()-start,completed_utc=dt.datetime.now(dt.timezone.utc).isoformat())
    write_json(OUT/'qa_results.json',qa)
    print('C_SPEC_SUPPLEMENTARY_QA_PASS',checks,'reconciled rows;',len(qa['figures']),'figures;',qa['wall_seconds'],'seconds')
