"""Contract checks for the 27 August 2026 Bishai lab-talk deck.

Does not invent HA coefficients. Does not freeze Gate 3.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TALK = ROOT / "reports" / "lab_talk_2026-08-27"
SLIDES = TALK / "slides.html"
NOTES = TALK / "SPEAKER_NOTES.md"
README = TALK / "README.md"
FOREST = TALK / "figures" / "forest.png"
SERIES = TALK / "figures" / "series.png"

REQUIRED_NUMBERS = (
    "156,156",
    "29,681",
    "132",
    "1.022",
    "1.002–1.042",
    "0.192",
    "1.073",
    "1.006–1.144",
    "1.011",
    "0.991–1.032",
    "1.113",
    "1.053–1.176",
    "141 of 145",
    "0.508",
)

REQUIRED_SLIDE_IDS = (
    "title",
    "two-jobs",
    "lab-family",
    "cannot-substitute",
    "summer-arc",
    "what-arrived",
    "estimand",
    "design",
    "forest",
    "leading",
    "finding",
    "novelty",
    "daily-refusal",
    "two-documents",
    "hogan-comments",
    "still-human",
    "ask",
)


def _slides() -> str:
    return SLIDES.read_text(encoding="utf-8")


def test_pack_files_exist():
    assert SLIDES.is_file()
    assert NOTES.is_file()
    assert README.is_file()
    assert FOREST.is_file() and FOREST.stat().st_size > 50_000
    assert SERIES.is_file() and SERIES.stat().st_size > 50_000


def test_sixteen_by_nine_and_navigation():
    html = _slides()
    assert "1920px" in html and "1080px" in html
    assert "ArrowRight" in html and "ArrowLeft" in html
    assert 'src="figures/forest.png"' in html
    assert 'src="figures/series.png"' in html
    assert "F11" in html


def test_seventeen_named_slides():
    html = _slides()
    ids = re.findall(r'<section class="slide[^"]*" data-id="([^"]+)"', html)
    assert ids == list(REQUIRED_SLIDE_IDS), ids
    assert html.count("<section") == 17


def test_required_numbers_and_honesty():
    html = _slides()
    for num in REQUIRED_NUMBERS:
        assert num in html, num
    assert "every <em>q</em>-value exceeded 0.19" in html
    assert "no confirmed association" in html
    assert "Gate 3 remains open" in html or "Gate 3 is open" in html
    assert "specified, <strong>not fitted</strong>" in html
    assert "Hogan does not sign form 2a" in html
    assert "No stroke coefficient exists" in html


def test_no_forbidden_claims():
    html = _slides()
    html_l = html.lower()
    notes = NOTES.read_text(encoding="utf-8")
    # Slides must not put Roro's excess-death range on screen.
    for phrase in ("1,455", "3,238", "1455", "3238"):
        assert phrase not in html
        for phrase in ("gate 3 is closed", "gate 3 closed", "we found that hot nights cause"):
            assert phrase not in html_l
    assert "do not quote" in notes.lower() and "1,455" in notes
    assert "IRB  " not in html
    assert "UW 24" not in html


def test_speaker_notes_point_at_html_not_pdf_spine():
    notes = NOTES.read_text(encoding="utf-8")
    assert "slides.html" in notes
    assert "Do not say we found a heat or cold effect" in notes
    assert "slide 9" in notes and "slide 10" in notes and "slide 17" in notes
    assert README.read_text(encoding="utf-8").startswith("# Lab talk")
