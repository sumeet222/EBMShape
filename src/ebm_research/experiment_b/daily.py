"""Stage 1 daily features on the frozen minute view; no source retrieval or fitting."""
import datetime as dt
import math

import numpy as np
import pandas as pd

from .pilot import ET, UTC, calendar, prior_full


def at(day, clock):
    """Aware UTC bar start from an ET session date and local clock (DST aware)."""
    return pd.Timestamp(f"{day} {clock}", tz=ET).tz_convert(UTC)


def valid_price(bar):
    """Positive, finite, internally consistent OHLC; None is an absent minute."""
    if bar is None:
        return False
    o, h, l, c = (bar[k] for k in ("open", "high", "low", "close"))
    return all(math.isfinite(v) and v > 0 for v in (o, h, l, c)) and l <= min(o, c) <= max(o, c) <= h


def opening_rv(bars):
    """30 consecutive opening bars supplied in order, otherwise NaN; no filling."""
    if len(bars) != 30 or not all(valid_price(b) for b in bars):
        return math.nan
    closes = np.array([b["close"] for b in bars], dtype=float)
    q = np.log(closes / np.r_[bars[0]["open"], closes[:-1]])
    return float(np.sqrt(q @ q))


def build_daily(minutes, config, source_qa):
    """One row per scheduled full XNYS session, including explicit exclusions.

    Input: genuine SPY UTC-start minute OHLCV/count records and D2 QA flags.
    Output: daily anchors, simple returns/bps, opening RV, availability and QC.
    Missing prior full close never triggers an older full-session fallback.
    """
    if minutes.duplicated(["symbol", "timestamp_utc"]).any():
        raise ValueError("Daily input contains duplicate minute keys")
    t = pd.to_datetime(minutes.timestamp_utc)
    if str(t.dt.tz) != "UTC" or not minutes.symbol.eq(config["symbol"]).all():
        raise ValueError("Daily input must be SPY with aware UTC timestamps")
    if (t.dt.second.ne(0) | t.dt.microsecond.ne(0)).any():
        raise ValueError("Minute starts must be exact minutes")
    local = t.dt.tz_convert(ET)
    if not local.dt.date.eq(minutes.session_et).all():
        raise ValueError("Source session_et disagrees with UTC/ET timestamp")
    cal = calendar(config["start"], config["end"])
    qa = source_qa.set_index("session_et")
    records = minutes.to_dict("records")
    lookup = {r["timestamp_utc"]: r for r in records}
    # Calendar lookup per session, rather than repeated per minute (~244k rows).
    bounds = {str(s.date()): (cal.session_open(s), cal.session_close(s))
              for s in cal.sessions_in_range(config["start"], config["end"])}
    by_day = {}
    for r in records:
        day = str(r["session_et"])
        if day not in bounds or not (bounds[day][0] <= r["timestamp_utc"] < bounds[day][1]):
            raise ValueError(f"Minute outside scheduled regular session: {day}")
        by_day.setdefault(day, []).append(r)

    def flagged(b, key):
        return b is not None and pd.notna(b.get(key)) and bool(b.get(key))

    rows = []
    for session in cal.sessions_in_range(config["start"], config["end"]):
        day = session.date().isoformat()
        if cal.session_close(session).tz_convert(ET).strftime("%H:%M") != "16:00":
            continue
        prior = prior_full(cal, day)
        opening_times = list(pd.date_range(at(day, "09:30"), periods=30, freq="min"))
        late_times = list(pd.date_range(at(day, "15:00"), periods=30, freq="min"))
        target_times = list(pd.date_range(at(day, "15:30"), periods=30, freq="min"))
        required = opening_times + [at(day, "14:59")] + late_times + target_times
        bars = [lookup.get(t) for t in opening_times]
        prior_bar = lookup.get(at(prior, "15:59"))
        anchors = {name: lookup.get(at(day, clock)) for name, clock in config["anchors"].items()}
        prices = {name: b["close"] if valid_price(b) else math.nan for name, b in anchors.items()}
        prices["Pprev"] = prior_bar["close"] if valid_price(prior_bar) else math.nan
        n_open = sum(valid_price(b) for b in bars)
        n_required = sum(valid_price(lookup.get(t)) for t in required)
        invalid = sum(not valid_price(b) for b in by_day.get(day, []))
        rv = opening_rv(bars)
        reasons = []
        if not valid_price(prior_bar):
            reasons.append("MISSING_PRIOR_FULL_ANCHOR")
        if n_open != 30:
            reasons.append("INCOMPLETE_OPENING_30")
        if not all(valid_price(b) for b in anchors.values()):
            reasons.append("MISSING_OR_INVALID_CRITICAL_CANDLE")
        if n_required != len(required):
            reasons.append("INCOMPLETE_REQUIRED_91")
        if invalid:
            reasons.append("INVALID_OHLC")
        r1 = prices["P10"] / prices["Pprev"] - 1
        r12 = prices["P1530"] / prices["P15"] - 1
        r13 = prices["P16"] / prices["P1530"] - 1
        repaired = lambda times: sum(flagged(lookup.get(t), "is_repaired") for t in times)
        terminal = any(flagged(lookup.get(t), "one_sided_terminal_gap") for t in required + [at(prior, "15:59")])
        source_row = qa.loc[day]
        skipped = cal.sessions_in_range(prior, day)[1:-1]
        # Provider delivery latency is unobserved: these are earliest bar-completion times.
        early_available = max(opening_times + [at(prior, "15:59")]) + pd.Timedelta(minutes=1)
        late_available = max(late_times + [at(day, "14:59")]) + pd.Timedelta(minutes=1)
        target_available = max(target_times) + pd.Timedelta(minutes=1)
        if early_available > at(day, "10:00") or late_available > at(day, "15:30") or target_available != at(day, "16:00"):
            raise ValueError(f"Feature time leakage for {day}")
        row = dict(symbol=config["symbol"], session_et=dt.date.fromisoformat(day),
                   split="train" if day <= config["train"][1] else "validation" if day < config["sealed_test"][0] else "sealed_test",
                   prior_full_session=dt.date.fromisoformat(prior), prior_elapsed_calendar_days=(dt.date.fromisoformat(day)-dt.date.fromisoformat(prior)).days,
                   skipped_early_sessions=len(skipped), preceding_session_was_early_close=len(skipped)>0,
                   **prices, r1=r1, r12=r12, r13=r13,
                   x_open_bp=config["returns"]["scale_bp"]*r1, w_preclose_bp=config["returns"]["scale_bp"]*r12, y_last30_bp=config["returns"]["scale_bp"]*r13,
                   rv_open_raw=rv, rv_open_log=math.log(rv+config["rv_epsilon"]) if math.isfinite(rv) else math.nan,
                   n_open_minute_bars=n_open, n_required_valid=n_required, invalid_ohlc_rows=invalid,
                   eligible_primary=not reasons, eligibility_reason=";".join(reasons) or "ELIGIBLE",
                   prior_anchor_complete=valid_price(prior_bar), return_anchors_complete=all(valid_price(b) for b in anchors.values()),
                   source_available_at=early_available, early_features_available_at=early_available,
                   late_features_available_at=late_available, target_available_at=target_available,
                   information_time_note="E: X,RV by 10:00 ET; L: W additionally by 15:30; Y complete at 16:00; vendor latency unmeasured",
                   daily_trade_count_available=bool(source_row.daily_trade_count_available), daily_ge500=bool(source_row.daily_ge500),
                   daily_count_basis=str(source_row.daily_count_basis), daily_close_comparison_available=False,
                   price_basis=config["adjustment"], known_ex_dividend_example=day in config["known_ex_dividend_dates"],
                   ex_dividend_status="D1_VERIFIED_EXAMPLE" if day in config["known_ex_dividend_dates"] else "UNKNOWN_NOT_A_COMPLETE_EVENT_REGISTER",
                   repaired_minutes_session=sum(flagged(b,"is_repaired") for b in by_day.get(day,[])),
                   repaired_opening=repaired(opening_times), repaired_late=repaired(late_times), repaired_target=repaired(target_times),
                   repaired_1459=repaired([at(day,"14:59")]), prior_anchor_repaired=flagged(prior_bar,"is_repaired"),
                   terminal_repair_dependency=terminal,
                   source_view="alpaca+source1" if "one_sided_terminal_gap" in minutes.columns else "alpaca")
        for name,b in anchors.items():
            row[name+"_complete"] = valid_price(b)
            row[name+"_repaired"] = flagged(b,"is_repaired")
        row["repaired_other"] = row["repaired_minutes_session"] - sum(row[k] for k in ("repaired_opening","repaired_late","repaired_target","repaired_1459"))
        for col, output in [("volume", "volume_open_30"),("trade_count", "trades_open_30")]:
            vals = [b.get(col, math.nan) if b else math.nan for b in bars]
            row[output] = float(sum(vals)) if n_open==30 and all(pd.notna(v) and math.isfinite(v) and v>=0 for v in vals) else math.nan
        row["r_open_intraday_only"] = prices["P10"]/bars[0]["open"]-1 if valid_price(bars[0]) else math.nan
        row["open_overnight_part"] = bars[0]["open"]/prices["Pprev"]-1 if valid_price(bars[0]) else math.nan
        rows.append(row)
    daily = pd.DataFrame(rows)
    if daily.duplicated(["symbol","session_et"]).any():
        raise ValueError("Duplicate daily session key")
    return daily


def training_rows(daily, config):
    """Slice permitted dates before any regression routine reads outcomes/state."""
    dates = daily.session_et.astype(str)
    return daily.loc[daily.eligible_primary & dates.between(*config["train"])].copy()


def guard_training(frame, config):
    """Reject later dates before the fitting code accesses scientific columns."""
    if frame.empty or not frame.session_et.astype(str).between(*config["train"]).all():
        raise ValueError("Stage 1 regression accepts training dates only; validation/test are sealed here")
    if frame.session_et.duplicated().any() or not frame.session_et.is_monotonic_increasing:
        raise ValueError("Regression needs unique chronologically ordered daily observations")
