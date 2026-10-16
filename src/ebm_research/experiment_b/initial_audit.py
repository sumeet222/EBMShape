"""Offline, training-only raw-bin feasibility audit; no predictive model fitting.

Run ``freeze`` before ``run``. Source files and previous research are immutable.
Intervals describe fixed empirical bands under a circular day-block resampling
scheme; they are neither pointwise conditional-mean nor selective confidence sets.
"""
import argparse
import datetime as dt
import importlib.metadata as metadata
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import time

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from .acquisition import file_ref, verify_files
from .daily import at, guard_training, opening_rv, valid_price
from .pilot import ROOT, ET, calendar, prior_full, sha, write_json
from .repair import merge_overlay

OUT = ROOT / 'artifacts/B/initial_audit'
PROTOCOL = OUT / 'config/initial_audit_protocol_v1.json'
TRAIN = ['2016-01-05', '2021-12-31']
STATES = ['low', 'middle', 'high']
COLORS = ['#0072B2', '#009E73', '#D55E00']
FILENAMES = ['01_scatter_state_lines.png', '02_conditional_means_with_intervals.png',
             '03_raw_XZ_conditional_response_heatmap.png', '04_support_and_state_contrasts.png',
             '05_temporal_and_outlier_robustness.png']
READS = []


def root_data():
    return Path(os.environ.get('EBM_DATA_ROOT', ROOT / 'data')).expanduser().resolve()


def read_json(path):
    return json.loads(Path(path).read_text())


def panel(x, label, unit='bp', state='rv_open_log', facet='ALL', time='15:30'):
    return dict(x=x, label=label, unit=unit, state=state, facet=facet, cutoff=time)


def directions():
    """All attempted variants in fixed order, independent of any response values."""
    return {
        'A2': dict(title='Late momentum × opening RV', panels=[panel('w_preclose_bp', 'W: 15:00–15:30')]),
        'A3': dict(title='Recent momentum and acceleration × opening RV', panels=[
            panel(f'late_return_{h}m_bp', f'Last {h} minutes') for h in [5, 10, 15]] +
            [panel('late_accel_bp', 'Recent 5m minus disjoint earlier 5m')]),
        'A4': dict(title='Overnight gap versus morning intraday × opening RV', panels=[
            panel('gap_bp', 'Overnight gap G', time='10:00'),
            panel('morning_bp', '09:30–10:00 intraday I', time='10:00')]),
        'A5': dict(title='Extreme magnitude and asymmetry × opening RV', panels=[
            panel('x_open_bp', 'Signed opening X', time='10:00'),
            panel('abs_x_bp', '|X|', time='10:00'),
            panel('x_squared_bp2', 'X² (direction removed)', 'bp²', time='10:00'),
            panel('x_centered_squared_bp2', '(X − TRAIN mean X)²', 'bp²', time='10:00'),
            panel('abs_x_bp', '|X| conditional on X < 0', facet='NEGATIVE', time='10:00'),
            panel('abs_x_bp', '|X| conditional on X ≥ 0', facet='NONNEGATIVE', time='10:00')]),
        'A6': dict(title='Late momentum × recent versus opening RV', panels=[
            panel('w_preclose_bp', 'W; recent RV PRINCIPAL', state='rv_late_log'),
            panel('w_preclose_bp', 'W; opening RV COMPARISON')]),
        'B1': dict(title='Downside event probability × opening RV', panels=[
            panel('x_open_bp', 'Opening X — early information', time='10:00'),
            panel('w_preclose_bp', 'Late W — late information')]),
        'B2': dict(title='Late volume × opening RV', panels=[
            panel('late_volume_30m', '15:00–15:30 volume', 'shares'),
            panel('late_volume_5m', '15:25–15:30 volume', 'shares'),
            panel('relative_late_volume', 'Late volume / prior 20 eligible mean', 'ratio')]),
        'B3': dict(title='Lagged full-session momentum × opening RV', panels=[
            panel(f'lag_close_{h}_bp', f'Prior {h}-full-session return', time='10:00') for h in [1, 5, 20]]),
        'C1': dict(title='Fixed-rule decision feasibility — MODEL_DEPENDENT / DEFER', panels=[
            panel('abs_w_bp', '|W|; fixed sign(W) continuation')]),
    }


def freeze():
    """Freeze choices and immutable-input hashes before loading training outcomes."""
    if PROTOCOL.exists():
        raise FileExistsError('Protocol already frozen; inspect it, then use run. Never silently replace it.')
    data = root_data()
    old = read_json(ROOT / 'config/B_stage2A_linear_spline_protocol.json')
    stage1 = read_json(data / 'registry/B_stage1_daily_manifest.json')
    baseline = read_json(data / 'registry/D2_spy_source_manifest.json')
    overlay = read_json(data / 'registry/D2_1c_hf_repair_manifest.json')
    refs = [stage1['daily'], overlay['patch']] + [b['canonical'] for b in baseline['blocks'].values()]
    verify_files(data, refs)
    # Byte hashes of preexisting results do not deserialize scientific values.
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    paths = {ROOT / p for p in tracked if p and (ROOT / p).is_file()}
    paths |= {p for p in (ROOT / 'artifacts/B/checkpoints').rglob('*') if p.is_file()}
    paths |= {data / r['path'] for r in refs}
    snapshot = []
    for path in sorted(paths):
        relative = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else None
        # External data references remain portable relative to EBM_DATA_ROOT.
        snapshot.append(dict(base='repo' if relative else 'data', path=relative or path.relative_to(data).as_posix(),
                             bytes=path.stat().st_size, sha256=sha(path)))
    write_json(OUT / 'registries/start_snapshot.json', dict(
        created_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        branch=subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT).decode().strip(),
        commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip(),
        status=subprocess.check_output(['git', 'status', '--short'], cwd=ROOT).decode(),
        files=snapshot, free_disk_bytes=shutil.disk_usage(ROOT).free))
    p = dict(task_id='B_INITIAL_AUDIT_NINE_REMAINING_EXPERIMENTS_V1', version=1,
             frozen_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(), train=TRAIN,
             daily=stage1['daily'], data_refs=refs, directions=directions(),
             source_id=stage1['dataset_id'], symbol='SPY', timezone='America/New_York',
             adjustment='Alpaca SIP split + exactly 39 D2.1c native missing-key rows; no D2.1b',
             outcome='y_last30_bp = 10000*(C15:59/C15:29-1), signed; available16:00 ET',
             opening_cutoffs_log=old['preprocessing']['cutoffs_log'],
             opening_cutoffs_raw=old['preprocessing']['cutoffs_raw'], rv_epsilon=1e-8,
             new_state='sqrt(log(C15:00/O15:00)^2 +29 adjacent close-log increments through15:29); log(RV+1e-8); own TRAIN terciles',
             features=dict(late_returns='10000*(C15:29/C15:(29-h)-1), h5/10/15',
                           acceleration='last5 -10000*(C15:24/C15:19-1); disjoint intervals',
                           gap='10000*open_overnight_part', morning='10000*r_open_intraday_only',
                           magnitude='abs(X),X²,(X-mean_TRAIN_X)²; sign facets share magnitude bin edges',
                           volume='sum15:00..15:29 / sum15:25..15:29; relative denominator shift(1).rolling20 mean of eligible full sessions',
                           lag='C[t-1]/C[t-1-h]-1 on scheduled full sessions, h1/5/20; all h+1 anchors required; early closes skipped only'),
             binning=dict(primary=8, coarse=5, z_bins=6, ties='unique quantile edges; boundary equality lower; no response use',
                          display_quantiles=[.005, .995], display_min_n=20, display_min_groups=10),
             contrast_candidates=[[.10, .30, .70, .90], [.05, .35, .65, .95], [0., .40, .60, 1.]],
             contrast_selection='first candidate with ≥50 dates/20 groups in all six X-band×state cells; partner marginalized; selection uses predictors only; B1 event gate applied AFTER selection without fallback',
             support=dict(min_n=50, min_groups=20, strong_n=100, strong_groups=30,
                          event_min=5, nonevent_min=5, event_groups_min=3),
             bootstrap=dict(seed=20261016, B=300, length=5, scheme='joint circular consecutive eligible-day records; fixed cells/masks; no re-estimated bins',
                            percentile=[2.5, 97.5], min_valid=270,
                            length10_sensitivity='not run; optional, no most-interpretable response-based selection'),
             exclusions=dict(DROP_TOP1=old['drop_top1'], DROP_TOP5=old['drop_top5']),
             masks=['FULL', 'DROP_TOP1', 'DROP_TOP5', 'NO_2020', 'PRE_2020', 'YEAR_2020', 'YEAR_2021', 'COMMON_DATES'],
             event_threshold_bp=-20, optional_threshold_minus40='omitted; no response-based threshold selection',
             costs_bp=[0, 2, 5, 10], rule='sign(W) continuation only; zero signal flat, costs per active round trip',
             execution='hypothetical entry at C15:29 and exit at C15:59; immediate availability/fill assumed; no observed bid/ask, latency or slippage; TRADING_NOT_ESTABLISHED',
             optional_features='VWAP, lagged volatility, partner stratification, A6 last5 and reversal omitted to keep bounded scope; patch VWAP/trade counts null',
             ranking=dict(primary_panel='first listed for each direction; all variants displayed, never chosen by response',
                          PROMISING_TO_TEST='primary H-L contrast supported; interval excludes0; |D|>=max(1bp,0.10*SD(Y)) or0.02 probability; all3 fixed exclusion signs agree and at least2 temporal raw contrasts agree with display-level20/10 support; ≥50% primary curve cells pass 50/20; no unresolved integrity issue',
                          LOW_PRIORITY='supported primary with interval crossing0 and |D|<0.05*SD(Y) (B1<0.01), or ≥2 of3 supported fixed exclusions reverse sign',
                          INCONCLUSIVE='all other available-data cases, including support/uncertainty failures',
                          DATA_BLOCKED='missing required inputs or feature-integrity failure',
                          C1='MODEL_DEPENDENT / DEFER, always', selection='interpretive triage of8 exploratory families; no composite score or formal significance; NO_CLEAR_WINNER allowed'),
             bans=['2022–2026 scientific reads', 'new downloads', 'predictive fits', 'validation selection', 'learned policy', 'null reruns'])
    write_json(PROTOCOL, p)
    print(json.dumps(dict(status='FROZEN_BEFORE_OUTCOME_READ', protocol_sha256=sha(PROTOCOL),
                          preserved_files=len(snapshot), source_bytes=sum(r['bytes'] for r in refs))))


def read_training(path, columns, eligible=False, start='2016-01-04'):
    """Arrow projects columns and predicates dates BEFORE scientific transformation."""
    if not '2016-01-04' <= start <= TRAIN[1]:
        raise ValueError('Training reader rejects dates outside 2016–2021 before I/O')
    end = dt.date.fromisoformat(TRAIN[1])
    filters = [('session_et', '>=', dt.date.fromisoformat(start)), ('session_et', '<=', end)]
    if eligible:
        filters.append(('eligible_primary', '=', True))
    READS.append(dict(path=Path(path).name,columns=list(dict.fromkeys(['session_et']+columns)),
                      filters=[(a,b,str(c)) for a,b,c in filters]))
    frame = pd.read_parquet(path, columns=list(dict.fromkeys(['session_et'] + columns)), filters=filters)
    dates = frame.session_et.astype(str)
    if not dates.between(start, TRAIN[1]).all():
        raise ValueError('INVALID_RERUN: training predicate failed')
    return frame


def lagged_closes(close_series, h):
    """Prior h-full-session simple return; missing interior anchors invalidate it."""
    prior = close_series.shift(1)
    complete = prior.rolling(h + 1, min_periods=h + 1).count().eq(h + 1)
    return (10000 * (prior / prior.shift(h) - 1)).where(complete)


def prior_volume(volume, lookback=20):
    """Mean of exactly prior eligible sessions; current volume never enters."""
    return volume.shift(1).rolling(lookback, min_periods=lookback).mean()


def feature_layer(data, p):
    """One in-memory training minute projection, one feature-only persisted table."""
    daily_path = data / p['daily']['path']
    # NO response column in this phase. P16 is a historical-anchor input shifted below.
    columns = ['eligible_primary', 'Pprev', 'P16', 'prior_full_session', 'skipped_early_sessions',
               'x_open_bp', 'w_preclose_bp', 'rv_open_log', 'rv_open_raw',
               'open_overnight_part', 'r_open_intraday_only', 'early_features_available_at',
               'late_features_available_at', 'terminal_repair_dependency']
    full = read_training(daily_path, columns).sort_values('session_et').reset_index(drop=True)
    daily = full.loc[full.eligible_primary].reset_index(drop=True)
    guard_training(daily, dict(train=TRAIN))
    if len(daily) != 1495:
        raise ValueError(f'Expected1495 training rows, got{len(daily)}')
    baseline = read_json(data / 'registry/D2_spy_source_manifest.json')
    patch_manifest = read_json(data / 'registry/D2_1c_hf_repair_manifest.json')
    if sha(data / 'registry/D2_spy_source_manifest.json') != patch_manifest['baseline_manifest_sha256']:
        raise ValueError('Wrong source1 baseline manifest')
    mcols = ['symbol', 'timestamp_utc', 'open', 'high', 'low', 'close', 'volume']
    original = pd.concat([read_training(data / baseline['blocks'][str(y)]['canonical']['path'], mcols)
                          for y in range(2016, 2022)], ignore_index=True)
    patch = read_training(data / patch_manifest['patch']['path'], mcols + ['validation_status'])
    # Allowed missing-key file is metadata only. The approved native overlay is sole patch.
    missing = pd.read_csv(data / 'registry/D2_spy_missing_candles.csv')
    allowed = {('SPY', pd.Timestamp(t)) for t in missing.timestamp_utc}
    minutes = merge_overlay(original, patch, allowed)
    local = minutes.timestamp_utc.dt.tz_convert(ET)
    if not local.dt.date.eq(minutes.session_et).all():
        raise ValueError('Minute UTC/ET day mismatch')
    minutes['clock'] = local.dt.strftime('%H:%M')
    if not minutes.symbol.eq('SPY').all() or minutes.duplicated(['symbol', 'timestamp_utc']).any():
        raise ValueError('Invalid SPY minute keys')
    close = minutes.pivot(index='session_et', columns='clock', values='close')
    features = pd.DataFrame({'session_et': daily.session_et})
    dates = daily.session_et
    c = close.reindex(dates)
    for h, clock in [(5, '15:24'), (10, '15:19'), (15, '15:14')]:
        features[f'late_return_{h}m_bp'] = (10000 * (c['15:29'] / c[clock] - 1)).to_numpy()
    features['late_accel_bp'] = features.late_return_5m_bp - (10000 * (c['15:24'] / c['15:19'] - 1)).to_numpy()
    features['gap_bp'] = 10000 * daily.open_overnight_part
    features['morning_bp'] = 10000 * daily.r_open_intraday_only
    features['abs_x_bp'] = daily.x_open_bp.abs()
    features['x_squared_bp2'] = daily.x_open_bp ** 2
    features['x_centered_squared_bp2'] = (daily.x_open_bp - daily.x_open_bp.mean()) ** 2
    features['abs_w_bp'] = daily.w_preclose_bp.abs()
    late = minutes.loc[minutes.clock.between('15:00', '15:29')].copy()
    assert late.clock.max() == '15:29'  # 15:30-start candle is prohibited.
    rv, v30, v5 = {}, {}, {}
    for day, g in late.groupby('session_et', sort=True):
        g = g.sort_values('timestamp_utc')
        expected = pd.date_range(at(day, '15:00'), periods=30, freq='min')
        if not pd.DatetimeIndex(g.timestamp_utc).equals(expected):
            continue
        rv[day] = opening_rv(g.to_dict('records'))  # Same 30-increment semantics, later window.
        if np.isfinite(g.volume).all() and g.volume.ge(0).all():
            v30[day] = g.volume.sum()
            v5[day] = g.loc[g.clock.ge('15:25'), 'volume'].sum()
    features['rv_late_30'] = dates.map(rv)
    features['rv_late_log'] = np.log(features.rv_late_30 + p['rv_epsilon'])
    features['late_volume_30m'] = dates.map(v30)
    features['late_volume_5m'] = dates.map(v5)
    denominator = prior_volume(features.late_volume_30m)
    features['relative_late_volume'] = features.late_volume_30m / denominator.where(denominator.gt(0))
    # Full-session index includes missing-opening days. Never drop missing full closes.
    cal = calendar('2016-01-04', TRAIN[1])
    scheduled = [s.date() for s in cal.sessions_in_range('2016-01-04', TRAIN[1])
                 if cal.session_close(s).tz_convert(ET).strftime('%H:%M') == '16:00']
    if full.session_et.tolist() != scheduled:
        raise ValueError('Canonical full-session calendar mismatch; no lag feature computed')
    history = full.set_index('session_et').P16
    for h in [1, 5, 20]:
        features[f'lag_close_{h}_bp'] = dates.map(lagged_closes(history, h))
    if features.duplicated('session_et').any():
        raise ValueError('Duplicate feature keys')
    for day, prior, skipped, early, late_time in zip(dates, daily.prior_full_session,
            daily.skipped_early_sessions, daily.early_features_available_at, daily.late_features_available_at):
        if prior_full(cal, str(day)) != str(prior) or not prior < day:
            raise ValueError(f'Wrong prior full-session mapping {day}')
        if skipped != len(cal.sessions_in_range(str(prior), str(day))) - 2:
            raise ValueError(f'Wrong early-session skip {day}')
        if early > at(day, '10:00') or late_time > at(day, '15:30'):
            raise ValueError(f'Feature cutoff violated {day}')
    joined = daily.merge(features, on='session_et', validate='one_to_one')
    cuts = dict(rv_open_log=p['opening_cutoffs_log'],
                rv_late_log=np.quantile(features.rv_late_log.dropna(), [1/3, 2/3]).tolist())
    for s, v in cuts.items():
        joined[s + '_state'] = np.searchsorted(v, joined[s], side='left')
    qa = real_feature_checks(joined, full, minutes, features, p)
    qa.update(training_minutes=len(minutes), native_patch_training_rows=len(patch),
              complete_late_RV=int(features.rv_late_30.notna().sum()),
              feature_rows=len(features), new_feature_columns=len(features.columns)-1,
              x_mean_train_bp=float(daily.x_open_bp.mean()),
              relative_volume_warmup=int(features.relative_late_volume.isna().sum()),
              early_skip_training_dates=[str(x) for x in dates[daily.skipped_early_sessions.gt(0)]],
              excluded_full_sessions=full.loc[~full.eligible_primary, ['session_et']].astype(str).to_dict('records'))
    return joined, features, cuts, qa


def real_feature_checks(frame, full, minutes, features, p):
    """Independent scalar calculations on DST, half-day, repair and crisis examples."""
    checks = []
    for day in ['2016-01-05', '2019-03-08', '2019-03-11', '2019-08-12', '2019-12-02', '2020-03-18', '2021-05-06']:
        d = dt.date.fromisoformat(day)
        row = frame.loc[frame.session_et.eq(d)].iloc[0]
        m = minutes.loc[minutes.session_et.eq(d)].set_index('clock')
        expected = {f'late_return_{h}m_bp':10000*(float(m.loc['15:29','close'])/float(m.loc[t,'close'])-1)
                    for h,t in [(5,'15:24'),(10,'15:19'),(15,'15:14')]}
        expected['late_accel_bp'] = expected['late_return_5m_bp']-10000*(float(m.loc['15:24','close'])/float(m.loc['15:19','close'])-1)
        late = m.loc['15:00':'15:29']
        q = [np.log(float(late.iloc[0].close)/float(late.iloc[0].open))]
        q += [np.log(float(late.iloc[i].close)/float(late.iloc[i-1].close)) for i in range(1,30)]
        expected['rv_late_30'] = float(np.sqrt(sum(x*x for x in q)))
        expected['late_volume_30m'] = float(late.volume.sum())
        expected['late_volume_5m'] = float(late.loc['15:25':'15:29'].volume.sum())
        expected['gap_bp'] = 10000*(float(m.loc['09:30','open'])/row.Pprev-1)
        expected['morning_bp'] = 10000*(float(m.loc['09:59','close'])/float(m.loc['09:30','open'])-1)
        for key, value in expected.items():
            if not np.isclose(value, row[key], rtol=1e-10, atol=1e-9):
                raise ValueError(f'Manual feature mismatch {day}:{key}')
        idx = full.index[full.session_et.eq(d)][0]
        for h in [1,5,20]:
            if idx >= h+1:
                manual = 10000*(full.P16.iloc[idx-1]/full.P16.iloc[idx-1-h]-1)
                if not np.isclose(manual,row[f'lag_close_{h}_bp'], rtol=1e-10, atol=1e-9):
                    raise ValueError(f'Manual lag mismatch {day}:h{h}')
        vi = features.index[features.session_et.eq(d)][0]
        if vi >= 20:
            manual = row.late_volume_30m / features.late_volume_30m.iloc[vi-20:vi].mean()
            if not np.isclose(manual,row.relative_late_volume):
                raise ValueError(f'Manual past-volume mismatch {day}')
        checks.append(dict(session_et=day, status='PASS', checked_fields=list(expected),
                           late_increments=len(q), early_available_utc=at(day,'10:00').isoformat(),
                           late_available_utc=at(day,'15:30').isoformat(),
                           prior_full_session=str(row.prior_full_session), skipped_early=int(row.skipped_early_sessions)))
    return dict(real_date_checks=checks, manual_checks='PASS', chronology='PASS',
                no_1530_start_predictor=True, timezone_DST='zoneinfo America/New_York',
                volume_reference='20 previous eligible days, excludes current',
                close_reference='1/5/20 completed scheduled full sessions, missing anchors never skipped')


def quantile_edges(x, count):
    """Fixed pooled predictor quantiles; remove ties deterministically."""
    return np.unique(np.quantile(x[np.isfinite(x)], np.linspace(0, 1, count+1)))


def assign_bins(x, edges):
    return np.searchsorted(edges[1:-1], x, side='left')


def panel_mask(frame, spec):
    mask = np.isfinite(frame[spec['x']]) & np.isfinite(frame[spec['state']])
    if spec['facet'] == 'NEGATIVE':
        mask &= frame.x_open_bp.lt(0)
    if spec['facet'] == 'NONNEGATIVE':
        mask &= frame.x_open_bp.ge(0)
    return mask.to_numpy()


def design(frame, p, cuts):
    """Numerical cells/endpoints chosen from predictors only, before response read."""
    plans = {}
    common = np.ones(len(frame), dtype=bool)
    for group in p['directions'].values():
        for spec in group['panels']:
            # Sign facets are scientific subpopulations, not a common-mask requirement.
            common &= np.isfinite(frame[spec['x']]) & np.isfinite(frame[spec['state']])
    block_id = np.arange(len(frame)) // p['bootstrap']['length']
    for identity, group in p['directions'].items():
        plans[identity] = []
        for spec in group['panels']:
            x = frame[spec['x']].to_numpy(float)
            mask = panel_mask(frame, spec)
            pooled = np.isfinite(x)  # Same magnitude boundaries in both sign facets.
            e = quantile_edges(x[pooled], p['binning']['primary'])
            coarse = quantile_edges(x[pooled], p['binning']['coarse'])
            zedges = quantile_edges(frame.loc[np.isfinite(frame[spec['state']]),spec['state']].to_numpy(),p['binning']['z_bins'])
            states = frame[spec['state']+'_state'].to_numpy()
            candidates = []
            selected = None
            for quantiles in p['contrast_candidates']:
                values = np.quantile(x[pooled], quantiles)
                bands = [mask & (x >= values[0]) & (x <= values[1]),
                         mask & (x >= values[2]) & (x <= values[3])]
                # Disjoint endpoints even under tied quantiles.
                bands[1] &= ~bands[0]
                cells = [b & (states==s) for s in range(3) for b in bands]
                counts = [int(c.sum()) for c in cells]
                groups = [len(np.unique(block_id[c])) for c in cells]
                passes = min(counts)>=p['support']['min_n'] and min(groups)>=p['support']['min_groups']
                candidates.append(dict(quantiles=quantiles, bands=values.tolist(), n=counts, groups=groups, passes=passes))
                if selected is None and passes:
                    selected = len(candidates)-1
            plans[identity].append(dict(**spec, edges=e.tolist(), coarse_edges=coarse.tolist(),
                                       centers=[float(np.median(x[pooled & (assign_bins(x,e)==i)])) for i in range(len(e)-1)],
                                       z_edges=zedges.tolist(), candidates=candidates, selected=selected,
                                       actual_bins=len(e)-1, merged_bins=p['binning']['primary']-(len(e)-1),
                                       display_limits=np.quantile(x[pooled],p['binning']['display_quantiles']).tolist(),
                                       clipped_predictor_count=int((mask & ((x<np.quantile(x[pooled],.005)) | (x>np.quantile(x[pooled],.995)))).sum()),
                                       n=int(mask.sum()), first=str(frame.loc[mask,'session_et'].iloc[0]),
                                       last=str(frame.loc[mask,'session_et'].iloc[-1])))
    return plans, common


def circular_indices(n, B, length, seed):
    """Joint chronological day resamples shared across every panel/state/cell."""
    rng = np.random.default_rng(seed)
    starts = rng.integers(0,n,size=(B,int(np.ceil(n/length))))
    return ((starts[:,:,None]+np.arange(length))%n).reshape(B,-1)[:,:n]


def grouped_bootstrap(cell, y, indices, n_cells):
    """Ratio-of-sums means/rates; empty cells remain NaN, never fabricated zero."""
    draws = np.full((len(indices), n_cells), np.nan)
    for b, index in enumerate(indices):
        c = cell[index]
        ok = c>=0
        n = np.bincount(c[ok],minlength=n_cells)
        sums = np.bincount(c[ok],weights=y[index][ok],minlength=n_cells)
        np.divide(sums,n,out=draws[b],where=n>0)
    return draws


def interval(values, support, p):
    finite = values[np.isfinite(values)]
    if not support:
        return np.nan, np.nan, len(finite), 'ABSTAIN_SUPPORT'
    if len(finite)<p['bootstrap']['min_valid']:
        return np.nan, np.nan, len(finite), 'ABSTAIN_BOOTSTRAP_EMPTY'
    lo, hi = np.percentile(finite,p['bootstrap']['percentile'])
    if hi-lo <= 1e-12:
        return np.nan, np.nan, len(finite), 'ABSTAIN_DEGENERATE'
    return float(lo),float(hi),len(finite),'EXPLORATORY_BLOCK_PERCENTILE'


def masks(frame, p, common):
    dates = frame.session_et.astype(str)
    return dict(FULL=np.ones(len(frame),bool),
                DROP_TOP1=~dates.isin(p['exclusions']['DROP_TOP1']).to_numpy(),
                DROP_TOP5=~dates.isin(p['exclusions']['DROP_TOP5']).to_numpy(),
                NO_2020=~dates.str.startswith('2020').to_numpy(),
                PRE_2020=(dates<'2020-01-01').to_numpy(),
                YEAR_2020=dates.str.startswith('2020').to_numpy(),
                YEAR_2021=dates.str.startswith('2021').to_numpy(), COMMON_DATES=common)


def response(frame, identity, p):
    y = frame.y_last30_bp.to_numpy(float)
    if identity=='B1':
        return (y<p['event_threshold_bp']).astype(float)
    if identity=='C1':
        return np.sign(frame.w_preclose_bp.to_numpy(float))*y
    return y


def cell_statistics(frame, spec, y, identity, subset, subset_name, indices, p, kind='curve', bin_count=8):
    """Raw empirical cells, date/group/event counts, fixed-bin block intervals."""
    x = frame[spec['x']].to_numpy(float)
    z = frame[spec['state']].to_numpy(float)
    edge = spec['coarse_edges'] if bin_count==5 else spec['edges']
    xb = assign_bins(x,edge)
    states = frame[spec['state']+'_state'].to_numpy()
    zb = assign_bins(z,spec['z_edges']) if kind=='heatmap' else states
    nz = len(spec['z_edges'])-1 if kind=='heatmap' else 3
    nx = len(edge)-1
    good = panel_mask(frame,spec) & subset
    cell = np.where(good,zb*nx+xb,-1)
    draws = grouped_bootstrap(cell,y,indices,nz*nx)
    group_id = np.arange(len(frame))//p['bootstrap']['length']
    records = []
    for k in range(nz*nx):
        valid = cell==k
        n = int(valid.sum()); groups = len(np.unique(group_id[valid]))
        events = int(y[valid].sum()) if identity=='B1' else None
        nonevents = n-events if identity=='B1' else None
        event_groups = len(np.unique(group_id[valid & (y==1)])) if identity=='B1' else None
        supported = n>=p['support']['min_n'] and groups>=p['support']['min_groups']
        display = n>=p['binning']['display_min_n'] and groups>=p['binning']['display_min_groups']
        if identity=='B1':
            event_ok = events>=p['support']['event_min'] and nonevents>=p['support']['nonevent_min'] and event_groups>=p['support']['event_groups_min']
            supported &= event_ok; display &= event_ok
        lo,hi,nb,status = interval(draws[:,k],supported,p)
        records.append(dict(experiment=identity, predictor=spec['x'], facet=spec['facet'],state=spec['state'],
                            panel_label=spec['label'], mask=subset_name, kind=kind, requested_bins=bin_count,
                            x_bin=k%nx,z_bin=k//nx, x_left=edge[k%nx],x_right=edge[k%nx+1],
                            x_mean=float(x[valid].mean()) if n else np.nan,
                            mean=float(y[valid].mean()) if n else np.nan,
                            sd=float(y[valid].std(ddof=1)) if n>1 else np.nan,
                            n=n, groups=groups,events=events,nonevents=nonevents,event_groups=event_groups,
                            display_supported=bool(display),contrast_level_supported=bool(supported),
                            ci_low=lo,ci_high=hi,valid_bootstraps=nb,interval_status=status,
                            first=str(frame.loc[valid,'session_et'].min()) if n else '',
                            last=str(frame.loc[valid,'session_et'].max()) if n else ''))
    return records


def select_rows(table,identity,spec,mask='FULL',kind='curve',bins=8):
    """Select one declared panel without choosing a response-favorable variant."""
    return table.loc[table.experiment.eq(identity) & table.predictor.eq(spec['x']) &
                     table.facet.eq(spec['facet']) & table.state.eq(spec['state']) & table['mask'].eq(mask) &
                     table.kind.eq(kind) & table.requested_bins.eq(bins)].copy()


def select_contrasts(table,identity,spec,mask='FULL'):
    return table.loc[table.experiment.eq(identity) & table.predictor.eq(spec['x']) &
                     table.facet.eq(spec['facet']) & table.state.eq(spec['state']) & table['mask'].eq(mask)].copy()


def summarize(frame,plans,bins,contrasts,p):
    """Apply frozen triage to FIRST panel; report all-panel diagnostics separately."""
    rows=[]
    for identity,specs in plans.items():
        spec=specs[0]
        c=select_contrasts(contrasts,identity,spec)
        primary=c.loc[c.comparison.eq('high-low')].iloc[0]
        cells=select_rows(bins,identity,spec)
        exclusion=[]; temporal=[]
        for mask in ['DROP_TOP1','DROP_TOP5','NO_2020','PRE_2020','YEAR_2020','YEAR_2021']:
            r=select_contrasts(contrasts,identity,spec,mask).iloc[0]
            v=r.estimate if r.supported else np.nan
            if mask in ['DROP_TOP1','DROP_TOP5','NO_2020']:
                exclusion.append(v)
            else:
                temporal.append(r.descriptive_only_estimate)
        effect=primary.estimate
        sign=lambda v: bool(np.isfinite(v) and np.isfinite(effect) and np.sign(v)==np.sign(effect))
        n_exclusion=sum(sign(v) for v in exclusion)
        n_temporal=sum(sign(v) for v in temporal)
        n_reversed=sum(np.isfinite(v) and np.isfinite(effect) and np.sign(v)!=np.sign(effect) for v in exclusion)
        y=response(frame,identity,p)
        noise=float(y[panel_mask(frame,spec)].std(ddof=1))
        fraction=float(cells.contrast_level_supported.mean())
        excludes0=bool(np.isfinite(primary.ci_low) and primary.ci_low*primary.ci_high>0)
        threshold=.02 if identity=='B1' else max(1.,.10*noise)
        small=.01 if identity=='B1' else .05*noise
        if identity=='C1':
            rating='MODEL_DEPENDENT / DEFER'
        elif primary.supported and excludes0 and abs(effect)>=threshold and n_exclusion==3 and n_temporal>=2 and fraction>=.5:
            rating='PROMISING_TO_TEST'
        elif primary.supported and ((not excludes0 and abs(effect)<small) or n_reversed>=2):
            rating='LOW_PRIORITY'
        else:
            rating='INCONCLUSIVE'
        allfull=contrasts.loc[contrasts.experiment.eq(identity)&contrasts['mask'].eq('FULL')]
        rows.append(dict(experiment=identity,rating=rating,
                         n_min=min(s['n'] for s in specs),n_max=max(s['n'] for s in specs),
                         primary_n=spec['n'],first=min(s['first'] for s in specs),last=max(s['last'] for s in specs),
                         primary_predictor=spec['x'],primary_state=spec['state'],
                         primary_contrast=effect,ci_low=primary.ci_low,ci_high=primary.ci_high,
                         interval_status=primary.interval_status,primary_cell_support_fraction=fraction,
                         primary_contrast_n=primary.n,primary_contrast_groups=primary.groups,
                         supported_primary_family_contrasts=int(allfull.supported.sum()),
                         abstained_primary_family_contrasts=int((~allfull.supported).sum()),
                         y_sd=noise,effect_noise_ratio=abs(effect)/noise if np.isfinite(effect) and noise else np.nan,
                         fixed_exclusion_same_sign=n_exclusion,fixed_exclusion_supported=sum(np.isfinite(exclusion)),
                         temporal_same_sign_display_level=n_temporal,
                         temporal_display_supported=sum(np.isfinite(temporal)),
                         primary_materiality_screen=threshold,interval_excludes_zero=excludes0,
                         sign_reversals_fixed_exclusions=int(n_reversed),
                         freshness='10:00 /15:30 separate' if identity=='B1' else spec['cutoff'],
                         interpretation='Exploratory raw bands; partners marginalized; no predictive or causal confirmation'))
    return pd.DataFrame(rows)


def feature_registry(frame,features,p):
    """Compact exact formula, units, lineage, cutoff and warmup register."""
    defs={
        'x_open_bp':('10000*(C09:59/Pprev-1)','bp','prior full close–10:00','10:00','Stage1 daily','none'),
        'w_preclose_bp':('10000*(C15:29/C14:59-1)','bp','15:00–15:30','15:30','Stage1 daily','none'),
        'rv_open_log':('log(sqrt(log(C09:30/O09:30)^2+29 adjacent close logs squared)+1e-8)','log RV','09:30–10:00','10:00','Stage1 daily; frozen cuts','all 30 valid'),
        'gap_bp':('10000*open_overnight_part =10000*(O09:30/Pprev-1)','bp','prior full close–09:30','10:00','Stage1 daily components','prior full anchor required'),
        'morning_bp':('10000*r_open_intraday_only =10000*(C09:59/O09:30-1)','bp','09:30–10:00','10:00','Stage1 daily components','none'),
        'late_accel_bp':('late_return_5m_bp -10000*(C15:24/C15:19-1)','bp','15:20–15:30, disjoint5m','15:30','D2 +D2.1c minute close','all endpoints genuine'),
        'abs_x_bp':('abs(x_open_bp)','bp','prior full close–10:00','10:00','Stage1 daily X','none; sign facets X<0/X>=0'),
        'x_squared_bp2':('x_open_bp**2','bp²','prior full close–10:00','10:00','Stage1 daily X','none; removes direction'),
        'x_centered_squared_bp2':('(x_open_bp - TRAIN mean X)**2','bp²','prior full close–10:00','10:00','Stage1 daily X; retrospective TRAIN centering','center known after training; not live historical transform'),
        'abs_w_bp':('abs(w_preclose_bp)','bp','15:00–15:30','15:30','Stage1 daily W','none'),
        'rv_late_30':('sqrt(log(C15:00/O15:00)^2+29 adjacent close logs squared)','dimensionless RV','15:00–15:30','15:30','D2 +D2.1c minute OHLC','all 30 valid; no overnight'),
        'rv_late_log':('log(rv_late_30+1e-8)','log RV','15:00–15:30','15:30','new RV; distinct TRAIN-only terciles','all 30 valid'),
        'late_volume_30m':('sum(volume15:00..15:29)','shares','15:00–15:30','15:30','D2 +D2.1c volume','all 30 finite/nonnegative'),
        'late_volume_5m':('sum(volume15:25..15:29)','shares','15:25–15:30','15:30','D2 +D2.1c volume','all 5 finite/nonnegative'),
        'relative_late_volume':('late_volume_30m / mean(previous 20 eligible full-session late_volume_30m)','ratio','current/prior 20 eligible sessions','15:30','same volume; denominator shift1 rolling20','first20 eligible days missing; positive denominator'),
    }
    for h,t in [(5,'15:24'),(10,'15:19'),(15,'15:14')]:
        defs[f'late_return_{h}m_bp']=(f'10000*(C15:29/C{t}-1)','bp',f'close {t} to15:29','15:30','D2 +D2.1c minute close','genuine completed endpoints')
    for h in [1,5,20]:
        defs[f'lag_close_{h}_bp']=(f'10000*(C[t-1]/C[t-1-{h}]-1)','bp',f'{h} completed full sessions ending prior full close','10:00','scheduled full-session Stage1 P16, shift1',f'{h+1} consecutive full close anchors; half-days skipped only; missing anchors invalidate')
    records=[]
    for name,(formula,unit,window,cutoff,lineage,warmup) in defs.items():
        ok=frame[name].notna()
        records.append(dict(feature=name,formula=formula,unit=unit,observation_window=window,
                            earliest_usable_time_ET=cutoff,field_lineage=lineage,
                            missing_policy='no imputation; retain primary sample and mark unavailable feature',
                            warmup=warmup,n=int(ok.sum()),missing=int((~ok).sum()),
                            first=str(frame.loc[ok,'session_et'].min()),last=str(frame.loc[ok,'session_et'].max()),
                            persisted_new_feature=name in features.columns,
                            source_dataset=p['source_id'],adjustment=p['adjustment']))
    records += [dict(feature='B1_event',formula='1{y_last30_bp < -20}',unit='probability',
                     observation_window='15:30–16:00',earliest_usable_time_ET='16:00 LABEL ONLY',
                     field_lineage='frozen signedY; never a predictor',n=len(frame),missing=0,persisted_new_feature=False),
                dict(feature='C1_payoff',formula='sign(W)*Y - cost_bp*1{W!=0}; costs0/2/5/10',unit='bp',
                     observation_window='hypothetical entry C15:29/exit C15:59',earliest_usable_time_ET='16:00 OUTCOME ONLY',
                     field_lineage='fixed unoptimized rule; TRADING_NOT_ESTABLISHED',n=len(frame),missing=0,persisted_new_feature=False)]
    return pd.DataFrame(records)


def plot_setup():
    # A local bounded font cache; no global environment/package change.
    os.environ.setdefault('MPLCONFIGDIR',str(OUT/'config/matplotlib_cache'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':9,'axes.titlesize':10,'axes.labelsize':9,
                         'legend.fontsize':8,'figure.dpi':110,'savefig.dpi':120})
    return plt


def y_unit(identity):
    return 'Downside probability (0–1)' if identity=='B1' else 'Illustrative payoff (bp)' if identity=='C1' else 'Y: 15:30–16:00 return (bp)'


def figure_title(fig,identity,group,kind):
    state='recent RV + opening RV comparison' if identity=='A6' else 'opening one-minute RV'
    fig.suptitle(f'{identity} — {group["title"]}\n{kind}; {y_unit(identity)} | state: {state}\n'
                 f'TRAIN ONLY {TRAIN[0]}–{TRAIN[1]} | information cutoff in each panel (ET)',fontsize=12,y=.995)


def draw_curve(ax,rows,spec,identity,p,intervals=False):
    for state,color in enumerate(COLORS):
        g=rows.loc[rows.z_bin.eq(state)].sort_values('x_bin')
        if g.empty:
            continue
        x=np.asarray(spec['centers'])
        values=g['mean'].to_numpy().copy()
        values[~g.display_supported.to_numpy()]=np.nan
        # NaN gaps are retained; unsupported ranges are never bridged.
        ax.plot(x,values,'o-',ms=3,lw=1.5,color=color,
                label=f'{STATES[state]} n={g.n.sum()}, shown {g.display_supported.sum()}/{len(g)}')
        if intervals:
            ok=g.interval_status.eq('EXPLORATORY_BLOCK_PERCENTILE').to_numpy()
            ax.vlines(x[ok],g.ci_low.to_numpy()[ok],g.ci_high.to_numpy()[ok],color=color,lw=1.1)
            # Percentile intervals need not contain the observed statistic.
            ax.plot(x[ok],g.ci_low.to_numpy()[ok],'_',color=color,ms=4)
            ax.plot(x[ok],g.ci_high.to_numpy()[ok],'_',color=color,ms=4)
            for k,(_,r) in enumerate(g.iterrows()):
                # Uniformly spaced count labels avoid collisions near X=0.
                ax.text((k+.5)/len(g),-.23-.06*state,f'Q{k+1}: {int(r.n)}/{int(r.groups)}',color=color,
                        fontsize=7,ha='center',transform=ax.transAxes,clip_on=False)
    ax.set_xlim(*spec['display_limits'])
    ax.set_xlabel(f'{spec["label"]} ({spec["unit"]})' + ('; cell n / 5-row groups below' if intervals else ''))
    ax.set_ylabel(y_unit(identity))
    if identity=='B1':
        ax.set_ylim(-.04,1.04)
    else:
        ax.axhline(0,color='gray',lw=.6)
    ax.grid(alpha=.15)


def panel_axes(plt,n,height=4.0):
    cols=1 if n==1 else 2
    rows=int(np.ceil(n/cols))
    fig,axes=plt.subplots(rows,cols,figsize=(14,rows*height+1.6),squeeze=False)
    for ax in axes.flat[n:]:
        ax.set_visible(False)
    return fig,list(axes.flat[:n])


def save_figure(plt,fig,identity,name):
    directory=OUT/'figures'/identity
    directory.mkdir(parents=True,exist_ok=True)
    fig.savefig(directory/name,facecolor='white')
    plt.close(fig)
    total=sum(f.stat().st_size for f in (OUT/'figures').rglob('*.png'))
    if total>50_000_000:
        raise RuntimeError('Figure storage exceeded50MB; stop before uncontrolled growth')


def plots(frame,plans,bins,contrasts,costs,cuts,p):
    """44 fixed raw-data figures: no fitted curves or learned decisions."""
    plt=plot_setup()
    for identity,specs in plans.items():
        group=p['directions'][identity]
        y=response(frame,identity,p)
        # 1: points plus supported empirical means, predictor-only display limits.
        fig,axes=panel_axes(plt,len(specs))
        figure_title(fig,identity,group,'Raw points and empirical binned means — no fitted model')
        for ax,spec in zip(axes,specs):
            ok=panel_mask(frame,spec)
            states=frame[spec['state']+'_state'].to_numpy()
            for s,color in enumerate(COLORS):
                use=ok&(states==s)
                ax.scatter(frame.loc[use,spec['x']],y[use],s=8,alpha=.22,color=color,rasterized=True)
            draw_curve(ax,select_rows(bins,identity,spec),spec,identity,p)
            ax.set_title(f'{spec["label"]} | {spec["state"]} | {spec["cutoff"]} ET\nn={spec["n"]}; X outside viewing range={spec["clipped_predictor_count"]}; estimates retain all')
            ax.legend(loc='best')
        fig.text(.02,.015,'Lines require ≥20 dates /10 distinct five-row groups; events additionally ≥5 events/nonevents, ≥3 event groups. Intervals use stricter50/20. No response clipping.',fontsize=8)
        fig.subplots_adjust(top=1-1.35/fig.get_size_inches()[1],bottom=.12,hspace=.65,wspace=.22)
        save_figure(plt,fig,identity,FILENAMES[0])
        # 2: curves with joint-block percentile variability intervals, all raw dates.
        variants=[(s,'FULL') for s in specs] if identity!='C1' else [(specs[0],f'FULL_COST_{c}') for c in p['costs_bp']]
        fig,axes=panel_axes(plt,len(variants),height=4.7)
        figure_title(fig,identity,group,'Raw band means/rates and exploratory 95% joint day-block intervals')
        for ax,(spec,mask) in zip(axes,variants):
            rows=select_rows(bins,identity,spec,mask)
            draw_curve(ax,rows,spec,identity,p,True)
            if identity=='C1':
                ax.set_ylabel('Hypothetical net illustrative payoff (bp)')
            events=f'; event count={int(rows.events.sum())}' if identity=='B1' else ''
            ax.set_title(f'{spec["label"]} | {spec["cutoff"]} ET | '+(mask if identity=='C1' else spec['state'])+events)
            ax.legend(loc='best')
        fig.text(.02,.012,'Cell labels n / distinct 5-row groups (not independent clusters). Whiskers only if 50/20 support and ≥270/300 valid draws; no whisker means ABSTAIN.\nB1 uses event-rate resampling, not Gaussian-Y intervals. C1 costs are hypothetical round-trip scenarios; no bid/ask/slippage/latency evidence.',fontsize=8)
        fig.subplots_adjust(top=1-1.35/fig.get_size_inches()[1],bottom=.30 if len(variants)<3 else .20,hspace=.95,wspace=.22)
        save_figure(plt,fig,identity,FILENAMES[1])
        # 3: actual continuous log-RV cells with no interpolation.
        fig,axes=panel_axes(plt,len(specs),height=4.4)
        figure_title(fig,identity,group,'Raw empirical X–continuous log-RV response; unsupported cells gray')
        for ax,spec in zip(axes,specs):
            rows=select_rows(bins,identity,spec,kind='heatmap')
            nx=spec['actual_bins']; nz=len(spec['z_edges'])-1
            matrix=rows.sort_values(['z_bin','x_bin'])['mean'].to_numpy().reshape(nz,nx)
            support=rows.sort_values(['z_bin','x_bin']).display_supported.to_numpy().reshape(nz,nx)
            matrix=np.ma.array(matrix,mask=~support)
            cmap=plt.get_cmap('viridis' if identity=='B1' else 'RdBu_r').copy()
            cmap.set_bad('#dddddd')
            kw=dict(cmap=cmap,shading='flat')
            if identity=='B1':
                kw.update(vmin=0,vmax=1)
            elif matrix.count():
                bound=max(1,float(np.max(np.abs(matrix.compressed()))))
                kw.update(vmin=-bound,vmax=bound)
            # Quantile-spaced geometry keeps narrow numerical bands readable.
            # Only coordinates change; every colored cell remains its raw mean.
            mesh=ax.pcolormesh(np.arange(nx+1),np.arange(nz+1),matrix,**kw)
            fig.colorbar(mesh,ax=ax,label='Probability' if identity=='B1' else 'Raw mean (bp)')
            for _,r in rows.iterrows():
                xx=r.x_bin+.5; yy=r.z_bin+.5
                txt=f'n{r.n}' + (f'\ne{int(r.events)}' if identity=='B1' else '')
                ax.text(xx,yy,txt,ha='center',va='center',fontsize=8,color='black',
                        bbox=dict(facecolor='white',alpha=.55,pad=.2,edgecolor='none'))
            for cut in cuts[spec['state']]:
                ax.axhline(np.interp(cut,spec['z_edges'],np.arange(nz+1)),color='#222222',lw=1,ls='--')
            ax.set_xticks(np.arange(nx)+.5,[f'Q{k+1}\n{v:.2g}'.replace('e+0','e').replace('e+','e') for k,v in enumerate(spec['centers'])],fontsize=7)
            ax.set_yticks(np.arange(nz)+.5,[f'{a:.2f} to {b:.2f}' for a,b in zip(spec['z_edges'][:-1],spec['z_edges'][1:])],fontsize=7)
            ax.set_title(f'{spec["label"]} | {spec["cutoff"]} ET | n={spec["n"]}\n{spec["state"]}; quantile-spaced cells, all tails retained')
            ax.set_xlabel(f'{spec["label"]}: pooled X-bin median ({spec["unit"]})')
            ax.set_ylabel(f'{spec["state"]}: numerical log-RV band')
        fig.text(.02,.02,'Cells: pooled 8 X-quantile ×6 continuous log-RV-quantile bands; display support 20 dates/10 groups (+ B1 event gate). Dashed: named TRAIN terciles.\nQuantile-spaced coordinates with numerical labels (not equal numerical widths). Cell n shown; gray = unsupported; no response interpolation. Brightness may be noise/variance.',fontsize=8)
        fig.subplots_adjust(top=1-1.35/fig.get_size_inches()[1],bottom=.14,hspace=.65,wspace=.34)
        save_figure(plt,fig,identity,FILENAMES[2])
        # 4: joint occupancy and selected, genuinely supported cross-state increments.
        fig,axes=plt.subplots(len(specs),2,figsize=(15,3.7*len(specs)+1.9),squeeze=False)
        figure_title(fig,identity,group,'Support and cross-state increment evidence' if identity!='C1' else 'Illustrative support and hypothetical cost break-even feasibility')
        for row,spec in enumerate(specs):
            ax,bx=axes[row]
            cells=select_rows(bins,identity,spec).sort_values(['z_bin','x_bin'])
            n=cells.n.to_numpy().reshape(3,-1); g=cells.groups.to_numpy().reshape(3,-1)
            status=cells.contrast_level_supported.to_numpy().reshape(3,-1)
            ax.imshow(status.astype(float),vmin=0,vmax=1,cmap=plt.get_cmap('Greys'),alpha=.25,aspect='auto',origin='lower')
            for s in range(3):
                for k in range(spec['actual_bins']):
                    extra=f'\ne{int(cells.events.iloc[s*spec["actual_bins"]+k])}' if identity=='B1' else ''
                    ax.text(k,s,f'{n[s,k]}/{g[s,k]}{extra}',ha='center',va='center',fontsize=8)
            ax.set_yticks(range(3),STATES)
            ax.set_xticks(range(spec['actual_bins']),[f'{x:.2g}' for x in spec['centers']],rotation=35)
            ax.set_xlabel(f'{spec["label"]} ({spec["unit"]}); pooled X-bin median')
            ax.set_title(f'{spec["cutoff"]} ET: n / distinct five-row groups\nDark cells pass 50/20 (+ event gate for B1)')
            if identity=='C1':
                for s,color in enumerate(COLORS):
                    r=costs.loc[costs.state.eq(STATES[s])].sort_values('cost_bp')
                    bx.plot(r.cost_bp,r['mean'],'o-',color=color,label=STATES[s])
                    bx.vlines(r.cost_bp,r.ci_low,r.ci_high,color=color)
                bx.axhline(0,color='black',lw=.8)
                bx.set_xlabel('Hypothetical round-trip cost (bp), active days only')
                bx.set_ylabel('Mean hypothetical net payoff (bp)')
                bx.set_title('Fixed sign(W) continuation; gross = cost0\nNo bid/ask/latency/fill evidence — TRADING_NOT_ESTABLISHED')
                bx.legend()
            else:
                c=select_contrasts(contrasts,identity,spec)
                for j,(_,r) in enumerate(c.iterrows()):
                    if r.interval_status=='EXPLORATORY_BLOCK_PERCENTILE':
                        bx.plot(r.estimate,j,'o',color=COLORS[j])
                        bx.hlines(j,r.ci_low,r.ci_high,color=COLORS[j],lw=2)
                    else:
                        bx.text(.02,j,'ABSTAIN: '+r.interval_status,transform=bx.get_yaxis_transform(),fontsize=8)
                bx.axvline(0,color='gray',lw=.7)
                bx.set_yticks(range(3),c.comparison)
                bx.set_ylim(-.7,2.7)
                bx.set_xlabel('Difference of within-state X-band increments ('+('probability' if identity=='B1' else 'bp')+')')
                candidate=spec['candidates'][spec['selected'] if spec['selected'] is not None else 0]
                bx.set_title(f'{spec["label"]} | {spec["cutoff"]} ET\nEndpoint cell n={candidate["n"]}; groups={candidate["groups"]}',fontsize=9)
                if not c.supported.any():
                    bx.text(.5,.88,'INSUFFICIENT_SUPPORT — NO SCIENTIFIC CONTRAST',transform=bx.transAxes,ha='center',fontsize=8,color='#aa0000')
                else:
                    bands=candidate['bands']
                    bx.text(.01,-.24,f'X bands [{bands[0]:.3g},{bands[1]:.3g}] → [{bands[2]:.3g},{bands[3]:.3g}] {spec["unit"]}; partner marginalized',transform=bx.transAxes,fontsize=8)
        fig.text(.02,.015,'Support groups are occupancy diagnostics, not certified independent clusters. First predictor-only qualifying endpoint pair fixed before Y read; no response-based fallback.\nIntervals: 300 joint circular 5-day draws, fixed empirical bands; not point D_m, causal effects, selection-adjusted or theorem-certified inference.',fontsize=8)
        fig.subplots_adjust(top=1-1.5/fig.get_size_inches()[1],bottom=1.35/fig.get_size_inches()[1],hspace=.85,wspace=.36)
        save_figure(plt,fig,identity,FILENAMES[3])
        if identity=='C1':
            continue
        # 5: fixed bins and masks; differences in levels are not moderation proof.
        fig,axes=plt.subplots(len(specs),2,figsize=(15,3.8*len(specs)+1.8),squeeze=False)
        figure_title(fig,identity,group,'Fixed-bin temporal and outlier robustness — descriptive, support masked')
        for row,spec in enumerate(specs):
            for ax,names,title in [(axes[row,0],['FULL','DROP_TOP1','DROP_TOP5','NO_2020'],'Fixed exclusions; FULL remains primary'),
                                  (axes[row,1],['PRE_2020','YEAR_2020','YEAR_2021'],'Disjoint dated environments')]:
                for name in names:
                    r=select_rows(bins,identity,spec,name)
                    high=r.loc[r.z_bin.eq(2)].sort_values('x_bin')
                    low=r.loc[r.z_bin.eq(0)].sort_values('x_bin')
                    value=high['mean'].to_numpy()-low['mean'].to_numpy()
                    good=high.display_supported.to_numpy()&low.display_supported.to_numpy()
                    value[~good]=np.nan
                    ax.plot(spec['centers'],value,'o-',ms=3,label=f'{name}: {int(good.sum())}/{spec["actual_bins"]} supported')
                ax.set_xlim(*spec['display_limits']);ax.axhline(0,color='gray',lw=.7)
                ax.set_xlabel(f'{spec["label"]} ({spec["unit"]})')
                ax.set_ylabel('High−low raw conditional level ('+('probability' if identity=='B1' else 'bp')+')')
                ax.set_title(f'{title}\n{spec["label"]} | {spec["state"]} | {spec["cutoff"]} ET')
                ax.legend(fontsize=7)
        fig.text(.02,.015,'All fixed cells/cuts retained; no crisis deletion from primary. Lines only where BOTH states pass display20/10 (+ B1 event counts).\nA constant high−low level is a state main effect; variation over X is the descriptive moderation question. Small subperiod cells often abstain; no stability certification.',fontsize=8)
        fig.subplots_adjust(top=1-1.5/fig.get_size_inches()[1],bottom=1.05/fig.get_size_inches()[1],hspace=.7,wspace=.24)
        save_figure(plt,fig,identity,FILENAMES[4])


def contrast_statistics(frame,spec,y,identity,subset,subset_name,indices,p):
    """Supported raw band difference-of-increments; no fallback after outcome gate."""
    selected = spec['selected']
    candidate = spec['candidates'][selected if selected is not None else 0]
    a0,a1,b0,b1 = candidate['bands']
    x = frame[spec['x']].to_numpy(float)
    states = frame[spec['state']+'_state'].to_numpy()
    mask = panel_mask(frame,spec) & subset
    a = mask & (x>=a0) & (x<=a1)
    b = mask & (x>=b0) & (x<=b1) & ~a
    cell = np.full(len(frame),-1)
    for s in range(3):
        cell[a & (states==s)] = 2*s
        cell[b & (states==s)] = 2*s+1
    draws = grouped_bootstrap(cell,y,indices,6)
    group_id = np.arange(len(frame))//p['bootstrap']['length']
    counts=[int((cell==k).sum()) for k in range(6)]
    groups=[len(np.unique(group_id[cell==k])) for k in range(6)]
    events=[int(y[cell==k].sum()) for k in range(6)] if identity=='B1' else None
    means=np.array([y[cell==k].mean() if counts[k] else np.nan for k in range(6)])
    records=[]
    for low, high in [(0,2),(0,1),(1,2)]:
        needed=[2*low,2*low+1,2*high,2*high+1]
        supported=selected is not None and all(counts[k]>=p['support']['min_n'] and groups[k]>=p['support']['min_groups'] for k in needed)
        display=all(counts[k]>=p['binning']['display_min_n'] and groups[k]>=p['binning']['display_min_groups'] for k in needed)
        if identity=='B1':
            event_ok=all(events[k]>=p['support']['event_min'] and counts[k]-events[k]>=p['support']['nonevent_min'] and
                         len(np.unique(group_id[(cell==k)&(y==1)]))>=p['support']['event_groups_min'] for k in needed)
            supported &= event_ok; display &= event_ok
        d = means[2*high+1]-means[2*high]-means[2*low+1]+means[2*low]
        boot=draws[:,2*high+1]-draws[:,2*high]-draws[:,2*low+1]+draws[:,2*low]
        lo,hi,nb,status=interval(boot,supported,p)
        records.append(dict(experiment=identity,predictor=spec['x'],facet=spec['facet'],state=spec['state'],
                            panel_label=spec['label'],mask=subset_name,comparison=STATES[high]+'-'+STATES[low],
                            candidate=selected,bands=json.dumps(candidate['bands']),n=json.dumps([counts[k] for k in needed]),
                            groups=json.dumps([groups[k] for k in needed]),events=json.dumps([events[k] for k in needed]) if events else '',
                            supported=bool(supported),display_supported=bool(display),
                            estimate=float(d) if supported else np.nan,
                            descriptive_only_estimate=float(d) if display else np.nan,
                            low_state_increment=float(means[2*low+1]-means[2*low]) if supported else np.nan,
                            high_state_increment=float(means[2*high+1]-means[2*high]) if supported else np.nan,
                            ci_low=lo,ci_high=hi,valid_bootstraps=nb,interval_status=status,
                            strong=bool(supported and all(counts[k]>=100 and groups[k]>=30 for k in needed)),
                            estimand='raw broad-X-band increments across RV terciles; partners marginalized; not point D_m'))
    return records


def number(value,unit=''):
    return f'{value:.3g}{unit}' if pd.notna(value) else 'ABSTAIN'


def markdown(frame):
    """Small dependency-free Markdown table, preserving missingness explicitly."""
    escape=lambda v: str(v).replace('|','/').replace('\n',' ')
    return '\n'.join(['| '+' | '.join(frame.columns)+' |', '| '+' | '.join(['---']*len(frame.columns))+' |']+
                     ['| '+' | '.join(escape(v) for v in row)+' |' for row in frame.itertuples(index=False,name=None)])


NOTES = {
    'A2': ('W directly tests late momentum/reversal, with other information marginalized.',
           'A2 is already explored in Stage2B; this is a training-only raw-view audit, not an independent discovery. Broad bands do not hold opening X fixed.'),
    'A3': ('All last5/10/15 and disjoint5-minute acceleration variants are shown; none is selected for a better response.',
           'These overlapping recent-return features are strongly related. Acceleration is a difference of disjoint returns, not a second independent trial.'),
    'A4': ('Gap G and morning I isolate two components of the overnight-inclusive opening predictor.',
           'Simple returns compose multiplicatively: X/10000=(1+G/10000)(1+I/10000)-1. Opening RV shares the morning price path; gap and morning facets do not control for each other.'),
    'A5': ('Signed X, magnitude, two squares and both sign-specific magnitude facets are all retained.',
           'Magnitude/squares remove direction and are dependent transforms, not independent replications. Low-RV large-magnitude support is structurally thin; TRAIN centering is retrospective.'),
    'A6': ('The principal recent state and opening-state comparison use exactly the same W/Y dates.',
           'Recent RV shares 15:00–15:30 prices with W; changed state occupancy can alter composition. Distinct named cutoffs prevent conflating this with opening-RV discretization.'),
    'B1': ('Both early X and late W panels show the fixed Y<−20bp adverse event.',
           'Event scarcity and clustering restrict local probability contrasts. These resampled event rates are not Gaussian-return inference, classifier calibration or forecasts.'),
    'B2': ('Raw30m volume, raw5m volume and strictly prior20-eligible-session relative volume are all shown.',
           'Volume units and normalization change the question; a volume/RV level effect is not moderation. Relative volume loses its first20eligible days. VWAP is omitted because repaired VWAP is null.'),
    'B3': ('One/five/20-session returns end at the previous completed full-session close.',
           'The lag calendar skips scheduled half-days, but retains full sessions with missing opening data. Missing full-close anchors invalidate windows; price returns are not dividend-adjusted total returns.'),
    'C1': ('The fixed, unoptimized sign(W) continuation rule is displayed versus |W|; no policy is learned.',
           'Entry at C15:29/exit at C15:59 assumes immediate availability and fills. Cost0/2/5/10bp is hypothetical; bid/ask, latency and slippage are absent. TRADING_NOT_ESTABLISHED.'),
}


def write_reports(frame,features,plans,bins,contrasts,costs,summary,cuts,qa,p,resources):
    """Self-contained image gallery and separate methods report, using all variants."""
    table=[]
    for _,r in summary.iterrows():
        unit=' probability' if r.experiment=='B1' else 'bp'
        table.append(dict(ID=r.experiment,X=r.primary_predictor,state=r.primary_state,
                          n=f'{r.n_min}–{r.n_max}' if r.n_min!=r.n_max else str(r.n_min),
                          evidence=f'D_HL {number(r.primary_contrast,unit)} [{number(r.ci_low)}, {number(r.ci_high)}]',
                          support=f'{r.primary_cell_support_fraction:.0%} primary cells; {r.supported_primary_family_contrasts} contrasts',
                          caveat=NOTES[r.experiment][1].split('.')[0],verdict=r.rating))
    comparison=markdown(pd.DataFrame(table))
    gallery=['# Experiment B — Initial Visual Audit of Nine Remaining Directions',
             '## How to interpret these plots (TRAINING ONLY / not confirmatory)',
             f'**PASS_WITH_QUALIFICATIONS.** All nine directions and 44 figures use only 1,495 eligible SPY training sessions, {TRAIN[0]}–{TRAIN[1]}. '
             'The original full training sample remains primary. No 2022–2023 response, no 2024–2026 scientific values, no predictive fits, no new source requests and no trading optimization were used.',
             'The lines are empirical binned means/rates, **not learned EBM curves**. Blue/green/orange denote low/middle/high RV. '
             'Display support requires 20 dates / 10 distinct five-row groups; contrast/interval support requires 50/20 (strong 100/30). '
             'Groups measure occupancy, not proven independence. B1 additionally needs 5 events, 5 nonevents and 3 event-bearing groups. '
             'Gray/missing cells abstain; gaps are never bridged. Predictor-only display limits hide tails visually but preserve all outcomes in estimates.',
             'Whiskers are exploratory 95% percentile variability intervals from 300 shared joint circular five-day resamples, conditional on fixed bins/cuts/masks. '
             'Nonstationarity, serial dependence, heavy tails, data reuse and eight-family selection preclude theorem-certified or post-selection population coverage. '
             'Differences of within-state predictor increments address moderation; a high-state outcome level or variance alone does not.',
             'All panels share [feature definitions](registries/feature_definitions.csv), '
             '[frozen protocol](config/initial_audit_protocol_v1.json), '
             '[numerical predictor-only design](registries/predictor_only_design.json) and '
             '[source/output hashes](registries/initial_audit_manifest.json). '
             'See [prior A1/A2 closeout](../../../reports/B/stage2C_literature_anchored_A1_A2_closeout.md) as historical context only; A1 was not rerun.',
             '## One-page comparison and ranked review (include C1 as deferred)',comparison,
             '**NO_CLEAR_WINNER.** No direction passes the frozen conjunctive PROMISING_TO_TEST rubric. Ratings use the first prespecified panel; every variant is displayed and reported below. '
             'C1 is deferred regardless of gross payoff. Effect units differ, so no cross-target effect-size ranking is made. '
             f'All-feature common-date sensitivity has n={qa["common_dates_n"]}; exact direction/variant masks and dates are in the registries.']
    descriptions=[]
    for identity,specs in plans.items():
        r=summary.loc[summary.experiment.eq(identity)].iloc[0]
        gallery += [f'## {identity} — {p["directions"][identity]["title"]}',
                    '### Scientific question and feature/target definitions',NOTES[identity][0],
                    f'Target: {y_unit(identity)}. Panels: '+ '; '.join(f'{s["label"]} ({s["unit"]}), {s["state"]}, known {s["cutoff"]} ET, n={s["n"]}, {s["first"]}–{s["last"]}' for s in specs)+'.']
        individual=[]
        for spec in specs:
            c=select_contrasts(contrasts,identity,spec).iloc[0]
            common_c=select_contrasts(contrasts,identity,spec,'COMMON_DATES').iloc[0]
            cells=select_rows(bins,identity,spec)
            valid=cells.loc[cells.display_supported]
            span=f'{valid["mean"].min():.3g} to {valid["mean"].max():.3g}' if len(valid) else 'none supported'
            individual.append(dict(panel=spec['label'],n=spec['n'],supported_curve_cells=f'{cells.contrast_level_supported.sum()}/{len(cells)}',
                                   displayed_mean_range=span,D_HL=number(c.estimate),
                                   interval=f'[{number(c.ci_low)}, {number(c.ci_high)}]',
                                   low_increment=number(c.low_state_increment),high_increment=number(c.high_state_increment),status=c.interval_status))
            individual[-1]['D_HL_common_dates']=number(common_c.estimate)
        desc=markdown(pd.DataFrame(individual))
        gallery += [desc]
        # Narrative describes this hash-frozen dataset, never an extra selector.
        details = {
            'A2': 'The high-state W increment is positive in the selected bands, but its difference from the low-state increment has a wide interval crossing zero. The orange raw curve is jagged rather than a stable continuation slope.',
            'A3': 'The last 5 and last 10 contrasts point in opposite directions; last 15 and acceleration are nearer zero. None of their H−L intervals excludes zero. That endpoint dependence argues against treating the visually strongest recent-return panel as a discovery.',
            'A4': 'Gap G has a negative H−L increment contrast whose nominal exploratory interval excludes zero; the morning I contrast remains interval-inconclusive. All three fixed exclusions retain the gap sign, but only one temporal comparison meets even the weaker display-support gate. The gap deserves visual scrutiny, with multiplicity and missing temporal confirmation kept explicit.',
            'A5': '|X| and X² give identical rank-bin contrasts because squaring is monotone on nonnegative magnitude; these are the same observations, not replication. Signed-X, magnitude, centered-square and positive-sign intervals cross zero. The negative-sign magnitude contrast abstains for joint support.',
            'A6': 'Replacing opening RV by recent RV leaves an interval-inconclusive W increment contrast. Only 61.1% of days keep the same state, so visually different curves partly reflect regrouping. Neither state specification establishes moderation or a preference for a new model.',
            'B1': 'There are 217 adverse days out of 1,495 (14.5%), with 52 adjacent event pairs. The early-X H−L contrast fails because one necessary cell has only four events. The supported late-W contrast is near zero with a broad probability interval; a higher high-state event level is not changed momentum response.',
            'B2': 'Raw 30m and 5m volume contrasts are positive while relative volume is negative, and all H−L intervals cross zero. Normalization changes the feature meaning; the sign difference cannot justify choosing whichever scale looks favorable. Relative volume ranges to 7.90× and has 20 warmup days.',
            'B3': 'The one-session primary contrast is small relative to daily Y noise and its interval crosses zero; five-session evidence is also weak, while the 20-session estimate points negative with an interval crossing zero. These differing horizons provide no coherent moderation signal.',
            'C1': 'The all-day fixed-rule gross mean is 0.833 bp, with an exploratory interval spanning zero. Hypothetical net means at 2/5/10 bp costs are −1.14/−4.09/−9.01bp; implied gross break-even is only 0.846 bp per active day. Zero-signal days (23) stay flat. These assumptions are not executable alpha evidence.',
        }
        gallery += [details[identity]]
        captions=[
            f'All {len(specs)} prespecified panel(s) are shown. Raw points include crisis days. '
            f'Primary viewing-window exclusions are {specs[0]["clipped_predictor_count"]} predictor-tail points; estimates retain them. '
            f'Displayed primary curve cells: {select_rows(bins,identity,specs[0]).display_supported.sum()}/24; numerical state increments appear in the table above.',
            f'Intervals abstain where date/group or event support fails. Primary H−L increment difference is '
            f'{number(r.primary_contrast)} [{number(r.ci_low)}, {number(r.ci_high)}], status {r.interval_status}. '
            + ('All four cost scenarios use the same fixed rule and dates; they are illustrative, not observed net executions.' if identity=='C1' else 'Cell n/group counts accompany the means, and rare-event counts are printed for B1.'),
            'These are raw empirical responses across continuous log-RV cells, with cell counts and separately marked terciles. '
            f'{specs[0]["state"]} is the principal state. Gray cells forbid a continuous-surface inference; brighter extremes can be noisy.',
            f'Across all displayed variants: {r.supported_primary_family_contrasts} supported and '
            f'{r.abstained_primary_family_contrasts} abstained FULL pairwise state contrasts. '
            + ('The right panel is a hypothetical cost break-even diagnostic; it is not a learned-model interaction.' if identity=='C1' else
               'The first qualifying predictor-only bands and all required endpoint counts are shown; broad-band partners are marginalized rather than held fixed.'),
            f'For the primary panel, {r.fixed_exclusion_same_sign}/{r.fixed_exclusion_supported} supported fixed-exclusion contrasts keep the FULL sign; '
            f'{r.temporal_same_sign_display_level}/{r.temporal_display_supported} temporal contrasts agree at the weaker display-level support threshold. '
            'Each line remains on the original bin grid; the high−low level difference alone is not a moderator effect.',
        ]
        count=4 if identity=='C1' else 5
        names=['Raw scatter and state lines','Conditional means with intervals','Raw X–Z conditional-response heatmap',
               'Support and state contrasts','Temporal and outlier robustness']
        for i in range(count):
            gallery += [f'### Figure {i+1}: {names[i]}',f'![{identity} {names[i]}](figures/{identity}/{FILENAMES[i]})',captions[i]]
        gallery += ['### What looks promising, and why',
                    f'The inputs are available without acquisition; primary n={r.primary_n}. '
                    f'The supported primary effect/noise ratio is {number(r.effect_noise_ratio)}; '
                    f'{r.primary_cell_support_fraction:.0%} of primary state×X cells pass contrast-level support. '
                    + ('The fixed-rule display shows where hypothetical costs exceed gross means; it cannot nominate an EBM.' if identity=='C1' else
                       'The raw increments and every variant above provide a concrete candidate to falsify, rather than evidence of model superiority.'),
                    '### What argues against it / key limitations / support / uncertainty',NOTES[identity][1],
                    f'The primary interval '+('excludes' if r.interval_excludes_zero else 'does not exclude / cannot assess')+
                    f' zero. Fixed-exclusion supported sign reversals: {r.sign_reversals_fixed_exclusions}; '
                    'unsupported sensitivities cannot establish stability. Broad-band state compositions differ, and the direction was screened with seven other families.',
                    '### Feasibility verdict, new data needed, and recommended next model stage',
                    f'**{r.rating}.** No new data are needed for this descriptive audit. '
                    + ('Actual execution/fill/cost evidence and a separately frozen learned-model protocol are prerequisites to a later trading study.' if identity=='C1' else
                       'No model stage is automatically authorized by a visual pattern. If selected after human review, freeze one primary predictor/state contrast, its supported mask and simple state-aware/additive comparators before any future model work. Do not reopen reserved/sealed outcomes for this triage.')]
        descriptions.append(f'### {identity}\n\n{NOTES[identity][0]} {NOTES[identity][1]}\n\n{details[identity]}\n\n{desc}\n\n'
                            f'Rating **{r.rating}**; fixed exclusion same-sign {r.fixed_exclusion_same_sign}/{r.fixed_exclusion_supported}; temporal display-level {r.temporal_same_sign_display_level}/{r.temporal_display_supported}.')
    gallery += ['## Final decision: prospective experiments to prioritize, unresolved data needs, multiplicity, protocol freeze and what would falsify candidate state dependence',
                'No family is confirmatory. Review the apparent A4 gap contrast and its missing temporal support first, then A6 against its opening-state control and the A5/B1 support limitations; this concerns interpretation, not a validation-based ranking. '
                'A replicated change of increments on a supported predeclared grid would be the next falsifiable claim. '
                'Loss of that difference under fixed exclusions, different environments, stronger additive/state-aware baselines or future properly reserved evaluation would argue against it. '
                'Eight-family exploration and dependent transforms incur multiplicity. A later selected analysis needs a fresh frozen protocol with stagewise/hierarchical multiplicity and appropriately scoped full-process null assumptions; no such fits/nulls occur here. '
                'NO_CLEAR_WINNER and supported ABSTAIN are valid outcomes. C1 stays MODEL_DEPENDENT / DEFER.',
                '## Reproduction commands and link to technical report',
                'With the matching authorized canonical sources available under `EBM_DATA_ROOT` (default `data/`), use the existing environment: '
                '`python -B scripts/b_initial_audit.py run` then `python -B scripts/b_initial_audit.py qa`. '
                'On a new checkout lacking this audit protocol, run `freeze` first. No provider credentials or network are used by this stage. '
                'Install the project and the existing pinned `requirements-stage2B.lock.txt` on a fresh machine; licensed/private input acquisition remains a prerequisite.',
                '[Technical report](../../../reports/B/initial_audit_nine_experiments_feasibility.md). '
                '[Detailed cell results](registries/empirical_bins_and_support.csv); '
                '[all contrasts and sensitivities](registries/empirical_state_contrasts.csv).']
    (OUT/'NINE_EXPERIMENTS_VISUAL_REVIEW.md').write_text('\n\n'.join(gallery)+'\n')
    (OUT/'README.md').write_text('# Initial nine-direction visual audit\n\n'
        '**TRAINING ONLY, descriptive, no predictive fits or executable alpha claims.**\n\n'
        'Open [the self-contained visual review](NINE_EXPERIMENTS_VISUAL_REVIEW.md) for all 44 plots and nine assessments. '
        'Inputs reference one immutable canonical daily table and training-minute partitions with the sole D2.1c overlay. '
        'No original minute/daily prices are duplicated here; the ignored Parquet stores new features/session keys only. '
        'Community-source rights and adjustment qualifications remain; do not redistribute private raw inputs.\n\n'
        'Protocol, numerical design, source preservation snapshot, feature definitions, empirical results and checked manifest are in `config/` and `registries/`. '
        'Reproduce: `python -B scripts/b_initial_audit.py run`, then `python -B scripts/b_initial_audit.py qa`.\n')
    common=['# Experiment B — Initial audit of nine remaining directions',
            '**PASS_WITH_QUALIFICATIONS.** Nine data-supported sections, 44 figures (36 mandatory + 8 robustness). '
            'ABSTAIN is intentional for inadequate support. There were no predictive fits, new downloads, validation-response reads or sealed scientific reads.',
            '[Visual gallery](../../artifacts/B/initial_audit/NINE_EXPERIMENTS_VISUAL_REVIEW.md).',
            '## Sources, sample and timing',
            f'Daily source **{p["source_id"]}**, SHA256 `{p["daily"]["sha256"]}`. '
            'Immutable Alpaca SIP split-adjusted D2 + exactly 39 D2.1c native missing-key repairs, never D2.1b. '
            f'This run projects only 2016–2021 minute/daily scientific columns before transforms: {qa["training_minutes"]} minute rows, '
            f'{qa["native_patch_training_rows"]} training patch rows, 1,495 eligible days. '
            'Full-file byte hashes may include later periods; they do not deserialize scientific values. '
            'The full table 2680 / 2675 eligible and later 497 / 683 split counts are frozen metadata only. '
            'Session keys are unique; opening-missing days remain excluded; the original primary training population is intact.',
            'UTC timestamps label bar starts; ET conversion uses zoneinfo and XNYS schedule. '
            'E uses completed bars through 09:59 at 10:00; L through 15:29 at 15:30. '
            'Y=10000(C15:59/C15:29−1) is observed 16:00. One-minute RV includes first open→close plus 29 adjacent-close increments. '
            'Vendor latency is unknown. Half-days are skipped only in prior-full anchors; missing full anchors never fall back. '
            'B3 uses all scheduled full-session historical close anchors, including days with incomplete opening RV, and requires every anchor in the lag window.',
            '## Precommit, features and masks',
            f'Protocol SHA256 `{sha(PROTOCOL)}` frozen before response exploration. Numerical predictor-only bins, masks, endpoint candidates and recent-state cuts were written before loading Y; their hash is in the manifest. '
            'Opening logcuts '+str(cuts['rv_open_log'])+'; **separate recent logcuts** '+str(cuts['rv_late_log'])+'. Equality belongs to the lower state. '
            f'TRAIN meanX for centered square={qa["x_mean_train_bp"]:.12g}bp. These TRAIN retrospectives are descriptive, not historical live cutoffs.',
            markdown(feature_registry(frame,features,p)[['feature','formula','unit','earliest_usable_time_ET','n','missing','warmup']].fillna('')),
            'The feature-only Parquet has '+str(features.shape)+' (including session key), no target/price/original-daily copies. '
            f'B2 relative volume initializes after 20 eligible days; common all-feature n={qa["common_dates_n"]}. '
            'Sign facets use the pooled magnitude bin boundaries. Exact per-variant n/effective dates and missing masks are in predictor_only_design.json; '
            'ALL families additionally have the common-date mask in the contrast/bin registries. Rankings do not compare bp/probability/shares scales as if commensurable.',
            'Fixed sensitivities: FULL, DROP_TOP1='+str(p['exclusions']['DROP_TOP1'])+', DROP_TOP5='+str(p['exclusions']['DROP_TOP5'])+
            ', NO_2020, PRE_2020, YEAR_2020, YEAR_2021, COMMON_DATES. All endpoints/bins/cutoffs remain FULL-training fixed; no outlier reranking. '
            'The optional VWAP, reversal rule,−40bp event, past-volatility and late5 recent-RV expansion are intentionally omitted.',
            '## Raw bins, uncertainty and support',
            'Pooled predictor-only 8 quantile bins, deterministic unique-edge ties; a 5-bin sensitivity is retained in metadata/results and not used for ranking. '
            'Heatmaps use8×6 predictor/log-RV quantile cells, spaced evenly for legibility with numerical X medians and log-RV interval labels; they retain all tails. Scatter/curve display limits are predictor0.5/99.5percentiles; all tails remain in numerical estimates. '
            'Means/lines display at 20 dates / 10 five-row groups; uncertainty and cross-state contrasts require 50/20 per necessary cell, strong 100/30. '
            'Heatmaps below display support are gray; no interpolation. Group identifiers are floor(original eligible row/5), unchanged under masks; occupancy does not prove independent blocks.',
            'Candidate endpoint quantile bands, in order: '+str(p['contrast_candidates'])+'. Select first passing all six predictor-band×state date/group cells before reading Y. '
            'B1 subsequently requires 5 events, 5 nonevents and 3 event-bearing groups in each necessary cell; failure abstains without trying a different endpoint pair. '
            'Reported D_HL=(mean_b,H−mean_a,H)−(mean_b,L−mean_a,L), plus M−L and H−M. '
            'These broad-band, partner-marginal empirical means differ from pointwise D_m and from a fixed-partner EBM surface. '
            'Missing intervals/estimates are not zeros; separately labeled descriptive-only values at weaker 20/10 support are used only for the predeclared temporal feasibility screen.',
            'Circular joint eligible-day block bootstrap: seed 20261016, length 5, 300 replicates shared across all states/variants, fixed bins and already-causal lagged features; '
            '2.5/97.5percentiles, at least 270 finite draws and nondegenerate width. Resampling conditions on feature construction and thresholds; no raw-minute resampling, full learner/selection reconstruction or formal event-probability coverage is claimed. '
            'For fixed masks the original joint sequence is resampled with that mask, so excluded dates do not create artificial adjacency. '
            'Nonstationarity, heavy tails, dependent events and eight-family exploration qualify every interval. No independent state shuffle or Gaussian event bars. Optional block10 sensitivity omitted without response-based selection.',
            '## Nine-family results and frozen rubric',comparison,
            'Ratings apply the exact conjunctive protocol rubric to the first prespecified panel, never the best variant. '
            'PROMISING needs support, an interval excluding 0, a nontrivial raw effect relative to noise, all three exclusion signs, at least two temporal signs with disclosed weaker support, and ≥50% cell support. '
            'LOW_PRIORITY requires a supported small/interval-inconclusive effect or severe supported sign instability; unavailable/weak support is INCONCLUSIVE, not proof of absence. '
            'C1 is always MODEL_DEPENDENT / DEFER. No composite score or winner is forced.',
            *descriptions,
            '## Additional diagnostics',
            'B1 event prevalence, event-bearing groups and clustering; B2 relative-volume tails/warmup; B3 lag warmup and early-session mappings; A6 state cross-occupancy; '
            'C1 scenario means and break-even values are recorded in `registries/feature_and_state_diagnostics.json` and `registries/illustrative_cost_scenarios.csv`. '
            'Source1 terminal-repair dependence on 2019-08-12/13 and unverified community upstream redistribution rights/adjustment remain prior-source qualifications. '
            'No source fidelity, raw-shape theorem, causal, predictive or trading superiority claim follows.',
            '## QA, resource use and reproduction',
            f'Seven independent real-date scalar checks cover DST transition, half-day skip, native repair, crisis day and2021 gap context. '
            'Checks include endpoints, disjoint acceleration, all 30RV increments, volume sums, strictly prior20volume and lagged close equations. '
            'Focused deterministic tests cover current-day exclusion, missing interior anchors, timestamp endpoints, return units, bootstrap joint cells and degenerate/support abstention. '
            'Manifest records output reads, preservation hashes, PNG/gallery QA and actual software versions. See mandatory session report for commands/failures and visual inspection.',
            'Run `python -B scripts/b_initial_audit.py run` then `python -B scripts/b_initial_audit.py qa` in the existing environment. '
            'Fresh setup: install the project and pinned requirements-stage2B.lock.txt, supply matching authorized canonical sources via EBM_DATA_ROOT, then use the already frozen protocol. '
            'No credentials/API are accessed. Scope is offline SPY/B only. ',
            f'Numerical/plot run resource measurements are in the final manifest; statistics elapsed before publication={resources["analysis_wall_seconds"]:.2f}s. '
            'All44figurepaths have exact manifest hashes; new-feature schema/bytes are registered. No user files moved/deleted; no prior results overwritten.',
            '## Handoff',
            'Human-review the standalone gallery before nominating another experiment. A6 is a comparison of two measured states, A3 extends late returns, A5/B1 illustrate support constraints, and C1 lacks execution evidence. '
            'Any later model stage needs a separately approved frozen predictor/state/contrast and matched simple baselines, multiplicity/selection plan and honest future evaluation. '
            'The original A1/A2 inconclusive developmental closeout remains unchanged.']
    (ROOT/'reports/B/initial_audit_nine_experiments_feasibility.md').write_text('\n\n'.join(x.rstrip() for x in common)+'\n')


def diagnostics(frame,features,cuts,indices,p):
    """Small feature-only/event/support metadata, never a duplicate research table."""
    events=frame.y_last30_bp.lt(p['event_threshold_bp']).to_numpy()
    groups=np.arange(len(frame))//5
    adjacent=int(np.sum(events[:-1]&events[1:]))
    state_counts=pd.crosstab(frame.rv_open_log_state,frame.rv_late_log_state).to_numpy().tolist()
    record=dict(event=dict(threshold_bp=p['event_threshold_bp'],events=int(events.sum()),nonevents=int((~events).sum()),
                           prevalence=float(events.mean()),event_bearing_groups=len(np.unique(groups[events])),
                           adjacent_event_pairs=adjacent,
                           per_year={str(y):int(events[frame.session_et.astype(str).str.startswith(str(y))].sum()) for y in range(2016,2022)}),
                A6=dict(opening_recent_cross_counts=state_counts,row_state='opening low/middle/high',column_state='recent low/middle/high',
                        same_state_fraction=float(frame.rv_open_log_state.eq(frame.rv_late_log_state).mean()),named_log_cutoffs=cuts),
                relative_volume=dict(n=int(features.relative_late_volume.notna().sum()),
                                     first=str(features.loc[features.relative_late_volume.notna(),'session_et'].min()),
                                     quantiles={str(q):float(features.relative_late_volume.quantile(q)) for q in [0,.01,.5,.99,1]}),
                lag_warmup={str(h):dict(n=int(features[f'lag_close_{h}_bp'].notna().sum()),
                                        missing=int(features[f'lag_close_{h}_bp'].isna().sum()),
                                        first=str(features.loc[features[f'lag_close_{h}_bp'].notna(),'session_et'].min())) for h in [1,5,20]},
                C1=dict(zero_signal_days=int(frame.w_preclose_bp.eq(0).sum()),execution=p['execution']))
    payoff=response(frame,'C1',p); active=frame.w_preclose_bp.ne(0).to_numpy()
    rows=[]
    state=frame.rv_open_log_state.to_numpy()
    for cost in p['costs_bp']:
        y=payoff-cost*active
        for s in range(4):
            mask=(state==s) if s<3 else np.ones(len(frame),bool)
            cells=np.where(mask,0,-1)
            draws=grouped_bootstrap(cells,y,indices,1)[:,0]
            lo,hi,nb,status=interval(draws,True,p)
            rows.append(dict(state=STATES[s] if s<3 else 'all',cost_bp=cost,n=int(mask.sum()),
                             mean=float(y[mask].mean()),ci_low=lo,ci_high=hi,valid_bootstraps=nb,interval_status=status,
                             gross_break_even_cost_bp=float(payoff[mask].sum()/active[mask].sum()),
                             execution='hypothetical C15:29–C15:59; no observed fills/spreads/slippage'))
    return record,pd.DataFrame(rows)


def qa_outputs(preserve=True):
    """Minimal PNG/link/schema/preservation QA; no models or later outcomes read."""
    p=read_json(PROTOCOL)
    plt=plot_setup()
    figures=[]
    for identity in p['directions']:
        for name in FILENAMES[:4 if identity=='C1' else 5]:
            path=OUT/'figures'/identity/name
            if not path.exists() or path.stat().st_size<1000:
                raise ValueError('Missing/empty mandatory figure '+str(path.relative_to(ROOT)))
            img=plt.imread(path)
            if img.ndim!=3 or img.shape[0]<400 or img.shape[1]<800 or np.std(img)<.01:
                raise ValueError('Unreadable/blank figure '+str(path))
            figures.append(file_ref(path,ROOT))
    gallery=(OUT/'NINE_EXPERIMENTS_VISUAL_REVIEW.md').read_text()
    links=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',gallery)
    if len(links)!=44 or not all((OUT/link).is_file() for link in links):
        raise ValueError('Gallery image links/count do not resolve')
    derived=OUT/'derived/initial_audit_new_features.parquet'
    columns=pq.read_schema(derived).names
    forbidden={'y_last30_bp','P16','P1530','timestamp_utc','x_open_bp','w_preclose_bp','rv_open_log'}
    if forbidden.intersection(columns):
        raise ValueError('Feature-only table contains copied original/target data')
    features=pd.read_parquet(derived,columns=['session_et'])
    guard_training(features,dict(train=TRAIN))
    if len(features)!=1495:
        raise ValueError('Wrong feature-table date population')
    contrasts=pd.read_csv(OUT/'registries/empirical_state_contrasts.csv')
    intervals=contrasts.interval_status.eq('EXPLORATORY_BLOCK_PERCENTILE')
    if not contrasts.loc[intervals,'supported'].all() or not contrasts.loc[intervals,'valid_bootstraps'].ge(270).all():
        raise ValueError('Unsupported/fabricated contrast interval')
    if contrasts.loc[~contrasts.supported,['estimate','ci_low','ci_high']].notna().any().any():
        raise ValueError('Unsupported scientific estimate/interval must be missing')
    bins=pd.read_csv(OUT/'registries/empirical_bins_and_support.csv')
    if not (bins.groups.le(bins.n)&bins.n.ge(0)).all():
        raise ValueError('Invalid cell/group counts')
    event=bins.loc[bins.experiment.eq('B1')]
    if not event.events.add(event.nonevents).eq(event.n).all():
        raise ValueError('B1 event/nonevent counts do not reconcile')
    ci=bins.interval_status.eq('EXPLORATORY_BLOCK_PERCENTILE')
    if not bins.loc[ci,'contrast_level_supported'].all() or not bins.loc[ci,'valid_bootstraps'].ge(270).all():
        raise ValueError('Cell uncertainty fails declared support/draw rule')
    verified=0
    if preserve:
        for ref in read_json(OUT/'registries/start_snapshot.json')['files']:
            path=(ROOT if ref['base']=='repo' else root_data())/ref['path']
            if not path.exists() or path.stat().st_size!=ref['bytes'] or sha(path)!=ref['sha256']:
                raise ValueError('Preexisting input changed: '+ref['path'])
            verified+=1
    result=dict(status='PASS',figure_count=len(figures),image_links=len(links),figures=figures,
                preexisting_files_verified_unchanged=verified,feature_rows=len(features),feature_columns=columns,
                primary_contrasts=len(contrasts.loc[contrasts['mask'].eq('FULL')]),
                primary_abstained=int((~contrasts.loc[contrasts['mask'].eq('FULL'),'supported']).sum()),
                all_mask_contrasts=len(contrasts),all_mask_abstained=int((~contrasts.supported).sum()),
                empirical_cell_rows=len(bins),empirical_cells_with_intervals=int(ci.sum()),
                no_supported_zero_width_intervals=bool((contrasts.loc[intervals,'ci_high']>contrasts.loc[intervals,'ci_low']).all()))
    write_json(OUT/'registries/output_QA.json',result)
    return result


def run():
    """One bounded descriptive run; freeze numerical design before response I/O."""
    wall=time.perf_counter();cpu=time.process_time();free=shutil.disk_usage(ROOT).free
    p=read_json(PROTOCOL);protocol_sha=sha(PROTOCOL);data=root_data()
    verify_files(data,p['data_refs'])
    frame,features,cuts,qa=feature_layer(data,p)
    plans,common=design(frame,p,cuts)
    numerical=dict(created_before_outcome_read=True,protocol_sha256=protocol_sha,
                   cutoffs_log=cuts,plans=plans,common_dates_n=int(common.sum()),
                   common_first=str(frame.loc[common,'session_et'].min()),common_last=str(frame.loc[common,'session_et'].max()))
    numerical_path=OUT/'registries/predictor_only_design.json'
    if numerical_path.exists():
        if read_json(numerical_path)!=numerical:
            raise ValueError('Predictor design changed from frozen run; inspect before proceeding')
    else:
        write_json(numerical_path,numerical)
    numerical_sha=sha(numerical_path)
    outcome_read_at=dt.datetime.now(dt.timezone.utc).isoformat()
    y=read_training(data/p['daily']['path'],['y_last30_bp'],eligible=True,start=TRAIN[0])
    frame=frame.merge(y,on='session_et',validate='one_to_one')
    guard_training(frame,dict(train=TRAIN))
    if len(frame)!=1495 or not np.isfinite(frame.y_last30_bp).all():
        raise ValueError('Training outcome integrity failure')
    indices=circular_indices(len(frame),**{k:p['bootstrap'][k] for k in ['B','length','seed']})
    subsets=masks(frame,p,common);bins=[];contrasts=[]
    for identity,specs in plans.items():
        target=response(frame,identity,p)
        for spec in specs:
            for name,subset in subsets.items():
                bins+=cell_statistics(frame,spec,target,identity,subset,name,indices,p)
                contrasts+=contrast_statistics(frame,spec,target,identity,subset,name,indices,p)
            bins+=cell_statistics(frame,spec,target,identity,subsets['FULL'],'FULL',indices,p,kind='heatmap')
            bins+=cell_statistics(frame,spec,target,identity,subsets['FULL'],'FULL',indices,p,bin_count=5)
            if identity=='C1':
                for cost in p['costs_bp']:
                    value=target-cost*frame.w_preclose_bp.ne(0).to_numpy()
                    bins+=cell_statistics(frame,spec,value,identity,subsets['FULL'],f'FULL_COST_{cost}',indices,p)
        print(f'{identity}: numerical descriptive screen complete',flush=True)
    bins=pd.DataFrame(bins);contrasts=pd.DataFrame(contrasts)
    summary=summarize(frame,plans,bins,contrasts,p)
    diag,costs=diagnostics(frame,features,cuts,indices,p)
    (OUT/'derived').mkdir(parents=True,exist_ok=True)
    features.to_parquet(OUT/'derived/initial_audit_new_features.parquet',index=False,compression='zstd')
    registry=OUT/'registries'
    for name,table in [('feature_definitions',feature_registry(frame,features,p)),('empirical_bins_and_support',bins),
                       ('empirical_state_contrasts',contrasts),('experiment_feasibility_summary',summary),
                       ('illustrative_cost_scenarios',costs)]:
        table.to_csv(registry/(name+'.csv'),index=False)
    write_json(registry/'feature_and_state_diagnostics.json',diag)
    qa['common_dates_n']=int(common.sum())
    qa['masks']={name:dict(n=int(mask.sum()),first=str(frame.loc[mask,'session_et'].min()),last=str(frame.loc[mask,'session_et'].max())) for name,mask in subsets.items()}
    write_json(registry/'feature_QA.json',qa)
    plots(frame,plans,bins,contrasts,costs,cuts,p)
    resources=dict(analysis_wall_seconds=time.perf_counter()-wall)
    write_reports(frame,features,plans,bins,contrasts,costs,summary,cuts,qa,p,resources)
    output_qa=qa_outputs()
    if sha(PROTOCOL)!=protocol_sha or sha(numerical_path)!=numerical_sha:
        raise ValueError('Frozen design unexpectedly modified')
    files=[path for path in OUT.rglob('*') if path.is_file() and path.name!='initial_audit_manifest.json'
           and path.suffix!='.log' and 'matplotlib_cache' not in path.parts]
    manifest=dict(task_id=p['task_id'],status='PASS_WITH_QUALIFICATIONS',
                  created_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                  protocol_sha256=protocol_sha,numerical_design_sha256=numerical_sha,
                  numerical_design_before_outcome=True,outcome_read_at_utc=outcome_read_at,
                  source_dataset=p['source_id'],source_refs=p['data_refs'],source_root='EBM_DATA_ROOT, default data/',
                  training_range=TRAIN,training_rows=1495,eligible_rows_by_direction=summary[['experiment','n_min','n_max']].to_dict('records'),
                  input_read_trace=READS,validation_outcome_rows_read=0,sealed_scientific_rows_read=0,
                  model_fit_calls=0,network_requests=0,new_raw_copies=0,deleted_files=[],
                  cutoffs_log=cuts,bootstrap=p['bootstrap'],qa=output_qa,
                  new_feature_table=file_ref(OUT/'derived/initial_audit_new_features.parquet',ROOT),
                  code=[file_ref(ROOT/x,ROOT) for x in ['src/ebm_research/experiment_b/initial_audit.py','scripts/b_initial_audit.py']],
                  environment=dict(python=platform.python_version(),**{k:metadata.version(k) for k in ['numpy','pandas','pyarrow','matplotlib','exchange-calendars']}),
                  git_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),
                  resources=dict(wall_seconds=time.perf_counter()-wall,cpu_seconds=time.process_time()-cpu,
                                 new_audit_bytes=sum(f.stat().st_size for f in files),
                                 figure_bytes=sum(r['bytes'] for r in output_qa['figures']),
                                 free_disk_before=free,free_disk_after=shutil.disk_usage(ROOT).free),
                  outputs=[file_ref(path,ROOT) for path in sorted(files)],
                  technical_report=file_ref(ROOT/'reports/B/initial_audit_nine_experiments_feasibility.md',ROOT),
                  qualifications=['exploratory fixed-band variability, not point/theorem/postselection inference',
                                  'A2 not independent discovery; prior A1/A2 closeout unchanged',
                                  'C1 hypothetical execution/cost assumptions, TRADING_NOT_ESTABLISHED',
                                  'no source-rights/adjustment limitations repaired by this audit'])
    write_json(registry/'initial_audit_manifest.json',manifest)
    print(summary[['experiment','n_min','n_max','rating','primary_contrast']].to_string(index=False),flush=True)
    print(json.dumps(dict(status=manifest['status'],resources=manifest['resources'],
                          primary_abstained=output_qa['primary_abstained'],all_mask_abstained=output_qa['all_mask_abstained'])),flush=True)


def publish():
    """Republish plot/prose formatting from fixed numerical outputs; no bootstrap rerun."""
    wall=time.perf_counter();cpu=time.process_time()
    p=read_json(PROTOCOL);registry=OUT/'registries'
    manifest=read_json(registry/'initial_audit_manifest.json')
    numerical=read_json(registry/'predictor_only_design.json')
    if sha(PROTOCOL)!=manifest['protocol_sha256'] or sha(registry/'predictor_only_design.json')!=manifest['numerical_design_sha256']:
        raise ValueError('Publication cannot alter frozen design')
    names=['empirical_bins_and_support','empirical_state_contrasts','experiment_feasibility_summary',
           'illustrative_cost_scenarios']
    before={name:sha(registry/(name+'.csv')) for name in names}
    tables={name:pd.read_csv(registry/(name+'.csv')) for name in names}
    features=pd.read_parquet(OUT/'derived/initial_audit_new_features.parquet')
    daily=read_training(root_data()/p['daily']['path'],
                        ['x_open_bp','w_preclose_bp','rv_open_log','y_last30_bp'],eligible=True,start=TRAIN[0])
    frame=daily.merge(features,on='session_et',validate='one_to_one')
    guard_training(frame,dict(train=TRAIN))
    cuts=numerical['cutoffs_log']
    for state,values in cuts.items():
        frame[state+'_state']=np.searchsorted(values,frame[state],side='left')
    plots(frame,numerical['plans'],tables[names[0]],tables[names[1]],tables[names[3]],cuts,p)
    qa=read_json(registry/'feature_QA.json')
    write_reports(frame,features,numerical['plans'],tables[names[0]],tables[names[1]],tables[names[3]],tables[names[2]],cuts,qa,p,
                  dict(analysis_wall_seconds=manifest['resources']['wall_seconds']))
    output_qa=qa_outputs()
    if before!={name:sha(registry/(name+'.csv')) for name in names}:
        raise ValueError('Publication modified numerical results')
    elapsed=time.perf_counter()-wall
    manifest['publication']=dict(wall_seconds=elapsed,cpu_seconds=time.process_time()-cpu,
        purpose='Count-label spacing, quantile-spaced numerical heatmap axes and fuller fixed-result narrative; no numerical choices changed',
        numerical_CSV_hashes_unchanged=before,bootstrap_reruns=0,input_read_trace=READS)
    history=manifest.setdefault('publication_history',[])
    history.append(manifest['publication'].copy())
    manifest['qa']=output_qa
    manifest['resources']['figure_bytes']=sum(r['bytes'] for r in output_qa['figures'])
    manifest['resources']['cumulative_compute_wall_seconds']=manifest['resources']['wall_seconds']+sum(r['wall_seconds'] for r in history)
    manifest['resources']['cumulative_cpu_seconds']=manifest['resources']['cpu_seconds']+sum(r['cpu_seconds'] for r in history)
    files=[f for f in OUT.rglob('*') if f.is_file() and f.name!='initial_audit_manifest.json'
           and f.suffix!='.log' and 'matplotlib_cache' not in f.parts]
    manifest['outputs']=[file_ref(f,ROOT) for f in sorted(files)]
    manifest['resources']['new_audit_bytes']=sum(f.stat().st_size for f in files)
    manifest['code']=[file_ref(ROOT/x,ROOT) for x in ['src/ebm_research/experiment_b/initial_audit.py','scripts/b_initial_audit.py']]
    manifest['technical_report']=file_ref(ROOT/'reports/B/initial_audit_nine_experiments_feasibility.md',ROOT)
    write_json(registry/'initial_audit_manifest.json',manifest)
    print(json.dumps(dict(status='PUBLICATION_QA_PASS',seconds=elapsed,figures=44,numerical_outputs_unchanged=True)))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['freeze','run','publish','qa'])
    args=parser.parse_args()
    if args.action=='freeze':
        freeze()
    elif args.action=='publish':
        publish()
    elif args.action=='qa':
        result=qa_outputs()
        print(json.dumps({k:v for k,v in result.items() if k!='figures'}))
    else:
        try:
            run()
        except Exception as error:
            write_json(OUT/'registries/last_failure.json',dict(time_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                        error=repr(error),recovery='Preserve immutable inputs/protocol; correct implementation, then rerun run. Partial products are not a PASS.'))
            raise


if __name__=='__main__':
    main()
