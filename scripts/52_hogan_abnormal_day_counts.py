#!/usr/bin/env python3
"""Hogan 24 Aug 2026 alternative to Jingjing TV-day counts.

Leave-one-year-out day-of-year climatology from HKO dailyExtract 2012–2023.
Monthly counts of days above/below that climatology for tmean, tmax, tmin.
Also writes monthly mean RH and total rainfall as a check against climate_monthly.
REAL weather only. No health coefficients.
"""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import date
from pathlib import Path
from statistics import mean

ROOT = Path("/workspace")
EXTRACT = ROOT / "data_raw/hko/daily_extract"
YEARS_CLIM = range(2012, 2024)
YEARS_STUDY = range(2013, 2024)


def parse_num(x):
    s = str(x).strip()
    if s in {"", "***", "----", "--", "NA", "N/A"}:
        return None
    if s.lower() == "trace":
        return 0.0
    try:
        return float(s)
    except ValueError:
        return None


def parse_year(path: Path, year: int) -> list[dict]:
    raw = json.loads(path.read_text())
    rows = []
    for mobj in raw["stn"]["data"]:
        mo = int(mobj["month"])
        for day_vec in mobj["dayData"]:
            label = str(day_vec[0]).strip()
            if not label.isdigit():
                continue
            day = int(label)
            rows.append(
                {
                    "date": date(year, mo, day),
                    "year": year,
                    "month": mo,
                    "day": day,
                    "month_day": f"{mo:02d}-{day:02d}",
                    # HKO dailyExtract order (0-based): day, pressure, tmax, tmean, tmin,
                    # dew point, RH%, cloud, rainfall mm, ...
                    "tmax": parse_num(day_vec[2]),
                    "tmean": parse_num(day_vec[3]),
                    "tmin": parse_num(day_vec[4]),
                    "rh": parse_num(day_vec[6]),
                    "rain": parse_num(day_vec[8]),
                }
            )
    return rows


def main() -> None:
    daily: list[dict] = []
    for y in YEARS_CLIM:
        path = EXTRACT / f"dailyExtract_{y}.xml"
        if not path.is_file():
            raise SystemExit(f"Missing {path}")
        daily.extend(parse_year(path, y))

    by_md_other: dict[tuple[int, str], dict[str, list[float]]] = defaultdict(
        lambda: {"tmean": [], "tmax": [], "tmin": []}
    )
    for row in daily:
        for y in YEARS_STUDY:
            if row["year"] == y:
                continue
            key = (y, row["month_day"])
            for k in ("tmean", "tmax", "tmin"):
                if row[k] is not None:
                    by_md_other[key][k].append(row[k])

    clim = {}
    for key, vals in by_md_other.items():
        clim[key] = {
            "tmean": mean(vals["tmean"]) if vals["tmean"] else None,
            "tmax": mean(vals["tmax"]) if vals["tmax"] else None,
            "tmin": mean(vals["tmin"]) if vals["tmin"] else None,
        }

    monthly: dict[str, dict] = {}
    for row in daily:
        if row["year"] not in YEARS_STUDY:
            continue
        mid = f"{row['year']:04d}-{row['month']:02d}"
        rec = monthly.setdefault(
            mid,
            {
                "month_id": mid,
                "year": row["year"],
                "month": row["month"],
                "n_days": 0,
                "n_days_tmean_above_doy": 0,
                "n_days_tmean_below_doy": 0,
                "n_days_tmax_above_doy": 0,
                "n_days_tmax_below_doy": 0,
                "n_days_tmin_above_doy": 0,
                "n_days_tmin_below_doy": 0,
                "rh": [],
                "rain": [],
            },
        )
        rec["n_days"] += 1
        c = clim.get((row["year"], row["month_day"]), {})
        for src, ckey, above, below in (
            ("tmean", "tmean", "n_days_tmean_above_doy", "n_days_tmean_below_doy"),
            ("tmax", "tmax", "n_days_tmax_above_doy", "n_days_tmax_below_doy"),
            ("tmin", "tmin", "n_days_tmin_above_doy", "n_days_tmin_below_doy"),
        ):
            obs, ref = row[src], c.get(ckey)
            if obs is None or ref is None:
                continue
            if obs > ref:
                rec[above] += 1
            elif obs < ref:
                rec[below] += 1
        if row["rh"] is not None:
            rec["rh"].append(row["rh"])
        if row["rain"] is not None:
            rec["rain"].append(row["rain"])

    rows_out = []
    for mid in sorted(monthly):
        rec = monthly[mid]
        rec["mean_relative_humidity"] = mean(rec["rh"]) if rec["rh"] else ""
        rec["total_rainfall_mm"] = sum(rec["rain"]) if rec["rain"] else ""
        del rec["rh"]
        del rec["rain"]
        rows_out.append(rec)

    if len(rows_out) != 132:
        raise SystemExit(f"expected 132 months, got {len(rows_out)}")

    cols = [
        "month_id",
        "year",
        "month",
        "n_days",
        "n_days_tmean_above_doy",
        "n_days_tmean_below_doy",
        "n_days_tmax_above_doy",
        "n_days_tmax_below_doy",
        "n_days_tmin_above_doy",
        "n_days_tmin_below_doy",
        "mean_relative_humidity",
        "total_rainfall_mm",
    ]
    text = ",".join(cols) + "\n"
    for rec in rows_out:
        text += ",".join(str(rec[c]) for c in cols) + "\n"

    processed = ROOT / "data_processed/hogan_abnormal_day_counts_2013_2023.csv"
    tables = ROOT / "outputs/tables/hogan_abnormal_day_counts_2013_2023.csv"
    tables.parent.mkdir(parents=True, exist_ok=True)
    processed.write_text(text)
    tables.write_text(text)

    jan = [r["n_days_tmean_below_doy"] for r in rows_out if r["month"] == 1]
    jul = [r["n_days_tmean_below_doy"] for r in rows_out if r["month"] == 7]
    meta = (
        "n_months,climatology,study_window,jan_mean_tmean_below,jul_mean_tmean_below,provenance\n"
        f"132,2012-2023 leave-one-year-out,2013-01 to 2023-12,"
        f"{sum(jan)/len(jan):.3f},{sum(jul)/len(jul):.3f},REAL_HKO_DAILY\n"
    )
    (ROOT / "outputs/tables/hogan_abnormal_day_counts_meta.csv").write_text(meta)
    print(f"wrote {processed} ({len(rows_out)} months)")
    print(f"Jan mean days tmean below DOY: {sum(jan)/len(jan):.1f}; Jul: {sum(jul)/len(jul):.1f}")


if __name__ == "__main__":
    main()
