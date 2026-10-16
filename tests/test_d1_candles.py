"""Two focused deterministic checks for D1's scientific timing/gap risks."""
import json
from pathlib import Path
import tempfile
import unittest

import pyarrow as pa
import pyarrow.parquet as pq

from ebm_research.experiment_b.pilot import (
    ROOT, aggregate, anchor_check, audit_session, calendar, grid, prior_full,
)

CONFIG = json.loads((ROOT / "config/D1_spy_source.json").read_text())


def bars_for(cal, day):
    return [{"t": t.isoformat(), "o": 100.0, "h": 101.0, "l": 99.0, "c": 100.0, "v": 10.0, "n": 2} for t in grid(cal, day)]


class CandleAuditTests(unittest.TestCase):
    def test_missing_clusters_and_critical_endpoints(self):
        cal = calendar("2024-03-07", "2024-03-11")
        complete = bars_for(cal, "2024-03-08")
        # Remove two consecutive opening minutes and the 15:29 anchor.
        missing_indices = {15, 16, 359}
        partial = [b for i, b in enumerate(complete) if i not in missing_indices]
        partial[1], partial[2] = partial[2], partial[1]
        partial.append(dict(partial[0]))  # identical duplicate is never an extra minute
        prior = bars_for(cal, "2024-03-07")[-1:]
        row, gaps, missing = audit_session("2024-03-08", partial, partial + prior, cal, CONFIG)
        self.assertEqual((row["missing_count"], row["gap_clusters"], row["longest_gap_length"]), (3, 2, 2))
        self.assertEqual(sum(x["length"] for x in gaps), len(missing))
        self.assertEqual(row["observed_unique_regular"] + row["missing_count"], 390)
        self.assertEqual(row["duplicates"], 1)
        self.assertGreater(row["raw_ordering_violations"], 0)
        self.assertFalse(row["eligible_rv"])
        self.assertFalse(row["eligible_r12"])
        self.assertFalse(row["eligible_r13"])
        self.assertFalse(row["eligible_primary"])
        summary = aggregate([row], gaps, missing, cal)
        self.assertEqual(summary["missing"], 3)

    def test_calendar_prior_close_formula_and_smoke(self):
        cal = calendar("2024-03-07", "2024-12-02")
        self.assertEqual(grid(cal, "2024-03-08")[0].strftime("%H:%M"), "14:30")
        self.assertEqual(grid(cal, "2024-03-11")[0].strftime("%H:%M"), "13:30")
        self.assertFalse(cal.is_session("2024-11-28"))
        self.assertEqual(len(grid(cal, "2024-11-29")), 210)
        self.assertEqual(prior_full(cal, "2024-12-02"), "2024-11-27")
        half = bars_for(cal, "2024-11-29")
        row, gaps, missing = audit_session("2024-11-29", half, half + bars_for(cal, "2024-11-27")[-1:], cal, CONFIG)
        self.assertEqual(row["missing_count"], 0)
        self.assertIsNone(row["longest_gap_start_et"])
        self.assertFalse(row["eligible_r13"])
        self.assertFalse(row["eligible_primary"])
        current, prev = bars_for(cal, "2024-03-08"), bars_for(cal, "2024-03-07")[-1:]
        prev[0]["c"] = 99.0
        calc = anchor_check("2024-03-08", current + prev, cal)
        self.assertAlmostEqual(calc["r1"], 100 / 99 - 1)
        self.assertEqual(calc["r12"], 0)
        self.assertEqual(calc["r13"], 0)
        self.assertEqual(calc["rv_open_raw"], 0)
        with tempfile.TemporaryDirectory(prefix="ebm_d1_smoke_") as tmp:
            dest = Path(tmp) / "smoke.parquet"
            pq.write_table(pa.Table.from_pylist([{"expected": 210}]), dest, compression="zstd")
            self.assertEqual(pq.read_table(dest).to_pylist(), [{"expected": 210}])


if __name__ == "__main__":
    unittest.main()
