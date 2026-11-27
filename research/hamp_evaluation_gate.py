"""Validate timestamp and split metadata for a research-only HAMP cohort."""

import argparse
from collections import Counter
import csv
from datetime import datetime, time
import json
from pathlib import Path


SPLITS = ("train", "validation", "test")
DISPOSITIONS = frozenset({"disqualified", "paid_off", "censored", "no_event"})
FEATURES = frozenset({"last_installment_month_gap", "reporting_pattern", "payment_history_change"})
COHORT_FIELDS = (
    "loan_id", "modification_id", "split", "cutoff_at", "horizon_end_at",
    "disposition", "evidence_at", "label_available_at",
)
FEATURE_FIELDS = ("modification_id", "feature", "event_at", "available_at")


def records(path, fields):
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source, strict=True)
        if (
            reader.fieldnames is None
            or len(reader.fieldnames) != len(fields)
            or set(reader.fieldnames) != set(fields)
        ):
            raise ValueError("CSV header does not match the documented schema.")
        for record in reader:
            if None in record or any(value is None or not value.strip() for value in record.values()):
                raise ValueError("CSV rows must have one nonempty value per column.")
            yield {key: value.strip() for key, value in record.items()}


def timestamp(value):
    parsed = datetime.fromisoformat(value)
    if "T" not in value or parsed.utcoffset() is None:
        raise ValueError("Timestamps require an explicit UTC offset.")
    return parsed


def month_boundary(value):
    return value.day == 1 and value.time() == time(0)


def cohort_metadata(cohort, issues, require_all_splits):
    examples = {}
    loans = {}
    split_counts = Counter()
    outcome_counts = Counter()
    first_cutoff = {}
    last_label = {}
    for record in cohort:
        loan = record["loan_id"]
        modification = record["modification_id"]
        split = record["split"]
        if modification in examples:
            issues["duplicate_modification"] += 1
            continue
        if split not in SPLITS:
            issues["unknown_split"] += 1
            continue
        cutoff, horizon, evidence, available = (
            timestamp(record[field])
            for field in ("cutoff_at", "horizon_end_at", "evidence_at", "label_available_at")
        )
        if loans.setdefault(loan, split) != split:
            issues["loan_in_multiple_splits"] += 1
        if (
            not month_boundary(cutoff) or not month_boundary(horizon)
            or (horizon.year - cutoff.year) * 12 + horizon.month - cutoff.month != 6
        ):
            issues["invalid_horizon_boundaries"] += 1
        disposition = record["disposition"]
        if disposition not in DISPOSITIONS:
            issues["unknown_disposition"] += 1
        elif disposition == "no_event" and evidence < horizon:
            issues["no_event_before_full_follow_up"] += 1
        elif disposition != "no_event" and not cutoff <= evidence < horizon:
            issues["event_or_censoring_outside_horizon"] += 1
        else:
            outcome_counts[disposition] += 1
        if available < evidence:
            issues["label_available_before_evidence"] += 1
        examples[modification] = cutoff
        split_counts[split] += 1
        first_cutoff[split] = min(first_cutoff.get(split, cutoff), cutoff)
        last_label[split] = max(last_label.get(split, available), available)

    if require_all_splits:
        for split in SPLITS:
            if not split_counts[split]:
                issues[f"empty_{split}_split"] += 1
    splits_to_compare = SPLITS if require_all_splits else [split for split in SPLITS if split_counts[split]]
    for earlier, later in zip(splits_to_compare, splits_to_compare[1:]):
        if earlier in last_label and later in first_cutoff:
            if last_label[earlier] >= first_cutoff[later]:
                issues[f"{earlier}_labels_overlap_{later}_cutoff"] += 1
    return examples, split_counts, outcome_counts


def evaluate(cohort, features, *, require_all_splits=True):
    issues = Counter()
    examples, split_counts, outcome_counts = cohort_metadata(cohort, issues, require_all_splits)
    feature_examples = set()
    feature_rows = 0
    for row in features:
        feature_rows += 1
        cutoff = examples.get(row["modification_id"])
        if cutoff is None:
            issues["unknown_feature_modification"] += 1
            continue
        event, available = (timestamp(row[field]) for field in ("event_at", "available_at"))
        if row["feature"] not in FEATURES:
            issues["unapproved_feature"] += 1
        if event >= cutoff:
            issues["feature_event_at_or_after_cutoff"] += 1
        if available >= cutoff:
            issues["feature_available_at_or_after_cutoff"] += 1
        if available < event:
            issues["feature_available_before_event"] += 1
        feature_examples.add(row["modification_id"])

    missing = len(examples) - len(feature_examples)
    if missing:
        issues["modifications_without_feature_rows"] = missing
    return {
        "status": "fail" if issues else "pass",
        "modifications": len(examples),
        "feature_rows": feature_rows,
        "by_split": {split: split_counts[split] for split in SPLITS},
        "outcome_metadata_by_disposition": {name: outcome_counts[name] for name in sorted(DISPOSITIONS)},
        "violations": dict(sorted(issues.items())),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cohort", required=True, type=Path)
    parser.add_argument("--features", required=True, type=Path)
    args = parser.parse_args()
    try:
        summary = evaluate(records(args.cohort, COHORT_FIELDS), records(args.features, FEATURE_FIELDS))
    except (ValueError, OSError, csv.Error):
        # Keep source values, file names, and loan identifiers out of the output.
        summary = {"status": "fail", "violations": {"invalid_input": 1}}
        print(json.dumps(summary, indent=2))
        return 2
    print(json.dumps(summary, indent=2))
    return 0 if summary["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
