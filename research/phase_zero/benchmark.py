import csv
import hashlib
import json
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent
SOURCE = "https://home.treasury.gov/system/files/256/129_HAMP_Modification_Performance_Summary_Mar2023_v1.0.pdf"

def predict(data, tier, year):
    history = [v for (t, y), v in data.items() if t == 1 and y <= year - 2]
    return {
        "historical_tier1": mean(b for a, b in history),
        "local_lag2": data[tier, year - 2][1],
        "month6_method": data[tier, year][0] + mean(b-a for a, b in history),
    }

def main():
    path = ROOT / "data" / "cohorts.csv"
    data = {}
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            key = (int(row["tier"]), int(row["year"]))
            a = float(row["month_6_90plus_pct"])
            b = float(row["month_12_90plus_pct"])
            if key in data or not (0 <= a <= 100 and 0 <= b <= 100):
                raise ValueError(f"Invalid cohort: {key}")
            data[key] = (a, b)
    assert len(data) == 15 and data[1, 2014] == (4.7, 10.6)
    assert data[2, 2017] == (7.0, 16.7)
    changed = dict(data)
    changed[1, 2015] = (5.3, 99.0)
    changed[1, 2014] = (1.0, 88.0)
    assert predict(data, 1, 2015) == predict(changed, 1, 2015)
    results = {}
    summaries = []
    for tier in (1, 2):
        errors = {}
        details = []
        for year in range(2014, 2018):
            actual = data[tier, year][1]
            estimates = predict(data, tier, year)
            for method, estimate in estimates.items():
                errors.setdefault(method, []).append(estimate - actual)
            details.append(dict(year=year, actual=actual, estimates=estimates))
        mae = {k: round(mean(abs(v) for v in values), 5) for k, values in errors.items()}
        results[str(tier)] = dict(cohorts=details, mae_pp=mae)
        summaries.append(f"<tr><td>{tier}</td><td>{mae['historical_tier1']:.2f}</td>"
                         f"<td>{mae['local_lag2']:.2f}</td><td>{mae['month6_method']:.2f}</td></tr>")
        print(f"Tier {tier}: {mae}")
    assert results["1"]["mae_pp"]["month6_method"] == 0.92554
    assert results["2"]["mae_pp"]["month6_method"] == 2.15304
    assert results["2"]["mae_pp"]["local_lag2"] == 0.9
    results["source"] = SOURCE
    results["csv_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    page = """<!doctype html><html lang="en"><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>U.S. mortgage repayment review</title><style>
    body{max-width:50rem;margin:3rem auto;padding:0 1rem;font:17px/1.55 system-ui;color:#243841}
    h1{font-family:Georgia,serif}td,th{padding:.55rem;border-bottom:1px solid #bbb}table{border-collapse:collapse}
    </style><main><h1>What six months of repayment history can tell us</h1>
    <p>Mean absolute error in percentage points for four annual U.S. HAMP cohorts, 2014–2017. Lower values are better.</p>
    <table><thead><tr><th>Tier</th><th>Historical Tier 1 mean</th><th>Same-tier lag</th><th>Month-six method</th></tr></thead><tbody>"""
    page += "".join(summaries) + "</tbody></table>"
    page += '<p>The early estimate improved on both baselines in Tier 1 and underestimated all four Tier 2 cohorts. These are retrospective aggregate data, not individual default predictions or a bank pilot.</p>'
    page += f'<a href="{SOURCE}">Original U.S. Treasury tables</a></main></html>'
    for folder in ("results", "docs"):
        (ROOT / folder).mkdir(exist_ok=True)
    (ROOT / "results" / "benchmark.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    (ROOT / "docs" / "index.html").write_text(page, encoding="utf-8")

if __name__ == "__main__":
    main()
