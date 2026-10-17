# Experiment C P0 — normalized RV-profile feasibility

**Implementation / scientific QA: PASS. Preliminary scientific recommendation: WEAK.**

Primary P0 evidence is mixed, so the overall recommendation is WEAK/INCONCLUSIVE. The OPEN-state whole-day closing-half-hour contrast is -1.196 percentage points (block5 interval -2.131 to -0.294); after post-10:00 renormalization it is -1.160pp, but the block10 interval crosses zero (-2.355 to +0.053pp). PREV primary closing-half-hour and midday contrasts are uncertain. A promising, separately labeled supplementary PREV closing-hour contrast is +2.005pp (block10 +0.839 to +3.206pp), with positive remaining-day, drop-top1 and median contrasts; it is not promoted to the primary window. Remaining-day profile TV is0.0361 OPEN and0.0444 PREV, below the C-spec reporting tolerance0.05 as point estimates only, with no equivalence inference. These signals warrant design-thread review, not a claim that the RV-state extension has been confirmed or ruled out.

This is a model-free SPY RV-proxy screen, not the Andersen opening-VIX/futures estimator, a predictive test, a full C experiment, or evidence of tradability. No learners, VIX, trading or 2022–2026 scientific values were used. P0's descriptive 2016–2021 cohort does not instantiate the full C specification's future 60/20/20 fitted evaluation.

## Source and coverage

Alpaca SPY SIP, one-minute **UTC bar starts**, split-only adjustment (not dividend adjustment); ET sessions follow XNYS with DST. The existing D2 91-minute subsets were reused by hash. Only absent RTH minute keys were retained in one C supplement; all overlapping OHLC matched to relative tolerance1e-10. No HF patch was used. Source snapshots were obtained at different times; agreement over observed overlap does not prove absence of all vendor corrections. SIP bars reflect eligible reported trades, not a tick-level efficient-price curve. Vendor account/data terms still apply; the cache is not authorized for public redistribution by this report.

- Requested source range: 2016-01-04 through 2021-12-31; Jan4 is auxiliary predecessor data only. Main descriptive dates: 2016-01-05 through 2021-12-31.
- OPEN eligible days: **1491**; PREV: **1472**; common dates: **1472**. Main outcomes require 390 actual minute bars. Early closes, missing sessions/minutes, invalid prices and zero denominators are excluded; no forward fill.
- Response bodies transferred: **119,675,359 / 1,000,000,000 bytes** including failed requests and retries. Three sandbox network attempts returned 0 bytes; authorized network retry succeeded. Supplemental cache: **10,318,012 bytes**, 72 monthly disjoint-key Parquets. Raw JSON bodies were processed in memory and not retained.
- Source manifest: [preliminary_RV_profile_v1_1/source_manifest.json](../../artifacts/C/preliminary_RV_profile_v1_1/source_manifest.json); response ledger: [download_budget.jsonl](../../artifacts/C/preliminary_RV_profile_v1_1/download_budget.jsonl); file hashes and source references are included. The one cache must be restored along with matching original D2 referenced files; no source rows are copied by seed/fold.

Exclusions of main scheduled sessions:

| reason | sessions |
| --- | --- |
| ELIGIBLE | 1491 |
| EARLY_CLOSE | 12 |
| INCOMPLETE_OR_WRONG_RTH_GRID | 7 |


PREV eligibility on current complete main sessions:

| prior-session status | sessions |
| --- | --- |
| ELIGIBLE | 1472 |
| PREDECESSOR_INCOMPLETE_OR_EARLY | 19 |


All date-level reasons and missing-minute counts are in [missingness_exclusions.csv](../../artifacts/C/preliminary_RV_profile_v1_1/missingness_exclusions.csv). At least 300 full days across 2 years were required before analysis; both branches exceed this gate.

The 7 incomplete ordinary sessions are 2016-02-02 (9 missing minutes),2019-08-12 (30),2020-03-09/12/16/18 (14 each),2021-05-05 (5). Their 100 missing minutes are not imputed; several are major crisis dates. Consequently completeness selection is nonrandom, and this result concerns the eligible cohort, not all crisis sessions. Missing bars may reflect trading interruptions as well as provider coverage; no cause was established here. Early-close rows are rejected by calendar before price analysis and their additional source minutes are deliberately not retained; their missing-grid counts are not a claim of provider failure.

## Exact statistical object and state rules

For a 390-minute session, r[0]=log(C09:30/O09:30); r[j]=log(C[j]/C[j-1]) for j=1,...,389. Each increment is assigned to the five-minute bin containing its bar start. Thus 09:34 belongs to09:30–09:35; 09:35 to09:35–09:40; 15:54 and15:55 are in distinct final bins. No overnight term, no return spanning a missing minute, no borrowing an extra first-bin return. rv[d,k]=sum of five squared minute logs, RV_day=sum of 78 rv, q[d,k]=rv[d,k]/RV_day. The plotted mean is **mean of daily ratios**, not ratio of group RV totals. There is no square root or log transform of the state in P0.

RV_open=sum of first 6 bins (09:30–10:00). This overlaps the first six outcomes and is **RETROSPECTIVE_DESCRIPTIVE**, not an available-at-open forecast. RV_prev is RV_day of the immediately prior scheduled exchange session. Missing/incomplete/early-close predecessors invalidate PREV; we never leap to an older full session or inherit B's prior-full rule. Prior data may inform the state but not today's scientific target. Whole-sample, branch-specific terciles use stable(value,date) order and label=floor(3*zero-based-rank/N). Fixed labels are exhaustive/disjoint for each branch; full-sample descriptive cuts are unsuitable for an untouched predictive claim.

| branch | state | n |
| --- | --- | --- |
| OPEN | low | 497 |
| OPEN | middle | 497 |
| OPEN | high | 497 |
| PREV | low | 491 |
| PREV | middle | 491 |
| PREV | high | 490 |


OPEN boundaries: `[{'lower_group_max': 2.4240058767852755e-06, 'upper_group_min': 2.4268936859696e-06, 'tie_split': False}, {'lower_group_max': 5.87432083963739e-06, 'upper_group_min': 5.893814782135056e-06, 'tie_split': False}]`; tied rows: 0. PREV boundaries: `[{'lower_group_max': 1.594454268225785e-05, 'upper_group_min': 1.5981230788703634e-05, 'tie_split': False}, {'lower_group_max': 4.0351235743971525e-05, 'upper_group_min': 4.036774070495583e-05, 'tie_split': False}]`; tied rows: 0. Boundary ties may split by date and are explicitly flagged. Whole-curve comparisons mix different marginal state cohorts unless the matched-date view below is used.

**Approved window resolution:** P0 primary OPEN 09:30–10:00 (bins0:6), MID 12:00–13:00 (30:42), CLOSE 15:30–16:00 (72:78). Per explicit 2026-10-17 user decision, frozen C-spec MID 11:30–13:30 (24:48) and CLOSE 15:00–16:00 (66:78) are supplementary. These unequal-duration shares are fractions of whole-day RV, not comparable per-minute rates. Windows do not exhaust the day and are dependent. C-spec reporting tolerances remain 0.02 for closing-hour/opening share and 0.05 for profile TV; P0 does not claim equivalence or calibrate power to these tolerances.

## Primary numerical contrasts and uncertainty

All estimates below are high-minus-low **fractions** (multiply by100 for percentage points). `effect_daily_SD` divides the contrast by pooled high/low daily within-group SD; it is a descriptive scale comparison, not a predictive effect or test statistic. `whole` is primary q; `remaining` uses rv[6:78]/sum(rv[6:78]) with unchanged original state labels. The latter removes direct numerator overlap with RV_open but not every compositional/state dependence.

| branch | mode | window | summary | lo_5 | hi_5 | lo_10 | hi_10 | effect_daily_SD |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OPEN | whole | OPEN | 0.019457 | 0.00827941 | 0.0304506 | 0.00828496 | 0.032163 | 0.262523 |
| OPEN | whole | MID | -0.000714934 | -0.00684706 | 0.00563588 | -0.00653967 | 0.0048964 | -0.0141803 |
| OPEN | whole | CLOSE | -0.0119644 | -0.0213086 | -0.00293994 | -0.0222774 | -0.00102205 | -0.197442 |
| OPEN | remaining | MID | 0.0013628 | -0.0054371 | 0.00828171 | -0.00505116 | 0.00755933 | 0.0245312 |
| OPEN | remaining | CLOSE | -0.0115976 | -0.0218827 | -0.00112799 | -0.0235507 | 0.000531961 | -0.16841 |
| PREV | whole | OPEN | -0.0220523 | -0.0319275 | -0.0122425 | -0.0316927 | -0.0109376 | -0.305082 |
| PREV | whole | MID | 0.00508117 | -0.00174623 | 0.0112523 | -0.00172057 | 0.0120567 | 0.096562 |
| PREV | whole | CLOSE | 0.00594303 | -0.00246983 | 0.0142292 | -0.00343329 | 0.0152017 | 0.0994707 |
| PREV | remaining | MID | 0.00285086 | -0.00463638 | 0.00962078 | -0.00457877 | 0.010046 | 0.0493705 |
| PREV | remaining | CLOSE | 0.00294517 | -0.007297 | 0.0126351 | -0.00748606 | 0.0136215 | 0.0427754 |


## Supplementary C-spec windows

| branch | mode | window | summary | lo_5 | hi_5 | lo_10 | hi_10 | effect_daily_SD |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OPEN | whole | C_SPEC_MID | -0.000751627 | -0.0106294 | 0.00925359 | -0.0105016 | 0.00803208 | -0.00996694 |
| OPEN | whole | C_SPEC_CLOSE | -0.00414756 | -0.0160679 | 0.0079543 | -0.0173088 | 0.00962865 | -0.0514292 |
| OPEN | remaining | C_SPEC_MID | 0.00453732 | -0.00616591 | 0.0147682 | -0.00616221 | 0.0139295 | 0.0556808 |
| OPEN | remaining | C_SPEC_CLOSE | -0.000994033 | -0.0141952 | 0.0122097 | -0.0149214 | 0.014419 | -0.0112335 |
| PREV | whole | C_SPEC_MID | 0.00348534 | -0.00664217 | 0.0135667 | -0.00741519 | 0.0143454 | 0.0447422 |
| PREV | whole | C_SPEC_CLOSE | 0.0200498 | 0.0092714 | 0.030796 | 0.00839002 | 0.0320587 | 0.256817 |
| PREV | remaining | C_SPEC_MID | -0.0021698 | -0.0129521 | 0.00840621 | -0.0132403 | 0.00877682 | -0.025711 |
| PREV | remaining | C_SPEC_CLOSE | 0.017371 | 0.0056369 | 0.0293666 | 0.00458935 | 0.0306822 | 0.199999 |


## Shape effect magnitudes

| branch | mode | mean_abs_HL | max_abs_HL | sum_abs_HL | TV | sum_HL | top_contrast_ET |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPEN | whole | 0.00106723 | 0.00945412 | 0.0832441 | 0.0416221 | 1.80411e-16 | 15:55 |
| OPEN | remaining | 0.00100268 | 0.0104839 | 0.0721929 | 0.0360964 | 2.09902e-16 | 15:55 |
| PREV | whole | 0.00124385 | 0.00818767 | 0.0970202 | 0.0485101 | 7.45931e-17 | 09:30 |
| PREV | remaining | 0.00123197 | 0.00525059 | 0.0887015 | 0.0443508 | 1.45717e-16 | 15:55 |


Mean/max/summed absolute H−L are computed over 78 bins (72 for remaining); TV=0.5×summed absolute difference. Top contrast bins are exploratory descriptive locations, not a post-hoc aggregated inferential target. The automatic sum(H−L)=0 identity follows from closure and provides no evidence for/against specific time differences.

## Dependence, uncertainty and robustness

Seed 42; 1,000 valid circular date-block draws per branch and block length 5/10. Each draw resamples whole scheduled exchange-date slots jointly across all bins and states, including ineligible and early-close slots marked−1. Invalid slots do not enter group means; they are not filled or collapsed so blocks never jump over internal missing dates. Circular wrapping occurs only at cohort endpoints. Tercile labels/cuts are held fixed, so intervals condition on the observed classification and are not unconditional sample-quantile or causal uncertainty. Bands and window intervals are percentile 95% **pointwise**, not simultaneous/global tests; two block sizes do not establish robustness to all dependence structures. Failed/empty draw counts are in [bootstrap_log.csv](../../artifacts/C/preliminary_RV_profile_v1_1/bootstrap_log.csv).

Within each branch remove ceil(1%×N) largest RV_day sessions, date-tie order fixed, preserving original labels. FULL remains primary and is never overwritten. Median window contrasts are medians of daily window shares, not sums of per-bin medians. Per-bin median curves need not sum to one and are not probability profiles.

| branch | variant | window | summary | sd | n |
| --- | --- | --- | --- | --- | --- |
| OPEN | FULL | MID | 0.0013628 | 0.0555539 | 994 |
| OPEN | FULL | CLOSE | -0.0115976 | 0.0688656 | 994 |
| OPEN | DROP_TOP1 | MID | 0.00146533 | 0.055784 | 979 |
| OPEN | DROP_TOP1 | CLOSE | -0.0135611 | 0.0680314 | 979 |
| OPEN | MEDIAN | MID | 0.000285332 | 0.0555539 | 994 |
| OPEN | MEDIAN | CLOSE | -0.0098426 | 0.0688656 | 994 |
| PREV | FULL | MID | 0.00285086 | 0.0577442 | 981 |
| PREV | FULL | CLOSE | 0.00294517 | 0.068852 | 981 |
| PREV | DROP_TOP1 | MID | 0.0034431 | 0.057986 | 966 |
| PREV | DROP_TOP1 | CLOSE | 0.000882795 | 0.0680475 | 966 |
| PREV | MEDIAN | MID | 0.003668 | 0.0577442 | 981 |
| PREV | MEDIAN | CLOSE | 0.00637871 | 0.068852 | 981 |


Top1% concentration of raw RV (levels, not a measure of normalized shape) and removed counts:

| branch | top1_count | top1_RV_concentration |
| --- | --- | --- |
| OPEN | 15 | 0.224914 |
| PREV | 15 | 0.181132 |


All removed dates/levels are in [top1_dates.csv](../../artifacts/C/preliminary_RV_profile_v1_1/top1_dates.csv); first listed dates:

| branch | date | RV_day | state |
| --- | --- | --- | --- |
| OPEN | 2020-03-17 | 0.00294511 | high |
| OPEN | 2020-03-23 | 0.00254264 | high |
| OPEN | 2020-03-13 | 0.00215883 | high |
| OPEN | 2020-03-19 | 0.00211469 | high |
| OPEN | 2020-03-20 | 0.00166983 | high |
| OPEN | 2020-03-03 | 0.00159884 | high |
| OPEN | 2020-03-25 | 0.00138518 | high |
| OPEN | 2020-02-28 | 0.00126038 | high |
| OPEN | 2020-03-26 | 0.00111845 | high |
| OPEN | 2020-03-10 | 0.000999174 | high |
| OPEN | 2020-03-24 | 0.000886031 | high |
| OPEN | 2020-03-11 | 0.000776993 | high |


## Matched-date comparison

Both branches share1472 outcome dates. This sensitivity retains each branch's original tercile assignment; it does not re-rank on the intersection. High and low members differ across states even on identical outcome dates, so this is not a paired causal state comparison. Low/middle/high state cross-count matrix (OPEN rows, PREV columns): `[[348, 129, 14], [137, 247, 111], [6, 115, 365]]`.

| branch | mode | window | HL | n_low | n_high | matched_dates | labels |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPEN | whole | OPEN | 0.0193247 | 491 | 486 | 1472 | original fixed branch ranks, not reranked |
| OPEN | whole | MID | -0.00109875 | 491 | 486 | 1472 | original fixed branch ranks, not reranked |
| OPEN | whole | CLOSE | -0.0112722 | 491 | 486 | 1472 | original fixed branch ranks, not reranked |
| OPEN | remaining | MID | 0.000920014 | 491 | 486 | 1472 | original fixed branch ranks, not reranked |
| OPEN | remaining | CLOSE | -0.0107552 | 491 | 486 | 1472 | original fixed branch ranks, not reranked |
| PREV | whole | OPEN | -0.0220523 | 491 | 490 | 1472 | original fixed branch ranks, not reranked |
| PREV | whole | MID | 0.00508117 | 491 | 490 | 1472 | original fixed branch ranks, not reranked |
| PREV | whole | CLOSE | 0.00594303 | 491 | 490 | 1472 | original fixed branch ranks, not reranked |
| PREV | remaining | MID | 0.00285086 | 491 | 490 | 1472 | original fixed branch ranks, not reranked |
| PREV | remaining | CLOSE | 0.00294517 | 491 | 490 | 1472 | original fixed branch ranks, not reranked |


## QA and limits

Eight focused tests cover known390-return/78-bin accounting, endpoints/first-open term, DST/holiday/half-day logic, missing/duplicate/order/end-label/invalid/zero cases, immediate predecessors, stable ties, stream byte cap and temporary-output/joint-block reconstruction. A real-data scalar recomputation for one full day per year agrees with the vector kernel. Unique symbol/minute keys, stored session-vs-ET consistency, full grid, positive finite prices, row/group q closure, remaining closure and independently reconstructed ranks were checked. Group means, FULL/drop-top1/median windows and plotted differences reconcile independently from saved daily arrays to1e-10. Both block-length percentile outputs were independently replayed using weighted date counts rather than selected-row means. Images decode, are nonblank, have widths≥1600, correct ET bin ordering/common comparable scales and all three state legends. See [qa_results.json](../../artifacts/C/preliminary_RV_profile_v1_1/qa_results.json). All334 snapshotted prior files, including B artifacts and source references, remain hash-unchanged. A source QA PASS does not prove bar-level market microstructure fidelity or validate the scientific hypothesis.

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

No further model or source acquisition is authorized by these results. Review this screen in the C-design thread before approving a next experiment. Primary implementation files are `preliminary.py`, `profile_audit.py`, `reporting.py` and the thin CLI. Runtime: 3.14.6; packages: `{'numpy': '2.5.4', 'pandas': '3.0.6', 'pyarrow': '23.0.1', 'exchange-calendars': '4.13.2', 'matplotlib': '3.11.2'}`. Successful analysis/QA/plot wall time 165.3s. Source acquisition wall time 85.5s. Final exact output hashes/storage and session commands are recorded separately in the coding-session report.
