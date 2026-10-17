"""Model-free C P0 summaries, joint date-block intervals and rendered audit."""
import datetime as dt
import importlib.metadata as metadata
import json
import math
import platform
import time

import numpy as np
import pandas as pd

from .preliminary import (ROOT, OUT, CONFIG, ET, UTC, WINDOWS, SUPPLEMENTARY,
                          NAMES, COLORS, read_json, data_root, source_frame,
                          profile_day, strict_previous, rank_groups,
                          block_indices, bootstrap_means, calendar, sha,
                          write_json, verify_files)

ALL_WINDOWS={**WINDOWS,**SUPPLEMENTARY}
TICKS=np.array([0,6,18,30,42,54,66,77])
CLOCKS=['09:30','10:00','11:00','12:00','13:00','14:00','15:00','15:55']


def collect_days(p,m):
    """Join disjoint existing/supplemental keys in memory; audit every session."""
    data=data_root();cal=calendar(p['source_start'],p['end'])
    dates=np.array([str(s.date()) for s in cal.sessions_in_range(p['source_start'],p['end'])])
    rv=np.full((len(dates),78),np.nan);audit=[];independent=[]
    lookup={s:i for i,s in enumerate(dates)}
    for year in range(2016,2022):
        base=source_frame(data,p,year);pieces=[base];bad=set()
        for tag,entry in m['months'].items():
            if tag.startswith(str(year)):
                verify_files(data,[entry['supplement']])
                pieces.append(pd.read_parquet(data/entry['supplement']['path']))
                bad.update(entry['excluded_snapshot_revision_dates'])
        frame=pd.concat(pieces,ignore_index=True)
        if frame.duplicated(['symbol','timestamp_utc']).any():raise ValueError('INVALID_QA duplicate source keys')
        if set(frame.symbol.unique())!={'SPY'}:raise ValueError('INVALID_QA unexpected symbol')
        frame['day']=frame.timestamp_utc.dt.tz_convert(ET).dt.strftime('%Y-%m-%d')
        if not (frame.session_et.astype(str)==frame.day).all():raise ValueError('INVALID_QA source session date disagrees with ET')
        grouped=dict(tuple(frame.groupby('day',sort=False)))
        for day in dates[np.char.startswith(dates,str(year))]:
            day=str(day)
            f=grouped.get(day,frame.iloc[:0]).sort_values('timestamp_utc')
            grid=cal.session_minutes(day)
            r,reason=profile_day(f,day,cal)
            if day in bad:r=None;reason='SOURCE_SNAPSHOT_REVISION'
            if r is not None:
                rv[lookup[day]]=r
                # Independent scalar arithmetic for one actual full day per year.
                if not any(x['year']==year for x in independent):
                    close=f.close.to_numpy();opening=float(f.open.iloc[0]);manual=np.zeros(78)
                    for j in range(390):
                        previous=opening if j==0 else close[j-1]
                        manual[j//5]+=math.log(close[j]/previous)**2
                    np.testing.assert_allclose(manual,r,atol=1e-15,rtol=1e-10)
                    independent.append(dict(year=year,day=day,max_error=float(np.max(np.abs(manual-r)))))
            audit.append(dict(date=day,source_rows=len(f),expected_rows=len(grid),
                missing_minutes=len(grid.difference(pd.DatetimeIndex(f.timestamp_utc))),
                reason=reason,auxiliary=day<p['start']))
    return dates,rv,pd.DataFrame(audit),independent,cal


def joint_bootstrap(x,labels,p,length,independent=False):
    """Condition on original labels; draw whole scheduled date slots jointly."""
    rng=np.random.default_rng(p['bootstrap']['seed']);draws=[];failed=0;attempts=0
    while len(draws)<p['bootstrap']['B'] and attempts<p['bootstrap']['max_attempts']:
        ix=block_indices(len(x),length,rng);attempts+=1
        if independent:
            # Independent weighted reconstruction, separate from group row means.
            weights=np.bincount(ix,minlength=len(x));means=[]
            for g in range(3):
                w=weights*((labels==g)&np.isfinite(x).all(axis=1))
                if not w.sum():break
                means.append(np.einsum('i,ij->j',w,np.nan_to_num(x))/w.sum())
            value=np.array(means) if len(means)==3 else None
        else:value=bootstrap_means(x,labels,ix)
        if value is None:failed+=1
        else:draws.append(value)
    if len(draws)!=p['bootstrap']['B']:raise ValueError('INVALID_QA insufficient valid bootstrap draws')
    return np.array(draws),dict(length=length,valid=len(draws),failed=failed,attempts=attempts,seed=p['bootstrap']['seed'])


def summarize(q,rem,labels,rv_day,dates,branch,p):
    """Tabulate primary/remaining profiles and prespecified robustness summaries."""
    x=np.c_[q,rem];means=np.array([x[labels==g].mean(axis=0) for g in range(3)])
    prof=[];windows=[];bands=[];metrics=[];bootlog=[];top=[]
    boot={}
    for length in p['bootstrap']['lengths']:
        boot[length],log=joint_bootstrap(x,labels,p,length);bootlog.append(dict(branch=branch,**log))
    n=int((labels>=0).sum());order=np.flatnonzero(labels>=0)
    order=order[np.lexsort((dates[order],-rv_day[order]))];removed=order[:math.ceil(.01*n)]
    keep=(labels>=0)&~np.isin(np.arange(len(labels)),removed)
    for i in removed:top.append(dict(branch=branch,date=dates[i],RV_day=float(rv_day[i]),state=NAMES[labels[i]]))
    total=float(rv_day[labels>=0].sum());concentration=float(rv_day[removed].sum()/total)
    for variant in ['FULL','DROP_TOP1','MEDIAN']:
        vmeans=[]
        for g in range(3):
            mask=(labels==g)&(keep if variant=='DROP_TOP1' else True)
            arr=x[mask];fun=np.median if variant=='MEDIAN' else np.mean
            vmeans.append(fun(arr,axis=0))
        vmeans=np.array(vmeans)
        for mode,start,stop in [('whole',0,78),('remaining',78,150)]:
            mu=vmeans[:,start:stop];difference=mu[2]-mu[0]
            for g in range(3):
                mask=(labels==g)&(keep if variant=='DROP_TOP1' else True)
                for k,value in enumerate(mu[g]):
                    prof.append(dict(branch=branch,mode=mode,variant=variant,state=NAMES[g],
                        bin=k+(6 if mode=='remaining' else 0),mean=float(value),n=int(mask.sum())))
            metrics.append(dict(branch=branch,mode=mode,variant=variant,n=int(keep.sum()) if variant=='DROP_TOP1' else n,
                mean_abs_HL=float(np.abs(difference).mean()),max_abs_HL=float(np.abs(difference).max()),
                sum_abs_HL=float(np.abs(difference).sum()),TV=float(np.abs(difference).sum()/2),sum_HL=float(difference.sum()),
                top1_count=len(removed),top1_RV_concentration=concentration,
                top_contrast_bin=int(np.argmax(np.abs(difference)))+(6 if mode=='remaining' else 0),
                median_profile_sums_to_one=variant!='MEDIAN'))
            for name,(a,b) in ALL_WINDOWS.items():
                if mode=='remaining' and name=='OPEN':continue
                offset=6 if mode=='remaining' else 0;aa,bb=a-offset,b-offset
                samples=x[:,start+aa:start+bb].sum(axis=1)
                for g in range(3):
                    mask=(labels==g)&(keep if variant=='DROP_TOP1' else True)
                    # Median of window shares is not sum of per-bin medians.
                    value=float((np.median if variant=='MEDIAN' else np.mean)(samples[mask]))
                    row=dict(branch=branch,mode=mode,variant=variant,window=name,state=NAMES[g],
                        summary=value,sd=float(samples[mask].std(ddof=1)),n=int(mask.sum()),
                        role='PRIMARY_P0' if name in WINDOWS else 'SUPPLEMENTARY_C_SPEC')
                    if variant=='FULL':
                        for length,draw in boot.items():
                            stat=draw[:,g,start+aa:start+bb].sum(axis=1)
                            row[f'lo_{length}'],row[f'hi_{length}']=map(float,np.percentile(stat,[2.5,97.5]))
                    windows.append(row)
                high=samples[(labels==2)&(keep if variant=='DROP_TOP1' else True)]
                low=samples[(labels==0)&(keep if variant=='DROP_TOP1' else True)]
                fun=np.median if variant=='MEDIAN' else np.mean
                row=dict(branch=branch,mode=mode,variant=variant,window=name,state='high-minus-low',
                    summary=float(fun(high)-fun(low)),sd=float(np.sqrt((high.var(ddof=1)+low.var(ddof=1))/2)),
                    n=len(high)+len(low),role='PRIMARY_P0' if name in WINDOWS else 'SUPPLEMENTARY_C_SPEC')
                if variant=='FULL':
                    for length,draw in boot.items():
                        stat=(draw[:,2,start+aa:start+bb]-draw[:,0,start+aa:start+bb]).sum(axis=1)
                        row[f'lo_{length}'],row[f'hi_{length}']=map(float,np.percentile(stat,[2.5,97.5]))
                windows.append(row)
        if variant=='FULL':
            for length,draw in boot.items():
                for mode,a,b in [('whole',0,78),('remaining',78,150)]:
                    diff=draw[:,2,a:b]-draw[:,0,a:b];lo,hi=np.percentile(diff,[2.5,97.5],axis=0)
                    for j in range(b-a):bands.append(dict(branch=branch,mode=mode,block=length,
                        bin=j+(6 if mode=='remaining' else 0),HL=float(means[2,a+j]-means[0,a+j]),lo=float(lo[j]),hi=float(hi[j])))
    return prof,windows,bands,metrics,bootlog,top


def write_tables(items):
    names=['profile_by_bin','window_shares_by_state','bootstrap_profile_pointwise','effect_metrics','bootstrap_log','top1_dates']
    for name,rows in zip(names,items):pd.DataFrame(rows).to_csv(OUT/(name+'.csv'),index=False,float_format='%.17g')


def verify_tables(p):
    """Rebuild means/windows/ranks/percentiles independently from saved day arrays."""
    z=np.load(OUT/'daily_profiles.npz');q=z['q'];rem=z['remaining'];dates=z['dates'];x=np.c_[q,rem]
    prof=pd.read_csv(OUT/'profile_by_bin.csv');win=pd.read_csv(OUT/'window_shares_by_state.csv')
    band=pd.read_csv(OUT/'bootstrap_profile_pointwise.csv');checks=[]
    for branch,key in [('OPEN','open_labels'),('PREV','prev_labels')]:
        label=z[key];state=z['RV_open' if branch=='OPEN' else 'RV_prev']
        valid=np.flatnonzero(label>=0);ordered=sorted(valid,key=lambda i:(state[i],dates[i]))
        rebuilt=np.full(len(label),-1)
        for rank,i in enumerate(ordered):rebuilt[i]=3*rank//len(ordered)
        np.testing.assert_array_equal(rebuilt,label)
        for mode,arr,offset in [('whole',q,0),('remaining',rem,6)]:
            for g in range(3):
                f=prof[(prof.branch==branch)&(prof['mode']==mode)&(prof.variant=='FULL')&(prof.state==NAMES[g])].sort_values('bin')
                expected=np.sum(arr[label==g],axis=0)/np.sum(label==g)
                np.testing.assert_allclose(f['mean'],expected,atol=1e-10,rtol=0)
                np.testing.assert_allclose(expected.sum(),1,atol=1e-10,rtol=0)
                for name,(a,b) in ALL_WINDOWS.items():
                    if mode=='remaining' and name=='OPEN':continue
                    v=np.mean([sum(row[a-offset:b-offset]) for row in arr[label==g]])
                    row=win[(win.branch==branch)&(win['mode']==mode)&(win.variant=='FULL')&(win.window==name)&(win.state==NAMES[g])].iloc[0]
                    np.testing.assert_allclose(row.summary,v,atol=1e-10,rtol=0)
        order=sorted(valid,key=lambda i:(-z['RV_day'][i],dates[i]));drop=set(order[:math.ceil(.01*len(valid))])
        for variant in ['FULL','DROP_TOP1','MEDIAN']:
            fun=np.median if variant=='MEDIAN' else np.mean
            for mode,arr,offset in [('whole',q,0),('remaining',rem,6)]:
                for g in range(3):
                    rows=np.array([i for i in valid if label[i]==g and (variant!='DROP_TOP1' or i not in drop)])
                    expected=fun(arr[rows],axis=0)
                    f=prof[(prof.branch==branch)&(prof['mode']==mode)&(prof.variant==variant)&(prof.state==NAMES[g])].sort_values('bin')
                    np.testing.assert_allclose(f['mean'],expected,atol=1e-10,rtol=0)
                    assert (f.n==len(rows)).all()
                for name,(a,b) in ALL_WINDOWS.items():
                    if mode=='remaining' and name=='OPEN':continue
                    values=np.array([sum(row[a-offset:b-offset]) for row in arr])
                    expectations=[]
                    for g in range(3):
                        rows=[i for i in valid if label[i]==g and (variant!='DROP_TOP1' or i not in drop)]
                        v=fun(values[rows]);expectations.append(v)
                        f=win[(win.branch==branch)&(win['mode']==mode)&(win.variant==variant)&(win.window==name)&(win.state==NAMES[g])].iloc[0]
                        np.testing.assert_allclose(f.summary,v,atol=1e-10,rtol=0)
                    f=win[(win.branch==branch)&(win['mode']==mode)&(win.variant==variant)&(win.window==name)&(win.state=='high-minus-low')].iloc[0]
                    np.testing.assert_allclose(f.summary,expectations[2]-expectations[0],atol=1e-10,rtol=0)
        for length in p['bootstrap']['lengths']:
            draw,log=joint_bootstrap(x,label,p,length,independent=True)
            for mode,a,b in [('whole',0,78),('remaining',78,150)]:
                expected=np.percentile(draw[:,2,a:b]-draw[:,0,a:b],[2.5,97.5],axis=0)
                f=band[(band.branch==branch)&(band['mode']==mode)&(band.block==length)].sort_values('bin')
                np.testing.assert_allclose(f[['lo','hi']].to_numpy().T,expected,atol=1e-10,rtol=0)
                for name,(aa,bb) in ALL_WINDOWS.items():
                    if mode=='remaining' and name=='OPEN':continue
                    offset=6 if mode=='remaining' else 0
                    for state,g in [(NAMES[0],0),(NAMES[1],1),(NAMES[2],2),('high-minus-low',None)]:
                        values=draw[:,g,a+aa-offset:a+bb-offset].sum(axis=1) if g is not None else (draw[:,2,a+aa-offset:a+bb-offset]-draw[:,0,a+aa-offset:a+bb-offset]).sum(axis=1)
                        expected=np.percentile(values,[2.5,97.5])
                        row=win[(win.branch==branch)&(win['mode']==mode)&(win.variant=='FULL')&(win.window==name)&(win.state==state)].iloc[0]
                        np.testing.assert_allclose(row[[f'lo_{length}',f'hi_{length}']].to_numpy(float),expected,atol=1e-10,rtol=0)
            checks.append(dict(branch=branch,block=length,status='PASS',tolerance=1e-10,**{k:v for k,v in log.items() if k!='length'}))
    return checks


def plot_all(p,meta):
    """Twelve fixed figures driven directly by the reconciled saved tables."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from PIL import Image,ImageOps,ImageDraw
    plt.rcParams.update({'font.size':12,'axes.titlesize':14,'axes.labelsize':12,'legend.fontsize':10})
    figure_dir=OUT/'figures';figure_dir.mkdir(exist_ok=True)
    z=np.load(OUT/'daily_profiles.npz');prof=pd.read_csv(OUT/'profile_by_bin.csv');win=pd.read_csv(OUT/'window_shares_by_state.csv')
    band=pd.read_csv(OUT/'bootstrap_profile_pointwise.csv');metrics=pd.read_csv(OUT/'effect_metrics.csv')
    full=prof[prof.variant=='FULL'];figures=[];plot_qa=[]
    ymax=float(full['mean'].max()*1.15)
    limit=float(np.abs(band[['lo','hi']].to_numpy()).max()*1.08)
    def clock(ax,remaining=False):
        ticks=TICKS[TICKS>=6] if remaining else TICKS
        ax.set_xticks(ticks,[CLOCKS[list(TICKS).index(t)] for t in ticks]);ax.set_xlabel('Five-minute bin start · America/New_York')
        ax.grid(alpha=.2);ax.set_xlim(6 if remaining else 0,77)
    def save(fig,name,title,axes):
        fig.suptitle(title,fontsize=16)
        fig.text(.5,.012,'SPY · 2016–2021 · descriptive RV proxy · fixed-label date-block intervals are pointwise, not simultaneous',ha='center',fontsize=10)
        fig.tight_layout(rect=[0,.04,1,.94]);path=figure_dir/name
        fig.savefig(path,dpi=160);plt.close(fig);figures.append(path)
        with Image.open(path) as im:
            im.load();assert im.width>=1600 and np.asarray(im).std()>5
            plot_qa.append(dict(file=path.relative_to(ROOT).as_posix(),width=im.width,height=im.height,sha256=sha(path)))
    for bi,branch in enumerate(['OPEN','PREV']):
        suffix='RETROSPECTIVE: first six bins overlap state' if branch=='OPEN' else 'State from immediate prior scheduled full session'
        fig,ax=plt.subplots(figsize=(12,6))
        for g,color in zip(NAMES,COLORS):
            d=full[(full.branch==branch)&(full['mode']=='whole')&(full.state==g)].sort_values('bin')
            ax.plot(d.bin,d['mean'],label=f'{g} (n={d.n.iloc[0]})',color=color)
        ax.set_ylim(0,ymax);ax.set_ylabel('Mean daily RV fraction per five-minute bin');clock(ax);ax.legend()
        if branch=='OPEN':ax.axvspan(0,5.9,alpha=.12,color='gray')
        assert len(ax.get_legend().texts)==3
        save(fig,f'{1+bi:02}_{branch.lower()}_three_state_profiles.png',f'{branch} RV terciles · {suffix}',[ax])
        fig,ax=plt.subplots(figsize=(12,6))
        d=band[(band.branch==branch)&(band['mode']=='whole')&(band.block==5)].sort_values('bin')
        ax.plot(d.bin,d.HL,color=COLORS[2],label='high − low');ax.fill_between(d.bin,d.lo,d.hi,color=COLORS[2],alpha=.2,label='95% pointwise · 5-session blocks')
        ax.axhline(0,color='black',lw=.8);ax.set_ylim(-limit,limit);ax.set_ylabel('Difference in daily RV fraction');clock(ax);ax.legend()
        if branch=='OPEN':ax.axvspan(0,5.9,alpha=.12,color='gray')
        save(fig,f'{3+bi:02}_{branch.lower()}_high_minus_low_pointwise.png',f'{branch} · normalized whole-day H−L · {suffix}',[ax])
        fig,ax=plt.subplots(figsize=(12,6));xs=np.arange(3)
        for g,color in zip(NAMES,COLORS):
            d=win[(win.branch==branch)&(win['mode']=='whole')&(win.variant=='FULL')&(win.state==g)].set_index('window').loc[list(WINDOWS)]
            xpos=xs+(NAMES.index(g)-1)*.22
            ax.errorbar(xpos,d.summary,yerr=[d.summary-d.lo_5,d.hi_5-d.summary],fmt='o',capsize=5,color=color,label=f'{g} (n={int(d.n.iloc[0])})')
        ax.set_xticks(xs,['OPEN 09:30–10:00','MID 12:00–13:00','CLOSE 15:30–16:00']);ax.set_ylabel('Fraction of whole-day RV (unequal window durations)');ax.set_ylim(0,meta['share_ymax']);ax.legend();ax.grid(alpha=.2)
        save(fig,f'{5+bi:02}_{branch.lower()}_window_share_summary.png',f'{branch} · P0 windows · group means and 95% intervals (block 5)',[ax])
        fig,axs=plt.subplots(1,3,figsize=(13,6),sharey=True);label=z['open_labels' if branch=='OPEN' else 'prev_labels']
        for ax,(name,(a,b)) in zip(axs,WINDOWS.items()):
            shares=z['q'][:,a:b].sum(axis=1);vals=[shares[label==g] for g in range(3)]
            boxes=ax.boxplot(vals,tick_labels=NAMES,showfliers=True,patch_artist=True,flierprops=dict(marker='.',markersize=3,alpha=.4))
            for box,color in zip(boxes['boxes'],COLORS):box.set_facecolor(color);box.set_alpha(.4)
            ax.set_title({'OPEN':'OPEN 09:30–10:00','MID':'MID 12:00–13:00','CLOSE':'CLOSE 15:30–16:00'}[name]);ax.set_ylim(0,1);ax.grid(alpha=.2)
        axs[0].set_ylabel('Daily window fraction · all outliers shown')
        save(fig,f'{7+bi:02}_{branch.lower()}_window_share_distributions.png',f'{branch} · primary daily window distributions · n={int((label>=0).sum())}',axs)
        fig,axs=plt.subplots(2,1,figsize=(12,8),sharex=True)
        for g,color in zip(NAMES,COLORS):
            d=full[(full.branch==branch)&(full['mode']=='remaining')&(full.state==g)].sort_values('bin')
            axs[0].plot(d.bin,d['mean'],color=color,label=f'{g} (n={d.n.iloc[0]})')
        axs[0].set_ylim(0,ymax);axs[0].set_ylabel('Mean remaining-RV fraction');axs[0].legend()
        d=band[(band.branch==branch)&(band['mode']=='remaining')&(band.block==5)].sort_values('bin')
        axs[1].plot(d.bin,d.HL,color=COLORS[2]);axs[1].fill_between(d.bin,d.lo,d.hi,alpha=.2,color=COLORS[2]);axs[1].axhline(0,color='black',lw=.8)
        axs[1].set_ylim(-limit,limit);axs[1].set_ylabel('H−L · 95% pointwise block 5')
        for ax in axs:clock(ax,True)
        save(fig,f'{9+bi:02}_{branch.lower()}_nonoverlap_post1000.png',f'{branch} · post-10:00 renormalized 72-bin profile · same fixed states',axs)
    fig,axs=plt.subplots(1,2,figsize=(13,6),sharey=True)
    for ax,branch in zip(axs,['OPEN','PREV']):
        for variant,marker in [('FULL','o'),('DROP_TOP1','s'),('MEDIAN','^')]:
            d=win[(win.branch==branch)&(win['mode']=='remaining')&(win.variant==variant)&(win.state=='high-minus-low')].set_index('window').loc[['MID','CLOSE']]
            ax.plot([0,1],d.summary,marker=marker,label=f'{variant} (H+L n={int(d.n.iloc[0])})')
        ax.axhline(0,color='black',lw=.8);ax.set_xticks([0,1],['MID 12:00–13:00','CLOSE 15:30–16:00']);ax.set_title(branch);ax.legend();ax.grid(alpha=.2)
    axs[0].set_ylabel('H−L fraction of remaining (post-10:00) RV')
    save(fig,'11_top1pct_and_median_fragility.png','Robustness · fixed labels · FULL primary · median of daily window shares',axs)
    fig,axs=plt.subplots(1,2,figsize=(13,6))
    years=pd.to_datetime(z['dates']).year
    for branch,offset in [('OPEN',-.17),('PREV',.17)]:
        label=z['open_labels' if branch=='OPEN' else 'prev_labels']
        axs[0].bar(np.arange(2016,2022)+offset,[int(((years==y)&(label>=0)).sum()) for y in range(2016,2022)],width=.34,label=branch)
    axs[0].set_title('Eligible sessions by year');axs[0].set_ylabel('Session count');axs[0].legend()
    for branch,offset in [('OPEN',-.1),('PREV',.1)]:
        d=win[(win.branch==branch)&(win['mode']=='remaining')&(win.variant=='FULL')&(win.state=='high-minus-low')].set_index('window').loc[['MID','CLOSE']]
        axs[1].plot(np.array([0,1])+offset,d.summary/d.sd,'o-',label=branch)
    axs[1].set_xticks([0,1],['MID','CLOSE']);axs[1].axhline(0,color='black',lw=.8);axs[1].set_ylabel('H−L / pooled daily within-group SD');axs[1].set_title('Remaining-day effect vs daily dispersion');axs[1].legend()
    save(fig,'12_coverage_and_effect_sizes.png','Coverage and descriptive standardized effects · not a predictive test',axs)
    thumbs=[]
    for path in sorted(figures):
        with Image.open(path) as im:
            thumb=ImageOps.contain(im.convert('RGB'),(650,440));tile=Image.new('RGB',(670,475),'white');tile.paste(thumb,((670-thumb.width)//2,25));ImageDraw.Draw(tile).text((10,5),path.name,fill='black');thumbs.append(tile)
    sheet=Image.new('RGB',(2010,1900),'#eeeeee')
    for i,im in enumerate(thumbs):sheet.paste(im,((i%3)*670,(i//3)*475))
    sheet.save(figure_dir/'contact_sheet.png')
    # Comparable panels use exactly common limits and ordered ET ticks by construction.
    return dict(images=plot_qa,common_profile_ylim=[0,ymax],common_contrast_ylim=[-limit,limit],ticks=TICKS.tolist(),clock_labels=CLOCKS,legends_three_groups=True,pointwise_not_simultaneous=True)


def run():
    """Execute one frozen, descriptive-only P0 with no model or held-out reads."""
    start=time.perf_counter();p=read_json(CONFIG);m=read_json(OUT/'source_manifest.json')
    if m.get('complete_months')!=72 or m['protocol_sha256']!=sha(CONFIG):raise RuntimeError('SOURCE_INCOMPLETE: resume acquire first')
    if sha(ROOT/p['spec_path'])!=p['spec_sha256']:raise ValueError('C specification changed after freeze')
    dates,rv,audit,independent,cal=collect_days(p,m)
    total=rv.sum(axis=1);opening=rv[:,:6].sum(axis=1);prev,previous_reasons=strict_previous(dates,total,cal)
    q=rv/total[:,None];remaining=rv[:,6:]/rv[:,6:].sum(axis=1)[:,None]
    allowed=(dates>=p['start'])&(dates<=p['end'])&np.isfinite(q).all(axis=1)
    if allowed.sum()<p['min_days'] or len(set(s[:4] for s in dates[allowed]))<p['min_years']:
        audit.to_csv(OUT/'missingness_exclusions.csv',index=False)
        raise RuntimeError('INSUFFICIENT_COVERAGE: fewer than300 complete days across2 years; no main scientific verdict')
    if not np.isfinite(remaining[allowed]).all():raise ValueError('INVALID_QA nonpositive remaining-day RV denominator')
    open_labels,open_meta=rank_groups(np.where(allowed,opening,np.nan),dates)
    prev_labels,prev_meta=rank_groups(np.where(allowed,prev,np.nan),dates)
    for values in [q[allowed],remaining[allowed]]:
        assert np.isfinite(values).all() and (values>=0).all()
        np.testing.assert_allclose(values.sum(axis=1),1,atol=1e-10,rtol=0)
    audit['previous_reason']=previous_reasons;audit['OPEN_state']=open_labels;audit['PREV_state']=prev_labels
    audit.to_csv(OUT/'missingness_exclusions.csv',index=False)
    np.savez_compressed(OUT/'daily_profiles.npz',dates=dates,rv=rv,q=q,remaining=remaining,RV_day=total,RV_open=opening,RV_prev=prev,open_labels=open_labels,prev_labels=prev_labels)
    pd.DataFrame(dict(date=dates,RV_day=total,RV_open=opening,RV_prev=prev,OPEN_state=open_labels,PREV_state=prev_labels)).to_csv(OUT/'daily_states.csv',index=False,float_format='%.17g')
    accum=[[] for _ in range(6)]
    for branch,labels in [('OPEN',open_labels),('PREV',prev_labels)]:
        result=summarize(q,remaining,labels,total,dates,branch,p)
        for target,rows in zip(accum,result):target.extend(rows)
        print(branch,'summaries/bootstrap complete',flush=True)
    write_tables(accum)
    matched=(open_labels>=0)&(prev_labels>=0);matched_rows=[]
    for branch,labels in [('OPEN',open_labels),('PREV',prev_labels)]:
        for mode,array,offset in [('whole',q,0),('remaining',remaining,6)]:
            for name,(a,b) in ALL_WINDOWS.items():
                if mode=='remaining' and name=='OPEN':continue
                values=array[:,a-offset:b-offset].sum(axis=1)
                low=values[matched&(labels==0)];high=values[matched&(labels==2)]
                matched_rows.append(dict(branch=branch,mode=mode,window=name,HL=float(high.mean()-low.mean()),n_low=len(low),n_high=len(high),matched_dates=int(matched.sum()),labels='original fixed branch ranks, not reranked'))
    pd.DataFrame(matched_rows).to_csv(OUT/'matched_date_comparison.csv',index=False,float_format='%.17g')
    win=pd.DataFrame(accum[1]);share_ymax=float(win.loc[(win.variant=='FULL')&(win['mode']=='whole')&(win.window.isin(WINDOWS))&(win.state!='high-minus-low'),'hi_5'].max()*1.15)
    meta=dict(status='NUMERIC_QA_PENDING',protocol_sha256=sha(CONFIG),source_manifest_sha256=sha(OUT/'source_manifest.json'),
        OPEN=open_meta,PREV=prev_meta,first=str(dates[allowed][0]),last=str(dates[allowed][-1]),
        scheduled_source_slots=len(dates),matched_dates=int(matched.sum()),cross_state_counts=pd.crosstab(open_labels[matched],prev_labels[matched]).values.tolist(),
        exclusion_counts=audit.loc[~audit.auxiliary,'reason'].value_counts().to_dict(),predecessor_exclusions=audit.loc[allowed,'previous_reason'].value_counts().to_dict(),
        source_scalar_crosschecks=independent,share_ymax=share_ymax,versions={s:metadata.version(s) for s in ['numpy','pandas','pyarrow','exchange-calendars','matplotlib']},
        python=platform.python_version(),transfer_bytes=m['cumulative_body_bytes'],retained_cache_bytes=m['retained_cache_bytes'],source_start=p['source_start'],source_end=p['end'])
    checks=verify_tables(p);print('Independent table/interval reconstruction PASS',flush=True)
    plotqa=plot_all(p,meta)
    snapshot=read_json(OUT/'start_snapshot.json');changed=[]
    for ref in snapshot['files']:
        file=(ROOT if ref['base']=='repo' else data_root())/ref['path']
        if not file.exists() or sha(file)!=ref['sha256']:changed.append(ref['path'])
    if changed:raise ValueError('INVALID_QA preexisting file changed: '+str(changed))
    meta.update(status='PASS',bootstrap_independent_reconstruction=checks,plots=plotqa,preserved_file_count=len(snapshot['files']),
        B_and_preexisting_files_unchanged=True,wall_seconds=time.perf_counter()-start,completed_utc=dt.datetime.now(UTC).isoformat())
    write_json(OUT/'qa_results.json',meta)
    print('C_P0_QA_PASS',meta['OPEN']['n'],meta['PREV']['n'],'seconds',meta['wall_seconds'],flush=True)
