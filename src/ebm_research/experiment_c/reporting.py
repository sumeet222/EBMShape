"""Readable P0 handback built only from reconciled compact outputs."""
import pandas as pd
from .preliminary import ROOT,OUT,CONFIG,read_json,sha,write_json,WINDOWS


def table(frame):
    """Small Markdown tables without an additional runtime dependency."""
    def fmt(x):
        if isinstance(x,float):return f'{x:.6g}'
        return str(x)
    return '| '+' | '.join(frame.columns)+' |\n| '+' | '.join(['---']*len(frame.columns))+' |\n'+'\n'.join('| '+' | '.join(map(fmt,row))+' |' for row in frame.itertuples(index=False,name=None))+'\n'


def generate(verdict,interpretation):
    """Write reports after human/agent review; never optimize a model or cutoff."""
    if verdict not in ['GO','WEAK','NO_GO_RV_PROXY_THIS_SAMPLE']:raise ValueError('Unknown P0 verdict')
    qa=read_json(OUT/'qa_results.json');assert qa['status']=='PASS'
    p=read_json(CONFIG);source=read_json(OUT/'source_manifest.json')
    w=pd.read_csv(OUT/'window_shares_by_state.csv');e=pd.read_csv(OUT/'effect_metrics.csv')
    missing=pd.read_csv(OUT/'missingness_exclusions.csv');match=pd.read_csv(OUT/'matched_date_comparison.csv')
    top=pd.read_csv(OUT/'top1_dates.csv')
    stats=w[(w.variant=='FULL')&(w.state=='high-minus-low')].copy()
    stats['effect_daily_SD']=stats.summary/stats.sd
    cols=['branch','mode','window','summary','lo_5','hi_5','lo_10','hi_10','effect_daily_SD']
    primary=stats[stats.window.isin(WINDOWS)][cols]
    supplementary=stats[~stats.window.isin(WINDOWS)][cols]
    fragility=w[(w.state=='high-minus-low')&(w['mode']=='remaining')&(w.window.isin(['MID','CLOSE']))][['branch','variant','window','summary','sd','n']]
    groups=[]
    for branch in ['OPEN','PREV']:
        meta=qa[branch]
        for state,n in zip(['low','middle','high'],meta['counts']):groups.append(dict(branch=branch,state=state,n=n))
    effects=e[['branch','mode','variant','mean_abs_HL','max_abs_HL','sum_abs_HL','TV','sum_HL','top_contrast_bin']].copy()
    effects['top_contrast_ET']=effects.top_contrast_bin.map(lambda k:f'{9+(30+5*int(k))//60:02}:{(30+5*int(k))%60:02}')
    full_effects=effects[effects.variant=='FULL'].drop(columns=['variant','top_contrast_bin'])
    artifact='../../artifacts/C/preliminary_RV_profile_v1_1/'
    common=f'''**Implementation / scientific QA: PASS. Preliminary scientific recommendation: {verdict}.**

{interpretation}

This is a model-free SPY RV-proxy screen, not the Andersen opening-VIX/futures estimator, a predictive test, a full C experiment, or evidence of tradability. No learners, VIX, trading or 2022–2026 scientific values were used. P0's descriptive 2016–2021 cohort does not instantiate the full C specification's future 60/20/20 fitted evaluation.

## Source and coverage

Alpaca SPY SIP, one-minute **UTC bar starts**, split-only adjustment (not dividend adjustment); ET sessions follow XNYS with DST. The existing D2 91-minute subsets were reused by hash. Only absent RTH minute keys were retained in one C supplement; all overlapping OHLC matched to relative tolerance1e-10. No HF patch was used. Source snapshots were obtained at different times; agreement over observed overlap does not prove absence of all vendor corrections. SIP bars reflect eligible reported trades, not a tick-level efficient-price curve. Vendor account/data terms still apply; the cache is not authorized for public redistribution by this report.

- Requested source range: {p['source_start']} through {p['end']}; Jan4 is auxiliary predecessor data only. Main descriptive dates: {qa['first']} through {qa['last']}.
- OPEN eligible days: **{qa['OPEN']['n']}**; PREV: **{qa['PREV']['n']}**; common dates: **{qa['matched_dates']}**. Main outcomes require 390 actual minute bars. Early closes, missing sessions/minutes, invalid prices and zero denominators are excluded; no forward fill.
- Response bodies transferred: **{qa['transfer_bytes']:,} / 1,000,000,000 bytes** including failed requests and retries. Three sandbox network attempts returned 0 bytes; authorized network retry succeeded. Supplemental cache: **{qa['retained_cache_bytes']:,} bytes**, 72 monthly disjoint-key Parquets. Raw JSON bodies were processed in memory and not retained.
- Source manifest: [{OUT.name}/source_manifest.json]({artifact}source_manifest.json); response ledger: [download_budget.jsonl]({artifact}download_budget.jsonl); file hashes and source references are included. The one cache must be restored along with matching original D2 referenced files; no source rows are copied by seed/fold.

Exclusions of main scheduled sessions:

{table(pd.DataFrame(list(qa['exclusion_counts'].items()),columns=['reason','sessions']))}

PREV eligibility on current complete main sessions:

{table(pd.DataFrame(list(qa['predecessor_exclusions'].items()),columns=['prior-session status','sessions']))}

All date-level reasons and missing-minute counts are in [missingness_exclusions.csv]({artifact}missingness_exclusions.csv). At least 300 full days across 2 years were required before analysis; both branches exceed this gate.

The 7 incomplete ordinary sessions are 2016-02-02 (9 missing minutes),2019-08-12 (30),2020-03-09/12/16/18 (14 each),2021-05-05 (5). Their 100 missing minutes are not imputed; several are major crisis dates. Consequently completeness selection is nonrandom, and this result concerns the eligible cohort, not all crisis sessions. Missing bars may reflect trading interruptions as well as provider coverage; no cause was established here. Early-close rows are rejected by calendar before price analysis and their additional source minutes are deliberately not retained; their missing-grid counts are not a claim of provider failure.

## Exact statistical object and state rules

For a 390-minute session, r[0]=log(C09:30/O09:30); r[j]=log(C[j]/C[j-1]) for j=1,...,389. Each increment is assigned to the five-minute bin containing its bar start. Thus 09:34 belongs to09:30–09:35; 09:35 to09:35–09:40; 15:54 and15:55 are in distinct final bins. No overnight term, no return spanning a missing minute, no borrowing an extra first-bin return. rv[d,k]=sum of five squared minute logs, RV_day=sum of 78 rv, q[d,k]=rv[d,k]/RV_day. The plotted mean is **mean of daily ratios**, not ratio of group RV totals. There is no square root or log transform of the state in P0.

RV_open=sum of first 6 bins (09:30–10:00). This overlaps the first six outcomes and is **RETROSPECTIVE_DESCRIPTIVE**, not an available-at-open forecast. RV_prev is RV_day of the immediately prior scheduled exchange session. Missing/incomplete/early-close predecessors invalidate PREV; we never leap to an older full session or inherit B's prior-full rule. Prior data may inform the state but not today's scientific target. Whole-sample, branch-specific terciles use stable(value,date) order and label=floor(3*zero-based-rank/N). Fixed labels are exhaustive/disjoint for each branch; full-sample descriptive cuts are unsuitable for an untouched predictive claim.

{table(pd.DataFrame(groups))}

OPEN boundaries: `{qa['OPEN']['boundaries']}`; tied rows: {qa['OPEN']['tied_rows']}. PREV boundaries: `{qa['PREV']['boundaries']}`; tied rows: {qa['PREV']['tied_rows']}. Boundary ties may split by date and are explicitly flagged. Whole-curve comparisons mix different marginal state cohorts unless the matched-date view below is used.

**Approved window resolution:** P0 primary OPEN 09:30–10:00 (bins0:6), MID 12:00–13:00 (30:42), CLOSE 15:30–16:00 (72:78). Per explicit 2026-10-17 user decision, frozen C-spec MID 11:30–13:30 (24:48) and CLOSE 15:00–16:00 (66:78) are supplementary. These unequal-duration shares are fractions of whole-day RV, not comparable per-minute rates. Windows do not exhaust the day and are dependent. C-spec reporting tolerances remain 0.02 for closing-hour/opening share and 0.05 for profile TV; P0 does not claim equivalence or calibrate power to these tolerances.

## Primary numerical contrasts and uncertainty

All estimates below are high-minus-low **fractions** (multiply by100 for percentage points). `effect_daily_SD` divides the contrast by pooled high/low daily within-group SD; it is a descriptive scale comparison, not a predictive effect or test statistic. `whole` is primary q; `remaining` uses rv[6:78]/sum(rv[6:78]) with unchanged original state labels. The latter removes direct numerator overlap with RV_open but not every compositional/state dependence.

{table(primary)}

## Supplementary C-spec windows

{table(supplementary)}

## Shape effect magnitudes

{table(full_effects)}

Mean/max/summed absolute H−L are computed over 78 bins (72 for remaining); TV=0.5×summed absolute difference. Top contrast bins are exploratory descriptive locations, not a post-hoc aggregated inferential target. The automatic sum(H−L)=0 identity follows from closure and provides no evidence for/against specific time differences.

## Dependence, uncertainty and robustness

Seed 42; 1,000 valid circular date-block draws per branch and block length 5/10. Each draw resamples whole scheduled exchange-date slots jointly across all bins and states, including ineligible and early-close slots marked−1. Invalid slots do not enter group means; they are not filled or collapsed so blocks never jump over internal missing dates. Circular wrapping occurs only at cohort endpoints. Tercile labels/cuts are held fixed, so intervals condition on the observed classification and are not unconditional sample-quantile or causal uncertainty. Bands and window intervals are percentile 95% **pointwise**, not simultaneous/global tests; two block sizes do not establish robustness to all dependence structures. Failed/empty draw counts are in [bootstrap_log.csv]({artifact}bootstrap_log.csv).

Within each branch remove ceil(1%×N) largest RV_day sessions, date-tie order fixed, preserving original labels. FULL remains primary and is never overwritten. Median window contrasts are medians of daily window shares, not sums of per-bin medians. Per-bin median curves need not sum to one and are not probability profiles.

{table(fragility)}

Top1% concentration of raw RV (levels, not a measure of normalized shape) and removed counts:

{table(e[(e.variant=='FULL')&(e['mode']=='whole')][['branch','top1_count','top1_RV_concentration']])}

All removed dates/levels are in [top1_dates.csv]({artifact}top1_dates.csv); first listed dates:

{table(top.head(12))}

## Matched-date comparison

Both branches share{qa['matched_dates']} outcome dates. This sensitivity retains each branch's original tercile assignment; it does not re-rank on the intersection. High and low members differ across states even on identical outcome dates, so this is not a paired causal state comparison. Low/middle/high state cross-count matrix (OPEN rows, PREV columns): `{qa['cross_state_counts']}`.

{table(match[match.window.isin(WINDOWS)])}

## QA and limits

Eight focused tests cover known390-return/78-bin accounting, endpoints/first-open term, DST/holiday/half-day logic, missing/duplicate/order/end-label/invalid/zero cases, immediate predecessors, stable ties, stream byte cap and temporary-output/joint-block reconstruction. A real-data scalar recomputation for one full day per year agrees with the vector kernel. Unique symbol/minute keys, stored session-vs-ET consistency, full grid, positive finite prices, row/group q closure, remaining closure and independently reconstructed ranks were checked. Group means, FULL/drop-top1/median windows and plotted differences reconcile independently from saved daily arrays to1e-10. Both block-length percentile outputs were independently replayed using weighted date counts rather than selected-row means. Images decode, are nonblank, have widths≥1600, correct ET bin ordering/common comparable scales and all three state legends. See [qa_results.json]({artifact}qa_results.json). All{qa['preserved_file_count']} snapshotted prior files, including B artifacts and source references, remain hash-unchanged. A source QA PASS does not prove bar-level market microstructure fidelity or validate the scientific hypothesis.

Single SPY asset and selected descriptive era; no VIX, futures, jump-robust latent periodicity estimator, causal effect, forecasting result or independent confirmatory holdout. State assignments are ex-post sample terciles. Bands are exploratory, with no multiplicity-adjusted global shape test or full-process re-estimation of cutoffs. State/compositional dependence persists after nonoverlap. Crisis concentration in total RV does not itself establish normalized-mean fragility; the reported robust contrasts address that separately.

## Reproduce and handoff

Use the repository's editable Python environment (`pip install -e .`), configured Alpaca credentials in local.env, and matching authorized D2 source files from the manifest (or portable EBM_DATA_ROOT). Never copy licensed files into a public clone. Preserve the frozen [C P0 configuration](../../config/C_preliminary_RV_profile_v1.json), authoritative C spec hash and source supplement hashes. Existing C sources are reused without more downloads by `acquire`; resume incomplete months only while preserving the cumulative ledger. Fresh network acquisition at a later date may produce vendor revisions and must be a new source snapshot rather than silently claiming the same hashes.

```sh
.venv/bin/python -B -m unittest discover -s tests -p 'test_c_preliminary_RV_profile.py' -v
.venv/bin/python -B scripts/c_preliminary_RV_profile.py check
.venv/bin/python -B scripts/c_preliminary_RV_profile.py acquire
.venv/bin/python -B scripts/c_preliminary_RV_profile.py run
.venv/bin/python -B scripts/c_preliminary_RV_profile.py verify
.venv/bin/python -B scripts/c_preliminary_RV_profile.py report
```

No further model or source acquisition is authorized by these results. Review this screen in the C-design thread before approving a next experiment. Primary implementation files are `preliminary.py`, `profile_audit.py`, `reporting.py` and the thin CLI. Runtime: {qa['python']}; packages: `{qa['versions']}`. Successful analysis/QA/plot wall time {qa['wall_seconds']:.1f}s. Source acquisition wall time {source['wall_seconds']:.1f}s. Final exact output hashes/storage and session commands are recorded separately in the coding-session report.
'''
    reports=ROOT/'reports/C';reports.mkdir(exist_ok=True)
    (reports/'C_preliminary_RV_profile_results.md').write_text('# Experiment C P0 — normalized RV-profile feasibility\n\n'+common)
    figs=sorted((OUT/'figures').glob('[0-9][0-9]_*.png'))
    def embed(numbers):
        return '\n\n'.join(f'![{f.stem}]({artifact}figures/{f.name})' for f in figs if int(f.name[:2]) in numbers)
    gallery=f'''# Experiment C P0 — visual review gallery

**QA PASS · scientific recommendation {verdict}.** {interpretation}

Read the [scientific report](C_preliminary_RV_profile_results.md) for complete source, exclusions, arithmetic, fixed terciles and limitations. OPEN n={qa['OPEN']['n']}, PREV n={qa['PREV']['n']}; matched n={qa['matched_dates']}; {qa['first']}–{qa['last']}. Fractions below become percentage points after multiplying by100. Bands are pointwise exploratory date-block intervals, never simultaneous proof. P0 windows are primary; C-spec wider windows are supplementary per user decision.

## OPEN: retrospective descriptive same-day state

The first six response bins enter the state directly. The shaded interval marks this mechanical overlap; assess later/renormalized behavior separately. Counts are in legends, and shared scales match PREV.

{embed([1,3,5,7])}

## PREV: immediate prior scheduled-session state

Missing and half-day predecessors are excluded, not skipped. The grouping is temporally prior, but descriptive tercile thresholds use the full observed branch cohort.

{embed([2,4,6,8])}

## Nonoverlap diagnostic

These 72-bin profiles renormalize only10:00–16:00 variance and keep the original state labels. This removes direct opening-numerator overlap, not all dependence. Primary full-day curves above remain the main result.

{embed([9,10])}

## Primary H−L numerical window shares

{table(primary)}

## Supplementary wider C-spec windows

{table(supplementary)}

## Matched dates, outliers and dependence

Matched outcome cohort n={qa['matched_dates']}; original ranks retained (no new quantile selection). OPEN×PREV cross-state counts: `{qa['cross_state_counts']}`.

{table(match[(match['mode']=='remaining')&(match.window.isin(['MID','CLOSE']))])}

{table(fragility)}

{embed([11,12])}

Top1% exclusion is a sensitivity with FULL primary; medians describe daily shares and are not normalized mean curves. Both 5/10 block interval sets appear in the numeric tables. Ordinary within-group daily scatter is substantial; standardized effects are not predictive performance. No strongest-bin aggregation, VIX replication, model fitting or trading inference follows from these figures.

## Whole-profile magnitudes and handback

{table(full_effects)}

**{verdict}.** {interpretation}

Report and [machine QA]({artifact}qa_results.json) distinguish passed numerical implementation from this provisional scientific judgment. [Contact sheet]({artifact}figures/contact_sheet.png) and individual figures are self-contained; all Markdown image paths resolve locally.
'''
    (reports/'C_preliminary_RV_profile_visual_gallery.md').write_text(gallery)
    write_json(OUT/'scientific_verdict.json',dict(verdict=verdict,interpretation=interpretation,qa_sha256=sha(OUT/'qa_results.json'),
        protocol_sha256=sha(CONFIG),rubric=p['rubric'],no_models=True,no_heldout_claim=True))
