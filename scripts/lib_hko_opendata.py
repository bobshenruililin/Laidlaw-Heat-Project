"""Parse Hong Kong Observatory open-data CLM* CSVs (public)."""
from __future__ import annotations

import csv
from datetime import date, timedelta
from pathlib import Path


def parse_hko_opendata(path: Path, year_min: int = 2013, year_max: int = 2023) -> dict[str, dict]:
    """Return {YYYY-MM-DD: {value, completeness}} from an HKO CLMTEMP/MAXT/MINT CSV."""
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    idx = None
    for i, line in enumerate(lines):
        if line.startswith("年/Year") or (line.startswith("年") and "Year" in line):
            idx = i
            break
    if idx is None:
        raise RuntimeError(f"No Year/Month/Day header in {path}")
    out: dict[str, dict] = {}
    for row in csv.reader(lines[idx + 1 :]):
        if len(row) < 5:
            continue
        try:
            y, m, d = int(row[0]), int(row[1]), int(row[2])
        except ValueError:
            continue
        if y < year_min or y > year_max:
            continue
        key = f"{y:04d}-{m:02d}-{d:02d}"
        raw = row[3].strip()
        try:
            val = float(raw)
        except ValueError:
            val = None
        out[key] = {"value": val, "completeness": row[4].strip()}
    return out


def expected_dates(year_min: int = 2013, year_max: int = 2023) -> list[str]:
    start = date(year_min, 1, 1)
    end = date(year_max, 12, 31)
    out = []
    cur = start
    while cur <= end:
        out.append(cur.isoformat())
        cur += timedelta(days=1)
    return out
