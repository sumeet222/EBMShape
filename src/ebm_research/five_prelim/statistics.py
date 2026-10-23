"""Whole-date exploratory OLS and shared-grid conditional means; no EBM/ML."""
import hashlib
import json
import numpy as np
import pandas as pd
from .core import *
from .features import CAL


def block_weights(dates,length,B,seed,event=False):
    """Circular scheduled-day blocks; identical date weights shared across stocks."""
    dates=np.asarray(dates);rng=np.random.default_rng(seed)
    if event:
        n=len(dates);return np.array([np.bincount(rng.integers(n,size=n),minlength=n) for _ in range(B)],float)
    sessions=CAL.sessions_in_range(min(dates),max(dates)).strftime('%Y-%m-%d').to_numpy();span=len(sessions)
    positions=pd.Index(sessions).get_indexer(dates)
    if (positions<0).any():raise ValueError('BLOCK_NON_SESSION_DATE')
    out=np.empty((B,len(dates)))
    for b in range(B):
        starts=rng.integers(span,size=int(np.ceil(span/length)));draw=((starts[:,None]+np.arange(length))%span).ravel()[:span]
        out[b]=np.bincount(draw,minlength=span)[positions]
    return out


def design(frame,states,controls=(),fixed_assets=False):
    g=np.column_stack([(frame.state==state).to_numpy(float) for state in states]);x=frame.x.to_numpy(float)
    columns=['intercept:'+str(s) for s in states]+['slope:'+str(s) for s in states]
    blocks=[g,g*x[:,None]]
    for c in controls:blocks.append(frame[c].to_numpy(float)[:,None]);columns.append(c)
    if fixed_assets:
        for symbol in sorted(frame.symbol.unique())[1:]:blocks.append((frame.symbol==symbol).to_numpy(float)[:,None]);columns.append('asset:'+symbol)
    return np.column_stack(blocks),columns


def fit_daily(frame,states,controls=(),fixed_assets=False,B=500,seed=20261022,event=False,extra_contrasts=None):
    """OLS plus weighted per-day normal equations; all rows of a day stay together."""
    x,columns=design(frame,states,controls,fixed_assets);y=frame.y.to_numpy(float)
    if np.linalg.matrix_rank(x)!=x.shape[1]:raise ValueError('SINGULAR_STATE_DESIGN')
    beta=np.linalg.lstsq(x,y,rcond=None)[0];dates=np.sort(frame.date_et.unique());di=pd.Index(dates).get_indexer(frame.date_et)
    xx=np.zeros((len(dates),x.shape[1],x.shape[1]));xy=np.zeros((len(dates),x.shape[1]))
    np.add.at(xx,di,x[:,:,None]*x[:,None,:]);np.add.at(xy,di,x*y[:,None])
    W=block_weights(dates,5,B,seed,event);gram=np.einsum('bd,dij->bij',W,xx);rhs=W@xy
    ranks=np.linalg.matrix_rank(gram);valid=ranks==x.shape[1];draws=np.full((B,x.shape[1]),np.nan)
    draws[valid]=np.linalg.solve(gram[valid],rhs[valid,:,None])[:,:,0]
    n=len(states);slopes=beta[n:2*n];sd=draws[:,n:2*n]
    contrast=slopes[-1]-slopes[0];delta=sd[:,-1]-sd[:,0]
    error=y-x@beta
    result=dict(n_rows=len(frame),n_independent_days=len(dates),first=str(min(dates)),last=str(max(dates)),columns=columns,
        coefficients=beta.tolist(),state_slopes={str(s):float(slopes[i]) for i,s in enumerate(states)},
        slope_intervals={str(s):np.nanquantile(sd[:,i],[.025,.975]).tolist() for i,s in enumerate(states)},
        contrast=float(contrast),contrast_lo=float(np.nanquantile(delta,.025)),contrast_hi=float(np.nanquantile(delta,.975)),
        bootstrap_valid=int(valid.sum()),B=B,mean_squared_residual=float(np.mean(error**2)),residual_sd=float(np.std(error,ddof=x.shape[1])),
        residual_skew=float(pd.Series(error).skew()),residual_excess_kurtosis=float(pd.Series(error).kurt()),
        method='OLS; 5-session circular date-block percentile sensitivity, conditional exploratory; not confirmatory',
        controls=list(controls),asset_fixed_effects=fixed_assets)
    result['coefficient_intervals']={name:np.nanquantile(draws[:,i],[.025,.975]).tolist() for i,name in enumerate(columns)}
    result['extra_contrasts']={}
    for name,vector in (extra_contrasts or {}).items():
        vector=np.asarray(vector,float)
        if len(vector)!=len(beta):raise ValueError('REFERENCE_CONTRAST_DIMENSION')
        d=draws@vector;result['extra_contrasts'][name]=dict(estimate=float(beta@vector),lo=float(np.nanquantile(d,.025)),hi=float(np.nanquantile(d,.975)))
    return result,sd,W,dates


def fit_point(frame,states,controls=(),fixed_assets=False):
    x,_=design(frame,states,controls,fixed_assets)
    if len(frame)<=x.shape[1] or np.linalg.matrix_rank(x)<x.shape[1]:return np.nan
    b=np.linalg.lstsq(x,frame.y.to_numpy(float),rcond=None)[0];return float(b[2*len(states)-1]-b[len(states)])


def bin_curves(frame,states,cfg):
    """Reference-X-only common edges, raw means, joint date-block resampling and support masks."""
    reference=frame[frame.date_et<=cfg['reference_period_end']]
    if 'bin_end_utc' in reference:reference=reference.drop_duplicates(['date_et','bin_end_utc','state'])
    bounds=[reference.loc[reference.state==s,'x'].quantile([.05,.95]).to_numpy() for s in states]
    if any(not np.isfinite(b).all() for b in bounds):return pd.DataFrame(),dict(status='NO_COMMON_REFERENCE_SUPPORT')
    lower=max(b[0] for b in bounds);upper=min(b[1] for b in bounds)
    if upper<=lower:return pd.DataFrame(),dict(status='NO_COMMON_SUPPORT')
    edges=np.linspace(lower,upper,cfg['bins']+1);centers=(edges[:-1]+edges[1:])/2
    dates=np.sort(frame.date_et.unique());W=block_weights(dates,5,cfg['bootstrap']['replicates'],cfg['bootstrap']['seed']);di=pd.Index(dates).get_indexer(frame.date_et)
    bucket=np.searchsorted(edges,frame.x.to_numpy(),side='right')-1;rows=[]
    for s in states:
        for k,center in enumerate(centers):
            mask=(frame.state.to_numpy()==s)&(bucket==k);n=int(mask.sum());nd=len(set(frame.date_et[mask]))
            sums=np.bincount(di[mask],weights=frame.y.to_numpy()[mask],minlength=len(dates));counts=np.bincount(di[mask],minlength=len(dates));denom=W@counts
            values=np.divide(W@sums,denom,out=np.full(W.shape[0],np.nan),where=denom>0)
            valid=nd>=cfg['support']['min_bin_independent'];mean=float(frame.y[mask].mean()) if n else np.nan
            rows.append(dict(state=str(s),bin=k,x=center,x_lower=edges[k],x_upper=edges[k+1],y=mean,
                lo=np.nanquantile(values,.025) if n else np.nan,hi=np.nanquantile(values,.975) if n else np.nan,
                n_rows=n,n_independent_days=nd,supported=valid,rare_le5=nd<=5,bootstrap_valid=int(np.isfinite(values).sum())))
    return pd.DataFrame(rows),dict(status='SUPPORTED_GRID',edges=edges.tolist(),anchor_support=all(lower<=x<=upper for x in cfg['x_anchors']),
        excluded_x_rows=int(((frame.x<lower)|(frame.x>upper)).sum()),bin_mean_estimand='finite interval conditional means, x coordinate fixed midpoint; not raw singleton m')


def preflight(id):
    cfg,ch=load_config(id);manifest=RUN/'manifests/validated_inputs.json';inputs=json.loads(manifest.read_text())
    if inputs['source_registry_sha256']!=cfg['source_registry_sha256']:raise ValueError('SOURCE_REGISTRY_CHANGED')
    for ref in inputs['original_source_refs']:path_for(ref)
    for ref in inputs['derived'].values():path_for(ref)
    fingerprint=hashlib.sha256(json.dumps(inputs['derived'],sort_keys=True).encode()).hexdigest()
    print(id,'|',cfg['source_ids'],'|',cfg['target'],'|',cfg['state'],'|',cfg['independent_unit'],'|',cfg['coverage'],'|',ch,'|',fingerprint,flush=True)
    return cfg,ch,inputs,fingerprint


def terciles(values,reference_mask):
    finite=np.asarray(values)[reference_mask&np.isfinite(values)]
    if len(finite)<30:raise ValueError('INSUFFICIENT_REFERENCE_STATE')
    cuts=np.quantile(finite,[1/3,2/3]);return np.searchsorted(cuts,values,side='right'),cuts.tolist()


def load_frame(id,cfg,inputs):
    refs=inputs['derived'];extra={};controls=[];states=['low','middle','high']
    if id==IDS[0]:
        f=pd.read_parquet(path_for(refs['market_returns_5m']));assert set(f.symbol)=={'SPY',*STOCKS}
        if f.duplicated(['symbol','date_et','bin_end_utc']).any():raise ValueError('5M_DUPLICATE_KEY')
        market=f[f.symbol=='SPY'][['date_et','bin_end_utc','return_5m_log_bp','clock_state']].rename(columns={'return_5m_log_bp':'x','clock_state':'market_clock'})
        stocks=f[f.symbol!='SPY'].rename(columns={'return_5m_log_bp':'y','clock_state':'state'})
        f=stocks.merge(market,on=['date_et','bin_end_utc'],how='inner',validate='many_to_one');assert (f.state==f.market_clock).all();states=['early','mid','late']
        assert (f.bin_start_minute_ET>=600).all() and set(f.symbol)==set(STOCKS)
    elif id==IDS[1]:
        f=pd.read_parquet(path_for(refs['daily_rv_semivariance']));f=f.dropna(subset=['next_log_RV','log_RV','lag_log_RV']).copy()
        f['x']=f.log_RV;f['y']=f.next_log_RV;f['state']=pd.cut(f.q_down,bins=[-1e-12,1/3,2/3,1+1e-12],labels=states,right=False).astype(str);controls=['lag_log_RV']
        extra['definition']='389 within-session one-minute intervals; epsilon0; logRV positive only; no C RV390 reuse'
    elif id==IDS[2]:
        f=pd.read_parquet(path_for(refs['daily_spy_treasury_returns'])).dropna(subset=['yield_spread_pp']).copy();f['symbol']='IEF';f['x']=f.spy_oc_bp;f['y']=f.ief_oc_bp
        groups,cuts=terciles(f.yield_spread_pp.to_numpy(),(f.date_et<=cfg['reference_period_end']).to_numpy());f['state']=np.array(states)[groups];extra['state_cutpoints_pp']=cuts
        assert (f.available_at<f.session_open).all() and (f.rate_observation_date<f.date_et).all()
        extra['availability_qualification']='Next federal-business-day17:00ET conservative release assumption; current FRED vintage, no ALFRED historical revision reconstruction'
    elif id==IDS[3]:
        f=pd.read_parquet(path_for(refs['daily_stock_returns_volume']));f=f.dropna(subset=['stock_return_bp','stock_next_return_bp','relative_log_volume','spy_oc_bp']).copy()
        f['x']=f.stock_return_bp;f['y']=f.stock_next_return_bp;f['state']='';cuts={}
        for symbol,g in f.groupby('symbol'):
            labels,cut=terciles(g.relative_log_volume.to_numpy(),(g.date_et<=cfg['reference_period_end']).to_numpy());f.loc[g.index,'state']=np.array(states)[labels];cuts[symbol]=cut
        controls=['spy_oc_bp'];extra['per_stock_state_cutpoints']=cuts;assert (f.prior20_count==20).all();assert set(f.symbol)==set(STOCKS)
        extra['adjustment_qualification']='Massive split-only close-to-close price returns, not dividend-adjusted total returns; observed source volume'
    else:
        f=pd.read_parquet(path_for(refs['fomc_events']));extra['all_published_event_count']=len(f);extra['excluded_events']=f.loc[~f.eligible,['date_et','exclusion_reason']].to_dict('records')
        f=f[f.eligible & (abs(f.surprise_bp)>cfg['p05_zero_tolerance_bp'])].copy();f['x']=abs(f.surprise_bp);f['y']=f.event_return_bp;f['symbol']='SPY';f['state']=np.where(f.surprise_bp>0,'positive','negative');states=['negative','positive']
        extra['source_column']='FOMC (update 2023) / MPS, rate percentage points×100=bp; no MPS_ORTH; no futures return substituted for SPY'
    f['date_et']=f.date_et.astype(str)
    if not np.isfinite(f[['x','y']+controls].to_numpy(float)).all():raise ValueError('NONFINITE_REQUIRED_OBSERVATION')
    if (f.date_et<cfg['coverage'][0]).any() or (f.date_et>cfg['coverage'][1]).any():raise ValueError('EXPERIMENT_DATE_BOUNDARY')
    return f.reset_index(drop=True),states,controls,extra


def analyse(frame,states,controls,cfg,label):
    fixed=len(frame.symbol.unique())>1;result,draws,_,_=fit_daily(frame,states,controls,fixed,B=cfg['bootstrap']['replicates'],seed=cfg['bootstrap']['seed'],event=cfg['experiment_id']==IDS[4])
    result['label']=label;curves,support=bin_curves(frame,states,cfg);result['common_support']=support
    perstate=frame.groupby('state').agg(n_rows=('date_et','size'),n_independent_days=('date_et','nunique'),x_min=('x','min'),x_max=('x','max')).reset_index()
    result['state_support']=perstate.to_dict('records')
    date_extremes=frame.assign(extreme=abs(frame.x)).groupby('date_et').extreme.max();n=max(1,int(np.ceil(.01*len(date_extremes))));excluded=date_extremes.nlargest(n).index
    stress=frame[~frame.date_et.isin(excluded)];result['top1percent_dates_excluded']=list(excluded);result['contrast_without_top1percent']=fit_point(stress,states,controls,fixed)
    pivot=cfg['reference_period_end'];result['contrast_reference_period']=fit_point(frame[frame.date_et<=pivot],states,controls,fixed);result['contrast_later_period']=fit_point(frame[frame.date_et>pivot],states,controls,fixed)
    material=cfg['materiality'];supported=all(r['n_independent_days']>=cfg['support']['min_state_days'] for r in result['state_support'])
    supported=supported and len(result['state_support'])==len(states)
    common_bins=0 if curves.empty else int(curves.pivot(index='bin',columns='state',values='supported').all(axis=1).sum())
    result['jointly_supported_bins']=common_bins
    supported=supported and support['status']=='SUPPORTED_GRID' and common_bins>=3
    stable=all(np.isfinite(v) and np.sign(v)==np.sign(result['contrast']) for v in [result['contrast_without_top1percent'],result['contrast_reference_period'],result['contrast_later_period']])
    excludes_zero=result['contrast_lo']>0 or result['contrast_hi']<0
    if not supported:status='DATA HOLD'
    elif abs(result['contrast'])>=material and excludes_zero and stable:status='GO'
    elif max(abs(result['contrast_lo']),abs(result['contrast_hi']))<material:status='NO-GO'
    else:status='WEAK'
    result.update(status=status,temporal_and_top1_sign_stable=bool(stable),materiality_slope=material,curvature='NOT_TESTED; linear state slope changes suffice',
        support_status='ADEQUATE_OPERATIONAL_COUNTS' if supported else 'INSUFFICIENT_STATE_SUPPORT',uncertainty='EXPLORATORY_FIXED_DESIGN_BLOCK_SENSITIVITY; not untouched confirmation')
    return result,curves,draws


def screen():
    plan=RUN/'configs/analysis_completion_before_screen.json'
    if not plan.exists():write_json(plan,dict(at=now(),P01='Report per-stock early/mid/late betas and early-minus-late cross-stock SD with common shared date resamples; primary generic contrast late-minus-early mean slope retained',
        P02='SPY principal and pooled stocks separately; logRVnext on current logRV/state interactions plus strict laglogRV; rawRVnext on positive/negative semivariances reference',
        P03='IEF/SPY open-close price return same-day response; reference cutpoints frozen by period',P04='Pooled stock fixed effects, state slopes, SPY O-C control; own stock-volume state',
        P05='Require15events/sign for shape; otherwise DATA HOLD count graphic, no economic curve. Raw published MPS rate-pp converted100to bp, independently documented by Bauer-Swanson p16',
        inference='B500 joint5-session calendar blocks; no marginal p-values promoted to confirmation'),exclusive=True)
    for id in IDS:
        cfg,ch,inputs,fingerprint=preflight(id);dest=RUN/'experiments'/id
        for sub in ['results','plots','diagnostics']:(dest/sub).mkdir(parents=True,exist_ok=True)
        completion=dest/'results/completion.json'
        if completion.exists():
            old=json.loads(completion.read_text())
            if old['config_sha256']!=ch or old['input_fingerprint']!=fingerprint:raise ValueError('STALE_EXPERIMENT_CHECKPOINT')
            print('SKIP_VERIFIED_EXPERIMENT',id,flush=True);continue
        common=dict(experiment_id=id,config_sha256=ch,source_manifest_sha256=sha(RUN/'manifests/validated_inputs.json'),input_fingerprint=fingerprint,target=cfg['target'],predictor=cfg['predictor'],state=cfg['state'],independent_unit=cfg['independent_unit'],time_range=cfg['coverage'])
        try:
            f,states,controls,extra=load_frame(id,cfg,inputs)
            if id==IDS[4]:
                counts=f.groupby('state').date_et.nunique().to_dict();n=len(f)
                if any(counts.get(s,0)<cfg['support']['min_events_per_sign'] for s in states):
                    result=dict(status='DATA HOLD',n_independent_days=n,n_rows=n,state_counts=counts,reason='Insufficient independent negative/positive events for frozen sign/magnitude shape support; no curves fitted',**extra)
                    pd.DataFrame([dict(state=s,n_events=counts.get(s,0)) for s in states]).to_csv(dest/'results/event_support.csv',index=False)
                    # Signed benchmark and exact event LOO are explicitly descriptive, not the held shape.
                    x=np.c_[np.ones(len(f)),f.surprise_bp];b=np.linalg.lstsq(x,f.y,rcond=None)[0]
                    loo=[]
                    for i in range(len(f)):
                        mask=np.arange(len(f))!=i;coef=np.linalg.lstsq(x[mask],f.y.to_numpy()[mask],rcond=None)[0]
                        loo.append(dict(event_id=f.event_id.iloc[i],date_et=f.date_et.iloc[i],signed_slope_without_event=coef[1]))
                    pd.DataFrame(loo).to_csv(dest/'diagnostics/signed_benchmark_leave_one_event_out.csv',index=False)
                    result['signed_linear_benchmark_bp_per_bp']=float(b[1]);write_json(dest/'results/summary.json',dict(**common,**result));write_json(completion,common);continue
            primary=f[f.symbol=='SPY'].copy() if id==IDS[1] else f
            result,curves,draws=analyse(primary,states,controls,cfg,'SPY' if id==IDS[1] else 'POOLED')
            result.update(extra);subresults=[]
            if id==IDS[0]:
                slopes=[];all_draws=[]
                for symbol,g in f.groupby('symbol',sort=True):
                    rr,dd,_,_=fit_daily(g,states,(),False,B=cfg['bootstrap']['replicates'],seed=cfg['bootstrap']['seed'])
                    slopes.extend([dict(symbol=symbol,state=s,beta=rr['state_slopes'][s],lo=rr['slope_intervals'][s][0],hi=rr['slope_intervals'][s][1],n_independent_days=rr['n_independent_days']) for s in states]);all_draws.append(dd);subresults.append(dict(symbol=symbol,**rr))
                slopes=pd.DataFrame(slopes);slopes.to_csv(dest/'results/stock_state_betas.csv',index=False)
                # Identical weights require the same scheduled span, even when stock eligibility differs.
                common_dates=set(f.date_et)
                for _,g in f.groupby('symbol'):common_dates&=set(g.date_et)
                result['balanced_panel_days']=len(common_dates)
                # Cross-stock dispersion sampling evaluated on the balanced panel only.
                if len(common_dates)>=30:
                    balanced=[];point=[]
                    for symbol,g in f[f.date_et.isin(common_dates)].groupby('symbol',sort=True):
                        rr,dd,_,_=fit_daily(g,states,(),False,B=cfg['bootstrap']['replicates'],seed=cfg['bootstrap']['seed']);balanced.append(dd);point.append([rr['state_slopes'][s] for s in states])
                    arr=np.array(balanced);disp=arr[:,:,0].std(axis=0,ddof=1)-arr[:,:,2].std(axis=0,ddof=1);point=np.array(point)
                    result['early_minus_late_beta_dispersion']=float(point[:,0].std(ddof=1)-point[:,2].std(ddof=1));result['dispersion_block_interval']=np.nanquantile(disp,[.025,.975]).tolist()
                    pd.DataFrame(dict(draw=np.arange(len(disp)),early_minus_late_SD=disp)).to_csv(dest/'results/beta_dispersion_draws.csv',index=False)
            if id==IDS[1]:
                stocks=f[f.symbol!='SPY']
                if len(stocks):
                    rr,cc,dd=analyse(stocks,states,controls,cfg,'STOCKS_POOLED');subresults.append(rr);cc.to_csv(dest/'results/stocks_conditional_curves.csv',index=False)
                scale=float(primary.RV.mean());reference=primary.copy()
                reference['x']=reference.RS_minus/scale;reference['y']=reference.next_session_RV/scale
                reference['RS_plus_scaled']=reference.RS_plus/scale;reference['lag_RV_scaled']=reference.lag_RV/scale;reference['state']='total'
                sr,_,_,_=fit_daily(reference,['total'],['RS_plus_scaled','lag_RV_scaled'],False,B=cfg['bootstrap']['replicates'],seed=cfg['bootstrap']['seed'],extra_contrasts={'negative_minus_positive':[0,1,-1,0]})
                b=sr['coefficients']
                result['raw_semivariance_reference']=dict(intercept_scaled=float(b[0]),negative_coefficient=float(b[1]),positive_coefficient=float(b[2]),negative_minus_positive=float(b[1]-b[2]),lag_RV_coefficient=float(b[3]),scale_RV=scale,
                    coefficient_intervals=sr['coefficient_intervals'],contrast_interval=sr['extra_contrasts']['negative_minus_positive'],definition='nextRV/scale ~1+RSminus/scale+RSplus/scale+lagRV/scale; same date-block sensitivity')
                xb=np.c_[np.ones(len(primary)),primary.x,primary.lag_log_RV];bb=np.linalg.lstsq(xb,primary.y,rcond=None)[0];result['lag_controlled_no_state_baseline']=dict(columns=['intercept','current_log_RV','lag_log_RV'],coefficients=bb.tolist(),MSE=float(np.mean((primary.y-xb@bb)**2)))
            curves.to_csv(dest/'results/conditional_curves.csv',index=False);write_json(dest/'diagnostics/subgroup_models.json',subresults)
            write_json(dest/'results/summary.json',dict(**common,**result));write_json(dest/'diagnostics/screen_design.json',dict(states=states,controls=controls,source_rows=len(f),first=str(f.date_et.min()),last=str(f.date_et.max()),state_counts=f.groupby('state').date_et.nunique().to_dict()))
            write_json(completion,common)
        except (KeyError,ValueError,FileNotFoundError) as e:
            write_json(dest/'results/summary.json',dict(**common,status='DATA HOLD',n_independent_days=0,n_rows=0,reason=type(e).__name__+': '+str(e)[:350]))
            write_json(completion,common)
        print('SCREEN',id,json.loads((dest/'results/summary.json').read_text())['status'],flush=True)
