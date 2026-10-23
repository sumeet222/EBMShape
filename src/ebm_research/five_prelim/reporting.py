"""Measured figures, provenance sidecars, portable review bundle and fail-closed QA."""
import importlib.metadata
import re
import sys
import textwrap
from zipfile import ZipFile, ZIP_DEFLATED
import numpy as np
import pandas as pd
from .core import *

os.environ['MPLCONFIGDIR']=str(RUN/'cache/matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from .statistics import load_frame,bin_curves,design

FIG=RUN/'reports/figures'
PLOT=RUN/'reports/figure_data'
COLORS=['#2166ac','#178578','#d66018']
LABELS={
 IDS[0]:('SPY synchronous 5-minute log return (bp)','Stock synchronous 5-minute log return (bp)','early / mid / late clock time'),
 IDS[1]:('Current session log RV (389 close intervals)','Next session log RV (389 close intervals)','downside share: low / middle / high fixed thirds'),
 IDS[2]:('SPY same-day open-to-close log return (bp)','IEF same-day open-to-close log return (bp)','prior-available 10Y minus 2Y spread terciles'),
 IDS[3]:('Stock current close-to-close log return (bp)','Same stock next-session log return (bp)','own relative log volume: low / middle / high'),
 IDS[4]:('Absolute published raw surprise (bp)','SPY 14:00–14:30 log return (bp)','negative / positive published raw surprise')}


def read(path):return json.loads(Path(path).read_text())


def fmt(value,digits=3):
    return 'unavailable' if value is None or not np.isfinite(value) else f'{value:.{digits}g}'


def md_table(rows,columns):
    """Small Markdown tables without an optional tabulate dependency."""
    return '| '+' | '.join(columns)+' |\n| '+' | '.join(['---']*len(columns))+' |\n'+''.join(
        '| '+' | '.join(str(row.get(k,'')).replace('|',' / ').replace('\n',' ') for k in columns)+' |\n' for row in rows)


def provenance(id,result):
    cfg,ch=load_config(id)
    expected=dict(experiment_id=id,config_sha256=ch,source_manifest_sha256=sha(RUN/'manifests/validated_inputs.json'),
        target=cfg['target'],predictor=cfg['predictor'],state=cfg['state'],independent_unit=cfg['independent_unit'],time_range=cfg['coverage'])
    inputs=read(RUN/'manifests/validated_inputs.json')
    expected['input_fingerprint']=hashlib.sha256(json.dumps(inputs['derived'],sort_keys=True).encode()).hexdigest()
    for key,value in expected.items():
        if result.get(key)!=value:raise ValueError('RESULT_PROVENANCE_MISMATCH: '+id+':'+key)
    return expected


def check_sidecar(meta,expected,figure=None,data=None):
    """Pure verifier, also used with wrong-ID/target disposable negative fixtures."""
    for key,value in expected.items():
        if meta.get(key)!=value:raise ValueError('FIGURE_METADATA_MISMATCH: '+key)
    if figure is not None and sha(figure)!=meta['figure_sha256']:raise ValueError('FIGURE_HASH_MISMATCH')
    if data is not None and sha(data)!=meta['plot_data_sha256']:raise ValueError('PLOT_DATA_HASH_MISMATCH')
    if meta['experiment_id'] in IDS and meta['axis_semantics']!=list(LABELS[meta['experiment_id']]):raise ValueError('AXIS_SEMANTICS_MISMATCH')
    if meta['experiment_id'] in IDS:
        states=['early','mid','late'] if meta['experiment_id']==IDS[0] else ['negative','positive'] if meta['experiment_id']==IDS[4] else ['low','middle','high']
        if meta.get('series')!=states or meta.get('series_colors')!=dict(zip(states,COLORS)):raise ValueError('STATE_SERIES_ORDER_MISMATCH')
    return True


def check_png(path):
    """Decode actual exports, require legibility and nonblank content; return evidence."""
    with Image.open(path) as im:
        im.load();a=np.asarray(im.convert('RGB'));width,height=im.size
    if width<1200 or height<500:raise ValueError('FIGURE_TOO_SMALL: '+str(path))
    if a.std()<8 or np.mean(np.min(a,axis=2)<220)<.015:raise ValueError('BLANK_FIGURE: '+str(path))
    return dict(width=width,height=height,rgb_sd=float(a.std()),nonwhite_fraction=float(np.mean(np.min(a,axis=2)<220)))


def check_links(path):
    images=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',Path(path).read_text())
    for rel in images:
        if not (Path(path).parent/rel).is_file():raise ValueError('BROKEN_EMBEDDED_IMAGE: '+rel)
    return images


def publish(fig,id,suffix,table,result,*,series=None,notes=''):
    """Save exact chart coordinates before drawing; hash-bind image and all semantics."""
    expected=provenance(id,result);FIG.mkdir(parents=True,exist_ok=True);PLOT.mkdir(parents=True,exist_ok=True)
    name=id+'_'+suffix;csv=PLOT/(name+'.csv');table.to_csv(csv,index=False)
    # Round trip must preserve every plotted numeric coordinate and support mask.
    saved=pd.read_csv(csv)
    for col in table.select_dtypes(include=[np.number]).columns:
        np.testing.assert_allclose(saved[col],table[col],rtol=1e-12,atol=1e-12,equal_nan=True)
    fig.canvas.draw();renderer=fig.canvas.get_renderer();outside=[];undrawn_ticks=set()
    for ax in fig.axes:
        for axis in [ax.xaxis,ax.yaxis]:
            low,high=sorted(axis.get_view_interval())
            for tick in axis.get_major_ticks()+axis.get_minor_ticks():
                if tick.get_loc()<low-1e-10 or tick.get_loc()>high+1e-10:undrawn_ticks.update([tick.label1,tick.label2])
    for text in fig.findobj(matplotlib.text.Text):
        if text in undrawn_ticks or not text.get_visible() or not text.get_text():continue
        box=text.get_window_extent(renderer)
        if box.x0 < -1 or box.y0 < -1 or box.x1>fig.bbox.width+1 or box.y1>fig.bbox.height+1:outside.append(text.get_text()[:70])
    if outside:raise ValueError('CLIPPED_FIGURE_TEXT: '+str(outside))
    path=FIG/(name+'.png');fig.savefig(path,dpi=145,facecolor='white');plt.close(fig)
    imageqa=check_png(path)
    meta=dict(**expected,plot_data_sha256=sha(csv),figure_sha256=sha(path),plot_data_path=str(csv.relative_to(RUN/'reports')),
        axis_semantics=list(LABELS[id]),series=series or [],series_colors=dict(zip(series or [],COLORS)),state_cutpoints=result.get('state_cutpoints_pp',result.get('per_stock_state_cutpoints',
            [0,1/3,2/3,1] if id==IDS[1] else ['10:00','11:30','14:00','16:00'] if id==IDS[0] else None)),
        png_qa=imageqa,chart_input_roundtrip='PASS',text_boundary_check='PASS',notes=notes)
    write_json(path.with_suffix('.meta.json'),meta);check_sidecar(meta,expected,path,csv)
    plot_index=RUN/'experiments'/id/'plots'/('reference_'+suffix+'.json')
    write_json(plot_index,dict(figure=str(path.relative_to(RUN)),figure_sha256=sha(path),sidecar=str(path.with_suffix('.meta.json').relative_to(RUN)),plot_data=str(csv.relative_to(RUN)),
        explanation='One authoritative figure, referenced here without copying image bytes.'))
    return path


def plot_curves(ax,curves,states,id):
    """Unsupported cells are NaN gaps, never joined across missing support."""
    grids=[]
    for i,state in enumerate(states):
        g=curves[curves.state==state].sort_values('bin');grids.append(g.x.to_numpy())
        supported=g.supported.to_numpy(bool);y=np.where(supported,g.y,np.nan);lo=np.where(supported,g.lo,np.nan);hi=np.where(supported,g.hi,np.nan)
        line,=ax.plot(g.x,y,'o-',color=COLORS[i],label=state,linewidth=1.5,markersize=4)
        np.testing.assert_allclose(line.get_xdata(),g.x);np.testing.assert_allclose(line.get_ydata(),y,equal_nan=True)
        if line.get_label()!=state:raise ValueError('REVERSED_STATE_LEGEND')
        ax.fill_between(g.x,lo,hi,color=COLORS[i],alpha=.14)
        if (g.loc[supported,'lo']>g.loc[supported,'hi']).any():raise ValueError('REVERSED_INTERVAL')
    for grid in grids[1:]:np.testing.assert_array_equal(grid,grids[0])
    ax.set(xlabel=LABELS[id][0],ylabel=LABELS[id][1],title='Raw finite-bin conditional means\n95% date-block percentile bands; gaps = insufficient dates')
    ax.legend(title='State',frameon=False);ax.grid(alpha=.2);ax.set_xlim(float(curves.x_lower.min()),float(curves.x_upper.max()))


def rows_slopes(result):
    return [dict(kind='state_slope',state=s,x=i,y=b,lo=result['slope_intervals'][s][0],hi=result['slope_intervals'][s][1],
        n_independent_days=next(r['n_independent_days'] for r in result['state_support'] if r['state']==s)) for i,(s,b) in enumerate(result['state_slopes'].items())]


def error_points(ax,table,title,xlabel):
    for i,row in enumerate(table.to_dict('records')):
        if pd.isna(row['y']):
            ax.text(.03,i,'not estimable',transform=ax.get_yaxis_transform(),va='center',color='.4');continue
        lo,hi=row.get('lo',np.nan),row.get('hi',np.nan)
        if pd.notna(lo) and pd.notna(hi):ax.hlines(i,lo,hi,color=COLORS[i%3],linewidth=2)
        ax.plot(row['y'],i,'o',color=COLORS[i%3])
    ax.set_yticks(np.arange(len(table)),table.state);ax.set_ylim(-.5,len(table)-.5);ax.axvline(0,color='.6',linewidth=.8);ax.set(title=title,xlabel=xlabel);ax.grid(axis='x',alpha=.2)


def figures(id,result):
    cfg,_=load_config(id);dest=RUN/'experiments'/id;hold=result['status']=='DATA HOLD'
    n=result.get('n_independent_days',0);period=(result.get('first') or cfg['coverage'][0])+' to '+(result.get('last') or cfg['coverage'][1])
    plt.rcParams.update({'font.size':10,'axes.titlesize':11,'axes.labelsize':10,'legend.fontsize':9})
    fig,axes=plt.subplots(1,2,figsize=(14,6),layout='constrained');fig.suptitle(id+' | '+result['status']+' | '+str(n)+' independent '+('events' if id==IDS[4] else 'dates'),fontsize=16)
    if hold:
        counts=result.get('state_counts',{r['state']:r['n_independent_days'] for r in result.get('state_support',[])})
        order=['negative','positive'] if id==IDS[4] else ['low','middle','high']
        counts={s:counts[s] for s in order if s in counts}
        table=pd.DataFrame([dict(kind='support',state=s,x=i,y=v,n_events=v if id==IDS[4] else np.nan,n_independent_days=v) for i,(s,v) in enumerate(counts.items())])
        if not table.empty:
            axes[0].bar(table.state,table.y,color=COLORS[:len(table)]);axes[0].set(ylabel='Independent '+('FOMC events' if id==IDS[4] else 'dates'),title='Measured eligible support')
            limit=cfg['support']['min_events_per_sign'] if id==IDS[4] else cfg['support']['min_state_days'];axes[0].axhline(limit,color='black',ls='--',label='Frozen minimum = '+str(limit));axes[0].legend()
            for x,y in zip(table.x,table.y):axes[0].text(x,y+.5,str(y),ha='center')
            axes[0].set_ylim(0,max(max(table.y)*1.2,limit*1.3))
        else:axes[0].axis('off');axes[0].text(.5,.5,'No valid support table',ha='center')
        reason=result.get('reason','Insufficient common predictor/state support under the frozen eligibility rules.')
        if id==IDS[1]:
            inputs=read(RUN/'manifests/validated_inputs.json');f,_,_,_=load_frame(id,cfg,inputs);f=f[f.symbol=='SPY']
            hist,edges=np.histogram(f.q_down,bins=np.linspace(0,1,31))
            axes[1].bar((edges[:-1]+edges[1:])/2,hist,width=np.diff(edges),color=COLORS[0],alpha=.8)
            axes[1].axvline(1/3,color='black',ls='--');axes[1].axvline(2/3,color='black',ls='--')
            axes[1].set(xlabel='Continuous downside share q = RS− / RV',ylabel='SPY sessions',title='NO VALID RESULT for the q-state shape\nMeasured composition support; no response curve')
            table=pd.concat([table,pd.DataFrame(dict(kind='q_histogram',state='SPY',x=(edges[:-1]+edges[1:])/2,x_lower=edges[:-1],x_upper=edges[1:],y=hist,n_independent_days=hist))],ignore_index=True)
        else:
            axes[1].axis('off');axes[1].text(.02,.92,'NO VALID RESULT',fontsize=23,color='#a12e24',va='top',weight='bold');axes[1].text(.02,.75,textwrap.fill(reason,56),va='top',fontsize=12)
        if id==IDS[4]:axes[1].text(.02,.36,'Published raw MPS × 100 → bp.\nOfficial 14:00 releases only.\nNo sign/magnitude economic curve fitted.\nDescriptive signed OLS and event LOO saved separately.',va='top',fontsize=11)
        fig.supxlabel(period+' | exploratory coverage | '+LABELS[id][2]+'\n'+('NO_COMMON_SUPPORT; fixed tail states have only10 and5dates, minimum30.' if id==IDS[1] else ''),fontsize=10)
        if table.empty:table=pd.DataFrame([dict(kind='status',state='NO_VALID_SUPPORT',x=0,y=0,n_independent_days=0)])
        publish(fig,id,'summary',table,result,series=list(counts),notes='NO VALID RESULT: support graphic only; no fabricated economic response')
        return
    curves=pd.read_csv(dest/'results/conditional_curves.csv');states=list(result['state_slopes']);plot_curves(axes[0],curves,states,id)
    slopes=pd.DataFrame(rows_slopes(result));additional=slopes
    if id==IDS[1]:
        sr=result['raw_semivariance_reference'];v=sr['coefficient_intervals']
        additional=pd.DataFrame([dict(kind='raw_semivariance',state=s,x=i,y=sr[k],lo=v[c][0],hi=v[c][1],n_independent_days=n) for i,(s,k,c) in enumerate([
            ('negative RS','negative_coefficient','slope:total'),('positive RS','positive_coefficient','RS_plus_scaled'),('lag RV','lag_RV_coefficient','lag_RV_scaled')])])
        error_points(axes[1],additional,'Raw next-RV reference, controlling lag RV\n95% joint date-block percentile intervals','Next RV response / current RV component (unitless)')
    else:error_points(axes[1],slopes,'State-specific OLS slopes\n95% joint date-block percentile intervals','Response units per predictor unit')
    state_note=(' | spread cutpoints (pp): '+', '.join(fmt(v) for v in result['state_cutpoints_pp'])) if id==IDS[2] else (' | per-stock reference cutpoints in sidecar' if id==IDS[3] else '')
    note=period+' | '+LABELS[id][2]+state_note+'\nB=500, 5-session blocks; exploratory. Curvature not tested. Bin means are unadjusted; OLS includes declared controls.'
    fig.supxlabel(note,fontsize=9)
    data=pd.concat([curves.assign(kind='curve'),additional],ignore_index=True);publish(fig,id,'summary',data,result,series=states)
    # Separate support view, including the required per-stock beta audit for P01.
    fig,axes=plt.subplots(1,2,figsize=(14,6),layout='constrained');fig.suptitle(id+' | joint support audit | '+period,fontsize=15)
    for i,state in enumerate(states):
        g=curves[curves.state==state];axes[0].plot(g.x,g.n_independent_days,'o-',label=state,color=COLORS[i])
    axes[0].axhline(cfg['support']['min_bin_independent'],color='black',ls='--',label='Minimum = 10 dates');axes[0].set(xlabel=LABELS[id][0],ylabel='Unique dates per finite bin',title='Counts, not stock/bar rows');axes[0].legend();axes[0].grid(alpha=.2)
    support=curves.assign(kind='bin_support',y=curves.n_independent_days)
    if id==IDS[0]:
        beta=pd.read_csv(dest/'results/stock_state_betas.csv');names=sorted(beta.symbol.unique())
        for i,state in enumerate(states):
            g=beta[beta.state==state].set_index('symbol').loc[names];y=np.arange(len(names))+(i-1)*.22
            for a,b,c in zip(g.lo,g.hi,y):axes[1].hlines(c,a,b,color=COLORS[i],alpha=.7)
            axes[1].plot(g.beta,y,'o',label=state,color=COLORS[i],markersize=4)
        axes[1].set_yticks(np.arange(len(names)),names);axes[1].set(xlabel='Stock beta to synchronous SPY return',title='Per-stock state slopes; date-block intervals');axes[1].legend();axes[1].grid(axis='x',alpha=.2)
        support=pd.concat([support,beta.assign(kind='stock_beta',y=beta.beta,x=beta.symbol.map({s:i for i,s in enumerate(names)}))],ignore_index=True)
    else:
        counts=pd.DataFrame(result['state_support']).set_index('state').loc[states].reset_index()
        bars=axes[1].bar(counts.state,counts.n_independent_days,color=COLORS)
        np.testing.assert_allclose([bar.get_height() for bar in bars],counts.n_independent_days)
        for i,bar in enumerate(bars):np.testing.assert_allclose(bar.get_facecolor(),matplotlib.colors.to_rgba(COLORS[i]))
        axes[1].set(ylabel='Unique dates with this state',title='Overall state support (dates can overlap for pooled stocks)')
        support=pd.concat([support,counts.assign(kind='state_support',x=np.arange(len(counts)),y=counts.n_independent_days)],ignore_index=True)
    fig.supxlabel('Reference-only common X grid; no line interpolation across unsupported cells in response plots. '+('Balanced all-stock dates: '+str(result.get('balanced_panel_days')) if id==IDS[0] else LABELS[id][2]),fontsize=9)
    publish(fig,id,'support',support,result,series=states)
    # Whole linear surface four-point contrast; controls and intercepts cancel.
    rows=[dict(kind='contrast',state='main, 95% block interval',x=0,y=result['contrast'],lo=result['contrast_lo'],hi=result['contrast_hi'],n_independent_days=n)]
    rows += [dict(kind='contrast',state=s,x=i+1,y=result[k],lo=np.nan,hi=np.nan,n_independent_days=n) for i,(s,k) in enumerate([
        ('without top 1% |X| dates','contrast_without_top1percent'),('reference period','contrast_reference_period'),('later period','contrast_later_period')])]
    contrast=pd.DataFrame(rows);fig,axes=plt.subplots(1,2,figsize=(14,6),layout='constrained');fig.suptitle(id+' | declared slope and whole-surface contrasts | '+result['status'],fontsize=15)
    error_points(axes[0],contrast,'Last state minus first state slope\nSensitivity points have no displayed intervals','Response units / predictor unit');axes[0].axvline(cfg['materiality'],color='.5',ls=':');axes[0].axvline(-cfg['materiality'],color='.5',ls=':')
    if result['common_support'].get('anchor_support'):
        delta=cfg['x_anchors'][1]-cfg['x_anchors'][0];anchor=contrast.iloc[:1].copy();anchor[['y','lo','hi']]*=delta;anchor['kind']='anchored_whole_surface';anchor['state']='D = (b_last − b_first) × (x_b − x_a)'
        error_points(axes[1],anchor,'Whole fitted linear-surface four-point contrast\nX anchors: '+str(cfg['x_anchors']),'Response units');contrast=pd.concat([contrast,anchor],ignore_index=True)
    else:axes[1].axis('off');axes[1].text(.02,.8,'Anchored contrast withheld',fontsize=17);axes[1].text(.02,.65,'Frozen X anchors fall outside shared support.\nNo extrapolated four-point claim.',fontsize=12)
    if id==IDS[0]:
        disp=result.get('early_minus_late_beta_dispersion');ci=result.get('dispersion_block_interval')
        extra='Early − late cross-stock beta SD: '+fmt(disp)+'; 95% shared-date interval '+str([float(f'{v:.3g}') for v in ci] if ci else 'unavailable')
        contrast=pd.concat([contrast,pd.DataFrame([dict(kind='dispersion',state='early_minus_late_beta_SD',x=0,y=disp,lo=ci[0] if ci else np.nan,hi=ci[1] if ci else np.nan,n_independent_days=result.get('balanced_panel_days',0))])],ignore_index=True)
    else:extra='Control-adjusted OLS surface contrasts; raw finite-bin curves are a separate descriptive estimand.'
    fig.supxlabel(period+' | exploratory; no multiplicity correction or causal claim\n'+extra,fontsize=9)
    publish(fig,id,'shape_contrast',contrast,result,series=states)


def validate_statistics(id,result,inputs):
    """Reconstruct all conditional points and OLS from the shared source, before embedding."""
    cfg,_=load_config(id);f,states,controls,extra=load_frame(id,cfg,inputs)
    if id==IDS[1]:f=f[f.symbol=='SPY'].copy()
    if result['status']=='DATA HOLD':
        counts=f.groupby('state').date_et.nunique().to_dict()
        reported=result.get('state_counts',{r['state']:r['n_independent_days'] for r in result.get('state_support',[])})
        if reported!=counts:raise ValueError('HOLD_COUNTS_DISAGREE')
        return dict(status='PASS',support_counts=counts,curves='no valid state shape presented for DATA HOLD; diagnostic references retained')
    x,columns=design(f,states,controls,len(f.symbol.unique())>1);beta=np.linalg.lstsq(x,f.y.to_numpy(float),rcond=None)[0]
    np.testing.assert_allclose(beta,result['coefficients'],rtol=1e-10,atol=1e-10)
    curves,support=bin_curves(f,states,cfg);saved=pd.read_csv(RUN/'experiments'/id/'results/conditional_curves.csv')
    for col in ['x','x_lower','x_upper','y','lo','hi','n_rows','n_independent_days']:
        np.testing.assert_allclose(saved[col],curves[col],rtol=1e-10,atol=1e-10,equal_nan=True)
    # A direct source-row mean independently checks the first supported bin per state.
    for state in states:
        g=saved[(saved.state==state)&saved.supported].iloc[0];mask=(f.state==state)&(f.x>=g.x_lower)&(f.x<g.x_upper)
        np.testing.assert_allclose(f.loc[mask,'y'].mean(),g.y,rtol=1e-10,atol=1e-10)
        if f.loc[mask,'date_et'].nunique()!=g.n_independent_days:raise ValueError('BIN_DATE_COUNT_DISAGREES')
    return dict(status='PASS',OLS_reconstructed=True,all_curve_coordinates_reconstructed=True,direct_source_bins=len(states),supported_common_bins=result['jointly_supported_bins'],
        bootstrap_valid=result['bootstrap_valid'],CI_center_outside_percentiles=int(((saved.y<saved.lo)|(saved.y>saved.hi)).sum()),
        note='Percentile intervals need not contain original estimates; outside centers flagged, never forced inside. Nonlinear curvature not tested.')


def beta_scatter(result,inputs):
    """Deterministic display thinning only; primary fits/bins retain every eligible row."""
    id=IDS[0];cfg,_=load_config(id);f,states,_,_=load_frame(id,cfg,inputs)
    fig,axes=plt.subplots(1,3,figsize=(15,5.5),sharex=True,sharey=True,layout='constrained');tables=[];support=[]
    for i,(ax,state) in enumerate(zip(axes,states)):
        full=f[f.state==state].sort_values(['date_et','bin_end_utc','symbol']);stride=max(1,int(np.ceil(len(full)/1000)));g=full.iloc[::stride].copy()
        points=ax.scatter(g.x,g.y,s=6,alpha=.3,color=COLORS[i]);np.testing.assert_allclose(points.get_offsets(),g[['x','y']].to_numpy())
        ax.set(title=state+': '+str(full.date_et.nunique())+' dates; '+str(len(full))+' source rows\n'+str(len(g))+' deterministically strided display points',xlabel=LABELS[id][0]);ax.grid(alpha=.2);ax.axhline(0,color='.7',lw=.6);ax.axvline(0,color='.7',lw=.6)
        g['kind']='display_scatter';g['n_independent_days']=1;tables.append(g[['kind','state','symbol','date_et','bin_end_utc','x','y','n_independent_days']])
        for label,mask in [('down',full.x<0),('up',full.x>0)]:support.append(dict(state=state,market_direction=label,n_rows=int(mask.sum()),n_independent_days=full.loc[mask,'date_et'].nunique()))
    axes[0].set_ylabel(LABELS[id][1]);fig.suptitle(id+' | synchronous raw returns by clock state | no curvature claim',fontsize=15)
    fig.supxlabel('2019 only; all primary fits and curves use full matched data. Points are illustrative, correlated within dates; no pointwise inference.',fontsize=10)
    publish(fig,id,'scatter',pd.concat(tables,ignore_index=True),result,series=states,notes='Deterministic date/time/symbol row stride for display only, not model or universe selection')
    pd.DataFrame(support).to_csv(RUN/'experiments'/id/'diagnostics/market_direction_support.csv',index=False)


def limitations(id,result):
    common='All dates shown are exploratory. State-bin means are finite-interval averages, not a raw singleton conditional-mean function. B=500 intervals are conditional date-block sensitivity, without multiplicity correction or confirmatory coverage guarantees. '
    specifics={
      IDS[0]:'2019 only; ten coverage/sector-selected stocks, incomplete minute days excluded without filling. Cross-stock beta dispersion uses common balanced dates and identical resampled dates across stocks. Primary status uses the pooled last-minus-first slope; dispersion is an additional diagnostic. Neither curvature nor a novel intraday effect is asserted.',
      IDS[1]:'SPY2016–2021 is principal; ten-stock2019 is reported separately and must not be pooled with SPY as independent confirmation. RV uses389 adjacent observed closes, excludes overnight and the opening O-C return. Strict prior/next scheduled-session joins discard gaps. Fixed q bins can have weak tail support. Lag logRV is controlled. The raw semivariance regression includes lag RV; it is a separate estimand.',
      IDS[2]:'IEF and SPY are actual ETF symbols, same-day O-C price returns. This avoids claiming dividend-adjusted total returns from the source. FRED is current vintage: observation t is conservatively usable only after17:00ET on the next federal business day; exact historical releases/revisions are not reconstructed. This is a contemporaneous association, not an ex-ante return forecast or exact source replication.',
      IDS[3]:'Native30-minute observed stock OHLCV; split-only, not dividend-adjusted close-to-close price returns. Only full13-bar days retained. Own log volume uses previous20eligible full days, excludes current; terciles fitted per stock in reference period. Next return requires the immediately next scheduled session. SPY O-C is a declared same-day market control, not the target or state. One year and ten stocks limit generalization.',
      IDS[4]:'Raw SF Fed updated FOMC-sheet MPS, not MPS_ORTH. MPS rate percentage points are multiplied by100 to bp (ED4 unit loading in the author paper p16). The publisher chart is only a units crosscheck:53/54overlapping values differ by less than0.025bp, but2019-07-31differs by4.714bp (workbook0.576bp versus chart5.29bp). The cause is unresolved, possibly a vintage/revision difference; no value is silently replaced. Standard14:00 releases verified against official statements; other times excluded, not shifted. Shock construction overlaps the stock-response window, so association is contemporaneous, not an ex-ante forecast or clean causal estimate. Insufficient negative events and unresolved source disagreement limit this branch; the signed OLS/LOO diagnostic does not remove the hold.'}
    return common+specifics[id]


def experiment_text(id,result,*,prefix='figures/'):
    cfg,ch=load_config(id);n=result.get('n_independent_days',0)
    text=f'## {id} — results and limitations\n\n**{result["status"]}**; {n} independent '+('FOMC events' if id==IDS[4] else 'dates')+f'; {result.get("n_rows",0):,} matched rows.\n\n'
    text+=f'![{id} measured summary]({prefix}{id}_summary.png)\n\n'
    if result['status']!='DATA HOLD':
        text+='Primary last-minus-first slope contrast: **'+fmt(result['contrast'])+'**, 95% date-block sensitivity interval **['+fmt(result['contrast_lo'])+', '+fmt(result['contrast_hi'])+']**. Frozen material slope threshold: '+fmt(cfg['materiality'])+'.\n\n'
        text+=md_table([dict(state=s,slope=fmt(v),interval=str([float(f'{a:.4g}') for a in result['slope_intervals'][s]])) for s,v in result['state_slopes'].items()],['state','slope','interval'])+'\n'
        text+='![Whole-surface and slope contrast]('+prefix+id+'_shape_contrast.png)\n\n![Support audit]('+prefix+id+'_support.png)\n\n'
        text+=f'{result["jointly_supported_bins"]} jointly supported common-X bins; {result["bootstrap_valid"]}/{result["B"]} nonsingular resamples. Reference-half contrast '+fmt(result.get('contrast_reference_period'))+', later '+fmt(result.get('contrast_later_period'))+', without top1% absolute-X dates '+fmt(result.get('contrast_without_top1percent'))+'. Sign stability: '+str(result['temporal_and_top1_sign_stable'])+'. These sensitivity results do not replace the primary estimate.\n\n'
        if id==IDS[0]:
            text+='![Synchronous stock-market scatter]('+prefix+id+'_scatter.png)\n\n'
            text+='Early minus late cross-stock beta SD: '+fmt(result.get('early_minus_late_beta_dispersion'))+'; shared-date95% interval '+str(result.get('dispersion_block_interval'))+'; '+str(result.get('balanced_panel_days'))+' common dates. Per-stock beta estimates are saved. '
            text+=('All500 dispersion draws are saved.\n\n' if result.get('dispersion_block_interval') else '**Dispersion compression cannot be assessed reliably:** there are fewer than30common dates across all ten stocks; HCA/KLAC each have only6eligible dates. No balanced-panel dispersion bootstrap or literature-dispersion replication claim is made. The NO-GO status applies to the pooled mean-beta contrast only.\n\n')
        if id==IDS[1]:
            sr=result['raw_semivariance_reference'];text+='Raw-RV reference coefficients: negative '+fmt(sr['negative_coefficient'])+', positive '+fmt(sr['positive_coefficient'])+', lagRV '+fmt(sr['lag_RV_coefficient'])+'; negative-minus-positive '+str(sr['contrast_interval'])+'. No-state current/lag logRV baseline MSE '+fmt(result['lag_controlled_no_state_baseline']['MSE'])+' versus state model '+fmt(result['mean_squared_residual'])+'.\n\n'
            subs=read(RUN/'experiments'/id/'diagnostics/subgroup_models.json');text+=md_table([dict(sample=s['label'],dates=s['n_independent_days'],rows=s['n_rows'],contrast=fmt(s['contrast']),interval=str([s['contrast_lo'],s['contrast_hi']]),status=s['status']) for s in subs],['sample','dates','rows','contrast','interval','status'])+'\n'
        if id==IDS[2]:text+='Reference spread tercile cutpoints (percentage points): '+str(result.get('state_cutpoints_pp'))+'.\n\n'
        if id==IDS[3]:text+='Per-stock reference log-volume cutpoints: `results/summary.json → per_stock_state_cutpoints`. They were not fitted to future returns.\n\n'
        directions={IDS[0]:'The pooled mean beta is slightly lower late than early. This is a mean-slope finding, not evidence of the literature’s cross-stock dispersion compression.',IDS[2]:'The high-spread beta point estimate is lower than the low-spread beta, but the difference interval spans zero. The later period has only the low-spread state (377dates), so its full contrast is not estimable; the reference-period contrast has the opposite sign. State and calendar era are strongly confounded. No reliable sign-reversal or hedge claim follows.',IDS[3]:'The high-minus-low-volume slope estimate is slightly positive, rather than the historical more-negative-autocorrelation direction; its interval is wide. This recent survivorship-selected sample does not reproduce a robust negative contrast.'}
        if id in directions:text+=directions[id]+'\n\n'
    else:
        counts=result.get('state_counts',{r['state']:r['n_independent_days'] for r in result.get('state_support',[])})
        text+='**NO VALID RESULT for the intended state shape.** '+result.get('reason','Insufficient state counts and/or common predictor support.')+' State event/date counts: '+str(counts)+'. No supported response curve or shape-contrast image is presented.\n\n'
        if id==IDS[1]:
            sr=result['raw_semivariance_reference'];text+='The fixed q tail states have10low and5high SPY days (minimum30); reference-only common logRV support is empty. No bins were merged. Continuous q support is shown in the summary. The separate raw-RV reference remains descriptive: negative coefficient '+fmt(sr['negative_coefficient'])+', positive '+fmt(sr['positive_coefficient'])+', lagRV '+fmt(sr['lag_RV_coefficient'])+'; negative-minus-positive95% interval '+str(sr['contrast_interval'])+'. No-state current/lag logRV MSE '+fmt(result['lag_controlled_no_state_baseline']['MSE'])+'; state model '+fmt(result['mean_squared_residual'])+'. The held state-slope contrast and any rank-deficient bootstrap draws are not treated as evidence.\n\n'
            subs=read(RUN/'experiments'/id/'diagnostics/subgroup_models.json');text+=md_table([dict(sample=s['label'],dates=s['n_independent_days'],rows=s['n_rows'],status=s['status']) for s in subs],['sample','dates','rows','status'])+'\n'
        if id==IDS[4]:text+='Descriptive signed linear benchmark slope '+fmt(result.get('signed_linear_benchmark_bp_per_bp'))+' bp SPY response per bp shock; event leave-one-out slopes are saved only as diagnostics. This is not the held sign/magnitude shape.\n\n'
        if id==IDS[4]:
            loo=pd.read_csv(RUN/'experiments'/id/'diagnostics/signed_benchmark_leave_one_event_out.csv')
            text+='Published2016–2021rows:54; verified standard14:00and complete SPY events:47; excluded nonstandard/unverified release-time rows:7. Exact exclusion dates/reasons are in `../manifests/fomc_event_eligibility.csv`. Event leave-one-out signed-slope range ['+fmt(loo.signed_slope_without_event.min())+', '+fmt(loo.signed_slope_without_event.max())+'] bp/bp. No independent-event nonlinear confidence band is estimated under the hold.\n\n'
    text+=limitations(id,result)+'\n\n'
    text+='Exact definitions: Y=`'+cfg['target']+'`; X=`'+cfg['predictor']+'`; Z=`'+cfg['state']+'`.\n\n'
    text+='Config SHA-256 `'+ch+'`; input fingerprint `'+result['input_fingerprint']+'`; source manifest SHA-256 `'+result['source_manifest_sha256']+'`.\n\n'
    return text


def resources():
    trace=[json.loads(s) for s in (RUN/'logs/storage.jsonl').read_text().splitlines()]
    current=Budget().check(0,'final review outputs')
    return dict(hard_cap_bytes=10_000_000_000,measured_peak_bytes=max([current]+[r['used_bytes'] for r in trace]),
        largest_reserved_envelope_bytes=max(r['used_bytes']+r['reserved_bytes'] for r in trace),current_incremental_bytes=current,
        baseline=read(RUN/'manifests/storage_budget.json'),new_data_bytes=sum(p.stat().st_size for p in DATA.rglob('*') if p.is_file()),
        run_bytes=sum(p.stat().st_size for p in RUN.rglob('*') if p.is_file()))


def integrity_audit():
    """Verify frozen sources, old files, twelve unique validated months and no raw temps."""
    inputs=read(RUN/'manifests/validated_inputs.json')
    for ref in inputs['original_source_refs']:
        path_for(ref)
        if 'metadata' in ref:path_for(ref['metadata'])
    for ref in inputs['derived'].values():path_for(ref)
    legacy=read(RUN/'manifests/protected_legacy_files.json');changed=[]
    # Inventory stores path -> identity, not copied source data.
    entries=legacy.get('files',legacy) if isinstance(legacy,dict) else legacy
    if isinstance(entries,dict):entries=[dict(path=k,**(v if isinstance(v,dict) else {'sha256':v})) for k,v in entries.items()]
    for ref in entries:
        p=ROOT/ref['path']
        if not p.exists() or sha(p)!=ref['sha256']:changed.append(ref['path'])
    if changed:raise ValueError('PREEXISTING_FILE_CHANGED: '+str(changed[:5]))
    ledger=[json.loads(s) for s in (RUN/'checkpoints/hf_months.jsonl').read_text().splitlines()];valid=[r for r in ledger if r['status']=='validated']
    union=read(RUN/'manifests/union_acquisition_plan.json');months=[m['month'] for m in union['months']]
    if sorted(r['month'] for r in valid)!=sorted(months) or len(valid)!=len(set(r['month'] for r in valid)):raise ValueError('DUPLICATE_OR_MISSING_VALIDATED_MONTH')
    from .sources import validated_month_output
    for r in valid:validated_month_output(r,r['month'],path_for(r['output']))
    network=[json.loads(s) for s in (RUN/'logs/network.jsonl').read_text().splitlines()]
    market=[r for r in network if r.get('status')==200 and r['path'].endswith('.source.parquet')]
    if len(market)!=len(months) or len(set(r['url'] for r in market))!=len(months):raise ValueError('DUPLICATE_MARKET_DOWNLOAD_PASS')
    if any('/datasets/mito0o852/OHLCV-1m/resolve/'+HF_REV+'/' not in r['url'] for r in market):raise ValueError('MARKET_SOURCE_ALIAS_MIXUP')
    official=read(RUN/'manifests/official_event_times.json');statement_checks=0
    for event in official.values():
        if 'source' in event:path_for(event['source']);statement_checks+=1
    metadata=pd.read_parquet(path_for(read(RUN/'manifests/acquired_sources.json')['small_sources']['instrument_metadata.parquet']))
    identity=metadata[metadata.symbol.isin(['SPY','IEF'])]
    if set(identity.symbol)!={'SPY','IEF'} or not identity.asset_type.eq('ETF').all():raise ValueError('TREASURY_IDENTITY_FAILED')
    leftovers=list((RUN/'scratch').glob('*.parquet'))+list(RUN.rglob('*.part'))+list(DATA.rglob('*.part'))
    if leftovers:raise ValueError('UNEXPECTED_RAW_OR_PARTIAL_TEMP: '+str(leftovers))
    for id in IDS:load_config(id)
    result=dict(status='PASS',protected_preexisting_files=len(entries),changed_preexisting_files=changed,validated_months=len(valid),unique_validated_months=len(set(r['month'] for r in valid)),
        raw_monthly_temps_remaining=0,source_and_derived_hashes_checked=len(inputs['original_source_refs'])+len(inputs['derived']),
        dataset='mito0o852/OHLCV-1m',revision=HF_REV,no_mirror=True,bootstrap_B=500,seed=20261022)
    result['successful_monthly_network_transfers']=len(market);result['total_monthly_network_bytes']=sum(r['bytes'] for r in market)
    result['additional_official_statement_hashes_checked']=statement_checks
    write_json(RUN/'manifests/final_integrity_QA.json',result);return result


def overview(results):
    fig,axes=plt.subplots(3,2,figsize=(20,15),layout='constrained')
    for ax,id in zip(axes.flat,IDS):
        with Image.open(FIG/(id+'_summary.png')) as im:ax.imshow(np.asarray(im.convert('RGB')))
        ax.axis('off')
    axes.flat[5].axis('off');lines=['FIVE PRELIMINARY SCREENS','Actual observations; no EBM / ML training','']
    for id in IDS:lines.append(id+': '+results[id]['status'])
    lines+=['','All examined dates are exploratory.','Bands are date-block sensitivity, not confirmation.','Curvature was not tested.','DATA HOLD is distinct from a negative result.']
    axes.flat[5].text(.04,.95,'\n'.join(lines),va='top',fontsize=17,linespacing=1.6)
    fig.suptitle('Five state-dependent research ideas | measured results and support',fontsize=24)
    p=FIG/'five_experiment_overview.png';fig.savefig(p,dpi=120,facecolor='white');plt.close(fig)
    data=pd.DataFrame([dict(experiment_id=id,status=results[id]['status'],n_independent=results[id].get('n_independent_days',0),summary_sha256=sha(FIG/(id+'_summary.png'))) for id in IDS]);csv=PLOT/'five_experiment_overview.csv';data.to_csv(csv,index=False)
    write_json(p.with_suffix('.meta.json'),dict(experiment_id='OVERVIEW',config_sha256=sha(RUN/'manifests/frozen_configs.json'),source_manifest_sha256=sha(RUN/'manifests/validated_inputs.json'),
        input_fingerprint=results[IDS[0]]['input_fingerprint'],target=[CONTRACTS[id]['target'] for id in IDS],predictor=[CONTRACTS[id]['predictor'] for id in IDS],state=[CONTRACTS[id]['state'] for id in IDS],
        independent_unit='dates / FOMC events, never pooled across experiments',time_range={id:load_config(id)[0]['coverage'] for id in IDS},plot_data_sha256=sha(csv),figure_sha256=sha(p),png_qa=check_png(p)))


def bundle():
    path=RUN/'reports/five_experiment_prelim_review_bundle_v1.zip';Budget().check(50_000_000,'review ZIP reservation')
    files=[]
    for p in (RUN/'reports').rglob('*'):
        if p.is_file() and p.suffix in ['.md','.png','.json','.csv'] and 'review_bundle' not in p.name:files.append(p)
    for sub in ['configs','manifests','logs']:
        for p in (RUN/sub).rglob('*'):
            if p.is_file() and p.name not in ['final_verification.json','artifact_inventory.csv'] and p.suffix in ['.json','.jsonl','.md','.csv','.txt','.log'] and p.stat().st_size<3_000_000:files.append(p)
    for id in IDS:
        for p in (RUN/'experiments'/id).rglob('*'):
            if p.is_file() and p.suffix in ['.md','.json','.csv']:files.append(p)
    tmp=path.with_suffix('.zip.tmp')
    with ZipFile(tmp,'w',ZIP_DEFLATED) as z:
        for p in sorted(set(files)):z.write(p,str(p.relative_to(RUN)))
    tmp.replace(path)
    with ZipFile(path) as z:
        if z.testzip() is not None:raise ValueError('REVIEW_ZIP_CORRUPT')
        if any(n.endswith(('.parquet','.xlsx')) for n in z.namelist()):raise ValueError('RAW_DATA_IN_REVIEW_ZIP')
    return path


def write_reports(results,qa,integrity):
    r=resources();write_json(RUN/'manifests/final_storage.json',r)
    rows=[]
    for id,result in results.items():
        cfg,_=load_config(id);contrast='not estimable: '+result.get('reason','insufficient support') if result['status']=='DATA HOLD' else fmt(result['contrast'])+' ['+fmt(result['contrast_lo'])+', '+fmt(result['contrast_hi'])+']'
        rows.append({'Experiment ID':id,'Source and period':', '.join(cfg['source_ids'])+'; '+str(cfg['coverage']),'Scientific target':cfg['target'],'Independent days/events':result.get('n_independent_days',0),'Main state contrast':contrast,'Uncertainty/support':str(result.get('jointly_supported_bins','held'))+' common bins; exploratory','Status':result['status'],'Figure':'[summary](figures/'+id+'_summary.png)'})
    text='# Preliminary screen of five state-dependent EBM research ideas\n\n## Executive decision matrix\n\n'+md_table(rows,list(rows[0]))+'\n'
    text+='![Five measured summaries](figures/five_experiment_overview.png)\n\nImplementation/QA verdict: **PASS WITH QUALIFICATIONS**. The requested preliminary workflow has executed; a DATA HOLD is a completed, explicitly limited branch, not evidence of no relationship. No EBM, ML or trading backtest was run.\n\n'
    text+='## Shared data sources, provenance and storage\n\n'
    text+='Existing SPY minute files (2016–2021), cached observed BAC/KO minute partitions (2019), and ten original native30-minute stock files were reused by exact hash reference. Full source paths, SHA-256, byte sizes and schemas are in `../manifests/validated_inputs.json` and `source_registry.json`; input rows are not copied into experiments. Earlier A/B/C plots, fitted models and conclusions were not used as evidence.\n\n'
    text+='New minute intake used only [mito0o852/OHLCV-1m](https://huggingface.co/datasets/mito0o852/OHLCV-1m), revision `'+HF_REV+'`, twelve2019months, eight missing symbols. Each month was downloaded once, verified against LFS SHA-256, batch-filtered, then its raw temporary file deleted. All twelve validated outputs were skipped on the small-source recovery run. No mirror, snapshot, second minute pass or hidden HF cache. Private-research permission is user-authorized and backed by the supplied human-reported maintainer receipt; upstream vendor rights have not been independently certified. Raw data are excluded from the review bundle.\n\n'
    text+='[ETF daily source](https://huggingface.co/datasets/thecharttruth/etf-data) pinned revision `fb85708dc152ddaa15d9f75608171219cc3fc69a`: actual SPY and IEF O-C prices, instrument metadata identifies both as ETF; names are absent, so no names are invented. Custom research/education terms prohibit redistribution/resale without permission. [FRED DGS10](https://fred.stlouisfed.org/series/DGS10) and DGS2 are current-vintage daily percentage yields, with conservative lag rather than exact historical-vintage reconstruction. [SF Fed raw monetary-policy surprises](https://www.frbsf.org/research-and-insights/data-and-indicators/monetary-policy-surprises/) use updated FOMC sheet MPS. The [author paper, p16](https://www.michaeldbauer.com/files/mps.pdf) specifies percentage-point ED4 scaling: MPS×100 gives bp. The chart CSV is units QA only and has vintage differences. Official statement HTML verifies announcement times;2021 historical-calendar404 was recovered through direct official statements.\n\n'
    text+=f'Measured incremental peak **{r["measured_peak_bytes"]:,} bytes**; largest reserved envelope **{r["largest_reserved_envelope_bytes"]:,} bytes**; current retained **{r["current_incremental_bytes"]:,} bytes** (includes code, filtered data, figures, caches and any existing review ZIP). Hard cap **10,000,000,000 bytes**. Initial forecast620,814,381bytes. See exact final values in `../manifests/final_storage.json` and streaming trace `../logs/storage.jsonl`; later report/ZIP additions are checked again at final verification. Raw monthly temps remaining:0.\n\n'
    text+='Frozen stock list: '+', '.join(STOCKS)+'. Selected by roster membership, sector diversity and coverage before viewing response relationships. CAT/JNJ were not eligible roster members. Reference-only state/X cutoffs; raw data without winsorization; per-date top1% absolute focal-X exclusion is sensitivity only. No missing minute or volume is imputed.\n\n'
    for id,result in results.items():
        section=experiment_text(id,result);text+=section
        individual='# '+id+' preliminary screen\n\n'+experiment_text(id,result,prefix='../../reports/figures/')
        individual+='Reproduction: from repository root, `.venv/bin/python -B scripts/five_prelim.py screen` (verified completed screens are skipped), then `report` and `verify`. Config and source identities are frozen.\n'
        (RUN/'experiments'/id/'report.md').write_text(individual)
    text+='## Cross-experiment methodological comparison\n\nP01 tests contemporaneous clock-dependent stock beta and cross-stock dispersion; P03 tests contemporaneous equity/bond association. P02 and P04 have next-session targets but are exploratory associations with declared lags/controls, not demonstrated implementable forecasts. P05 is an event-response association with overlapping shock measurement and response windows. Their target units, states, populations and periods differ and must not be pooled. None is an exact literature replication or a nonlinear-curvature test. Directional context comes from the controlling design; apparent agreement here is a qualified adaptation, not an exact reproduced coefficient.\n\nConditional raw bin means and controlled OLS slopes are distinct estimands. Uncertainty is date-block resampling across all stock/bar rows together, or independent-event diagnostics for P05. Intervals and GO decisions are exploratory; no untouched confirmation, economic profitability, novelty or EBM theory guarantee follows. NO-GO denotes a supported small contrast in this design, not a population equivalence proof. Missing/rare support remains DATA HOLD.\n\n'
    text+='## Ranked recommendations for possible next EBM studies\n\n'
    ranked=sorted(IDS,key=lambda id:['GO','WEAK','NO-GO','DATA HOLD'].index(results[id]['status']))
    for rank,id in enumerate(ranked,1):
        status=results[id]['status'];reason={'GO':'Material, interval-supported and directionally stable under the frozen checks; merits scientific review before any EBM stage.','WEAK':'Sensitivity or interval width prevents a strong feasibility recommendation; do not tune this examined sample to improve the result.','NO-GO':'The valid preliminary contrast is small under the frozen materiality criterion; preserve the negative result.','DATA HOLD':'Resolve independent support or source limitations first; no EBM shape inference is authorized by this screen.'}[status]
        text+=f'{rank}. **{id}: {status}.** {reason}\n'
    text+='\nRanking groups statuses only; ties retain experiment-ID order. No return-score optimization or cross-experiment p-value ranking.\n\n## QA and artifacts index\n\n'
    text+='All plotted coordinates, interval endpoints and date/event counts: `figure_data/*.csv`; paired `figures/*.meta.json` bind target/state/config/source/input and both hashes. Five separate `../experiments/<ID>/report.md`, results and diagnostics; frozen configs `../configs`; data-lineage schema `../manifests/validated_inputs.json`; source/month/storage/legacy integrity `../manifests/final_integrity_QA.json`; full test and visual QA `../manifests/final_visual_statistical_QA.json`. See [execution integrity](five_experiment_execution_integrity_v1.md).\n\n'
    text+='The [review ZIP](five_experiment_prelim_review_bundle_v1.zip) preserves relative image paths and contains no raw market Parquet or source workbook. Upload **this Markdown, the ZIP, and all six standalone summary/overview PNGs to the EBM Theory ChatGPT chat**. Uploading Markdown alone does not attach its local images.\n'
    (RUN/'reports/five_experiment_prelim_closeout_v1.md').write_text(text)
    commands=['inventory','metadata','freeze','acquire','acquire (small-source recovery; twelve validated months skipped)','derive (timestamp-unit failure interrupted)','derive (strict-universe audit failure)','derive (corrected RTH/cache adaptation; PASS)','screen','report','verify']
    integrity_text='# Five-experiment execution integrity v1\n\n'+f'As of {now()}. Source/legacy/month/config audit: **{integrity["status"]}**; protected preexisting files {integrity["protected_preexisting_files"]}; changed0; unique validated months12/12; remaining raw monthly archives0.\n\n'
    integrity_text+='## Actual execution and reproducibility\n\nWorking directory: repository root. CLI sequence below uses `.venv/bin/python -B scripts/five_prelim.py <phase>`; every phase log is retained under `../logs`.\n\n'+ '\n'.join(str(i+1)+'. '+c for i,c in enumerate(commands))+'\n\n'
    integrity_text+='No packages installed; Python/dependency/code snapshots: `../manifests/runtime_environment.json`. New tests: `.venv/bin/python -B -m unittest discover -s tests -p test_five_prelim.py -v`; scoped existing pure-data/OLS tests recorded in test evidence, excluding EBM training. Synthetic tests do not certify every raw observation.\n\n'
    evidence=RUN/'manifests/test_execution_evidence.json'
    if evidence.exists():integrity_text+=json.dumps(read(evidence),indent=2)+'\n\n'
    integrity_text+='## Configs and experiment QA\n\n'+md_table([dict(ID=id,config_sha256=results[id]['config_sha256'],QA=qa[id]['status'],result=results[id]['status']) for id in IDS],['ID','config_sha256','QA','result'])+'\n'
    integrity_text+='Input fingerprint `'+results[IDS[0]]['input_fingerprint']+'`; source manifest `'+sha(RUN/'manifests/validated_inputs.json')+'`. Original and derived source SHA-256s rechecked before statistics/rendering/final verification. Wrong-ID/target/hash/stale-config fixtures reject; no frozen science changed to work around results.\n\n'
    integrity_text+='## Storage and one-pass evidence\n\n'+json.dumps(r,indent=2)+'\n\nExact monthly ledger `../checkpoints/hf_months.jsonl`, network receipts `../logs/network.jsonl`, controlled deletion paths `../logs/cleanup.jsonl`, storage samples including each1MiB download chunk `../logs/storage.jsonl`. Private sources are read only and not redistributed in the ZIP.\n\n'
    integrity_text+='## Exceptions and recovery\n\nSandbox DNS initially failed; approved network execution succeeded.2021 Fed historical-calendar404 was resolved with direct official statements from published dates; non14:00events remain excluded. A microsecond/nanosecond calendar comparison originally rejected valid SPY sessions; the job was interrupted before derivative output/statistical fits, units normalized and regression-tested. Reused BAC/KO files include extended hours; applying the frozen RTH filter restored eligible sessions. The subsequent complete derivation passed; invalid attempts are preserved in separate logs and never used for results. PyArrow emits sandbox CPU-cache/sysctl warnings without affecting returned data or checks. Publisher chart and workbook vintage differences are documented, not repaired by substituting shocks.\n\n'
    integrity_text+='## Statistical/visual QA\n\n'+json.dumps(qa,indent=2)+'\n\nActual exported PNGs are decoded and tested for minimum size/nonblank content. Text extents, shared X grids, support masks, coordinate roundtrips, independent source-row means and OLS reconstructions are checked. A manual opening of all six reviewer images is separately recorded in `../manifests/manual_visual_review.json`; until present, subjective visual inspection must not be inferred from automated QA.\n'
    manual=RUN/'manifests/manual_visual_review.json'
    if manual.exists():integrity_text+='\nManual review record:\n\n'+json.dumps(read(manual),indent=2)+'\n'
    (RUN/'reports/five_experiment_execution_integrity_v1.md').write_text(integrity_text)


def report():
    Budget().check(80_000_000,'all bounded figures and reports')
    integrity=integrity_audit();inputs=read(RUN/'manifests/validated_inputs.json');results={};qa={}
    for id in IDS:
        result=read(RUN/'experiments'/id/'results/summary.json');provenance(id,result)
        qa[id]=validate_statistics(id,result,inputs);figures(id,result);results[id]=result
    beta_scatter(results[IDS[0]],inputs)
    overview(results);write_json(RUN/'manifests/final_visual_statistical_QA.json',qa)
    versions={name:importlib.metadata.version(name) for name in ['numpy','pandas','pyarrow','scipy','statsmodels','matplotlib','Pillow','exchange_calendars']}
    for name in ['interpret','interpret-core']:
        try:versions[name]=importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:versions[name]='not installed; no EBM trained'
    code=list((ROOT/'src/ebm_research/five_prelim').glob('*.py'))+[ROOT/'scripts/five_prelim.py',ROOT/'tests/test_five_prelim.py']
    write_json(RUN/'manifests/runtime_environment.json',dict(python=sys.version,packages=versions,code={str(p.relative_to(ROOT)):sha(p) for p in sorted(code)},all_installed_distributions=sorted(d.metadata['Name']+'=='+d.version for d in importlib.metadata.distributions()),CLI='.venv/bin/python -B scripts/five_prelim.py <phase>',seed=20261022,B=500))
    write_reports(results,qa,integrity);bundle();verify()


def verify():
    integrity=integrity_audit();checked=[]
    for id in IDS:
        result=read(RUN/'experiments'/id/'results/summary.json');expected=provenance(id,result)
        for p in FIG.glob(id+'_*.png'):
            meta=read(p.with_suffix('.meta.json'));data=RUN/'reports'/meta['plot_data_path'];check_sidecar(meta,expected,p,data);check_png(p);checked.append(str(p.relative_to(RUN)))
        check_links(RUN/'experiments'/id/'report.md')
    overview_path=FIG/'five_experiment_overview.png';m=read(overview_path.with_suffix('.meta.json'))
    expected_overview=dict(experiment_id='OVERVIEW',config_sha256=sha(RUN/'manifests/frozen_configs.json'),source_manifest_sha256=sha(RUN/'manifests/validated_inputs.json'),
        input_fingerprint=result['input_fingerprint'],target=[CONTRACTS[id]['target'] for id in IDS],predictor=[CONTRACTS[id]['predictor'] for id in IDS],state=[CONTRACTS[id]['state'] for id in IDS],
        independent_unit='dates / FOMC events, never pooled across experiments',time_range={id:load_config(id)[0]['coverage'] for id in IDS})
    check_sidecar(m,expected_overview)
    if sha(overview_path)!=m['figure_sha256'] or sha(PLOT/'five_experiment_overview.csv')!=m['plot_data_sha256']:raise ValueError('OVERVIEW_HASH_MISMATCH')
    check_png(overview_path);links=check_links(RUN/'reports/five_experiment_prelim_closeout_v1.md')
    zip_path=RUN/'reports/five_experiment_prelim_review_bundle_v1.zip'
    with ZipFile(zip_path) as z:
        if z.testzip():raise ValueError('ZIP_CRC_FAILED')
        for rel in links:
            name='reports/'+rel
            if hashlib.sha256(z.read(name)).hexdigest()!=sha(RUN/'reports'/rel):raise ValueError('ZIP_IMAGE_STALE')
        if z.read('reports/five_experiment_prelim_closeout_v1.md')!=(RUN/'reports/five_experiment_prelim_closeout_v1.md').read_bytes():raise ValueError('ZIP_REPORT_STALE')
        if any(n.endswith(('.parquet','.xlsx')) for n in z.namelist()):raise ValueError('RAW_MARKET_DATA_IN_BUNDLE')
    storage=resources();write_json(RUN/'manifests/final_storage.json',storage)
    write_json(RUN/'manifests/final_verification.json',dict(at=now(),status='PASS',figure_count=len(checked)+1,embedded_images=len(links),integrity=integrity,storage=storage,review_bundle_sha256=sha(zip_path),review_bundle_bytes=zip_path.stat().st_size))
    write_json(RUN/'checkpoints/current_stage.json',dict(stage=4,at=now(),state='ALL_GATES_VERIFIED',next_action='STOP; upload review artifacts for scientific review. No EBM training authorized.',completed_experiments=IDS,source_registry_sha256=sha(RUN/'manifests/source_registry.json'),frozen_configs_sha256=sha(RUN/'manifests/frozen_configs.json')))
    print('VERIFIED',len(checked)+1,'figures; legacy files unchanged; storage',storage['current_incremental_bytes'],'peak',storage['measured_peak_bytes'],flush=True)
