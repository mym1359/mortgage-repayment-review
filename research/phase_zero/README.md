# U.S. Mortgage Repayment Review

Run python benchmark.py (on Windows: py benchmark.py). Requires Python 3.8+, no third-party packages. Open docs/index.html for the public demo. See results/benchmark.json for each annual estimate and the input SHA-256. No raw loan records, contacts or automated decisions are involved.

Source: U.S. Treasury, HAMP Performance Summary, March 2023, Tier 1 and Tier 2 tables. The CSV transcribes month-6 and month-12 90+ delinquency percentages. Each annual cohort is weighted equally. The early estimate adds the Tier 1 historical change from months 6 to 12 to the target cohort's observed month-6 rate. Training cohorts have effective years at least two years older than the test year. Data come from a single revised vintage. Treasury carries disqualified modifications forward and excludes paid-off and withdrawn accounts from subsequent periods. Program-level results do not establish increased recovery or individual creditworthiness.

The retrospective benchmark and starter were developed with AI assistance. Add dated contributions and independent evaluations as the project progresses.