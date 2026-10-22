"""C1R local-only source reconciliation and draft splits; no models or downloads.

Only the verified P0 2016–2021 arrays may supply scientific values. Later
sources are inspected through schemas, footers and saved coverage metadata.
"""
import argparse
import datetime as dt
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import time

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from .preliminary import ROOT, calendar, rank_groups

P0 = Path('artifacts/C/preliminary_RV_profile_v1_1')
OUT = Path('artifacts/C/C1R')
WINDOWS = {'OPEN30': [0, 6], 'MID_C': [24, 48], 'CLOSE_C': [66, 78],
           'MID_P0': [30, 42], 'CLOSE_P0': [72, 78], 'PRE_CLOSE_DIAG': [66, 72]}
AUTHORITY = [
    'docs/specs/C/experiment_C_revised_complete_research_design_v1_1.md',
    'docs/specs/C/experiment_C_revised_transition_and_next_stage_handoff_v1_1.md',
    'docs/specs/experiment_C_state_dependent_intraday_volatility_profiles_research_spec_v1.md',
    'docs/specs/experiment_C_P0_supplied_handoff_v1_1.md', 'AGENTS.md']


def digest(path):
    """Stream a local file checksum without retaining another copy."""
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def safe_path(root, relative):
    """Resolve a declared relative input; reject traversal and symlink components."""
    relative = Path(relative)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError(f'UNSAFE_SOURCE_PATH: {relative}')
    path = root
    for part in relative.parts:
        path = path / part
        if path.is_symlink():
            raise ValueError(f'SYMLINK_SOURCE_REFUSED: {relative}')
    if not path.is_file():
        raise FileNotFoundError(f'MISSING_SOURCE_DOCUMENT_OR_DATA: {relative}')
    return path


def prior_states(dates, rv, cal):
    """Z0/Zchg from strict scheduled predecessors, positive finite RV only."""
    lookup = dict(zip(dates, np.asarray(rv, float)))
    rows = []
    for day in dates:
        p = str(cal.previous_session(str(day)).date())
        pp = str(cal.previous_session(p).date())
        def valid(key):
            return (len(cal.session_minutes(key)) == 390
                    and np.isfinite(lookup.get(key, np.nan)) and lookup[key] > 0)
        z0 = math.log(lookup[p]) if valid(p) else np.nan
        zchg = z0 - math.log(lookup[pp]) if valid(p) and valid(pp) else np.nan
        rows.append(dict(date_et=str(day), predecessor_et=p, second_predecessor_et=pp,
                         Z0=z0, Zchg=zchg,
                         Z0_reason='AVAILABLE_VERIFIED' if valid(p) else 'NO_VALID_IMMEDIATE_PREDECESSOR',
                         Zchg_reason='AVAILABLE_VERIFIED' if valid(p) and valid(pp) else 'NO_VALID_TWO_SESSION_CHAIN'))
    return pd.DataFrame(rows)


def fit_s0(training, train_end):
    """Fit two linear empirical quantiles using dated training Z0 only.

    Boundary ties map to the upper category at transform time; ties are never
    split by validation ranks. This is a candidate reusable transform, not
    approval of a full-C cohort or fitted full-C thresholds.
    """
    if training.date_et.duplicated().any() or (training.date_et > train_end).any():
        raise ValueError('TRAIN_ONLY_S0: duplicate dates or post-training rows')
    values = training.Z0.to_numpy(float)
    if not len(values) or not np.isfinite(values).all():
        raise ValueError('TRAIN_ONLY_S0: require nonempty finite training Z0')
    cuts = np.quantile(values, [1/3, 2/3], method='linear')
    return dict(cuts=cuts.tolist(), train_end=train_end, n_train=len(values),
                method='linear', boundary_ties='upper', status='TRAIN_ONLY_TRANSFORM')


def transform_s0(values, fitted):
    """Apply saved cutpoints unchanged; missing numeric states map to -1."""
    values = np.asarray(values, float)
    return np.where(np.isfinite(values), np.searchsorted(fitted['cuts'], values, side='right'), -1)


def split_candidate(manifest, freeze=False):
    """Dry-run chronological integer splits of an approved date-only manifest.

    Required metadata: dates, cohort, complete_metadata, evaluation_authorized.
    No reading values, no official freeze in C1R, including on complete metadata.
    """
    if freeze:
        raise ValueError('C1R_FREEZE_NOT_AUTHORIZED: coverage and scientific approval required')
    dates = manifest['dates']
    if any(dt.date.fromisoformat(d).isoformat() != d for d in dates):
        raise ValueError('SPLIT_DATES: require ISO ET calendar dates')
    if len(set(dates)) != len(dates):
        raise ValueError('SPLIT_DATES: duplicates prohibited')
    dates = sorted(dates)
    if len(dates) < 5:
        raise ValueError('SPLIT_DATES: at least five dates required for a dry run')
    n = len(dates)
    a, b = 3*n//5, 4*n//5
    blocks = [dates[:a], dates[a:b], dates[b:]]
    return dict(status='ILLUSTRATIVE_NOT_FULL_C', cohort=manifest['cohort'], n=n,
                date_manifest_sha256=hashlib.sha256(('\n'.join(dates)+'\n').encode()).hexdigest(),
                indices=[a, b], sizes=[len(x) for x in blocks],
                ranges=[[x[0], x[-1]] for x in blocks],
                complete_metadata=manifest['complete_metadata'], official_cutoffs=None,
                evaluation_status='NOT_AUTHORIZED', locked=False,
                prior_exposure='ALL_P0_DATES_EXPLORED',
                withheld_status='ILLUSTRATIVE_EVALUATION_WITHHELD_NOT_A_BLIND_TEST')


def audit(root=ROOT, data=None):
    """Validate registered P0 identities; emit only compact C1R preparation."""
    started = time.perf_counter()
    root = Path(root).resolve()
    data = Path(data or os.environ.get('EBM_DATA_ROOT') or root/'data').expanduser()
    if data.is_symlink():
        raise ValueError('SYMLINK_DATA_ROOT_REFUSED')
    data = data.resolve()
    reads, identities, protected = [], [], {}
    def read_json(relative):
        path = safe_path(root, relative)
        reads.append(dict(path=str(relative), operation='json_metadata', columns='metadata'))
        protected[path] = digest(path)
        return json.loads(path.read_text())
    def verify(base, ref):
        path = safe_path(base, ref['path'])
        actual = digest(path)
        if actual != ref['sha256'] or path.stat().st_size != ref['bytes']:
            raise ValueError(f'SOURCE_IDENTITY_MISMATCH: {ref["path"]}')
        protected[path] = actual
        identities.append(dict(root='repo' if base == root else 'EBM_DATA_ROOT', **ref, status='PASS'))
        return path
    authorities = []
    for relative in AUTHORITY:
        path = safe_path(root, relative)
        content = path.read_text()
        protected[path] = digest(path)
        authorities.append(dict(path=relative, sha256=digest(path), bytes=path.stat().st_size,
                                headings=sum(s.startswith('#') for s in content.splitlines())))
    config = read_json('config/C_preliminary_RV_profile_v1.json')
    registry = read_json('data/registry/C_preliminary_RV_profile_v1_1.json')
    source = read_json(P0/'source_manifest.json')
    qa = read_json(P0/'qa_results.json')
    outputs = read_json(P0/'outputs_manifest.json')
    d2 = read_json('data/registry/D2_spy_source_manifest.json')
    d1 = read_json('data/registry/D1_spy_source_manifest.json')
    assert registry['source_range'] == ['2016-01-04', '2021-12-31']
    assert registry['analysis_range'] == ['2016-01-05', '2021-12-31']
    assert [Path(r['path']).name for r in config['base_refs']] == [f'year={y}.parquet' for y in range(2016, 2022)]
    assert set(source['months']) == {f'{y}-{m:02}' for y in range(2016, 2022) for m in range(1, 13)}
    assert digest(root/'config/C_preliminary_RV_profile_v1.json') == source['protocol_sha256'] == registry['protocol_sha256']
    assert digest(root/P0/'source_manifest.json') == registry['source_manifest_sha256'] == qa['source_manifest_sha256']
    assert digest(root/config['spec_path']) == config['spec_sha256']
    assert digest(root/AUTHORITY[3]) == config['handoff_sha256']
    # Verify the registered P0 product, not a reconstructed full day-by-bin copy.
    product = next(r for r in outputs['files'] if r['path'] == registry['daily_product'])
    path = verify(root, product)
    with np.load(path, allow_pickle=False) as saved:
        z = {k: saved[k] for k in saved.files}
    reads.append(dict(path=product['path'], operation='development_npz', columns=list(z),
                      date_mask='2016-01-04..2021-12-31'))
    dates = z['dates']
    assert min(dates) == '2016-01-04' and max(dates) == '2021-12-31'
    assert len(dates) == len(set(dates)) and np.all(dates[1:] > dates[:-1])
    cal = calendar('2016-01-04', '2026-09-30')
    q_ok = np.isfinite(z['q']).all(axis=1) & (dates >= config['start'])
    assert z['q'].shape == z['rv'].shape == (len(dates), 78)
    assert np.all(z['q'][q_ok] >= 0) and np.all(z['RV_day'][q_ok] > 0)
    np.testing.assert_allclose(z['q'][q_ok].sum(axis=1), 1, atol=1e-10, rtol=0)
    np.testing.assert_allclose(z['rv'][q_ok].sum(axis=1), z['RV_day'][q_ok], atol=1e-18, rtol=1e-12)
    np.testing.assert_allclose(z['q'][q_ok], z['rv'][q_ok]/z['RV_day'][q_ok, None], atol=1e-10, rtol=0)
    states = prior_states(dates, z['RV_day'], cal)
    np.testing.assert_allclose(np.exp(states.Z0), z['RV_prev'], atol=1e-18, rtol=1e-12, equal_nan=True)
    z0_ok = q_ok & np.isfinite(states.Z0)
    assert int(q_ok.sum()) == qa['OPEN']['n'] == 1491
    assert int(z0_ok.sum()) == qa['PREV']['n'] == 1472
    # Independent retrospective rank check; do not fit S0 on observed outcomes.
    for key, values in [('open_labels', z['RV_open']), ('prev_labels', z['RV_prev'])]:
        labels, _ = rank_groups(np.where(q_ok, values, np.nan), dates)
        np.testing.assert_array_equal(labels, z[key])
    exclusions_path = safe_path(root, P0/'missingness_exclusions.csv')
    protected[exclusions_path] = digest(exclusions_path)
    exclusions = pd.read_csv(exclusions_path)
    reads.append(dict(path=str(P0/'missingness_exclusions.csv'), operation='saved_eligibility_metadata', columns=list(exclusions)))
    incomplete = exclusions[exclusions.reason == 'INCOMPLETE_OR_WRONG_RTH_GRID']
    expected_gaps = ['2016-02-02', '2019-08-12', '2020-03-09', '2020-03-12', '2020-03-16', '2020-03-18', '2021-05-05']
    assert incomplete.date.tolist() == expected_gaps and incomplete.missing_minutes.sum() == 100
    assert (exclusions.reason == 'EARLY_CLOSE').sum() == 12
    # Predetermined chronological selection, including the Monday after DST.
    spot_dates = [str(next(d for d in dates[q_ok] if d.startswith(str(y)))) for y in [2016, 2018, 2019, 2020, 2021]] + ['2019-03-11']
    spots, key_counts = [], []
    key_columns = ['symbol', 'timestamp_utc', 'session_et']
    price_columns = key_columns + ['open', 'high', 'low', 'close']
    def parquet(path, columns, day=None):
        # Scientific columns may only be read from identity-verified P0 sources.
        if path not in protected:
            raise ValueError('UNVERIFIED_PARQUET_REFUSED')
        filters = [('session_et', '=', dt.date.fromisoformat(day))] if day else None
        frame = pd.read_parquet(path, columns=columns, filters=filters)
        if len(frame) and not frame.session_et.astype(str).between('2016-01-04', '2021-12-31').all():
            raise ValueError('C1R_RESERVED_VALUE_FIREWALL')
        reads.append(dict(path=path.relative_to(data).as_posix(), operation='development_parquet', columns=columns,
                          date_mask=day or '2016..2021 keys only', rows=len(frame)))
        return frame
    source_paths = {}
    for ref in config['base_refs']:
        source_paths[ref['path']] = verify(data, ref)
    for entry in source['months'].values():
        ref = entry['supplement']
        source_paths[ref['path']] = verify(data, ref)
    assert sum(e['supplement']['bytes'] for e in source['months'].values()) == 10318012
    for year in range(2016, 2022):
        ref = config['base_refs'][year-2016]
        base = source_paths[ref['path']]
        supplements = {tag: source_paths[entry['supplement']['path']] for tag, entry in source['months'].items() if tag.startswith(str(year))}
        keys = pd.concat([parquet(p, key_columns) for p in [base, *supplements.values()]], ignore_index=True)
        assert set(keys.symbol) == {'SPY'}
        assert not keys.duplicated(['symbol', 'timestamp_utc']).any(), 'D2_SUPPLEMENT_KEY_OVERLAP'
        assert (keys.timestamp_utc.dt.tz_convert('America/New_York').dt.strftime('%Y-%m-%d') == keys.session_et.astype(str)).all()
        key_counts.append(dict(year=year, unique_keys=len(keys), overlaps=0))
        grouped = keys.groupby(keys.session_et.astype(str)).timestamp_utc
        for day in dates[q_ok & np.char.startswith(dates, str(year))]:
            assert pd.DatetimeIndex(grouped.get_group(day).sort_values()).equals(cal.session_minutes(str(day)))
        for day in [d for d in spot_dates if d.startswith(str(year))]:
            frame = pd.concat([parquet(p, price_columns, day) for p in [base, supplements[day[:7]]]], ignore_index=True).sort_values('timestamp_utc')
            assert pd.DatetimeIndex(frame.timestamp_utc).equals(cal.session_minutes(day))
            # Scalar math is independent of P0's vector reshape/summation kernel.
            closes = frame.close.to_list()
            increments = [math.log(closes[0]/frame.open.iloc[0])] + [math.log(closes[i]/closes[i-1]) for i in range(1, 390)]
            rv = np.array([math.fsum(x*x for x in increments[5*k:5*k+5]) for k in range(78)])
            total = math.fsum(rv)
            q = rv/total
            ix = int(np.flatnonzero(dates == day)[0])
            np.testing.assert_allclose(rv, z['rv'][ix], atol=1e-18, rtol=1e-12)
            np.testing.assert_allclose(total, z['RV_day'][ix], atol=1e-18, rtol=1e-12)
            np.testing.assert_allclose(q, z['q'][ix], atol=1e-10, rtol=0)
            window_errors = {name: abs(math.fsum(q[a:b])-math.fsum(z['q'][ix, a:b])) for name, (a, b) in WINDOWS.items()}
            assert max(window_errors.values()) < 1e-10
            spots.append(dict(date_et=day, rows=390, max_rv_error=float(np.max(abs(rv-z['rv'][ix]))),
                              R_error=abs(total-z['RV_day'][ix]), max_Q_error=float(np.max(abs(q-z['q'][ix]))),
                              window_errors=window_errors, price_tolerance='identical persisted source bytes; no cross-feed price substitution'))
    # Future partitions: FOOTERS ONLY, no column statistics or OHLCV arrays.
    footers = []
    for year in range(2022, 2027):
        ref = d2['blocks'][str(year)]['canonical']
        p = safe_path(data, ref['path'])
        f = pq.ParquetFile(p)
        footers.append(dict(path=ref['path'], bytes=p.stat().st_size, rows=f.metadata.num_rows,
                            columns=f.schema_arrow.names, declared_sha256=ref['sha256'], checksum_status='DECLARED_NOT_REHASHED'))
        reads.append(dict(path=ref['path'], operation='footer_only', columns='schema_names_and_row_counts_only'))
    ref = d1['canonical']
    p = safe_path(data, ref['path_relative_to_data_root'])
    f = pq.ParquetFile(p)
    footers.append(dict(path=ref['path_relative_to_data_root'], bytes=p.stat().st_size, rows=f.metadata.num_rows,
                        columns=f.schema_arrow.names, declared_sha256=ref['sha256'], checksum_status='DECLARED_NOT_REHASHED'))
    reads.append(dict(path=ref['path_relative_to_data_root'], operation='footer_only', columns='schema_names_and_row_counts_only'))
    # CSV usecols physically parses only these saved QA metadata fields.
    qa_columns = ['session_et', 'session_type', 'missing_count', 'retrieval_complete']
    qa_path = safe_path(root, 'data/registry/D2_spy_candle_qa_sessions.csv')
    meta = pd.read_csv(qa_path, usecols=qa_columns)
    protected[qa_path] = digest(qa_path)
    reads.append(dict(path='data/registry/D2_spy_candle_qa_sessions.csv', operation='coverage_metadata_only', columns=qa_columns))
    full_d1 = [d for d in d1['identity']['sessions'] if len(cal.session_minutes(d)) == 390]
    coverage, future_sessions = [], []
    for year in range(2016, 2027):
        end = '2026-09-30' if year == 2026 else f'{year}-12-31'
        sessions = cal.sessions_in_range(f'{year}-01-01', end)
        ordinary = [str(s.date()) for s in sessions if len(cal.session_minutes(s)) == 390]
        pilot = [d for d in full_d1 if d.startswith(str(year))]
        future = year >= 2022
        mask = np.char.startswith(dates, str(year))
        known_full = len(pilot) if future else int((q_ok & mask).sum()) + (year == 2016)
        gap = len(ordinary)-known_full
        old = meta[meta.session_et.str.startswith(str(year))]
        if future:
            missing_d2 = set(old.loc[(old.session_type == 'full') & (old.missing_count > 0), 'session_et'])
            for day in ordinary:
                previous = str(cal.previous_session(day).date())
                future_sessions.append(dict(date_et=day, predecessor_et=previous,
                    predecessor_is_ordinary=len(cal.session_minutes(previous)) == 390,
                    physical_coverage='D1_MANIFEST_390' if day in pilot else 'D2_91_ONLY',
                    D2_historical_gap=day in missing_d2, needs_full_session_supplement=day not in pilot,
                    target_validity='UNVERIFIED', Z0_validity='UNVERIFIED', values_withheld=True))
        coverage.append(dict(year=year, through=end, calendar_full_days=len(ordinary), early_close_days=len(sessions)-len(ordinary),
                             verified_or_manifest_full_days=known_full, primary_Q_days=int((q_ok & mask).sum()) if not future else None,
                             Z0_days=int((z0_ok & mask).sum()) if not future else None,
                             coverage_status='390MIN_VERIFIED_P0' if not future else '91MIN_D2_PLUS_SPARSE_D1' if pilot else '91MIN_ONLY',
                             full_day_dates=';'.join(pilot), missing_full_day_coverage=gap,
                             existing_D2_gap_dates=';'.join(old.loc[(old.session_type == 'full') & (old.missing_count > 0), 'session_et']),
                             target_validity='VERIFIED_P0' if not future else 'UNVERIFIED_FUTURE_ELIGIBILITY_METADATA_UNKNOWN',
                             reference=f'canonical/spy_minute/B_alpaca_sip_SPY_1m_split_D2_v1/year={year}.parquet',
                             supplement_reference=registry['supplement_directory'] if not future else 'ABSENT',
                             D1_reference=ref['path_relative_to_data_root'] if pilot else '',
                             estimated_new_transfer_bytes=math.ceil(gap*119675359/1499) if future else 0,
                             estimated_new_retained_bytes=math.ceil(gap*10318012/1499) if future else 0,
                             estimate_basis='P0 bytes/full scheduled day; not entitlement or complete-source guarantee',
                             exposure='P0_EXPLORED' if not future else 'B_RETURN_DEVELOPMENT_EXPOSED' if year < 2024 else 'B_RESERVED_NO_C_VALUES'))
    states = states.loc[q_ok].copy()
    states['source_dataset_id'] = registry['dataset_id']
    states['available_before'] = 'date_et 09:30 America/New_York'
    states['S0_status'] = 'TRAIN_ONLY_CUTPOINTS_PENDING_OFFICIAL_SPLIT'
    states['Zret_status'] = 'BLOCKED_DEFINITION_PREVIOUS_TWO_CLOSE_ANCHORS'
    states['Zvol_status'] = 'BLOCKED_DEFINITION_LOOKBACK_EPS_VOLUME_AUDIT'
    candidates = [split_candidate(dict(dates=dates[q_ok].tolist(), cohort='Q_ELIGIBLE_THEN_MASK_Z0', complete_metadata=False, evaluation_authorized=False)),
                  split_candidate(dict(dates=dates[z0_ok].tolist(), cohort='Z0_ELIGIBLE', complete_metadata=False, evaluation_authorized=False))]
    for candidate, pool in zip(candidates, [dates[q_ok], dates[z0_ok]]):
        a, b = candidate['indices']
        present = set(dates[z0_ok])
        candidate['Z0_matched_sizes'] = [sum(d in present for d in part) for part in [pool[:a], pool[a:b], pool[b:]]]
    result = dict(task_id='C1R_SOURCE_STATE_PROTOCOL_v1_1', stage_verdict='READY_FOR_C2R_DEV', implementation='PASS_WITH_QUALIFICATIONS',
                  authority=authorities, dataset_id=registry['dataset_id'], source_id=d2['identity']['dataset_id'],
                  daily_product=product, sources=identities, q_days=int(q_ok.sum()), z0_days=int(z0_ok.sum()),
                  zchg_days=int(states.Zchg.notna().sum()), first=str(dates[q_ok][0]), last=str(dates[q_ok][-1]),
                  Q_closure_max_error=float(np.max(abs(z['q'][q_ok].sum(axis=1)-1))),
                  incomplete_dates=incomplete[['date', 'missing_minutes']].to_dict('records'),
                  early_close_dates=exclusions.loc[exclusions.reason == 'EARLY_CLOSE', 'date'].tolist(),
                  source_key_counts=key_counts, spot_checks=spots, future_footers=footers,
                  network_bytes=0, raw_copies=0, duplicate_Q_copies=0,
                  science_value_dates_read=['2016-01-04', '2021-12-31'], read_ledger=reads,
                  historical_rank_labels='VERIFIED_RETROSPECTIVE_D_ONLY_NOT_F_S0',
                  source_status='SOURCE_INSPIRED_PROXY', protected_recheck='PENDING',
                  versions={s: importlib.metadata.version(s) for s in ['numpy', 'pandas', 'pyarrow', 'exchange-calendars']},
                  python=platform.python_version(), wall_seconds=time.perf_counter()-started)
    changed = [str(p) for p, h in protected.items() if digest(p) != h]
    if changed:
        raise ValueError(f'PROTECTED_INPUT_CHANGED: {changed}')
    result['protected_recheck'] = dict(status='PASS', files=len(protected))
    output = root/OUT
    output.mkdir(parents=True, exist_ok=True)
    (output/'source_identity_qa.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    pd.DataFrame(coverage).to_csv(output/'coverage_by_period.csv', index=False)
    pd.DataFrame(future_sessions).to_csv(output/'future_session_coverage.csv', index=False)
    state_path = data/'derived/C/c_development_states_v1_1.parquet'
    state_path.parent.mkdir(parents=True, exist_ok=True)
    states.to_parquet(state_path, index=False, compression='zstd')
    availability = states.drop(columns=['Z0', 'Zchg']).copy()
    availability['Z0_available'] = states.Z0.notna()
    availability['Zchg_available'] = states.Zchg.notna()
    availability.to_csv(output/'development_state_availability.csv', index=False)
    split = dict(status='DRAFT_PENDING_COVERAGE_AND_RELEASE', split_population_policy='PENDING_APPROVAL',
                 recommended_population='Z0_ELIGIBLE for primary F matched comparisons',
                 full_C_horizon='NOT_EXACTLY_FIXED_BY_C_SPEC; local-source feasibility 2016-01-05..2026-09-30',
                 rule='sorted unique ET dates; floor(0.6*N), floor(0.8*N), final remainder',
                 official_cutoffs=None, evaluation_status='NOT_AUTHORIZED', locked=False,
                 examples=candidates, future_target_and_predecessor_validity='UNVERIFIED',
                 exposure=[{'dates':'2016..2021', 'status':'ALL_P0_Q_AND_WINDOWS_EXPLORED'},
                           {'dates':'2022..2023', 'status':'B_RETURN_RELATED_WORK_PREVIOUSLY_EXPOSED'},
                           {'dates':'2024..2026-09-30', 'status':'B_RESERVED_C_VALUES_NOT_ACCESSED'}])
    (output/'split_candidate_manifest.json').write_text(json.dumps(split, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['stage_verdict', 'q_days', 'z0_days', 'zchg_days', 'wall_seconds', 'network_bytes']}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['audit', 'split'])
    parser.add_argument('--data-root', type=Path)
    parser.add_argument('--eligible-manifest', type=Path)
    parser.add_argument('--freeze', action='store_true')
    args = parser.parse_args()
    if args.action == 'audit':
        if args.freeze or args.eligible_manifest:
            parser.error('audit does not accept split/freeze flags')
        audit(data=args.data_root)
    else:
        if args.eligible_manifest is None:
            parser.error('split requires --eligible-manifest (date-only JSON)')
        manifest = json.loads(args.eligible_manifest.read_text())
        print(json.dumps(split_candidate(manifest, freeze=args.freeze), indent=2))


if __name__ == '__main__':
    main()
