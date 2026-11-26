"""Summarize HAMP monthly evidence under the revised research partition."""

import argparse
import csv
from datetime import date, timedelta
import json
from pathlib import Path


TRAIN_LAST_MONTH = date(2012, 6, 1)
FIRST_VALIDATION_CUTOFF = date(2013, 7, 1)
PARTITIONS = ("train", "embargo", "validation", "gap", "test")
COUNT_FIELDS = (
    "reference_modifications",
    "retrospective_month_six_reports",
    "snapshot_before_cutoff",
    "snapshot_before_cutoff_with_active_payment_fields",
    "verified_month_six_available_by_cutoff",
    "verified_label_availability",
    "verified_month_six_and_label",
)


def partition(month):
    if month <= TRAIN_LAST_MONTH:
        return "train"
    if month.year == 2012:
        return "embargo"
    return {2013: "validation", 2014: "gap"}.get(month.year, "test")


def horizon_end(month):
    return month.replace(year=month.year + 1)


def month_six_cutoff(month):
    year_offset, month_index = divmod(month.month - 1 + 6, 12)
    return date(month.year + year_offset, month_index + 1, 1)


def month_rows(items):
    keyed = {date.fromisoformat(item["effective_month"]): item for item in items}
    if not keyed or len(keyed) != len(items):
        raise ValueError("Expected one entry per effective month.")
    return keyed


def coverage(payment_audit, snapshot_audits):
    if payment_audit["month_six_availability_independently_verified"] is not False:
        raise ValueError("This report expects an audit of untimestamped public monthly data.")
    payments = month_rows(payment_audit["by_effective_month"])
    snapshot_data = []
    for snapshot in snapshot_audits:
        capture = (snapshot.get("capture_date_utc") or snapshot["capture_utc"])[:10]
        observations = month_rows(snapshot["tier1_by_effective_month"])
        if observations.keys() != payments.keys():
            raise ValueError("Snapshot and payment audits must cover the same reference months.")
        snapshot_data.append((capture, observations))
    if not snapshot_data or len({capture for capture, _ in snapshot_data}) != len(snapshot_data):
        raise ValueError("Expected distinct archived snapshot audits.")

    monthly = []
    for month, payment in sorted(payments.items()):
        if month.day != 1 or not 2009 <= month.year <= 2017:
            raise ValueError(f"Unexpected Tier 1 effective month: {month}.")
        cutoff_lo = date.fromisoformat(payment["first_month_six_cutoff"])
        cutoff_hi = date.fromisoformat(payment["last_month_six_cutoff"])
        cutoff = cutoff_hi + timedelta(days=1)
        if (
            cutoff_lo != cutoff_hi or cutoff != month_six_cutoff(month)
            or not 0 <= payment["reported_proxy"] <= payment["modifications"]
        ):
            raise ValueError(f"Inconsistent retrospective audit for {month}.")
        candidates = []
        for capture, observations in snapshot_data:
            observation = observations[month]
            before = observation["snapshot_before_cutoff"]
            active = observation["earlier_snapshot_with_active_state_and_payment_fields"]
            if observation["reference_modifications"] != payment["modifications"] or not (
                0 <= active <= before <= payment["modifications"]
            ):
                raise ValueError(f"Snapshot counts do not reconcile for {month}.")
            if before:
                if date.fromisoformat(capture) >= cutoff:
                    raise ValueError(f"Pre-cutoff snapshot counts contradict {capture} for {month}.")
                candidates.append((capture, before, active))
        if len(candidates) > 1:
            raise ValueError("Overlapping snapshots require a loan-level join before deduplication.")
        capture, before, active = candidates[0] if candidates else ("", 0, 0)

        split = partition(month)
        end = horizon_end(month)
        if split == "train" and end >= FIRST_VALIDATION_CUTOFF:
            raise ValueError(f"Training follow-up overlaps validation for {month}.")
        monthly.append({
            "effective_month": month.isoformat(),
            "partition": split,
            "cutoff_exclusive": cutoff.isoformat(),
            "horizon_end_exclusive": end.isoformat(),
            "reference_modifications": payment["modifications"],
            "retrospective_month_six_reports": payment["reported_proxy"],
            "snapshot_capture_utc_date": capture,
            "snapshot_before_cutoff": before,
            "snapshot_before_cutoff_with_active_payment_fields": active,
            # Audited archives lack timing evidence for these claims at record level.
            "verified_month_six_available_by_cutoff": 0,
            "verified_label_availability": 0,
            "verified_month_six_and_label": 0,
        })
    totals = {}
    for label in PARTITIONS:
        included = [row for row in monthly if row["partition"] == label]
        if not included:
            raise ValueError(f"Missing proposed partition: {label}.")
        totals[label] = {
            "effective_months": len(included),
            **{key: sum(row[key] for row in included) for key in COUNT_FIELDS},
        }
    return {
        "status": "insufficient_source_evidence_for_evaluation",
        "training_last_effective_month": TRAIN_LAST_MONTH.isoformat(),
        "first_validation_cutoff": FIRST_VALIDATION_CUTOFF.isoformat(),
        "totals_by_partition": totals,
        "monthly_cohorts": monthly,
    }


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--payment-audit", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path, action="append", required=True)
    parser.add_argument("--monthly-csv", type=Path)
    args = parser.parse_args()
    report = coverage(read_json(args.payment_audit), [read_json(path) for path in args.snapshot])
    if args.monthly_csv:
        rows = report["monthly_cohorts"]
        with args.monthly_csv.open("w", encoding="utf-8", newline="") as output:
            writer = csv.DictWriter(output, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
