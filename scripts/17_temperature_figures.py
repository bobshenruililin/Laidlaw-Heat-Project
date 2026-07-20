#!/usr/bin/env python3
"""Build monthly temperature ribbon and lag-1 illustration figures.

Outputs:
  figures/temperature/monthly_temp_ribbon_2013_2023.{pdf,png}
  figures/temperature/tmax_lag1_example.{pdf,png}
"""

from __future__ import annotations

import csv
import math
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

ROOT = Path(__file__).resolve().parents[1]
CLIMATE = ROOT / "data_processed" / "climate_monthly_2013_2023.csv"
OUT = ROOT / "figures" / "temperature"


def load_climate():
    rows = list(csv.DictReader(CLIMATE.open()))
    dates = [datetime.strptime(r["month_id"], "%Y-%m") for r in rows]
    tmean = [float(r["mean_temp"]) for r in rows]
    tmin = [float(r["mean_tmin"]) for r in rows]
    tmax = [float(r["mean_tmax"]) for r in rows]
    return dates, tmean, tmin, tmax


def pearson(a, b):
    n = len(a)
    ma = sum(a) / n
    mb = sum(b) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    da = math.sqrt(sum((x - ma) ** 2 for x in a))
    db = math.sqrt(sum((y - mb) ** 2 for y in b))
    return num / (da * db)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    dates, tmean, tmin, tmax = load_climate()
    assert len(dates) == 132
    assert dates[0].strftime("%Y-%m") == "2013-01"
    assert dates[-1].strftime("%Y-%m") == "2023-12"

    r = pearson(tmax[1:], tmax[:-1])

    fig, ax = plt.subplots(figsize=(10.5, 4.2), dpi=200)
    ax.fill_between(
        dates,
        tmin,
        tmax,
        color="#94a3b8",
        alpha=0.35,
        linewidth=0,
        label="Monthly mean Tmin–Tmax range",
    )
    ax.plot(dates, tmean, color="#0f172a", linewidth=1.6, label="Monthly mean temperature")
    ax.plot(dates, tmax, color="#b45309", linewidth=0.9, alpha=0.85, label="Monthly mean Tmax")
    ax.plot(dates, tmin, color="#1d4ed8", linewidth=0.9, alpha=0.85, label="Monthly mean Tmin")
    ax.set_title("Hong Kong Observatory Headquarters", fontsize=13, fontweight="bold", pad=8)
    ax.text(
        0.0,
        1.02,
        "Monthly temperature, January 2013–December 2023  |  N = 132 months  |  Environmental exposure data only",
        transform=ax.transAxes,
        fontsize=8.5,
        color="#334155",
        va="bottom",
    )
    ax.set_ylabel("Temperature (°C)", fontsize=10)
    ax.set_xlim(datetime(2013, 1, 1), datetime(2023, 12, 1))
    ax.set_ylim(12, 34)
    ax.xaxis.set_major_locator(mdates.YearLocator(base=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_minor_locator(mdates.YearLocator())
    ax.yaxis.set_major_locator(mticker.MultipleLocator(5))
    ax.grid(True, which="major", color="#e2e8f0", linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=4, frameon=False, fontsize=8.5)
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.22)
    fig.savefig(OUT / "monthly_temp_ribbon_2013_2023.pdf", bbox_inches="tight")
    fig.savefig(OUT / "monthly_temp_ribbon_2013_2023.png", bbox_inches="tight")
    plt.close(fig)

    fig2, ax2 = plt.subplots(figsize=(6.2, 3.6), dpi=200)
    d36 = dates[-36:]
    ax2.plot(d36, tmax[-36:], color="#b45309", linewidth=1.5, label="Tmax (same month)")
    ax2.plot(d36, tmax[-37:-1], color="#64748b", linewidth=1.4, linestyle="--", label="Tmax lag-1 month")
    ax2.set_title("Lag construction (last 36 months)", fontsize=11, fontweight="bold")
    ax2.text(
        0.0,
        1.03,
        f"Same-month vs previous-month mean Tmax  |  r ≈ {r:.2f} over full series (N = 131 pairs)",
        transform=ax2.transAxes,
        fontsize=8,
        color="#334155",
    )
    ax2.set_ylabel("Tmax (°C)", fontsize=9)
    ax2.set_xlim(d36[0], d36[-1])
    ax2.xaxis.set_major_locator(mdates.YearLocator())
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax2.grid(True, color="#e2e8f0", linewidth=0.8)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2, frameon=False, fontsize=8)
    fig2.tight_layout()
    fig2.subplots_adjust(bottom=0.22)
    fig2.savefig(OUT / "tmax_lag1_example.pdf", bbox_inches="tight")
    fig2.savefig(OUT / "tmax_lag1_example.png", bbox_inches="tight")
    plt.close(fig2)

    print(f"Wrote ribbon + lag figures to {OUT}")
    print(f"Verified r(Tmax, lag-1 Tmax) = {r:.6f}")


if __name__ == "__main__":
    main()
