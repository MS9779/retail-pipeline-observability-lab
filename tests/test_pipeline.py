import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from check_pipeline import build_health_report


class PipelineHealthTests(unittest.TestCase):
    def test_detects_expected_synthetic_issues(self):
        report = build_health_report()
        codes = {item["code"] for item in report["issues"]}
        self.assertEqual(report["status"], "attention_required")
        self.assertTrue({"DUPLICATE_EVENT_ID", "LOW_DAILY_VOLUME", "STALE_EVENT", "INVALID_EVENT_TYPE"}.issubset(codes))


if __name__ == "__main__":
    unittest.main()
