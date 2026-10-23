# Shared feature QA

{
  "tables": {
    "daily_rv_semivariance": {
      "rows": 2699,
      "columns": [
        "symbol",
        "date_et",
        "RV",
        "RS_minus",
        "RS_plus",
        "q_down",
        "n_return_intervals",
        "source_id",
        "observed",
        "is_imputed",
        "large_minute_move",
        "available_at",
        "open",
        "close",
        "volume",
        "event_return_bp",
        "pre_event_return_bp",
        "event_start_reference",
        "event_end_reference",
        "previous_session",
        "next_session",
        "lag_RV",
        "next_session_RV",
        "log_RV",
        "lag_log_RV",
        "next_log_RV",
        "next_target_available_at"
      ],
      "schema": "symbol: large_string\ndate_et: large_string\nRV: double\nRS_minus: double\nRS_plus: double\nq_down: double\nn_return_intervals: int64\nsource_id: large_string\nobserved: bool\nis_imputed: bool\nlarge_minute_move: bool\navailable_at: large_string\nopen: double\nclose: double\nvolume: double\nevent_return_bp: double\npre_event_return_bp: double\nevent_start_reference: large_string\nevent_end_reference: large_string\nprevious_session: large_string\nnext_session: large_string\nlag_RV: double\nnext_session_RV: double\nlog_RV: double\nlag_log_RV: double\nnext_log_RV: double\nnext_target_available_at: large_string\n-- schema metadata --\npandas: '{\"index_columns\": [], \"column_indexes\": [], \"columns\": [{\"name\":' + 3351",
      "input_frequency": "daily"
    },
    "market_returns_5m": {
      "rows": 104760,
      "columns": [
        "symbol",
        "date_et",
        "bin_start_minute_ET",
        "bin_end_utc",
        "return_5m_log_bp",
        "clock_state",
        "source_id",
        "n_genuine_intervals",
        "observed"
      ],
      "schema": "symbol: large_string\ndate_et: large_string\nbin_start_minute_ET: int64\nbin_end_utc: large_string\nreturn_5m_log_bp: double\nclock_state: large_string\nsource_id: large_string\nn_genuine_intervals: int64\nobserved: bool\n-- schema metadata --\npandas: '{\"index_columns\": [], \"column_indexes\": [], \"columns\": [{\"name\":' + 1175",
      "input_frequency": "5min"
    },
    "daily_stock_returns_volume": {
      "rows": 2470,
      "columns": [
        "symbol",
        "date_et",
        "open",
        "close",
        "volume",
        "source_id",
        "adjustment",
        "observed",
        "stock_return_bp",
        "stock_next_return_bp",
        "next_session",
        "relative_log_volume",
        "prior20_count",
        "state_available_at",
        "target_available_at",
        "spy_oc_bp"
      ],
      "schema": "symbol: large_string\ndate_et: large_string\nopen: double\nclose: double\nvolume: double\nsource_id: large_string\nadjustment: large_string\nobserved: bool\nstock_return_bp: double\nstock_next_return_bp: double\nnext_session: large_string\nrelative_log_volume: double\nprior20_count: int64\nstate_available_at: large_string\ntarget_available_at: large_string\nspy_oc_bp: double\n-- schema metadata --\npandas: '{\"index_columns\": [], \"column_indexes\": [], \"columns\": [{\"name\":' + 2024",
      "input_frequency": "daily"
    },
    "daily_spy_treasury_returns": {
      "rows": 664,
      "columns": [
        "date_et",
        "ief_oc_bp",
        "spy_oc_bp",
        "source_id",
        "session_open",
        "rate_observation_date",
        "DGS2",
        "DGS10",
        "available_at",
        "yield_spread_pp",
        "macro_source_id"
      ],
      "schema": "date_et: large_string\nief_oc_bp: double\nspy_oc_bp: double\nsource_id: large_string\nsession_open: timestamp[us, tz=UTC]\nrate_observation_date: large_string\nDGS2: double\nDGS10: double\navailable_at: timestamp[us, tz=UTC]\nyield_spread_pp: double\nmacro_source_id: large_string\n-- schema metadata --\npandas: '{\"index_columns\": [], \"column_indexes\": [], \"columns\": [{\"name\":' + 1470",
      "input_frequency": "daily"
    },
    "daily_etf_oc_controls": {
      "rows": 1099,
      "columns": [
        "date_et",
        "ief_oc_bp",
        "spy_oc_bp",
        "source_id"
      ],
      "schema": "date_et: large_string\nief_oc_bp: double\nspy_oc_bp: double\nsource_id: large_string\n-- schema metadata --\npandas: '{\"index_columns\": [], \"column_indexes\": [], \"columns\": [{\"name\":' + 555",
      "input_frequency": "daily"
    },
    "fomc_events": {
      "rows": 54,
      "columns": [
        "event_id",
        "date_et",
        "release_time_source",
        "published_MPS_percentage_points",
        "surprise_bp",
        "official_1400",
        "sheet_1400",
        "standard_1400",
        "source_id",
        "event_return_bp",
        "pre_event_return_bp",
        "eligible",
        "exclusion_reason"
      ],
      "schema": "event_id: large_string\ndate_et: large_string\nrelease_time_source: large_string\npublished_MPS_percentage_points: double\nsurprise_bp: double\nofficial_1400: bool\nsheet_1400: bool\nstandard_1400: bool\nsource_id: large_string\nevent_return_bp: double\npre_event_return_bp: double\neligible: bool\nexclusion_reason: large_string\n-- schema metadata --\npandas: '{\"index_columns\": [], \"column_indexes\": [], \"columns\": [{\"name\":' + 1715",
      "input_frequency": "event"
    }
  },
  "holds": {},
  "complete_rv_days": 2699,
  "minute_days_checked": 4019
}

Every derivative is unique-keyed and source-hash bound; no missing minute is filled. New RV389 intentionally differs from old C RV390. Calendar-adjacent next/previous labels never jump over ineligible sessions. Rates use next federal-business-day17:00 assumed publication plus strict prior-open join; current vintage and historical revision uncertainty remain explicit. Stock volume is native observed volume, not a filled/imputed series or share turnover.
