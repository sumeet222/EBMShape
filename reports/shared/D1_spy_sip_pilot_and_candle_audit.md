# D1 — Alpaca SIP split-adjusted SPY pilot and candle-quality audit

**Gate: PASS WITH QUALIFICATIONS.** B only; A remained on hold. Acquisition and all required candle-gap accounting passed for the explicitly sampled conditions. A separate D2 acquisition prompt is justified, subject to the qualifications below. This does not certify every session in 2016–2026 or support a predictive/scientific effect claim.

## Pilot selection and coverage

Source: authenticated **Alpaca consolidated SIP**, SPY, `timeframe=1Min`, `adjustment=split`, ascending bar-start timestamps. Dates and diagnostic thresholds were fixed in `config/D1_spy_source.json` before acquisition. The three additional dates below contain **only a prior-close anchor**, not audited complete sessions.

| Sample condition | Whole sessions acquired | Why / calendar and anchor check |
|---|---|---|
| Normal complete trading week | 2026-09-14, 09-15, 09-16, 09-17, 09-18 | Five full sessions; 09-15 overlaps D0 and Massive; no outcome-based date replacement |
| Actual ex-dividend boundary | 2026-09-17, 09-18, 09-21 | Issuer-verified 09-18 event; neighboring full sessions; reuses the week, no second copy |
| Spring DST boundary | 2024-03-08, 03-11 | 09:30 ET = 14:30 UTC before and 13:30 UTC after Sunday 03-10 |
| Early-close boundary | 2024-11-27, 11-29, 12-02 | Thanksgiving 11-28 is closed; 11-29 ends at 13:00 ET (210 expected minutes); ordinary neighbors have 390 |
| Prior-anchor-only inputs | 2024-03-07, 2024-11-26, 2026-09-11 | One 15:59-start split-adjusted candle each; remaining prior anchors already in whole-session set |
| Known split boundary | **NOT TESTED** | No actual split event selected; no assertion that complete split history was verified |
| Older 2016/2019 sessions | No new requests | D0 remains sparse raw-history evidence; no additional adjustment question justified redundant dates |

SPY's **2026-09-18** ex-date is supported by the [issuer distribution listing](https://www.ssga.com/us/en/institutional/resources/documents/etf-dividend-distributions) and the [2026 distribution schedule, page 3](https://www.ssga.com/library-content/products/fund-data/etfs/us/distribution/SPDR_Dividend_Distribution_Schedule.pdf), version 2026-10-14. The listing reports a 1.888834 USD distribution, record date 09-18, payable 10-30. The [NYSE early-close announcement](https://s2.q4cdn.com/154085107/files/doc_news/NYSE-Group-Announces-2024-2025-and-2026-Holiday-and-Early-Closings-Calendar-2023.pdf) confirms 2024-11-29 at 13:00 ET. XNYS was used as the regular U.S. equity session calendar; calendar history is not provider history.

## Comprehensive real-candle audit

**4,110 expected = 4,110 observed unique = 4,110 valid regular-session candles. Missing: 0 (0%). Gap clusters: 0. Largest gap: 0 minutes; timestamps null.** The canonical artifact additionally contains the three valid prior-anchor-only candles, giving **4,113 rows**. These three rows are excluded from whole-session denominators and day-cluster counts.

| Stratum | Sessions | Expected / observed valid | Missing / gap clusters |
|---|---:|---:|---:|
| 2024 March (DST) | 2 full | 780 / 780 | 0 / 0 |
| 2024 November | 1 full + 1 early close | 600 / 600 | 0 / 0 |
| 2024 December | 1 full | 390 / 390 | 0 / 0 |
| 2026 September | 6 full | 2,340 / 2,340 | 0 / 0 |
| Full-session total | 10 | 3,900 / 3,900 | 0 / 0 |
| Early-close total | 1 | 210 / 210 | 0 / 0 |

All of the following are zero: duplicate timestamps, conflicting duplicates, raw ordering violations, timestamp parse errors, invalid OHLC/volume/count rows, zero-volume rows, zero-trade-count rows, missing volume/count fields, outside-session intrusions, and manual-review extremes under the predeclared 5% within-candle-range/adjacent-close-jump thresholds. No clipping, outlier deletion, forward fill or day substitution occurred. Requests themselves excluded after-hours; absence of intrusions is not a survey of the provider's extended-hours stream.

Every absent-run length bin (1, 2–4, 5–9, >=10) is zero. `D1_spy_candle_gap_clusters.csv` and `D1_spy_missing_candles.csv` contain headers and **zero data rows**, not fabricated zero-length gaps. The longest-gap timestamps are null in per-session QA and the aggregate longest-gap record is null; the top-10 list is empty. Missing count equals summed cluster lengths per date and globally. Observed unique timestamps plus missing equals each calendar grid after excluding extras; duplicates never inflate unique-minute counts. The synthetic regression check verifies these invariants with actual missing runs.

Opening completeness: **30/30 valid bars on every one of the 11 sessions**, including the half-day; loss among otherwise eligible full sessions is **0/10 = 0%**, below the fixed 2% escalation threshold. Every full session has all four anchors and all 91 required bar starts (09:30–09:59, 14:59, 15:00–15:59), all 30 late-predictor minutes and all 30 final-target minutes. Overlapping window missing flags and disjoint missing categories both reconcile to zero. Half-day late windows/15:59 are scheduled unavailable and are not counted as missing regular candles.

Incomplete full sessions: **0**. Affected full-session opening-RV days: **0**. Affected full-session scientific closing labels: **0**. Complete full-day rate: **100%**; complete required-window rate among full days: **100%**. Combined primary scientific eligibility: **10 full days**, each one daily cluster; the **11-29 half-day is excluded with `HALF_DAY`** despite complete opening data. No inference treats 4,110 minutes as independent daily observations.

Actual contiguous eligible exchange-session runs are 2024-03-08→03-11 (2), 2024-11-27 (1), 2024-12-02 (1), and 2026-09-14→09-21 (6). Maximum run: **6 eligible sessions**. The intervening half-day breaks primary eligibility. Longest consecutive run of sessions with missing candles: **0**. Unsampled months are coverage interruptions, not within-session candle gaps. All 390 time-of-day missingness rates and each named-window rate are zero; denominators reflect the half-day schedule, not a uniform 390 assumption.

Machine-readable evidence: [per-session QA](../../data/registry/D1_spy_candle_qa_sessions.csv), [gap clusters](../../data/registry/D1_spy_candle_gap_clusters.csv), [missing minutes](../../data/registry/D1_spy_missing_candles.csv), [aggregate QA](../../data/registry/D1_spy_candle_qa_summary.json).

## Scientific anchors and corporate actions

Bar starts are stored as UTC-aware timestamps; ET is derived with ZoneInfo. Full-session anchors are `P10=C09:59`, `P15=C14:59`, `P1530=C15:29`, `P16=C15:59`, and `Pprev` is preceding permissible **full-session** 15:59 close. A 16:00-start candle is not a close anchor. On **2024-12-02**, the D1 prompt's explicit full-session rule selects **2024-11-27 15:59**, skipping the 11-29 early close; no 13:00 close or nonexistent 15:59 was substituted. This extends the elapsed return interval and must remain visible in later analyses.

One actual day, **2024-03-08**, was used only to verify all five named anchors, `r1=P10/Pprev−1`, `r12=P1530/P15−1`, `r13=P16/P1530−1`, and opening RV from the first open→close increment plus 29 close→close increments. An independent NumPy log-difference calculation agrees (absolute tolerance 1e-14; relative 1e-10). Numerical results remain in ignored `actual_anchor_check.json`; tracked [actual-check evidence](../../data/registry/D1_spy_actual_checks.json) contains only QA status. No correlations, state terciles, regression, forecasting or economic metric was calculated. The sealed 2024–2026 dates were accessed for authorized acquisition QA only.

At the ex-dividend boundary, raw and split OHLC agree in **11 tiny diagnostic candles**: 09-17 15:59, 09-18 09:30–09:34 and 09-21 09:30–09:34. The dividend-adjusted 09-17 close is **1.89 USD lower** (ratio to split 0.997521734), while the two subsequent opening windows are unchanged. This is consistent with the confirmed cash distribution and price rounding; dividend adjustment is a different price basis and is never merged into the split-only canonical dataset. No natural ex-dividend price gap was classified as a bad candle. Actual split-event adjustment accuracy remains **NOT TESTED**, distinct from documented mode semantics and successful explicit split requests.

All **11 Alpaca daily SIP split-adjusted aggregates** were returned. Their daily close minus final regular minute close ranges from **−0.045 to +0.100 USD**. Daily trade counts range **233,589–737,848**, exceed regular-minute sums, and all satisfy a diagnostic >=500 condition. Daily price/count aggregation differs from minute aggregation; [Alpaca's documented rules](https://docs.alpaca.markets/us/docs/market-data-faq) distinguish daily versus minute trade conditions and day grouping. Exact trade-level attribution of the observed differences was not established. The prescribed minute anchors remain authoritative; daily fields are not forced to agree, substituted into r1/r13, or claimed TAQ-equivalent.

## Split-adjusted Massive overlap

2026-09-15 was queried with Massive `adjusted=true`, limited to the same regular interval. There are **390 matching minute starts**, with no missing overlap. Comparison tolerance is **0.000001 USD** per OHLC field; this is a reporting tolerance, not a tick-size/trading-cost estimate.

| Field | Maximum absolute difference, USD | Candles outside tolerance |
|---|---:|---:|
| Open | 0.013000 | 2 |
| High | 0.000046 | 1 |
| Low | 0 | 0 |
| Close | 0 | 0 |

These small discrepancies are preserved, with no feed splicing or clipping. They qualify cross-provider OHLC identity and require consistent primary-source use. No independence of their upstream sources or Massive historical-plan depth is asserted. Detailed prices/counts and requests stay in ignored auxiliary files registered by hash.

## Reproducibility, retention and D2 size plan

Dataset: `B_alpaca_sip_SPY_1m_split_D1_v1`. Sole canonical file: `data/canonical/spy_minute/B_alpaca_sip_SPY_1m_split_D1_v1/pilot.parquet`, **152,721 bytes**, **4,113 × 13 columns**, Zstandard-compressed. SHA-256: `065ab7a800749ab73cf62e4afc854891a30f2eb30fdfed513aa3e131411e4cf8`. Schema and restore lineage are in [source manifest](../../data/registry/D1_spy_source_manifest.json). Canonical volume/trade count are int64 for these observed integer values; future fractional source volumes must remain numeric without truncation.

Only one retained whole-session candle representation exists. Whole-session JSON response bytes are hashed in the ignored request ledger and transformed directly to Parquet, not also saved as raw full-day files. Four small daily responses, six small ex-dividend responses, one Massive response, comparisons, actual-anchor check and request ledger occupy **113,892 bytes** in 14 ignored auxiliary files. D0 raw diagnostics were read/referenced and preserved, never relabelled or copied. No separate 91-window, per-year, fold, seed or model-input file was created. No derived scientific daily table exists.

Successful acquisition: **25 HTTP 200 requests**, **491,773 response bytes**, approximately **10.47 s** wall time including throttling. There was one preceding sandbox-blocked first request; it produced no candle artifact and was recovered through approved escalation. Cached runs verify canonical/auxiliary hashes and make **zero HTTP requests**. Dependency setup used Python 3.14.6, exchange-calendars 4.13.2, pyarrow 23.0.1, pandas 3.0.6, NumPy 2.5.4 and tzdata 2026.5; all transitive runtime versions are in `requirements-d1.lock.txt`. The ignored virtual environment is about **243 MB**, separately accounted from the approximately **0.27 MB** of retained canonical/auxiliary data.

[Measured storage projection](../../data/registry/D1_spy_storage_projection.json): XNYS has **2,701 calendar sessions** over 2016-01-04–2026-09-30, including **2,680 full** and **21 early** sessions. These counts do not certify SIP availability or the initial prior anchor. Selecting the pilot's required windows/anchors in memory gives **943 rows / 37,674 compressed bytes**, without retaining a second artifact. Scaling the observed ratio estimates **~9.74 MB** for 243,881 minimal-window/leading-anchor rows, or **~38.97 MB** for full regular-session retention. Partition overhead/compression will differ. Budget a conservative margin (e.g. <100 MB candle/QA/lineage material), measure an initial small partition, and flag unexpected growth before 2 GB. No large acquisition has been run.

D2 must **fetch and audit full sessions** to report complete-grid missingness even if only the approved ~91 minutes/full session are retained afterward. Preserve compact QA and response hashes; avoid retaining both full-day and minimal-window copies. Missing/no-qualifying-trade minutes, if encountered, must remain missing under strict RV/anchor rules, not be filled. Daily auxiliary data may be small/reused but must stay on a separately documented basis.

Fresh clone (authorized account required):

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-d1.lock.txt
.venv/bin/python -m pip install -e .
.venv/bin/python -B -m unittest discover -s tests -p 'test_d1_candles.py' -v
.venv/bin/python -B scripts/d1_spy_pilot.py --dry-run
# Export APCA_API_KEY_ID, APCA_API_SECRET_KEY and optionally MASSIVE_API_KEY privately.
.venv/bin/python -B scripts/d1_spy_pilot.py
```

Use `--data-root` or `EBM_DATA_ROOT` for an external authorized store. The script loads **environment values only**; the session launcher loaded the existing `.env` into the process environment privately. On Windows use the corresponding `.venv/Scripts/python` path. Copied tracked manifests without the ignored data do not constitute a restored dataset: use a new data root for an authorized reconstruction; vendor revisions can produce different hashes. Do not delete original manifests or overwrite a conflicting dataset identity.

License inspection: [Alpaca terms](https://files.alpaca.markets/disclosures/library/TermsAndConditions.pdf) describe personal/noncommercial use and sharing restrictions; separate subscriber/account terms still apply. Raw licensed values remain ignored and no redistribution is authorized. No account, subscription, secret, scientific split or protocol was changed.

## Test verdict, uncertainties and next gate

Two focused deterministic tests **PASS**: one missing-opening/two-cluster/15:29/duplicate/order invariant case; one calendar/DST/half-day/prior-full-anchor/formula/temporary-Parquet smoke case. Actual-sample equation and independent RV check **PASS**. Cached acquisition reruns **PASS with zero network calls**. Pyarrow emitted sandbox CPU-cache sysctl warnings while all Parquet operations passed; these are recorded in the session report. General multi-year provider integrity, actual split-event handling and source-era fidelity remain untested.

There is no observed missingness to characterize as isolated or extended, and no evidence that a gap clusters at opening/close in this pilot. This small, purposeful selection cannot establish random missingness or guarantee full-history rates. The daily/minute price differences and minor OHLC cross-feed discrepancies remain documented qualifications, not concealed failures or a basis for changing scientific anchors.

**D2 is justified as a separate, explicitly authorized acquisition stage.** It should freeze the source/config, cover the approved 2016-start modern branch through 2026-09-30, handle the leading prior-close boundary honestly, repeat comprehensive session/window/gap QA, enforce the >2% opening-loss stop rule, and retain one compact source. No model fitting, original-era replication, A work or full acquisition is authorized or performed here.
