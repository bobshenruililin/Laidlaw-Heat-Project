#!/usr/bin/env python3
"""Effective rank of the first-wave HM/CM month flags.

The catalogue names 98 recipes. The file on disk is the first-wave set:
twelve binary flags plus HM23 event starts. CM05 is a zero column.
This script asks how many independent month-flags those binaries actually are.

EXPOSURE ONLY. No health coefficients. No HA rows. Not a licence to fit more
definitions. Live paper stays on the six HKO encodings.

Usage:
  python3 scripts/58_hm_cm_effective_rank.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FLAGS = ROOT / "data_processed" / "hm_cm_month_flags_2013_2023.csv"
OUT_TAB = ROOT / "outputs" / "hm_cm_rank"
OUT_FIG = ROOT / "figures" / "hm_cm_rank"

BINARY_ORDER = [
    "HM08", "HM15", "HM17", "HM19", "HM27", "HM32",
    "HM23",
    "CM03", "CM08", "CM15", "CM05", "CM30",
]


def jaccard(a: np.ndarray, b: np.ndarray) -> float | None:
    aa = a > 0
    bb = b > 0
    inter = int(np.sum(aa & bb))
    union = int(np.sum(aa | bb))
    if union == 0:
        return None
    return round(inter / union, 4)


def is_subset(a: np.ndarray, b: np.ndarray) -> bool:
    return bool(np.all((a > 0) <= (b > 0)))


def calendar_months_on(month_ids: list[str], flag: np.ndarray) -> list[int]:
    months = sorted({int(mid[5:7]) for mid, on in zip(month_ids, flag) if on > 0})
    return months


def write_scree(path: Path, evals: list[float], pr: float) -> None:
    w, h = 720, 420
    left, right, top, bot = 56, 28, 64, 56
    inner_w = w - left - right
    inner_h = h - top - bot
    ymax = 5.0
    n = len(evals)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="Georgia, serif">',
        '<rect width="100%" height="100%" fill="#f4efe4"/>',
        '<text x="24" y="28" font-size="16">Eleven flags, about four dimensions</text>',
        '<text x="24" y="48" font-size="11" fill="#5b6773">'
        "Eigenvalues of the correlation matrix of the non-degenerate first-wave "
        "HM/CM binaries. Participation ratio = effective rank. Exposure only.</text>",
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{h - bot}" stroke="#12181f"/>',
        f'<line x1="{left}" y1="{h - bot}" x2="{w - right}" y2="{h - bot}" stroke="#12181f"/>',
    ]
    bw = inner_w / n
    for i, lam in enumerate(evals):
        bh = (lam / ymax) * inner_h
        x = left + i * bw
        y = h - bot - bh
        fill = "#0c6b74" if i < 2 else "#5b6773"
        parts.append(
            f'<rect x="{x + 8:.1f}" y="{y:.1f}" width="{bw - 16:.1f}" height="{bh:.1f}" '
            f'fill="{fill}" fill-opacity="0.88"/>'
        )
        parts.append(
            f'<text x="{x + bw / 2:.1f}" y="{h - bot + 16:.1f}" text-anchor="middle" '
            f'font-size="11">{i + 1}</text>'
        )
    for tick in (0, 1, 2, 3, 4, 5):
        y = h - bot - (tick / ymax) * inner_h
        parts.append(f'<line x1="{left - 4}" y1="{y:.1f}" x2="{left}" y2="{y:.1f}" stroke="#12181f"/>')
        parts.append(
            f'<text x="{left - 8}" y="{y + 4:.1f}" text-anchor="end" font-size="11" fill="#5b6773">{tick}</text>'
        )
    parts.append(
        f'<text x="{left}" y="{h - 18}" font-size="11" fill="#5b6773">'
        f"Effective rank {pr:.2f}. PC1+PC2 hold 67% of the 11-flag correlation. "
        "Heat never co-fires with cold. CM05 is a zero column, not a test. "
        "Not a health finding.</text>"
    )
    parts.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts) + "\n")


def main() -> int:
    rows = list(csv.DictReader(FLAGS.open()))
    if len(rows) != 132:
        raise RuntimeError(f"Expected 132 months, got {len(rows)}.")
    month_ids = [r["month_id"] for r in rows]
    raw = {name: np.array([float(r[name]) for r in rows], float) for name in BINARY_ORDER}
    starts = np.array([float(r["HM23_event_starts"]) for r in rows], float)

    degenerate = [name for name, x in raw.items() if float(x.std()) == 0]
    live_names = [name for name in BINARY_ORDER if name not in degenerate]
    X = np.column_stack([raw[name] for name in live_names])
    C = np.corrcoef(X, rowvar=False)
    evals = np.clip(np.sort(np.linalg.eigvalsh(C))[::-1], 0.0, None)
    pr = float((evals.sum() ** 2) / np.sum(evals ** 2))
    share = evals / evals.sum()

    jac = []
    for i, a in enumerate(live_names):
        for j, b in enumerate(live_names):
            if j <= i:
                continue
            jac.append({
                "a": a,
                "b": b,
                "jaccard": jaccard(X[:, i], X[:, j]),
                "intersection": int(np.sum((X[:, i] > 0) & (X[:, j] > 0))),
                "union": int(np.sum((X[:, i] > 0) | (X[:, j] > 0))),
            })

    heat = [n for n in live_names if n.startswith("HM")]
    cold = [n for n in live_names if n.startswith("CM")]
    heat_cold = [row for row in jac if (row["a"][:2] != row["b"][:2])]
    max_hc = max((row["jaccard"] or 0.0) for row in heat_cold)

    subsets = []
    for a in live_names:
        for b in live_names:
            if a == b:
                continue
            if is_subset(raw[a], raw[b]) and int(np.sum(raw[a] > 0)) < int(np.sum(raw[b] > 0)):
                subsets.append({
                    "inner": a,
                    "outer": b,
                    "n_inner": int(np.sum(raw[a] > 0)),
                    "n_outer": int(np.sum(raw[b] > 0)),
                })

    flag_rows = []
    for name in BINARY_ORDER:
        x = raw[name]
        flag_rows.append({
            "name": name,
            "n_months_on": int(np.sum(x > 0)),
            "degenerate": name in degenerate,
            "calendar_months_ever_on": calendar_months_on(month_ids, x),
        })

    payload = {
        "title": "Effective rank of first-wave HM/CM flags",
        "window": {"start": "2013-01", "end": "2023-12", "n_months": 132},
        "source": "data_processed/hm_cm_month_flags_2013_2023.csv",
        "provenance": (
            "REAL HKO-derived first-wave hot-month and cold-month binaries. "
            "The on-disk file has twelve named flags plus HM23 event starts, "
            "not the 98-recipe catalogue. Effective rank is the participation "
            "ratio of the correlation-matrix eigenvalues of the 11 "
            "non-degenerate binaries. Exposure descriptives only. No health "
            "outcomes. No project coefficients."
        ),
        "why_this_exists": (
            "An unlocked catalogue can look like 98 independent tests. The "
            "fitted first-wave set is 11 live binaries whose correlation has "
            "effective rank about four, and heat never co-fires with cold. "
            "Adding the next ID is not a new test unless it leaves this span."
        ),
        "n_named_binaries_on_disk": 12,
        "n_nondegenerate": len(live_names),
        "degenerate": degenerate,
        "live_names": live_names,
        "heat_names": heat,
        "cold_names": cold,
        "eigenvalues": [round(float(v), 4) for v in evals],
        "variance_share": [round(float(v), 4) for v in share],
        "pc1_share": round(float(share[0]), 4),
        "pc1_pc2_share": round(float(share[:2].sum()), 4),
        "pc1_pc2_pc3_share": round(float(share[:3].sum()), 4),
        "effective_rank": round(pr, 3),
        "max_heat_cold_jaccard": round(float(max_hc), 4),
        "nested_subsets": subsets,
        "flags": flag_rows,
        "hm23_event_starts": {
            "n_months_with_start": int(np.sum(starts > 0)),
            "n_event_starts_total": int(starts.sum()),
            "max_starts_in_a_month": int(starts.max()),
            "note": "Count 0–3, not a binary; excluded from the correlation rank.",
        },
        "pairwise_jaccard": jac,
        "punchline": (
            f"{len(live_names)} non-degenerate first-wave flags; effective rank "
            f"{pr:.2f}; PC1+PC2 {share[:2].sum():.0%}. Heat–cold Jaccard is "
            f"{max_hc:.2f} (they never co-fire). CM05 is all zeros. "
            "The 98-recipe catalogue is not 98 tests."
        ),
        "claim_boundaries": [
            "This rank does not use hospital counts.",
            "Do not reopen the outcome panel because the rank is small.",
            "Do not treat a nested inner flag as an independent sensitivity.",
            "Do not call the 98-recipe catalogue a fitted universe; most IDs were unfitted on purpose.",
            "This is not Gate 3, not form 2a, and not a Hogan lock by itself.",
        ],
    }

    OUT_TAB.mkdir(parents=True, exist_ok=True)
    (OUT_TAB / "hm_cm_effective_rank.json").write_text(json.dumps(payload, indent=2) + "\n")
    with (OUT_TAB / "hm_cm_flag_counts.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["name", "n_months_on", "degenerate", "calendar_months_ever_on"])
        w.writeheader()
        for row in flag_rows:
            w.writerow({
                **{k: row[k] for k in ("name", "n_months_on", "degenerate")},
                "calendar_months_ever_on": ",".join(str(m) for m in row["calendar_months_ever_on"]),
            })
    with (OUT_TAB / "hm_cm_pairwise_jaccard.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["a", "b", "jaccard", "intersection", "union"])
        w.writeheader()
        w.writerows(jac)

    write_scree(OUT_FIG / "hm_cm_scree.svg", [float(v) for v in evals], pr)
    print(payload["punchline"])
    print("wrote", OUT_TAB / "hm_cm_effective_rank.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
