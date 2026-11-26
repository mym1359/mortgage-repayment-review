"""Audit the proposed HAMP partitions using calendar boundaries only."""

import argparse
import json
from pathlib import Path

import duckdb

from hamp_reconstruct import attach


def query(connection, sql):
    result = connection.execute(sql)
    fields = [column[0] for column in result.description]
    return [dict(zip(fields, row, strict=True)) for row in result.fetchall()]


def audit(connection):
    connection.execute("""
        CREATE TEMP VIEW calendar AS
        SELECT loan, modification, effective_date,
               CASE
                 WHEN year(effective_date) BETWEEN 2009 AND 2012 THEN 'train'
                 WHEN year(effective_date) = 2013 THEN 'validation'
                 WHEN year(effective_date) = 2014 THEN 'gap'
                 WHEN year(effective_date) BETWEEN 2015 AND 2017 THEN 'test'
               END AS partition,
               (effective_date + INTERVAL '6 months')::DATE AS cutoff,
               (effective_date + INTERVAL '12 months')::DATE AS horizon_end
        FROM latest_archive.latest
        WHERE kind = 'Modification Information' AND program = 'Tier 1 HAMP'
    """)
    invalid = connection.execute("""
        SELECT count(*) FROM calendar
        WHERE partition IS NULL OR loan IS NULL OR modification IS NULL OR day(effective_date) <> 1
    """).fetchone()[0]
    if invalid or connection.execute("""
        SELECT count(*) <> count(DISTINCT modification) FROM calendar
    """).fetchone()[0]:
        raise ValueError("Tier 1 snapshot has invalid or ambiguous calendar records.")

    partitions = query(connection, """
        SELECT partition, count(*) AS modifications, count(DISTINCT cutoff) AS cutoff_months,
               min(cutoff) AS first_cutoff, max(cutoff) AS last_cutoff,
               min(horizon_end) AS first_horizon_end, max(horizon_end) AS last_horizon_end
        FROM calendar GROUP BY partition ORDER BY first_cutoff
    """)
    if {partition["partition"] for partition in partitions} != {"train", "validation", "gap", "test"}:
        raise ValueError("Expected all four proposed calendar partitions.")

    adjacent = query(connection, """
        WITH boundaries AS (
            SELECT before, after, min(cutoff) AS next_cutoff
            FROM (VALUES ('train', 'validation'), ('validation', 'test')) pairs(before, after)
            JOIN calendar c ON c.partition = after
            GROUP BY before, after
        )
        SELECT before AS earlier_partition, after AS later_partition, next_cutoff,
               count(*) AS earlier_modifications,
               count(*) FILTER (WHERE horizon_end >= next_cutoff) AS not_mature_by_boundary,
               min(effective_date) FILTER (WHERE horizon_end >= next_cutoff) AS first_affected_effective_date,
               max(effective_date) FILTER (WHERE horizon_end >= next_cutoff) AS last_affected_effective_date
        FROM boundaries JOIN calendar ON calendar.partition = before
        GROUP BY before, after, next_cutoff ORDER BY next_cutoff
    """)
    crossing_loans = connection.execute("""
        SELECT count(*) FROM (
            SELECT loan FROM calendar WHERE partition <> 'gap'
            GROUP BY loan HAVING count(DISTINCT partition) > 1
        )
    """).fetchone()[0]
    return {
        "assumption": "Uniform complete follow-up through month 12, with zero reporting delay.",
        "partitions": partitions,
        "adjacent_partition_boundaries": adjacent,
        "loans_in_multiple_analysis_partitions": crossing_loans,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--latest-db", required=True, type=Path)
    args = parser.parse_args()
    with duckdb.connect() as connection:
        attach(connection, "latest_archive", args.latest_db)
        result = audit(connection)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
