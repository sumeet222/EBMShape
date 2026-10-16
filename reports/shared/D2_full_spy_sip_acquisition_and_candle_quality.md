# D2 — Full SPY SIP acquisition, candle-quality audit and canonical freeze

**Task:** B_D2_FULL_ALPACA_SIP_HISTORY_AND_CANDLE_QA. **Gate: PASS WITH QUALIFICATIONS. Stage 1 is permitted as a separate future task on the documented eligible data.** No models, scientific/predictive correlations, state thresholds, hypothesis tests or trading evaluation were run. Experiment A remained on hold.

## Exact source and coverage

Primary source is authenticated **Alpaca consolidated SIP / SPY / 1Min / explicit adjustment=split**. Requested **2016-01-04–2026-09-30 inclusive**; all **2,701 scheduled XNYS sessions** were successfully retrieved and audited: **2,680 full and 21 early-close sessions**. Calendar counts match D1's projection; they were independently enumerated rather than asserted. There are **zero unknown/unretrieved sessions and zero successfully retrieved whole sessions with no candles**. The final 2026 year intentionally stops at September 30; no unexpected partial month/year was found.

Observed retained bounds are **2016-01-04 14:30:00 UTC** through **2026-09-30 19:59:00 UTC** (09:30 and 15:59 ET respectively). The optional **2015-12-31 15:59 ET** prior anchor query returned HTTP200 with zero bars. Thus **2016-01-04 is retained but ineligible for r1**; first primary-eligible session is **2016-01-05**. This does not establish the provider's entire pre-2016 archive boundary. No prior price was invented and no other provider was used.

D1's 11-date pilot and historical reports remain immutable diagnostics. Those few overlapping dates were reacquired within D2's contiguous monthly requests, avoiding fragmented request logic and establishing a consistent new extraction lineage. D1 rows were not concatenated/copied into D2, and D1 is not a second authoritative full-history dataset.

The [Alpaca bars documentation](https://docs.alpaca.markets/us/reference/stockbars) supports explicit feed/adjustment selection, inclusive query boundaries and continuation-token pagination. First January batch returned every expected regular minute and page/range checks passed before scaling. Monthly API spans also return extended-hours bars between the endpoints: **1,053,001 such rows were explicitly identified and discarded before regular-session QA**, with per-batch counts. They are not unexpected missing/extra regular candles. Every included regular bar retained its genuine UTC bar start; ZoneInfo and XNYS determine ET session boundaries and DST.

## Complete year coverage and retained partitions

| Year | Sessions (full / early) | Expected RTH candles | Observed = valid | Missing | Gap clusters | Eligible full days | Retained rows / bytes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2016 | 252 (251 / 1) | 98,100 | 98,091 | 9 | 1 | 250 | 22,841 / 785,927 |
| 2017 | 251 (249 / 2) | 97,530 | 97,530 | 0 | 0 | 249 | 22,659 / 774,109 |
| 2018 | 251 (248 / 3) | 97,350 | 97,350 | 0 | 0 | 248 | 22,568 / 782,288 |
| 2019 | 252 (249 / 3) | 97,740 | 97,710 | 30 | 2 | 247 | 22,629 / 797,568 |
| 2020 | 253 (251 / 2) | 98,310 | 98,254 | 56 | 4 | 248 | 22,799 / 869,578 |
| 2021 | 252 (251 / 1) | 98,100 | 98,095 | 5 | 1 | 251 | 22,841 / 857,427 |
| 2022 | 251 (250 / 1) | 97,710 | 97,710 | 0 | 0 | 250 | 22,750 / 869,271 |
| 2023 | 250 (248 / 2) | 97,140 | 97,136 | 4 | 1 | 247 | 22,564 / 849,491 |
| 2024 | 252 (249 / 3) | 97,740 | 97,740 | 0 | 0 | 249 | 22,659 / 865,357 |
| 2025 | 250 (247 / 3) | 96,960 | 96,960 | 0 | 0 | 247 | 22,477 / 871,110 |
| 2026 | 187 (187 / 0) | 72,930 | 72,930 | 0 | 0 | 187 | 17,017 / 653,037 |

All observed unique regular candles are valid. **1,049,610 expected = 1,049,506 observed/valid + 104 absent.** Missing rate **0.00990844%**, using all scheduled regular minute starts as denominator. Raw observed counts equal unique counts because duplicates=0. No API failure or uncommitted period is converted into a missing-candle count. The 21 scheduled early closes have their correct smaller grids and missing late scientific windows are excluded by schedule, not counted as 180 missing full-day bars.

All of these are zero across the retrieved regular sessions: timestamp parse errors, out-of-order inputs, duplicate timestamps, conflicting duplicates, invalid OHLCV/count rows, zero volume, zero trade count, missing required price/volume/count fields, invalid numeric volume/count, unexpected regular-session extras and review-only >5% candle-range/adjacent-close-jump flags. No clipping, outcome-dependent day selection, interpolation or forward fill occurred.

## Exact missing-candle clusters

There are **104 absent minutes in nine maximal within-session clusters across eight sessions**. **Largest: 28 minutes, 2019-08-12 15:32–15:59 ET (19:32–19:59 UTC)**; there is **one largest-gap tie**. Mean cluster length **11.555556**, median **14**, 95th percentile **22.4 minutes** (linear sample quantile; no inferential claim). Cluster-size bins: **1=0, 2–4=2, 5–9=2, 10–29=5, 30+=0**. All nine clusters, the complete top-20 list, are:

| Session ET | Start–end ET (bar starts) | Length | Affected scientific windows |
| --- | --- | --- | --- |
| 2019-08-12 | 15:32–15:59 | 28 | anchor;final_target |
| 2020-03-09 | 09:35–09:48 | 14 | opening_rv |
| 2020-03-12 | 09:36–09:49 | 14 | opening_rv |
| 2020-03-16 | 09:31–09:44 | 14 | opening_rv |
| 2020-03-18 | 12:57–13:10 | 14 | other |
| 2016-02-02 | 11:19–11:27 | 9 | other |
| 2021-05-05 | 11:27–11:31 | 5 | other |
| 2023-06-05 | 09:52–09:55 | 4 | opening_rv |
| 2019-08-12 | 15:29–15:30 | 2 | anchor;final_target;late_predictor |

Reasons remain `UNKNOWN_NO_QUALIFYING_BAR_OR_VENDOR_GAP`: the returned data alone do not distinguish a no-qualifying-trade interval, market halt or vendor omission. No cause was invented, and no isolated re-query or feed substitution was used to conceal gaps.

Affected-day runs are separate from within-day clusters. **Maximum affected-day run is one exchange session**, with all eight tied dates: 2016-02-02, 2019-08-12, 2020-03-09, 2020-03-12, 2020-03-16, 2020-03-18, 2021-05-05 and 2023-06-05. There are no wholly absent requested dates. The longest contiguous **eligible** exchange-session run is **250 sessions, 2021-11-29–2022-11-23**. Half-days and primary exclusions break eligible runs; weekends/holidays do not. The extra prior-anchor exclusion on 2019-08-13 is an eligibility effect, not a second day with absent candles.

Nonzero month distributions (all other requested months have zero missing candles, with denominators retained in the coverage CSV):

| Period | Missing / expected candles | Missing rate | Clusters | Share of all missing candles |
| --- | --- | --- | --- | --- |
| 2016-02 | 9 / 7,800 | 0.115385% | 1 | 8.6538% |
| 2019-08 | 30 / 8,580 | 0.349650% | 2 | 28.8462% |
| 2020-03 | 56 / 8,580 | 0.652681% | 4 | 53.8462% |
| 2021-05 | 5 / 7,800 | 0.064103% | 1 | 4.8077% |
| 2023-06 | 4 / 8,190 | 0.048840% | 1 | 3.8462% |

Nonzero quarter distributions:

| Period | Missing / expected candles | Missing rate | Clusters | Share of all missing candles |
| --- | --- | --- | --- | --- |
| 2016-Q1 | 9 / 23,790 | 0.037831% | 1 | 8.6538% |
| 2019-Q3 | 30 / 24,780 | 0.121065% | 2 | 28.8462% |
| 2020-Q1 | 56 / 24,180 | 0.231596% | 4 | 53.8462% |
| 2021-Q2 | 5 / 24,570 | 0.020350% | 1 | 4.8077% |
| 2023-Q2 | 4 / 24,180 | 0.016543% | 1 | 3.8462% |

Year distributions and denominator counts appear above; machine summaries also retain the proportions of all clusters and missing bars by year/month/quarter. The complete month CSV covers all **129 requested months**, including zero-gap months; the quarter CSV covers **43 quarters**. No unacquired dates are assigned a numerical candle-loss rate.

## Window-sensitive completeness and scientific eligibility

Disjoint missing categories reconcile exactly: **opening 46 + 14:59 anchor 0 + 15:00–15:29 late predictor 1 + 15:30–15:59 final target 29 + other 28 = 104**. Separate overlapping anchor flags count two absent anchor instants (15:29 and 15:59 on 2019-08-12); these are not added again to the disjoint total. There is no missing 09:59 or 14:59 anchor.

Opening candles account for **44.23%** of absent minutes, final-target candles **27.88%**, the late predictor **0.96%**, other regular minutes **26.92%**. These are shares of absence, not estimates of randomly missing data. Missing opening candles occur on four full sessions; closing gaps on 2019-08-12 compromise both final-target anchors and the next day's prior close. This concentration can select unusual market conditions; missingness is not assumed random.

Per-window actual denominators (including eligible scheduled portions of early sessions): opening **46/81,030** missing; overlapping anchor flags **2/10,741**; late predictor **1/80,400**; final target **29/80,400**; other **28/805,100**. All 390 ET minute-of-day denominators/rates are in the aggregate summary. Named overlapping flags are explicitly marked and need not sum to the full grid; disjoint categories above do.

**Eight full sessions** have at least one missing regular candle. Whole-full-session completeness is **99.701493%**; complete valid 91-window rate among full sessions is **99.813433%**. Scientific eligibility is **2,673/2,680 full sessions (99.738806%)**, a distinct quantity: some noncritical gaps leave primary eligibility intact, while an entirely complete day can lack a usable prior close. The **21 early closes are all excluded from the primary target** and are not counted in the full-session denominator.

| Split | Full-day denominator | Eligible / excluded | Opening-RV loss among otherwise eligible |
| --- | --- | --- | --- |
| train | 1499 | 1493 / 6 | 3 / 1496 (0.200535%) |
| validation | 498 | 497 / 1 | 1 / 498 (0.200803%) |
| sealed_test | 683 | 683 / 0 | 0 / 683 (0.000000%) |

Overall strict opening-RV loss is **4/2,677 otherwise eligible full days (0.149421%)**, below the frozen **2%** stop condition; separate train/validation/test rates above are also below it. The otherwise-eligible denominator requires valid non-RV return endpoints/prior anchor and no invalid candles; the CSV separately reports RV loss among all full days. All four RV-loss days have an available 09:59 endpoint. No criterion/state definition was weakened.

The seven primary-ineligible full sessions are exactly:

- **2016-01-04:** missing pre-sample permissible prior full close.
- **2019-08-12:** missing 15:29 and 15:59 anchors / closing-window minutes.
- **2019-08-13:** its preceding full session 15:59 is absent; no older full-session fallback.
- **2020-03-09, 2020-03-12, 2020-03-16, 2023-06-05:** incomplete opening 30-minute RV input.

Primary-eligible full sessions cover six complete calendar years with no primary exclusion: **2017, 2018, 2021, 2022, 2024, 2025**, in addition to qualified years and the requested partial 2026 year. This exceeds the minimum history screen; it does not establish nonlinear power, common support or any financial effect. The sealed period's **683/683 full days** pass mechanical eligibility; no return patterns or predictive metrics were inspected.

The fixed prior-permissible-**full**-session rule is preserved across **21 full sessions following an early close**. Their elapsed calendar days and the immediately preceding session type are recorded. Shortened days have no 15:59 target; no 13:00 close or after-hours 16:00-start candle is substituted. Missing full-session anchors invalidate r1 rather than invoking the half-day skip rule. Exact definitions remain P10=C09:59, P15=C14:59, P1530=C15:29, P16=C15:59, Pprev=preceding permissible full-session 15:59 close. D2 checks input availability only; production returns and the opening RV formula are deferred to Stage 1.

Alpaca daily SIP split-adjusted trade counts were available on **all 2,701 sessions**, and all have the diagnostic **>=500** flag. This flag does not change primary eligibility or assert TAQ-equivalent counting. D1's daily-versus-minute price/count differences remain advisory provenance; D2 did not force equality, substitute daily prices into minute anchors, or repeat Massive comparisons. Actual split-event correction remains untested; explicit split-only request semantics are preserved and dividend/all-adjusted data are never mixed into the source.

## Canonical freeze, resources and restore

Dataset ID **B_alpaca_sip_SPY_1m_split_D2_v1**, schema version **1**. **Eleven annual Zstandard Parquets, 243,804 actual rows, 8,975,163 bytes (8.975 MB)**. The 2,680 full-session retention grids require 243,880 minute starts; **76 required starts are absent**, retained as absence records rather than fabricated rows. The other **28 missing minutes** fall outside retained windows. Early-close candles were audited and are not retained, since the primary target is unavailable; their QA rows remain. The optional initial anchor is absent and therefore adds zero source rows.

Schema: `symbol`, `timestamp_utc:timestamp[us, UTC]`, `session_et:date32`, OHLC, `volume`, `trade_count`, `vwap` float64, `source_batch`, `role`; sorted stable key `(symbol,timestamp_utc)`. Float64 numeric volume/count preserves any fractional values without integer truncation. Conflicting duplicates would block the affected partition; exact identical duplicates would be counted and removed transparently, but none occurred.

[Source manifest](../../data/registry/D2_spy_source_manifest.json) records each partition and annual QA block's path/size/SHA-256, config/spec/source identity, software versions, execution-code histories, optional anchor, source bounds and freeze time. Dataset freeze: **2026-10-16 17:58:00 UTC / 13:58:00 EDT**. Vendor supplies no immutable release ID: this is a frozen extraction across recorded request times, not a claim of an immutable vendor release. No raw full-day JSON/CSV, second 91-window store, train/test copy, run snapshot or scientific daily table exists. D1 remains a historical pilot, not a competing full-history authority.

Net retained data and QA before report text: **17,522,718 bytes (~17.52 MB)**: canonical **8,975,163**, request ledger **162,322**, resumable per-year QA blocks **7,144,002**, consolidated registries/QA **1,241,231**. The annual QA JSON retains detailed counters for resume; it contains no price rows and is not a duplicate candle source. Code/docs/session report add a small amount. Existing ~243 MB D1 environment was reused; **no new dependency installed**. Initial free disk **64.3072 GB**, later **63.8976 GB**; direct retained-file sizes, rather than unrelated global disk movement, measure D2 growth. Well below the <1 GB target; no 2 GB escalation needed.

API cost: **271 successful HTTP200 requests** (260 minute pages including the optional anchor, plus 11 daily pages; see ledger for exact pagination), **222,454,942 response bytes (~222.45 MB)**, **0 HTTP errors, 0 transient retries/backoffs**. Measured acquisition/QA invocation times **88.888s + 559.300s = 648.188s (~10m48s)**, excluding preparation/approvals/assistant work. Measured HTTP wall time **151.3405s**; configured pacing is 0.5s/request. These are resource counts, not a claimed dollar price/account plan. The first month's measured 61,429 bytes projected ~8.66 MB; final 8.98 MB is consistent with that measured scale.

Whole sessions were audited once during construction, then only required minutes written. Saved QA and response hashes allow cheap counter/integrity review; unused whole-day prices are not retained, so recomputing those discarded-minute audits would require a new authorized vendor retrieval. No cosmetic multi-year re-download/re-audit was performed. Cheap `--verify-only` validates completed immutable data/QA hashes and the committed request-ledger prefix with **zero network calls**. One operational resume defect was found in review: treating the growing request ledger as immutable could reject a legitimately interrupted run. The guard now verifies the committed prefix, accepts appended work and rejects mutation; a tiny regression passes. Downloaded candles/QA were unaffected, and acquisition versus post-freeze maintenance code hashes are distinguished.

Portable commands (Python3.14.6 and existing `requirements-d1.lock.txt`; Windows uses `.venv/Scripts/python`):

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-d1.lock.txt
.venv/bin/python -m pip install -e .
.venv/bin/python -B -m unittest discover -s tests -p 'test_d*_*.py' -v
.venv/bin/python -B scripts/d2_spy_acquire.py --dry-run
# Privately export APCA_API_KEY_ID and APCA_API_SECRET_KEY.
.venv/bin/python -B scripts/d2_spy_acquire.py --max-years 1
.venv/bin/python -B scripts/d2_spy_acquire.py --resume
.venv/bin/python -B scripts/d2_spy_acquire.py --verify-only
```

Use `--data-root PATH` or `EBM_DATA_ROOT` for a portable authorized store. Environment values only are read by the engine; the session launcher privately loaded existing .env values. A public clone does not contain licensed Parquets. Restore matching files/QA from an authorized local backup and verify, or acquire into a new empty data root. A saved manifest without its sources is not a restored dataset. Resume skips completed, hash-verified annual blocks; an unregistered .tmp/orphan, source response revision, key/page conflict or changed immutable checksum requires inspection and is never overwritten. Uncommitted-year coverage is explicitly unknown, not classified as missing candles.

## Evidence, QA limits and handoff

Machine outputs: [sessions](../../data/registry/D2_spy_candle_qa_sessions.csv), [gap clusters](../../data/registry/D2_spy_candle_gap_clusters.csv), [absent minutes](../../data/registry/D2_spy_missing_candles.csv), [invalid instants](../../data/registry/D2_spy_invalid_candles.csv), [aggregate summary](../../data/registry/D2_spy_candle_qa_summary.json), [year](../../data/registry/D2_spy_coverage_year.csv), [month](../../data/registry/D2_spy_coverage_month.csv), [quarter](../../data/registry/D2_spy_coverage_quarter.csv), [exceptions](../../data/registry/D2_spy_exception_log.json). Invalid-instant CSV is header-only; absence files contain exactly 104 minutes and nine clusters. Detailed year checkpoints are indexed in the source manifest.

**Tests PASS 4/4:** reused two D1 fixtures, plus two focused D2 regressions for a complete retrieved empty day versus unknown coverage, exact full-day cluster accounting, immutable hash conflict, append-only ledger resume and page overlap. Full real QA reconciles every session's present+absent=expected, duplicate handling, summed cluster lengths, and global/year/month/window counts. Arrow's known sandbox CPU-cache sysctl warnings were nonfatal; Parquet/hash/I/O checks pass. No broad new test infrastructure, model fit, extra provider, source-era download or A work.

[Alpaca terms](https://files.alpaca.markets/disclosures/library/TermsAndConditions.pdf) and account/exchange agreements apply; this is private noncommercial research access, not permission to redistribute licensed bars. Git ignores candle/source data and credentials. No purchase, subscription, secret, commit or push was changed.

**Stage 1 may proceed only on documented eligible days**, carrying forward missingness selection, initial-anchor, half-day elapsed-time and D1 price-basis qualifications. Its separate future task is one canonical daily table and source-style OLS benchmarks for the modern 2016-start branch. This is **not Gao's 1993–2013 TAQ replication**, a supported EBM relationship, or a trading result. D2 is complete; Stage 1 was not executed.
