#!/usr/bin/env python3
"""Add Guo et al. 2016 (EHP, PMID 27258598) temperature variability to the monthly HKO panel.

Guo TV is the sample standard deviation of daily Tmin and Tmax over the exposure
window, e.g. TV0-1 = sd(Tmin_d, Tmax_d, Tmin_{d-1}, Tmax_{d-1}). It is a
continuous daily index, not a binary 'TV date'.

This script does not fit health models, does not edit Stage 3 PDFs, and does not
overwrite Hogan's live weather paragraph. Existing temperature-panel columns are
copied through unchanged.
"""
from __future__ import annotations

import csv
import json
import math
import statistics
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRACT_DIR = ROOT / "data_raw" / "hko" / "daily_extract"
PANEL_PATHS = [
    ROOT / "outputs" / "share_for_roro" / "temperature_monthly_panel_2013_2023.csv",
    ROOT / "analysis_plan" / "send_pack_2026-08-12" / "attach_for_roro" / "temperature_monthly_panel_2013_2023.csv",
]
STUDY_START = date(2013, 1, 1)
STUDY_END = date(2023, 12, 31)
NEW_COLS = [
    "tv_guo2016_0_1_mean",
    "tv_guo2016_0_7_mean",
    "tv_guo2016_0_1_days",
    "high_tv_guo2016_0_1_days",
    "dtr_mean",
]


def parse_hko_number(x) -> float | None:
    s = str(x).strip()
    if s in {"", "***", "----", "--", "NA", "N/A"}:
        return None
    if s.lower() == "trace":
        return 0.0
    try:
        return float(s)
    except ValueError:
        return None


def parse_year_extract(path: Path, year: int) -> list[dict]:
    raw = json.loads(path.read_text())
    rows = []
    for mobj in raw["stn"]["data"]:
        mo = int(mobj["month"])
        for day_vec in mobj["dayData"]:
            day_label = str(day_vec[0]).strip()
            if not day_label.isdigit():
                continue
            day = int(day_label)
            rows.append(
                {
                    "date": date(year, mo, day),
                    "tmax": parse_hko_number(day_vec[2]),
                    "tmean": parse_hko_number(day_vec[3]),
                    "tmin": parse_hko_number(day_vec[4]),
                }
            )
    return rows


def guo_tv(daily: dict[date, dict], on: date, lag_end: int) -> float | None:
    vals = []
    for lag in range(0, lag_end + 1):
        d = on - timedelta(days=lag)
        row = daily.get(d)
        if row is None or row["tmin"] is None or row["tmax"] is None:
            return None
        vals.extend([row["tmin"], row["tmax"]])
    if len(vals) < 2:
        return None
    return statistics.stdev(vals)


def fmt(x: float | None, nd: int = 6) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return ""
    return f"{x:.{nd}f}".rstrip("0").rstrip(".") if nd else str(int(x))


def main() -> None:
    years = range(2012, 2024)
    rows = []
    for y in years:
        path = EXTRACT_DIR / f"dailyExtract_{y}.xml"
        if not path.exists():
            raise SystemExit(f"Missing {path}")
        rows.extend(parse_year_extract(path, y))
    daily = {r["date"]: r for r in rows}

    # Hand check: 2013-01-02 uses 1–2 Jan 2013 Tmin/Tmax.
    d0 = date(2013, 1, 2)
    expected = statistics.stdev(
        [
            daily[d0]["tmin"],
            daily[d0]["tmax"],
            daily[date(2013, 1, 1)]["tmin"],
            daily[date(2013, 1, 1)]["tmax"],
        ]
    )
    got = guo_tv(daily, d0, 1)
    if got is None or abs(got - expected) > 1e-12:
        raise SystemExit(f"TV0-1 hand check failed: {got} vs {expected}")

    study_days = []
    d = STUDY_START
    while d <= STUDY_END:
        row = daily[d]
        tv01 = guo_tv(daily, d, 1)
        tv07 = guo_tv(daily, d, 7)
        dtr = None
        if row["tmax"] is not None and row["tmin"] is not None:
            dtr = row["tmax"] - row["tmin"]
        study_days.append(
            {
                "date": d.isoformat(),
                "month_id": d.strftime("%Y-%m"),
                "tmin": row["tmin"],
                "tmax": row["tmax"],
                "tv_guo2016_0_1": tv01,
                "tv_guo2016_0_7": tv07,
                "dtr": dtr,
            }
        )
        d += timedelta(days=1)

    tv01_vals = [x["tv_guo2016_0_1"] for x in study_days if x["tv_guo2016_0_1"] is not None]
    if not tv01_vals:
        raise SystemExit("No defined TV0-1 days")
    p90 = sorted(tv01_vals)[int(round(0.9 * (len(tv01_vals) - 1)))]

    monthly: dict[str, dict] = {}
    for rec in study_days:
        m = rec["month_id"]
        bucket = monthly.setdefault(
            m,
            {
                "tv01": [],
                "tv07": [],
                "dtr": [],
                "high01": 0,
                "n_days": 0,
            },
        )
        bucket["n_days"] += 1
        if rec["tv_guo2016_0_1"] is not None:
            bucket["tv01"].append(rec["tv_guo2016_0_1"])
            if rec["tv_guo2016_0_1"] >= p90:
                bucket["high01"] += 1
        if rec["tv_guo2016_0_7"] is not None:
            bucket["tv07"].append(rec["tv_guo2016_0_7"])
        if rec["dtr"] is not None:
            bucket["dtr"].append(rec["dtr"])

    month_out = {}
    for m, b in monthly.items():
        if not b["tv01"] or not b["tv07"]:
            raise SystemExit(f"Missing Guo TV in {m}")
        month_out[m] = {
            "tv_guo2016_0_1_mean": statistics.mean(b["tv01"]),
            "tv_guo2016_0_7_mean": statistics.mean(b["tv07"]),
            "tv_guo2016_0_1_days": len(b["tv01"]),
            "high_tv_guo2016_0_1_days": b["high01"],
            "dtr_mean": statistics.mean(b["dtr"]),
        }

    if len(month_out) != 132:
        raise SystemExit(f"Expected 132 months, got {len(month_out)}")
    jan = month_out["2013-01"]
    if jan["tv_guo2016_0_1_days"] != 31:
        raise SystemExit("January 2013 TV0-1 should be defined on all 31 days via Dec 2012")
    if any(v["high_tv_guo2016_0_1_days"] > v["tv_guo2016_0_1_days"] for v in month_out.values()):
        raise SystemExit("high-TV day count exceeds defined TV days")

    src = PANEL_PATHS[0]
    with src.open(newline="") as f:
        reader = csv.DictReader(f)
        old_fields = list(reader.fieldnames or [])
        old_rows = list(reader)
    if len(old_rows) != 132:
        raise SystemExit(f"{src} has {len(old_rows)} rows")
    for col in NEW_COLS:
        if col in old_fields:
            old_fields = [c for c in old_fields if c not in NEW_COLS]
            break

    new_fields = old_fields + NEW_COLS
    written_rows = []
    for row in old_rows:
        mid = row["month_id"]
        extra = month_out[mid]
        out = {k: row[k] for k in old_fields}
        out["tv_guo2016_0_1_mean"] = fmt(extra["tv_guo2016_0_1_mean"])
        out["tv_guo2016_0_7_mean"] = fmt(extra["tv_guo2016_0_7_mean"])
        out["tv_guo2016_0_1_days"] = str(extra["tv_guo2016_0_1_days"])
        out["high_tv_guo2016_0_1_days"] = str(extra["high_tv_guo2016_0_1_days"])
        out["dtr_mean"] = fmt(extra["dtr_mean"])
        written_rows.append(out)
        for k in old_fields:
            if out[k] != row[k]:
                raise SystemExit(f"Old column {k} changed in {mid}")

    # Preserve the 12 August pack as sent; write the living share + a dated TV pack.
    dests = [
        ROOT / "outputs" / "share_for_roro" / "temperature_monthly_panel_2013_2023.csv",
        ROOT / "analysis_plan" / "send_pack_2026-08-21_tv" / "temperature_monthly_panel_2013_2023.csv",
    ]
    sidecar = ROOT / "outputs" / "tables" / "tv_guo2016_monthly_2013_2023.csv"
    daily_out = ROOT / "outputs" / "tables" / "tv_guo2016_daily_2013_2023.csv"

    for dest in dests:
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=new_fields, lineterminator="\n")
            w.writeheader()
            w.writerows(written_rows)

    sidecar.parent.mkdir(parents=True, exist_ok=True)
    with sidecar.open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["month_id"] + NEW_COLS + ["high_tv_threshold_tv0_1_p90"],
            lineterminator="\n",
        )
        w.writeheader()
        for mid in sorted(month_out):
            rec = {"month_id": mid, "high_tv_threshold_tv0_1_p90": fmt(p90)}
            rec.update({k: (str(month_out[mid][k]) if k.endswith("days") else fmt(month_out[mid][k])) for k in NEW_COLS})
            w.writerow(rec)

    with daily_out.open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["date", "month_id", "tmin", "tmax", "tv_guo2016_0_1", "tv_guo2016_0_7", "dtr"],
            lineterminator="\n",
        )
        w.writeheader()
        for rec in study_days:
            w.writerow(
                {
                    "date": rec["date"],
                    "month_id": rec["month_id"],
                    "tmin": fmt(rec["tmin"], 1),
                    "tmax": fmt(rec["tmax"], 1),
                    "tv_guo2016_0_1": fmt(rec["tv_guo2016_0_1"]),
                    "tv_guo2016_0_7": fmt(rec["tv_guo2016_0_7"]),
                    "dtr": fmt(rec["dtr"]),
                }
            )

    # Re-read share panel: old extremes unchanged, TV present, 132 rows.
    with dests[0].open(newline="") as f:
        check = list(csv.DictReader(f))
    assert len(check) == 132
    assert check[0]["hot_nights"] == old_rows[0]["hot_nights"]
    assert sum(int(r["cold_days"]) for r in check) == 145
    assert all(r["tv_guo2016_0_1_mean"] for r in check)
    assert got == expected

    summary = ROOT / "outputs" / "tables" / "tv_guo2016_summary.json"
    payload = {
        "built_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "Guo et al. 2016 Environ Health Perspect 124:1554-1559; doi:10.1289/EHP149; PMID 27258598",
        "operator": "sample SD of Tmin and Tmax over lags 0-k (Python statistics.stdev; same as R sd, n-1)",
        "n_months": 132,
        "n_days_tv01_defined": len(tv01_vals),
        "tv0_1_p90": p90,
        "tv0_1_mean_of_monthly_means": statistics.mean(v["tv_guo2016_0_1_mean"] for v in month_out.values()),
        "tv0_7_mean_of_monthly_means": statistics.mean(v["tv_guo2016_0_7_mean"] for v in month_out.values()),
        "high_tv_days_total": sum(v["high_tv_guo2016_0_1_days"] for v in month_out.values()),
        "hand_check_2013_01_02_tv0_1": expected,
        "not_done": [
            "no health model",
            "not Guo binary TV dates (paper has none)",
            "P15 mean diurnal range is a different proxy",
        ],
    }
    summary.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
    print("Wrote", dests[0])
    print("Wrote", dests[1])
    print("Wrote", sidecar)
    print("Wrote", daily_out)


if __name__ == "__main__":
    main()
