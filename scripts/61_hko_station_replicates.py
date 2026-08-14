#!/usr/bin/env python3
"""Public HKO station replicates: Headquarters vs King's Park vs Waglan.

Splits siting from instrument. These are published HKO open-data series, not
ERA5 cells and not a substitute Headquarters encoding for the live paper.

Usage:
  python3 scripts/61_hko_station_replicates.py
"""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib_hko_opendata import expected_dates, parse_hko_opendata  # noqa: E402

RAW = ROOT / "data_raw" / "hko"
OUT_TAB = ROOT / "outputs" / "station_replicates"
OUT_FIG = ROOT / "figures" / "station_replicates"
OUT_DOCS = ROOT / "docs" / "id"
HN_C, VHD_C, CD_C = 28.0, 33.0, 12.0
STATIONS = {
    "HKO": {
        "name": "Hong Kong Observatory Headquarters",
        "role": "live-paper encoding",
        "tmin": RAW / "CLMMINT_HKO.csv",
        "tmax": RAW / "CLMMAXT_HKO.csv",
    },
    "KP": {
        "name": "King's Park",
        "role": "nearby official park station",
        "tmin": RAW / "CLMMINT_KP.csv",
        "tmax": RAW / "CLMMAXT_KP.csv",
    },
    "WGL": {
        "name": "Waglan Island",
        "role": "marine official station",
        "tmin": RAW / "CLMMINT_WGL.csv",
        "tmax": RAW / "CLMMAXT_WGL.csv",
    },
}


def load_station(code: str) -> dict[str, dict]:
    spec = STATIONS[code]
    tmin = parse_hko_opendata(spec["tmin"])
    tmax = parse_hko_opendata(spec["tmax"])
    dates = expected_dates()
    rows = {}
    for d in dates:
        mn = tmin.get(d, {"value": None, "completeness": "missing"})
        mx = tmax.get(d, {"value": None, "completeness": "missing"})
        rows[d] = {
            "date": d,
            "year": int(d[:4]),
            "month": int(d[5:7]),
            "tmin": mn["value"],
            "tmax": mx["value"],
            "tmin_c": mn["completeness"],
            "tmax_c": mx["completeness"],
        }
    return rows


def flag_counts(rows: dict[str, dict], *, complete_only: bool) -> dict:
    n = n_tmin = n_tmax = hn = vhd = cd = 0
    n_tmin_c = n_tmax_c = 0
    for r in rows.values():
        n += 1
        if r["tmin_c"] == "C":
            n_tmin_c += 1
        if r["tmax_c"] == "C":
            n_tmax_c += 1
        tmin_ok = r["tmin"] is not None and ((r["tmin_c"] == "C") if complete_only else True)
        tmax_ok = r["tmax"] is not None and ((r["tmax_c"] == "C") if complete_only else True)
        if tmin_ok:
            n_tmin += 1
            if r["tmin"] >= HN_C:
                hn += 1
            if r["tmin"] <= CD_C:
                cd += 1
        if tmax_ok:
            n_tmax += 1
            if r["tmax"] >= VHD_C:
                vhd += 1
    return {
        "n_calendar_days": n,
        "n_tmin_used": n_tmin,
        "n_tmax_used": n_tmax,
        "n_tmin_complete_C": n_tmin_c,
        "n_tmax_complete_C": n_tmax_c,
        "hot_nights": hn,
        "very_hot_days": vhd,
        "cold_days": cd,
        "complete_only": complete_only,
    }


def jaccard_flags(a: dict[str, dict], b: dict[str, dict], field: str, cut: float, op: str) -> dict:
    both = hn_a = hn_b = inter = 0
    for d, ra in a.items():
        rb = b.get(d)
        if rb is None:
            continue
        if ra[field] is None or rb[field] is None:
            continue
        ca = ra["tmin_c"] if field == "tmin" else ra["tmax_c"]
        cb = rb["tmin_c"] if field == "tmin" else rb["tmax_c"]
        if ca != "C" or cb != "C":
            continue
        fa = ra[field] >= cut if op == ">=" else ra[field] <= cut
        fb = rb[field] >= cut if op == ">=" else rb[field] <= cut
        both += 1
        hn_a += int(fa)
        hn_b += int(fb)
        inter += int(fa and fb)
    union = hn_a + hn_b - inter
    return {
        "n_both_complete": both,
        "n_a": hn_a,
        "n_b": hn_b,
        "n_both_flag": inter,
        "n_a_only": hn_a - inter,
        "n_b_only": hn_b - inter,
        "jaccard": None if union == 0 else round(inter / union, 4),
        "subset_b_in_a": None if hn_b == 0 else round(inter / hn_b, 4),
    }


def monthly_counts(rows: dict[str, dict], field: str, cut: float, op: str) -> dict[str, int]:
    out = defaultdict(int)
    for r in rows.values():
        if r[field] is None or (r["tmin_c"] if field == "tmin" else r["tmax_c"]) != "C":
            continue
        hit = r[field] >= cut if op == ">=" else r[field] <= cut
        if hit:
            out[f"{r['year']:04d}-{r['month']:02d}"] += 1
    return dict(out)


def identifying_share(monthly: dict[str, int]) -> float | None:
    months = []
    values = []
    for y in range(2013, 2024):
        for m in range(1, 13):
            months.append(m)
            values.append(float(monthly.get(f"{y:04d}-{m:02d}", 0)))
    values_a = np.array(values, float)
    months_a = np.array(months, int)
    grand = float(values_a.mean())
    ss_b = ss_w = 0.0
    for mo in range(1, 13):
        v = values_a[months_a == mo]
        ss_b += len(v) * (float(v.mean()) - grand) ** 2
        ss_w += float(np.sum((v - v.mean()) ** 2))
    tot = ss_b + ss_w
    return None if tot == 0 else round(ss_w / tot, 4)


def write_bars(path: Path, counts: dict[str, dict]) -> None:
    w, h = 720, 380
    left, top, right, bot = 64, 88, 24, 78
    inner_w = w - left - right
    inner_h = h - top - bot
    order = ["HKO", "KP", "WGL"]
    vmax = max(counts[c]["complete"]["hot_nights"] for c in order)
    bw = inner_w / 3.6
    gap = (inner_w - 3 * bw) / 2
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        'preserveAspectRatio="xMidYMid meet" font-family="Georgia, serif" role="img">',
        '<rect width="100%" height="100%" fill="#f4efe4"/>',
        '<text x="24" y="28" font-size="18">Official hot nights are a place, even among HKO stations</text>',
        '<text x="24" y="48" font-size="12" fill="#5b6773">'
        "Complete (C) days only, 2013–2023. Public HKO open data. Not ERA5. Not a health finding.</text>",
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{h - bot}" stroke="#12181f"/>',
        f'<line x1="{left}" y1="{h - bot}" x2="{w - right}" y2="{h - bot}" stroke="#12181f"/>',
    ]
    labels = {"HKO": "Headquarters", "KP": "King's Park", "WGL": "Waglan"}
    fills = {"HKO": "#0c6b74", "KP": "#8a6d12", "WGL": "#c24e16"}
    for i, code in enumerate(order):
        x = left + i * (bw + gap)
        v = counts[code]["complete"]["hot_nights"]
        bh = 0 if vmax == 0 else v / vmax * (inner_h - 24)
        y = h - bot - bh
        parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{fills[code]}"/>'
        )
        parts.append(
            f'<text x="{x + bw / 2:.1f}" y="{y - 8:.1f}" text-anchor="middle" font-size="16">{v}</text>'
        )
        parts.append(
            f'<text x="{x + bw / 2:.1f}" y="{h - bot + 22}" text-anchor="middle" font-size="16">{labels[code]}</text>'
        )
    parts.append(
        f'<text x="24" y="{h - 18}" font-size="12" fill="#5b6773">'
        "King's Park is not Headquarters. Waglan is not an ERA5 cell. Live paper stays on Headquarters.</text>"
    )
    parts.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts) + "\n")


def main() -> int:
    loaded = {code: load_station(code) for code in STATIONS}
    n_days = len(expected_dates())
    for code, rows in loaded.items():
        if len(rows) != n_days:
            raise RuntimeError(f"{code} expected {n_days} days, got {len(rows)}")
    if flag_counts(loaded["HKO"], complete_only=True)["hot_nights"] != 449:
        raise RuntimeError("HKO Headquarters complete hot nights must remain 449.")
    if flag_counts(loaded["HKO"], complete_only=True)["cold_days"] != 145:
        raise RuntimeError("HKO Headquarters complete cold days must remain 145.")

    counts = {}
    for code, rows in loaded.items():
        counts[code] = {
            "name": STATIONS[code]["name"],
            "role": STATIONS[code]["role"],
            "complete": flag_counts(rows, complete_only=True),
            "numeric_including_incomplete": flag_counts(rows, complete_only=False),
        }
        hn_m = monthly_counts(rows, "tmin", HN_C, ">=")
        counts[code]["identifying_share_hot_nights"] = identifying_share(hn_m)

    pairs = {
        "HKO_vs_KP_hot_nights": jaccard_flags(loaded["HKO"], loaded["KP"], "tmin", HN_C, ">="),
        "HKO_vs_WGL_hot_nights": jaccard_flags(loaded["HKO"], loaded["WGL"], "tmin", HN_C, ">="),
        "HKO_vs_KP_very_hot_days": jaccard_flags(loaded["HKO"], loaded["KP"], "tmax", VHD_C, ">="),
        "HKO_vs_WGL_very_hot_days": jaccard_flags(loaded["HKO"], loaded["WGL"], "tmax", VHD_C, ">="),
        "HKO_vs_KP_cold_days": jaccard_flags(loaded["HKO"], loaded["KP"], "tmin", CD_C, "<="),
        "HKO_vs_WGL_cold_days": jaccard_flags(loaded["HKO"], loaded["WGL"], "tmin", CD_C, "<="),
    }

    payload = {
        "title": "Public HKO station replicates",
        "window": {"start": "2013-01-01", "end": "2023-12-31", "n_days": n_days},
        "provenance": (
            "REAL_PUBLIC. Hong Kong Observatory open-data CLMMINT/CLMMAXT for "
            "stations HKO, KP, and WGL. Completeness code C is the primary cut. "
            "Not ERA5. Not a substitute Headquarters series. Exposure only."
        ),
        "stations": counts,
        "pairs": pairs,
        "punchline": (
            f"On days both complete, Headquarters has "
            f"{pairs['HKO_vs_KP_hot_nights']['n_a']} hot nights and King's Park "
            f"{pairs['HKO_vs_KP_hot_nights']['n_b']} (Jaccard "
            f"{pairs['HKO_vs_KP_hot_nights']['jaccard']}). Waglan Jaccard "
            f"{pairs['HKO_vs_WGL_hot_nights']['jaccard']}. Nearby siting is not "
            "the same instrument. Live paper stays on Headquarters."
        ),
        "claim_boundaries": [
            "These series are not a validation of ERA5.",
            "Do not replace Headquarters with King's Park or Waglan in the live paper.",
            "Do not overlay hospital counts on stations.",
            "Incomplete (#) days are reported separately and are not the primary cut.",
        ],
    }

    OUT_TAB.mkdir(parents=True, exist_ok=True)
    OUT_FIG.mkdir(parents=True, exist_ok=True)
    OUT_DOCS.mkdir(parents=True, exist_ok=True)
    (OUT_TAB / "station_replicates.json").write_text(json.dumps(payload, indent=2) + "\n")
    with (OUT_TAB / "station_flag_counts.csv").open("w", newline="") as f:
        wcsv = csv.DictWriter(
            f,
            fieldnames=[
                "station", "name", "cut", "hot_nights", "very_hot_days", "cold_days",
                "n_tmin_used", "n_tmax_used", "identifying_share_hot_nights",
            ],
        )
        wcsv.writeheader()
        for code, block in counts.items():
            for cut_name in ("complete", "numeric_including_incomplete"):
                c = block[cut_name]
                wcsv.writerow({
                    "station": code,
                    "name": block["name"],
                    "cut": cut_name,
                    "hot_nights": c["hot_nights"],
                    "very_hot_days": c["very_hot_days"],
                    "cold_days": c["cold_days"],
                    "n_tmin_used": c["n_tmin_used"],
                    "n_tmax_used": c["n_tmax_used"],
                    "identifying_share_hot_nights": block["identifying_share_hot_nights"],
                })
    write_bars(OUT_FIG / "hko_station_hot_nights.svg", counts)
    write_bars(OUT_DOCS / "hko_station_hot_nights.svg", counts)
    slim = {
        k: payload[k]
        for k in ("title", "window", "provenance", "stations", "pairs", "punchline", "claim_boundaries")
    }
    (OUT_DOCS / "stations_embed.js").write_text(
        "window.ID_STATIONS = " + json.dumps(slim, separators=(",", ":")) + ";\n"
    )
    print(payload["punchline"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
