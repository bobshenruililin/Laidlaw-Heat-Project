"""Compare two archived HKO Headquarters products and their monthly aggregates."""

import calendar
import csv
import hashlib
import io
import json
import math
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

from .weather_design import CLIMATE, EXPOSURES, _source_rows


SERIES = {
    "mean_temp": ("CLMTEMP", "Mean", 3),
    "mean_tmax": ("CLMMAXT", "Maximum", 2),
    "mean_tmin": ("CLMMINT", "Minimum", 4),
}
STATION_FILES = {key: f"data_raw/hko/{tag}_HKO.csv" for key, (tag, _, _) in SERIES.items()}
EXTRACT_FILES = {year: f"data_raw/hko/daily_extract/dailyExtract_{year}.xml" for year in range(2013, 2024)}
SOURCE_SHA256 = {
    STATION_FILES["mean_temp"]: "7146b3b156c874a9330796683188ee97687cb0c500082cf8ef1d37518ae96aba",
    STATION_FILES["mean_tmax"]: "5a0a646b4d125e40c25871abbccd5cd24e4f552063a547803ebac820166be4c9",
    STATION_FILES["mean_tmin"]: "e1db1ce51271f9a635ecb1ad593fbe3f368d1ed647232bf397d0d6b3bde8826b",
    EXTRACT_FILES[2013]: "52729d026c9ec9454e6d7934d786b738a1e85a6bafc0971fe89001c30967a95a",
    EXTRACT_FILES[2014]: "a9e662061008ae04eff02114bf7ae96d5bc765958f7620eb1023a49f36ff6bf0",
    EXTRACT_FILES[2015]: "bc2f1199c43dce592c0a8a0e3f6e87a3a5e923086afc19232f860f0f2bb14a39",
    EXTRACT_FILES[2016]: "6d912b8e6430caef98773cbedd960ddead9e73abc792f330c3124e4b0c0fbec4",
    EXTRACT_FILES[2017]: "cf98111157c47bda53cdced2759bc3974b0e2ec2a75e589e0d3fd739236f1624",
    EXTRACT_FILES[2018]: "7577e08a49677abd119039adf42ac8ac84436f803272ad3e586f879b1c03f50f",
    EXTRACT_FILES[2019]: "446cb40fc832c097a5a59f7c283dd5bc3522298ef15fd43584d3844523a08e49",
    EXTRACT_FILES[2020]: "6ac8fb4b43e4b40887d37e119ea9a6417b9c4634407c6ac6548edfa472f74546",
    EXTRACT_FILES[2021]: "9aa6d8e1a375a75351176fbcea05c95c01bbd2e3c305e77faf479f2d58bb1290",
    EXTRACT_FILES[2022]: "e3bfdb6ad83c6bda637314212218ceb0c8c5694e40341994119da74d5066dffc",
    EXTRACT_FILES[2023]: "0aec65724f4f6da2c241fa6e5096e50abd271c52bef26c775cb6c7f224f4372d",
}


def _text(root: Path, relative: str) -> str:
    data = (root / relative).read_bytes()
    if hashlib.sha256(data).hexdigest() != SOURCE_SHA256[relative]:
        raise ValueError(f"Unrecognised HKO source revision: {relative}")
    return data.decode("utf-8-sig")


def _tenths(value: str) -> int:
    # Both products publish temperatures to 0.1°C. Use integer arithmetic
    # for daily comparisons, threshold tests and monthly numerators.
    scaled = Decimal(value.strip()) * 10
    if not scaled.is_finite() or scaled != scaled.to_integral_value():
        raise ValueError(f"Temperature outside the archived 0.1°C precision: {value}")
    return int(scaled)


def _station_series(contents: str, title: str) -> dict[date, int]:
    rows = csv.reader(io.StringIO(contents))
    next(rows)
    if next(rows) != [f"Daily {title} Temperature (°C) at the Hong Kong Observatory"]:
        raise ValueError(f"Unexpected HKO station series: {title}")
    if next(rows)[-1] != "數據完整性/data Completeness":
        raise ValueError("Missing station CSV completeness field")
    result = {}
    for row in rows:
        if len(row) == 1:  # footnotes after the observations
            continue
        year = int(row[0])
        if not 2013 <= year <= 2023:
            continue
        observed = date(year, int(row[1]), int(row[2]))
        if observed in result or row[4] != "C":
            raise ValueError(f"Duplicate or incomplete {title} observation on {observed}")
        result[observed] = _tenths(row[3])
    return result


def _extract_series(root: Path) -> dict:
    result = {key: {} for key in SERIES}
    for year, relative in EXTRACT_FILES.items():
        # HKO's .xml endpoints in this archive contain JSON.
        for entry in json.loads(_text(root, relative))["stn"]["data"]:
            for row in entry["dayData"]:
                label = str(row[0]).strip()
                if label == "Mean/Total" or label.startswith("Normal"):
                    continue
                observed = date(year, int(entry["month"]), int(label))
                if observed in result["mean_temp"]:
                    raise ValueError(f"Duplicate dailyExtract observation on {observed}")
                for name, (_, _, column) in SERIES.items():
                    result[name][observed] = _tenths(row[column])
    return result


def _monthly(series: dict, dates: list[date]) -> dict:
    by_variable = {key: [series[key][day] for day in dates] for key in SERIES}
    values = {key: sum(days) / (10 * len(days)) for key, days in by_variable.items()}
    values["hot_nights"] = sum(t >= 280 for t in by_variable["mean_tmin"])
    values["cold_days"] = sum(t <= 120 for t in by_variable["mean_tmin"])
    values["very_hot_days"] = sum(t >= 330 for t in by_variable["mean_tmax"])
    return values


def compare_daily_sources(repo_root: Path) -> dict:
    """Reconstruct each monthly exposure twice, retaining every disagreement."""
    station = {
        name: _station_series(_text(repo_root, STATION_FILES[name]), title)
        for name, (_, title, _) in SERIES.items()
    }
    extract = _extract_series(repo_root)
    start = date(2013, 1, 1)
    dates = [start + timedelta(days=i) for i in range((date(2024, 1, 1) - start).days)]
    expected = set(dates)
    if any(set(product[name]) != expected for product in (station, extract) for name in SERIES):
        raise ValueError("Daily station products must each contain every study date")
    daily = [
        {"date": day.isoformat(), "exposure": name, "daily_extract_c": extract[name][day] / 10,
         "station_csv_c": station[name][day] / 10}
        for day in dates for name in SERIES if extract[name][day] != station[name][day]
    ]
    monthly = []
    reference = _source_rows(repo_root, CLIMATE)
    matched = {key: 0 for key in EXPOSURES}
    for row in reference:
        year, month = int(row["year"]), int(row["month"])
        days = [date(year, month, day) for day in range(1, calendar.monthrange(year, month)[1] + 1)]
        from_extract, from_station = _monthly(extract, days), _monthly(station, days)
        for name in EXPOSURES:
            # The published monthly CSV serialises non-rounded arithmetic
            # means. Allow only decimal serialization error at this step.
            if not math.isclose(from_extract[name], float(row[name]), rel_tol=0, abs_tol=1e-10):
                raise ValueError(f"Monthly paper source disagrees with dailyExtract at {row['month_id']}, {name}")
            if from_extract[name] == from_station[name]:
                matched[name] += 1
            else:
                monthly.append({"month": row["month_id"], "exposure": name,
                                "daily_extract": round(from_extract[name], 10),
                                "station_csv": round(from_station[name], 10),
                                "station_minus_extract": round(from_station[name] - from_extract[name], 10)})
    return {"n_dates": len(dates), "n_months": len(reference),
            "monthly_matches_by_exposure": matched,
            "daily_differences": daily, "monthly_differences": monthly}
