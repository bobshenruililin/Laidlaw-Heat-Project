"""Kill-list and mapping checks for the 2 September HHAP companion paper.

Does not fit health models. Does not freeze Gate 3. Does not evaluate warnings.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "manuscript" / "hhap" / "who2026_hong_kong_instrument_map.md"
LIVE = ROOT / "manuscript" / "live_collaborative" / "Heat_CVD_Manuscript_live_update.md"
PDF = ROOT / "manuscript" / "hhap" / "who2026_hong_kong_instrument_map.pdf"
HOGAN_PDF = (
    ROOT
    / "manuscript"
    / "live_collaborative"
    / "Heat_CVD_Manuscript_20260824_hogan.pdf"
)

TEXT = PAPER.read_text(encoding="utf-8")
LIVE_TEXT = LIVE.read_text(encoding="utf-8")


def test_hhap_paper_exists_and_names_who_eight():
    assert PAPER.is_file()
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
        assert element in TEXT.lower() or element.replace("–", "-") in TEXT.lower() or element in TEXT


def test_mapping_not_evaluation():
    low = TEXT.lower()
    assert "this is not an evaluation" in low or "does not evaluate" in low
    assert "we evaluated vhww" not in low
    assert "admissions were averted" not in low
    assert "does not count admissions averted" in low or "cannot estimate admissions averted" in low
    assert "hong kong already" in low
    assert "lacks heat–health instruments" not in low
    assert "lacks heat-health instruments" not in low
    assert "has no heat–health instruments is false" in low or "has no heat-health instruments is false" in low
    assert "table 2 is a design map" in low


def test_does_not_collapse_law2026_or_goggins():
    assert "law2026extremelyhot" in TEXT or "Law et al. (2026)" in TEXT
    assert "not an evaluation of the Very Hot Weather Warning *by this panel*" in TEXT
    assert "2.63" not in TEXT
    assert "1.148" in TEXT  # Law et al. own numeral, labelled as theirs


def test_locked_identification_numerals_are_quoted_not_promoted():
    assert "1.022 (1.002–1.042)" in TEXT or "1.022 (1.002-1.042)" in TEXT
    assert "1.073 (1.006–1.144)" in TEXT or "1.073 (1.006-1.144)" in TEXT
    assert "q*-values exceeded 0.19" in TEXT or "q-values exceeded 0.19" in TEXT
    assert "not evidence that a warning works" in TEXT.lower() or "are not evidence that a warning works" in TEXT


def test_cold_counterpart_not_retired():
    assert "Cold Weather Warning" in TEXT
    assert "heat-only" in TEXT.lower()
    assert "1.113" in TEXT


def test_forbidden_audit_phrases_absent():
    for phrase in (
        "can inform four",
        "sits with official",
        "continued attention",
        "Gate 3 is closed",
        "we evaluated VHWW",
        "5-df spline",
        "core panel",
    ):
        assert phrase not in TEXT
    # WHO language uses "household"; do not let that fail a housing-claim kill.
    assert re.search(r"(?<![A-Za-z])housing(?![A-Za-z])", TEXT, re.I) is None


def test_live_discussion_untouched_by_this_port():
    assert "Meteorological data was obtained from the HKO." in LIVE_TEXT
    assert "Still OPEN" not in LIVE_TEXT  # Gate 3 lives in decision_gates, not here
    body = LIVE_TEXT.split("## Discussion", 1)[1]
    assert "can inform four" not in body


def test_hhap_pdf_built():
    assert PDF.is_file(), PDF
    assert PDF.stat().st_size > 20_000
    import pymupdf

    pages = [" ".join(p.get_text().split()) for p in pymupdf.open(PDF)]
    full = " ".join(pages)
    assert "WHO 2026" in full or "heat-health action" in full.lower() or "heat–health action" in full
    assert "1.022" in full and "1.073" in full
    assert "1.148" in full
    assert "not an evaluation" in full.lower() or "does not evaluate" in full.lower()
    assert "Table 1" in full and "Table 2" in full
    assert "design map" in full.lower()
    n_pages = pymupdf.open(PDF).page_count
    assert 4 <= n_pages <= 8, n_pages


def test_hogan_identification_pdf_keeps_hko():
    assert HOGAN_PDF.is_file(), HOGAN_PDF
    import pymupdf

    full = " ".join(" ".join(p.get_text().split()) for p in pymupdf.open(HOGAN_PDF))
    assert "Meteorological data was obtained from the HKO." in full


if __name__ == "__main__":
    for fn in (
        test_hhap_paper_exists_and_names_who_eight,
        test_mapping_not_evaluation,
        test_does_not_collapse_law2026_or_goggins,
        test_locked_identification_numerals_are_quoted_not_promoted,
        test_cold_counterpart_not_retired,
        test_forbidden_audit_phrases_absent,
        test_live_discussion_untouched_by_this_port,
        test_hhap_pdf_built,
        test_hogan_identification_pdf_keeps_hko,
    ):
        fn()
        print("ok", fn.__name__)
    print("all passed")
