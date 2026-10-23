# Five immutable input contracts

| ID | source_ids | frequency | predictor | state | target | independent_unit |
| --- | --- | --- | --- | --- | --- | --- |
| P01_INTRADAY_BETA | ['HF_MINUTE_A', 'LOCAL_SPY_1M'] | 1min | spy_synchronous_5m_log_return_bp | clock_start_ET_early_mid_late | stock_5m_log_return_bp | trading_day |
| P02_SIGNED_RV | ['HF_MINUTE_A', 'LOCAL_SPY_1M'] | 1min | current_log_RV_389 | current_q_down_fixed_thirds | next_session_log_RV_389 | trading_day |
| P03_TREASURY_HEDGE | ['HF_ETF_DAILY', 'FED_RATES'] | daily | SPY_same_day_open_close_log_return_bp | prior_available_DGS10_minus_DGS2_terciles | IEF_same_day_open_close_log_return_bp | trading_day |
| P04_VOLUME_REVERSAL | ['LOCAL_OBSERVED_30M', 'HF_ETF_DAILY'] | 30min | same_stock_current_close_close_log_return_bp | own_log_volume_minus_prior20_mean_log_volume | same_stock_next_session_close_close_log_return_bp | trading_day |
| P05_FOMC_RESPONSE | ['FED_SHOCKS', 'LOCAL_SPY_1M'] | 1min_event | absolute_published_surprise_bp | published_raw_surprise_sign | SPY_standard_1400_1430_log_return_bp | FOMC_event |

Exact config SHA-256s: `../manifests/frozen_configs.json`. Swapped targets, source identities, frequencies and Treasury roles reject before plotting.
