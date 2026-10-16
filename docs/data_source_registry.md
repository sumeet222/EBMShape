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
