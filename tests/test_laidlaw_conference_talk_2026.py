"""Kill-list and structure tests for the Laidlaw conference 9-slide talk."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TALK = ROOT / "reports" / "laidlaw_conference_2026" / "talk"
SLIDES = TALK / "slides.html"
NOTES = TALK / "SPEAKER_NOTES.md"
README = TALK / "README.md"
TITLE_B = "Hot nights rose. Cold days stayed. The first heart admission did not settle the argument."


class SlideCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.slides: list[str] = []
        self._capture = False
        self._buf: list[str] = []
        self._depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        cls = dict(attrs).get("class", "") or ""
        if tag == "section" and "slide" in cls.split():
            self._capture = True
            self._depth = 1
            self._buf = []
            return
        if self._capture:
            if tag == "section":
                self._depth += 1
            self._buf.append(f"<{tag}>")

    def handle_endtag(self, tag: str) -> None:
        if not self._capture:
            return
        if tag == "section":
            self._depth -= 1
            if self._depth == 0:
                self.slides.append("".join(self._buf))
                self._capture = False
                self._buf = []
            return
        self._buf.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._buf.append(data)


def _html() -> str:
    return SLIDES.read_text(encoding="utf-8")


def _slides() -> list[str]:
    parser = SlideCollector()
    parser.feed(_html())
    return parser.slides


def test_exactly_nine_slides() -> None:
    slides = _slides()
    assert len(slides) == 9, f"expected 9 slides, got {len(slides)}"


def test_title_b_exact_on_first_and_last() -> None:
    html = _html()
    assert TITLE_B in html
    slides = _slides()
    assert TITLE_B in slides[0]
    assert TITLE_B in slides[-1]


def test_no_title_kicker_joke() -> None:
    html = _html().lower()
    for banned in (
        "we do not have a result",
        "whose result is that",
        "i refused a headline",
        "ambition as refusal",
    ):
        assert banned not in html, banned


def test_kill_list_absent_from_slides() -> None:
    import re

    html = _html().lower()
    for banned in (
        "gate 3",
        "pipeline",
        "warnings work",
        "twin confirmatory",
        "admissions averted",
        "ioannou",
    ):
        assert banned not in html, banned
    assert re.search(r"\biq\b", html) is None
    assert re.search(r"\bami\b", html) is None


def test_weather_copy_does_not_say_admissions_rose() -> None:
    slides = _slides()
    weather = slides[1].lower()
    assert "admissions rose" not in weather
    assert "admission rose" not in weather
    assert "156,156" in slides[1] or "156,156" in _html()
    assert "29,681" in _html()


def test_equation_one_present() -> None:
    html = _html()
    assert r"\log \mathrm{E}(Y_t)" in html
    assert r"\log(d_t)" in html
    assert "s(t; 4" in html or r"s(t; 4" in html
    assert "equation (1)" in html.lower()


def test_counts_and_q_fence() -> None:
    html = _html()
    assert "156,156" in html
    assert "29,681" in html
    assert "0.19" in html
    assert "0.192" in html


def test_1022_only_with_q() -> None:
    slides = _slides()
    found = False
    for slide in slides:
        if "1.022" in slide:
            found = True
            assert "0.192" in slide, "1.022 must share a slide with 0.192"
    assert found, "1.022 should appear (with q) on the residuals slide"


def test_1073_shares_slide_with_q() -> None:
    slides = _slides()
    for slide in slides:
        if "1.073" in slide:
            assert "0.192" in slide


def test_not_twins_and_asymmetry() -> None:
    html = _html()
    assert "not twins" in html.lower()
    assert "1.113" in html
    assert "more coherent" in html.lower()


def test_five_is_ruler_and_2018() -> None:
    html = _html()
    assert "I(count/5)" in html or r"I(\mathrm{count}/5)" in html
    assert "2018" in html
    assert "26" in html


def test_close_has_no_physiology_heading() -> None:
    slides = _slides()
    close = slides[-1].lower()
    assert "afterload" not in close
    assert "overnight" not in close
    assert "physiology" not in close


def test_no_cartoon_no_physiology_slide() -> None:
    html = _html().lower()
    assert "crossed-out" not in html
    assert "sketch-comedy" not in html
    headings = _html()
    assert "Overnight recovery" not in headings
    assert "afterload" not in headings.lower()


def test_speaker_notes_exist_and_forbid_printed_self_own() -> None:
    text = NOTES.read_text(encoding="utf-8")
    assert "Spoken, never printed" in text or "spoken, never printed" in text.lower()
    assert "afterload" in text.lower()
    assert "overnight" in text.lower()
    words = text.split()
    assert 700 <= len(words) <= 1400


def test_talk_readme_chrome_and_no_gate3_freeze() -> None:
    text = README.read_text(encoding="utf-8")
    assert "slides.html" in text
    assert "Chrome" in text or "chrome" in text
    assert "does **not** freeze Gate 3" in text or "not freeze Gate 3" in text.lower()
