# D2.1 — Targeted Hugging Face missing-candle recovery

**Decision: NO FEASIBLE SOURCE under the verified access/provenance conditions. Implementation and audit: PASS WITH QUALIFICATIONS. Use the existing 2,673 eligible Alpaca-only days.** This is an abstention, not evidence that no Hugging Face file contains the missing prices. No candidate price rows were extracted or compared; none were accepted. No patch or composite view was created, and no original D2 candle was altered. Experiment A remains on hold. No Stage 1 features, models, scientific outcomes or test returns were calculated.

The starting workspace was clean, branch `main`, commit `cbe397abaa425a94cdacb9384cec80b8378ac684`. The default repository `data/` root was active; no `EBM_DATA_ROOT` override was configured. All 32 registered original D2 files (11 annual canonical Parquets, 11 QA blocks, nine published QA outputs and the request ledger) passed size/SHA-256 verification. The D2 source manifest hash remains `54b450c1e67442a94f5497b50640a96aed155221779a256239cf727354d02fae`. Its frozen config and scientific-spec hashes also match.

## Predeclared screening and acquisition bounds

[Configuration](../../config/D2_1_hf_repair.json) was written before candidate outcomes were inspected. Acceptance would require genuine positive internally valid OHLC and finite nonnegative volume, aware UTC minute starts, exact original-missing keys, no collision with an Alpaca observation, sufficient provenance/rights and a defensible price basis. The screening defaults remain at least **10 neighboring matched closes**, median absolute level discrepancy **≤2 bp**, p95 level **≤5 bp**, and p95 matched log-return discrepancy **≤8 bp**. No thresholds were lowered. Calibration would require independently justified multiplicative alignment; none was estimated. Missing observations were never interpolated, shifted, inferred from returns or fabricated.

Caps were 300 MB network, 150 MB simultaneous temporary disk, five relevant monthly files, three candidate datasets and about 15 minutes of purposeful inspection/acquisition code. Only **one monthly footer** and one instrument footer were examined; no candle pages or full files were downloaded. Public access does not establish upstream redistribution rights. No gated acceptance, purchase or subscription was attempted.

## Sequential provider evidence and stop decisions

| Source | Exact observed evidence | Decision / prerequisite |
| --- | --- | --- |
| P1: [mito0o852/OHLCV-1m](https://huggingface.co/datasets/mito0o852/OHLCV-1m/tree/776328445b7ac6e7815ef3a483e9c8ded1eb6d56) | Revision `776328445b7ac6e7815ef3a483e9c8ded1eb6d56`; public API/card. All five requested month paths appear in listing. Card attributes Finnhub and says UTC minute starts; no license key or license/terms/notice file. | **R1: RIGHTS UNVERIFIED**. No candle extraction. June footer also shows ineffective row-group pruning; default all-candidate-group transfer exceeds cap. |
| P2: [valtermedeiros/ohlcv](https://huggingface.co/datasets/valtermedeiros/ohlcv/tree/ae15a75b073e7f6be4ef6563dcb94e98d6add0f4) | Revision `ae15a75b073e7f6be4ef6563dcb94e98d6add0f4`; public, card `license: mit`. Genuine listed **stock-specific path** `1m/stocks/SPY.parquet`, distinct from `1m/crypto/SPY.parquet`. Actual footer has `datetime` with **isAdjustedToUTC=false / no timezone**, capitalized OHLC, int64 Volume and `source`. Source statistics span `pitrading` and `iex`. | **R2: ABSTAIN—SOURCE CONTRACT UNRECONCILED**. Card's UTC/generic schema does not establish actual naive-clock semantics, bar-start labeling, raw versus adjusted prices, genuine nonfilled observation lineage or upstream source rights. No timezone or scale was guessed. Stock path alone does not validate exact ETF identity or any requested candle. |
| P3: [HaiwenWang/sp500-pit-benchmark](https://huggingface.co/datasets/HaiwenWang/sp500-pit-benchmark) | Revision `58aacebb76471042682d1a460dc324ae8f875bf2`; public API `gated=manual`; listed `spy/spy_minute.parquet`; anonymous README **HTTP401**. No configured HF token, standard cached token/stored-token file or authorized grant verified. | **R3: INELIGIBLE—GATED**. No restricted data request, access acceptance or return-to-OHLC reconstruction. Exact SPY schema and accessible license cannot be verified through this access. |

Repository metadata was requested sequentially P1→P2→P3. P3's public gate check occurred after P2's card/file listing and before the P2 footer follow-up; no candidate candle extraction began at any point. This minor inspection-order detail changed no acceptance rule. No alternative replacement history, Kaggle, mirror, Massive or Schwab was queried. Alpaca was not queried: there was no permissible candidate to compare with, so neighbor acquisition would have served no repair decision.

P1's `data/ohlcv_2023-06.parquet` is **332,444,106 bytes**, footer **22,687 bytes**, **26,538,286 rows in 26 row groups**. HTTP206 suffix and exact-footer reads succeeded. Schema is UTC-nanosecond timestamp, float64 OHLCV and string ticker. **All 26 ticker min/max intervals encompass SPY**, so standard statistics cannot eliminate a group. Candidate compressed column bytes sum **332,421,407** (not a measured extraction), exceeding 300 MB even before other requests. Ticker-only column chunks total **237,984 bytes**; a more sophisticated ticker-first/page selection might cost less, but was **not demonstrated or attempted after the rights gate**. Range access alone does not prove affordable SPY extraction. SPY inclusion remains unverified. Monthly file availability is metadata evidence, not exact missing-minute availability.

P2's stock instrument is **49,735,075 bytes**, with **2,248,701 rows / three groups**, footer **6,464 bytes**. All column chunks total **49,728,599 bytes**. Actual naive `datetime` min/max and `source` statistics:

| Group | Min datetime | Max datetime | Source statistics |
| --- | --- | --- | --- |
| 0 | 2002-12-30 09:30 | 2014-01-29 09:39 | pitrading only |
| 1 | 2014-01-29 09:40 | 2025-02-06 13:54 | iex…pitrading |
| 2 | 2025-02-06 13:55 | 2026-09-11 15:54 | iex only |

All repair dates lie inside group 1's **range**, whose compressed columns total **25,995,298 bytes**. This would be affordable; cost did **not** disqualify P2. Range endpoints do not prove each target date/minute exists. The history actually begins in 2002, showing why the advertised global range was not treated as instrument coverage. `09:30` naive earliest time is a warning about the UTC claim, **not proof of an ET conversion**. A bare MIT card does not document historical vendor adjustment or upstream market-data permissions. Resume only after reliable source-specific clock/bar/adjustment and rights evidence is supplied; an independent overlap audit could then establish alignment before accepting any price. There is no claim that P2 prices failed the numerical screening thresholds; they were not inspected.

## Every unresolved cluster

Providers attempted below means **metadata/contract inspection**, not actual per-cluster price retrieval. R1–R3 are the source gates above. Candidate rows zero means **not extracted**, not zero rows in the remote file. Price-error/return-error/factor/dispersion fields in the comparison CSV are null, not zero.

| Session ET | Bar-start interval ET | Missing | Providers attempted | Candidate rows retrieved | Accepted | Reason | Scientific eligibility after attempt |
| --- | --- | ---: | --- | ---: | ---: | --- | --- |
| 2016-02-02 | 11:19–11:27 | 9 | P1/P2/P3 metadata gates | 0 | 0 | R1/R2/R3 | Already eligible; unchanged |
| 2019-08-12 | 15:29–15:30 | 2 | P1/P2/P3 metadata gates | 0 | 0 | R1/R2/R3 | Ineligible; unchanged |
| 2019-08-12 | 15:32–15:59 | 28 | P1/P2/P3 metadata gates | 0 | 0 | R1/R2/R3 | Ineligible; unchanged |
| 2020-03-09 | 09:35–09:48 | 14 | P1/P2/P3 metadata gates | 0 | 0 | R1/R2/R3 | Ineligible; unchanged |
| 2020-03-12 | 09:36–09:49 | 14 | P1/P2/P3 metadata gates | 0 | 0 | R1/R2/R3 | Ineligible; unchanged |
| 2020-03-16 | 09:31–09:44 | 14 | P1/P2/P3 metadata gates | 0 | 0 | R1/R2/R3 | Ineligible; unchanged |
| 2020-03-18 | 12:57–13:10 | 14 | P1/P2/P3 metadata gates | 0 | 0 | R1/R2/R3 | Already eligible; unchanged |
| 2021-05-05 | 11:27–11:31 | 5 | P1/P2/P3 metadata gates | 0 | 0 | R1/R2/R3 | Already eligible; unchanged |
| 2023-06-05 | 09:52–09:55 | 4 | P1/P2/P3 metadata gates | 0 | 0 | R1/R2/R3 | Ineligible; unchanged |

The 15:32–15:59 cluster is explicitly **ONE_SIDED_TERMINAL_GAP**. No same-session right neighbor exists after 15:59; none was invented. Its unresolved close also keeps **2019-08-13** ineligible through the preceding-full-session anchor rule. No daily close was substituted. No local level/log-return/volume comparison, boundary-price judgment, calibration or RV-value computation was performed without candidate candles.

## Original versus empty-overlay accounting

All counts below were recomputed from the original gap/session CSVs, with the accepted-key set empty. Original maximum consecutive clusters were regenerated from exact UTC keys and compared with all nine saved intervals and lengths. All 104 ET/UTC keys agree through ZoneInfo. A key-only read of the original 11 partitions verifies 243,804 unique keys and that **none** of the 104 missing instants exists in the retained original store. Missing nonretained midday bars remain distinct from bars absent merely because D2 intentionally retained 91 windows.

| QA quantity | Original D2 | After attempt (no overlay) |
| --- | ---: | ---: |
| Expected regular candles, including scheduled early-session portions | 1,049,610 | 1,049,610 |
| Observed regular candles (saved D2 full-session audit) | 1,049,506 | 1,049,506 |
| Missing minutes / maximal clusters / dates | 104 / 9 / 8 | 104 / 9 / 8 |
| Largest remaining cluster | 28; 2019-08-12 15:32–15:59 ET | unchanged |
| Full sessions / complete full sessions | 2,680 / 2,672 | 2,680 / 2,672 |
| Complete required 91-window sessions | 2,675 | 2,675 |
| Required missing minutes | 76 | 76 |
| Complete opening-30 inputs among full days | 2,676 | 2,676 |
| Valid 15:29 / 15:59 anchors among full days | 2,679 / 2,679 | 2,679 / 2,679 |
| Valid preceding-full-session anchor | 2,678 | 2,678 |
| Primary eligible full days | 2,673 | 2,673 |
| Train / validation / sealed eligible | 1,493 / 497 / 683 | 1,493 / 497 / 683 |
| True restored minutes / newly eligible days | 0 / 0 | 0 / 0 |
| Excluded scheduled early closes | 21 | 21 |
| Retained canonical rows / bytes | 243,804 / 8,975,163 | unchanged |

Seven full dates remain excluded: **2016-01-04** (pre-sample prior close, separate from the 104), **2019-08-12** (closing gaps), **2019-08-13** (missing preceding close), and **2020-03-09/12/16, 2023-06-05** (incomplete opening RV). Full-session completeness and scientific eligibility are different. Noncritical midday gaps did not invalidate primary days and cannot be counted as recovered scientific observations. All **683/683 full sealed-test days, 2024-01-01–2026-09-30**, are unchanged. The same XNYS half-day skip and missing ordinary-full-close rules remain in force.

Observed D2 full-day counts are reused from hash-verified QA because discarded midday prices were never retained. There was no repeat multi-year download or re-audit of discarded price bodies. This stage independently checked hashes, key uniqueness and gap/accounting invariants; it did **not** independently recalculate all million source-bar OHLC checks or validate HF price quality.

## Artifacts, tests and costs

- [Repair manifest](../../data/registry/D2_1_hf_repair_manifest.json): original hashes, source revisions/gates, config/script hashes, environment, resources and full remaining-cluster/exclusion lists.
- [Per-minute decisions](../../data/registry/D2_1_hf_repair_decisions.csv): exactly 104 unresolved original keys. [Per-cluster comparisons](../../data/registry/D2_1_hf_repair_comparisons.csv): nine records, null unperformed discrepancy metrics, all rejection gates.
- Metadata evidence: `data/registry/D2_1_hf_candidate_1.json`, `_2.json`, `_2_instrument.json`, `_3.json`, `D2_1_hf_instrument_stats.json`, and retained sandbox failure evidence.
- **No patch Parquet, composite loader, patched annual replica or derived daily table** was created. A usable repaired loader and scale-calibration implementation would be premature when the required stop gates prohibit patching. Their proposed tests are skipped, explicitly; the original default reader/source contract is unchanged. A future approved repair must implement explicit opt-in, exact-missing-key validation and strict original-row collision rejection, with nullable unobserved trade_count/vwap.

**Tests: PASS 5/5**, command `.venv/bin/python -B -m unittest discover -s tests -p 'test_d*_*.py' -v`. Four reused D1/D2 checks cover calendar/anchors, candle endpoints, immutable conflicts and page overlap; one new deterministic gap-accounting check covers ET/UTC bar starts across DST, same-session consecutive grouping and duplicate-key rejection. Offline real-data audit passed; D2 `--verify-only` confirms all 11 years with zero network calls. The audit was rerun to verify repeatable counts and then to correct metadata-temp accounting; decision/comparison bytes remained stable. No models, financial tests or synthetic calibration algorithm were added.

**Network:** **1,707,719 measured HTTP response-body bytes (~1.71 MB)**. Twelve external requests (11 successful, one HTTP401) plus one sandbox DNS failure; no transient retry loops. TLS/headers/redirects and unread HTTP401 body are not measured and are not falsely reported as exact wire traffic. **No candle rows or full monthly/instrument files downloaded.** Probe-level purposeful code wall time totals **3.861 s**, CPU **0.308 s**, excluding process startup/imports, approvals and assistant work. The final offline key/hash audit takes about half a minute; all acquisition and audit code is comfortably below the 15-minute budget. Retained new evidence/code/reports is approximately **1.7 MB**, measured precisely in the session report. No source-data temporary file; peak atomic metadata `.tmp` about **1.313 MB** (within 150 MB). Existing environment reused; no installation. Free disk at audit about **62.67 GB**. The 300 MB cap was never approached.

The sandbox's initial DNS denial was retained as evidence and retried with explicit approved network escalation. P3's HTTP401 was respected. A read-only summary command encountered `AttributeError` on the absent gated README; it affected no source or decision and was corrected with guarded metadata inspection. Arrow emitted known nonfatal CPU-cache sysctl permission warnings; checks passed.

## Next safe action

Proceed only under a **separate Stage 1 instruction predeclaring Alpaca-only D2 as principal source**, using 2,673 eligible days and the documented missingness exclusions. D2.1 changes no source definition because it produced no overlay. A future accepted HF overlay would instead be an explicitly named **source-composite sensitivity dataset**, never a silent correction to the locked Alpaca-only baseline. To resume repair, first obtain reliable timestamp/adjustment/provenance and rights evidence for P2, or an appropriate grant for a source with sufficient genuine OHLCV; do not re-download these public metadata artifacts or infer authorization from an open URL. No scientific decision or threshold was changed, and no hypothesis conclusion follows from this audit.
