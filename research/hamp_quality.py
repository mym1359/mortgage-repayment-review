"""Profile an official HAMP supplemental archive and emit aggregate QA as JSON."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
from xml.etree import ElementTree
from zipfile import ZipFile

import duckdb


SOURCE_URL = "https://home.treasury.gov/system/files/256/HMP_Govt_Agency_Perf_Data.zip"
LISTING_URL = "https://home.treasury.gov/data/troubled-assets-relief-program/reports/mha-public-file"
GUIDE_URL = (
    "https://home.treasury.gov/system/files/136/"
    "HAMP%20Performance%20Supplemental%20Data%20File%20User%20Guide%20v1.0.pdf"
)
COLUMNS = (
    "rec_typ", "mha_ln_id", "fncl_ast_id", "pgm_mdfc_typ", "ln_mdfc_eff_dt",
    "ln_st_nme", "ln_mdfc_end_dt", "ln_owdrwn_rsn_nme", "ln_rcst_eff_yr",
    "ln_mthy_pi_with_rcst_amt", "ln_mthy_pi_wtho_rcst_amt", "ln_pmt_acvy_mth_dt",
    "ln_drvd_aft_mfdc_eff_dt_term", "ln_lpi_dt", "rptg_stat",
)
KEY = ("rec_typ", "fncl_ast_id", "ln_pmt_acvy_mth_dt")


def query_rows(connection, statement):
    cursor = connection.execute(statement)
    names = [column[0] for column in cursor.description]
    return [dict(zip(names, row, strict=True)) for row in cursor.fetchall()]


def profile_csv(connection, path):
    source = connection.read_csv(
        str(path), header=True, encoding="utf-8", delimiter=",", quotechar='"',
        all_varchar=True, strict_mode=True,
    )
    if tuple(source.columns) != COLUMNS:
        raise ValueError(f"Unexpected columns: {source.columns}")
    source.create("hamp")
    record_types = query_rows(connection, """
        SELECT rec_typ AS record_type, count(*) AS rows,
               count(DISTINCT mha_ln_id) AS distinct_loans,
               count(DISTINCT fncl_ast_id) AS distinct_modifications,
               count(*) FILTER (WHERE mha_ln_id IS NULL) AS missing_loan_id,
               count(*) FILTER (WHERE fncl_ast_id IS NULL) AS missing_modification_id
        FROM hamp GROUP BY rec_typ ORDER BY rec_typ
    """)
    if {row["record_type"] for row in record_types} != {
        "Modification Information", "Payment Information"
    }:
        raise ValueError(f"Unexpected record types: {record_types}")

    connection.execute("""
        CREATE TEMP VIEW modifications AS
        SELECT * FROM hamp WHERE rec_typ = 'Modification Information';
        CREATE TEMP VIEW payments AS
        SELECT *, try_cast(ln_pmt_acvy_mth_dt AS DATE) AS activity_date
        FROM hamp WHERE rec_typ = 'Payment Information';
    """)
    summary = query_rows(connection, """
        SELECT
            (SELECT count(*) FROM hamp) AS rows,
            (SELECT count(DISTINCT mha_ln_id) FROM hamp) AS distinct_loans,
            (SELECT count(DISTINCT fncl_ast_id) FROM hamp) AS distinct_modifications,
            (SELECT count(*) FROM (
                SELECT mha_ln_id FROM modifications WHERE mha_ln_id IS NOT NULL
                GROUP BY mha_ln_id HAVING count(DISTINCT fncl_ast_id) > 1
            )) AS loans_with_multiple_modifications,
            (SELECT count(*) FROM (
                SELECT fncl_ast_id FROM hamp WHERE fncl_ast_id IS NOT NULL
                GROUP BY fncl_ast_id HAVING count(DISTINCT mha_ln_id) > 1
            )) AS modification_ids_with_multiple_loans
    """)[0]
    modification_quality = query_rows(connection, """
        SELECT
            min(try_cast(ln_mdfc_eff_dt AS DATE)) AS earliest_effective_date,
            max(try_cast(ln_mdfc_eff_dt AS DATE)) AS latest_effective_date,
            count(*) FILTER (WHERE ln_mdfc_eff_dt IS NULL) AS missing_effective_date,
            count(*) FILTER (WHERE ln_mdfc_eff_dt IS NOT NULL
                AND try_cast(ln_mdfc_eff_dt AS DATE) IS NULL) AS invalid_effective_date,
            count(*) FILTER (WHERE pgm_mdfc_typ IS NULL) AS missing_program_type,
            count(*) FILTER (WHERE ln_st_nme IS NULL) AS missing_loan_state,
            count(*) FILTER (WHERE ln_pmt_acvy_mth_dt IS NOT NULL) AS unexpected_activity_period
        FROM modifications
    """)[0]
    payment_quality = query_rows(connection, """
        SELECT
            min(activity_date) AS earliest_activity,
            max(activity_date) AS latest_activity,
            count(DISTINCT date_trunc('month', activity_date)) AS activity_months,
            count(*) FILTER (WHERE ln_pmt_acvy_mth_dt IS NULL) AS missing_activity_period,
            count(*) FILTER (WHERE ln_pmt_acvy_mth_dt IS NOT NULL
                AND activity_date IS NULL) AS invalid_activity_period,
            count(*) FILTER (WHERE day(activity_date) <> 1) AS activity_not_first_of_month,
            count(*) FILTER (WHERE ln_lpi_dt IS NULL) AS missing_last_paid_installment_date,
            count(*) FILTER (WHERE ln_lpi_dt IS NOT NULL
                AND try_cast(ln_lpi_dt AS DATE) IS NULL) AS invalid_last_paid_installment_date,
            count(*) FILTER (WHERE rptg_stat IS NULL) AS missing_reporting_status,
            count(*) FILTER (WHERE ln_drvd_aft_mfdc_eff_dt_term IS NULL)
                AS missing_months_after_modification,
            count(*) FILTER (WHERE ln_drvd_aft_mfdc_eff_dt_term IS NOT NULL
                AND try_cast(ln_drvd_aft_mfdc_eff_dt_term AS INTEGER) IS NULL)
                AS invalid_months_after_modification,
            count(*) FILTER (WHERE try_cast(ln_drvd_aft_mfdc_eff_dt_term AS INTEGER)
                BETWEEN 6 AND 12) AS activity_rows_at_months_6_through_12
        FROM payments
    """)[0]
    activity = query_rows(connection, """
        SELECT activity_date, count(*) AS rows,
               count(DISTINCT mha_ln_id) AS distinct_loans,
               count(DISTINCT fncl_ast_id) AS distinct_modifications
        FROM payments GROUP BY activity_date ORDER BY activity_date
    """)
    reporting_status = query_rows(connection, """
        SELECT rptg_stat AS reporting_status, count(*) AS rows,
               count(*) FILTER (WHERE ln_lpi_dt IS NULL) AS missing_last_paid_installment_date
        FROM payments GROUP BY rptg_stat ORDER BY rptg_stat
    """)
    modification_cohorts = query_rows(connection, """
        SELECT pgm_mdfc_typ AS program_type,
               year(try_cast(ln_mdfc_eff_dt AS DATE)) AS effective_year,
               count(DISTINCT fncl_ast_id) AS distinct_modifications
        FROM modifications GROUP BY program_type, effective_year
        ORDER BY program_type, effective_year
    """)
    unmatched = query_rows(connection, """
        WITH modification_pairs AS (
            SELECT DISTINCT fncl_ast_id, mha_ln_id FROM modifications
        )
        SELECT count(*) AS payment_rows_without_matching_modification
        FROM payments p ANTI JOIN modification_pairs m
        USING (fncl_ast_id, mha_ln_id)
    """)[0]

    # The activity period is blank on modification rows by design.
    # Retain NULL in the key and compare it with NULL-safe equality.
    key_columns = ", ".join(KEY)
    connection.execute(f"""
        CREATE TEMP TABLE repeated_keys AS
        SELECT {key_columns}, count(*) AS occurrences
        FROM hamp WHERE fncl_ast_id IS NOT NULL
        GROUP BY {key_columns} HAVING count(*) > 1
    """)
    key_match = " AND ".join(
        f"h.{column} IS NOT DISTINCT FROM r.{column}" for column in KEY
    )
    connection.execute(f"""
        CREATE TEMP TABLE repeated_rows AS
        SELECT h.* FROM hamp h INNER JOIN repeated_keys r ON {key_match}
    """)
    distinct_variants = query_rows(connection, f"""
        WITH variants AS (
            SELECT DISTINCT * FROM repeated_rows
        ), per_key AS (
            SELECT {key_columns}, count(*) AS variants FROM variants
            GROUP BY {key_columns}
        )
        SELECT r.rec_typ AS record_type, count(*) AS repeated_keys,
               sum(r.occurrences - 1) AS surplus_rows,
               sum(r.occurrences - v.variants) AS exact_duplicate_surplus_rows,
               count(*) FILTER (WHERE v.variants > 1) AS conflicting_keys
        FROM repeated_keys r JOIN per_key v ON
           {" AND ".join(f"r.{column} IS NOT DISTINCT FROM v.{column}" for column in KEY)}
        GROUP BY r.rec_typ ORDER BY r.rec_typ
    """)
    return {
        "summary": summary,
        "record_types": record_types,
        "modification_quality": modification_quality,
        "payment_quality": payment_quality | unmatched,
        "activity_by_month": activity,
        "payment_reporting_status": reporting_status,
        "modification_cohorts": modification_cohorts,
        "repeated_keys_by_record_type": distinct_variants,
    }


def profile_archive(archive, work_dir, source_url, retrieved_on):
    with archive.open("rb") as handle:
        sha256 = hashlib.file_digest(handle, "sha256").hexdigest()
    with ZipFile(archive) as bundle, tempfile.TemporaryDirectory(dir=work_dir) as scratch:
        csv_member, = (entry for entry in bundle.infolist() if entry.filename.endswith(".csv"))
        meta_member, = (entry for entry in bundle.infolist() if entry.filename.endswith(".meta"))
        if meta_member.file_size > 1_000_000:
            raise ValueError("The metadata member is larger than expected.")
        metadata = ElementTree.fromstring(bundle.read(meta_member))
        expected_rows = int(metadata.find(".//payloadFileMetaInfo").attrib["recordCount"])
        csv_path = Path(scratch) / "source.csv"
        with bundle.open(csv_member) as source, csv_path.open("wb") as target:
            shutil.copyfileobj(source, target)
        with duckdb.connect(str(Path(scratch) / "work.duckdb")) as connection:
            connection.execute("SET memory_limit = '2GB'; SET threads = 4")
            profile = profile_csv(connection, csv_path)
    return {
        "source": {
            "archive_url": source_url,
            "listing_url": LISTING_URL,
            "data_guide_url": GUIDE_URL,
            "retrieved_on": retrieved_on,
            "archive_bytes": archive.stat().st_size,
            "archive_sha256": sha256,
            "csv_member": csv_member.filename,
            "csv_uncompressed_bytes": csv_member.file_size,
            "metadata_rows": expected_rows,
            "metadata_row_count_matches": expected_rows == profile["summary"]["rows"],
        },
        "duckdb_version": duckdb.__version__,
        **profile,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--retrieved-on", required=True, help="Download date in YYYY-MM-DD")
    parser.add_argument("--source-url", default=SOURCE_URL)
    args = parser.parse_args()
    report = profile_archive(args.archive, args.work_dir, args.source_url, args.retrieved_on)
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
