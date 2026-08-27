#!/usr/bin/env python3
"""Rebuild live-manuscript Figure 3 (and Supplementary Figure S6).

Reads existing HA_APPROVED_AGGREGATE trend/window estimates. Fits no health model.
Does not touch outputs/release_chd_hf/figures/figure4_*.

Live Figure 3 is no longer a copy of the 15 x 8 in release figure. It is a
portrait 2 x 3 official-count forest whose y-axis names time-trend spline df
and whose strips name five additional official days in the month.

Supplementary Figure S6 holds the three continuous-temperature columns so the
pre-2020 inverse-T pattern is not hidden.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "outputs" / "tables" / "cvd_trend_depletion_sensitivity.csv"
FIG_DIR = ROOT / "figures" / "live_identification"
CONTRACT = FIG_DIR / "figure_D_relabel_contract.json"

# Match live-identification house colours (figure_B / release teal).
TEAL = "#174d5b"
GREY = "#7A8087"
TEXT = "#202124"
SUB = "#42464B"
CAPTION = "#5F6368"
GRID = "#EEF0F2"
STRIP = "#E8EAED"
VLINE = "#9AA0A6"
MODEL1_BAND = "#F3F5F6"
SPINE = "#303236"

WIDTH_IN = 6.20
HEIGHT_IN = 7.35
DPI = 320

SCENARIOS: list[tuple[str, str]] = [
    ("baseline_ns4", "Model 1 (time-trend spline, 4 df)"),
    ("trend_ns3", "Time-trend spline, 3 df"),
    ("trend_ns6", "Time-trend spline, 6 df"),
    ("trend_ns8", "Time-trend spline, 8 df"),
    ("year_fixed_effects", "Year indicators"),
    ("pre_covid", "Pre-2020 (Jan 2013–Dec 2019)"),
    ("covid_phase_adjusted", "COVID-period indicators"),
    ("drop_first_12_months", "Drop first 12 months"),
    ("drop_first_24_months", "Drop first 24 months"),
]

OFFICIAL = [
    ("hot_nights", "Hot nights", "per 5 extra days in month"),
    ("very_hot_days", "Very hot days", "per 5 extra days in month"),
    ("cold_days", "Cold days", "per 5 extra days in month"),
]
CONTINUOUS = [
    ("mean_temp", "Mean temperature", "per 1 °C"),
    ("mean_tmax", "Mean maximum temperature", "per 1 °C"),
    ("mean_tmin", "Mean minimum temperature", "per 1 °C"),
]
OUTCOMES = [("chd", "Coronary heart disease"), ("hf", "Heart failure")]

FORBIDDEN_LABELS = (
    "Spline df 3",
    "Spline df 6",
    "Spline df 8",
    "Spline df",
    "Pre-COVID",
    "per 5 days",
    "Baseline: spline df 4",
)


def _register_fonts() -> None:
    for path in (
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf",
    ):
        p = Path(path)
        if p.is_file():
            font_manager.fontManager.addfont(str(p))
    plt.rcParams.update(
        {
            "font.family": "Liberation Sans",
            "font.size": 8.0,
            "axes.unicode_minus": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "savefig.dpi": DPI,
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
        }
    )


def load_rows() -> dict[tuple[str, str, str], dict]:
    out: dict[tuple[str, str, str], dict] = {}
    with SRC.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row["data_status"] != "HA_APPROVED_AGGREGATE":
                raise SystemExit(f"unexpected data_status {row['data_status']!r}")
            key = (row["outcome"], row["exposure"], row["scenario"])
            out[key] = {
                "rr": float(row["rr"]),
                "lo": float(row["rr_low"]),
                "hi": float(row["rr_high"]),
                "n": int(row["n_months"]),
            }
    expected = 2 * 6 * 9
    if len(out) != expected:
        raise SystemExit(f"expected {expected} rows, got {len(out)}")
    return out


def _excludes(lo: float, hi: float) -> bool:
    return not (lo <= 1.0 <= hi)


def _xlim(data: dict, exposure: str) -> tuple[float, float]:
    los: list[float] = []
    his: list[float] = []
    for outcome, _ in OUTCOMES:
        for scen, _ in SCENARIOS:
            rec = data[(outcome, exposure, scen)]
            los.append(rec["lo"])
            his.append(rec["hi"])
    lo, hi = min(los), max(his)
    pad = max(0.012, 0.08 * (hi - lo))
    return lo - pad, hi + pad


def _draw_strip(ax, title: str, scale: str, title_size: float = 7.6) -> None:
    ax.add_patch(
        FancyBboxPatch(
            (0.0, 1.0),
            1.0,
            0.22,
            boxstyle="square,pad=0",
            transform=ax.transAxes,
            facecolor=STRIP,
            edgecolor="none",
            clip_on=False,
            zorder=4,
        )
    )
    ax.text(
        0.03,
        1.155,
        title,
        transform=ax.transAxes,
        fontsize=title_size,
        fontweight="bold",
        color=TEXT,
        va="center",
        ha="left",
        clip_on=False,
        zorder=5,
    )
    ax.text(
        0.03,
        1.055,
        scale,
        transform=ax.transAxes,
        fontsize=6.6,
        color=SUB,
        va="center",
        ha="left",
        clip_on=False,
        zorder=5,
    )


def draw_grid(
    data: dict,
    columns: list[tuple[str, str, str]],
    *,
    title: str,
    subtitle: str,
    caption: str,
    stem: str,
    strip_title_size: float = 7.6,
) -> Path:
    n_scen = len(SCENARIOS)
    ys = list(range(n_scen - 1, -1, -1))  # Model 1 at top

    fig = plt.figure(figsize=(WIDTH_IN, HEIGHT_IN))
    gs = GridSpec(
        2,
        3,
        figure=fig,
        left=0.305,
        right=0.985,
        top=0.78,
        bottom=0.105,
        wspace=0.16,
        hspace=0.38,
    )

    axes = [[fig.add_subplot(gs[r, c]) for c in range(3)] for r in range(2)]

    for c, (exposure, col_title, scale) in enumerate(columns):
        xlim = _xlim(data, exposure)
        for r, (outcome, outcome_label) in enumerate(OUTCOMES):
            ax = axes[r][c]
            ax.set_xlim(*xlim)
            ax.set_ylim(-0.65, n_scen - 0.35)
            ax.axhspan(ys[0] - 0.45, ys[0] + 0.45, color=MODEL1_BAND, zorder=0)
            ax.axvline(1.0, color=VLINE, ls=(0, (3.2, 2.4)), lw=0.8, zorder=1)
            ax.set_yticks(ys)
            if c == 0:
                ax.set_yticklabels([lab for _, lab in SCENARIOS], fontsize=7.05, color=TEXT)
                ax.set_ylabel(
                    outcome_label,
                    fontsize=8.2,
                    fontweight="bold",
                    color=TEXT,
                    labelpad=7,
                )
            else:
                ax.set_yticklabels([])
                ax.set_ylabel("")
            ax.tick_params(axis="x", labelsize=6.4, colors=TEXT, length=2.5, width=0.5)
            ax.tick_params(axis="y", length=0)
            ax.grid(axis="y", color=GRID, lw=0.6, zorder=0)
            ax.grid(axis="x", visible=False)
            for spine in ("top", "right"):
                ax.spines[spine].set_visible(False)
            ax.spines["left"].set_color(SPINE)
            ax.spines["bottom"].set_color(SPINE)
            ax.spines["left"].set_linewidth(0.6)
            ax.spines["bottom"].set_linewidth(0.6)
            if r == 1:
                ax.set_xlabel("Count ratio", fontsize=7.2, color=SPINE, labelpad=3)
            else:
                ax.set_xlabel("")

            for y, (scen, _lab) in zip(ys, SCENARIOS):
                rec = data[(outcome, exposure, scen)]
                colour = TEAL if _excludes(rec["lo"], rec["hi"]) else GREY
                ax.plot(
                    [rec["lo"], rec["hi"]],
                    [y, y],
                    color=colour,
                    lw=1.35,
                    solid_capstyle="butt",
                    zorder=2,
                )
                ax.plot(
                    rec["rr"],
                    y,
                    "o",
                    color=colour,
                    ms=3.7,
                    zorder=3,
                    markeredgewidth=0,
                )

            if r == 0:
                _draw_strip(ax, col_title, scale, title_size=strip_title_size)

    fig.text(0.045, 0.985, title, fontsize=9.6, fontweight="bold", color=TEXT, va="top")
    fig.text(
        0.045,
        0.945,
        subtitle,
        fontsize=7.2,
        color=SUB,
        va="top",
        linespacing=1.28,
    )
    legend = [
        Line2D([0], [0], color=TEAL, marker="o", ms=4.5, lw=1.4, label="95% CI excludes 1"),
        Line2D([0], [0], color=GREY, marker="o", ms=4.5, lw=1.4, label="95% CI includes 1"),
    ]
    fig.legend(
        handles=legend,
        loc="upper right",
        bbox_to_anchor=(0.985, 0.985),
        frameon=False,
        fontsize=6.6,
        handlelength=1.6,
        borderaxespad=0,
        labelcolor=TEXT,
    )
    fig.text(0.045, 0.018, caption, fontsize=6.15, color=CAPTION, va="bottom", wrap=True)

    png = FIG_DIR / f"{stem}.png"
    pdf = FIG_DIR / f"{stem}.pdf"
    fig.savefig(png, dpi=DPI)
    fig.savefig(pdf)
    plt.close(fig)
    return png


def write_contract(official_png: Path, supp_png: Path) -> None:
    y_labels = [lab for _, lab in SCENARIOS]
    col_titles = [f"{t} / {s}" for _, t, s in OFFICIAL]
    payload = {
        "figure3_png": str(official_png.relative_to(ROOT)),
        "figure_s6_png": str(supp_png.relative_to(ROOT)),
        "width_in": WIDTH_IN,
        "height_in": HEIGHT_IN,
        "dpi": DPI,
        "y_labels": y_labels,
        "official_column_titles": col_titles,
        "continuous_column_titles": [f"{t} / {s}" for _, t, s in CONTINUOUS],
        "required_in_y_labels": [
            "Time-trend spline, 6 df",
            "Time-trend spline, 8 df",
            "Time-trend spline, 3 df",
            "Model 1 (time-trend spline, 4 df)",
            "Pre-2020 (Jan 2013–Dec 2019)",
        ],
        "required_in_official_columns": ["per 5 extra days in month"],
        "forbidden_labels": list(FORBIDDEN_LABELS),
        "note": "Live Figure 3 is not a copy of release figure4_trend_depletion_sensitivity.",
    }
    CONTRACT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    _register_fonts()
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    data = load_rows()
    for _, lab in SCENARIOS:
        for bad in FORBIDDEN_LABELS:
            if lab == bad or lab.startswith("Spline df"):
                raise SystemExit(f"forbidden y-label {lab!r}")

    fig3 = draw_grid(
        data,
        OFFICIAL,
        title="Official-count Model 1 estimates: time-trend and window checks",
        subtitle=(
            "Rows labelled 3, 6, or 8 df change the time-trend spline, not heatwave length.\n"
            "The scale is five additional official days in the month, not consecutive days."
        ),
        caption=(
            "Health provenance: HA_APPROVED_AGGREGATE. Newey–West lag-6 95% intervals; "
            "days-in-month offset. Shaded row is Model 1 (4-df time-trend spline). "
            "Continuous-temperature fits for the same nine specifications are Supplementary Figure S6. "
            "Source: outputs/tables/cvd_trend_depletion_sensitivity.csv. No new health model."
        ),
        stem="figure_D_trend_depletion_sensitivity",
    )
    s6 = draw_grid(
        data,
        CONTINUOUS,
        title="Continuous-temperature Model 1 estimates: same nine checks",
        subtitle=(
            "Same specifications as main-text Figure 3. Each estimate is per 1 °C.\n"
            "Pre-2020 inverse associations for mean, maximum, and minimum temperature are in this panel."
        ),
        caption=(
            "Health provenance: HA_APPROVED_AGGREGATE. Newey–West lag-6 95% intervals; "
            "days-in-month offset. Shaded row is Model 1 (4-df time-trend spline). "
            "Source: outputs/tables/cvd_trend_depletion_sensitivity.csv. No new health model."
        ),
        stem="figure_E_continuous_temperature_sensitivity",
        strip_title_size=6.5,
    )
    write_contract(fig3, s6)
    print(f"wrote {fig3}")
    print(f"wrote {s6}")
    print(f"wrote {CONTRACT}")


if __name__ == "__main__":
    main()
