"""Two focused D2 regressions; no live API or simulated multi-year market."""
import datetime as dt
import json
from pathlib import Path
import tempfile
import unittest

from ebm_research.experiment_b.acquisition import (
    IntegrityError, audit_day, fetch_pages, file_ref, verify_files, verify_request_ledger,
)
from ebm_research.experiment_b.pilot import ROOT, UTC, calendar

CONFIG = json.loads((ROOT / "config/D2_spy_source.json").read_text())


class D2Tests(unittest.TestCase):
    def test_successfully_empty_full_day_is_one_390_minute_gap(self):
        cal = calendar("2019-07-12", "2019-07-15")
        row, gaps, missing, invalid = audit_day("2019-07-15", [], [], cal, CONFIG, None)
        self.assertEqual(row["retrieval_status"], "COMPLETE")
        self.assertTrue(row["zero_returned_candles"])
        self.assertEqual((row["expected_minutes"], row["observed_unique_regular"], row["missing_count"]), (390, 0, 390))
        self.assertEqual(len(gaps), 1)
        self.assertEqual(gaps[0]["length"], len(missing))
        self.assertEqual(gaps[0]["start_et"][11:16], "09:30")
        self.assertEqual(gaps[0]["end_et"][11:16], "15:59")
        self.assertFalse(row["eligible_primary"])
        self.assertFalse(invalid)

    def test_resume_hash_conflict_and_page_overlap_abort(self):
        with tempfile.TemporaryDirectory(prefix="ebm_d2_smoke_") as temp:
            root = Path(temp)
            p = root / "tiny.txt"
            p.write_text("verified checkpoint")
            refs = [file_ref(p, root)]
            verify_files(root, refs)
            p.write_text("changed checkpoint")
            with self.assertRaises(IntegrityError):
                verify_files(root, refs)
            ledger = root / "requests.json"
            first = {"request_name": "committed", "status": 200}
            ledger.write_text(json.dumps([first], indent=2) + "\n")
            manifest = {"request_ledger": file_ref(ledger, root), "requests_total": 1}
            ledger.write_text(json.dumps([first, {"request_name": "incomplete_year"}], indent=2) + "\n")
            verify_request_ledger(root, manifest)  # legitimate appended work survives
            ledger.write_text(json.dumps([{"request_name": "changed"}], indent=2) + "\n")
            with self.assertRaises(IntegrityError):
                verify_request_ledger(root, manifest)
            ledger.write_bytes((json.dumps([first], indent=2) + "\n").replace("\n", "\r\n").encode())
            manifest = {"request_ledger": file_ref(ledger, root), "requests_total": 1}
            ledger.write_bytes((json.dumps([first, {"request_name": "appended"}], indent=2) + "\n").replace("\n", "\r\n").encode())
            verify_request_ledger(root, manifest)

        class TwoPages:
            config = {"max_pages_per_request": 2}
            calls = 0

            def get(self, name, endpoint, params, headers):
                self.calls += 1
                return {"bars": [{"t": "2019-07-15T13:30:00Z"}], "next_page_token": "next" if self.calls == 1 else None}

        a = dt.datetime(2019, 7, 15, 13, 30, tzinfo=UTC)
        with self.assertRaises(IntegrityError):
            fetch_pages(TwoPages(), "tiny_overlap", a, a + dt.timedelta(minutes=1), {})


if __name__ == "__main__":
    unittest.main()
