"""Review an authorized HAMP sample and emit only aggregate findings."""

import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path
import re

from hamp_evaluation_gate import evaluate, timestamp as parse_timestamp


class InvalidTimestamp(ValueError):
    pass


def timestamp(value):
    try:
        return parse_timestamp(value)
    except (ValueError, OverflowError) as error:
        raise InvalidTimestamp from error


def is_text(value):
    return isinstance(value, str) and bool(value.strip()) and value == value.strip()


def required_text(record, key):
    value = record.get(key)
    if not is_text(value):
        raise ValueError("Expected nonempty text.")
    return value


def month_index(value):
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}", value):
        raise ValueError("Expected a calendar month.")
    month = date.fromisoformat(value + "-01")
    return month.year * 12 + month.month


def check_source(source, kind, gaps, cutoff=None):
    if source is None or source == {}:
        gaps[kind + "_missing"] += 1
        return False
    if not isinstance(source, dict):
        raise ValueError("Expected a source record.")
    if (
        any(not is_text(source.get(field)) for field in
            ("source_ref", "version", "retrieved_at", "sha256", "event_at", "available_at"))
        or not re.fullmatch(r"[0-9a-fA-F]{64}", source["sha256"])
        or "supersedes" not in source
        or (source["supersedes"] is not None and (
            not is_text(source["supersedes"]) or source["supersedes"] == source["version"]
        ))
    ):
        gaps[kind + "_incomplete"] += 1
        return False

    event = timestamp(source["event_at"])
    available = timestamp(source["available_at"])
    retrieved = timestamp(source["retrieved_at"])
    if source.get("verified") is not True:
        gaps[kind + "_unverified"] += 1
        return False
    if not event <= available <= retrieved:
        gaps[kind + "_inconsistent_timing"] += 1
        return False
    if cutoff is not None and available >= cutoff:
        gaps[kind + "_late"] += 1
        return False
    return True


def check_report_history(report, history, gaps):
    if not isinstance(history, list):
        raise ValueError("Expected a list of previous report versions.")

    versions = {report["version"]: report}
    for version in history:
        if not check_source(version, "month_six_report_predecessor", gaps):
            continue
        if version["version"] in versions:
            gaps["month_six_report_duplicate_version"] += 1
        else:
            versions[version["version"]] = version

    visited = {report["version"]}
    current = report
    while current["supersedes"] is not None:
        predecessor_id = current["supersedes"]
        if predecessor_id not in versions:
            gaps["month_six_report_predecessor_missing"] += 1
            return
        predecessor = versions[predecessor_id]
        if (
            predecessor_id in visited
            or predecessor.get("activity_month") != report["activity_month"]
            or timestamp(predecessor["available_at"]) > timestamp(current["available_at"])
        ):
            gaps["month_six_report_predecessor_inconsistent"] += 1
            return
        visited.add(predecessor_id)
        current = predecessor
    if visited != versions.keys():
        gaps["month_six_report_history_has_unlinked_versions"] += 1


def review_sample(cases):
    if not isinstance(cases, list) or any(not isinstance(case, dict) for case in cases):
        raise ValueError("Expected a list of modification records.")

    gaps = Counter()
    cohort = []
    features = []
    if not cases:
        gaps["sample_empty"] = 1

    for case in cases:
        loan, modification, split, effective, cutoff_at, horizon = (
            required_text(case, field) for field in
            ("loan_id", "modification_id", "split", "effective_month", "cutoff_at", "horizon_end_at")
        )
        cutoff = timestamp(cutoff_at)
        timestamp(horizon)
        tier = case.get("program_tier")
        if type(tier) is not int or tier != 1 or case.get("permanent") is not True:
            gaps["permanent_tier_one_not_established"] += 1
        cutoff_month = cutoff.year * 12 + cutoff.month
        if cutoff_month != month_index(effective) + 6:
            gaps["cutoff_does_not_follow_month_six"] += 1

        report = case.get("month_six_report")
        if check_source(report, "month_six_report", gaps, cutoff):
            activity_month = report.get("activity_month")
            if not is_text(activity_month):
                gaps["activity_month_missing"] += 1
            elif month_index(activity_month) != cutoff_month - 1:
                gaps["report_is_not_month_six"] += 1
            else:
                check_report_history(report, case.get("month_six_report_history", []), gaps)

        active = case.get("active_status")
        if check_source(active, "active_status", gaps, cutoff):
            status_at = timestamp(active["event_at"])
            if active.get("active") is not True:
                gaps["active_status_not_established"] += 1
            elif status_at.year * 12 + status_at.month != cutoff_month - 1:
                gaps["active_status_not_for_month_six"] += 1

        outcome = case.get("outcome")
        if check_source(outcome, "outcome", gaps):
            if not is_text(outcome.get("disposition")):
                gaps["outcome_disposition_missing"] += 1
            else:
                cohort.append({
                    "loan_id": loan, "modification_id": modification, "split": split,
                    "cutoff_at": cutoff_at, "horizon_end_at": horizon,
                    "disposition": outcome["disposition"], "evidence_at": outcome["event_at"],
                    "label_available_at": outcome["available_at"],
                })

        case_features = case.get("features", [])
        if case_features is None:
            case_features = []
        if not isinstance(case_features, list):
            raise ValueError("Expected a list of feature sources.")
        if not case_features:
            gaps["feature_sources_missing"] += 1
        for feature in case_features:
            if not check_source(feature, "feature_source", gaps, cutoff):
                continue
            name = required_text(feature, "feature")
            if name == "last_installment_month_gap":
                if not is_text(feature.get("due_date")) or not is_text(feature.get("posted_at")):
                    gaps["installment_dates_incomplete"] += 1
                    continue
                if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", feature["due_date"]):
                    raise ValueError("Expected an installment due date.")
                date.fromisoformat(feature["due_date"])
                if timestamp(feature["posted_at"]) != timestamp(feature["event_at"]):
                    gaps["installment_event_does_not_match_posting"] += 1
                    continue
            features.append({
                "modification_id": modification, "feature": name,
                "event_at": feature["event_at"], "available_at": feature["available_at"],
            })

    result = {
        "status": "insufficient_evidence",
        "modification_rows": len(cases),
        "evidence_gaps": dict(sorted(gaps.items())),
    }
    if cohort:
        covered = {row["modification_id"] for row in cohort}
        available_features = [row for row in features if row["modification_id"] in covered]
        metadata = evaluate(cohort, available_features, require_all_splits=False)
        result["metadata"] = metadata
        if not gaps:
            result["status"] = "sample_supported" if metadata["status"] == "pass" else "metadata_rejected"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = review_sample(json.loads(args.sample.read_text(encoding="utf-8-sig")))
    except OSError:
        result = {"status": "invalid_input", "reason": "unreadable_file"}
    except (json.JSONDecodeError, UnicodeError, RecursionError):
        result = {"status": "invalid_input", "reason": "invalid_json"}
    except InvalidTimestamp:
        result = {"status": "invalid_input", "reason": "invalid_timestamp"}
    except (ValueError, OverflowError):
        result = {"status": "invalid_input", "reason": "invalid_record"}
    # Source paths, identifiers and field values belong in the private review.
    print(json.dumps(result, indent=2))
    if result["status"] == "invalid_input":
        return 2
    return 0 if result["status"] == "sample_supported" else 1


if __name__ == "__main__":
    raise SystemExit(main())
