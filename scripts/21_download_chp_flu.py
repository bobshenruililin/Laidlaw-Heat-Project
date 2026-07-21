#!/usr/bin/env python3
"""Download CHP Flu Express weekly CSV and aggregate to monthly flu indicators.

Source: https://www.chp.gov.hk/files/misc/flux_data.csv
Dictionary: https://www.chp.gov.hk/files/pdf/flux_spec_en.pdf

Writes:
  data_raw/chp_flu/flux_data.csv
  data_raw/chp_flu/flu_monthly_2013_2023.csv  (month_id, flu_indicator, ...)
"""

from __future__ import annotations

import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data_raw" / "chp_flu"
URL = "https://www.chp.gov.hk/files/misc/flux_data.csv"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    req = Request(URL, headers={"User-Agent": "LaidlawHeatProject/1.0"})
    raw = urlopen(req, timeout=120).read()
    raw_path = OUT / "flux_data.csv"
    raw_path.write_bytes(raw)

    text = raw.decode("utf-8-sig", errors="replace")
    rows = list(csv.DictReader(text.splitlines()))
    # Expected cols: Year, Week, From, To, AandB_proportion, ILI_FMC, ...
    by_month: dict[str, list[float]] = defaultdict(list)
    by_month_ili: dict[str, list[float]] = defaultdict(list)
    for r in rows:
        # Prefer From date for month assignment
        from_s = (r.get("From") or r.get("from") or "").strip()
        year = (r.get("Year") or r.get("year") or "").strip()
        week = (r.get("Week") or r.get("week") or "").strip()
        month_id = None
        if from_s:
            for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
                try:
                    d = datetime.strptime(from_s, fmt)
                    month_id = d.strftime("%Y-%m")
                    break
                except ValueError:
                    pass
        if month_id is None and year and week:
            # fallback: ISO week
            try:
                d = datetime.fromisocalendar(int(year), int(week), 1)
                month_id = d.strftime("%Y-%m")
            except Exception:
                continue

        prop = r.get("AandB_proportion") or r.get("aandb_proportion") or ""
        ili = r.get("ILI_FMC") or r.get("ili_fmc") or ""
        try:
            by_month[month_id].append(float(prop))
        except Exception:
            pass
        try:
            by_month_ili[month_id].append(float(ili))
        except Exception:
            pass

    out_rows = []
    for mid in sorted(by_month.keys()):
        y = int(mid[:4])
        if y < 2013 or y > 2023:
            continue
        vals = by_month[mid]
        ili_vals = by_month_ili.get(mid, [])
        out_rows.append(
            {
                "month_id": mid,
                "flu_indicator": sum(vals) / len(vals) if vals else "",
                "flu_ili_fmc_mean": sum(ili_vals) / len(ili_vals) if ili_vals else "",
                "n_weeks": len(vals),
                "flu_metric": "monthly_mean_AandB_proportion",
                "source": "CHP Flu Express flux_data.csv",
            }
        )

    monthly_path = OUT / "flu_monthly_2013_2023.csv"
    with monthly_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "month_id",
                "flu_indicator",
                "flu_ili_fmc_mean",
                "n_weeks",
                "flu_metric",
                "source",
            ],
        )
        w.writeheader()
        w.writerows(out_rows)

    # Also copy a merge-ready two-column file for 06_build_confounders.R
    merge_path = OUT / "flu_for_confounders.csv"
    with merge_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["month_id", "flu_indicator"])
        w.writeheader()
        for r in out_rows:
            if r["flu_indicator"] != "":
                w.writerow({"month_id": r["month_id"], "flu_indicator": r["flu_indicator"]})

    print(f"Wrote {raw_path} ({len(rows)} weekly rows)")
    print(f"Wrote {monthly_path} ({len(out_rows)} months)")
    print(f"Wrote {merge_path}")


if __name__ == "__main__":
    main()
