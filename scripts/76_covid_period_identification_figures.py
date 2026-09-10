#!/usr/bin/env python3
"""Rebuild COVID-period identification figures from existing public tables.

Does not open governed HA panels. Does not fit health models.
Figure 1 uses annual first-event totals plus the C&SD 35+ mean already stored
on that table. Figure 2 uses the stored month-year cold-day file. Figure 3 is
delegated to scripts/66_live_figure3_relabel.py.
"""
from __future__ import annotations

import csv
import runpy
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures" / "live_identification"
ANNUAL = ROOT / "outputs" / "tables" / "cvd_descriptive_annual_totals.csv"
COLD = ROOT / "outputs" / "live_identification" / "cold_days_by_month_year.csv"

TEAL = "#174d5b"
HF_RED = "#8A3E4C"
GREY = "#6C737A"
TEXT = "#202124"


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def figure_b() -> Path:
    rows = _read_csv(ANNUAL)
    years = list(range(2013, 2024))
    chd = [int(r["total_events"]) for r in rows if r["outcome"] == "chd"]
    hf = [int(r["total_events"]) for r in rows if r["outcome"] == "hf"]
    pop = []
    for y in years:
        vals = [float(r["mean_population"]) for r in rows if int(r["year"]) == y]
        pop.append(float(np.mean(vals)))

    fig, axes = plt.subplots(3, 1, figsize=(8.0, 8.2), sharex=True)
    series = [
        (axes[0], years, chd, "CHD first hospitalisations (annual total)", TEAL),
        (axes[1], years, hf, "HF first hospitalisations (annual total)", HF_RED),
        (
            axes[2],
            years,
            pop,
            "Hong Kong population aged 35+ (persons; contextual only)",
            GREY,
        ),
    ]
    for ax, xs, ys, title, color in series:
        ax.plot(xs, ys, color=color, lw=1.8, marker="o", ms=4.2)
        ax.set_title(title, loc="left", fontsize=10, color=TEXT, fontweight="bold")
        ax.set_xticks(years)
        ax.tick_params(labelsize=8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda v, _pos: f"{v:,.0f}")
        )
    axes[2].set_xticklabels([str(y) for y in years], rotation=45, ha="right")
    fig.suptitle(
        "First-event counts fell while the general population aged 35+ rose",
        fontsize=12,
        fontweight="bold",
        color=TEXT,
        x=0.01,
        ha="left",
    )
    fig.text(
        0.01,
        0.01,
        "Health provenance: HA_APPROVED_AGGREGATE annual summaries. "
        "Population: C&SD 35+ already stored on the annual table (not the T2D/HTN risk set). "
        "Not consecutive duration. Not physiology.",
        fontsize=7.5,
        color="#5F6368",
    )
    fig.tight_layout(rect=(0.0, 0.04, 1.0, 0.97))
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    png = FIG_DIR / "figure_B_first_event_depletion.png"
    fig.savefig(png, dpi=320, facecolor="white")
    plt.close(fig)
    return png


def figure_a() -> Path:
    rows = _read_csv(COLD)
    years = sorted({int(r["year"]) for r in rows})
    months = list(range(1, 13))
    grid = np.zeros((len(months), len(years)))
    for r in rows:
        grid[int(r["month"]) - 1, years.index(int(r["year"]))] = float(r["cold_days"])
    fig, ax = plt.subplots(figsize=(8.0, 5.8))
    im = ax.imshow(grid, aspect="auto", cmap="Blues", origin="upper")
    ax.set_xticks(range(len(years)))
    ax.set_xticklabels([str(y) for y in years], rotation=45, ha="right")
    ax.set_yticks(range(12))
    ax.set_yticklabels(
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    )
    ax.set_title(
        "Official cold days by year and month (HKO Headquarters)",
        loc="left",
        fontsize=11,
        fontweight="bold",
        color=TEXT,
    )
    fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02, label="Official cold days")
    fig.text(
        0.01,
        0.01,
        "REAL HKO official cold-day flags (Tmin ≤ 12 °C), month totals. "
        "141 of 145 days fall in Dec–Feb. Not consecutive duration. Not physiology.",
        fontsize=7.5,
        color="#5F6368",
    )
    fig.tight_layout(rect=(0.0, 0.05, 1.0, 1.0))
    png = FIG_DIR / "figure_A_cold_day_identification.png"
    fig.savefig(png, dpi=320, facecolor="white")
    plt.close(fig)
    return png


def figure_d() -> None:
    runpy.run_path(str(ROOT / "scripts" / "66_live_figure3_relabel.py"), run_name="__main__")


def main() -> None:
    a = figure_a()
    b = figure_b()
    figure_d()
    print(f"wrote {a}")
    print(f"wrote {b}")
    print(f"wrote {FIG_DIR / 'figure_D_trend_depletion_sensitivity.png'}")


if __name__ == "__main__":
    main()
