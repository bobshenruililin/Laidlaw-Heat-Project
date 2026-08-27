#!/usr/bin/env python3
"""Teaching forest for Bishai's 27 Aug 2026 Figure 3 comments.

Reads existing HA_APPROVED_AGGREGATE trend/depletion estimates. Fits no health model.
Y-axis labels say 'time-trend spline, N df' so spline flexibility cannot be read as
an N-day heatwave. The 'per 5 days' unit is the reporting scale, not consecutive duration.

Outputs:
  reports/bishai_forest_hhap_2026-08-27/figure_teaching_spline_df_not_duration.png
  reports/bishai_forest_hhap_2026-08-27/quoted_estimates.csv
"""
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "outputs" / "tables" / "cvd_trend_depletion_sensitivity.csv"
OUT_DIR = ROOT / "reports" / "bishai_forest_hhap_2026-08-27"
PNG = OUT_DIR / "figure_teaching_spline_df_not_duration.png"
CSV_OUT = OUT_DIR / "quoted_estimates.csv"

# Display order: top = what Bishai likely pointed at (df 8 / 6 / 3), then pre-COVID, then Model 1.
SCENARIOS = [
    ("trend_ns8", "Time-trend spline, 8 df (sensitivity)"),
    ("trend_ns6", "Time-trend spline, 6 df (sensitivity)"),
    ("trend_ns3", "Time-trend spline, 3 df (sensitivity)"),
    ("pre_covid", "Pre-COVID window (Jan 2013–Dec 2019, 84 months)"),
    ("covid_phase_adjusted", "COVID-phase adjusted (full 132 months)"),
    ("year_fixed_effects", "Year fixed effects (sensitivity)"),
    ("baseline_ns4", "Model 1 baseline (time-trend spline, 4 df)"),
]

PANELS = [
    (
        "chd",
        "hot_nights",
        "CHD · official hot nights",
        "per 5 additional hot nights in the month\n(reporting scale, not consecutive duration)",
        (0.985, 1.085),
    ),
    (
        "hf",
        "cold_days",
        "HF · official cold days",
        "per 5 additional cold days in the month\n(reporting scale, not consecutive duration)",
        (0.96, 1.30),
    ),
]


def fmt_ci(rr: float, lo: float, hi: float) -> str:
    """Three-decimal display, except keep four decimals when 3-dp would hide a bound on 1."""
    if lo < 1.0 <= round(lo, 3):
        return f"{rr:.3f} ({lo:.4f}–{hi:.3f})"
    return f"{rr:.3f} ({lo:.3f}–{hi:.3f})"


def load_rows() -> dict[tuple[str, str, str], dict]:
    out: dict[tuple[str, str, str], dict] = {}
    with SRC.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = (row["outcome"], row["exposure"], row["scenario"])
            out[key] = {
                "rr": float(row["rr"]),
                "lo": float(row["rr_low"]),
                "hi": float(row["rr_high"]),
                "n": int(row["n_months"]),
                "acf1": float(row["residual_acf1"]),
                "data_status": row["data_status"],
            }
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data = load_rows()

    quoted = []
    fig, axes = plt.subplots(1, 2, figsize=(12.4, 6.6), sharey=True)
    fig.patch.set_facecolor("white")

    for ax, (outcome, exposure, title, subtitle, xlim) in zip(axes, PANELS):
        ys = list(range(len(SCENARIOS)))[::-1]
        for y, (scen, label) in zip(ys, SCENARIOS):
            rec = data[(outcome, exposure, scen)]
            excludes = not (rec["lo"] <= 1.0 <= rec["hi"])
            color = "#1F4E79" if excludes else "#7A7A7A"
            display = fmt_ci(rec["rr"], rec["lo"], rec["hi"])
            ax.plot([rec["lo"], rec["hi"]], [y, y], color=color, lw=2.0, solid_capstyle="butt")
            ax.plot(rec["rr"], y, "o", color=color, ms=7, zorder=3)
            ax.text(
                rec["hi"] + (xlim[1] - xlim[0]) * 0.012,
                y,
                display,
                va="center",
                fontsize=7.2,
                color=color,
            )
            quoted.append(
                {
                    "outcome": outcome,
                    "exposure": exposure,
                    "scenario": scen,
                    "label": label,
                    "rr": rec["rr"],
                    "rr_low": rec["lo"],
                    "rr_high": rec["hi"],
                    "display": display,
                    "interval": "excludes 1" if excludes else "includes 1",
                    "n_months": rec["n"],
                    "residual_acf1": rec["acf1"],
                    "data_status": rec["data_status"],
                }
            )
        ax.axvline(1.0, color="#444444", ls="--", lw=0.9)
        ax.set_title(title, loc="left", fontsize=11, fontweight="bold", pad=8)
        ax.text(0.0, 1.02, subtitle, transform=ax.transAxes, fontsize=8, color="#333333", va="bottom")
        ax.set_yticks(ys)
        ax.set_yticklabels([lab for _, lab in SCENARIOS], fontsize=8.5)
        ax.set_xlabel("Count ratio (Newey–West lag-6 95% CI)")
        ax.set_xlim(*xlim)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="x", color="#EEEEEE", lw=0.8)

    legend = [
        Line2D([0], [0], color="#1F4E79", marker="o", lw=2, label="95% CI excludes 1"),
        Line2D([0], [0], color="#7A7A7A", marker="o", lw=2, label="95% CI includes 1"),
    ]
    axes[1].legend(handles=legend, loc="lower right", frameon=False, fontsize=8)
    fig.suptitle(
        "Teaching read of live-manuscript Figure 3: spline df is a time-trend control, not a heatwave duration",
        fontsize=12,
        fontweight="bold",
        y=0.98,
    )
    fig.text(
        0.5,
        0.01,
        "Source: outputs/tables/cvd_trend_depletion_sensitivity.csv (HA_APPROVED_AGGREGATE). "
        "No new health model. Gate 3 open. All twelve Model 1 q-values > 0.19.",
        ha="center",
        fontsize=7.5,
        color="#444444",
    )
    fig.tight_layout(rect=(0.02, 0.05, 0.99, 0.90))
    fig.savefig(PNG, dpi=160)
    plt.close(fig)

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(quoted[0].keys()))
        w.writeheader()
        w.writerows(quoted)
    print(f"wrote {PNG}")
    print(f"wrote {CSV_OUT}")


if __name__ == "__main__":
    main()
