"""Two tiny checks for local scale math and nonoverwriting explicit overlays."""
import runpy
import unittest

import pandas as pd

from ebm_research.experiment_b.pilot import ROOT
from ebm_research.experiment_b.repair import merge_overlay


class RepairTests(unittest.TestCase):
    def test_constant_factor_calibration_and_matched_minute_math(self):
        ns = runpy.run_path(str(ROOT / "scripts/d2_1b_hf_compare.py"))
        j = pd.DataFrame({"key":pd.date_range("2019-08-12T18:00:00Z",periods=10,freq="min"), "Close":[50.+i for i in range(10)], "Volume":[10.]*10, "volume":[20.]*10})
        for a,b in [("Open","open"),("High","high"),("Low","low"),("Close","close")]:
            j[a]=j.Close
            j[b]=j.Close*2
        factor=ns["calibration_factor"](j)
        self.assertEqual(factor,2.)
        self.assertIsNone(ns["calibration_factor"](j.iloc[:9]))
        result=ns["discrepancies"](j,factor)
        self.assertEqual(result["close_max_bp"],0.)
        self.assertAlmostEqual(result["return_max_bp"],0.)
        self.assertEqual(result["matched_return_pairs"],9)
        self.assertEqual(result["median_volume_ratio"],.5)

    def test_explicit_union_rejects_original_collision_and_unknown_keys(self):
        t=pd.Timestamp("2019-08-12T19:29:00Z")
        row={"symbol":"SPY","timestamp_utc":t,"open":1.,"high":2.,"low":1.,"close":2.,"volume":10.,"validation_status":"ACCEPTED_LOCAL_ALIGNMENT"}
        patch=pd.DataFrame([row])
        original=pd.DataFrame([{**row,"timestamp_utc":t-pd.Timedelta(minutes=1)}])
        result=merge_overlay(original,patch,{("SPY",t)})
        self.assertEqual(len(result),2)
        with self.assertRaisesRegex(ValueError,"collides"):
            merge_overlay(patch,patch,{("SPY",t)})
        with self.assertRaisesRegex(ValueError,"not originally missing"):
            merge_overlay(original,patch,set())
        with self.assertRaisesRegex(ValueError,"Duplicate"):
            merge_overlay(original,pd.concat([patch,patch]),{("SPY",t)})


if __name__ == "__main__":
    unittest.main()
