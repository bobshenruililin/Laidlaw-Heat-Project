"""Contract checks for the 29 August STORM physiology + HHAP write.

Physiology is labelled hypothesis. HHAP mapping informs and does not evaluate
Hong Kong warnings. Table 2, Abstract, and Hogan weather sentences stay locked.
Reads no governed HA microdata. Fits no health model.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MS = ROOT / "manuscript" / "live_collaborative" / "Heat_CVD_Manuscript_live_update.md"
ESSAY = ROOT / "reports" / "laidlaw_stage3" / "laidlaw_research_report_2026.md"
STORM = ROOT / "reports" / "storm_physio_hhap_2026-08-29"
BUILDER = ROOT / "scripts" / "64_hogan_20260824_manuscript_docx.py"

MS_TEXT = MS.read_text(encoding="utf-8")
ESSAY_TEXT = ESSAY.read_text(encoding="utf-8")
BUILDER_TEXT = BUILDER.read_text(encoding="utf-8")


def _paragraph(text: str, opening: str) -> str:
    return next(p for p in text.split("\n\n") if p.startswith(opening))


def _between(text: str, start: str, end: str) -> str:
    i = text.index(start)
    return text[i : text.index(end, i)]


WARNINGS = _paragraph(MS_TEXT, "A monthly official-day total")
NIGHTS = _paragraph(MS_TEXT, "Candidate mechanisms for a night residual")
COLD = _paragraph(MS_TEXT, "A corresponding hypothesis for HF")
HHAP = _paragraph(MS_TEXT, "The World Health Organization")


def test_storm_packet_exists():
    for name in (
        "00_topic.md",
        "01_perspectives.md",
        "02_conversations.md",
        "03_outline.md",
        "04_article.md",
        "05_hhap_crosswalk.md",
        "06_kill_list.md",
        "07_peer_review.md",
        "08_sol_live.md",
    ):
        assert (STORM / name).is_file(), name


def test_consecutive_paragraph_still_refuses_evaluation():
    assert "Interrupted overnight recovery is one hypothesis" in WARNINGS
    assert "The present monthly design cannot test that hypothesis." in WARNINGS
    assert "reporting scale rather than a consecutive-day trigger" in WARNINGS
    assert "Hong Kong issues official heat and cold warnings." in WARNINGS
    assert "These estimates do not evaluate those warnings." in WARNINGS
    for banned in ("should", "recommend", "policy", "HHAP", "Heat–Health Action Plan", "we advise"):
        assert banned.lower() not in WARNINGS.lower()


def test_night_physiology_is_hypothesis_not_identification():
    assert "physiological claim is therefore a hypothesis" in NIGHTS
    assert "This panel does not identify that pathway." in NIGHTS
    assert "do not measure first CHD hospitalisation" in NIGHTS
    assert "do not measure indoor temperature" in NIGHTS
    assert "blood-pressure findings were mixed" in NIGHTS
    assert "none demonstrated sleep as a mediator" in NIGHTS
    assert "26.3" in NIGHTS and "0.2" in NIGHTS
    assert "[23]" in NIGHTS and "[24]" in NIGHTS and "[25]" in NIGHTS and "[26]" in NIGHTS
    assert "[17]" in NIGHTS


def test_cold_physiology_is_hypothesis_not_goggins_import():
    assert "corresponding hypothesis for HF" in COLD
    assert "not a magnitude to import" in COLD
    assert "do not measure afterload" in COLD
    assert "[27,28]" in COLD or "[27, 28]" in COLD
    assert "[21]" in COLD
    assert "2.63" not in COLD


def test_hhap_maps_who_eight_and_hk_bundle_without_evaluation():
    for element in (
        "governance",
        "heat–health warning system",
        "populations at increased risk",
        "communication",
        "health-system resilience",
        "reducing heat exposure",
        "heat–health surveillance",
        "monitoring, evaluation and learning",
    ):
        assert element in HHAP
    assert "Very Hot Weather Warning" in HHAP
    assert "Prolonged Heat Special Alert" in HHAP
    assert "hot nights" in HHAP
    assert "heart disease or high blood pressure" in HHAP
    assert "Cold Weather Warning" in HHAP
    assert "cannot evaluate any of them" in HHAP
    assert "That overlap is a mapping, not a test of the alert." in HHAP
    assert "do not set a five-day trigger" in HHAP
    assert "do not count admissions averted" in HHAP
    assert "do not say whether existing warnings work" in HHAP
    assert "[29]" in HHAP and "[32]" in HHAP and "[31,33]" in HHAP


def test_kill_list_absent_from_manuscript_body():
    body = _between(MS_TEXT, "## Discussion", "## References")
    low = body.lower()
    assert "gate 3" not in body
    assert "admissions averted" in body  # refusal sentence
    assert "admissions were averted" not in low
    assert "5-df" not in low and "5 df spline" not in low
    assert "6-day" not in low and "8-day" not in low and "5-day heatwave" not in low
    assert "we evaluated" not in low
    assert "housing" not in low
    assert "medication" not in low
    assert "core panel" not in low


def test_locked_surfaces_untouched():
    abstract = _between(MS_TEXT, "**Background.**", "**Keywords:**")
    assert "1.022 (1.002–1.042)" in abstract
    assert "1.073 (1.006–1.144)" in abstract
    table2 = _between(MS_TEXT, "**Table 2. Model 1", "All twelve *q*-values")
    assert "| CHD | Hot nights / 5 days | 1.022 (1.002–1.042) | 0.032 | 0.192 |" in table2
    assert "| HF | Cold days / 5 days | 1.073 (1.006–1.144) | 0.031 | 0.192 |" in table2
    weather = _between(MS_TEXT, "#### Weather and pollutants data", "#### Population")
    assert "Meteorological data was obtained from the HKO." in weather
    assert "All monthly data were derived by taking the average of daily data in each calendar month." in weather
    assert "Acknowledgements\n\nNone." in MS_TEXT or "## Acknowledgements\n\nNone." in MS_TEXT


def test_builder_and_live_discussion_stay_in_sync():
    for needle in (
        "Candidate mechanisms for a night residual sit outside this design.",
        "A corresponding hypothesis for HF is haemodynamic rather than nocturnal.",
        "This panel can inform four of those elements and cannot evaluate any of them.",
        "That overlap is a mapping, not a test of the alert.",
        "Chevance G, Minor K, Vielma C",
        "Ioannou LG, Tsoutsoubi L, Mantzios K",
        "9789289062930",
    ):
        assert needle in MS_TEXT
        assert needle in BUILDER_TEXT


def test_laidlaw_report_carries_the_same_science():
    text = ESSAY_TEXT
    low = text.lower()
    assert "model 1" in low and "model 2" in low and "model 3" in low
    assert "core panel" not in low
    assert "gate 3" not in text
    for num in ("156,156", "29,681", "1.022", "1.073", "0.192", "1.011", "1.113"):
        assert num in text
    assert "@chevance2024sleep" in text
    assert "@ioannou2024heatwave" in text
    assert "@oconnor2025bedroom" in text
    assert "@ashe2025ehe" in text
    assert "@ikaheimo2018cold" in text
    assert "@li2026cold" in text
    assert "@who2026hhap" in text
    assert "@chong2023hko" in text
    assert "@chp2025heatstroke" in text
    assert "Table A2" in text
    assert "do not justify disease-specific warning thresholds" in text
    assert "I do not count admissions averted" in text
    assert "have not been fitted" in text or "not fitted here" in text
    assert "no health coefficients are invented" in text or "No health coefficients are invented" in text


def test_references_bib_has_storm_keys():
    bib = (ROOT / "literature" / "references.bib").read_text(encoding="utf-8")
    for key in (
        "chevance2024sleep",
        "ioannou2024heatwave",
        "oconnor2025bedroom",
        "ashe2025ehe",
        "ikaheimo2018cold",
        "li2026cold",
        "who2026hhap",
        "chong2023hko",
        "hko_vhw",
        "chp2025heatstroke",
        "had_heat_shelters",
    ):
        assert key in bib
    assert "10.1139/apnm-2024-0105" in bib
    assert "10.1186/s12916-025-04513-0" in bib
    assert "Bernard, Paquito" in bib
    assert "Mekjavic, Igor B." in bib
    assert "Benmarhnia" not in bib
    assert "Daanen" not in bib
