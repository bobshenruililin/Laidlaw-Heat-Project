"""Contract checks for the live-manuscript Figure 3 caption and the two
sensitivity Discussion paragraphs (spline df; consecutive days and warnings).

Locks the Hogan-register wording, the quoted spline-df numerals, and the scope
limits Bob set: no policy recommendation, no warning-system evaluation, and
consecutive-night recovery kept as a hypothesis.

Reads no governed HA microdata. Fits no health model.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MS = ROOT / "manuscript" / "live_collaborative" / "Heat_CVD_Manuscript_live_update.md"
SRC = ROOT / "outputs" / "tables" / "cvd_trend_depletion_sensitivity.csv"
CONTRACT = ROOT / "figures" / "live_identification" / "figure_D_relabel_contract.json"

TEXT = MS.read_text(encoding="utf-8")


def _between(start: str, end: str) -> str:
    i = TEXT.index(start)
    return TEXT[i : TEXT.index(end, i)]


def _paragraph(opening: str) -> str:
    return next(p for p in TEXT.split("\n\n") if p.startswith(opening))


def _row(outcome: str, exposure: str, scenario: str) -> dict:
    with SRC.open(encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            if (
                rec["outcome"] == outcome
                and rec["exposure"] == exposure
                and rec["scenario"] == scenario
            ):
                return rec
    raise AssertionError(f"missing {outcome} {exposure} {scenario}")


CAPTION = _between("**Figure 3. Model 1 count ratios", "![Figure 3]")
SPLINE = _paragraph("The two residual signals")
WARNINGS = _paragraph("A monthly official-day total")


def test_caption_states_the_five_day_scale_once() -> None:
    assert "the monthly official day count divided by five" in CAPTION
    assert "count ratio per five additional such days in that month" in CAPTION
    assert (
        "Neither the five-day scale nor the spline degrees of freedom refers to consecutive days."
        in CAPTION
    )
    # The guardrail is stated once, not restated as a second negation.
    assert "not heatwave length" not in CAPTION
    assert "rather than consecutive duration" not in CAPTION


def test_caption_keeps_locked_window_and_cross_reference() -> None:
    assert "Rows labelled 3, 6, or 8 df replace the 4-df time-trend spline of Model 1." in CAPTION
    assert "Pre-2020 is January 2013–December 2019 (84 months)." in CAPTION
    assert "shown in Supplementary Figure S6" in CAPTION


def test_caption_row_labels_match_the_figure_contract() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    for label in ("Time-trend spline, 3 df", "Time-trend spline, 6 df", "Time-trend spline, 8 df"):
        assert label in contract["y_labels"]
    assert "Model 1 (time-trend spline, 4 df)" in contract["y_labels"]
    for bad in contract["forbidden_labels"]:
        assert bad not in contract["y_labels"]


def test_spline_paragraph_numerals_match_the_approved_aggregate() -> None:
    quoted = {
        ("chd", "hot_nights", "trend_ns3"): "1.011, 0.990–1.032",
        ("chd", "hot_nights", "trend_ns6"): "1.024, 1.005–1.044",
        ("chd", "hot_nights", "trend_ns8"): "1.023, 1.005–1.042",
        ("hf", "cold_days", "trend_ns8"): "1.062, 0.994–1.135",
    }
    for (outcome, exposure, scenario), display in quoted.items():
        rec = _row(outcome, exposure, scenario)
        assert rec["data_status"] == "HA_APPROVED_AGGREGATE"
        rr, lo, hi = float(rec["rr"]), float(rec["rr_low"]), float(rec["rr_high"])
        assert display == f"{rr:.3f}, {lo:.3f}–{hi:.3f}"
        assert f"({display})" in SPLINE
    year = _row("chd", "hot_nights", "year_fixed_effects")
    assert float(year["rr_low"]) < 1.0 < float(year["rr_high"])
    assert "1.025, 0.9998–1.050" in SPLINE


def test_spline_paragraph_reports_inclusion_of_one_correctly() -> None:
    ns3 = _row("chd", "hot_nights", "trend_ns3")
    ns6 = _row("chd", "hot_nights", "trend_ns6")
    ns8_chd = _row("chd", "hot_nights", "trend_ns8")
    ns8 = _row("hf", "cold_days", "trend_ns8")
    assert float(ns3["rr_low"]) < 1.0 < float(ns3["rr_high"])
    assert float(ns6["rr_low"]) > 1.0
    assert float(ns8_chd["rr_low"]) > 1.0
    assert float(ns8["rr_low"]) < 1.0 < float(ns8["rr_high"])
    assert "includes 1 under a stiffer 3-df spline" in SPLINE
    assert "excludes 1 under the 6-df and 8-df splines" in SPLINE
    assert "includes 1 under the most flexible 8-df spline" in SPLINE
    assert "No trend specification is preferred" not in SPLINE  # that sentence lives in Results
    results = _between("### Sensitivity analyses", "**Figure 3. Model 1 count ratios")
    assert "No trend specification is preferred over the 4-df spline in Model 1." in results
    assert "the 6-df interval excludes 1" not in results


def test_spline_paragraph_refuses_a_duration_reading() -> None:
    assert "do not describe a physiological duration" in SPLINE
    assert "5-, 6-, or 8-day" not in SPLINE
    for word in ("threshold", "trigger", "heatwave"):
        assert word not in SPLINE.lower()


def test_consecutive_night_recovery_stays_a_hypothesis() -> None:
    assert "Interrupted overnight recovery is one hypothesis" in WARNINGS
    assert "The present monthly design cannot test that hypothesis." in WARNINGS
    assert "reporting scale rather than a consecutive-day trigger" in WARNINGS


def test_warning_sentence_is_scope_not_policy() -> None:
    assert "Hong Kong issues official heat and cold warnings." in WARNINGS
    assert "These estimates do not evaluate those warnings." in WARNINGS
    for banned in ("should", "recommend", "policy", "HHAP", "Heat–Health Action Plan", "we advise"):
        assert banned.lower() not in WARNINGS.lower()


def test_locked_surfaces_untouched() -> None:
    abstract = _between("**Background.**", "**Keywords:**")
    assert "1.022 (1.002–1.042)" in abstract
    assert "1.073 (1.006–1.144)" in abstract
    table2 = _between("**Table 2. Model 1", "All twelve *q*-values")
    assert "| CHD | Hot nights / 5 days | 1.022 (1.002–1.042) | 0.032 | 0.192 |" in table2
    assert "| HF | Cold days / 5 days | 1.073 (1.006–1.144) | 0.031 | 0.192 |" in table2
    weather = _between("#### Weather and pollutants data", "#### Population")
    assert "T~min~ ≥ 28°C" in weather
    assert "T~min~ ≤ 12°C" in weather


def test_no_gate_language_in_the_scientific_body() -> None:
    assert "Gate 3" not in TEXT
    assert "Monthly official-day totals cannot identify consecutive duration." in TEXT
    methods = _between("## Methods", "## Results")
    assert "not a new weather threshold and not a consecutive-duration rule" in methods
