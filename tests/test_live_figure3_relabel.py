"""Contract checks for rebuilt live-manuscript Figure 3.

The teaching forest in reports/bishai_forest_hhap_2026-08-27/ is not this figure.
Live Figure 3 is no longer a copy of release figure4_trend_depletion_sensitivity.
Reads no governed HA microdata. Fits no health model.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures" / "live_identification" / "figure_D_trend_depletion_sensitivity.png"
S6 = ROOT / "figures" / "live_identification" / "figure_E_continuous_temperature_sensitivity.png"
CONTRACT = ROOT / "figures" / "live_identification" / "figure_D_relabel_contract.json"
RELEASE = ROOT / "outputs" / "release_chd_hf" / "figures" / "figure4_trend_depletion_sensitivity.png"
MS = ROOT / "manuscript" / "live_collaborative" / "Heat_CVD_Manuscript_live_update.md"


def test_live_figure3_is_portrait_print_size() -> None:
    im = Image.open(FIG)
    w, h = im.size
    assert h > w
    width_in = w / 320
    height_in = h / 320
    assert 6.0 <= width_in <= 6.4
    assert 7.0 <= height_in <= 7.6


def test_release_figure4_untouched() -> None:
    im = Image.open(RELEASE)
    assert im.size == (6000, 3200)


def test_axis_language_cannot_be_read_as_duration() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    labels = contract["y_labels"] + contract["official_column_titles"]
    blob = " | ".join(labels)
    for bad in (
        "Spline df 3",
        "Spline df 6",
        "Spline df 8",
        "Pre-COVID",
        "Baseline: spline df 4",
    ):
        assert bad not in blob
    assert "per 5 days" not in blob
    assert "Time-trend spline, 6 df" in contract["y_labels"]
    assert "Model 1 (time-trend spline, 4 df)" in contract["y_labels"]
    assert "Pre-2020 (Jan 2013–Dec 2019)" in contract["y_labels"]
    assert any("official hot nights" in t for t in contract["official_column_titles"])
    assert any("official cold days" in t for t in contract["official_column_titles"])
    assert any("per 1 °C" in t for t in contract["continuous_column_titles"])
    assert S6.is_file()


def test_live_markdown_points_at_relabelled_figure() -> None:
    text = MS.read_text(encoding="utf-8")
    assert "figure_D_trend_depletion_sensitivity.png" in text
    assert "Supplementary Figure S6" in text
    caption = text.split("**Figure 3. Model 1 count ratios", 1)[1].split("![Figure 3]", 1)[0]
    assert "five additional such days" in caption
    assert "Spline df 6" not in caption
    assert "Gate 3" not in text
