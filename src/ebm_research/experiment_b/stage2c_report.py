"""Separate Stage2C qualifications/closeout; never rewrite historical stage reports."""
import json
import os

import numpy as np
import pandas as pd

from .pilot import ROOT


def table(rows,columns):
    """Small dependency-free Markdown table, retaining negative values and missing status."""
    lines=['| '+' | '.join(columns)+' |','| '+' | '.join(['---']*len(columns))+' |']
    for row in rows:
        values=[]
        for key in columns:
            value=row.get(key)
            if isinstance(value,(list,dict)):value=json.dumps(value)
            if value is None or (isinstance(value,float) and np.isnan(value)):value='—'
            elif isinstance(value,(float,np.floating)):value=f'{value:.7g}'
            values.append(str(value).replace('|','\\|').replace('\n',' '))
        lines.append('| '+' | '.join(values)+' |')
    return '\n'.join(lines)


def make_overlay(root,protocol):
    """Two optional same-model/three-state displays from the existing frozen sparse table."""
    os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'logs/stage2C_matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot as plt
    source=pd.read_csv(root/'registry/B_stage2B_ebm_surfaces.csv')
    out=ROOT/'artifacts/B/stage2C';out.mkdir(parents=True,exist_ok=True);paths=[]
    states=['low','middle','high'];colors=['tab:blue','tab:orange','tab:green']
    for info in ['E','L']:
        f=source.loc[source.model_id.eq('A1c_'+info)&source.seed.eq(42)&source.variant.eq('FULL')&source['mode'].eq('fixed')]
        fig,ax=plt.subplots(figsize=(9,5.5));xs=np.asarray(protocol['sparse_plot']['x'])
        masks=[]
        for state,color in zip(states,colors):
            part=f.loc[f.state.eq(state)].sort_values('x')
            if not np.array_equal(xs,part.x.to_numpy()):raise ValueError('Overlay must use exactly the saved Stage2B grid')
            masks.append(part.supported.to_numpy())
            ax.plot(part.x,part.forecast,'o--',color=color,alpha=.6,label=state+' RV state (same A1c model)',ms=4)
            if info=='E':ax.plot(part.x,np.where(part.supported,part.forecast,np.nan),'o-',color=color,ms=4)
        common=np.logical_and.reduce(masks)
        for j,x in enumerate(xs):
            if info=='L' or not common[j]:
                left=(xs[j-1]+x)/2 if j else xs[0];right=(x+xs[j+1])/2 if j+1<len(xs) else xs[-1]
                ax.axvspan(left,right,color='gray',alpha=.14)
        title='A1 / E at10:00 — one fitted A1c_E, three RV states' if info=='E' else 'A2 / L at15:30 — one fitted A1c_L, W=0 bp'
        ax.set(title=title,xlabel='Prior full close →10:00 return X (bp)',ylabel='Total fitted signed final-30-minute return F (bp)',xlim=(xs[0],xs[-1]))
        ax.legend(fontsize=8);ax.axhline(0,color='black',lw=.6)
        if info=='E':
            caption='Solid: broad-tercile local cells ≥50dates/20five-row groups. Gray: common-state screen fails.\nDashed: model display only. Continuous-point population shape and its CI are NOT CERTIFIED.'
        else:
            caption='MODEL DISPLAY ONLY — SCIENTIFIC ABSTAIN\nNo declared late joint-support candidate passes. Dashed curves have no population confidence claim.'
        fig.text(.5,.035,caption,ha='center',fontsize=9)
        fig.text(.5,.005,'Frozen state medians/grid, FULL seed42; lines connect saved queries, not derivatives or confidence bands.',ha='center',fontsize=8)
        fig.tight_layout(rect=(0,.13,1,1));path=out/f'one_model_three_volatility_states_{info}.png';fig.savefig(path,dpi=125);plt.close(fig);paths.append(path)
    return paths


def write_reports(root,p,rows,e):
    """Publish theorem-by-theorem scope and an explicitly developmental A1/A2 conclusion."""
    audit=ROOT/'reports/B/stage2C_theorem_method_audit.md'
    narrative='''# Experiment B Stage 2C — theorem-to-diagnostic audit

**PASS WITH QUALIFICATIONS. Zero EXACT_SCOPE_INSTANTIATION claims.** This audit received 22 original theorem/proposition **statements**, their source filenames/starting lines, and the supplied A.0 setting boundaries. It did not receive or independently reverify the full proofs/settings or access the user's ChatGPT project. The exact supplied appendix is preserved in [theorem packet](../../docs/specs/experiment_B_stage2C_supplied_theorem_extracts_v1.md); its hash, per-excerpt hashes and original lines are in the manifest/crosswalk. A source label such as PROVED HERE records the internal mathematical research's status under its own hypotheses. It is not proof of applicability to SPY, priority/publication, or a new result proved by this session.

The source packet supersedes Stage2B's then-correct statement that original theorem text was unavailable. The old reports, protocol, ledger and fitted results remain verbatim. This Stage2C report is the authoritative **qualification**; no numerical result, model setting, source or scientific definition was changed. All evidence is developmental train2016–2021/validation2022–2023; the 683 sealed2024–September2026 scientific observations remain unopened.

## What was actually verified

The 11 native model families, 562 successful component records, five seeds, 210 complete497date validation series and declared native terms/types reconcile. Saved actuals/losses and forecast chronology reconcile. All11 primary saved models reproduced four frozen query predictions and small validation prediction spot-checks without fitting. A1c_E D_F≈0.526240bp; additive/state-blind cross-state X increments cancel numerically. Full E local bands at±20bp/h15 have n/block counts116/90,189/122,72/60,67/52. These are finite-sample occupancy diagnostics; distinct five-row groups are not established independent clusters. No late candidate passes; its±10bp/h5,W0±5 display is audit-only and scientificABSTAIN. All70 candidate decisions were recounted from training predictors, without choosing a new candidate.

The raw continuous-point query at the frozen medianZ is different from four broad local-X×RV-tercile cell means. The latter also averages differing X/W distributions. Counts cannot supply an identified regular version, Holder constant, finite-range bound or localization bias. E pointwise raw inference remains **NOT_CERTIFIED/INCONCLUSIVE**, despite accepted broad bands. Validation contains only31low-state days, so a four-cell validation band check cannot meet50percell. Lraw contrast remains **ABSTAIN**, not an estimate of zero.

## Corrections that matter

1. **DIRECTLY_VALID → CONDITIONAL_STANDARD_INFERENCE for ordinary paired-loss HAC.** Its arithmetic is correct. Validity still needs adequate loss moments, a weak-dependence/FCLT regime, bandwidth adequacy and attention to evolving fitted forecasts. The T22.E1 statement specifically conditions on full discovery and independent held-out clusters, with its own IID/known finite-dependence or separate bounded/Gaussian routes. These premises are not verified here. Heavy tails, heteroskedasticity, serial dependence and development reuse qualify the inference. Conditions are unverified, not declared mathematically false merely from diagnostic rejection.
2. **Holm is multiplicity adjustment, not full selection conditioning.** Two primary fixed-loss p-values were adjusted; neither is an exact selected-shape pivot or independent confirmation. Settings were chosen on2021 training-era development, but2022–2023 were reused for Stage2A/2B reporting and retrospective comparisons; quarterly learners also consume earlier validation outcomes. A fixed-vector HAC summary does not fully model that forecast-estimation path.
3. **Materiality requires the relevant uncertainty bound.** Fitted|D_F|<1bp is not raw equivalence. T15.C1/T25.F1 need the appropriate raw confidence event. For positive predictive materiality, T22.E1 requires a valid gain lower bound above the positive threshold; the Stage2B operational screen of pointgain≥threshold plus CIabovezero is weaker. No primary affirmative materiality decision passed, so this clarification invalidates no published primary number/decision. Any positive flags against weaker S4/S6 models are not theorem-certified meaningful improvement or superiority over C1/N0.
4. **Algorithm mismatch is not a universal prohibition.** T22.G2(7.3), T24.I1(10.4) and T25.F1(12.2) permit arbitrary measurable current fits, including data-selected native outputs, on an appropriate simultaneous raw event. Native-vs-idealized learner mismatch alone does not block these current-output bounds. What is missing here is the calibrated raw event, matched estimand and any required localization/class information. Conversely, future-path, optimization and literal12tree theorems do require their actual dictionary/path hypotheses; native iteration metadata is no certificate.
5. **The composition calculation is a different identity.** The saved error split is exactly (p_val−p_train)·L_train+p_val·(L_val−L_train). It includes training optimism and changing within-state difficulty. It is not T18.A1's two-state projector or T24.E1's population conditional shape/level/kernel decomposition, and it is not causal transport.

## Classification inventory

'''
    counts=pd.Series([r['classification'] for r in rows]).value_counts().to_dict()
    narrative+=table([dict(classification=k,rows=v) for k,v in counts.items()],['classification','rows'])
    narrative+='''

Algebraic rows below certify only deterministic observed-table/prediction identities, not a theorem's probability event. CONDITIONAL_STANDARD_INFERENCE rows are standard classical inference with stated assumptions, not novel internal-theory guarantees. ADAPTED_DESCRIPTIVE rows implement useful ideas without claiming source hypotheses. BLOCKED_ASSUMPTIONS means a relevant route lacks premises; NOT_APPLICABLE marks a genuinely different experiment/dictionary. NOT_EXECUTED/DEFERRED records no calculation.

## Theorem-by-theorem correspondence

'''
    for r in rows:
        narrative+=f'''### {r['implementation_id']} — {r['classification']}

Source: `{r['original_filename']}`, original line **{r['source_line_or_section']}**; supplied packet lines{r['packet_line_start']}–{r['packet_line_end']}. Access: statement and A.0 only. Source status verbatim: {r['source_status']}

Target: {r['theorem_exact_target']}. Observation law: {r['theorem_observation_law']}. Learner/dictionary: {r['learner_or_dictionary']}. Scope: {r['finite_sample_or_asymptotic']}.

Required information: {r['required_known_information']}. Selection/conditioning: {r['selection_and_conditioning']}.

'''
        for assumption,evidence in json.loads(r['actual_SPY_evidence_for_each_assumption']).items():narrative+=f'- **{assumption}:** {evidence}\n'
        narrative+=f'''
Actual computation: {r['software_computation_and_path']}. Missing/mismatched evidence: {r['mismatch_or_missing_evidence']}

Permitted claim: {r['valid_claim']}. **Forbidden claim:** {r['forbidden_claim']}. Future condition: {r['remedy_or_future_condition']}.

'''
    narrative+='''## Source-setting gaps and scholarly record

A.0 explicitly places T16–T18 in idealized proper tree spaces and specified greedy histories. T17 has no original statement supplied here; no invented theorem ID or optimizer result is quoted. T19/T21 are supplied **scope notes only**, separating environments/shared-time-panel assumptions and mixture stability from conditional shape/causal drift. The stand-alone T19 source was not supplied. FD/FL, (D)/(H), full G1/G2/B1, I1/J1–J3, P0-G/Q-RARE/U-RARE, and the T25 response/admissibility settings were not recovered beyond the supplied statements/A.0. A complete exact-scope instantiation would need those definitions and verified evidence for every premise; none is claimed.

The source's PROVED HERE/PROVED IN T25 labels include T10B.B2, T18.A1/R1, T23.G1, T24.E1 and T25 statements, while acknowledging classical representer, residualization, concentration, projection and confidence-event ingredients. T12.C1 explicitly specializes a known conditional-Gaussian principle. T15.C1/F1 and T20/T22 include inherited/classical confidence-event consequences. This audit preserves those labels instead of calling standard HAC/bootstrap a newly proved inference method. Neither independent mathematical-proof validation nor originality/publication priority was audited.

## Practical accomplishment and boundary

The executed contribution is a reproducible theorem-to-implementation ledger with actual native term/forecast/source verification, support-aware whole-response contrasts, raw-versus-band/fit distinctions, explicit selection/dependence/materiality qualifications and a closed developmental experiment. This is distinct from proving that the internal theorems hold for the financial data. No model refit, discovery search, new dependency, network request, null/permutation, sealed evaluation or economics was performed. See [A1/A2 closeout](stage2C_literature_anchored_A1_A2_closeout.md) for the scientific conclusion.
'''
    audit.write_text(narrative)
    close=ROOT/'reports/B/stage2C_literature_anchored_A1_A2_closeout.md'
    score=e['scorecard'];simple=pd.read_csv(root/'registry/B_stage2A_validation_metrics.csv')
    baseline=simple.loc[simple.variant.eq('FULL')&simple['mode'].eq('quarterly')&simple.model_id.isin(['N0','N1','OLS1_E','OLS3_L','OLS2_L','C1_E','C1_L','C2_E','C2_L','S4_E','S4_L'])]
    source=pd.read_csv(root/'registry/B_stage1_coefficients.csv')
    slopes=source.loc[source.cohort.eq('principal')&source.hac_lag.eq(5)&source.model.isin(['OLS1_E','OLS3_L'])&source.term.isin(['x_open_bp','w_preclose_bp'])]
    statement='''# Experiment B — literature-anchored A1/A2 developmental closeout

**A1: CLOSED_INCONCLUSIVE_DEVELOPMENT. A2: CLOSED_INCONCLUSIVE_DEVELOPMENT.** The specified literature-anchored development pipeline is complete. The qualified negative finding is **no credible incremental state-interaction forecasting benefit established**. This is not a proof of no population effect or equivalence. Scientific raw shapes remain uncertified; late joint-support comparisons abstain. No progression to a permutation, sealed test or trading stage is needed to close this developmental work.

## Actual dataset, timing and source fidelity

One canonical SPY daily table derives from immutable Alpaca SIP split-adjusted D2 plus exactly39 native-price D2.1c Hugging Face missing-key repairs. Daily ID B_SPY_daily_split_source1_stage1_v1; SHA256 `2aa3e2df1cab897abd679ed9cbeff8f6fcb004ecc01a7b32c5938aa6c23b5c2f`. Stored full-session metadata2016-01-04–2026-09-30; first eligible2016-01-05. Training1,495days2016–2021; developmental validation497days2022–2023. Sealed683days2024–September2026 were not used for science here. Short sessions and missing critical anchors/opening minutes remain excluded; no new price repair or dataset copy.

Time zone America/New_York, minute bar timestamps denote UTC starts. Pprev is the preceding permitted full-session15:59close; P10/P15/P1530/P16 are09:59/14:59/15:29/15:59bar closes. X=10,000(P10/Pprev−1), including overnight; W=10,000(P1530/P15−1); Y=10,000(P16/P1530−1), the signed scientific final30minute return. OpeningRV=√[log(C09:30/O09:30)²+Σ29consecutiveclose-log-return²], Z=log(RV+1e−8). A1/E10:00 uses X and this opening state; A2/L15:30 adds W. L is not an early forecast and its inherited X-shape question does not isolate pure W effects. A2c_L separately explores W×Z beyond its X×Z interaction.

Gao1993–2013/ Limkriangkrai1996–2013 source-era data are unavailable: this is the approved modern2016start branch, not exact historical replication. The RV operational proxy/source normalization, TAQ versus SIP trade-count filtering, native community patch adjustment/rights and one-sided terminal repair qualifications remain in the [source crosswalk](../../docs/experiment_B_source_method_crosswalk.md). User-directed private use does not establish public redistribution rights. Modern training slopes do not corroborate the historical positive pattern:

'''+table(slopes.to_dict('records'),['model','term','n','coefficient','ci_low','ci_high','p_value'])+'''

These linear-projection HAC intervals are conditional on their own moment/dependence/selection assumptions. Within-state significance is not a between-state difference. Stage2A's six primary moderation/curvature tests did not survive Holm; C1/C2/S4 did not show convincing incremental benefit, with splines overfitting. Negative results were not rescued by changing targets, samples or state definitions.

## Executed model/evaluation ladder

Eleven native InterpretML0.7.3 families: SB_E/L; additive A0c_E/L and A0d_E/L; X×S A1d_E/L; X×Z A1c_E/L; secondary late A2c_L adds W×Z. No automatic interaction mining; S nominal and Z numerical. Same frozen RV cutoffs[0.001558374721607106,0.0024281183976187152] across validation. Two bounded settings selected on training-era2016–2020→2021; five final seeds; eight final bags; internal stochastic train-only early stopping is algorithmic. All562component fits/55FULLfamily-seed fits completed, including predeclared crisis/outlier/matched-source/temporal sensitivities. Native bins update within each past history. The old total662 field was an arithmetic error; all seven intended component counts sum562.

Both fixed2016–2021 and strictly past-only quarterly expanding predictions exist on identical497validationdates. Quarterly models can use earlier completed validation outcomes, never current/future Y; original category cutoffs/settings stay fixed. The validation period was reused across stages and comparisons, so it is development, not independent confirmation. E versus L mixes information availability and is not an equal-information model contest.

Quarterly FULL seed42 EBM scorecard (RMSEbp, MSEbp²):

'''+table(score,['model_id','n','RMSE','MSE'])+'''

Simple/naive quarterly comparators on identical dates:

'''+table(baseline.to_dict('records'),['model_id','n','RMSE','MSE'])+'''

Principal and strong-comparator paired gains (positive favors A1c; conditional asymptotic BartlettHAC5/10/20 numerical verification):

'''+table(e['paired_checks'],['info','candidate','comparator','n','lag','gain','ci_low','ci_high','p_holm'])+'''

A1c−A0c primary quarterly gains are negative in E and L, Holm p≈.2065/.8590. C1 is the strongest saved state-aware simple comparator within E/L, and N0 is stronger among the saved naive/source-OLS references. A1c_E is worse than C1/N0 by point MSE; A1c_L's small point gains over C1/N0 have wide intervals including no gain. The discrete interaction adds almost nothing over its categorical additive counterpart: quarterly A1d−A0d gains≈−.173bp²E/+ .220bp²L, both intervals includezero. Some EBMs beat overfit S4/S6 models, which does not establish increment over C1/N0. Early SB has lower observed RMSE than the state-aware EBMs; late A2c_L has the smallest late EBM point RMSE, but neither a minimum row nor its small A2c_L−A1c_L gain proves a reliable state/W interaction.

Interpretation: adding additive Z information, nonlinear state-blind flexibility, X×state moderation and W×state moderation are different questions. State-linked conditional scale/ARCH is evident but is not useful signed-mean moderation by itself. Standard paired loss/bootstrap uncertainty is **CONDITIONAL_STANDARD_INFERENCE**, not exact post-selection or raw shape inference. Holm does not repair dependence/moment violations or account for the entire discovery trajectory. A materiality claim would need the relevant valid lower bound, not only a favorable point gain.

## Scientific shape, support and stability

The frozen E comparison is X−20→+20bp with local Xhalfwidth15 and broad low/high RVterciles. Training cell counts116/189/72/67, with90/122/60/52distinct five-row groups, satisfy an exploratory heuristic. The four continuous model query values at fixed training medianZ give A1c_E D_F≈.52624bp. Additive controls cancel by construction. None of this is a raw pointwise D_m estimate or affirmative±1bp equivalence. Broad band means integrate different X/W/Z distributions; their raw-versus-predicted band comparison is a different estimand. Validation low/middle/high occupancy31/151/315 prevents the required independent local-band confirmation. Lhas no accepted joint X/RV/Wcandidate, so raw scientific contrast **ABSTAIN**, never zero.

Heavy tails, serial dependence, residual conditional scale, influential2020-03-18 and native sparse/extreme bins persist. Fixed single/top-five/2020/matched-source deletions, seeds and dated-window refits are perturbation diagnostics, not independent sampling confidence. No sensitivity replaces FULL because it looks favorable. The empirical state-error mixture decomposition is exact observed algebra and includes training optimism; it is not a transport or stable-conditional-shape theorem. Within-tercile Z/prediction spread documents finite-panel compression, not a known-moment inverse or isolated causal information loss.

Optional explanatory overlays show **one model, three states**, on the original grid and state medians. Gray/dashed regions are unsupported/model display only; no confidence bands or new science selection:

![A1 early three-state total display](../../artifacts/B/stage2C/one_model_three_volatility_states_E.png)
![A2 late three-state total display](../../artifacts/B/stage2C/one_model_three_volatility_states_L.png)

## Theory correspondence and accomplishment

Twenty-two supplied source statements were audited, with zero exact-scope instantiations. The [theorem audit](stage2C_theorem_method_audit.md) and [flat crosswalk](../../data/registry/B_stage2C_theorem_diagnostic_crosswalk.csv) preserve each source's filename/line/status and separate actual deterministic algebra, adapted diagnostics, conditional standard inference, blocked premises and different-model theorems. T12 exact Gaussian selection and literal tree-path guarantees do not apply by analogy. T22.G2/T24.I1/T25.F1 can cover an arbitrary current native output **if** valid matched raw confidence/bias information exists; it does not exist here. Unverified population bounds, smoothness, moments and mixing are marked unverified, not inferred false just from sample diagnostics. Omitted settings/proofs were not independently certified.

CV-ready executed record:

- Implemented and audited an11family native EBM ladder with fixed information times/interactions, five-seed matched chronological development evaluation and stronger simple/naive controls, retaining negative and abstaining findings.
- Adapted support-aware whole-response and raw-versus-fitted scientific diagnostics from the internal theory program; produced an assumption-by-assumption crosswalk against22supplied statements and independent no-refit numerical verification.
- Distinguished original internal source labels from classical tools and software application; did not claim a new proof, publication priority, theorem validity for dependent SPY, certified shape or alpha.

## Explicit closure and remaining boundaries

**Close A1/A2 development now as CLOSED_INCONCLUSIVE_DEVELOPMENT.** Implementation and bounded developmental science are complete, with qualified negative incremental-prediction evidence and uncertified/unsupported raw shapes. H0exacthistoricalreplication is unavailable; H1modernpredictive benefit is not confirmed; H2/H3moderation/nonlinear increment are not established; H4representation differences are descriptive; H5rawenvironmental equivalence is uncertified; H6economics is untested.

**No-test/no-permutation decision:** zero new learner fits, zero null replicates, zero sealed evaluation and no trading/cost analysis. The previously deferred100full-discovery null (~8400native fits for the recorded two-family five-seed path) stays deferred; this session does not launch or require it. Sealed2024–September2026 stays sealed. A future sealed/permutation/economic study would need a separate reviewed task, assumptions and frozen protocol. Do not describe development closure as completion of the original full confirmatory/economic agenda.

A3–A6, rolling-RV, macro/options or new targets are separate research projects, never retroactive rescues of this A1/A2 result. No mandatory next model experiment remains for this closeout. All earlier reports/data/models/forecasts were preserved verbatim. See [closeout manifest](../../data/registry/B_stage2C_closeout_manifest.json) and the linked detailed session report for exact access, checks, hashes, commands and resources.
'''
    close.write_text(statement)
    return [audit,close]
