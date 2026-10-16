"""Three small guards for training isolation, date keys and baseline comparison."""
import datetime as dt
import json
import unittest

import numpy as np
import pandas as pd

from ebm_research.experiment_b.linear_diagnostics import (compare_baseline, fit_ols,
                                                         ranked_influence)
from ebm_research.experiment_b.pilot import ROOT


class LinearDiagnosticTests(unittest.TestCase):
    def setUp(self):
        self.config=json.loads((ROOT/'config/B_stage1_dataset_selection.json').read_text())
        self.settings=json.loads((ROOT/'config/B_stage1_5_diagnostics.json').read_text())

    def test_guard_precedes_any_outcome_or_predictor_access(self):
        for day in ['2022-01-03','2024-01-02']:
            with self.assertRaisesRegex(ValueError,'training dates only'):
                fit_ols(pd.DataFrame({'session_et':[dt.date.fromisoformat(day)]}),['x_open_bp'],self.config)

    def test_cook_ranking_keeps_date_keys_with_nondefault_index(self):
        n=12;x=np.linspace(-2,2,n);y=.3*x+np.sin(np.arange(n))*.1;y[8]+=5
        f=pd.DataFrame(dict(session_et=[dt.date(2016,1,5)+dt.timedelta(days=i) for i in range(n)],
                            x_open_bp=x,w_preclose_bp=x*x,y_last30_bp=y,rv_open_raw=np.ones(n)*.01),index=np.arange(n)*7+100)
        result,_=fit_ols(f,['x_open_bp'],self.config)
        top=ranked_influence(f,result,self.config)
        self.assertEqual(top.iloc[0].session_et,f.iloc[8].session_et)
        self.assertEqual(top.index[0],f.index[8])
        self.assertNotIn(top.iloc[0].session_et,set(f.loc[~f.session_et.isin(top.session_et.iloc[:1])].session_et))

    def test_baseline_equality_tolerance_and_mismatch_abort(self):
        row=dict(cohort='principal',model='OLS1_E',term='x_open_bp',hac_lag=5,n=12,coefficient=.1,
                 ordinary_se=.02,r_squared=.01,hac_se=.03,ci_low=-.01,ci_high=.2,p_value=.5)
        self.assertEqual(compare_baseline([row],pd.DataFrame([row]),self.settings)['status'],'PASS')
        with self.assertRaisesRegex(ValueError,'INVALID—RERUN'):
            compare_baseline([{**row,'coefficient':.11}],pd.DataFrame([row]),self.settings)


if __name__=='__main__':
    unittest.main()
