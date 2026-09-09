"""Bob-only mechanism-review PDF: discussion cards plus 500–1000 words per point.

Does not send the PDF to Hogan. Does not cut the live manuscript.
Does not freeze a confirmatory claim.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "reports" / "hogan_2026-09-04" / "mechanism_review"
MD = PACK / "REVIEW.md"
PDF = PACK / "REVIEW.pdf"
LIVE = ROOT / "manuscript" / "live_collaborative" / "Heat_CVD_Manuscript_live_update.md"
BULLETS = ROOT / "reports" / "hogan_2026-09-04" / "MECHANISM_BULLETS.md"

POINT_LABELS = ("KEEP", "KEEP", "DROP", "DROP", "REFUSE", "REFUSE", "REFUSE")


def _words(text: str) -> list[str]:
    text = re.sub(r"<[^>]+>", " ", text)
    return re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z]+)?", text)


def _point_bodies(text: str) -> list[tuple[str, str]]:
    parts = re.split(r"\n(?=## )", text)
    out = []
    for part in parts:
        first = part.splitlines()[0]
        if first.startswith("## Point "):
            out.append((first, part))
    return out


def test_review_files_exist():
    assert MD.is_file()
    assert PDF.is_file()
    assert PDF.stat().st_size > 100_000
    assert (PACK / "README.md").is_file()
    assert (ROOT / "scripts" / "69_hogan_mechanism_review_pdf.py").is_file()
    for name in (
        "fig_nights_vs_spells.png",
        "fig_heat_cold_annual.png",
        "fig_table2_forest.png",
        "fig_se_ladder.png",
        "fig_overnight_schematic.png",
        "fig_afterload_schematic.png",
        "fig_ioannou_mismatch.png",
        "fig_indoor_outdoor.png",
    ):
        assert (PACK / "figures" / name).is_file(), name


def test_seven_points_are_review_length():
    bodies = _point_bodies(MD.read_text(encoding="utf-8"))
    assert len(bodies) == 7, [t for t, _ in bodies]
    for title, body in bodies:
        n = len(_words(body))
        assert 500 <= n <= 1000, (title, n)


def test_discussion_cards_make_the_decision_visible():
    text = MD.read_text(encoding="utf-8")
    low = text.lower()
    assert "conversation map" in low
    assert "on the table" in low
    assert "hogan asked" in low
    assert "live file" in low
    assert "do not send this pdf to hogan" in low
    assert "not a document" in low
    assert "doi under each point" in low
    assert "this rewrite" in low
    assert "not cut" in low
    bodies = _point_bodies(text)
    assert len(bodies) == 7
    for (title, body), label in zip(bodies, POINT_LABELS):
        assert label in title, title
        b = body.lower()
        assert "hogan asked" in b, title
        assert "live file" in b, title
        assert "on the table" in b, title
        assert f'<p class="label">{label}</p>' in body, title
        assert f"<strong>{label}</strong>" in body, title
        assert label.lower() in b, title


def test_packet_is_bob_only_and_not_a_hogan_send():
    text = MD.read_text(encoding="utf-8")
    low = text.lower()
    assert "bob review only" in low
    assert "do not send this pdf to hogan" in low
    readme = (PACK / "README.md").read_text(encoding="utf-8")
    assert "Not for Hogan" in readme or "not for Hogan" in readme
    parent = (ROOT / "reports" / "hogan_2026-09-04" / "README.md").read_text(encoding="utf-8")
    assert "mechanism_review" in parent
    bullets = BULLETS.read_text(encoding="utf-8")
    assert "Interrupted overnight recovery" in bullets
    assert "1.022" not in bullets


def test_science_rails():
    text = MD.read_text(encoding="utf-8")
    assert "1.022" in text
    assert "1.073" in text
    assert "0.192" in text
    assert "26 official hot nights" in text
    assert "failing heart" in text.lower()
    assert "failing left ventricle" not in text.lower()
    assert "I(count/5)" in text or "`I(count/5)`" in text
    live = LIVE.read_text(encoding="utf-8")
    assert "confinement study of seven men" in live
    assert "Meteorological data was obtained from the HKO." in live


def test_does_not_freeze_or_evaluate_warnings():
    text = MD.read_text(encoding="utf-8").lower()
    assert "gate 3 is closed" not in text
    assert "admissions averted" in text
    assert "do not" in text and "evaluate" in text
    pdf_head = PDF.read_bytes()[:8]
    assert pdf_head.startswith(b"%PDF")


if __name__ == "__main__":
    for fn in (
        test_review_files_exist,
        test_seven_points_are_review_length,
        test_discussion_cards_make_the_decision_visible,
        test_packet_is_bob_only_and_not_a_hogan_send,
        test_science_rails,
        test_does_not_freeze_or_evaluate_warnings,
    ):
        fn()
        print("ok", fn.__name__)
    print("all passed")
