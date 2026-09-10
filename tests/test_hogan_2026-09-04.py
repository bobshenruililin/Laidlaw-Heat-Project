"""Hogan 4 September 2026 briefing pack: half-page update, not a physiology workshop.

Does not fit health models. Does not freeze Gate 3. Does not lock weather from a blank sheet.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "reports" / "hogan_2026-09-04"
BRIEF = PACK / "BRIEFING.md"
TALK = PACK / "TALKING_POINTS.md"
SCORE = PACK / "APPENDIX_SCORECARD.md"
SHORT = PACK / "AGENT_OWNED_SHORTEN.md"
LIVE = (
    ROOT
    / "manuscript"
    / "archive"
    / "thermal_extremes_2026-08"
    / "live_collaborative_snapshot"
    / "Heat_CVD_Manuscript_live_update.md"
)


def _words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z]+)?", text)


def test_pack_files_exist():
    for p in (
        BRIEF,
        TALK,
        SCORE,
        SHORT,
        PACK / "APPENDIX_NEIGHBOURS.md",
        PACK / "DEBRIEF_TEMPLATE.md",
        PACK / "MECHANISM_BULLETS.md",
    ):
        assert p.is_file(), p


def test_briefing_is_a_half_page_update():
    text = BRIEF.read_text(encoding="utf-8")
    body = "\n".join(line for line in text.splitlines() if not line.startswith("#"))
    n = len(_words(body))
    assert 200 <= n <= 500, n
    assert "Meteorological data was obtained from the HKO." in text
    assert "more coherent residual" in text
    assert "labelled hypotheses" in text
    assert "not a request to lock weather today" in text.lower() or "not a request to lock weather" in text.lower()
    assert "If anything in this note is wrong" in text


def test_briefing_is_not_a_quiz():
    text = BRIEF.read_text(encoding="utf-8")
    low = text.lower()
    assert "keep / shorten" not in low
    assert "vote" not in low
    assert "ioannou" not in low
    assert "h4" not in low
    assert "gate 3" not in low
    assert "pipeline" not in low
    assert "housing" not in low
    assert "medication" not in low
    for needle in ("1.022", "1.073", "1.113", "2.63"):
        assert needle not in text


def test_talking_points_are_three_beats_and_bob_only():
    text = TALK.read_text(encoding="utf-8")
    assert "Do not hand this sheet over" in text
    assert "Do not ask him to vote on Ioannou" in text
    assert "Is anything in that update wrong?" in text
    assert "Open with the July HM/CM catalogue" in text or "Open with the July" in text


def test_scorecard_and_shorten_stay_in_appendix():
    score = SCORE.read_text(encoding="utf-8")
    short = SHORT.read_text(encoding="utf-8")
    assert "Do not hand this table to Hogan" in score
    assert "Not a Hogan vote" in short
    assert "SHORTEN" in short
    assert "Ioannou" in short
    live = LIVE.read_text(encoding="utf-8")
    # Live file unchanged this session: n=7 sentence still present until Bob pastes.
    assert "confinement study of seven men" in live


def test_scorecard_treats_h4_as_a_clause():
    score = SCORE.read_text(encoding="utf-8")
    assert "SATISFIED" in score
    assert "not an agenda item" in score.lower() or "not an agenda" in score.lower()
    assert "132" in score
    assert "Do not hand this table to Hogan" in score


def test_live_file_not_expanded_today():
    live = LIVE.read_text(encoding="utf-8")
    assert "can inform four" not in live
    assert "They are not a test of any alert" in live


def test_mechanism_bullets_are_short_and_hogan_facing():
    text = (PACK / "MECHANISM_BULLETS.md").read_text(encoding="utf-8")
    n = len(_words(text))
    assert n <= 120, n
    low = text.lower()
    assert "overnight recovery" in low
    assert "afterload" in low
    assert "seven-person" in low or "confinement" in low
    assert "bedroom" in low
    assert "nothing new is proposed" in low
    assert "1.022" not in text
    assert "gate 3" not in low
    assert "ioannou" not in low
    debrief = (PACK / "DEBRIEF_TEMPLATE.md").read_text(encoding="utf-8")
    assert "let me know beforehand about which mechanisms" in debrief
    assert "Locked something? No." in debrief


if __name__ == "__main__":
    for fn in (
        test_pack_files_exist,
        test_briefing_is_a_half_page_update,
        test_briefing_is_not_a_quiz,
        test_talking_points_are_three_beats_and_bob_only,
        test_scorecard_and_shorten_stay_in_appendix,
        test_scorecard_treats_h4_as_a_clause,
        test_live_file_not_expanded_today,
        test_mechanism_bullets_are_short_and_hogan_facing,
    ):
        fn()
        print("ok", fn.__name__)
    print("all passed")
