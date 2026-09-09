#!/usr/bin/env python3
"""Build Bob-only mechanism-review figures and an A4 PDF.

Does not fit a health model. Does not edit the live manuscript.
Weather series: REAL public HKO annual table already in git.
Count ratios: HA_APPROVED_AGGREGATE from the live Table 2 / Table 3.
Schematics are labelled SCHEMATIC.
"""
from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "reports" / "hogan_2026-09-04" / "mechanism_review"
FIG = PACK / "figures"
MD = PACK / "REVIEW.md"
HTML = PACK / "REVIEW.html"
PDF = PACK / "REVIEW.pdf"
ANNUAL = ROOT / "outputs" / "tables" / "exposure_aging" / "annual_extremes_and_spell_burden.csv"

TEAL = "#174d5b"
BRICK = "#7A2E32"
GREY = "#7A8087"
TEXT = "#202124"
SUB = "#42464B"
GRID = "#EEF0F2"
ACCENT = "#C45C26"
DPI = 220

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.edgecolor": "#303236",
        "axes.labelcolor": TEXT,
        "text.color": TEXT,
        "axes.titleweight": "bold",
    }
)


def _read_annual() -> list[dict]:
    with ANNUAL.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fig_nights_vs_spells(rows: list[dict]) -> Path:
    years = [int(r["year"]) for r in rows]
    nights = [int(r["hot_nights"]) for r in rows]
    spells = [int(r["days_in_hn_spell_ge5"]) for r in rows]
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    x = range(len(years))
    ax.bar([i - 0.18 for i in x], nights, 0.36, color=TEAL, label="Official hot nights")
    ax.bar(
        [i + 0.18 for i in x],
        spells,
        0.36,
        color=ACCENT,
        label="Days inside ≥5-night spells",
    )
    i2018 = years.index(2018)
    ax.annotate(
        "2018: 26 nights, 0 spell-days",
        xy=(i2018 + 0.18, 2),
        xytext=(i2018 + 0.6, 48),
        arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.1),
        color=ACCENT,
        fontsize=8,
    )
    ax.set_xticks(list(x), [str(y) for y in years], rotation=0)
    ax.set_ylabel("Days per year")
    ax.set_title("Official hot-night counts are not consecutive-night spells")
    ax.legend(frameon=False, loc="upper left")
    ax.set_facecolor("white")
    ax.yaxis.grid(True, color=GRID)
    ax.set_axisbelow(True)
    fig.text(
        0.01,
        0.01,
        "REAL public HKO Headquarters annual table. A spell-day is a day inside a run of ≥5 consecutive official hot nights.",
        fontsize=7,
        color=SUB,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    out = FIG / "fig_nights_vs_spells.png"
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    return out


def fig_heat_cold_annual(rows: list[dict]) -> Path:
    years = [int(r["year"]) for r in rows]
    nights = [int(r["hot_nights"]) for r in rows]
    cold = [int(r["cold_days"]) for r in rows]
    tmean = [float(r["mean_temp"]) for r in rows]
    fig, ax1 = plt.subplots(figsize=(7.2, 3.6))
    ax1.plot(years, nights, color=TEAL, marker="o", lw=1.8, label="Official hot nights")
    ax1.plot(years, cold, color=BRICK, marker="s", lw=1.8, label="Official cold days")
    ax1.set_ylabel("Official days per year")
    ax2 = ax1.twinx()
    ax2.plot(years, tmean, color=GREY, ls="--", marker=".", lw=1.2, label="Annual mean temperature")
    ax2.set_ylabel("Annual mean temperature (°C)")
    ax1.set_title("Hot nights rose. Cold days stayed. Mean temperature is a third series.")
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, frameon=False, loc="upper left")
    ax1.yaxis.grid(True, color=GRID)
    fig.text(
        0.01,
        0.01,
        "REAL public HKO Headquarters. Official hot night: Tmin ≥ 28 °C. Official cold day: Tmin ≤ 12 °C.",
        fontsize=7,
        color=SUB,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    out = FIG / "fig_heat_cold_annual.png"
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    return out


def fig_table2_forest() -> Path:
    # Live Table 2, Newey–West lag-6. HA_APPROVED_AGGREGATE.
    rows = [
        ("CHD  mean T / 1 °C", 0.993, 0.976, 1.010),
        ("CHD  mean Tmax / 1 °C", 0.993, 0.979, 1.007),
        ("CHD  mean Tmin / 1 °C", 0.994, 0.977, 1.012),
        ("CHD  hot nights / 5 days", 1.022, 1.002, 1.042),
        ("CHD  cold days / 5 days", 0.995, 0.949, 1.043),
        ("CHD  very hot days / 5 days", 0.999, 0.974, 1.025),
        ("HF  mean T / 1 °C", 0.974, 0.947, 1.002),
        ("HF  mean Tmax / 1 °C", 0.981, 0.958, 1.005),
        ("HF  mean Tmin / 1 °C", 0.973, 0.947, 1.000),
        ("HF  hot nights / 5 days", 1.003, 0.976, 1.031),
        ("HF  cold days / 5 days", 1.073, 1.006, 1.144),
        ("HF  very hot days / 5 days", 0.995, 0.963, 1.028),
    ]
    fig, ax = plt.subplots(figsize=(7.4, 5.4))
    y = list(range(len(rows) - 1, -1, -1))
    for yi, (lab, est, lo, hi) in zip(y, rows):
        excludes = lo > 1 or hi < 1
        color = TEAL if excludes else GREY
        ax.plot([lo, hi], [yi, yi], color=color, lw=1.6)
        ax.plot(est, yi, "o", color=color, ms=5.5)
    ax.axvline(1.0, color="#9AA0A6", ls="--", lw=0.9)
    ax.set_xlim(0.92, 1.18)
    ax.set_yticks(y, [lab for lab, *_ in rows], fontsize=8)
    ax.set_xlabel("Count ratio (Newey–West lag-6)")
    ax.set_title("Table 2: twelve Model 1 fits. Minimum q = 0.192.")
    fig.text(
        0.01,
        0.01,
        "HA_APPROVED_AGGREGATE. Live Table 2. Teal: interval excludes 1. Grey: includes 1. All twelve q > 0.19.",
        fontsize=7,
        color=SUB,
    )
    fig.tight_layout(rect=(0.02, 0.06, 1, 1))
    out = FIG / "fig_table2_forest.png"
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    return out


def fig_se_ladder() -> Path:
    # Live Table 3.
    specs = ["Model", "HC1", "NW lag-3", "NW lag-6"]
    chd = [(0.995, 1.049), (0.997, 1.047), (1.0003, 1.0439), (1.002, 1.042)]
    hf = [(1.023, 1.125), (1.011, 1.138), (1.007, 1.143), (1.006, 1.144)]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.5), sharex=True)
    for ax, title, est, intervals, color in (
        (axes[0], "CHD hot nights / 5 days\npoint 1.022", 1.022, chd, TEAL),
        (axes[1], "HF cold days / 5 days\npoint 1.073", 1.073, hf, BRICK),
    ):
        y = list(range(len(specs) - 1, -1, -1))
        for yi, (lo, hi) in zip(y, intervals):
            excludes = lo > 1
            ax.plot([lo, hi], [yi, yi], color=color if excludes else GREY, lw=1.8)
            ax.plot(est, yi, "o", color=color if excludes else GREY, ms=6)
        ax.axvline(1.0, color="#9AA0A6", ls="--", lw=0.9)
        ax.set_yticks(y, specs)
        ax.set_title(title, fontsize=9)
        ax.xaxis.grid(True, color=GRID)
    axes[0].set_xlabel("Count ratio")
    axes[1].set_xlabel("Count ratio")
    fig.suptitle("Uncertainty ladder: CHD is construction-dependent; HF is not", fontsize=11, y=0.98)
    fig.text(
        0.01,
        0.01,
        "HA_APPROVED_AGGREGATE. Live Table 3. q = 0.192 for both contrasts. Do not pick an SE because it excludes 1.",
        fontsize=7,
        color=SUB,
    )
    fig.tight_layout(rect=(0, 0.07, 1, 0.94))
    out = FIG / "fig_se_ladder.png"
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    return out


def fig_overnight_schematic() -> Path:
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_title("Why a hot-night count can differ from monthly mean temperature", loc="left")
    for x0, title, nights, mean in (
        (0.4, "Month A", 8, "same mean T"),
        (5.3, "Month B", 2, "same mean T"),
    ):
        box = FancyBboxPatch(
            (x0, 1.2),
            4.1,
            3.6,
            boxstyle="round,pad=0.08,rounding_size=0.12",
            facecolor="#F7F8F9",
            edgecolor=TEAL,
            lw=1.2,
        )
        ax.add_patch(box)
        ax.text(x0 + 2.05, 4.4, title, ha="center", fontsize=10, color=TEAL, fontweight="bold")
        ax.text(x0 + 2.05, 3.85, mean, ha="center", fontsize=8, color=SUB)
        # night ticks
        for i in range(nights):
            ax.add_patch(Rectangle((x0 + 0.35 + i * 0.42, 2.15), 0.28, 1.15, color=TEAL, alpha=0.85))
        ax.text(
            x0 + 2.05,
            1.5,
            f"{nights} official hot nights",
            ha="center",
            fontsize=8,
            color=TEXT,
        )
    ax.annotate(
        "Equation (1) sees X_t,\nnot sleep",
        xy=(5.0, 3.2),
        xytext=(4.15, 5.55),
        ha="center",
        fontsize=8,
        color=SUB,
        arrowprops=dict(arrowstyle="->", color=GREY),
    )
    fig.text(
        0.01,
        0.02,
        "SCHEMATIC. Not a fitted model. Official hot night = Tmin ≥ 28 °C at HKO Headquarters.",
        fontsize=7,
        color=SUB,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    out = FIG / "fig_overnight_schematic.png"
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    return out


def fig_afterload_schematic() -> Path:
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.set_title("Cold-related afterload is a haemodynamic hypothesis, not an estimate", loc="left")
    labels = [
        (0.4, "Official cold day\nTmin ≤ 12 °C"),
        (3.5, "Vasoconstriction\n↑ afterload"),
        (6.6, "Failing heart\nlittle reserve"),
    ]
    for i, (x, lab) in enumerate(labels):
        ax.add_patch(
            FancyBboxPatch(
                (x, 1.5),
                2.6,
                2.2,
                boxstyle="round,pad=0.08,rounding_size=0.12",
                facecolor="#F7F8F9",
                edgecolor=BRICK,
                lw=1.2,
            )
        )
        ax.text(x + 1.3, 2.6, lab, ha="center", va="center", fontsize=9, color=TEXT)
        if i < 2:
            ax.annotate(
                "",
                xy=(x + 2.75, 2.6),
                xytext=(x + 2.55, 2.6),
                arrowprops=dict(arrowstyle="->", color=BRICK, lw=1.4),
            )
    ax.text(5, 0.85, "This panel measures none of the middle or right boxes.", ha="center", fontsize=8, color=SUB)
    fig.text(
        0.01,
        0.02,
        "SCHEMATIC. Afterload = the pressure the heart pumps against. Not blood pressure, infection, or phenotype in this extract.",
        fontsize=7,
        color=SUB,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    out = FIG / "fig_afterload_schematic.png"
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    return out


def fig_ioannou_mismatch() -> Path:
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    ax.set_title("Ioannou 2024 is a chamber study. This extract is a territory-month count.", loc="left")
    ax.add_patch(FancyBboxPatch((0.3, 1.2), 4.3, 3.4, boxstyle="round,pad=0.1,rounding_size=0.12", facecolor="#F7F8F9", edgecolor=GREY, lw=1.2))
    ax.add_patch(FancyBboxPatch((5.4, 1.2), 4.3, 3.4, boxstyle="round,pad=0.1,rounding_size=0.12", facecolor="#F7F8F9", edgecolor=TEAL, lw=1.2))
    ax.text(2.45, 4.2, "Ioannou et al. 2024", ha="center", fontsize=10, fontweight="bold")
    ax.text(
        2.45,
        2.7,
        "n = 7 young men\n10-day confinement\nNights 4–6 at 26.3 °C\n+0.2 °C nocturnal core T\nduring and after",
        ha="center",
        va="center",
        fontsize=8,
    )
    ax.text(7.55, 4.2, "This extract", ha="center", fontsize=10, fontweight="bold", color=TEAL)
    ax.text(
        7.55,
        2.7,
        "132 territory-months\nT2D/HTN first CHD/HF\nNo admission cause\nOutdoor official counts\nNo core temperature",
        ha="center",
        va="center",
        fontsize=8,
    )
    fig.text(0.01, 0.02, "SCHEMATIC. Protocol numbers from Ioannou et al. 2024; not a coefficient in Table 2.", fontsize=7, color=SUB)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    out = FIG / "fig_ioannou_mismatch.png"
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    return out


def fig_indoor_outdoor() -> Path:
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    ax.set_title("Outdoor official counts do not measure bedroom temperature", loc="left")
    ax.add_patch(FancyBboxPatch((0.3, 1.3), 4.3, 3.3, boxstyle="round,pad=0.1,rounding_size=0.12", facecolor="#F7F8F9", edgecolor=TEAL, lw=1.2))
    ax.add_patch(FancyBboxPatch((5.4, 1.3), 4.3, 3.3, boxstyle="round,pad=0.1,rounding_size=0.12", facecolor="#F7F8F9", edgecolor=ACCENT, lw=1.2))
    ax.text(2.45, 4.15, "What this file has", ha="center", fontsize=10, fontweight="bold", color=TEAL)
    ax.text(2.45, 2.7, "HKO Headquarters\nTmin ≥ 28 °C = hot night\nMonthly official count X_t\nOutdoor, one station", ha="center", va="center", fontsize=8)
    ax.text(7.55, 4.15, "What O’Connor measured", ha="center", fontsize=10, fontweight="bold", color=ACCENT)
    ax.text(
        7.55,
        2.7,
        "47 adults ≥65 y\nSoutheast Queensland\nBedroom T bins from 24 °C\nNight-time HRV (lnRMSSD)\nIndoor, in-home sensors",
        ha="center",
        va="center",
        fontsize=8,
    )
    ax.annotate("", xy=(5.35, 2.9), xytext=(4.7, 2.9), arrowprops=dict(arrowstyle="->", color=GREY, lw=1.3))
    ax.text(5.05, 3.35, "no", ha="center", fontsize=8, color=BRICK)
    fig.text(0.01, 0.02, "SCHEMATIC. Official hot night is not a 24 °C bedroom.", fontsize=7, color=SUB)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    out = FIG / "fig_indoor_outdoor.png"
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    return out


def markdown_to_html(md_text: str) -> str:
    import markdown as md

    body = md.markdown(
        md_text,
        extensions=["tables", "fenced_code", "sane_lists"],
    )
    # Make image paths absolute for Chrome file://
    def _abs(m: re.Match) -> str:
        src = m.group(1)
        if src.startswith("http") or src.startswith("file:"):
            return m.group(0)
        p = (PACK / src).resolve()
        return f'src="{p.as_uri()}"'

    body = re.sub(r'src="([^"]+)"', _abs, body)
    css = """
@page { size: A4; margin: 16mm 15mm 18mm 15mm; }
html, body { font-family: "Liberation Serif", "Times New Roman", Times, serif; font-size: 11pt; line-height: 1.38; color: #202124; }
h1 { font-size: 16pt; line-height: 1.25; margin: 0 0 0.4em; }
h2 { font-size: 13pt; page-break-before: always; margin-top: 0.2em; border-bottom: 1px solid #cfd3d6; padding-bottom: 0.2em; }
h2:first-of-type { page-break-before: avoid; }
h3 { font-size: 11.5pt; margin-top: 1.1em; }
p { margin: 0.55em 0; }
.banner { background: #174d5b; color: #fff; padding: 10px 14px; margin: 0 0 14px; font-size: 10pt; }
.banner strong { letter-spacing: 0.02em; }
img { max-width: 100%; height: auto; display: block; margin: 0.7em auto; }
em { color: #42464B; }
ul, ol { margin: 0.4em 0 0.7em 1.2em; }
li { margin: 0.15em 0; }
table { border-collapse: collapse; width: 100%; font-size: 10pt; margin: 0.8em 0; }
th, td { border: 1px solid #d0d5d8; padding: 4px 6px; text-align: left; vertical-align: top; }
th { background: #eef3f4; }
caption, .caption { font-size: 9pt; color: #5F6368; }
.footer-note { font-size: 9pt; color: #5F6368; }
a { color: #174d5b; }
"""
    return (
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>"
        "<title>Mechanism points for Bob’s review</title>"
        f"<style>{css}</style></head><body>{body}</body></html>"
    )


def chrome_pdf(html_path: Path, pdf_path: Path) -> None:
    chrome = Path("/usr/local/bin/google-chrome")
    if not chrome.exists():
        chrome = Path("/usr/bin/google-chrome")
    profile = Path("/tmp/hogan-mechanism-review-chrome")
    profile.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(chrome),
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--allow-file-access-from-files",
        "--no-pdf-header-footer",
        f"--user-data-dir={profile}",
        "--virtual-time-budget=15000",
        f"--print-to-pdf={pdf_path}",
        html_path.resolve().as_uri(),
    ]
    try:
        subprocess.run(cmd, check=True, timeout=40)
    except subprocess.TimeoutExpired:
        if not pdf_path.exists() or pdf_path.stat().st_size < 20_000:
            raise
        print("chrome timed out after writing PDF; continuing")


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    rows = _read_annual()
    fig_nights_vs_spells(rows)
    fig_heat_cold_annual(rows)
    fig_table2_forest()
    fig_se_ladder()
    fig_overnight_schematic()
    fig_afterload_schematic()
    fig_ioannou_mismatch()
    fig_indoor_outdoor()
    md_text = MD.read_text(encoding="utf-8")
    HTML.write_text(markdown_to_html(md_text), encoding="utf-8")
    chrome_pdf(HTML, PDF)
    print(f"wrote {PDF} ({PDF.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
