"""Test the sample-review CLI with synthetic source metadata."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


def source(event_at, available_at):
    return {
        "source_ref": "private-source-reference",
        "version": "v2",
        "supersedes": "v1",
        "retrieved_at": "2025-01-01T09:00:00+00:00",
        "sha256": "a" * 64,
        "verified": True,
        "event_at": event_at,
        "available_at": available_at,
    }


def sample():
    month_six = source("2011-12-20T09:00:00-05:00", "2011-12-21T09:00:00-05:00")
    return [{
        "loan_id": "private-loan-reference",
        "modification_id": "private-modification-reference",
        "split": "train",
        "program_tier": 1,
        "permanent": True,
        "effective_month": "2011-07",
        "cutoff_at": "2012-01-01T00:00:00-05:00",
        "horizon_end_at": "2012-07-01T00:00:00-04:00",
        "month_six_report": {**month_six, "activity_month": "2011-12"},
        "month_six_report_history": [{
            **month_six, "version": "v1", "supersedes": None, "activity_month": "2011-12",
            "available_at": "2011-12-20T10:00:00-05:00",
        }],
        "active_status": {**month_six, "active": True},
        "outcome": {
            **source("2012-07-01T00:00:00-04:00", "2012-07-02T09:00:00-04:00"),
            "disposition": "no_event",
        },
        "features": [{
            **month_six,
            "feature": "last_installment_month_gap",
            "due_date": "2012-01-01",
            "posted_at": "2011-12-20T09:00:00-05:00",
        }],
    }]


class SampleReviewTest(unittest.TestCase):
    def run_review(self, cases):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "private-input.json"
            path.write_text(json.dumps(cases), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(Path(__file__).with_name("hamp_sample_review.py")), "--sample", str(path)],
                capture_output=True, text=True, check=False,
            )
        self.assertNotIn("private-", result.stdout + result.stderr)
        self.assertTrue(result.stdout, result.stderr)
        return result.returncode, json.loads(result.stdout)

    def test_verified_single_case_supports_sample_feasibility(self):
        code, report = self.run_review(sample())
        self.assertEqual(code, 0)
        self.assertEqual(report["status"], "sample_supported")
        self.assertEqual(report["metadata"]["modifications"], 1)

    def test_missing_unverified_and_late_evidence_explain_an_insufficient_sample(self):
        cases = sample()
        cases[0]["outcome"] = None
        cases[0]["active_status"]["verified"] = False
        cases[0]["month_six_report"]["available_at"] = "2012-01-01T05:00:00+00:00"
        cases[0]["features"][0].pop("supersedes")
        code, report = self.run_review(cases)
        self.assertEqual(code, 1)
        self.assertEqual(report["status"], "insufficient_evidence")
        self.assertEqual(report["evidence_gaps"], {
            "active_status_unverified": 1,
            "feature_source_incomplete": 1,
            "month_six_report_late": 1,
            "outcome_missing": 1,
        })

    def test_existing_gate_rejects_premature_event_free_label(self):
        cases = sample()
        cases[0]["outcome"]["event_at"] = "2012-06-30T23:59:59-04:00"
        code, report = self.run_review(cases)
        self.assertEqual(code, 1)
        self.assertEqual(report["metadata"]["violations"], {"no_event_before_full_follow_up": 1})

    def test_malformed_timestamps_report_invalid_input_without_source_values(self):
        cases = sample()
        cases[0]["cutoff_at"] = "2012-01-01T00:00:00"
        code, report = self.run_review(cases)
        self.assertEqual(code, 2)
        self.assertEqual(report, {"status": "invalid_input", "reason": "invalid_timestamp"})

    def test_sample_requires_permanent_tier_one_modifications(self):
        cases = sample()
        cases[0]["program_tier"] = 2
        code, report = self.run_review(cases)
        self.assertEqual(code, 1)
        self.assertEqual(report["evidence_gaps"], {"permanent_tier_one_not_established": 1})

    def test_reports_metadata_violations_alongside_incomplete_evidence(self):
        cases = sample()
        cases[0]["active_status"] = None
        cases[0]["outcome"]["event_at"] = "2012-06-30T23:59:59-04:00"
        code, report = self.run_review(cases)
        self.assertEqual(code, 1)
        self.assertEqual(report["evidence_gaps"], {"active_status_missing": 1})
        self.assertEqual(report["metadata"]["violations"], {"no_event_before_full_follow_up": 1})

    def test_stale_active_status_and_missing_report_predecessor_are_insufficient(self):
        cases = sample()
        cases[0]["active_status"]["event_at"] = "2011-11-20T09:00:00-05:00"
        cases[0]["month_six_report_history"] = []
        code, report = self.run_review(cases)
        self.assertEqual(code, 1)
        self.assertEqual(report["evidence_gaps"], {
            "active_status_not_for_month_six": 1,
            "month_six_report_predecessor_missing": 1,
        })
