"""Bounded offline Stage2C theorem/diagnostic audit. No fitting or sealed analytics."""
import ast
import datetime as dt
import importlib.metadata as metadata
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
from unittest.mock import patch

import joblib
import numpy as np
import pandas as pd
from scipy.stats import norm
from interpret.glassbox import ExplainableBoostingRegressor
from statsmodels.regression.linear_model import OLS

from .pilot import ROOT,sha,write_json
from .stage2b import data_root,read_development
from .ebm_models import features,query_frame,assert_graph
from .stage2c_theory import annotations

PACKET=ROOT/'docs/specs/experiment_B_stage2C_supplied_theorem_extracts_v1.md'
SNAPSHOT=ROOT/'data/registry/B_stage2C_start_snapshot.json'
PREFIX='B_stage2C_'


class SubstantiveError(RuntimeError):
    """A frozen input/result contradiction; never authorize a model rerun here."""


def require(condition,message):
    """Fail the minimal affected audit branch with an explicit authorization boundary."""
    if not condition:raise SubstantiveError('SUBSTANTIVE_ERROR_REQUIRES_SEPARATE_AUTHORIZATION: '+message)


def source_statements():
    """Parse the 22 supplied source blocks verbatim, including original attribution/status."""
    text=PACKET.read_text();lines=text.splitlines()
    pattern=r'^Source: (T[0-9A-Z]+\.[A-Z][0-9]+) — (.+), original line (\d+)$'
    starts=[(i,re.match(pattern,line)) for i,line in enumerate(lines) if re.match(pattern,line)]
    result={}
    for k,(i,match) in enumerate(starts):
        end=starts[k+1][0] if k+1<len(starts) else len(lines)
        block='\n'.join(lines[i:end]);identity,filename,original=match.groups()
        status=next(line.removeprefix('Status: ') for line in lines[i:end] if line.startswith('Status: '))
        import hashlib
        result[identity]=dict(theorem_id=identity,original_filename=filename,source_line_or_section=int(original),
                              source_status=status,packet_line_start=i+1,packet_line_end=end,
                              excerpt_sha256=hashlib.sha256(block.encode()).hexdigest(),title=lines[i+1])
    require(set(result)==set(annotations()),'supplied theorem IDs differ from editorial annotations')
    return result


def crosswalk(statements):
    """Exact source labels plus explicit, noncertifying source/implementation distinctions."""
    rows=[]
    for identity,a in annotations().items():
        s=statements[identity]
        rows.append(dict(s,implementation_id=identity+'_source_applicability',source_kind='SUPPLIED_STATEMENT',
                         theorem_exact_target=a['target'],theorem_observation_law=a['law'],
                         theorem_assumption_list=json.dumps([v[0] for v in a['premises']]),
                         required_known_information=a['known'],selection_and_conditioning=a['selection'],
                         learner_or_dictionary=a['learner'],finite_sample_or_asymptotic=a['time'],
                         software_computation_and_path=a['computation'],
                         actual_SPY_evidence_for_each_assumption=json.dumps(dict(a['premises'])),
                         mismatch_or_missing_evidence='; '.join(v[1] for v in a['premises'])+'; Original setting/proof text outside supplied excerpt and A.0 was not independently inspected.',
                         classification=a['classification'],valid_claim=a['valid'],forbidden_claim=a['forbidden'],
                         remedy_or_future_condition=a['remedy'],impact_on_A1_A2_closeout='Qualified inconclusive developmental closeout; no theorem-certified raw shape or independent final-test claim'))
    methods=[
        ('fixed_loss_HAC','T22.E1','CONDITIONAL_STANDARD_INFERENCE',
         'Matched mean comparator squared loss minus candidate squared loss; Bartlett5/10/20 normal intervals, n/(n-1)',
         'B_stage2B_ebm_paired_loss_tests.csv; independent direct-meat verification in Stage2C',
         'Weak-dependence/FCLT, appropriate loss moments and bandwidth; evolving forecasts and development reuse require more than fixed-vector treatment',
         'Gains/interval arithmetic reproduces; assumptions not empirically certified. Stage2B DIRECTLY_VALID is superseded by this qualified classification.',
         'Numerical development loss evidence under stated unverified standard assumptions',
         'Exact T22.E1 coverage, selection adjustment or independent held-out confirmation'),
        ('fixed_loss_block_bootstrap','T22.E1','CONDITIONAL_STANDARD_INFERENCE',
         'Fixed-loss circular moving-block percentile summaries, blocks5/20,B500; not full learner bootstrap',
         'B_stage2B_ebm_paired_loss_tests.csv existing rows only; no bootstrap rerun',
         'Stationarity/weak dependence, moments, block adequacy and nonstationarity control; selection process not rerun',
         'Existing bounds retained as sensitivity; no exact independence/stationarity proof',
         'Conditional descriptive/asymptotic loss robustness summary',
         '500fixed-loss draws are500full-pipeline nulls or population shape bands'),
        ('local_support_screen','T10B.B1','ADAPTED_DESCRIPTIVE',
         'Predetermined local X/RV-tercile/W counts and distinct nonoverlapping five-row blocks',
         'B_stage2B_ebm_support.csv; contrast_grid.json; Stage2C independent E/L candidate recount',
         '50dates/20blocks or100/30 are pragmatic safeguards; population pointwise regularity/positive-mass conditions are not inferred',
         'Efirst qualifying candidate±20,h15; Lnone; raw pointwise Euncertified; validation lowstate31',
         'Research support/abstention rule, not a numerical theorem confidence constant',
         'Distinct five-row groups are independent clusters or observed support implies population identification'),
        ('whole_prediction_D','T22.G2','ALGEBRAIC_IDENTITY_ONLY',
         'D_F=F(x+,zH,w)-F(x-,zH,w)-F(x+,zL,w)+F(x-,zL,w); additive controls cancel',
         '11savedFULLseed42models .predict on four frozen query rows; no model.fit',
         'Only deterministic arithmetic and correct feature/partner order are required for the computed identity',
         'A1c_E .52624bp; SB/A0≈0; numerical identity is NOT an instantiation of G2 probability event',
         'Fitted total-model nonadditivity at specified coordinates',
         'D_F equals D_m, proves material curvature, or has a population CI'),
        ('observed_MSE_composition','T24.E1','ALGEBRAIC_IDENTITY_ONLY',
         'Observed MSE difference=(p_val-p_train)·L_train+p_val·(L_val-L_train)',
         'B_stage2B_ebm_state_composition.csv; recounted from saved fixedFULL42train/validation predictions',
         'Finite observed means and same three state definitions; no sampling/causal premise for this arithmetic',
         'Exact deterministic observed error identity, NOT T24.E1 conditional shape/level/kernel identity',
         'Separate observed error-mixture contribution from within-state error difference, including training optimism',
         'Transport proof, conditional-law invariance or causal drift decomposition'),
        ('empirical_band_fidelity','T24.I1','ADAPTED_DESCRIPTIVE',
         'Four local-X by broad-RV-tercile Y means versus predicted means on identical observed row distributions',
         'B_stage2B_ebm_empirical_bands.csv and empirical_cells.csv',
         'Adequate local support; independent raw calibration/localization/dependence conditions for stronger inference are missing',
         'TrainingEbands exploratory; validation/Lfail; broad bands differ from continuous medianZpointquery',
         'Finite-panel band/model fidelity diagnostic with explicit estimand mismatch',
         'Raw medians/pointwise D_m estimated with certified localization bias or independent validation confirmation'),
        ('native_path_and_bins','T16.I2','ADAPTED_DESCRIPTIVE',
         'Actual feature/term graph, native bins, score tensor occupancy, bags/iterations and seed/refit stability',
         'B_stage2B_ebm_models.csv;11selectednativeartifacts; software_components/term_importance/stability tables',
         'Package graph metadata can be checked; idealized dictionary/frame/gap hypotheses are not established',
         'InterpretML0.7.3 actual nominal S and fixed interactions; cyclic bags/early stopping differ from idealized12trees',
         'Software fidelity and algorithmic sensitivity, not optimizer or future-path certificate',
         'Iteration counts or native bagSD certify global optimizer distance or raw scientific coverage'),
        ('within_tercile_dispersion','T25.I1','ADAPTED_DESCRIPTIVE',
         'Observed within-tercile Z spread and different native-model prediction RMS on common rows',
         'B_stage2B_ebm_discretization.csv; fixedstatecutoffs shared across all fits',
         'Finite-panel summaries are computable; known moments, supplied affine class and independent pilot not instantiated',
         'Prediction spread also includes X/W variation and distinct fitted-model errors',
         'Descriptive compression/representation comparison, not pure conditional information loss',
         'Certified affine moment inversion, retained-space closure, or oracle V_Z estimate'),
        ('declared_materiality','T25.F1','BLOCKED_ASSUMPTIONS',
         'Affirmative±1bpshape equivalence and predictive gain lower bound above a meaningful threshold',
         'Stage2BshapeNOT_CERTIFIED and decisionsNO_CREDIBLE_INCREMENT;1bp/.0025R2thresholds retained',
         'Justified joint raw intervals for shapes; T22.E1meaningful gain needs LCB>delta, not only point>=delta and LCB>0',
         'Stage2Boperational materiality flag is a weaker screen; no primary affirmative conclusion passed, so no numerical/primary decision invalidated',
         'Inconclusive/rawABSTAIN and qualified negative predictive finding',
         'Small fitted D or a point-threshold flag is theorem-certified equivalence/material benefit'),
        ('development_null','T22.E1','NOT_EXECUTED/DEFERRED',
         '100full-selection/refit null replications; distinct destroyed-alignment versus conditional-interaction null',
         'No null results; Stage2B8400fit cost estimate retained without launch',
         'A separately frozen null invariance/dependence and full discovery design would be required',
         '0newnullreplicates; no p-value; not required to close developmental pipeline in Stage2C',
         'Explicit deferred/unperformed status',
         'Saved-forecast shuffle or fixed-loss bootstrap is a full-discovery permutation'),
        ('action_economics','T22.E1','NOT_EXECUTED/DEFERRED',
         'Executable action/payoff comparison with costs and information/fill timing',
         'No action/PnL/transaction-cost calculation in Stage2C or claimed Stage2B results',
         'Specified action map, actual evaluation law, costs/fills and matched independent comparison',
         'Signed scientific Ypredictor is not an executed strategy or complete payoff distribution',
         'Economic value untested; no future trading evaluation automatically authorized',
         'Alpha/profit/no-trade-cost conclusion or pure Wdecision value from Lmodel'),
    ]
    for name,identity,classification,target,path,premise,evidence,valid,forbidden in methods:
        source=statements[identity]
        rows.append(dict(source,implementation_id=name,source_kind='IMPLEMENTATION_METHOD',
                         theorem_exact_target=annotations()[identity]['target'],implementation_target=target,
                         theorem_observation_law=annotations()[identity]['law'],theorem_assumption_list=json.dumps([premise]),
                         required_known_information=annotations()[identity]['known'],selection_and_conditioning=annotations()[identity]['selection'],
                         learner_or_dictionary=annotations()[identity]['learner'],finite_sample_or_asymptotic=annotations()[identity]['time'],
                         software_computation_and_path=path,actual_SPY_evidence_for_each_assumption=json.dumps({premise:evidence}),
                         mismatch_or_missing_evidence=evidence,classification=classification,valid_claim=valid,forbidden_claim=forbidden,
                         remedy_or_future_condition='No additional work needed to close development; stronger future inference needs explicitly matched premises and separate authorization.',
                         impact_on_A1_A2_closeout='CLOSED_INCONCLUSIVE_DEVELOPMENT; no claim of theorem instantiation from this implementation row'))
    return rows


def audit(root,protocol):
    """Three numerical/source groups plus an enforced no-fit/no-seal group; predictions only."""
    started=time.perf_counter();cpu=time.process_time();read_files=[]
    def read_json(path):read_files.append(path);return json.loads(path.read_text())
    def csv(name,columns=None):
        path=root/'registry'/name;read_files.append(path);return pd.read_csv(path,usecols=columns,low_memory=False)
    previous=read_json(root/'registry/B_stage2B_ebm_manifest.json')
    for ref in previous['products']:
        path=root/ref['path'];require(path.exists() and sha(path)==ref['sha256'],f'Stage2Bproduct changed/missing: {path.name}')
    for ref in previous['code']+previous['models']+previous['figures']+previous['reports']:
        path=ROOT/ref['path'];require(path.exists() and sha(path)==ref['sha256'],f'Stage2Bcode/model/report/figure changed: {path.name}')
    require(sha(root/protocol['daily']['path'])==protocol['daily']['sha256'],'daily hash mismatch')
    path=root/protocol['daily']['path'];read_files.append(path)
    columns=['session_et','eligible_primary','x_open_bp','w_preclose_bp','y_last30_bp','rv_open_raw','rv_open_log']
    train=read_development(path,*protocol['train'],columns=columns)
    val=read_development(path,*protocol['validation'],columns=columns)
    dates=pd.read_parquet(path,columns=['session_et','eligible_primary'])
    counts={name:int((dates.eligible_primary & dates.session_et.astype(str).between(*bounds)).sum()) for name,bounds in [('train',protocol['train']),('validation',protocol['validation']),('sealed',protocol['sealed'])]}
    require(counts==dict(train=1495,validation=497,sealed=683),'date-only seal/count mismatch')
    predpath=root/previous['predictions']['path'];read_files.append(predpath);pred=pd.read_parquet(predpath)
    pred.session_et=pred.session_et.astype(str)
    require(not pred.duplicated(['model_id','setting','seed','variant','mode','cohort','session_et']).any(),'duplicate forecast identity')
    require(pred.session_et.lt('2024-01-01').all(),'forbidden sealed forecast row')
    source=pd.concat([train,val]).assign(session_et=lambda x:x.session_et.astype(str)).set_index('session_et')
    require(np.array_equal(pred.actual.to_numpy(),source.loc[pred.session_et,'y_last30_bp'].to_numpy()),'forecast actualY mismatch')
    require(np.allclose(pred.loss,(pred.actual-pred.forecast)**2,atol=1e-10,rtol=1e-14),'saved loss algebra mismatch')
    v=pred.loc[pred.cohort.eq('validation')];series=0
    for key,g in v.groupby(['model_id','setting','seed','variant','mode']):
        require(sorted(g.session_et)==val.session_et.astype(str).tolist(),f'matched-date failure: {key}');series+=1
    require((v.history_last<v.session_et).all() and (v.history_last<v['asof']).all(),'forecast chronology')
    models=csv('B_stage2B_ebm_models.csv')
    require(len(models)==562 and models.status.eq('PASS').all(),'fit-completion inventory mismatch')
    require(set(models.seed)==set(protocol['seeds']),'seed pool mismatch')
    for _,r in models.iterrows():
        spec=next(s for s in protocol['models'] if s['model_id']==r.model_id);pars=json.loads(r.effective_parameters);terms=json.loads(r.term_features)
        require(pars['feature_names']==spec['features'],'model feature mismatch')
        require({tuple(t) for t in terms if len(t)>1}=={tuple(spec['features'].index(c) for c in e) for e in spec['edges']},f'graph mismatch {r.fit_id}')
        if r['mode']=='quarterly':require(int(r.n)==int((source.index<r['asof']).sum()),f'quarterly history count {r.fit_id}')
    paired=csv('B_stage2B_ebm_paired_loss_tests.csv');multiplicity=csv('B_stage2B_ebm_interaction_and_multiplicity.csv')
    baselinepath=root/protocol['stage2A_predictions']['path'];read_files.append(baselinepath);baseline=pd.read_parquet(baselinepath);baseline.session_et=baseline.session_et.astype(str)
    score=[];comparisons=[]
    for mid,q in v.loc[v.variant.eq('FULL')&v.seed.eq(42)&v['mode'].eq('quarterly')].groupby('model_id'):
        score.append(dict(model_id=mid,n=len(q),MSE=float(q.loss.mean()),RMSE=float(np.sqrt(q.loss.mean()))))
    for info in ['E','L']:
        candidate=v.loc[v.model_id.eq('A1c_'+info)&v.variant.eq('FULL')&v.seed.eq(42)&v['mode'].eq('quarterly')].sort_values('session_et')
        for comp in ['A0c_'+info,'SB_'+info,'C1_'+info,'C2_'+info,'S4_'+info,'N0','N1','OLS1_E' if info=='E' else 'OLS3_L']:
            other=v.loc[v.model_id.eq(comp)&v.variant.eq('FULL')&v.seed.eq(42)&v['mode'].eq('quarterly')]
            if other.empty:other=baseline.loc[baseline.model_id.eq(comp)&baseline.variant.eq('FULL')&baseline['mode'].eq('quarterly')]
            other=other.set_index('session_et').loc[candidate.session_et]
            require(np.array_equal(candidate.actual,other.actual),'paired Y mismatch')
            diff=(other.actual-other.forecast).to_numpy()**2-(candidate.actual-candidate.forecast).to_numpy()**2
            saved=paired.loc[paired.candidate.eq('A1c_'+info)&paired.comparator.eq(comp)&paired['mode'].eq('quarterly')&paired.method.eq('Bartlett_HAC5_normal')].iloc[0]
            require(abs(diff.mean()-saved.mean_loss_gain)<1e-9,'paired mean-loss sign/arithmetic discrepancy')
            for lag in ([5,10,20] if comp=='A0c_'+info else [5]):
                n=len(diff);u=diff-diff.mean();meat=np.dot(u,u)+sum(2*(1-k/(lag+1))*np.dot(u[k:],u[:-k]) for k in range(1,lag+1));se=np.sqrt(meat/n**2*n/(n-1));z=norm.ppf(.975)
                s=paired.loc[paired.candidate.eq('A1c_'+info)&paired.comparator.eq(comp)&paired['mode'].eq('quarterly')&paired.method.eq(f'Bartlett_HAC{lag}_normal')].iloc[0]
                require(abs(se-s.se)<1e-9 and abs(diff.mean()-z*se-s.ci_low)<1e-9,'paired HAC numerical discrepancy')
                record=dict(info=info,candidate='A1c_'+info,comparator=comp,n=n,lag=lag,gain=float(diff.mean()),se=float(se),ci_low=float(diff.mean()-z*se),ci_high=float(diff.mean()+z*se))
                if comp=='A0c_'+info and lag==5:record['p_holm']=float(multiplicity.loc[multiplicity.primary.eq(True)&multiplicity.candidate.eq('A1c_'+info),'p_holm'].iloc[0])
                comparisons.append(record)
    support=csv('B_stage2B_ebm_support.csv');shapes=csv('B_stage2B_ebm_shape_contrasts.csv');g=np.searchsorted(protocol['cutoffs_raw'],train.rv_open_raw,side='left');blocks=np.arange(len(train))//5;cells=[]
    for info in ['E','L']:
        for c in protocol['contrast_grid'][info]['candidates']:
            cell_ok=[]
            for state in [0,2]:
                for x in [-c['a'],c['a']]:
                    mask=(g==state)&(abs(train.x_open_bp.to_numpy()-x)<=c['h'])
                    if info=='L':mask &= abs(train.w_preclose_bp.to_numpy()-c['w'])<=c['w_halfwidth']
                    n=int(mask.sum());b=int(np.unique(blocks[mask]).size);cell_ok.append(n>=50 and b>=20)
                    r=support.loc[support.candidate_id.eq(c['candidate_id'])&support.state.eq(['low','middle','high'][state])&support.endpoint.eq(x)].iloc[0]
                    require(n==r.n and b==r.blocks,'support neighborhood/block discrepancy')
                    if c['candidate_id']==protocol['contrast_grid'][info]['display_candidate']['candidate_id']:
                        sub=train.loc[mask];cells.append(dict(info=info,candidate=c['candidate_id'],x=x,h=c['h'],w=c['w'],w_halfwidth=c['w_halfwidth'],state=['low','middle','high'][state],n=n,blocks=b,year_counts=sub.session_et.astype(str).str[:4].value_counts().to_dict(),z_min=float(sub.rv_open_log.min()),z_max=float(sub.rv_open_log.max())))
            require(all(cell_ok)==c['supported'],'candidate acceptance discrepancy')
    require(protocol['contrast_grid']['E']['chosen']['a']==20 and protocol['contrast_grid']['L']['chosen'] is None,'frozen first-qualifying E/L design changed')
    model_checks=[];four=[]
    for spec in protocol['models']:
        mid=spec['model_id'];path=ROOT/f'artifacts/B/checkpoints/stage2B/{mid}.joblib';read_files.append(path);model=joblib.load(path);assert_graph(model,spec)
        c=protocol['contrast_grid'][spec['info']]['display_candidate'];lo,_,hi=protocol['z_representatives']
        query=query_frame([-c['a'],c['a'],-c['a'],c['a']],[lo,lo,hi,hi],c['w']);pr=model.predict(features(query,spec,protocol));D=float(pr[3]-pr[2]-pr[1]+pr[0])
        saved=shapes.loc[shapes.model_id.eq(mid)&shapes.variant.eq('FULL')&shapes['mode'].eq('fixed')&shapes.seed.eq(42)].iloc[0]
        require(abs(D-saved.D_F)<1e-10,f'four-total-prediction mismatch {mid}')
        if not spec['edges']:require(abs(D)<1e-9,f'additive control failed {mid}')
        four.append(dict(model_id=mid,info=spec['info'],x_minus=-c['a'],x_plus=c['a'],w=c['w'],z_low=lo,z_high=hi,predictions_order='low_minus,low_plus,high_minus,high_plus',four_predictions_bp=pr.tolist(),D_F=D,raw_interval_status='NOT_CERTIFIED' if spec['info']=='E' else 'ABSTAIN'))
        q=v.loc[v.model_id.eq(mid)&v.variant.eq('FULL')&v.seed.eq(42)&v['mode'].eq('fixed')].sort_values('session_et').head(8)
        actual=model.predict(features(val.head(8),spec,protocol));require(np.max(abs(actual-q.forecast.to_numpy()))<1e-12,'read-only native prediction spot-check')
        for j,name in enumerate(model.feature_names_in_):
            bins=model.bins_[j];main=bins[0];levels=[]
            for level in bins:
                interior=len(set(level.values())) if isinstance(level,dict) else len(level)+1
                levels.append(dict(interior_bins=interior,total_bins_including_missing_unseen=interior+2,
                                   cuts_or_categories=level if isinstance(level,dict) else np.asarray(level).tolist()))
            main_term=next(k for k,t in enumerate(model.term_features_) if tuple(t)==(j,))
            main_weights=model.bin_weights_[main_term]
            model_checks.append(dict(model_id=mid,feature=name,type=model.feature_types_in_[j],levels=levels,
                                     missing_index=0,unseen_index='last',term_shapes=[list(t.shape) for t in model.term_scores_],
                                     main_bin_weights=main_weights.tolist(),main_missing_count=float(main_weights[0]),
                                     main_unseen_count=float(main_weights[-1]),
                                     lowest_highest_interior_counts=[float(main_weights[1]),float(main_weights[-2])],
                                     term_occupied_counts=[int((w>0).sum()) for w in model.bin_weights_],term_sparse_occupied_lt20=[int(((w>0)&(w<20)).sum()) for w in model.bin_weights_]))
    composition=csv('B_stage2B_ebm_state_composition.csv');state_counts={}
    for name,f in [('train',train),('validation',val)]:
        gg=np.searchsorted(protocol['cutoffs_raw'],f.rv_open_raw,side='left');state_counts[name]=np.bincount(gg,minlength=3).tolist()
    for info in ['E','L']:
        mid='A1c_'+info;q=pred.loc[pred.model_id.eq(mid)&pred.seed.eq(42)&pred.variant.eq('FULL')&pred['mode'].eq('fixed')]
        pt=np.asarray(state_counts['train'])/len(train);pv=np.asarray(state_counts['validation'])/len(val)
        lt=np.array([q.loc[q.cohort.eq('train')&q.state.eq(s),'loss'].mean() for s in ['low','middle','high']]);lv=np.array([q.loc[q.cohort.eq('validation')&q.state.eq(s),'loss'].mean() for s in ['low','middle','high']])
        r=composition.loc[composition.model_id.eq(mid)&composition.cohort.eq('train_to_validation_MSE_decomposition')].iloc[0]
        require(abs((pv-pt)@lt-r.composition_term)<1e-9 and abs(pv@(lv-lt)-r.within_state_term)<1e-9,'observed MSE identity discrepancy')
    # Register consequential existing tables read for the assumption audit, without recalculating their statistics.
    review={}
    for name in ['empirical_bands','empirical_cells','discretization','stability','term_importance','theory_method_ledger','decisions','continuous_grid','surfaces']:
        f=csv('B_stage2B_ebm_'+name+'.csv');review[name]=dict(rows=len(f),columns=list(f.columns))
    d=csv('B_stage2B_ebm_diagnostics.csv',columns=['model_id','seed','variant','mode','cohort','statistic','estimate','p_value'])
    d=d.loc[d.seed.eq(42)&d.variant.eq('FULL')&d['mode'].eq('fixed')&d.cohort.eq('train')&d.model_id.isin(['A1c_E','A1c_L'])&d.statistic.isin(['Pearson_kurtosis','residual_ACF_1','squared_residual_LjungBox_5','ARCH_LM5'])]
    return dict(checks=dict(source_attribution='PASS',model_forecast_and_loss='PASS',support_and_whole_prediction='PASS',no_fit_and_seal='PASS'),
                count_metadata=counts,fit_records=562,families=11,seeds=protocol['seeds'],matched_validation_series=series,
                scorecard=score,paired_checks=comparisons,state_counts=state_counts,support_cells=cells,
                four_point_checks=four,native_structures=model_checks,reviewed_tables=review,
                residual_evidence=d.astype(object).where(pd.notna(d),None).to_dict('records'),
                new_fit_calls=0,new_permutations=0,sealed_scientific_rows_exposed=0,sealed_metadata_only=True,
                read_files=sorted(set(str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else 'EBM_DATA_ROOT/'+str(p.relative_to(root)) for p in read_files)),
                wall_seconds=time.perf_counter()-started,cpu_seconds=time.process_time()-cpu)


def no_fit(*args,**kwargs):
    """Hard stop if a supposedly read-only audit attempts native or OLS fitting."""
    raise RuntimeError('Stage2C forbids fitting; investigate before any separate authorization')


def run():
    """Audit immutable inputs and supplied text; create only separate Stage2C products."""
    start=time.perf_counter();cpu=time.process_time();root=data_root();snapshot=json.loads(SNAPSHOT.read_text())
    protocol=json.loads((ROOT/'config/B_stage2B_EBM_protocol_v1.json').read_text());statements=source_statements()
    with patch.object(ExplainableBoostingRegressor,'fit',side_effect=no_fit),patch.object(OLS,'fit',side_effect=no_fit):
        evidence=audit(root,protocol)
    rows=crosswalk(statements);out=root/'registry/B_stage2C_theorem_diagnostic_crosswalk.csv';pd.DataFrame(rows).to_csv(out,index=False)
    write_json(root/'registry/B_stage2C_readonly_verification.json',evidence)
    from .stage2c_report import write_reports,make_overlay
    figs=make_overlay(root,protocol)
    reports=write_reports(root,protocol,rows,evidence)
    for ref in snapshot['files']:
        require(sha(ROOT/ref['path'])==ref['sha256'],f'preexisting artifact changed: {ref["path"]}')
    outputs=[out,root/'registry/B_stage2C_readonly_verification.json',*figs,*reports]
    def ref(f):return dict(path=str(f.relative_to(ROOT)) if f.is_relative_to(ROOT) else 'EBM_DATA_ROOT/'+str(f.relative_to(root)),bytes=f.stat().st_size,sha256=sha(f))
    manifest=dict(stage='B_STAGE2C_THEOREM_AUDIT_CLOSEOUT_V1',implementation_QA='PASS WITH QUALIFICATIONS',
                  A1_closeout='CLOSED_INCONCLUSIVE_DEVELOPMENT',A2_closeout='CLOSED_INCONCLUSIVE_DEVELOPMENT',
                  theorem_statements=len(statements),ledger_rows=len(rows),classification_counts=pd.Series([r['classification'] for r in rows]).value_counts().to_dict(),
                  exact_scope_instantiations=0,proof_verification='NOT_PERFORMED; only supplied statements and A.0 setting boundaries read',
                  theory_packet=ref(PACKET),request_sha256=snapshot['request_sha256'],snapshot=ref(SNAPSHOT),
                  protocol=ref(ROOT/'config/B_stage2B_EBM_protocol_v1.json'),new_fit_calls=0,new_permutations=0,
                  seal_intact=True,sealed_scientific_rows_exposed=0,new_market_data_requests=0,network_requests=0,
                  preexisting_artifacts_verified_unchanged=len(snapshot['files']),previous_stage2B_reports_and_results='VERBATIM_UNCHANGED',
                  numerical_discrepancies=[],editorial_corrections=['DIRECTLY_VALID -> CONDITIONAL_STANDARD_INFERENCE; source theorem T22.E1 not exactly instantiated','Point-threshold plus CI>0 is not LCB>materiality delta certification; no primary positive decision affected','Native learner mismatch alone does not preclude T22.G2/T24.I1/T25.F1; missing raw events/bias remain blocking'],
                  source_access='22user-supplied excerpts, original attribution/line/status; complete original source/proofs/context not on disk; no ChatGPT project access claimed',
                  code=[ref(ROOT/'src/ebm_research/experiment_b'/n) for n in ['stage2c.py','stage2c_theory.py','stage2c_report.py']],
                  commands=['.venv/bin/python -B -m ebm_research.experiment_b.stage2c'],
                  environment={n:metadata.version(n) for n in ['interpret-core','numpy','pandas','pyarrow','scipy','matplotlib']},
                  git_start=dict(branch=snapshot['branch'],commit=snapshot['commit'],dirty=True),
                  files_read=evidence['read_files'],outputs=[ref(f) for f in outputs],
                  preservation_hash_reads=[r['path'] for r in snapshot['files']],
                  additional_report_inputs=['data/registry/B_stage2A_validation_metrics.csv','data/registry/B_stage1_coefficients.csv'],
                  wall_seconds=time.perf_counter()-start,cpu_seconds=time.process_time()-cpu,
                  free_before=snapshot['free_bytes'],free_after=shutil.disk_usage(root).free,
                  newly_published_bytes=sum(f.stat().st_size for f in outputs),stop_go='CLOSE DEVELOPMENT; NO GO to final-test/permutation/trading without a separate task')
    write_json(root/'registry/B_stage2C_closeout_manifest.json',manifest)
    print(json.dumps(dict(verdict=manifest['implementation_QA'],A1=manifest['A1_closeout'],A2=manifest['A2_closeout'],theorems=len(statements),rows=len(rows),new_fits=0,bytes=manifest['newly_published_bytes'],seconds=manifest['wall_seconds'])))


if __name__=='__main__':run()
