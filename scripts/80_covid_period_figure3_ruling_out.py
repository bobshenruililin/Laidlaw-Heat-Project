#!/usr/bin/env python3
"""Rebuild the covid_period-only Figure 3 ruling-out exhibit.

Reads the same HA_APPROVED_AGGREGATE trend/window CSV as the live forest.
Fits no health model. Does not write under figures/live_identification/.

Colour encodes specification class (trend / nested overlapping refit /
full-sample COVID-phase intercepts), not whether a 95% interval excludes 1.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "outputs" / "tables" / "cvd_trend_depletion_sensitivity.csv"
LIVE_PNG = ROOT / "figures" / "live_identification" / "figure_D_trend_depletion_sensitivity.png"
FIG_DIR = ROOT / "figures" / "covid_period"
STEM = "figure_3_ruling_out_exhibit"
CONTRACT = FIG_DIR / "figure_3_ruling_out_contract.json"

TREND = "#174d5b"
NESTED = "#8A3E4C"
PHASE = "#3D5A80"
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

SCENARIOS: list[tuple[str, str, str]] = [
    ("baseline_ns4", "Model 1 (time-trend spline, 4 df)", "trend"),
    ("trend_ns3", "Time-trend spline, 3 df", "trend"),
    ("trend_ns6", "Time-trend spline, 6 df", "trend"),
    ("trend_ns8", "Time-trend spline, 8 df", "trend"),
    ("year_fixed_effects", "Year indicators", "trend"),
    ("pre_covid", "Nested 84-month overlapping refit", "nested"),
    ("covid_phase_adjusted", "COVID-phase intercept (full sample)", "phase"),
    ("drop_first_12_months", "Drop first 12 months", "trend"),
    ("drop_first_24_months", "Drop first 24 months", "trend"),
]

CLASS_COLOUR = {"trend": TREND, "nested": NESTED, "phase": PHASE}

OFFICIAL = [
    ("hot_nights", "Hot nights", "per 5 more official hot nights"),
    ("very_hot_days", "Very hot days", "per 5 more official very hot days"),
    ("cold_days", "Cold days", "per 5 more official cold days"),
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
    "COVID-period indicators",
    "Pre-2020 (Jan 2013–Dec 2019)",
    "95% CI excludes 1",
    "95% CI includes 1",
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


def _xlim(data: dict, exposure: str) -> tuple[float, float]:
    los: list[float] = []
    his: list[float] = []
    for outcome, _ in OUTCOMES:
        for scen, _lab, _cls in SCENARIOS:
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
        fontsize=6.2,
        color=SUB,
        va="center",
        ha="left",
        clip_on=False,
        zorder=5,
    )


def draw_grid(data: dict) -> Path:
    if FIG_DIR.resolve() == LIVE_PNG.parent.resolve():
        raise SystemExit("refusing to write into figures/live_identification/")

    n_scen = len(SCENARIOS)
    ys = list(range(n_scen - 1, -1, -1))

    fig = plt.figure(figsize=(WIDTH_IN, HEIGHT_IN))
    gs = GridSpec(
        2,
        3,
        figure=fig,
        left=0.318,
        right=0.985,
        top=0.76,
        bottom=0.105,
        wspace=0.16,
        hspace=0.38,
    )

    axes = [[fig.add_subplot(gs[r, c]) for c in range(3)] for r in range(2)]

    for c, (exposure, col_title, scale) in enumerate(OFFICIAL):
        xlim = _xlim(data, exposure)
        for r, (outcome, outcome_label) in enumerate(OUTCOMES):
            ax = axes[r][c]
            ax.set_xlim(*xlim)
            ax.set_ylim(-0.65, n_scen - 0.35)
            ax.axhspan(ys[0] - 0.45, ys[0] + 0.45, color=MODEL1_BAND, zorder=0)
            ax.axvline(1.0, color=VLINE, ls=(0, (3.2, 2.4)), lw=0.8, zorder=1)
            ax.set_yticks(ys)
            if c == 0:
                ax.set_yticklabels([lab for _, lab, _ in SCENARIOS], fontsize=6.7, color=TEXT)
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

            for y, (scen, _lab, cls) in zip(ys, SCENARIOS):
                rec = data[(outcome, exposure, scen)]
                colour = CLASS_COLOUR[cls]
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
                _draw_strip(ax, col_title, scale, title_size=7.6)

    fig.text(
        0.045,
        0.985,
        "Official-day Model 1 count ratios: trend, nested refit, intercepts",
        fontsize=9.4,
        fontweight="bold",
        color=TEXT,
        va="top",
    )
    fig.text(
        0.045,
        0.948,
        "Rows labelled 3, 6, or 8 df change the time-trend spline, not heatwave length.\n"
        "The scale is five additional official days in the month, not consecutive days.",
        fontsize=7.2,
        color=SUB,
        va="top",
        linespacing=1.28,
    )
    legend = [
        Line2D([0], [0], color=TREND, marker="o", ms=4.5, lw=1.4, label="Trend / sample-start"),
        Line2D([0], [0], color=NESTED, marker="o", ms=4.5, lw=1.4, label="Nested 84-month refit"),
        Line2D(
            [0],
            [0],
            color=PHASE,
            marker="o",
            ms=4.5,
            lw=1.4,
            label="COVID-phase intercepts",
        ),
    ]
    fig.legend(
        handles=legend,
        loc="upper right",
        bbox_to_anchor=(0.985, 0.988),
        frameon=False,
        fontsize=6.4,
        handlelength=1.6,
        borderaxespad=0,
        labelcolor=TEXT,
        ncol=1,
    )
    fig.text(
        0.045,
        0.018,
        "Health provenance: HA_APPROVED_AGGREGATE. Newey–West lag-6 95% intervals; "
        "days-in-month offset. Shaded row is Model 1 (4-df time-trend spline). "
        "Nested row is an overlapping-sample refit. COVID-phase row is a full-sample "
        "intercept adjustment, not a third window. Source: "
        "outputs/tables/cvd_trend_depletion_sensitivity.csv. No new health model.",
        fontsize=6.05,
        color=CAPTION,
        va="bottom",
        wrap=True,
    )

    FIG_DIR.mkdir(parents=True, exist_ok=True)
    png = FIG_DIR / f"{STEM}.png"
    fig.savefig(png, dpi=DPI)
    plt.close(fig)
    return png


def write_contract(png: Path) -> None:
    payload = {
        "figure3_png": str(png.relative_to(ROOT)),
        "live_source_png_untouched": str(LIVE_PNG.relative_to(ROOT)),
        "width_in": WIDTH_IN,
        "height_in": HEIGHT_IN,
        "dpi": DPI,
        "y_labels": [lab for _, lab, _ in SCENARIOS],
        "specification_class": {scen: cls for scen, _lab, cls in SCENARIOS},
        "class_colours": dict(CLASS_COLOUR),
        "official_column_titles": [f"{t} / {s}" for _, t, s in OFFICIAL],
        "legend_labels": [
            "Trend / sample-start",
            "Nested 84-month refit",
            "COVID-phase intercepts",
        ],
        "forbidden_in_figure": [
            "95% CI excludes 1",
            "95% CI includes 1",
            "Supplementary Figure S6",
            "COVID-period indicators",
            "Official-count Model 1 estimates: time-trend and window checks",
        ],
        "required_in_y_labels": [
            "Time-trend spline, 6 df",
            "Time-trend spline, 8 df",
            "Time-trend spline, 3 df",
            "Model 1 (time-trend spline, 4 df)",
            "Nested 84-month overlapping refit",
            "COVID-phase intercept (full sample)",
        ],
        "note": (
            "covid_period Figure 3 is a separate asset. "
            "It must not overwrite figures/live_identification/."
        ),
    }
    CONTRACT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    live_before = LIVE_PNG.read_bytes() if LIVE_PNG.is_file() else b""
    _register_fonts()
    data = load_rows()
    for _, lab, _cls in SCENARIOS:
        for bad in FORBIDDEN_LABELS:
            if lab == bad or lab.startswith("Spline df"):
                raise SystemExit(f"forbidden y-label {lab!r}")
    png = draw_grid(data)
    if png.resolve() == LIVE_PNG.resolve():
        raise SystemExit("refusing to overwrite the live Figure 3 PNG")
    write_contract(png)
    live_after = LIVE_PNG.read_bytes() if LIVE_PNG.is_file() else b""
    if live_before != live_after:
        raise SystemExit("live Figure 3 PNG changed; abort")
    print(f"wrote {png}")
    print(f"wrote {CONTRACT}")
    print(f"live PNG unchanged: {LIVE_PNG}")


if __name__ == "__main__":
    main()
