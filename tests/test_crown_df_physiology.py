"""Contract checks for the 27 Aug 2026 crown-among-5-6-8 memo.

Reads no governed HA microdata. Fits no health model.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMO = ROOT / "knowledge" / "2026-08-27_crown_df_physiology_policy.md"
TALK = ROOT / "reports" / "crown_df_physiology_2026-08-27" / "TALKING_POINTS.md"
FIG = ROOT / "reports" / "crown_df_physiology_2026-08-27" / "figure_joint_headline_vs_trend_df.png"
SCORE = ROOT / "reports" / "crown_df_physiology_2026-08-27" / "spline_df_joint_score.csv"
CONTRACT = ROOT / "reports" / "crown_df_physiology_2026-08-27" / "crown_contract.json"
SPELL = ROOT / "reports" / "crown_df_physiology_2026-08-27" / "spell_2018_firewall.json"
SRC = ROOT / "outputs" / "tables" / "cvd_trend_depletion_sensitivity.csv"
TABLE2 = ROOT / "outputs" / "release_chd_hf" / "tables" / "table2_core_models.csv"
MS = (
    ROOT
    / "manuscript"
    / "archive"
    / "thermal_extremes_2026-08"
    / "live_collaborative_snapshot"
    / "Heat_CVD_Manuscript_live_update.md"
)
ANNUAL = ROOT / "outputs" / "tables" / "exposure_aging" / "annual_extremes_and_spell_burden.csv"


def _row(outcome: str, exposure: str, scenario: str) -> dict:
    with SRC.open(encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            if rec["outcome"] == outcome and rec["exposure"] == exposure and rec["scenario"] == scenario:
                return rec
    raise AssertionError(f"missing {outcome} {exposure} {scenario}")


def _excludes(lo: float, hi: float) -> bool:
    return not (lo <= 1.0 <= hi)


def test_artifacts_exist() -> None:
    for path in (MEMO, TALK, FIG, SCORE, CONTRACT, SPELL):
        assert path.is_file(), path
    assert FIG.stat().st_size > 80_000


def test_no_five_df_spline_exists() -> None:
    with SRC.open(encoding="utf-8") as f:
        scenarios = {r["scenario"] for r in csv.DictReader(f)}
    assert "trend_ns5" not in scenarios
    assert "baseline_ns4" in scenarios
    assert "trend_ns3" in scenarios
    assert "trend_ns6" in scenarios
    assert "trend_ns8" in scenarios
    text = MEMO.read_text(encoding="utf-8")
    assert "There is no 5-df spline" in text
    assert "Five is not a spline" in text


def test_joint_preservation_only_ns4_and_ns6() -> None:
    scores = list(csv.DictReader(SCORE.open()))
    preserved = [r["scenario"] for r in scores if r["joint_headline_preserved"] == "true"]
    assert preserved == ["baseline_ns4", "trend_ns6"]
    crowned = [r for r in scores if r["crown_as_robustness"] == "true"]
    assert len(crowned) == 1
    assert crowned[0]["scenario"] == "trend_ns6"
    ns8 = next(r for r in scores if r["scenario"] == "trend_ns8")
    assert ns8["hf_cold_days_excludes_1"] == "false"
    ns3 = next(r for r in scores if r["scenario"] == "trend_ns3")
    assert ns3["chd_hot_nights_excludes_1"] == "false"
    year = next(r for r in scores if r["scenario"] == "year_fixed_effects")
    assert year["joint_headline_preserved"] == "false"


def test_score_table_matches_approved_aggregate() -> None:
    scores = {r["scenario"]: r for r in csv.DictReader(SCORE.open())}
    for scen in ("trend_ns3", "baseline_ns4", "trend_ns6", "trend_ns8", "year_fixed_effects"):
        chd = _row("chd", "hot_nights", scen)
        hf = _row("hf", "cold_days", scen)
        assert chd["data_status"] == "HA_APPROVED_AGGREGATE"
        assert abs(float(scores[scen]["chd_hot_nights_rr"]) - float(chd["rr"])) < 1e-12
        assert abs(float(scores[scen]["hf_cold_days_rr"]) - float(hf["rr"])) < 1e-12
        assert abs(float(scores[scen]["chd_hot_nights_acf1"]) - float(chd["residual_acf1"])) < 1e-12
        chd_ok = _excludes(float(chd["rr_low"]), float(chd["rr_high"])) and float(chd["rr_low"]) > 1.0
        hf_ok = _excludes(float(hf["rr_low"]), float(hf["rr_high"])) and float(hf["rr_low"]) > 1.0
        assert scores[scen]["chd_hot_nights_excludes_1"] == str(chd_ok).lower()
        assert scores[scen]["hf_cold_days_excludes_1"] == str(hf_ok).lower()
        assert scores[scen]["joint_headline_preserved"] == str(chd_ok and hf_ok).lower()


def test_ns8_opens_hf_cold_and_ns3_opens_chd_hot() -> None:
    ns8 = _row("hf", "cold_days", "trend_ns8")
    ns3 = _row("chd", "hot_nights", "trend_ns3")
    ns6_chd = _row("chd", "hot_nights", "trend_ns6")
    ns6_hf = _row("hf", "cold_days", "trend_ns6")
    assert float(ns8["rr_low"]) < 1.0 < float(ns8["rr_high"])
    assert float(ns3["rr_low"]) < 1.0 < float(ns3["rr_high"])
    assert float(ns6_chd["rr_low"]) > 1.0
    assert float(ns6_hf["rr_low"]) > 1.0


def test_2018_monthly_count_is_not_consecutive_duration() -> None:
    spell = json.loads(SPELL.read_text(encoding="utf-8"))
    assert spell["year_2018_official_hot_nights"] == 26
    assert spell["year_2018_days_in_hn_spell_ge5"] == 0
    assert spell["period_2013_2023_hot_nights"] == 449
    assert spell["period_2013_2023_days_in_hn_spell_ge5"] == 195
    with ANNUAL.open(encoding="utf-8") as f:
        y2018 = next(r for r in csv.DictReader(f) if int(r["year"]) == 2018)
    assert int(float(y2018["hot_nights"])) == 26
    assert int(float(y2018["days_in_hn_spell_ge5"])) == 0
    memo = MEMO.read_text(encoding="utf-8")
    assert "26 official hot nights" in memo
    assert "zero days" in memo


def test_memo_keeps_estimand_firewall() -> None:
    text = MEMO.read_text(encoding="utf-8")
    assert "daily mortality" in text.lower()
    assert "Wang et al." in text or "Wang, Lau, Ren" in text
    assert "Guo" in text
    assert "not a trigger this monthly panel validated" in text
    assert "Ioannou" in text
    assert "O’Connor" in text or "O'Connor" in text
    assert "Chevance" in text
    assert "Gate 3 remains open" in text
    assert "Table 2 remains Model 1" in text
    assert "form 2a" in text.lower()
    assert "not admissions averted" in text.lower()
    assert "What must not be said" in text
    assert "6-day cliff" in text


def test_memo_does_not_replace_table2() -> None:
    with TABLE2.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    chd = next(r for r in rows if r["outcome"] == "chd" and r["exposure"] == "hot_nights")
    hf = next(r for r in rows if r["outcome"] == "hf" and r["exposure"] == "cold_days")
    assert chd["count_ratio_95CI"] == "1.022 (1.002-1.042)"
    assert hf["count_ratio_95CI"] == "1.073 (1.006-1.144)"
    assert float(chd["q_value_core_bh"]) > 0.19
    assert float(hf["q_value_core_bh"]) > 0.19
    text = MEMO.read_text(encoding="utf-8")
    assert "1.022 (1.002–1.042)" in text
    assert "1.073 (1.006–1.144)" in text
    assert "1.024 (1.005–1.044)" in text
    assert "1.072 (1.005–1.143)" in text
    assert "1.062 (0.994–1.135)" in text


def test_talking_points_refuse_overclaim() -> None:
    text = TALK.read_text(encoding="utf-8")
    assert "Crown **6-df as the named robustness check**" in text
    assert "Do not move Table 2 off 4-df" in text
    assert "Do not crown 8" in text
    assert "Gate 3 is closed" in text  # listed as forbidden
    assert "Admissions will fall" in text  # listed as forbidden
    assert "26 official hot nights and zero five-night spells" in text


def test_contract_json_locks_the_crown() -> None:
    payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert payload["robustness_crown_among_more_flexible_splines"] == "trend_ns6"
    assert payload["five_is_not_a_spline"] is True
    assert payload["gate3_open"] is True
    assert payload["not_physiology"] is True
    assert payload["not_confirmatory"] is True
    assert payload["not_a_6_day_heatwave"] is True
    assert payload["joint_headline_preserved_scenarios"] == ["baseline_ns4", "trend_ns6"]
    assert payload["q_minimum"] == 0.192


def test_live_manuscript_table2_and_abstract_untouched() -> None:
    text = MS.read_text(encoding="utf-8")
    assert "Gate 3" not in text
    assert "**Background.**" in text
    i = text.index("**Background.**")
    abstract = text[i : text.index("**Keywords:**")]
    assert "1.022 (1.002–1.042)" in abstract
    assert "1.073 (1.006–1.144)" in abstract
    assert "| CHD | Hot nights / 5 days | 1.022 (1.002–1.042) | 0.032 | 0.192 |" in text
    assert "| HF | Cold days / 5 days | 1.073 (1.006–1.144) | 0.031 | 0.192 |" in text
    assert "No trend specification is preferred over the 4-df spline in Model 1." in text
    assert "Among specifications more flexible than Model 1, only the 6-df spline keeps both residual intervals away from 1." in text
    builder = (ROOT / "scripts" / "64_hogan_20260824_manuscript_docx.py").read_text(encoding="utf-8")
    assert "only the 6-df spline keeps both residual intervals away from 1" in builder
    assert "If a single more-flexible robustness check is named, it is the 6-df spline" in builder
