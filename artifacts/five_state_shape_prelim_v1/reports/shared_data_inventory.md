# Shared data inventory and final coverage

Stage0 inspected sources before downloads and froze the union. Exact paths/hashes/schemas are in `../manifests/source_registry.json` and `validated_inputs.json`. No prior analytical results were reused.

| source | period | reuse | purpose |
| --- | --- | --- | --- |
| Existing LOCAL_SPY_1M | 2016–2021 | 6annual base +72missing-key month supplements | P01 synchronous market; P02 RV389; P05 event prices |
| Existing HF_MINUTE_A cache | 2019 | 12observed partitions, BAC/KO only | P01/stockP02, no fill proxies |
| New HF_MINUTE_A selected | 2019 | 12months, remaining8stocks; one source pass | same shared minute union |
| Existing LOCAL_OBSERVED_30M | 2024-09-26–2025-09-25 analyzed | 10original raw files from99roster, metadata schema2 | P04 stock price returns and observed volume |
| New HF_ETF_DAILY | 2021-05-12–2025-09-25 selected | one pinned daily file; SPY/IEF | P03 O-C and P04 SPY control |
| New FED_RATES | 2021-04-01–2023-12-29 | DGS2/DGS10 CSV once each | P03 prior-available spread; current vintage |
| New FED_SHOCKS | 2016–2021 screened | published raw MPS workbook + official times | P05; chart values used only for units QA |

## Actual observed-minute support

| symbol | observed_sessions | complete_390_sessions |
| --- | --- | --- |
| BAC | 252 | 247 |
| DHR | 252 | 39 |
| HCA | 252 | 6 |
| HON | 252 | 50 |
| IP | 252 | 27 |
| KLAC | 252 | 6 |
| KO | 252 | 228 |
| LOW | 252 | 139 |
| ORCL | 252 | 223 |
| SLB | 252 | 242 |
| SPY | 1499 | 1492 |

No missing minute is filled. HCA/KLAC have only6complete sessions; there are0common complete dates across all ten stocks. P01 pooled beta remains interpretable only for its observed unbalanced panel; the cross-stock dispersion comparison is withheld. P02 fixed downside-share tails and P05 negative events fail frozen shape-support minima. No data-dependent universe replacement was made.
