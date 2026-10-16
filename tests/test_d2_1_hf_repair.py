"""One small deterministic check for the new gap-accounting function."""
import runpy
import unittest

from ebm_research.experiment_b.pilot import ROOT


class GapAccountingTests(unittest.TestCase):
    def test_dst_bar_start_clusters_and_duplicate_rejection(self):
        group = runpy.run_path(str(ROOT / "scripts/d2_1_hf_audit.py"))["clusters"]
        rows = [
            {"session_et": "2024-03-08", "timestamp_et": "2024-03-08T09:30:00-05:00", "timestamp_utc": "2024-03-08T14:30:00+00:00"},
            {"session_et": "2024-03-11", "timestamp_et": "2024-03-11T09:30:00-04:00", "timestamp_utc": "2024-03-11T13:30:00+00:00"},
            {"session_et": "2024-03-11", "timestamp_et": "2024-03-11T09:31:00-04:00", "timestamp_utc": "2024-03-11T13:31:00+00:00"},
        ]
        self.assertEqual([len(g) for g in group(rows[::-1])], [1, 2])
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            group(rows + rows[:1])
        with self.assertRaisesRegex(ValueError, "ET/UTC"):
            group([{**rows[1], "timestamp_et": "2024-03-11T09:30:00-05:00"}])


if __name__ == "__main__":
    unittest.main()
