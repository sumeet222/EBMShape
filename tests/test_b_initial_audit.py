"""Focused deterministic timing, lagging and raw-bootstrap invariants only."""
import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd

from ebm_research.experiment_b.daily import at, opening_rv
from ebm_research.experiment_b.initial_audit import (
    TRAIN, assign_bins, circular_indices, grouped_bootstrap, interval,
    lagged_closes, prior_volume, read_training, PROTOCOL,
    contrast_statistics,
)
from ebm_research.experiment_b.pilot import write_json


class InitialAuditTests(unittest.TestCase):
    def test_small_parquet_config_and_output_smoke(self):
        p=json.loads(PROTOCOL.read_text())
        self.assertEqual(len(p['directions']),9)
        with tempfile.TemporaryDirectory(prefix='EBMShape_initial_audit_smoke_') as tmp:
            path=Path(tmp)/'feature_fixture.parquet'
            pd.DataFrame({'session_et':[pd.Timestamp('2016-01-05').date()],
                          'new_feature':[1.]}).to_parquet(path,index=False)
            fixture=read_training(path,['new_feature'],start=TRAIN[0])
            write_json(Path(tmp)/'smoke.json',{'n':len(fixture)})
            self.assertEqual(json.loads((Path(tmp)/'smoke.json').read_text()),{'n':1})

    def test_completed_bar_cutoffs_and_DST(self):
        self.assertEqual(at('2019-03-08','10:00').hour,15)
        self.assertEqual(at('2019-03-11','10:00').hour,14)
        for day in ['2019-03-08','2019-03-11']:
            self.assertEqual(at(day,'09:59')+pd.Timedelta(minutes=1),at(day,'10:00'))
            self.assertEqual(at(day,'15:29')+pd.Timedelta(minutes=1),at(day,'15:30'))
            self.assertGreater(at(day,'15:30')+pd.Timedelta(minutes=1),at(day,'15:30'))

    def test_exact_30_increment_RV(self):
        price=100.;bars=[]
        for _ in range(30):
            close=price*np.exp(.001)
            bars.append(dict(open=price,close=close,high=close,low=price))
            price=close
        self.assertAlmostEqual(opening_rv(bars),np.sqrt(30)*.001,places=12)
        self.assertTrue(np.isnan(opening_rv(bars[:-1])))

    def test_prior_only_volume_and_lag_missing_anchor(self):
        values=pd.Series([100.,101.,102.,104.,108.,112.])
        self.assertAlmostEqual(lagged_closes(values,1).iloc[2],100.)
        self.assertAlmostEqual(lagged_closes(values,2).iloc[3],200.)
        changed=values.copy();changed.iloc[3]=9999
        self.assertEqual(lagged_closes(values,2).iloc[3],lagged_closes(changed,2).iloc[3])
        missing=values.copy();missing.iloc[1]=np.nan
        self.assertTrue(np.isnan(lagged_closes(missing,2).iloc[3]))
        volumes=pd.Series([10.,20.,30.,1000.])
        self.assertEqual(prior_volume(volumes,3).iloc[3],20.)
        self.assertTrue(prior_volume(volumes,3).iloc[:3].isna().all())

    def test_training_guard_before_IO(self):
        with patch('pandas.read_parquet') as reader:
            with self.assertRaises(ValueError):
                read_training('unused',['y_last30_bp'],start='2022-01-01')
            reader.assert_not_called()
        self.assertEqual(TRAIN[1],'2021-12-31')

    def test_joint_cell_resampling_and_degenerate_abstention(self):
        indices=circular_indices(20,30,5,42)
        # Within each original joint cell response is constant; resampling cannot mix labels.
        cell=np.tile([0,1],10); y=2.+3*cell
        draws=grouped_bootstrap(cell,y,indices,2)
        np.testing.assert_allclose(draws,np.tile([2.,5.],(30,1)))
        np.testing.assert_array_equal((np.diff(indices[:,:5],axis=1)%20),np.ones((30,4)))
        p=dict(bootstrap=dict(min_valid=27,percentile=[2.5,97.5]))
        self.assertEqual(interval(draws[:,0],True,p)[3],'ABSTAIN_DEGENERATE')
        self.assertEqual(interval(draws[:,0],False,p)[3],'ABSTAIN_SUPPORT')

    def test_bin_boundary_equality_lower(self):
        np.testing.assert_array_equal(assign_bins(np.array([0.,1.,2.,3.]),[0.,1.,2.,3.]),[0,0,1,2])

    def test_raw_difference_of_increments_against_hand_calculation(self):
        # Six cells: low increment2, middle4, high7 => H-L5,M-L2,H-M3.
        frame=pd.DataFrame({'session_et':pd.bdate_range('2016-01-05',periods=12).date,
                            'w':np.tile([0.,0.,1.,1.],3),'z':np.repeat([0.,1.,2.],4),
                            'z_state':np.repeat([0,1,2],4)})
        y=np.repeat([1.,3.,2.,6.,5.,12.],2)
        spec=dict(x='w',state='z',facet='ALL',label='hand fixture',selected=0,
                  candidates=[dict(bands=[0.,0.,1.,1.])])
        p=dict(bootstrap=dict(length=5,min_valid=27,percentile=[2.5,97.5]),
               support=dict(min_n=1,min_groups=1),binning=dict(display_min_n=1,display_min_groups=1))
        rows=contrast_statistics(frame,spec,y,'A2',np.ones(12,bool),'FULL',circular_indices(12,30,5,42),p)
        np.testing.assert_allclose([r['estimate'] for r in rows],[5.,2.,3.])


if __name__=='__main__':
    unittest.main()
