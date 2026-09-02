"""Current Hogan Word+PDF must exceed the 24 August snapshot in every scored dimension.

Snapshot file (Bob Desktop / upload): Heat_CVD_Manuscript_20260824_hogan.pdf
SHA-256 prefix b172ed31659d6cd6, 14 pages. The snapshot is not committed.

Does not fit health models. Does not freeze Gate 3. Does not invent Model 2/3 coefficients.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / "manuscript" / "live_collaborative" / "Heat_CVD_Manuscript_20260824_hogan.docx"
PDF = ROOT / "manuscript" / "live_collaborative" / "Heat_CVD_Manuscript_20260824_hogan.pdf"
SNAPSHOT_SHA16 = "b172ed31659d6cd6"
SNAPSHOT_CANDIDATES = [
    Path("/home/ubuntu/.cursor/projects/workspace/uploads/Heat_CVD_Manuscript_20260824_hogan_1e60.pdf"),
    Path("/Users/macbookpro/Desktop/Heat_CVD_Manuscript_20260824_hogan.pdf"),
]

LOCKED = (
    "1.022 (1.002-1.042)",
    "1.073 (1.006-1.144)",
    "156,156",
    "29,681",
    "Meteorological data was obtained from the HKO.",
    "All monthly data were derived by taking the average of daily data in each calendar month.",
    "UW XX-XXX",
    "None.",
)
WINS_ABSENT_FROM_SNAPSHOT = (
    "Candidate mechanisms for a night residual",
    "corresponding hypothesis for HF",
    "Prolonged Heat Special Alert",
    "reporting scale rather than a consecutive-day trigger",
    "6-df spline",
    "Supplementary Figure S6",
    "Neither the five-day scale nor the spline degrees of freedom refers to consecutive days",
)
SNAPSHOT_ONLY_FIG3 = "All twelve Model 1 fits are shown across nine specifications."


def _norm(text: str) -> str:
    collapsed = " ".join(text.replace("\u00ad", "").split())
    return collapsed.replace("–", "-").replace("—", "-")


def _sha16(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def _pdf_pages(path: Path) -> list[str]:
    import pymupdf

    pdf = pymupdf.open(path)
    return [_norm(page.get_text()) for page in pdf]


def _find_snapshot() -> Path | None:
    for path in SNAPSHOT_CANDIDATES:
        if path.is_file() and _sha16(path) == SNAPSHOT_SHA16:
            return path
    return None


def test_current_files_exist_and_are_not_the_snapshot():
    assert DOCX.is_file(), DOCX
    assert PDF.is_file(), PDF
    assert _sha16(PDF) != SNAPSHOT_SHA16


def test_locked_science_survives():
    full = "\n".join(_pdf_pages(PDF))
    for needle in LOCKED:
        assert needle in full, needle
    assert "Model 1" in full and "Model 2" in full and "Model 3" in full
    assert "housing" not in full.lower()
    assert full.lower().count("medication") == 0
    assert "core panel" not in full.lower()
    assert "gate 3" not in full.lower()


def test_print_contract_and_identification_figure():
    pages = _pdf_pages(PDF)
    full = "\n".join(pages)

    def page_with(needle: str) -> int:
        hits = [i for i, text in enumerate(pages) if needle in text]
        assert hits, needle
        return hits[0]

    t1 = page_with("Table 1. Outcome summary")
    t2 = page_with("Table 2. Model 1:")
    t3 = page_with("Table 3. Uncertainty ladder")
    f1 = page_with("Figure 1. First-event")
    f2 = page_with("Figure 2. Official cold days")
    f3 = page_with("Figure 3. Model 1 count ratios")
    assert len({t1, t2, t3, f1, f2, f3}) == 6
    assert SNAPSHOT_ONLY_FIG3 not in full
    assert "five additional such days" in pages[f3]
    assert "spline degrees of freedom" in pages[f3]


def test_discussion_wins_over_snapshot():
    full = "\n".join(_pdf_pages(PDF))
    for needle in WINS_ABSENT_FROM_SNAPSHOT:
        assert needle in full, needle
    assert "do not count admissions averted" in full
    assert "They are not a test of any alert" in full
    assert "Supplementary Table S9" in full


def test_word_comments_are_send_ready():
    from docx import Document

    d = Document(str(DOCX))
    joined = " ".join(c.text for c in d.comments).lower()
    for banned in ("paste", "circulate", "shared live", "pipeline", "rscript", "gate 3"):
        assert banned not in joined, banned
    assert "model 2" in joined
    assert "uw xx-xxx" in joined or "irb" in joined


def test_snapshot_file_loses_on_the_win_list_when_present():
    snap = _find_snapshot()
    if snap is None:
        return
    pages = _pdf_pages(snap)
    full = "\n".join(pages)
    assert len(pages) == 14
    assert SNAPSHOT_ONLY_FIG3 in full
    for needle in WINS_ABSENT_FROM_SNAPSHOT:
        assert needle not in full, needle
    # Snapshot packs Table 2 with Table 3; current must not.
    t2 = next(i for i, t in enumerate(pages) if "Table 2. Model 1:" in t)
    assert "Table 3. Uncertainty ladder" in pages[t2]


if __name__ == "__main__":
    for fn in (
        test_current_files_exist_and_are_not_the_snapshot,
        test_locked_science_survives,
        test_print_contract_and_identification_figure,
        test_discussion_wins_over_snapshot,
        test_word_comments_are_send_ready,
        test_snapshot_file_loses_on_the_win_list_when_present,
    ):
        fn()
        print("ok", fn.__name__)
    print("all passed")
