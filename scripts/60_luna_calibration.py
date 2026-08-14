#!/usr/bin/env python3
"""Exposure-only HKO/ERA5 calibration cut for 2013--2023.

This script reads only the three named REAL processed CSV files.  It uses the
Python standard library so that the calculation does not depend on scipy,
sklearn, or network access.
"""
from __future__ import annotations

import csv
import json
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HKO_DAILY = ROOT / "data_processed" / "md_daily_weather_design_2013_2023.csv"
ERA5_DAILY = ROOT / "data_processed" / "peer_cities" / "cache" / "hong_kong_daily.csv"
HKO_MONTHLY = ROOT / "data_processed" / "climate_monthly_2013_2023.csv"
OUT_MD = ROOT / "knowledge" / "2026-08-14_luna_calibration_cut.md"
OUT_JSON = ROOT / "outputs" / "identification_lab" / "luna_calibration.json"

HOT_C = 28.0
MATCHED_DAYS = 4017


def read_daily(path: Path, field: str) -> dict[str, float]:
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    dates = [row["date"] for row in rows]
    if len(dates) != len(set(dates)):
        raise AssertionError(f"Duplicate dates in {path}")
    return {row["date"]: float(row[field]) for row in rows}


def read_monthly(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def as_tenths(value: float) -> int:
    scaled = round(value * 10)
    if abs(value - scaled / 10) > 1e-8:
        raise AssertionError(f"Expected one-decimal Tmin, got {value}")
    return scaled


def rate_payload(n: int, numerator: int) -> dict[str, object]:
    if n == 0:
        return {"n": 0, "n_event": 0, "rate": None, "rate_fraction": None}
    return {
        "n": n,
        "n_event": numerator,
        "rate": round(numerator / n, 12),
        "rate_fraction": f"{numerator}/{n}",
    }


def make_bins(
    dates: list[str],
    hko: dict[str, float],
    event: dict[str, bool],
    lower_tenths: int,
    upper_tenths: int,
    width_tenths: int,
    event_key: str,
) -> list[dict[str, object]]:
    bins = []
    for low in range(lower_tenths, upper_tenths, width_tenths):
        high = low + width_tenths
        selected = [
            d
            for d in dates
            if low <= as_tenths(hko[d]) < high
        ]
        numerator = sum(event[d] for d in selected)
        row = {
            "lower_c": low / 10,
            "upper_c": high / 10,
            "interval": f"[{low / 10:.1f}, {high / 10:.1f})",
            **rate_payload(len(selected), numerator),
        }
        row[event_key] = numerator
        bins.append(row)
    return bins


def fmt_rate(value: float | None) -> str:
    return "NA" if value is None else f"{value:.12f}"


def fmt_pct(value: float) -> str:
    return f"{value:.12f}%"


def markdown_rate_table(rows: list[dict[str, object]], event_label: str) -> str:
    lines = [
        "| HKO Tmin interval (°C) | n | "
        f"{event_label} | rate | fraction |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['interval']}` | {row['n']} | {row['n_event']} | "
            f"{fmt_rate(row['rate'])} | `{row['rate_fraction'] or 'NA'}` |"
        )
    return "\n".join(lines)


def run_structure(
    dates: list[str], hko: dict[str, float], event: dict[str, bool]
) -> tuple[dict[str, dict[str, object]], list[dict[str, object]]]:
    run_by_date: dict[str, dict[str, object]] = {}
    i = 0
    while i < len(dates):
        if not hko[dates[i]] >= HOT_C:
            i += 1
            continue
        j = i
        while (
            j + 1 < len(dates)
            and hko[dates[j + 1]] >= HOT_C
            and date.fromisoformat(dates[j + 1])
            == date.fromisoformat(dates[j]) + timedelta(days=1)
        ):
            j += 1
        run_dates = dates[i : j + 1]
        run_length = len(run_dates)
        for position, current in enumerate(run_dates, start=1):
            if run_length == 1:
                position_label = "only"
                run_type = "isolated"
            elif position == 1:
                position_label = "start"
                run_type = "inside_run"
            elif position == run_length:
                position_label = "end"
                run_type = "inside_run"
            else:
                position_label = "middle"
                run_type = "inside_run"
            run_by_date[current] = {
                "run_type": run_type,
                "run_length": run_length,
                "position": position_label,
                "position_index": position,
                "run_start": run_dates[0],
                "run_end": run_dates[-1],
            }
        i = j + 1

    both = []
    for current in dates:
        if hko[current] >= HOT_C and event[current]:
            both.append({"date": current, **run_by_date[current]})
    return run_by_date, both


def build_outputs() -> tuple[dict[str, object], str]:
    hko = read_daily(HKO_DAILY, "tmin")
    era5 = read_daily(ERA5_DAILY, "tmin")
    monthly = read_monthly(HKO_MONTHLY)
    dates = sorted(set(hko) & set(era5))
    if len(dates) != MATCHED_DAYS:
        raise AssertionError(f"Expected {MATCHED_DAYS} matched days, got {len(dates)}")
    if dates[0] != "2013-01-01" or dates[-1] != "2023-12-31":
        raise AssertionError("Unexpected matched date range")

    hko_hot = {d: hko[d] >= HOT_C for d in dates}
    era5_hot = {d: era5[d] >= HOT_C for d in dates}
    era5_cold = {d: era5[d] <= 12.0 for d in dates}

    anchors = {
        "matched_days": len(dates),
        "hko_hot_nights": sum(hko_hot.values()),
        "era5_hot_nights": sum(era5_hot.values()),
        "both_hot_nights": sum(hko_hot[d] and era5_hot[d] for d in dates),
        "hko_only_hot_nights": sum(hko_hot[d] and not era5_hot[d] for d in dates),
        "era5_only_hot_nights": sum(not hko_hot[d] and era5_hot[d] for d in dates),
    }
    expected = {
        "matched_days": 4017,
        "hko_hot_nights": 449,
        "era5_hot_nights": 17,
        "both_hot_nights": 14,
        "hko_only_hot_nights": 435,
        "era5_only_hot_nights": 3,
    }
    if anchors != expected:
        raise AssertionError(f"Anchor mismatch: expected {expected}, got {anchors}")

    hot_dates = [d for d in dates if hko_hot[d]]
    bins_02 = make_bins(dates, hko, era5_hot, 260, 310, 2, "n_era5_ge28")
    bins_05 = make_bins(dates, hko, era5_hot, 240, 320, 5, "n_era5_ge28")
    hot_bins_02 = make_bins(hot_dates, hko, era5_hot, 280, 310, 2, "n_era5_ge28")
    hot_overall = rate_payload(len(hot_dates), sum(era5_hot[d] for d in hot_dates))
    cold_bins_02 = make_bins(
        dates, hko, era5_cold, 30, 310, 2, "n_era5_le12"
    )

    _, both_rows = run_structure(dates, hko, era5_hot)
    if len(both_rows) != 14:
        raise AssertionError(f"Expected 14 both-night rows, got {len(both_rows)}")
    for row in both_rows:
        row["hko_tmin_c"] = round(hko[row["date"]], 1)
        row["era5_tmin_c"] = round(era5[row["date"]], 1)

    hko_months = {
        row["month_id"]: int(float(row["hot_nights"]))
        for row in monthly
    }
    if len(monthly) != 132:
        raise AssertionError(f"Expected 132 monthly rows, got {len(monthly)}")
    if sum(hko_months.values()) != anchors["hko_hot_nights"]:
        raise AssertionError("Monthly HKO hot-night sum disagrees with daily HKO")
    hko_hot_months = sorted(m for m, n in hko_months.items() if n > 0)
    era5_month_counts = {
        month_id: sum(era5_hot[d] for d in dates if d[:7] == month_id)
        for month_id in hko_months
    }
    containing_months = [
        month_id for month_id in hko_hot_months if era5_month_counts[month_id] > 0
    ]
    both_jun_sep = [
        row["date"] for row in both_rows if row["date"][5:7] in {"06", "07", "08", "09"}
    ]
    both_may_oct = [
        row["date"] for row in both_rows if row["date"][5:7] in {"05", "10"}
    ]
    hko_jun_sep = sum(
        hko_hot[d] for d in dates if d[5:7] in {"06", "07", "08", "09"}
    )
    monthly = {
        "total_months": len(monthly),
        "hko_hot_months": len(hko_hot_months),
        "hko_hot_nights_total": sum(hko_months.values()),
        "months_with_era5_ge28": len(containing_months),
        "months_with_era5_ge28_ids": containing_months,
        "era5_ge28_counts_by_hko_hot_month": {
            month_id: era5_month_counts[month_id] for month_id in containing_months
        },
        "both_nights_june_september": len(both_jun_sep),
        "both_nights_may_october": len(both_may_oct),
        "both_nights_june_september_dates": both_jun_sep,
        "both_nights_may_october_dates": both_may_oct,
        "hko_hot_nights_june_september": hko_jun_sep,
        "hko_hot_nights_june_september_share": round(
            hko_jun_sep / anchors["hko_hot_nights"], 12
        ),
        "hko_hot_nights_june_september_fraction": (
            f"{hko_jun_sep}/{anchors['hko_hot_nights']}"
        ),
    }

    payload: dict[str, object] = {
        "title": "Luna calibration cut: HKO Headquarters versus ERA5-Land dry-bulb Tmin",
        "date_generated": "2026-08-14",
        "provenance": {
            "status": "REAL",
            "scope": "Exposure only; no hospital counts or health coefficients.",
            "sources": [
                str(HKO_DAILY.relative_to(ROOT)),
                str(ERA5_DAILY.relative_to(ROOT)),
                str(HKO_MONTHLY.relative_to(ROOT)),
            ],
            "alignment": "Inner join on date.",
            "matched_date_start": dates[0],
            "matched_date_end": dates[-1],
            "matched_days": len(dates),
            "bin_convention": "[lower, upper), with empty bins retained.",
        },
        "anchor_checks": anchors,
        "reliability": {
            "hko_tmin_bins_0p2_26_to_31": bins_02,
            "hko_tmin_bins_0p5_24_to_32": bins_05,
            "among_hko_hot_nights": {
                "overall": hot_overall,
                "hko_tmin_bins_0p2_28_to_31": hot_bins_02,
            },
        },
        "both_night_spell_structure": {
            "n_both_nights": len(both_rows),
            "n_isolated": sum(r["run_type"] == "isolated" for r in both_rows),
            "n_inside_runs": sum(r["run_type"] == "inside_run" for r in both_rows),
            "n_start": sum(r["position"] == "start" for r in both_rows),
            "n_middle": sum(r["position"] == "middle" for r in both_rows),
            "n_end": sum(r["position"] == "end" for r in both_rows),
            "dates": both_rows,
        },
        "monthly_containment": monthly,
        "cold_side_analogue": {
            "status": "computed",
            "event": "ERA5 dry-bulb Tmin <= 12.0°C",
            "conditioning": (
                "HKO Tmin in 0.2°C bins spanning 3.0–31.0°C; "
                "full observed HKO support retained"
            ),
            "hko_tmin_bins_0p2_3_to_31": cold_bins_02,
        },
        "claim_boundaries": [
            "These are exposure-calibration descriptives, not health estimates.",
            "No hospital counts, hospitalisation outcomes, coefficients, or q-values were used.",
            "ERA5 dry-bulb Tmin is not a reconstruction of HKO Headquarters Tmin.",
            "The 14 overlapping nights are not a replacement for the HKO hot-night series.",
            "Do not infer causal, clinical, mortality, or hospitalisation meaning from these tables.",
        ],
    }

    anchors_line = (
        "Across 4,017 matched days, the HKO 28°C hot-night rule marks 449 nights, "
        "while ERA5 marks 17 and both mark 14."
    )
    sentence_two = (
        "Among HKO hot nights, ERA5 is also ≥28°C on 14/449 "
        "(0.031180400891; 3.118040089087%)."
    )
    sentence_three = (
        "The 14 overlaps occur in 9 of 57 HKO-hot months, all 14 in June–September, "
        "while 400/449 (0.890868596882; 89.086859688196%) of HKO hot nights fall "
        "in June–September."
    )
    sentence_four = (
        "This is an exposure-calibration comparison of two thermometers; it contains "
        "no hospital counts, health coefficients, or hospitalisation finding."
    )
    md: list[str] = [
        "# Luna calibration cut — 14 August 2026",
        "",
        "**Provenance:** `REAL` files only; exposure-only; no network; no scipy/sklearn.",
        "",
        anchors_line,
        sentence_two,
        sentence_three,
        sentence_four,
        "",
        "The daily files were inner-joined on `date`; 4,017 matched days were "
        "required. Intervals are left-closed/right-open (`[lower, upper)`) and "
        "empty bins are retained. Rates are event count divided by `n`; the JSON "
        "sidecar also records the exact count fraction.",
        "",
        "## A. Reliability",
        "",
        "ERA5 event: dry-bulb Tmin ≥ 28°C.",
        "",
        "### All matched days: 0.2°C bins, HKO Tmin 26–31°C",
        "",
        markdown_rate_table(bins_02, "n ERA5 ≥28°C"),
        "",
        "### All matched days: 0.5°C bins, HKO Tmin 24–32°C",
        "",
        markdown_rate_table(bins_05, "n ERA5 ≥28°C"),
        "",
        "### HKO hot nights only: 0.2°C bins, HKO Tmin 28–31°C",
        "",
        f"Overall: **{hot_overall['n_event']}/{hot_overall['n']} = "
        f"{fmt_rate(hot_overall['rate'])}** "
        f"({float(hot_overall['rate']) * 100:.12f}%).",
        "",
        markdown_rate_table(hot_bins_02, "n ERA5 ≥28°C"),
        "",
        "## B. The 14 both-nights and HKO spell structure",
        "",
        "| Date | HKO Tmin | ERA5 Tmin | HKO run classification | "
        "Run length | Position | Run dates |",
        "|---|---:|---:|---|---:|---|---|",
    ]
    for row in both_rows:
        md.append(
            f"| `{row['date']}` | {row['hko_tmin_c']:.1f} | "
            f"{row['era5_tmin_c']:.1f} | {row['run_type']} | "
            f"{row['run_length']} | {row['position']} | "
            f"`{row['run_start']}–{row['run_end']}` |"
        )
    md += [
        "",
        "An isolated date has a one-day consecutive HKO hot-night run. "
        "For a multi-day run, position is `start`, `middle`, or `end`.",
        "",
        "## C. Monthly containment",
        "",
        f"- HKO months with `hot_nights > 0`: **{len(hko_hot_months)}**.",
        f"- Those HKO-hot months containing ≥1 ERA5 28°C night: "
        f"**{len(containing_months)}** "
        f"(`{', '.join(containing_months)}`).",
        f"- Both-nights in June–September: **{len(both_jun_sep)}/14**.",
        f"- Both-nights in May or October: **{len(both_may_oct)}/14**.",
        f"- HKO hot nights in June–September: **{hko_jun_sep}/449 = "
        f"{hko_jun_sep / anchors['hko_hot_nights']:.12f}** "
        f"({hko_jun_sep / anchors['hko_hot_nights'] * 100:.12f}%).",
        "",
        "The HKO monthly file has 132 rows and its `hot_nights` sum is 449; "
        "the daily HKO flags independently reproduce the same total.",
        "",
        "## D. Cold-side analogue",
        "",
        "Computed because it is inexpensive: "
        "**P(ERA5 Tmin ≤ 12°C | HKO Tmin in bin)**. The full 0.2°C table "
        "spans 3.0–31.0°C, retaining empty bins and the full observed HKO "
        "support; it is in the JSON sidecar under "
        "`cold_side_analogue.hko_tmin_bins_0p2_3_to_31`.",
        "",
        "Selected cold-side rows:",
        "",
        "| HKO Tmin interval (°C) | n | n ERA5 ≤12°C | rate | fraction |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in cold_bins_02:
        if 8.0 <= row["lower_c"] < 16.0:
            md.append(
                f"| `{row['interval']}` | {row['n']} | {row['n_event']} | "
                f"{fmt_rate(row['rate'])} | `{row['rate_fraction'] or 'NA'}` |"
            )
    md += [
        "",
        "## Claim boundaries",
        "",
        "- This cut is `REAL` exposure calibration only; it does not contain "
        "Hospital Authority or other hospital counts.",
        "- The HKO 28°C flag and ERA5 dry-bulb 28°C flag are different "
        "measurement/encoding objects; ERA5 is not a substitute HKO series.",
        "- The 14 overlaps, monthly containment, and cold analogue are not "
        "hospitalisation, mortality, causal, clinical, coefficient, or q-value "
        "findings.",
        "- No health coefficient, q-value, or sklearn-based calculation was used.",
        "",
        f"Reproducibility: `python3 scripts/60_luna_calibration.py`; JSON sidecar: "
        f"`{OUT_JSON.relative_to(ROOT)}`.",
        "",
    ]
    return payload, "\n".join(md)


def main() -> None:
    payload, markdown = build_outputs()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    OUT_MD.write_text(markdown)
    print(
        "Wrote",
        OUT_MD.relative_to(ROOT),
        "and",
        OUT_JSON.relative_to(ROOT),
        "| anchors:",
        payload["anchor_checks"],
    )


if __name__ == "__main__":
    main()
