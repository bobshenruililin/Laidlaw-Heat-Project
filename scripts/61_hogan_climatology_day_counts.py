#!/usr/bin/env python3
"""Monthly counts of days warmer/cooler than the historical same-calendar-day mean.

Hogan (24 Aug 2026): do not threshold a temperature-variability index.
Climatology is the leave-one-year-out mean of that month-day in the 2012–2023
HKO Headquarters dailyExtract series. No health outcomes are joined.
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRACT_DIR = ROOT / "data_raw" / "hko" / "daily_extract"


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


def parse_year(path: Path, year: int) -> list[dict]:
    raw = json.loads(path.read_text())
    rows = []
    for mobj in raw["stn"]["data"]:
        month = int(mobj["month"])
        for day_vec in mobj["dayData"]:
            label = str(day_vec[0]).strip()
            if not label.isdigit():
                continue
            day = int(label)
            rows.append(
                {
                    "date": date(year, month, day),
                    "year": year,
                    "month": month,
                    "day": day,
                    "md": f"{month:02d}-{day:02d}",
                    "tmax": parse_hko_number(day_vec[2]),
                    "tmean": parse_hko_number(day_vec[3]),
                    "tmin": parse_hko_number(day_vec[4]),
                    "relative_humidity": parse_hko_number(day_vec[6]),
                    "rainfall": parse_hko_number(day_vec[8]),
                }
            )
    return rows


def main() -> None:
    daily: list[dict] = []
    for year in range(2012, 2024):
        path = EXTRACT_DIR / f"dailyExtract_{year}.xml"
        if not path.exists():
            raise SystemExit(f"Missing {path}")
        daily.extend(parse_year(path, year))

    by_md_year: dict[str, dict[int, dict]] = defaultdict(dict)
    for row in daily:
        by_md_year[row["md"]][row["year"]] = row

    for row in daily:
        others = [
            other
            for y, other in by_md_year[row["md"]].items()
            if y != row["year"]
        ]
        tmeans = [o["tmean"] for o in others if o["tmean"] is not None]
        tmaxs = [o["tmax"] for o in others if o["tmax"] is not None]
        tmins = [o["tmin"] for o in others if o["tmin"] is not None]
        row["clim_tmean"] = sum(tmeans) / len(tmeans) if tmeans else None
        row["clim_tmax"] = sum(tmaxs) / len(tmaxs) if tmaxs else None
        row["clim_tmin"] = sum(tmins) / len(tmins) if tmins else None
        row["n_clim_years"] = len(others)
        row["warmer_tmean"] = int(
            row["tmean"] is not None
            and row["clim_tmean"] is not None
            and row["tmean"] > row["clim_tmean"]
        )
        row["cooler_tmean"] = int(
            row["tmean"] is not None
            and row["clim_tmean"] is not None
            and row["tmean"] < row["clim_tmean"]
        )
        row["warmer_tmax"] = int(
            row["tmax"] is not None
            and row["clim_tmax"] is not None
            and row["tmax"] > row["clim_tmax"]
        )
        row["cooler_tmin"] = int(
            row["tmin"] is not None
            and row["clim_tmin"] is not None
            and row["tmin"] < row["clim_tmin"]
        )

    study = [r for r in daily if 2013 <= r["year"] <= 2023]
    monthly: dict[tuple[int, int], dict] = {}
    for row in study:
        key = (row["year"], row["month"])
        slot = monthly.setdefault(
            key,
            {
                "month_id": f"{row['year']:04d}-{row['month']:02d}",
                "year": row["year"],
                "month": row["month"],
                "n_days": 0,
                "days_warmer_than_climatology": 0,
                "days_cooler_than_climatology": 0,
                "days_tmax_above_climatology": 0,
                "days_tmin_below_climatology": 0,
                "rh_sum": 0.0,
                "rh_n": 0,
                "total_rainfall_mm": 0.0,
                "n_clim_years_min": row["n_clim_years"],
            },
        )
        slot["n_days"] += 1
        slot["days_warmer_than_climatology"] += row["warmer_tmean"]
        slot["days_cooler_than_climatology"] += row["cooler_tmean"]
        slot["days_tmax_above_climatology"] += row["warmer_tmax"]
        slot["days_tmin_below_climatology"] += row["cooler_tmin"]
        if row["relative_humidity"] is not None:
            slot["rh_sum"] += row["relative_humidity"]
            slot["rh_n"] += 1
        if row["rainfall"] is not None:
            slot["total_rainfall_mm"] += row["rainfall"]
        slot["n_clim_years_min"] = min(slot["n_clim_years_min"], row["n_clim_years"])

    rows_out = []
    for key in sorted(monthly):
        slot = monthly[key]
        if slot["days_warmer_than_climatology"] + slot["days_cooler_than_climatology"] > slot["n_days"]:
            raise SystemExit(f"count overflow {slot}")
        rows_out.append(
            {
                "month_id": slot["month_id"],
                "year": slot["year"],
                "month": slot["month"],
                "n_days": slot["n_days"],
                "days_warmer_than_climatology": slot["days_warmer_than_climatology"],
                "days_cooler_than_climatology": slot["days_cooler_than_climatology"],
                "days_tmax_above_climatology": slot["days_tmax_above_climatology"],
                "days_tmin_below_climatology": slot["days_tmin_below_climatology"],
                "mean_relative_humidity": round(slot["rh_sum"] / slot["rh_n"], 6) if slot["rh_n"] else "",
                "total_rainfall_mm": round(slot["total_rainfall_mm"], 3),
                "n_clim_years_min": slot["n_clim_years_min"],
                "climatology_rule": "leave_one_year_out_same_calendar_day_2012_2023",
                "data_status": "REAL_PUBLIC_HKO",
            }
        )

    if len(rows_out) != 132:
        raise SystemExit(f"expected 132 months, got {len(rows_out)}")

    out_csv = ROOT / "data_processed" / "hogan_climatology_day_counts_2013_2023.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
        w.writeheader()
        w.writerows(rows_out)

    by_m = defaultdict(list)
    for r in rows_out:
        by_m[int(r["month"])].append(r)
    summary_path = ROOT / "outputs" / "tables" / "hogan_climatology_day_counts_by_calendar_month.csv"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with summary_path.open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "month",
                "mean_warmer",
                "mean_cooler",
                "mean_rainfall_mm",
                "mean_rh",
            ],
        )
        w.writeheader()
        for m in range(1, 13):
            grp = by_m[m]
            w.writerow(
                {
                    "month": m,
                    "mean_warmer": round(sum(r["days_warmer_than_climatology"] for r in grp) / len(grp), 3),
                    "mean_cooler": round(sum(r["days_cooler_than_climatology"] for r in grp) / len(grp), 3),
                    "mean_rainfall_mm": round(sum(r["total_rainfall_mm"] for r in grp) / len(grp), 3),
                    "mean_rh": round(sum(float(r["mean_relative_humidity"]) for r in grp) / len(grp), 3),
                }
            )

    mean_w = sum(r["days_warmer_than_climatology"] for r in rows_out) / 132
    mean_c = sum(r["days_cooler_than_climatology"] for r in rows_out) / 132
    print(f"Wrote {out_csv} ({len(rows_out)} months)")
    print(f"Mean warmer days/month={mean_w:.1f}; cooler={mean_c:.1f}")
    print(f"Wrote {summary_path}")


if __name__ == "__main__":
    main()
