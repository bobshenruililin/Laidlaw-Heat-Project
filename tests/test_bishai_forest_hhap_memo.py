"""Contract checks for the 27 Aug 2026 Bishai Figure 3 Explore memo.

Reads no governed HA microdata. Fits no health model.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMO = ROOT / "knowledge" / "2026-08-27_bishai_forest_precovid_duration_hhap.md"
TALK = ROOT / "reports" / "bishai_forest_hhap_2026-08-27" / "TALKING_POINTS.md"
DEBRIEF = ROOT / "reports" / "meeting_debrief_2026-08-27.md"
FIG = ROOT / "reports" / "bishai_forest_hhap_2026-08-27" / "figure_teaching_spline_df_not_duration.png"
QUOTED = ROOT / "reports" / "bishai_forest_hhap_2026-08-27" / "quoted_estimates.csv"
SRC = ROOT / "outputs" / "tables" / "cvd_trend_depletion_sensitivity.csv"
TABLE2 = ROOT / "outputs" / "release_chd_hf" / "tables" / "table2_core_models.csv"


def _row(outcome: str, exposure: str, scenario: str) -> dict:
    with SRC.open(encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            if rec["outcome"] == outcome and rec["exposure"] == exposure and rec["scenario"] == scenario:
                return rec
    raise AssertionError(f"missing {outcome} {exposure} {scenario}")


def test_artifacts_exist() -> None:
    for path in (MEMO, TALK, DEBRIEF, FIG, QUOTED):
        assert path.is_file(), path


def test_memo_maps_the_graph_not_duration() -> None:
    text = MEMO.read_text(encoding="utf-8")
    assert "live-manuscript Figure 3" in text
    assert "not a heatwave duration" in text
    assert "no 6-day heatwave" in text
    assert "does not freeze" in text.lower() or "Gate 3 remains open" in text
    assert "form 2a" in text.lower()
    assert "Hong Kong does not publish a single WHO-branded municipal Heat–Health Action Plan" in text


def test_pre_covid_referent_is_hf_cold_not_chd_hot() -> None:
    text = MEMO.read_text(encoding="utf-8")
    assert "1.113 (1.053–1.176)" in text
    assert "1.011 (0.991–1.032)" in text
    assert "pre-2020 **includes 1**" in text
    assert "pre-2020 **excludes 1**" in text
    precov = _row("hf", "cold_days", "pre_covid")
    assert abs(float(precov["rr"]) - 1.11283089052394) < 1e-12
    chd = _row("chd", "hot_nights", "pre_covid")
    lo, hi = float(chd["rr_low"]), float(chd["rr_high"])
    assert lo < 1.0 < hi


def test_spline_df_numbers_match_csv() -> None:
    quoted = { (r["outcome"], r["scenario"]): r for r in csv.DictReader(QUOTED.open()) }
    ns6 = quoted[("chd", "trend_ns6")]
    assert ns6["display"] == "1.024 (1.005–1.044)"
    assert ns6["interval"] == "excludes 1"
    ns3 = quoted[("chd", "trend_ns3")]
    assert ns3["interval"] == "includes 1"
    hf8 = quoted[("hf", "trend_ns8")]
    assert hf8["interval"] == "includes 1"
    year = quoted[("chd", "year_fixed_effects")]
    assert "0.9998" in year["display"]
    assert year["interval"] == "includes 1"


def test_table2_untouched() -> None:
    with TABLE2.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    chd = next(r for r in rows if r["outcome"] == "chd" and r["exposure"] == "hot_nights")
    hf = next(r for r in rows if r["outcome"] == "hf" and r["exposure"] == "cold_days")
    assert chd["count_ratio_95CI"] == "1.022 (1.002-1.042)"
    assert hf["count_ratio_95CI"] == "1.073 (1.006-1.144)"
    assert float(chd["q_value_core_bh"]) > 0.19
    assert float(hf["q_value_core_bh"]) > 0.19


def test_talking_points_refuse_overclaim() -> None:
    text = TALK.read_text(encoding="utf-8")
    assert "cannot test a daily 5-day warning rule" in text
    assert "Do not say" in text
    assert "Gate 3 is closed" in text  # listed as forbidden
