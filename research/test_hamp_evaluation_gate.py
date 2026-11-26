"""Exercise research gate boundaries with synthetic records only."""

import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from hamp_evaluation_gate import COHORT_FIELDS, FEATURE_FIELDS, evaluate


def example(index, year, split, disposition):
    return {
        "loan_id": f"synthetic-loan-{index}",
        "modification_id": f"synthetic-mod-{index}",
        "split": split,
        "cutoff_at": f"{year}-01-01T00:00:00-05:00",
        "horizon_end_at": f"{year}-07-01T00:00:00-04:00",
        "disposition": disposition,
        "evidence_at": f"{year}-07-01T00:00:00-04:00" if disposition == "no_event"
        else f"{year}-04-01T09:00:00-04:00",
        "label_available_at": f"{year}-07-02T12:00:00-04:00",
    }


class EvaluationGateTest(unittest.TestCase):
    def setUp(self):
        self.cohort = [
            example(1, 2012, "train", "no_event"),
            example(2, 2014, "validation", "paid_off"),
            example(3, 2016, "test", "disqualified"),
            example(4, 2016, "test", "censored"),
        ]
        self.features = [
            {
                "modification_id": row["modification_id"],
                "feature": "last_installment_month_gap",
                "event_at": f"{int(row['cutoff_at'][:4]) - 1}-12-20T09:00:00-05:00",
                "available_at": f"{int(row['cutoff_at'][:4]) - 1}-12-21T10:00:00-05:00",
            }
            for row in self.cohort
        ]

    def run_gate(self):
        return evaluate(self.cohort, self.features)

    def test_clean_cohort_keeps_competing_events_and_censoring_separate(self):
        result = self.run_gate()
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["outcome_metadata_by_disposition"], {
            "censored": 1, "disqualified": 1, "no_event": 1, "paid_off": 1,
        })

    def test_at_cutoff_is_late_even_with_a_different_utc_offset(self):
        self.features[0]["available_at"] = "2012-01-01T05:00:00+00:00"
        self.assertEqual(self.run_gate()["violations"], {"feature_available_at_or_after_cutoff": 1})

    def test_rejects_feature_event_after_cutoff_and_unsupported_feature(self):
        self.features[0]["event_at"] = "2012-01-02T09:00:00-05:00"
        self.features[0]["feature"] = "latest_final_state"
        self.assertEqual(self.run_gate()["violations"], {
            "feature_available_before_event": 1,
            "feature_event_at_or_after_cutoff": 1,
            "unapproved_feature": 1,
        })

    def test_rejects_same_loan_across_splits_and_late_training_label(self):
        self.cohort[1]["loan_id"] = self.cohort[0]["loan_id"]
        self.cohort[0]["label_available_at"] = self.cohort[1]["cutoff_at"]
        self.assertEqual(self.run_gate()["violations"], {
            "loan_in_multiple_splits": 1, "train_labels_overlap_validation_cutoff": 1,
        })

    def test_rejects_early_non_event_and_label_timestamp_before_evidence(self):
        self.cohort[0]["evidence_at"] = "2012-06-30T23:59:59-04:00"
        self.cohort[0]["label_available_at"] = "2012-06-30T22:00:00-04:00"
        self.assertEqual(self.run_gate()["violations"], {
            "label_available_before_evidence": 1, "no_event_before_full_follow_up": 1,
        })

    def test_outcome_at_end_of_month_twelve_is_outside_exclusive_window(self):
        self.cohort[2]["evidence_at"] = self.cohort[2]["horizon_end_at"]
        self.assertEqual(self.run_gate()["violations"], {"event_or_censoring_outside_horizon": 1})

    def test_rejects_bad_horizon_unknown_join_and_missing_features(self):
        self.cohort[0]["horizon_end_at"] = "2012-06-01T00:00:00-04:00"
        self.features[0]["modification_id"] = "missing-modification"
        self.assertEqual(self.run_gate()["violations"], {
            "invalid_horizon_boundaries": 1,
            "modifications_without_feature_rows": 1,
            "unknown_feature_modification": 1,
        })

    def cli(self):
        with tempfile.TemporaryDirectory() as scratch:
            command = [sys.executable, str(Path(__file__).with_name("hamp_evaluation_gate.py"))]
            for option, fields, values in (
                ("cohort", COHORT_FIELDS, self.cohort),
                ("features", FEATURE_FIELDS, self.features),
            ):
                path = Path(scratch) / f"{option}.csv"
                with path.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=fields)
                    writer.writeheader()
                    writer.writerows(values)
                command.extend((f"--{option}", str(path)))
            return subprocess.run(command, capture_output=True, text=True, check=False)

    def test_cli_reports_pass_and_policy_failure_as_different_exit_codes(self):
        result = self.cli()
        self.assertEqual(result.returncode, 0)
        self.features[0]["available_at"] = self.cohort[0]["cutoff_at"]
        result = self.cli()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["violations"], {
            "feature_available_at_or_after_cutoff": 1,
        })
        self.assertNotIn("synthetic-", result.stdout)

    def test_cli_rejects_timestamp_without_offset_without_echoing_input(self):
        self.features[0]["available_at"] = "2011-12-21T09:00:00"
        result = self.cli()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout), {"status": "fail", "violations": {"invalid_input": 1}})
        self.assertNotIn("synthetic-", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
