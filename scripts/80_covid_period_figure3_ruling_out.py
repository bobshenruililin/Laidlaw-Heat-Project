#!/usr/bin/env python3
"""Build the two covid_period thesis figures.

Figure 1 is the first-event count path (object 1).
Figure 2 is nested-84 versus full-132 official-day count ratios (object 2:
ruling-out exhibit). Neither graphic is a leftover thermal-identification forest.

Reads parked HA_APPROVED_AGGREGATE CSVs. Fits no health model. Does not write
under figures/live_identification/. Colour encodes the analysis window, not
whether a 95% interval excludes 1.

Aspect ratios are landscape so script 78 can print them at full A4 column
width (~6.1 in) instead of shrinking a tall canvas into a postage stamp.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
ANNUAL = ROOT / "outputs" / "tables" / "cvd_descriptive_annual_totals.csv"
SRC = ROOT / "outputs" / "tables" / "cvd_trend_depletion_sensitivity.csv"
LIVE_PNG = ROOT / "figures" / "live_identification" / "figure_D_trend_depletion_sensitivity.png"
LIVE_FIG1 = ROOT / "figures" / "live_identification" / "figure_B_first_event_depletion.png"
LIVE_FIG2 = ROOT / "figures" / "live_identification" / "figure_A_cold_day_identification.png"
FIG_DIR = ROOT / "figures" / "covid_period"
FIG1_STEM = "figure_1_count_path"
FIG2_STEM = "figure_2_nested_vs_full"
CONTRACT = FIG_DIR / "figure_3_ruling_out_contract.json"

TEAL = "#174d5b"
NESTED = "#8A3E4C"
GREY = "#6C737A"
TEXT = "#202124"
SUB = "#42464B"
CAPTION = "#5F6368"
GRID = "#EEF0F2"
VLINE = "#9AA0A6"
SPINE = "#303236"
SHADE = "#F4E6E8"
STRIP = "#E8EAED"

DPI = 320
COL_WIDTH_IN = 6.10
FIG1_MAX_H = 5.35
FIG2_MAX_H = 7.00

# Landscape canvases: printed width stays at the A4 column unless height exceeds the cap.
FIG1_SIZE = (6.30, 5.12)
FIG2_SIZE = (6.30, 6.55)

OFFICIAL = [
    ("hot_nights", "Hot nights"),
    ("very_hot_days", "Very hot days"),
    ("cold_days", "Cold days"),
]
OUTCOMES = [("chd", "Coronary heart disease"), ("hf", "Heart failure")]
WINDOWS = [
    ("pre_covid", "Nested 84 months", NESTED),
    ("baseline_ns4", "Full 132 months", TEAL),
]

FORBIDDEN_LABELS = (
    "95% CI excludes 1",
    "95% CI includes 1",
    "Pre-COVID",
    "Spline df",
    "per 5 days",
    "Supplementary Figure S6",
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
            "font.size": 9.0,
            "axes.unicode_minus": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "savefig.dpi": DPI,
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
        }
    )


def _printed_width(size_in: tuple[float, float], max_height: float) -> float:
    width, height = size_in
    natural_height = COL_WIDTH_IN * height / width
    if natural_height > max_height:
        return max_height * width / height
    return COL_WIDTH_IN


def _assert_full_column(stem: str, size_in: tuple[float, float], max_height: float) -> None:
    printed = _printed_width(size_in, max_height)
    if printed < 5.90:
        raise SystemExit(
            f"{stem} would print only {printed:.2f} in wide under a {max_height} in "
            f"height cap (canvas {size_in[0]:.2f} x {size_in[1]:.2f}). "
            "Flatten the canvas; do not ship a postage stamp."
        )


def load_annual() -> dict[str, dict[int, tuple[int, float]]]:
    out: dict[str, dict[int, tuple[int, float]]] = {"chd": {}, "hf": {}}
    with ANNUAL.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row["data_status"] != "HA_APPROVED_AGGREGATE":
                raise SystemExit(f"unexpected data_status {row['data_status']!r}")
            out[row["outcome"]][int(row["year"])] = (
                int(row["total_events"]),
                float(row["mean_population"]),
            )
    years = list(range(2013, 2024))
    if set(out["chd"]) != set(years) or set(out["hf"]) != set(years):
        raise SystemExit("annual table is missing years")
    return out


def load_official() -> dict[tuple[str, str, str], dict]:
    out: dict[tuple[str, str, str], dict] = {}
    with SRC.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row["data_status"] != "HA_APPROVED_AGGREGATE":
                raise SystemExit(f"unexpected data_status {row['data_status']!r}")
            if row["exposure"] not in {name for name, _ in OFFICIAL}:
                continue
            if row["scenario"] not in {scen for scen, _lab, _c in WINDOWS}:
                continue
            out[(row["outcome"], row["exposure"], row["scenario"])] = {
                "rr": float(row["rr"]),
                "lo": float(row["rr_low"]),
                "hi": float(row["rr_high"]),
                "n": int(row["n_months"]),
            }
    expected = 2 * 3 * 2
    if len(out) != expected:
        raise SystemExit(f"expected {expected} official-day rows, got {len(out)}")
    return out


def _fmt_rr(rec: dict) -> str:
    return f"{rec['rr']:.3f} ({rec['lo']:.3f}–{rec['hi']:.3f})"


def draw_figure1(annual: dict) -> Path:
    years = list(range(2013, 2024))
    chd = [annual["chd"][y][0] for y in years]
    hf = [annual["hf"][y][0] for y in years]
    pop = [annual["chd"][y][1] for y in years]

    fig, axes = plt.subplots(
        3,
        1,
        figsize=FIG1_SIZE,
        sharex=True,
        gridspec_kw={"height_ratios": [1.15, 1.05, 0.90], "hspace": 0.28},
    )
    fig.subplots_adjust(left=0.12, right=0.98, top=0.86, bottom=0.145)

    series = [
        (axes[0], chd, "CHD first hospitalisations (annual total)", TEAL, "{:,.0f}"),
        (axes[1], hf, "HF first hospitalisations (annual total)", NESTED, "{:,.0f}"),
        (
            axes[2],
            [v / 1e6 for v in pop],
            "Census population aged 35+ (millions; not the still-at-risk set)",
            GREY,
            "{:.2f}",
        ),
    ]
    callouts = {
        0: {2013: chd[0], 2019: chd[6], 2020: chd[7], 2023: chd[10]},
        1: {2013: hf[0], 2019: hf[6], 2020: hf[7], 2023: hf[10]},
        2: {2013: pop[0] / 1e6, 2023: pop[10] / 1e6},
    }
    offsets = {
        2013: (7, 7),
        2019: (-6, 9),
        2020: (5, -13),
        2023: (-52, 8),
    }

    for idx, (ax, ys, title, color, fmt) in enumerate(series):
        ax.axvspan(2019.5, 2023.4, color=SHADE, zorder=0)
        ax.axvline(2019.5, color=NESTED, ls=(0, (3.2, 2.0)), lw=1.0, zorder=1)
        ax.plot(years, ys, color=color, lw=2.15, marker="o", ms=6.2, zorder=3)
        ax.set_ylabel("")
        ax.set_title(title, loc="left", fontsize=10.2, color=TEXT, fontweight="bold", pad=4)
        ax.set_xticks(years)
        ax.tick_params(labelsize=8.4, colors=TEXT, length=3, width=0.6)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(SPINE)
        ax.spines["bottom"].set_color(SPINE)
        ax.grid(axis="y", color=GRID, lw=0.7, zorder=0)
        ax.set_axisbelow(True)
        lo, hi = min(ys), max(ys)
        pad = 0.12 * (hi - lo)
        ax.set_ylim(lo - pad, hi + pad)
        ax.set_xlim(2012.6, 2023.4)
        for year, value in callouts[idx].items():
            dx, dy = offsets[year]
            if idx == 2 and year == 2013:
                dx, dy = (8, 8)
            if idx == 2 and year == 2023:
                dx, dy = (-8, 10)
            ax.annotate(
                fmt.format(value),
                (year, value),
                textcoords="offset points",
                xytext=(dx, dy),
                fontsize=7.8,
                color=color,
                fontweight="bold",
                clip_on=False,
                ha="left" if dx >= 0 else "left",
            )

    axes[2].set_xticklabels([str(y) for y in years], rotation=0)
    axes[0].text(
        2021.45,
        axes[0].get_ylim()[1] - 0.08 * (axes[0].get_ylim()[1] - axes[0].get_ylim()[0]),
        "Later years in the\n132-month window only",
        ha="center",
        va="top",
        fontsize=7.6,
        color=NESTED,
    )

    fig.text(
        0.12,
        0.975,
        "First-event counts fell while the general population aged 35+ rose",
        fontsize=12.0,
        fontweight="bold",
        color=TEXT,
        va="top",
    )
    fig.text(
        0.12,
        0.928,
        "Most of the decline was already present by 2019. 2020 was a trough. 2023 returned toward 2019, not 2013.",
        fontsize=8.4,
        color=SUB,
        va="top",
    )
    fig.text(
        0.12,
        0.018,
        "Health provenance: HA_APPROVED_AGGREGATE annual totals. Population: C&SD Table 110-01001, "
        "already stored on that table; not the diabetes or hypertension still-at-risk set. "
        "Dashed line marks the nested 84-month window (January 2013–December 2019). "
        "Not incidence. Not physiology. Not consecutive duration.",
        fontsize=6.6,
        color=CAPTION,
        va="bottom",
        wrap=True,
    )

    FIG_DIR.mkdir(parents=True, exist_ok=True)
    png = FIG_DIR / f"{FIG1_STEM}.png"
    fig.savefig(png, dpi=DPI)
    plt.close(fig)
    return png


def _xlim_for(data: dict, outcome: str, exposure: str) -> tuple[float, float]:
    los = []
    his = []
    for scen, _lab, _c in WINDOWS:
        rec = data[(outcome, exposure, scen)]
        los.append(rec["lo"])
        his.append(rec["hi"])
    lo, hi = min(los), max(his)
    pad = max(0.022, 0.22 * (hi - lo))
    return lo - pad, hi + pad


def draw_figure2(data: dict) -> Path:
    fig, axes = plt.subplots(3, 2, figsize=FIG2_SIZE, sharey=True)
    fig.subplots_adjust(left=0.22, right=0.985, top=0.88, bottom=0.12, wspace=0.16, hspace=0.36)

    ys = [1.0, 0.0]
    y_labels = [lab for _s, lab, _c in WINDOWS]
    for col, (outcome, outcome_label) in enumerate(OUTCOMES):
        for row, (exposure, exp_label) in enumerate(OFFICIAL):
            ax = axes[row][col]
            xlim = _xlim_for(data, outcome, exposure)
            ax.set_xlim(*xlim)
            ax.set_ylim(-0.42, 1.45)
            ax.axvline(1.0, color=VLINE, ls=(0, (3.2, 2.4)), lw=1.1, zorder=1)
            ax.set_yticks(ys)
            ax.tick_params(axis="x", labelsize=8.6, colors=TEXT, length=3.2, width=0.55)
            ax.tick_params(axis="y", length=0, labelleft=False)
            ax.grid(axis="y", color=GRID, lw=0.7, zorder=0)
            for spine in ("top", "right"):
                ax.spines[spine].set_visible(False)
            ax.spines["left"].set_color(SPINE)
            ax.spines["bottom"].set_color(SPINE)
            ax.spines["left"].set_linewidth(0.7)
            ax.spines["bottom"].set_linewidth(0.7)
            if row == 2:
                ax.set_xlabel("")
            else:
                ax.set_xlabel("")

            ax.add_patch(
                FancyBboxPatch(
                    (0.0, 1.0),
                    1.0,
                    0.18,
                    boxstyle="square,pad=0",
                    transform=ax.transAxes,
                    facecolor=STRIP,
                    edgecolor="none",
                    clip_on=False,
                    zorder=4,
                )
            )
            header = f"{outcome_label} · {exp_label}" if row == 0 else exp_label
            ax.text(
                0.03,
                1.09,
                header,
                transform=ax.transAxes,
                fontsize=9.2,
                fontweight="bold",
                color=TEXT,
                va="center",
                ha="left",
                clip_on=False,
                zorder=5,
            )

            for y, (scen, _lab, colour) in zip(ys, WINDOWS):
                rec = data[(outcome, exposure, scen)]
                ax.plot(
                    [rec["lo"], rec["hi"]],
                    [y, y],
                    color=colour,
                    lw=2.8,
                    solid_capstyle="butt",
                    zorder=2,
                )
                ax.plot(
                    rec["rr"],
                    y,
                    "o",
                    color=colour,
                    ms=8.0,
                    zorder=3,
                    markeredgewidth=0,
                )

    for row in range(3):
        axes[row][0].tick_params(axis="y", labelleft=True, length=0)
        axes[row][0].set_yticks(ys)
        axes[row][0].set_yticklabels(y_labels, fontsize=9.6, color=TEXT)

    fig.text(
        0.02,
        0.985,
        "Official-day count ratios: nested 84 months versus full 132 months",
        fontsize=11.4,
        fontweight="bold",
        color=TEXT,
        va="top",
    )
    fig.text(
        0.02,
        0.948,
        "Overlapping-sample refit; 4-df spline re-knotted on the subset. Not a pre/post effect.\n"
        "Maroon = nested 84 months. Teal = full 132 months.",
        fontsize=8.1,
        color=SUB,
        va="top",
    )
    fig.text(
        0.60,
        0.078,
        "Count ratio per five additional official days",
        fontsize=8.6,
        color=SPINE,
        ha="center",
        va="top",
    )
    fig.text(
        0.02,
        0.018,
        "Health provenance: HA_APPROVED_AGGREGATE. Newey–West lag-6 95% intervals; days-in-month offset. "
        "Colour marks the analysis window, not whether an interval excludes 1. "
        "I(count/5) is a reporting scale. Numerals are in Table 2.",
        fontsize=6.6,
        color=CAPTION,
        va="bottom",
        wrap=True,
    )

    png = FIG_DIR / f"{FIG2_STEM}.png"
    fig.savefig(png, dpi=DPI)
    plt.close(fig)
    return png


def write_contract(fig1: Path, fig2: Path) -> None:
    payload = {
        "figure1_png": str(fig1.relative_to(ROOT)),
        "figure2_png": str(fig2.relative_to(ROOT)),
        "figure3_png": None,
        "dropped_from_main": [
            "figures/live_identification/figure_A_cold_day_identification.png",
            "figures/live_identification/figure_B_first_event_depletion.png",
            "figures/covid_period/figure_3_ruling_out_exhibit.png",
        ],
        "live_source_png_untouched": str(LIVE_PNG.relative_to(ROOT)),
        "figure1_size_in": list(FIG1_SIZE),
        "figure2_size_in": list(FIG2_SIZE),
        "dpi": DPI,
        "printed_width_in": {
            "figure1": round(_printed_width(FIG1_SIZE, FIG1_MAX_H), 3),
            "figure2": round(_printed_width(FIG2_SIZE, FIG2_MAX_H), 3),
        },
        "y_labels": [lab for _s, lab, _c in WINDOWS],
        "legend_labels": [
            "Nested 84 months (2013–2019)",
            "Full 132 months (2013–2023)",
        ],
        "class_colours": {"nested": NESTED, "full": TEAL},
        "forbidden_in_figure": [
            "95% CI excludes 1",
            "95% CI includes 1",
            "Supplementary Figure S6",
            "COVID-period indicators",
            "Official-count Model 1 estimates: time-trend and window checks",
        ],
        "required_in_y_labels": ["Nested 84 months", "Full 132 months"],
        "note": (
            "covid_period Figures 1 and 2 are separate assets. "
            "They must not overwrite figures/live_identification/. "
            "The 9-specification official-day forest is not a main-text figure."
        ),
    }
    CONTRACT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    live_before = {
        path: path.read_bytes() if path.is_file() else b""
        for path in (LIVE_PNG, LIVE_FIG1, LIVE_FIG2)
    }
    _register_fonts()
    _assert_full_column(FIG1_STEM, FIG1_SIZE, FIG1_MAX_H)
    _assert_full_column(FIG2_STEM, FIG2_SIZE, FIG2_MAX_H)
    fig1 = draw_figure1(load_annual())
    fig2 = draw_figure2(load_official())
    write_contract(fig1, fig2)
    stale = FIG_DIR / "figure_3_ruling_out_exhibit.png"
    if stale.is_file():
        stale.unlink()
    for path, before in live_before.items():
        after = path.read_bytes() if path.is_file() else b""
        if before != after:
            raise SystemExit(f"live identification PNG changed: {path}")
    labels = " | ".join(WINDOWS[0][1] + WINDOWS[1][1])
    for bad in FORBIDDEN_LABELS:
        if bad in labels:
            raise SystemExit(f"forbidden label {bad!r}")
    print(f"wrote {fig1}")
    print(f"wrote {fig2}")
    print(f"wrote {CONTRACT}")
    print("live identification PNGs unchanged")


if __name__ == "__main__":
    main()
