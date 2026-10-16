# D2.1b — Bounded Hugging Face extraction and optional SPY repair

**PARTIAL — PASS WITH QUALIFICATIONS.** Following the user's authorization to access up to **500 MB** and delete unnecessary temporary files, actual targeted extraction recovered **39 of the 104 original missing minutes**, retained in a **21,994-byte optional overlay**. **65 missing minutes in six clusters remain.** Original Alpaca D2 files and its default source definition remain unchanged. The composite restores primary eligibility on **2019-08-12 and 2019-08-13**, raising eligible full days from **2,673 to 2,675**. All **683 sealed-test full days** remain unchanged. No Stage1 model, response regression, hypothesis test or production RV/return table was created; Experiment A stayed on hold.

This follow-up supersedes the earlier *metadata-only feasibility outcome for the new optional composite*, not its historical record. The prior [D2.1 report](D2_1_huggingface_missing_candle_repair.md) and all fifteen preexisting untracked files remain byte-for-byte unchanged. Increasing the cap did not require using 500 MB: the selective method used only **26.00 MB new HF data**, plus **8,421 bytes of Alpaca reference responses**.

## Source, access and actual extraction

Used [valtermedeiros/ohlcv](https://huggingface.co/datasets/valtermedeiros/ohlcv/tree/ae15a75b073e7f6be4ef6563dcb94e98d6add0f4), pinned revision **ae15a75b073e7f6be4ef6563dcb94e98d6add0f4**, file **1m/stocks/SPY.parquet**, row group **1**. It is public and declares **MIT** in its card. That explicit declaration is the stated basis for limited **private research** extraction and the optional local composite. Upstream market-data redistribution rights were **not independently established**; no raw prices are published/tracked, and no exact SIP/source-replication claim follows. The earlier conservative metadata-only stop was re-evaluated for a bounded private empirical comparison; source licensing was not presumed resolved by the larger byte allowance.

P1 `mito0o852/OHLCV-1m` still lacks a declared license and was not downloaded. P3 remains manually gated and was not accessed. No new source search, subscription, paid access or gated acceptance occurred.

The remote stock file is **49,735,075 bytes**. Two footer ranges plus seven column-chunk ranges transferred **26,001,770 measured body bytes**: **25,995,298 selected column bytes + 6,464 footer + 8 trailer**. This is genuine selective row-group transfer; unrelated groups were not downloaded. A sparse temporary Parquet held only the selected original offsets and metadata, logical size49,735,075 / allocated31,485,952 bytes. It was **deleted immediately after extraction**, along with its task-created directory:

`data/cache/D2_1b_l9398lhs/selected_row_group.parquet`

Retained only **562 genuine candidate-context records ×7 source columns**, **21,368 bytes**, at `data/raw/diagnostics/D2_1b_hf_SPY_gap_context.parquet` (ignored). They cover the eight original missing dates, exact candidate minutes and ±20-minute comparison contexts under ET/UTC clock hypotheses, plus an independent pre-terminal segment. The source timestamps remain naive in this diagnostic extract. There are **zero duplicate naive timestamps, zero null required columns and zero zero-volume rows**. Source labels: **475 pitrading, 87 iex**. No resampling, interpolation or synthetic candle generation occurred in our extraction. Historical tick/trade provenance is not independently verified; acceptance is explicitly a qualified source-composite sensitivity.

Alpaca reference data were reused from original canonical windows wherever present. Only three isolated **SIP / split / 1Min** requests supplied nonretained neighbors: **2016-02-02 10:59–11:47 ET**, **2019-08-12 14:35–14:54 ET**, and **2023-06-05 10:00–10:15 ET**. Returned **76 rows**, stored once in a **7,476-byte ignored diagnostic Parquet**. No full-session/history redownload. One initial request failed401 because the implementation unpacked the credential dictionary into field names; passing the existing dictionary directly fixed that code error. Three subsequent requests succeeded with real configured credentials; secrets were never printed. The failed request and correction remain in the sanitized ledger.

## Clock and adjustment reconciliation

The dataset card's generic UTC assertion is inconsistent with the actual timezone-naive `datetime` schema. For accepted **pitrading** rows, paired prices and matched minute-return patterns empirically establish **America/New_York bar-start labels with zero minute shift**, covering both **EST (February2016)** and **EDT (August2019)**. UTC and ±1-minute alternatives were evaluated solely as data alignment diagnostics, never to improve a scientific response. With an all-overlap diagnostic scale, ET zero-shift p95 matched-return errors are **1.032bp** (2016) and **0.402bp** (2019); shifted ±1-minute alternatives are approximately **12.7–13.0bp** and **10.5–10.7bp**, respectively, while UTC offers at most one matched original close. Full hypothesis metrics are retained, including rejected-source rows; no unjustified fixed-hour shift was applied.

Original vendor adjustment semantics remain undocumented. Accepted prices use a transparent **local multiplicative HF→Alpaca alignment** from the **median of20 pre-gap matched close ratios per date**, without missing candles or later scientific target outcomes. Factors:

- **2016-02-02:** **1.1124043414626832**, calibrated10:59–11:18ET; independent post-gap20 closes validate it. Matched ratio variance **2.6284e−9**, relative ratio SD **0.570bp**; median HF/Alpaca volume ratio **0.973**.
- **2019-08-12:** **1.0386572821294104**, calibrated15:09–15:28ET, common to both closing gaps. Independent separated14:35–14:54ET20 closes plus the available15:31ET bar validate it. Matched ratio variance **9.7507e−9** for the first local window; relative SD **1.026bp**, median volume ratio **0.943**.

These are **estimated data-alignment factors**, not asserted known split or dividend factors. The same factor multiplies O/H/L/C; volume is unchanged. No additive offset, per-candle fit, return tweaking, target-sign selection or cross-provider overwrite. The predeclared minimum10 matches, median close error≤2bp, p95 close error≤5bp and p95 matched-return error≤8bp were unchanged. All accepted rows have positive finite internally consistent OHLC and positive finite volume. We additionally screened all four OHLC p95 level errors≤5bp and required at least10 independent validation overlaps. This is an engineering screen, not proof of scientific equivalence.

## Per-cluster decisions and diagnostics

All provider attempts here are P2/HF stock SPY; P1/P3 retain prior metadata/access blockers. Price columns below are **matched local close discrepancy median / p95 / maximum**, in bp after the pre-gap calibration; the last number is p95 consecutive matched-minute log-return difference in bp. Counts describe real extracted rows, not file listings. No calibration is used to create a fill where no genuine aligned observation exists.

| Cluster ET, bar starts | Original missing | Candidate rows | Accepted | Overlap count; close median/p95/max bp; return p95 bp | Decision |
| --- | ---: | ---: | ---: | --- | --- |
| 2016-02-02 11:19–11:27 | 9 | 9 | 9 | 40; 0.335 / 1.169 / 2.067; 1.032 | Accepted local alignment |
| 2019-08-12 15:29–15:30 | 2 | 2 | 2 | 41; 0.121 / 0.486 / 5.652; 0.402 | Accepted local alignment |
| 2019-08-12 15:32–15:59 | 28 | 28 | 28 | 38; 0.127 / 0.921 / 5.652; 0.413 | Accepted; one-sided terminal uncertainty |
| 2020-03-09 09:35–09:48 | 14 | 0 | 0 | not available | Unavailable under aligned ET clock |
| 2020-03-12 09:36–09:49 | 14 | 0 | 0 | not available | Unavailable under aligned ET clock |
| 2020-03-16 09:31–09:44 | 14 | 0 | 0 | not available | Unavailable under aligned ET clock |
| 2020-03-18 12:57–13:10 | 14 | 0 | 0 | not available | Unavailable under aligned ET clock |
| 2021-05-05 11:27–11:31 | 5 | 0 | 0 | not available | Unavailable under aligned ET clock |
| 2023-06-05 09:52–09:55 | 4 | 4 | 0 | 39; 2.800 / 6.900 / 9.787; 10.587 | Rejected: levels and returns fail; clock remains uncertain |

**One-sided terminal review:** The2019-08-12 15:32–15:59 cluster has no same-session right neighbor. Its independent pre-gap segment and terminal OHLC/positive volume/nonconstant price path were checked. The only intervening original15:31 bar differs by **5.652bp close /6.026bp high**; these **maxima** exceed5bp, while p95 and matched-return screens pass. This exception is preserved, not hidden or replaced. At the15:31→15:32 join the mixed-feed close step is **+4.209bp**, versus **−1.442bp** in HF alone. This was reviewed as a qualified boundary discrepancy rather than a gross discontinuity, and all28 rows carry **one_sided_terminal_gap=true**. The two preceding missing bars use the same factor; the original15:31 Alpaca candle remains untouched. Greater source uncertainty remains at the closing target, so the repaired view is a sensitivity source, not a silent principal-source correction.

**June2023 rejection:** Four IEX-labeled candidate rows were extracted but rejected. Under ET zero-shift and the20-pregap factor1.0395216886305416, median close error **2.800bp**, p95 **6.900bp**, p95 matched-return difference **10.587bp** fail the declared2/5/8bp limits. Volume median is only **1.862%** of Alpaca's. UTC/±1 clock diagnostics do not establish a permissible alternative basis (e.g. UTC zero-shift all-overlap-scaled p95 close error13.491bp). No alternate factor/clock was selected to manufacture acceptance. Its opening RV day remains ineligible.

The apparent UTC-clock “coverage” at crisis timestamps was actually different afternoon pitrading observations. Accepted pitrading clock validation prevents mistaking those for restored opening bars. No bars exist at the correct ET missing timestamps on March9/12/16/18,2020 or May5,2021 in this extracted source. No halt or missingness cause is asserted from absence alone.

## Original versus explicitly selected composite

| Quantity | Immutable Alpaca-only D2/default | Optional composite |
| --- | ---: | ---: |
| Expected regular minute starts |1,049,610|1,049,610|
| Observed regular minutes, saved source audit plus accepted keys |1,049,506|1,049,545|
| Missing minutes / maximal clusters / affected dates |104 /9 /8|65 /6 /6|
| Complete full sessions /2,680 |2,672|2,674|
| Complete91 required-window sessions |2,675|2,676|
| Missing required-window minutes |76|46|
| Complete opening30 inputs |2,676|2,676|
| Valid15:29 /15:59 anchors |2,679 /2,679|2,680 /2,680|
| Valid preceding-full-session close |2,678|2,679|
| Primary-eligible full days |2,673|2,675|
| Train /validation /sealed-test eligible |1,493 /497 /683|1,495 /497 /683|
| Early-close exclusions /leading-anchor exclusion |21 /1|21 /1|
| Physical original rows |243,804|same original +39-row delta|
| In-memory source-view rows |243,804|243,843|

Restoring2016's nine midday bars improves full-session completeness but creates **no new eligible scientific day**. Restoring2019's30 closing bars makes2019-08-12 eligible and restores the preceding-full-session close for2019-08-13: **two newly eligible train days**, not30 new observations. **No opening-RV day was recovered.** Remaining full-day primary exclusions:2016-01-04 leading prior close and2020-03-09/12/16,2023-06-05 incomplete opening RV.21 early closes remain excluded. All683 sealed full days and **every original price/counter/source field** in the composite are unchanged.

All65 remaining minutes are explicitly listed in [remaining keys](../../data/registry/D2_1b_hf_remaining_candles.csv). Remaining clusters:

| Date | Missing interval ET | Length |
| --- | --- | ---: |
|2020-03-09|09:35–09:48|14|
|2020-03-12|09:36–09:49|14|
|2020-03-16|09:31–09:44|14|
|2020-03-18|12:57–13:10|14|
|2021-05-05|11:27–11:31|5|
|2023-06-05|09:52–09:55|4|

Largest remaining cluster **14 minutes**, four ties exactly as above. Accounting: **104=39accepted+4rejected+61unavailable**; all43 actual candidate rows had valid OHLCV, but validity alone did not qualify the four rejected IEX rows. No duplicates accepted or discarded. All104 original keys have tracked decisions.

## Storage, loader and verification

Patch: `data/patches/B/B_spy_hf_repair_D2_1b_v1.parquet`, **39 rows ×30 columns,21,994 bytes**, SHA-256 **3eba48d0e6bc684de07ecc55a0bea4a48dcc037afc550f527757cf6be2147b44**. It records original remote URI/revision/group, raw-context hash, range-manifest hash, empirical timestamp method, factor/ratio variance, status and source origin. `trade_count` and `vwap` remain nullable float64 missing—not fabricated Alpaca measurements. Primary price/RV inputs remain usable; any volume/trade-count analysis must preserve this provenance and missingness.

The optional [loader](../../src/ebm_research/experiment_b/repair.py) reads one original store and a tiny accepted delta; it writes no complete composite copy:

```python
from pathlib import Path
from ebm_research.experiment_b.repair import load_minutes
original = load_minutes()  # default Alpaca only:243804 rows
composite = load_minutes(repair_manifest=Path('data/registry/D2_1b_hf_repair_manifest.json'))
```

Use `data_root=...` or `EBM_DATA_ROOT` for authorized external data. Original source and missing-registry hashes, patch checksum, acceptance status, exact originally missing keys, UTC/pre-test membership, OHLCV and strict original-key collisions are verified. Duplicate/unaccepted/unknown/colliding keys raise; originals are never overwritten. Two real composite loads were frame-identical. The default view stayed243,804 rows. Real mechanical required/opening/prior-key counts independently reproduce2,675 composite eligible days. All32 original registered D2 files and all15 preexisting untracked files remain hash-identical.

**Tests7/7 PASS** (two small tests added this session; existing five reused). They cover known multiplicative-factor math without synthetic vendor observations, matched-minute return calculations, unchanged volume, collision/unknown/duplicate rejection, plus existing DST/gap/candle/hash tests. The final loader hash-check addition passed the suite again. No model fitting or broad framework.

**Resources:** New HF26,001,770 +new Alpaca8,421 =**26,010,191 bytes** measured response bodies. Including the earlier D2.1 metadata: **27,717,910 bytes**, ~5.54% of500MB. Wire/TLS/headers/unread401body are unmeasured. Nine HF requests; four Alpaca attempts including the failed-header request, three successful. HF extraction4.892s wall/0.397s CPU; successful neighbor invocation2.084s wall; failed invocation0.642s; final complete mechanical loader QA7.615s. Code runtimes, including the few local comparison reruns, are comfortably below15min. No package installed. Peak source temporary logical49.735MB /allocated31.486MB; **no source temporary file remains**. Retained price artifacts total **50,838 bytes** (21,368 raw context +7,476 references +21,994 overlay). Small code/QA/reports add modest storage; exact final new bytes are in the session report. Original~8.98MB canonical is untouched.

## Stage handoff

**PASS WITH QUALIFICATIONS for partial recovery.** Default/principal source remains **Alpaca-only D2** unless a later Stage1 instruction explicitly predeclares the optional composite as principal or sensitivity before financial results are inspected. The composite changes the source definition through39 locally aligned pitrading bars, carries a one-sided terminal-source caveat and does not establish exact SIP/source-era replication or upstream redistribution rights. It must be reported separately. Do not spend the unused budget on broad replacement history or lower thresholds to fill the remaining65 minutes. [Detailed session report](../sessions/20261016_1437_B_D2_1b_hf_repair.md).
