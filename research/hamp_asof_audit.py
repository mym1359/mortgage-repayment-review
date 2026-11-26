"""Audit HAMP month-six event coverage and evidence of data availability."""

import argparse
import json
from pathlib import Path

import duckdb

from hamp_reconstruct import attach


def rows(connection, sql):
    cursor = connection.execute(sql)
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row, strict=True)) for row in cursor.fetchall()]


def audit(connection):
    connection.execute("""
        CREATE TEMP VIEW tier1 AS
        SELECT loan, modification, effective_date, state, end_date,
               CAST(effective_date + INTERVAL '5 months' AS DATE) AS month_six
        FROM latest_archive.latest
        WHERE kind = 'Modification Information' AND program = 'Tier 1 HAMP'
    """)
    if rows(connection, """
        SELECT modification FROM tier1
        GROUP BY modification HAVING modification IS NULL OR count(*) <> 1 LIMIT 1
    """):
        raise ValueError("Expected one latest Tier 1 row for each modification.")

    by_year = rows(connection, """
        WITH payments AS (
            SELECT loan, modification, activity_date, reporting, installment_due_date
            FROM historical_archive.historical WHERE kind = 'Payment Information' AND age = 6
            UNION ALL
            SELECT loan, modification, activity_date, reporting, installment_due_date
            FROM monthly_archive.monthly_update WHERE kind = 'Payment Information' AND age = 6
        ), selected AS (
            SELECT loan, modification, activity_date,
                   count(DISTINCT (reporting, installment_due_date)) AS variants,
                   min(reporting) AS reporting, min(installment_due_date) AS installment_due_date
            FROM payments GROUP BY loan, modification, activity_date
        ), classified AS (
            SELECT year(t.effective_date) AS year, t.loan,
                   last_day(t.month_six) AS cutoff,
                   CASE
                       WHEN t.end_date <= last_day(t.month_six) THEN 'exit_by_cutoff'
                       WHEN p.variants IS NULL THEN 'no_month_six_row'
                       WHEN p.variants > 1 THEN 'conflicting_month_six'
                       WHEN p.reporting IS DISTINCT FROM 'Reported'
                           OR p.installment_due_date IS NULL THEN 'no_usable_report'
                       WHEN p.installment_due_date > last_day(t.month_six)
                           THEN 'due_after_cutoff'
                       ELSE 'reported_proxy'
                   END AS disposition
            FROM tier1 t LEFT JOIN selected p
            ON p.loan = t.loan AND p.modification = t.modification
               AND p.activity_date = t.month_six
        )
        SELECT year, count(*) AS modifications, count(DISTINCT loan) AS loans,
               min(cutoff) AS first_month_six_cutoff, max(cutoff) AS last_month_six_cutoff,
               count(*) FILTER (WHERE disposition = 'exit_by_cutoff') AS retrospective_exit_by_cutoff,
               count(*) FILTER (WHERE disposition = 'no_month_six_row') AS no_month_six_row,
               count(*) FILTER (WHERE disposition = 'conflicting_month_six') AS conflicting_month_six,
               count(*) FILTER (WHERE disposition = 'no_usable_report') AS no_usable_report,
               count(*) FILTER (WHERE disposition = 'due_after_cutoff') AS due_after_cutoff,
               count(*) FILTER (WHERE disposition = 'reported_proxy') AS reported_proxy
        FROM classified GROUP BY year ORDER BY year
    """)
    revision_checks = rows(connection, """
        WITH older AS (
            SELECT 'historical' AS snapshot, loan, modification, effective_date, state, end_date
            FROM historical_archive.historical WHERE kind = 'Modification Information'
            UNION ALL
            SELECT 'monthly_update', loan, modification, effective_date, state, end_date
            FROM monthly_archive.monthly_update WHERE kind = 'Modification Information'
        )
        SELECT snapshot, count(*) AS paired_modifications,
               count(*) FILTER (WHERE o.effective_date IS DISTINCT FROM t.effective_date) AS different_effective_date,
               count(*) FILTER (WHERE o.state IS DISTINCT FROM t.state) AS different_state,
               count(*) FILTER (WHERE o.end_date IS DISTINCT FROM t.end_date) AS different_end_date,
               count(*) FILTER (WHERE coalesce(o.end_date <= last_day(t.month_six), false)
                    IS DISTINCT FROM coalesce(t.end_date <= last_day(t.month_six), false))
                    AS different_retrospective_exit_at_month_six
        FROM older o JOIN tier1 t USING (loan, modification)
        GROUP BY snapshot ORDER BY snapshot
    """)
    categories = (
        "retrospective_exit_by_cutoff", "no_month_six_row", "conflicting_month_six",
        "no_usable_report", "due_after_cutoff", "reported_proxy",
    )
    for row in by_year:
        if sum(row[key] for key in categories) != row["modifications"]:
            raise ValueError(f"Inconsistent month-six category totals for {row['year']}.")
    return {
        "cohort": "Tier 1 HAMP permanent modifications",
        "per_record_first_available_timestamp_in_supplied_schema": False,
        "month_six_availability_independently_verified": False,
        "by_effective_year": by_year,
        "totals": {key: sum(row[key] for row in by_year) for key in ("modifications", *categories)},
        "snapshot_comparison_to_2023": revision_checks,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("historical-db", "monthly-db", "latest-db"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    args = parser.parse_args()
    with duckdb.connect() as connection:
        connection.execute("SET memory_limit = '2GB'; SET threads = 3")
        attach(connection, "historical_archive", args.historical_db)
        attach(connection, "monthly_archive", args.monthly_db)
        attach(connection, "latest_archive", args.latest_db)
        result = audit(connection)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
