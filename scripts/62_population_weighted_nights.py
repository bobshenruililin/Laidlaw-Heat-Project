#!/usr/bin/env python3
"""Population-weight ERA5 28°C cell-nights with public WorldPop 2020 1 km.

Asks where the marine-south mass of 28°C nights sits relative to people.
Exposure only. Not a health-equity result. Not a district hospital map.

Usage:
  python3 scripts/62_population_weighted_nights.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POP = ROOT / "data_raw" / "worldpop" / "ppp_HKG_2020_1km_Aggregated.csv"
CELLS = ROOT / "outputs" / "hk_spatial" / "hk_spatial_cells.csv"
OUT_TAB = ROOT / "outputs" / "population_weighted_nights"
OUT_FIG = ROOT / "figures" / "population_weighted_nights"
OUT_DOCS = ROOT / "docs" / "id"
HALF = 0.05  # 0.1° cell half-width
SOUTH_LAT = 22.25  # southern two rows of the 0.1° lattice


def load_pop() -> list[tuple[float, float, float]]:
    rows = []
    with POP.open() as f:
        for row in csv.DictReader(f):
            z = float(row["Z"])
            if z < 0:
                continue
            rows.append((float(row["X"]), float(row["Y"]), z))
    if len(rows) < 1000:
        raise RuntimeError(f"WorldPop ASCII too small: {len(rows)}")
    return rows


def load_grid() -> list[dict]:
    out = []
    with CELLS.open() as f:
        for row in csv.DictReader(f):
            if row["kind"] != "grid":
                continue
            out.append({
                "id": row["id"],
                "lat": float(row["lat"]),
                "lon": float(row["lon"]),
                "hn_total": int(float(row["hn_total"])),
                "dist_coast_km": float(row["dist_coast_km"]),
            })
    if len(out) != 30:
        raise RuntimeError(f"Expected 30 grid cells, got {len(out)}")
    return out


def weight_cells(grid: list[dict], pop: list[tuple[float, float, float]]) -> list[dict]:
    for cell in grid:
        lon, lat = cell["lon"], cell["lat"]
        s = 0.0
        n = 0
        for x, y, z in pop:
            if lon - HALF <= x < lon + HALF and lat - HALF <= y < lat + HALF:
                s += z
                n += 1
        cell["pop"] = s
        cell["n_pop_pixels"] = n
        cell["south"] = lat <= SOUTH_LAT
        cell["hn_x_pop"] = cell["hn_total"] * s
    return grid


def write_bars(path: Path, unweighted: float, weighted: float) -> None:
    w, h = 720, 300
    left, top, right, bot = 64, 56, 36, 64
    inner_w = w - left - right
    inner_h = h - top - bot
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        'preserveAspectRatio="xMidYMid meet" font-family="Georgia, serif" role="img">',
        '<rect width="100%" height="100%" fill="#f4efe4"/>',
        '<text x="24" y="28" font-size="18">Unweighted 28°C nights sit south of the people</text>',
        '<text x="24" y="46" font-size="12" fill="#5b6773">'
        "Share of ERA5-Land 0.1° hot nights in cells at ≤22.25°N. WorldPop 2020 1 km. Exposure only.</text>",
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{h - bot}" stroke="#12181f"/>',
        f'<line x1="{left}" y1="{h - bot}" x2="{w - right}" y2="{h - bot}" stroke="#12181f"/>',
    ]
    items = [
        ("Unweighted cell-nights", unweighted, "#c24e16"),
        ("Population-weighted", weighted, "#0c6b74"),
    ]
    bw = inner_w / 2.8
    gap = (inner_w - 2 * bw) / 1.5
    for i, (lab, v, fill) in enumerate(items):
        x = left + i * (bw + gap)
        bh = v * inner_h
        y = h - bot - bh
        parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{fill}"/>'
        )
        parts.append(
            f'<text x="{x + bw / 2:.1f}" y="{y - 8:.1f}" text-anchor="middle" font-size="16">{v:.0%}</text>'
        )
        parts.append(
            f'<text x="{x + bw / 2:.1f}" y="{h - bot + 22}" text-anchor="middle" font-size="14">{lab}</text>'
        )
    parts.append(
        f'<text x="24" y="{h - 16}" font-size="12" fill="#5b6773">'
        "Not a hospital map. Not Marmot as a finding. Live paper stays on Headquarters.</text>"
    )
    parts.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts) + "\n")


def main() -> int:
    pop = load_pop()
    grid = weight_cells(load_grid(), pop)
    hn = sum(c["hn_total"] for c in grid)
    pop_total = sum(c["pop"] for c in grid)
    hn_south = sum(c["hn_total"] for c in grid if c["south"])
    pop_south = sum(c["pop"] for c in grid if c["south"])
    w_hn = sum(c["hn_x_pop"] for c in grid)
    w_hn_south = sum(c["hn_x_pop"] for c in grid if c["south"])
    if hn != 2935:
        raise RuntimeError(f"Grid hot-night total drifted: {hn}")
    unweighted_south = hn_south / hn
    weighted_south = w_hn_south / w_hn if w_hn else None
    pop_share_south = pop_south / pop_total if pop_total else None
    payload = {
        "title": "Population-weighted ERA5 28°C nights",
        "provenance": (
            "REAL_PUBLIC. WorldPop unconstrained 1 km 2020 ASCII over Hong Kong; "
            "ERA5-Land 0.1° cell-nights from script 49. Exposure descriptives only. "
            "No hospital counts. No district health overlay."
        ),
        "worldpop": {
            "n_pixels": len(pop),
            "sum_people_in_file": round(sum(z for _, _, z in pop), 1),
            "sum_people_in_30_cells": round(pop_total, 1),
            "source": "ppp_HKG_2020_1km_Aggregated.csv",
        },
        "grid": {
            "n_cells": 30,
            "hn_total": hn,
            "hn_south_le_22p25": hn_south,
            "pop_south_le_22p25": round(pop_south, 1),
        },
        "shares": {
            "unweighted_hn_south": round(unweighted_south, 4),
            "population_weighted_hn_south": None if weighted_south is None else round(weighted_south, 4),
            "population_share_south": None if pop_share_south is None else round(pop_share_south, 4),
        },
        "cells": [
            {
                "id": c["id"],
                "lat": c["lat"],
                "lon": c["lon"],
                "hn_total": c["hn_total"],
                "pop": round(c["pop"], 1),
                "n_pop_pixels": c["n_pop_pixels"],
                "south": c["south"],
            }
            for c in grid
        ],
        "punchline": (
            f"Southern cells (≤22.25°N) hold {hn_south}/{hn} unweighted ERA5 28°C "
            f"nights ({unweighted_south:.1%}) but "
            f"{pop_share_south:.1%} of the WorldPop mass in the lattice, so the "
            f"population-weighted night share is {weighted_south:.1%}. "
            "People are not where the marine flag is. Not a health finding."
        ),
        "claim_boundaries": [
            "This is not a Marmot / equity hospitalisation result.",
            "Do not overlay CHD/HF on cells or districts.",
            "WorldPop is not C&SD and not a T2D/HTN cohort denominator.",
            "The live paper stays on Headquarters.",
        ],
    }
    OUT_TAB.mkdir(parents=True, exist_ok=True)
    OUT_FIG.mkdir(parents=True, exist_ok=True)
    OUT_DOCS.mkdir(parents=True, exist_ok=True)
    (OUT_TAB / "population_weighted_nights.json").write_text(json.dumps(payload, indent=2) + "\n")
    with (OUT_TAB / "cell_population_weights.csv").open("w", newline="") as f:
        wcsv = csv.DictWriter(
            f,
            fieldnames=["id", "lat", "lon", "hn_total", "pop", "n_pop_pixels", "south"],
        )
        wcsv.writeheader()
        wcsv.writerows(payload["cells"])
    write_bars(
        OUT_FIG / "population_weighted_south_share.svg",
        unweighted_south,
        weighted_south or 0.0,
    )
    write_bars(
        OUT_DOCS / "population_weighted_south_share.svg",
        unweighted_south,
        weighted_south or 0.0,
    )
    slim = {k: payload[k] for k in ("title", "provenance", "worldpop", "grid", "shares", "punchline", "claim_boundaries")}
    (OUT_DOCS / "pop_embed.js").write_text(
        "window.ID_POP = " + json.dumps(slim, separators=(",", ":")) + ";\n"
    )
    print(payload["punchline"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
