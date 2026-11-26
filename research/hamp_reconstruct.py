"""Compare exploratory HAMP month-6 and month-12 rates with Treasury's table."""

import argparse
import json
from pathlib import Path
import re

import duckdb


PROGRAMS = ("Tier 1 HAMP", "Tier 2 HAMP")
HORIZONS = (6, 12)


def reference_rates(path):
    rates = {}
    tier = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if "Performance of HAMP Permanent Modifications - " in line:
            match = re.search(r" - Tier ([12])\s*$", line)
            tier = int(match[1]) if match else None
        fields = line.split()
        if tier and fields and re.fullmatch(r"20\d\d", fields[0]):
            year = int(fields[0])
            for horizon, index in zip(HORIZONS, (3, 5), strict=True):
                rates[tier, year, horizon] = float(fields[index].removesuffix("%"))
    expected = {(tier, year, horizon) for tier, start in ((1, 2009), (2, 2012))
                for year in range(start, 2018) for horizon in HORIZONS}
    if rates.keys() != expected:
        raise ValueError("Expected all 30 March 2023 rates for Tier 1 and Tier 2.")
    return rates


def attach(connection, alias, path):
    quoted = str(path.resolve()).replace("'", "''")
    connection.execute(f"ATTACH '{quoted}' AS {alias} (READ_ONLY)")


def reconstruct(connection):
    if connection.execute("""
        SELECT count(*) FROM (
            SELECT modification FROM latest_archive.latest
            WHERE kind = 'Modification Information' AND program IN (?, ?)
            GROUP BY modification HAVING modification IS NULL OR count(*) <> 1
        )
    """, PROGRAMS).fetchone()[0]:
        raise ValueError("The latest modification snapshot has ambiguous identifiers.")
    cursor = connection.execute("""
        WITH activity AS (
            SELECT loan, modification, activity_date, age, reporting, installment_due_date
            FROM historical_archive.historical WHERE kind = 'Payment Information'
            UNION ALL
            SELECT loan, modification, activity_date, age, reporting, installment_due_date
            FROM monthly_archive.monthly_update WHERE kind = 'Payment Information'
        ), available_months AS (
            SELECT activity_date FROM historical_archive.historical_coverage WHERE kind = 'Payment Information'
            UNION
            SELECT activity_date FROM monthly_archive.monthly_update_coverage WHERE kind = 'Payment Information'
        ), target_payments AS (
            SELECT loan, modification, activity_date, age,
                   count(*) AS rows, count(DISTINCT (reporting, installment_due_date)) AS variants,
                   min(reporting) AS reporting, min(installment_due_date) AS installment_due_date
            FROM activity WHERE age IN (6, 12)
            GROUP BY loan, modification, activity_date, age
        ), targets AS (
            SELECT mod.loan, mod.modification, year(mod.effective_date) AS year,
                   CASE mod.program WHEN 'Tier 1 HAMP' THEN 1 ELSE 2 END AS tier,
                   h.horizon, mod.state, mod.end_date,
                   CAST(mod.effective_date + (h.horizon - 1) * INTERVAL '1 month' AS DATE) AS target_month
            FROM latest_archive.latest mod CROSS JOIN (VALUES (6), (12)) h(horizon)
            WHERE mod.kind = 'Modification Information' AND mod.program IN (?, ?)
        ), classified AS (
            SELECT t.tier, t.year, t.horizon,
                   m.activity_date IS NOT NULL AS calendar_month_available,
                   p.rows IS NOT NULL AS payment_row_present,
                   coalesce(p.rows - 1, 0) AS surplus_payment_rows,
                   coalesce(p.variants > 1, false) AS conflicting_payment,
                   CASE
                     WHEN m.activity_date IS NULL THEN 'outside_archive_coverage'
                     WHEN t.end_date < t.target_month + INTERVAL '1 month'
                       AND t.state IN ('Paid Off', 'Withdrawn') THEN 'paid_off_or_withdrawn'
                     WHEN t.end_date < t.target_month + INTERVAL '1 month'
                       AND t.state = 'Disqualified' THEN 'carry_forward_disqualification'
                     WHEN p.variants > 1 THEN 'conflicting_payment'
                     WHEN p.reporting IS DISTINCT FROM 'Reported' OR p.installment_due_date IS NULL
                        THEN 'no_reported_installment_date'
                     WHEN date_diff('month', p.installment_due_date, t.target_month) >= 3
                        THEN 'delinquent_reported'
                     ELSE 'other_reported'
                   END AS disposition
            FROM targets t
            LEFT JOIN available_months m ON m.activity_date = t.target_month
            LEFT JOIN target_payments p ON p.loan = t.loan AND p.modification = t.modification
                AND p.activity_date = t.target_month AND p.age = t.horizon
        )
        SELECT tier, year, horizon, count(*) AS cohort_size,
               count(*) FILTER (WHERE NOT calendar_month_available) AS outside_archive_coverage,
               count(*) FILTER (WHERE disposition = 'paid_off_or_withdrawn') AS paid_off_or_withdrawn,
               count(*) FILTER (WHERE payment_row_present) AS exact_month_payment_rows,
               sum(surplus_payment_rows)::BIGINT AS surplus_payment_rows,
               count(*) FILTER (WHERE conflicting_payment) AS payment_keys_with_conflicts,
               count(*) FILTER (WHERE disposition = 'conflicting_payment') AS excluded_conflicts,
               count(*) FILTER (WHERE disposition = 'no_reported_installment_date') AS missing_activity,
               count(*) FILTER (WHERE disposition = 'no_reported_installment_date'
                   AND NOT payment_row_present) AS no_payment_row,
               count(*) FILTER (WHERE disposition = 'carry_forward_disqualification') AS disqualified,
               count(*) FILTER (WHERE disposition = 'delinquent_reported') AS delinquent_reported,
               count(*) FILTER (WHERE disposition = 'other_reported') AS other_reported
        FROM classified GROUP BY tier, year, horizon ORDER BY tier, year, horizon
    """, PROGRAMS)
    names = [column[0] for column in cursor.description]
    return [dict(zip(names, row, strict=True)) for row in cursor.fetchall()]


def compare(rows, expected):
    if {(row["tier"], row["year"], row["horizon"]) for row in rows} != expected.keys():
        raise ValueError("Reconstructed cohorts do not match the Treasury table.")
    for row in rows:
        denominator = row["disqualified"] + row["delinquent_reported"] + row["other_reported"]
        numerator = row["disqualified"] + row["delinquent_reported"]
        unclassified = row["outside_archive_coverage"] + row["excluded_conflicts"] + row["missing_activity"]
        if denominator + row["paid_off_or_withdrawn"] + unclassified != row["cohort_size"]:
            raise ValueError(f"Unexpected cohort totals: {row}")
        tier, year, horizon = (row[key] for key in ("tier", "year", "horizon"))
        official = expected[tier, year, horizon]
        rate = 100 * numerator / denominator if denominator and not row["outside_archive_coverage"] else None
        row.update(
            numerator=numerator, denominator=denominator,
            treasury_rate_percent=official, estimate_percent=None if rate is None else round(rate, 4),
            difference_pp=None if rate is None else round(rate - official, 4),
        )
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("historical-db", "monthly-db", "latest-db", "reference-text"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    args = parser.parse_args()
    expected = reference_rates(args.reference_text)
    with duckdb.connect() as connection:
        connection.execute("SET memory_limit = '2GB'; SET threads = 3")
        attach(connection, "historical_archive", args.historical_db)
        attach(connection, "monthly_archive", args.monthly_db)
        attach(connection, "latest_archive", args.latest_db)
        rows = compare(reconstruct(connection), expected)
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
