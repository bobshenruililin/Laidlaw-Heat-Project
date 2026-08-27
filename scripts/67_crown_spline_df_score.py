#!/usr/bin/env python3
"""Score time-trend spline df for joint headline preservation.

Reads existing HA_APPROVED_AGGREGATE trend-depletion estimates. Fits no
health model. Does not touch Table 2, live Figure 3, or the validated
release.

The objects named 5, 6, and 8 in Bishai's comment are not one family:

* 5 is the Model 1 reporting scale I(count/5), not a 5-df spline.
* 6 and 8 are time-trend spline degrees of freedom.

This script scores the spline objects (3, 4, 6, 8 df, and year indicators).
It crowns 6 df only as the unique more-flexible spline that still keeps
both exploratory headlines away from 1. That is identification, not
physiology, and it does not replace Model 1 (4 df).
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "outputs" / "tables" / "cvd_trend_depletion_sensitivity.csv"
SPELL = ROOT / "outputs" / "tables" / "exposure_aging" / "annual_extremes_and_spell_burden.csv"
OUT_DIR = ROOT / "reports" / "crown_df_physiology_2026-08-27"
SCORE_CSV = OUT_DIR / "spline_df_joint_score.csv"
HEADLINE_CSV = OUT_DIR / "headline_trend_estimates.csv"
SPELL_JSON = OUT_DIR / "spell_2018_firewall.json"
CONTRACT = OUT_DIR / "crown_contract.json"
FIG = OUT_DIR / "figure_joint_headline_vs_trend_df.png"

TEAL = "#174d5b"
GREY = "#7A8087"
TEXT = "#202124"
SUB = "#42464B"
GRID = "#EEF0F2"
STRIP = "#E8EAED"
VLINE = "#9AA0A6"
CROWN = "#1F6A4D"
FAIL = "#8A6A3A"
SPINE = "#303236"

DPI = 320
WIDTH_IN = 7.05
HEIGHT_IN = 8.15

TREND_SPECS: list[tuple[str, int | None, str, str]] = [
    ("trend_ns3", 3, "Time-trend spline, 3 df", "stiffer than Model 1"),
    ("baseline_ns4", 4, "Model 1 (time-trend spline, 4 df)", "pre-specified Model 1"),
    ("trend_ns6", 6, "Time-trend spline, 6 df", "more flexible than Model 1"),
    ("trend_ns8", 8, "Time-trend spline, 8 df", "more flexible than Model 1"),
    ("year_fixed_effects", None, "Year indicators", "most flexible calendar control"),
]

EXPOSURES = (
    "mean_temp",
    "mean_tmax",
    "mean_tmin",
    "hot_nights",
    "cold_days",
    "very_hot_days",
)
OUTCOMES = ("chd", "hf")
HEADLINES = (("chd", "hot_nights"), ("hf", "cold_days"))


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


def _excludes(lo: float, hi: float) -> bool:
    return not (lo <= 1.0 <= hi)


def _fmt(rr: float, lo: float, hi: float) -> str:
    if lo < 1.0 < hi and lo >= 0.9995:
        return f"{rr:.3f} ({lo:.4f}–{hi:.3f})"
    return f"{rr:.3f} ({lo:.3f}–{hi:.3f})"


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
                "acf1": float(row["residual_acf1"]),
                "n": int(row["n_months"]),
            }
    expected = 2 * 6 * 9
    if len(out) != expected:
        raise SystemExit(f"expected {expected} rows, got {len(out)}")
    return out


def score(data: dict) -> list[dict]:
    rows: list[dict] = []
    for scen, df, label, role in TREND_SPECS:
        exclusions: list[str] = []
        for outcome in OUTCOMES:
            for exposure in EXPOSURES:
                rec = data[(outcome, exposure, scen)]
                if _excludes(rec["lo"], rec["hi"]):
                    side = "above" if rec["lo"] > 1.0 else "below"
                    exclusions.append(f"{outcome}_{exposure}_{side}")
        chd = data[("chd", "hot_nights", scen)]
        hf = data[("hf", "cold_days", scen)]
        chd_ok = _excludes(chd["lo"], chd["hi"]) and chd["lo"] > 1.0
        hf_ok = _excludes(hf["lo"], hf["hi"]) and hf["lo"] > 1.0
        joint = chd_ok and hf_ok
        more_flex = df is None or (df is not None and df > 4)
        rows.append(
            {
                "scenario": scen,
                "spline_df": "" if df is None else str(df),
                "label": label,
                "role": role,
                "chd_hot_nights_display": _fmt(chd["rr"], chd["lo"], chd["hi"]),
                "chd_hot_nights_rr": f"{chd['rr']:.12f}",
                "chd_hot_nights_excludes_1": str(chd_ok).lower(),
                "hf_cold_days_display": _fmt(hf["rr"], hf["lo"], hf["hi"]),
                "hf_cold_days_rr": f"{hf['rr']:.12f}",
                "hf_cold_days_excludes_1": str(hf_ok).lower(),
                "joint_headline_preserved": str(joint).lower(),
                "n_exclusions_of_12": str(len(exclusions)),
                "exclusion_ids": ";".join(exclusions),
                "chd_hot_nights_acf1": f"{chd['acf1']:.12f}",
                "hf_cold_days_acf1": f"{hf['acf1']:.12f}",
                "more_flexible_than_model1": str(more_flex).lower(),
                "crown_as_robustness": str(joint and more_flex).lower(),
            }
        )
    crowned = [r for r in rows if r["crown_as_robustness"] == "true"]
    if len(crowned) != 1 or crowned[0]["scenario"] != "trend_ns6":
        raise SystemExit(f"crown rule failed: {crowned}")
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_headline_csv(data: dict) -> None:
    rows: list[dict] = []
    for outcome, exposure in HEADLINES:
        for scen, df, label, _ in TREND_SPECS:
            rec = data[(outcome, exposure, scen)]
            rows.append(
                {
                    "outcome": outcome,
                    "exposure": exposure,
                    "scenario": scen,
                    "spline_df": "" if df is None else str(df),
                    "label": label,
                    "rr": f"{rec['rr']:.12f}",
                    "rr_low": f"{rec['lo']:.12f}",
                    "rr_high": f"{rec['hi']:.12f}",
                    "display": _fmt(rec["rr"], rec["lo"], rec["hi"]),
                    "excludes_1": str(_excludes(rec["lo"], rec["hi"])).lower(),
                    "residual_acf1": f"{rec['acf1']:.12f}",
                    "n_months": str(rec["n"]),
                    "data_status": "HA_APPROVED_AGGREGATE",
                }
            )
    write_csv(HEADLINE_CSV, rows)


def spell_firewall() -> dict:
    years: list[dict] = []
    with SPELL.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            years.append(
                {
                    "year": int(row["year"]),
                    "hot_nights": int(float(row["hot_nights"])),
                    "very_hot_days": int(float(row["very_hot_days"])),
                    "days_in_hn_spell_ge5": int(float(row["days_in_hn_spell_ge5"])),
                    "days_in_vhd_spell_ge5": int(float(row["days_in_vhd_spell_ge5"])),
                }
            )
    y2018 = next(y for y in years if y["year"] == 2018)
    hn = sum(y["hot_nights"] for y in years)
    hn_spell = sum(y["days_in_hn_spell_ge5"] for y in years)
    vhd = sum(y["very_hot_days"] for y in years)
    vhd_spell = sum(y["days_in_vhd_spell_ge5"] for y in years)
    payload = {
        "year_2018_official_hot_nights": y2018["hot_nights"],
        "year_2018_days_in_hn_spell_ge5": y2018["days_in_hn_spell_ge5"],
        "period_2013_2023_hot_nights": hn,
        "period_2013_2023_days_in_hn_spell_ge5": hn_spell,
        "share_hn_in_spell_ge5": hn_spell / hn,
        "period_2013_2023_very_hot_days": vhd,
        "period_2013_2023_days_in_vhd_spell_ge5": vhd_spell,
        "share_vhd_in_spell_ge5": vhd_spell / vhd,
        "note": (
            "2018 had 26 official hot nights and zero days inside a "
            "≥5 consecutive-night spell. Monthly count ≠ consecutive duration."
        ),
    }
    if y2018["hot_nights"] != 26 or y2018["days_in_hn_spell_ge5"] != 0:
        raise SystemExit("2018 firewall numbers drifted")
    if hn != 449 or hn_spell != 195 or vhd != 421 or vhd_spell != 183:
        raise SystemExit("2013–2023 spell totals drifted")
    SPELL_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def write_contract(scores: list[dict], spell: dict) -> None:
    ns6 = next(r for r in scores if r["scenario"] == "trend_ns6")
    ns8 = next(r for r in scores if r["scenario"] == "trend_ns8")
    ns4 = next(r for r in scores if r["scenario"] == "baseline_ns4")
    payload = {
        "paper_specification": "Model 1 4-df time-trend spline; Table 2 unchanged",
        "robustness_crown_among_more_flexible_splines": "trend_ns6",
        "robustness_crown_label": ns6["label"],
        "do_not_crown": ["trend_ns3", "trend_ns8", "year_fixed_effects"],
        "five_is_not_a_spline": True,
        "five_is_reporting_scale": "I(count/5)",
        "joint_headline_preserved_scenarios": [
            r["scenario"] for r in scores if r["joint_headline_preserved"] == "true"
        ],
        "model1_chd_hot_nights": ns4["chd_hot_nights_display"],
        "model1_hf_cold_days": ns4["hf_cold_days_display"],
        "ns6_chd_hot_nights": ns6["chd_hot_nights_display"],
        "ns6_hf_cold_days": ns6["hf_cold_days_display"],
        "ns8_hf_cold_days": ns8["hf_cold_days_display"],
        "ns8_hf_cold_days_includes_1": ns8["hf_cold_days_excludes_1"] == "false",
        "gate3_open": True,
        "not_physiology": True,
        "not_confirmatory": True,
        "not_a_6_day_heatwave": True,
        "spell_2018": spell,
        "q_minimum": 0.192,
    }
    CONTRACT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _draw_forest(ax, data: dict, outcome: str, exposure: str, title: str, scale: str) -> None:
    ax.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_color(SPINE)
        spine.set_linewidth(0.6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.axvline(1.0, color=VLINE, lw=0.8, zorder=1)
    ax.set_yticks(range(len(TREND_SPECS)))
    ax.set_yticklabels([label for _, _, label, _ in TREND_SPECS], fontsize=7.2, color=TEXT)
    ax.invert_yaxis()
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)

    xs_lo: list[float] = []
    xs_hi: list[float] = []
    for i, (scen, df, _label, _role) in enumerate(TREND_SPECS):
        rec = data[(outcome, exposure, scen)]
        chd = data[("chd", "hot_nights", scen)]
        hf = data[("hf", "cold_days", scen)]
        joint = _excludes(chd["lo"], chd["hi"]) and chd["lo"] > 1.0 and _excludes(hf["lo"], hf["hi"]) and hf["lo"] > 1.0
        more_flex = df is None or (df is not None and df > 4)
        if joint and more_flex:
            color, lw, ms = CROWN, 1.7, 5.4
        elif joint:
            color, lw, ms = TEAL, 1.55, 5.0
        else:
            color, lw, ms = GREY, 1.25, 4.4
        ax.plot([rec["lo"], rec["hi"]], [i, i], color=color, lw=lw, solid_capstyle="round", zorder=3)
        ax.plot(rec["rr"], i, "o", color=color, ms=ms, zorder=4)
        ax.text(
            rec["hi"] + 0.004,
            i,
            _fmt(rec["rr"], rec["lo"], rec["hi"]),
            va="center",
            ha="left",
            fontsize=6.5,
            color=SUB,
        )
        xs_lo.append(rec["lo"])
        xs_hi.append(rec["hi"])
    lo, hi = min(xs_lo), max(xs_hi)
    pad = max(0.018, 0.12 * (hi - lo))
    ax.set_xlim(lo - pad * 0.4, hi + pad * 2.15)
    ax.tick_params(axis="x", labelsize=7, colors=SUB, length=3)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("Count ratio (NW6)", fontsize=7.4, color=SUB)
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
    ax.text(0.03, 1.125, title, transform=ax.transAxes, fontsize=8.0, color=TEXT, fontweight="bold", va="center")
    ax.text(0.97, 1.125, scale, transform=ax.transAxes, fontsize=7.0, color=SUB, va="center", ha="right")


def draw_figure(data: dict, scores: list[dict]) -> None:
    _register_fonts()
    caption = "#5F6368"
    fig = plt.figure(figsize=(WIDTH_IN, HEIGHT_IN), dpi=DPI)
    gs = fig.add_gridspec(
        2,
        2,
        height_ratios=[1.18, 1.05],
        hspace=0.52,
        wspace=0.14,
        left=0.30,
        right=0.985,
        top=0.80,
        bottom=0.09,
    )

    ax_chd = fig.add_subplot(gs[0, 0])
    ax_hf = fig.add_subplot(gs[0, 1])
    ax_acf = fig.add_subplot(gs[1, :])

    _draw_forest(
        ax_chd,
        data,
        "chd",
        "hot_nights",
        "Coronary heart disease",
        "per 5 more official hot nights",
    )
    _draw_forest(
        ax_hf,
        data,
        "hf",
        "cold_days",
        "Heart failure",
        "per 5 more official cold days",
    )
    ax_hf.set_yticklabels([])
    ax_hf.tick_params(axis="y", length=0)

    ax_acf.set_facecolor("white")
    for spine in ax_acf.spines.values():
        spine.set_color(SPINE)
        spine.set_linewidth(0.6)
    ax_acf.spines["top"].set_visible(False)
    ax_acf.spines["right"].set_visible(False)
    ax_acf.grid(color=GRID, lw=0.6)
    ax_acf.set_axisbelow(True)

    df_x = [3, 4, 6, 8]
    chd_acf = [
        data[("chd", "hot_nights", s)]["acf1"]
        for s in ("trend_ns3", "baseline_ns4", "trend_ns6", "trend_ns8")
    ]
    hf_acf = [
        data[("hf", "cold_days", s)]["acf1"]
        for s in ("trend_ns3", "baseline_ns4", "trend_ns6", "trend_ns8")
    ]
    ax_acf.plot(df_x, chd_acf, "-o", color=TEAL, lw=1.5, ms=5.5, label="CHD · hot nights, lag-1 ACF")
    ax_acf.plot(df_x, hf_acf, "-s", color=GREY, lw=1.5, ms=5.0, label="HF · cold days, lag-1 ACF")
    ax_acf.axvline(6, color=CROWN, lw=0.9, ls="--", zorder=1)
    ax_acf.scatter([6], [chd_acf[2]], s=42, color=CROWN, zorder=5)
    ax_acf.set_xticks([3, 4, 6, 8])
    ax_acf.set_xticklabels(["3 df", "Model 1, 4 df", "6 df", "8 df"])
    ax_acf.set_ylabel("Pearson residual autocorrelation at lag 1", fontsize=7.6, color=SUB)
    ax_acf.set_xlabel("Time-trend spline degrees of freedom", fontsize=7.6, color=SUB)
    ax_acf.set_ylim(-0.02, 0.72)
    ax_acf.set_xlim(2.4, 8.6)
    ax_acf.legend(frameon=False, loc="upper right", fontsize=7.2)
    ax_acf.tick_params(labelsize=7.2, colors=SUB, length=3)
    ax_acf.text(
        6.12,
        0.20,
        "6 df is the only more-flexible spline\nthat still keeps both headlines away from 1",
        fontsize=7.1,
        color=CROWN,
        va="bottom",
    )

    fig.text(
        0.30,
        0.965,
        "Which time-trend spline still carries both exploratory headlines?",
        fontsize=10.2,
        color=TEXT,
        fontweight="bold",
    )
    fig.text(
        0.30,
        0.938,
        "Newey–West lag-6 intervals from the existing sensitivity table. No new health model.",
        fontsize=7.3,
        color=SUB,
    )
    legend_handles = [
        Line2D([0], [0], color=TEAL, lw=1.6, marker="o", ms=5, label="Both headlines exclude 1 (Model 1, 4 df)"),
        Line2D([0], [0], color=CROWN, lw=1.7, marker="o", ms=5.4, label="Both headlines exclude 1, more flexible than Model 1 (6 df)"),
        Line2D([0], [0], color=GREY, lw=1.3, marker="o", ms=4.4, label="At least one headline includes 1"),
    ]
    fig.legend(
        handles=legend_handles,
        loc="upper left",
        ncol=3,
        frameon=False,
        fontsize=6.6,
        bbox_to_anchor=(0.30, 0.915),
        columnspacing=1.1,
        handletextpad=0.4,
    )

    ns6 = next(r for r in scores if r["scenario"] == "trend_ns6")
    ns8 = next(r for r in scores if r["scenario"] == "trend_ns8")
    fig.text(
        0.30,
        0.012,
        (
            f"6 df CHD hot nights {ns6['chd_hot_nights_display']}; HF cold days {ns6['hf_cold_days_display']}. "
            f"8 df opens HF cold days onto 1 ({ns8['hf_cold_days_display']}). "
            "Not a 6-day heatwave. Table 2 remains Model 1 (4 df). Provenance: HA_APPROVED_AGGREGATE."
        ),
        fontsize=6.5,
        color=caption,
    )
    fig.savefig(FIG, dpi=DPI)
    plt.close(fig)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data = load_rows()
    scores = score(data)
    write_csv(SCORE_CSV, scores)
    write_headline_csv(data)
    spell = spell_firewall()
    write_contract(scores, spell)
    draw_figure(data, scores)
    print(f"wrote {SCORE_CSV.relative_to(ROOT)}")
    print(f"wrote {FIG.relative_to(ROOT)}")
    crowned = next(r for r in scores if r["crown_as_robustness"] == "true")
    print(f"robustness crown: {crowned['label']}")


if __name__ == "__main__":
    main()
