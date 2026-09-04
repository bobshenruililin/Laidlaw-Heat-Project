"""Kill-list and word-count checks for the 2026 Laidlaw conference abstract.

Does not fit health models. Does not freeze Gate 3. Does not evaluate warnings.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUB = ROOT / "reports" / "laidlaw_conference_2026" / "ABSTRACT_SUBMISSION.md"
PASTE = ROOT / "reports" / "laidlaw_conference_2026" / "COPY_PASTE.md"

TITLE = (
    "Hot nights rose. Cold days stayed. "
    "The first heart admission did not settle the argument."
)


def _words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z]+)?", text.replace("—*q*", " q "))


def _section(text: str, heading: str, next_headings: tuple[str, ...]) -> str:
    start = text.index(heading)
    rest = text[start + len(heading) :]
    ends = [rest.index(h) for h in next_headings if h in rest]
    return rest[: min(ends)] if ends else rest


def test_files_exist():
    assert SUB.is_file(), SUB
    assert PASTE.is_file(), PASTE
    assert (ROOT / "reports" / "laidlaw_conference_2026" / "README.md").is_file()


def test_title_is_exactly_b():
    assert TITLE in SUB.read_text(encoding="utf-8")
    assert TITLE in PASTE.read_text(encoding="utf-8")


def test_q12_word_count_and_third_person():
    text = SUB.read_text(encoding="utf-8")
    body = _section(
        text,
        "## 12. How the presentation relates to “Ambitious” (50–100 words)",
        ("## 13.",),
    ).strip()
    # Drop the heading's following blank line only; keep the paragraph.
    para = "\n".join(
        line for line in body.splitlines() if line.strip() and not line.startswith("##")
    )
    n = len(_words(para))
    assert 50 <= n <= 100, n
    assert not re.search(r"\bI\b", para)
    assert not re.search(r"\b[Mm]y\b", para)
    # Weather stays weather until refusal.
    low = para.lower()
    assert "hot-night" in low or "hot night" in low
    assert "persisted" in low
    assert "not promoted" in low or "do not support" in low or "cannot run" in low


def test_abstract_word_count_and_scale():
    text = SUB.read_text(encoding="utf-8")
    body = _section(text, "## 14. Abstract (200–300 words)", ("## Panel", "## Word"))
    para = "\n".join(
        line for line in body.splitlines() if line.strip() and not line.startswith("##")
    )
    n = len(_words(para))
    assert 200 <= n <= 300, n
    assert "156,156" in para
    assert "29,681" in para
    assert "132" in para
    assert "0.19" in para
    assert "more coherent residual" in para.lower()
    assert "twin confirmatory" in para.lower()


def test_kill_list_on_conference_surfaces():
    sub = SUB.read_text(encoding="utf-8")
    paste = PASTE.read_text(encoding="utf-8")
    public = (
        _section(sub, "## 8. Presentation topic", ("## 9.",))
        + _section(sub, "## 12. How the presentation relates to “Ambitious” (50–100 words)", ("## 13.",))
        + _section(sub, "## 13. Presentation title", ("## 14.",))
        + _section(sub, "## 14. Abstract (200–300 words)", ("## Panel", "## Word"))
        + paste
    )
    for needle in ("1.022", "1.073", "1.113"):
        assert needle not in public, needle
    low = public.lower()
    assert "gate 3" not in low
    assert "pipeline" not in low
    assert "we evaluated" not in low
    assert "admissions averted" not in low
    assert "housing" not in low
    assert "medication" not in low
    assert "i evaluated hong kong" not in low
    assert "Do **not** tick PACE" in sub or "Do not tick PACE" in paste


def test_categories_sdgs_and_ambition_ticks():
    text = SUB.read_text(encoding="utf-8")
    for item in (
        "Applied Health and Medicine",
        "Climate and Sustainability",
        "Technology and Mathematical Sciences",
        "3 Good Health and Wellbeing",
        "11 Sustainable Cities and Communities",
        "13 Climate Action",
        "PASSION",
        "RESILIENCE",
        "POSSIBILITY",
        "VALUE-DRIVEN",
        "COLLECTIVITY",
        "SCALE",
        "VISION",
    ):
        assert item in text
    assert "PACE" in text


def test_paste_block_matches_submission_fields():
    sub = SUB.read_text(encoding="utf-8")
    paste = PASTE.read_text(encoding="utf-8")
    q12 = _section(
        sub,
        "## 12. How the presentation relates to “Ambitious” (50–100 words)",
        ("## 13.",),
    ).strip()
    q12_para = "\n".join(
        line for line in q12.splitlines() if line.strip() and not line.startswith("##")
    )
    abs_body = _section(sub, "## 14. Abstract (200–300 words)", ("## Panel", "## Word")).strip()
    for line in abs_body.splitlines():
        if line.strip() and not line.startswith("##"):
            assert line.strip() in paste
    assert q12_para in paste
    assert "Heat, cold, and first cardiac hospitalisation in Hong Kong: ambition as refusal." in paste


def test_hot_nights_are_weather_not_admissions():
    text = SUB.read_text(encoding="utf-8")
    abs_body = _section(text, "## 14. Abstract (200–300 words)", ("## Panel", "## Word"))
    # The weather hook must not say heart admissions increased.
    first = abs_body.strip().split("\n\n")[0]
    assert "hot-night" in first.lower() or "hot night" in first.lower()
    assert "admission" not in first.lower() or "first cardiac admission" in first.lower()
    # "first cardiac admission" in sentence 2 is the question, not a trend.
    assert "admissions increased" not in abs_body.lower()
    assert "admissions rose" not in abs_body.lower()


if __name__ == "__main__":
    for fn in (
        test_files_exist,
        test_title_is_exactly_b,
        test_q12_word_count_and_third_person,
        test_abstract_word_count_and_scale,
        test_kill_list_on_conference_surfaces,
        test_categories_sdgs_and_ambition_ticks,
        test_paste_block_matches_submission_fields,
        test_hot_nights_are_weather_not_admissions,
    ):
        fn()
        print("ok", fn.__name__)
    print("all passed")
