"""Stage projected HAMP records by streaming a ZIP in bounded batches."""

import argparse
import base64
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from xml.etree import ElementTree
from zipfile import ZipFile

import duckdb
import pyarrow as pa
from pyarrow import csv as arrow_csv


AGE_COLUMNS = {"ln_drvd_aft_mfdc_eff_dt_term", "ln_drvd_aft_mdfc_eff_dt_term"}


def stage_csv(database, table, stream, age_column):
    columns = (
        "rec_typ", "mha_ln_id", "fncl_ast_id", "pgm_mdfc_typ", "ln_mdfc_eff_dt",
        "ln_st_nme", "ln_mdfc_end_dt", "ln_pmt_acvy_mth_dt", age_column,
        "ln_lpi_dt", "rptg_stat",
    )
    reader = arrow_csv.open_csv(
        stream, read_options=arrow_csv.ReadOptions(use_threads=False, block_size=8 * 1024 * 1024),
        convert_options=arrow_csv.ConvertOptions(
            include_columns=columns, column_types={column: pa.string() for column in columns},
            strings_can_be_null=True, null_values=[""],
        ),
    )
    with duckdb.connect(str(database)) as connection:
        connection.execute("SET memory_limit = '2GB'; SET threads = 2")
        connection.execute("BEGIN")
        connection.execute(f"""
            CREATE OR REPLACE TABLE {table} (
                kind VARCHAR, loan BIGINT, modification BIGINT, program VARCHAR,
                effective_date DATE, state VARCHAR, end_date DATE, activity_date DATE,
                age INTEGER, installment_due_date DATE, reporting VARCHAR
            );
            CREATE TEMP TABLE batch_counts (
                kind VARCHAR, activity_date DATE, records BIGINT, target_rows BIGINT
            )
        """)
        for index, batch in enumerate(reader, start=1):
            connection.register("hamp_batch", pa.Table.from_batches([batch]))
            connection.execute(f"""
                INSERT INTO batch_counts
                SELECT rec_typ, CAST(ln_pmt_acvy_mth_dt AS DATE), count(*),
                       count(*) FILTER (WHERE CAST({age_column} AS INTEGER) IN (6, 12))
                FROM hamp_batch GROUP BY ALL
            """)
            connection.execute(f"""
                INSERT INTO {table}
                SELECT rec_typ, CAST(mha_ln_id AS BIGINT), CAST(fncl_ast_id AS BIGINT),
                       pgm_mdfc_typ, CAST(ln_mdfc_eff_dt AS DATE), ln_st_nme,
                       CAST(ln_mdfc_end_dt AS DATE), CAST(ln_pmt_acvy_mth_dt AS DATE),
                       CAST({age_column} AS INTEGER), CAST(ln_lpi_dt AS DATE), rptg_stat
                FROM hamp_batch WHERE rec_typ <> 'Payment Information'
                    OR CAST({age_column} AS INTEGER) IN (6, 12)
            """)
            connection.unregister("hamp_batch")
            if index % 64 == 0:
                connection.execute("COMMIT; BEGIN")
                pa.default_memory_pool().release_unused()
        connection.execute(f"""
            CREATE OR REPLACE TABLE {table}_coverage AS
            SELECT kind, activity_date, sum(records)::BIGINT AS records,
                   sum(target_rows)::BIGINT AS target_rows
            FROM batch_counts GROUP BY kind, activity_date
        """)
        keys = ("record_type", "rows", "earliest_activity", "latest_activity",
                "activity_months", "rows_at_month_6_or_12")
        facts = [dict(zip(keys, row, strict=True)) for row in connection.execute(f"""
            SELECT kind, sum(records)::BIGINT, min(activity_date), max(activity_date),
                   count(activity_date), sum(target_rows)::BIGINT
            FROM {table}_coverage GROUP BY kind ORDER BY kind
        """).fetchall()]
        if {item["record_type"] for item in facts} != {"Modification Information", "Payment Information"}:
            raise ValueError(f"Unexpected record types: {facts}")
        connection.execute("COMMIT")
        return facts


def source_manifest(archive):
    with ZipFile(archive) as bundle:
        entry, = (item for item in bundle.infolist() if item.filename.endswith(".csv"))
        metadata_files = [item for item in bundle.infolist() if item.filename.endswith(".meta")]
        declared_rows = None
        if metadata_files:
            member, = metadata_files
            metadata = ElementTree.fromstring(bundle.read(member))
            declared_rows = int(metadata.find(".//payloadFileMetaInfo").attrib["recordCount"])
    with archive.open("rb") as source:
        sha256 = hashlib.file_digest(source, "sha256").hexdigest()
        source.seek(0)
        wayback_sha1 = base64.b32encode(hashlib.file_digest(source, "sha1").digest()).decode()
    return {
        "archive_bytes": archive.stat().st_size, "archive_sha256": sha256,
        "payload_sha1_base32": wayback_sha1, "csv": entry.filename,
        "csv_bytes": entry.file_size, "declared_rows": declared_rows,
    }


def stage_archive(database, table, archive):
    manifest = source_manifest(archive)
    command = ["unzip", "-p", str(archive), manifest["csv"]]
    with subprocess.Popen(command, stdout=subprocess.PIPE) as unzip:
        first_line = unzip.stdout.readline()
        unzip.terminate()
    fields = next(csv.reader([first_line.decode("utf-8-sig")]))
    age_column, = AGE_COLUMNS.intersection(fields)
    with tempfile.TemporaryDirectory(dir=database.parent) as scratch:
        staging = Path(scratch) / "stage.duckdb"
        with subprocess.Popen(command, stdout=subprocess.PIPE) as unzip:
            try:
                records = stage_csv(staging, table, unzip.stdout, age_column)
            except BaseException:
                unzip.terminate()
                raise
            if unzip.wait():
                raise RuntimeError(f"Could not decompress {manifest['csv']}")
        if manifest["declared_rows"] is not None:
            if sum(row["rows"] for row in records) != manifest["declared_rows"]:
                raise ValueError("CSV row count does not match the archive metadata.")
        staging.replace(database)
    return {"source": manifest, "record_types": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database", type=Path)
    parser.add_argument("table", choices=["historical", "monthly_update", "latest"])
    parser.add_argument("--archive", type=Path, required=True)
    args = parser.parse_args()
    report = stage_archive(args.database, args.table, args.archive)
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
