# Data-source registry — D0, 16 October 2026 (America/New_York)

Evidence: `data/registry/d0_*` JSON; individual raw-response paths, sizes and SHA-256 hashes are in `data/registry/d0_file_manifest.json`. Access conclusions are limited to these requests, not inferred full coverage.

| Provider / experiment | Configured and observed | Coverage / rights / decision |
|---|---|---|
| WRDS CRSP / A | No WRDS environment keys, `.pgpass`, `.pg_service.conf` or `.netrc`; no authenticated connection | **BLOCKED**. CRSP remains preferred scientific candidate, not a verified-access recommendation. Need authorized WRDS account, CRSP subscription/schema access and historical/current release coverage |
| WRDS Compustat + CCM / A optional controls | No configured access; no SQL run | Need separate permissions, historical accounting fields and dated security links. Controlled Table IV unavailable |
| Alpaca SIP / B | Nonempty `APCA_API_KEY_ID`, `APCA_API_SECRET_KEY`; five HTTP 200 full sessions, four adjustment requests, five prior-close pairs | Preferred **verified diagnostic primary**. Dates below; continuous history/source-era entitlement unverified; account-specific storage/redistribution rights not certified |
| Massive / B | Nonempty `MASSIVE_API_KEY`; HTTP 200 for 2026-09-15, 882 extended-session bars, all 390 regular minutes | Verified **recent diagnostic backup**. Plan name/Basic status and historical limit not inferred from key or one success |
| HF `mito0o852/OHLCV-1m` / B historical candidate | Public metadata/tree/card HTTP 200; four-byte range HTTP 206 | 411 monthly files, 1992-01–2026-03 only; no September 2026 file. SPY inclusion **not verified**; filter request timed out. No declared license found; Finnhub attribution alone does not authorize redistribution. Not approved primary/backup |
| Kaggle candidates / B | Public metadata and file manifests HTTP 200; no credentials and no data downloads | See below. Historical candidates only; provenance, timezone and adjustments unresolved |
| Schwab / B | No configured credential names or supplied token cache in repository | Not contacted. Need existing authorized app credentials/token and documented historical depth; no OAuth or subscription initiated |

## Observed Alpaca coverage (SIP, raw, SPY, one-minute bar starts)

| Current session | Prior close diagnostic session | Regular rows | Opening rows | First–last ET |
|---|---|---:|---:|---|
| 2016-01-05 | 2016-01-04 | 390 | 30 | 09:30–15:59, UTC−05 |
| 2019-07-15 | 2019-07-12 | 390 | 30 | 09:30–15:59, UTC−04 |
| 2023-07-17 | 2023-07-14 | 390 | 30 | 09:30–15:59, UTC−04 |
| 2024-07-15 | 2024-07-12 | 390 | 30 | 09:30–15:59, UTC−04 |
| 2026-09-15 | 2026-09-14 | 390 | 30 | 09:30–15:59, UTC−04 |

Each full session is sorted, unique, has zero missing/extra regular minute starts and zero OHLCV integrity violations; no continuation token. Each prior-date request has 15:59 and 16:00 starts; only 15:59 close is the intended full-session anchor. All 390 overlapping September minute **closes** match Massive exactly; this does not establish equality of all fields or independent upstream provenance.

Adjustment probes cover only 2024-07-15 09:30–09:34 ET. First-minute close: raw=split=562.11; dividend=all=547.73. This demonstrates that dividend adjustment changes prices and must not be silently selected. It does not validate corporate-action processing across the archive. Alpaca documents the options in [historical bars](https://docs.alpaca.markets/us/reference/stockbars); Massive documents split-only adjustment in [Custom Bars](https://massive.com/docs/rest/stocks/aggregates/custom-bars).

## Hugging Face pinned inventory

Revision `776328445b7ac6e7815ef3a483e9c8ded1eb6d56`, repository last modified 2026-05-03T16:22:10Z. Observed monthly Parquet bytes sum to **87,719,544,647** (~87.72 GB); individual files 21,681,088–496,670,752 bytes. The tree contains 414 entries including directory and ancillary files. Card summary `download_size=60,116,469` is inconsistent with this manifest and must not drive budgeting.

The [dataset card](https://huggingface.co/datasets/mito0o852/OHLCV-1m) attributes source data to Finnhub and describes reformatted monthly tar archives, UTC bar starts and ticker/OHLCV fields. Adjustment policy, original extraction lineage, SPY completeness and rights remain unestablished. The card's displayed example says streaming but omits `streaming=True`; do not execute it as an acquisition recipe.

A pinned March 2026 object accepted `Range: bytes=0-3` and returned HTTP 206, 4 bytes, `PAR1`. Thus partial byte retrieval works. Actual SPY predicate extraction was **not demonstrated**: dataset-server filtering timed out after 20 seconds, and the viewer reports incompatible split formats. Future authorized footer/row-group inspection could select columns and prune groups; without ticker clustering/stats it may still scan most bytes. Sequential streaming/filtering could avoid whole-file retention while still transferring whole files. Neither proves efficient SPY-only network acquisition. No Parquet or archive was downloaded.

## Kaggle metadata-only candidates

| Dataset | Declared scope and manifest files | Observed size | License/provenance caveat |
|---|---|---:|---|
| [rockinbrock/spy-1-minute-data](https://www.kaggle.com/datasets/rockinbrock/spy-1-minute-data) | 2008–2021; `spy_1min_2008_2021_cleaned.csv` | 134,194,334 file bytes; search reports 23,207,040 | Other; uploader claims public-domain research/education. No upstream provider or cleaning audit |
| [gratefuldata/intraday-stock-data-1-min-sp-500-200821](https://www.kaggle.com/datasets/gratefuldata/intraday-stock-data-1-min-sp-500-200821) | Describes 2.07m SPY rows, 2008–2021; `1_min_SPY_2008-2021.csv` | 145,508,228 file bytes; search 38,107,429 | CC0 declared; description says mixed sources without identifying them |
| [cesarecastro/cleaned-spy-and-qqq-1-minute-data](https://www.kaggle.com/datasets/cesarecastro/cleaned-spy-and-qqq-1-minute-data) | `clean_SPY.csv`, `clean_QQQ.csv`, combined CSV, metadata JSON | SPY 1,378,002; total 6,216,514 file bytes; search 1,544,896 | CC0 declared; no description/date coverage established; combined file duplicates the separate inputs |

Search/list size differences likely reflect compressed versus expanded content, but that explanation was not verified. No candidate supplies verified September 2026 data. Uploader license labels are not proof of upstream redistribution rights. No Kaggle archive or CSV downloaded.

## A field-access checklist and prerequisites

The [official WRDS CRSP overview](https://wrds-www.wharton.upenn.edu/demo/crsp/form/) describes security identity, prices/volumes, distributions, delistings and historical shares. This is product documentation, **not this user's entitlement**. Once secure login and dataset permissions exist, inspect `information_schema.columns` and select **one security and at most two months** after discovering actual schema/table names. Avoid full-table `COUNT`/`MIN`/`MAX` scans initially.

Verify PERMNO/PERMCO, dated ticker/share/exchange/SIC codes, RET/RETX, PRC, VOL, SHROUT, adjustment factors, distribution amount/type/date, DLRET/DLSTCD and historical eligibility. Classic candidate tables `msf`, `msenames`, `msedist`, `msedelist` may be replaced by newer CIZ schemas: discover permissions and semantics first. Derive cap from documented price/share units or reconcile vendor cap. Inspect Compustat annual inputs and CCM dated links separately; do not claim point-in-time vintage from ordinary annual values alone. Latest September 2026 availability is unknown. No A data or schema permissions have been verified, and no scientifically compatible backup was found.

## Access and licensing boundaries

API success establishes access to the requested rows only. Existing account agreements were not available for inspection. Provider terms and exchange subscriber agreements remain applicable; no public redistribution is authorized here. [Alpaca's disclosure library](https://alpaca.markets/disclosures) lists exchange subscriber agreements; [Massive terms](https://massive.com/legal/terms) are the applicable starting reference. Store all samples locally under Git ignores; do not publish them. No purchase, new account, token refresh or login automation was performed.


## D1 evidence update — 16 October 2026

D0 observations above remain unchanged. D1 status is **PASS WITH QUALIFICATIONS** for the bounded split-adjusted SPY pilot; A remains on hold. Manifest: `data/registry/D1_spy_source_manifest.json`; candle statistics: `D1_spy_candle_qa_sessions.csv`, `D1_spy_candle_gap_clusters.csv`, `D1_spy_missing_candles.csv`, `D1_spy_candle_qa_summary.json`.

Alpaca SIP `adjustment=split` now has actual whole-session evidence for 2024-03-08, 2024-03-11, 2024-11-27, 2024-11-29 (early close), 2024-12-02, and 2026-09-14/15/16/17/18/21. All 4,110 expected regular candles are present and valid; missing clusters=0. Three extra requested anchor-only rows on 2024-03-07, 2024-11-26 and 2026-09-11 are valid. No continuous-history completeness claim follows.

The [issuer distribution listing](https://www.ssga.com/us/en/institutional/resources/documents/etf-dividend-distributions) identifies SPY's 2026-09-18 ex-date, record date 2026-09-18 and payment date 2026-10-30; the [2026 distribution schedule](https://www.ssga.com/library-content/products/fund-data/etfs/us/distribution/SPDR_Dividend_Distribution_Schedule.pdf), version 2026-10-14, page 3, supports the ex-date. The pre-event 15:59 close is unchanged between raw and split, but is 1.89 USD lower under the dividend query (rounded price adjustment); five opening prices on ex-date and the following session match across those modes. Raw/split OHLC agree in all 11 diagnostic bars. This is dividend-treatment evidence, **not a tested split boundary**; split QA remains NOT TESTED on an actual event.

The [NYSE announcement](https://s2.q4cdn.com/154085107/files/doc_news/NYSE-Group-Announces-2024-2025-and-2026-Holiday-and-Early-Closings-Calendar-2023.pdf) supports the 2024-11-29 13:00 ET early close. XNYS has 210 expected minutes; the target is absent by schedule and is excluded, without forward fill. March DST samples map 09:30 ET to 14:30 UTC before and 13:30 UTC after the transition.

Massive `adjusted=true` on 2026-09-15 returned 390 matching regular starts. Close and low match Alpaca exactly; **two opens** differ by more than the reporting tolerance of 0.000001 USD (maximum 0.013 USD), and **one high** differs (maximum 0.000046 USD). These are recorded discrepancies, not grounds to merge feeds or assert independent provenance. The tolerance is a diagnostic reporting threshold, not an inferred trading tick or a reason to clip data.

All 11 Alpaca daily split-adjusted bars are available with trade counts >=500. Daily close minus final regular minute close ranges **−0.045 to +0.100 USD**; daily counts exceed summed regular-minute counts. The [Alpaca aggregation FAQ](https://docs.alpaca.markets/us/docs/market-data-faq) documents distinct minute/daily condition rules and day grouping; these explain why equality should not be forced, but exact trade-level attribution was not investigated. B keeps its specified minute-price anchors. Counts are diagnostic and not TAQ-equivalent source filtering.

[Alpaca's public terms](https://files.alpaca.markets/disclosures/library/TermsAndConditions.pdf) describe personal/noncommercial use and restrictions on sharing content; account/exchange-specific agreements still apply. D1 retains licensed candles and price/count comparisons only in ignored local storage. No credentials/subscriptions changed; no license to publish raw bars is inferred.


## D2 verified full-period source — 16 October 2026

**Alpaca consolidated SIP, SPY, 1Min, adjustment=split is the sole authoritative B full-history provider.** D2 completed all 2,701 XNYS sessions requested for **2016-01-04–2026-09-30**, including 2,680 full and 21 early-close sessions. Every calendar month completed retrieval; unknown/whole-empty sessions=0. The optional 2015-12-31 15:59 anchor returned no bar, so 2016-01-04 is excluded from primary r1; first eligible day is 2016-01-05. No broader pre-2016 entitlement/coverage claim follows.

Full regular-session audit: **1,049,610 expected, 1,049,506 observed/valid, 104 absent**, nine maximal gaps across eight dates. Largest is 28 minutes on **2019-08-12 15:32–15:59 ET**. Source reasons remain unknown (no qualifying bar versus provider gap not independently identified). Four full days lack strict opening RV inputs; one lacks closing endpoints, its successor lacks prior close, and the initial day lacks the pre-sample anchor. Primary-eligible full days are **2,673**: **1,493 train / 497 validation / 683 sealed test**. Half-days are separately excluded. Opening losses are below 2%; Stage 1 is permitted as a separate task on documented eligible days, without power or effect claims.

Dataset **B_alpaca_sip_SPY_1m_split_D2_v1** has **11 annual Parquets, 243,804 rows, 8,975,163 bytes**. Full sessions were audited before retaining only 09:30–09:59, 14:59 and 15:00–15:59 bar starts. The manifest indexes immutable source/QA hashes and request lineage. D0/D1 remain preserved historical diagnostics; D1 is not a second authoritative full-period source. D2 made **271 HTTP200 requests, 222,454,942 response bytes, no HTTP failures/retries**, with no new Massive, WRDS, HF, Kaggle or Schwab request. A remains on hold.

Read `reports/shared/D2_full_spy_sip_acquisition_and_candle_quality.md`, `data/registry/D2_spy_source_manifest.json` and `D2_spy_candle_qa_sessions.csv` before using the source. Complete month/year/quarter and gap/time-of-day evidence are registered. Daily SIP/split count flags are available and >=500 on all sessions; minute prices remain authoritative. Existing D1 daily/cross-feed differences and actual split-event limitations are carried forward, not rechecked or silently fixed. All acquisition is modern-only; no Gao 1993–2013 TAQ replication or financial result is claimed. Licensed candles stay ignored/private under existing account/exchange terms.
