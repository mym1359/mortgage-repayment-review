"""Audit regional Treasury releases using digest-verified archived payloads."""

import argparse
import base64
from contextlib import contextmanager
import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path
import tempfile
from zipfile import ZipFile

import duckdb

from hamp_2016_snapshot import SOURCE_COLUMNS, evidence, rows, stage
from hamp_reconstruct import attach


@contextmanager
def csv_member(path):
    if path.suffix.lower() == ".zip":
        with ZipFile(path) as archive:
            member, = (item for item in archive.infolist() if item.filename.endswith(".csv"))
            with archive.open(member) as handle:
                yield handle, member.filename
    elif path.suffix.lower() == ".csv":
        with path.open("rb") as handle:
            yield handle, path.name
    else:
        raise ValueError("Expected a CSV or a ZIP containing one CSV.")


def audit(manifest_path, source_dir, latest_db, work_dir):
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    capture_times = [datetime.strptime(entry["capture_utc"], "%Y%m%d%H%M%S") for entry in manifest]
    if not manifest or len({capture.date() for capture in capture_times}) != 1:
        raise ValueError("A release must contain verified captures from the same UTC date.")
    if len({entry["file"] for entry in manifest}) != len(manifest):
        raise ValueError("Each regional payload must appear once in the manifest.")
    capture_date = max(capture_times).date()

    sources = []
    with tempfile.TemporaryDirectory(dir=work_dir) as scratch, duckdb.connect(
        str(Path(scratch) / "regional.duckdb")
    ) as connection:
        connection.execute("SET memory_limit = '2GB'; SET threads = 2")
        join_columns = set()
        for item in manifest:
            name = item["file"]
            if Path(name).name != name:
                raise ValueError("Manifest files must be direct children of the input directory.")
            input_path = source_dir / name
            if input_path.stat().st_size != item["bytes"]:
                raise ValueError(f"Archived payload size mismatch for {name}.")
            with input_path.open("rb") as handle:
                digest = base64.b32encode(hashlib.file_digest(handle, "sha1").digest()).decode()
                handle.seek(0)
                sha256 = hashlib.file_digest(handle, "sha256").hexdigest()
            if digest != item["payload_sha1_base32"] or sha256 != item["sha256"]:
                raise ValueError(f"Archived payload digest mismatch for {name}.")

            with csv_member(input_path) as (stream, member):
                columns = next(csv.reader([stream.readline().decode("utf-8-sig")]))
            if not set(SOURCE_COLUMNS[1:]).issubset(columns):
                raise ValueError(f"Required research columns are missing from {name}.")
            has_loan_id = SOURCE_COLUMNS[0] in columns
            join_columns.add(has_loan_id)
            if len(join_columns) > 1:
                raise ValueError("Regional files disagree on whether they contain a loan ID.")
            with csv_member(input_path) as (stream, _):
                stage(connection, stream, has_loan_id)
            sources.append({**item, "csv_member": member, "columns": len(columns)})

        profile = rows(connection, """
            SELECT count(*) AS rows, count(processed_date) AS rows_with_processing_date,
                   min(processed_date) AS earliest_processing_date,
                   max(processed_date) AS latest_processing_date
            FROM snapshot
        """)[0]
        attach(connection, "latest_archive", latest_db)
        has_loan_id, = join_columns
        yearly = evidence(connection, capture_date, match_loan_id=has_loan_id)

    partitions = {"train": 0, "validation": 0, "gap": 0, "test": 0}
    for item in yearly:
        year = item["year"]
        partition = "train" if year <= 2012 else {2013: "validation", 2014: "gap"}.get(year, "test")
        partitions[partition] += item["snapshot_before_cutoff"]
    return {
        "capture_date_utc": capture_date,
        "match_using_archive_loan_and_modification_ids": has_loan_id,
        "sources": sources,
        "source_profile": profile,
        "tier1_by_effective_year": yearly,
        "tier1_totals": {key: sum(item[key] for item in yearly) for key in yearly[0] if key != "year"},
        "snapshots_before_cutoff_by_partition": partitions,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("manifest", "source-dir", "latest-db", "work-dir"):
        parser.add_argument(f"--{name}", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.manifest, args.source_dir, args.latest_db, args.work_dir), indent=2, default=str))


if __name__ == "__main__":
    main()
