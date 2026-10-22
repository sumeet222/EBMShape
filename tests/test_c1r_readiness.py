"""Focused C1R timing, cutpoint, path and date-only split checks."""
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd

from ebm_research.experiment_c.readiness import (
    fit_s0, transform_s0, prior_states, split_candidate, safe_path, calendar, WINDOWS)


class ReadinessTests(unittest.TestCase):
    def test_strict_two_predecessors_and_positive_guard(self):
        cal = calendar('2019-01-01', '2019-12-31')
        dates = ['2019-11-26', '2019-11-27', '2019-11-29', '2019-12-02', '2019-12-03']
        states = prior_states(dates, [1., 2., np.nan, 4., 8.], cal)
        self.assertTrue(np.isnan(states.Z0.iloc[3]))  # Friday early close, never skip.
        self.assertAlmostEqual(states.Z0.iloc[4], np.log(4.))
        self.assertTrue(np.isnan(states.Zchg.iloc[4]))
        self.assertEqual(states.predecessor_et.iloc[3], '2019-11-29')
        finite_half = prior_states(dates, [1., 2., 3., 4., 8.], cal)
        self.assertTrue(np.isnan(finite_half.Z0.iloc[3]))
        gap = prior_states(['2019-03-08', '2019-03-11', '2019-03-12'], [0., 2., 3.], cal)
        self.assertTrue(np.isnan(gap.Z0.iloc[1]))
        self.assertTrue(np.isnan(gap.Zchg.iloc[2]))
        self.assertEqual(gap.predecessor_et.iloc[1], '2019-03-08')
        self.assertEqual(cal.session_open('2019-03-08').hour, 14)
        self.assertEqual(cal.session_open('2019-03-11').hour, 13)
        holiday = prior_states(['2019-12-24', '2019-12-26'], [np.nan, 2.], cal)
        self.assertEqual(holiday.predecessor_et.iloc[1], '2019-12-24')
        self.assertTrue(np.isnan(holiday.Z0.iloc[1]))

    def test_train_only_cutpoints_and_fixed_validation(self):
        train = pd.DataFrame({'date_et': ['2019-01-02','2019-01-03','2019-01-04'], 'Z0':[0., 3., 6.]})
        fitted = fit_s0(train, '2019-01-04')
        self.assertEqual(fitted['cuts'], [2., 4.])
        np.testing.assert_array_equal(transform_s0([-100., 2., 4., 100., np.nan], fitted), [0,1,2,2,-1])
        self.assertEqual(fitted['cuts'], [2., 4.])  # extremes do not re-fit validation cuts.
        with self.assertRaisesRegex(ValueError, 'post-training'):
            fit_s0(pd.concat([train,pd.DataFrame({'date_et':['2020-01-02'],'Z0':[999.]})]), '2019-01-04')
        tied = fit_s0(train.assign(Z0=1.), '2019-01-04')
        np.testing.assert_array_equal(transform_s0([1.], tied), [2])

    def test_split_integer_chronology_withheld_and_temporary_smoke(self):
        dates = pd.bdate_range('2019-01-01', periods=11).strftime('%Y-%m-%d').tolist()
        m = dict(dates=list(reversed(dates)), cohort='SYNTHETIC', complete_metadata=False, evaluation_authorized=False)
        result = split_candidate(m)
        self.assertEqual(result['indices'], [6,8])
        self.assertEqual(result['sizes'], [6,2,3])
        self.assertLess(result['ranges'][0][1], result['ranges'][1][0])
        self.assertLess(result['ranges'][1][1], result['ranges'][2][0])
        self.assertEqual(result['evaluation_status'], 'NOT_AUTHORIZED')
        self.assertIsNone(result['official_cutoffs'])
        self.assertEqual(result['date_manifest_sha256'], split_candidate({**m, 'dates':dates})['date_manifest_sha256'])
        with self.assertRaisesRegex(ValueError, 'FREEZE_NOT_AUTHORIZED'):
            split_candidate(m, freeze=True)
        with self.assertRaisesRegex(ValueError, 'duplicates'):
            split_candidate({**m, 'dates':dates+[dates[0]]})
        with tempfile.TemporaryDirectory(prefix='c1r_smoke_') as directory:
            p = Path(directory)/'split.json'
            p.write_text(json.dumps(result))
            self.assertEqual(json.loads(p.read_text())['sizes'], [6,2,3])

    def test_source_path_firewall_and_windows(self):
        with tempfile.TemporaryDirectory(prefix='c1r_path_') as directory:
            root = Path(directory)
            (root/'ok').write_text('metadata')
            self.assertEqual(safe_path(root, 'ok'), root/'ok')
            for path in ['../escape', '/absolute']:
                with self.assertRaisesRegex(ValueError, 'UNSAFE'):
                    safe_path(root, path)
            (root/'link').symlink_to(root/'ok')
            with self.assertRaisesRegex(ValueError, 'SYMLINK'):
                safe_path(root, 'link')
        self.assertEqual(WINDOWS['CLOSE_C'], [66,78])
        self.assertEqual(WINDOWS['MID_C'], [24,48])
        self.assertEqual(WINDOWS['PRE_CLOSE_DIAG'], [66,72])


if __name__ == '__main__':
    unittest.main()
