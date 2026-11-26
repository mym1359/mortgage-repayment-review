"""Measure month-six evidence available from the archived December 2016 HAMP file."""

import argparse
import base64
from datetime import date
import gzip
import hashlib
import json
from pathlib import Path
import tempfile
from xml.etree import ElementTree
from zipfile import ZipFile

import duckdb
import pyarrow as pa
from pyarrow import csv as arrow_csv

from hamp_reconstruct import attach


CAPTURE = "2016-12-16T03:02:03Z"
CAPTURE_DATE = date.fromisoformat(CAPTURE[:10])
ARCHIVE_DIGEST = "S7YAOKBAH7R3A4XTVEZ4URDF7ER6LXDE"
ORIGINAL_URL = b"http://mhadatafile.treasury.gov/Prod/reports/HMP_Public_User_Mod_Data_All.zip"
ARCHIVE_BYTES = 858_396_013
SOURCE_COLUMNS = (
    "mha_ln_id", "fncl_ast_id", "ln_st_nme", "ln_mdfc_mode_nme",
    "ln_mdfc_eff_dt", "ln_lpi_dt", "last_rptd_mthy_acvy_dt",
)


def rows(connection, statement, parameters=()):
    cursor = connection.execute(statement, parameters)
    names = [column[0] for column in cursor.description]
    return [dict(zip(names, row, strict=True)) for row in cursor.fetchall()]


def archived_headers(source):
    headers = {}
    for line in iter(source.readline, b""):
        if not line.strip():
            return headers
        key, value = line.split(b":", 1)
        headers[key.lower()] = value.strip()
    raise ValueError("Archived response has incomplete headers.")


def extract_warc(warc, target):
    with gzip.open(warc, "rb") as source, target.open("xb") as destination:
        if not source.readline().startswith(b"WARC/"):
            raise ValueError("Input must contain the indexed gzip-compressed WARC record.")
        headers = archived_headers(source)
        if headers.get(b"warc-target-uri") != ORIGINAL_URL or headers.get(b"warc-date") != CAPTURE.encode():
            raise ValueError("WARC target or capture date differs from the indexed record.")
        status = source.readline().split()
        http_headers = archived_headers(source)
        if status[1:2] != [b"200"] or int(http_headers.get(b"content-length", b"0")) != ARCHIVE_BYTES:
            raise ValueError("The archived response does not contain the full ZIP payload.")
        remaining = ARCHIVE_BYTES
        while remaining:
            block = source.read(min(remaining, 4 * 1024 * 1024))
            if not block:
                raise ValueError("Archived payload ended before its declared length.")
            destination.write(block)
            remaining -= len(block)
        if source.read(16) != b"\r\n\r\n":
            raise ValueError("Expected exactly one complete WARC response.")


def stage(connection, source):
    reader = arrow_csv.open_csv(
        source, read_options=arrow_csv.ReadOptions(use_threads=False, block_size=8 * 1024 * 1024),
        parse_options=arrow_csv.ParseOptions(newlines_in_values=True),
        convert_options=arrow_csv.ConvertOptions(
            include_columns=SOURCE_COLUMNS,
            column_types={column: pa.string() for column in SOURCE_COLUMNS},
            strings_can_be_null=True,
            null_values=[""],
        ),
    )
    connection.execute("""
        CREATE TABLE snapshot (
            loan BIGINT, modification BIGINT, state VARCHAR, mode VARCHAR,
            effective_date DATE, last_due_date DATE, processed_date DATE
        )
    """)
    connection.execute("BEGIN")
    for index, batch in enumerate(reader, start=1):
        connection.register("source_batch", pa.Table.from_batches([batch]))
        connection.execute("""
            INSERT INTO snapshot
            SELECT CAST(mha_ln_id AS BIGINT), CAST(fncl_ast_id AS BIGINT),
                   ln_st_nme, ln_mdfc_mode_nme, CAST(ln_mdfc_eff_dt AS DATE),
                   CAST(ln_lpi_dt AS DATE), CAST(last_rptd_mthy_acvy_dt AS DATE)
            FROM source_batch
        """)
        connection.unregister("source_batch")
        if index % 64 == 0:
            connection.execute("COMMIT; BEGIN")
            pa.default_memory_pool().release_unused()
    connection.execute("COMMIT")


def evidence(connection):
    connection.execute("""
        CREATE TEMP VIEW reference AS
        SELECT loan, modification, effective_date,
               CAST(effective_date + INTERVAL '6 months' AS DATE) AS cutoff
        FROM latest_archive.latest
        WHERE kind = 'Modification Information' AND program = 'Tier 1 HAMP'
    """)
    if connection.execute("""
        SELECT count(*) FROM
            (SELECT modification FROM reference GROUP BY modification
             HAVING modification IS NULL OR count(*) <> 1)
    """).fetchone()[0]:
        raise ValueError("Tier 1 reference has ambiguous modification IDs.")
    by_year = rows(connection, """
        WITH matched AS (
            SELECT s.loan, s.modification, count(*) AS raw_rows,
                   count(DISTINCT (s.state, s.effective_date, s.last_due_date, s.processed_date))
                       AS variants,
                   min(s.state) AS state,
                   min(s.effective_date) AS effective_date,
                   min(s.last_due_date) AS last_due_date, min(s.processed_date) AS processed_date
            FROM snapshot s JOIN reference r USING (loan, modification)
            WHERE s.mode = 'Official Modification'
            GROUP BY s.loan, s.modification
        ), assessed AS (
            SELECT year(r.effective_date) AS year, m.raw_rows, m.state, m.last_due_date,
                   m.processed_date, r.cutoff,
                   CASE
                     WHEN m.variants IS NULL THEN 'unmatched'
                     WHEN m.variants > 1 THEN 'conflicting_snapshot'
                     WHEN m.effective_date IS DISTINCT FROM r.effective_date THEN 'different_effective_date'
                     WHEN CAST(? AS DATE) >= r.cutoff THEN 'snapshot_at_or_after_cutoff'
                     ELSE 'snapshot_before_cutoff'
                   END AS availability
            FROM reference r LEFT JOIN matched m USING (loan, modification)
        )
        SELECT year, count(*) AS reference_modifications,
               count(*) FILTER (WHERE raw_rows IS NOT NULL) AS matched,
               coalesce(sum(raw_rows - 1), 0)::BIGINT AS surplus_matched_source_rows,
               count(*) FILTER (WHERE availability = 'conflicting_snapshot') AS conflicting_snapshot,
               count(*) FILTER (WHERE availability = 'different_effective_date') AS different_effective_date,
               count(*) FILTER (WHERE availability = 'snapshot_at_or_after_cutoff') AS snapshot_at_or_after_cutoff,
               count(*) FILTER (WHERE availability = 'snapshot_before_cutoff') AS snapshot_before_cutoff,
               count(*) FILTER (WHERE availability = 'snapshot_before_cutoff'
                   AND cutoff - INTERVAL '1 month' <= CAST(? AS DATE)
               ) AS snapshot_during_month_six,
               count(*) FILTER (
                   WHERE availability = 'snapshot_before_cutoff' AND state IN ('Active Payment', 'Active Non-Payment', 'Active')
                       AND last_due_date IS NOT NULL AND processed_date IS NOT NULL
                       AND processed_date <= CAST(? AS DATE)
               ) AS earlier_snapshot_with_active_state_and_payment_fields
        FROM assessed GROUP BY year ORDER BY year
    """, [CAPTURE_DATE, CAPTURE_DATE, CAPTURE_DATE])
    for row in by_year:
        if row["matched"] != sum(row[key] for key in (
            "conflicting_snapshot", "different_effective_date",
            "snapshot_at_or_after_cutoff", "snapshot_before_cutoff",
        )):
            raise ValueError("Snapshot assessment counts do not reconcile.")
    return by_year


def profile(archive, latest, work_dir):
    with archive.open("rb") as handle:
        digest = base64.b32encode(hashlib.file_digest(handle, "sha1").digest()).decode()
        handle.seek(0)
        sha256 = hashlib.file_digest(handle, "sha256").hexdigest()
    if digest != ARCHIVE_DIGEST:
        raise ValueError("The archive payload does not match the indexed capture.")
    with ZipFile(archive) as bundle, tempfile.TemporaryDirectory(dir=work_dir) as temp:
        csv_member, = (item for item in bundle.infolist() if item.filename.endswith(".csv"))
        meta_member, = (item for item in bundle.infolist() if item.filename.endswith(".meta"))
        metadata = ElementTree.fromstring(bundle.read(meta_member))
        expected = int(metadata.find(".//payloadFileMetaInfo").attrib["recordCount"])
        with duckdb.connect(str(Path(temp) / "snapshot.duckdb")) as connection:
            connection.execute("SET memory_limit = '2GB'; SET threads = 2")
            with bundle.open(csv_member) as source:
                stage(connection, source)
            source_profile = rows(connection, """
                SELECT count(*) AS rows, count(processed_date) AS rows_with_processing_date,
                       min(processed_date) AS earliest_processing_date,
                       max(processed_date) AS latest_processing_date
                FROM snapshot
            """)[0]
            if source_profile["rows"] != expected:
                raise ValueError("Parsed row count differs from the ZIP metadata.")
            attach(connection, "latest_archive", latest)
            by_year = evidence(connection)
    totals = {key: sum(row[key] for row in by_year) for key in by_year[0] if key != "year"}
    return {
        "capture_utc": CAPTURE,
        "archive_bytes": archive.stat().st_size,
        "archive_sha256": sha256,
        "archive_payload_sha1_base32": digest,
        "csv_member": csv_member.filename,
        "csv_uncompressed_bytes": csv_member.file_size,
        "metadata_rows": expected,
        "source_profile": source_profile,
        "tier1_by_effective_year": by_year,
        "tier1_totals": totals,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--archive", type=Path)
    source.add_argument("--warc", type=Path)
    parser.add_argument("--latest-db", required=True, type=Path)
    parser.add_argument("--work-dir", required=True, type=Path)
    args = parser.parse_args()
    if args.warc:
        with tempfile.TemporaryDirectory(dir=args.work_dir) as temp:
            archive = Path(temp) / "source.zip"
            extract_warc(args.warc, archive)
            result = profile(archive, args.latest_db, args.work_dir)
    else:
        result = profile(args.archive, args.latest_db, args.work_dir)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
