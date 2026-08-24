"""Stage 3 essay/poster must match Hogan's numbered-model language without
inventing Model 2/3 health coefficients or becoming a journal clone.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ESSAY_MD = ROOT / "reports" / "laidlaw_stage3" / "laidlaw_research_report_2026.md"
POSTER_TEX = ROOT / "reports" / "poster" / "Laidlaw_Stage3_A0_portrait.tex"
REPORT_PDF = ROOT / "outputs" / "ShenRuililin_Laidlaw_Stage3Report.pdf"
POSTER_PDF = ROOT / "outputs" / "ShenRuililin_Laidlaw_Stage3Poster.pdf"
REPORT_COPY = ROOT / "reports" / "laidlaw_stage3" / "ShenRuililin_Laidlaw_Stage3Report.pdf"
POSTER_COPY = ROOT / "reports" / "poster" / "ShenRuililin_Laidlaw_Stage3Poster.pdf"

# Filled after the 24 Aug rebuild. Update if Bob authorises another rebuild.
REPORT_SHA_PREFIX = "605cd8db43072cb5"
POSTER_SHA_PREFIX = "a972206e61932650"

BANNED = (
    "core panel",
    "twelve core",
    "12-core",
    "core count ratios",
    "machine-validated",
    "privacy-protected",
)

REQUIRED_NUMBERS = (
    "156,156",
    "29,681",
    "1.022",
    "1.073",
    "0.192",
    "1.011",
    "1.113",
)


def _essay() -> str:
    return ESSAY_MD.read_text(encoding="utf-8")


def _poster() -> str:
    return POSTER_TEX.read_text(encoding="utf-8")


def _intro_to_conclusion_words() -> int:
    text = _essay()
    if text.startswith("---"):
        text = text.split("---", 2)[2]
    start = text.find("# Introduction")
    end = text.find("# Acknowledgements")
    body = text[start:end]
    body = re.sub(r"```\{=latex\}.*?```", " ", body, flags=re.S)
    body = re.sub(r"!\[[^\]]*\]\([^)]+\)(?:\{[^}]*\})?", " ", body)
    return len(re.findall(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*", body))


def test_essay_names_nested_models_and_refuses_invention():
    text = _essay().lower()
    assert "model 1" in text and "model 2" in text and "model 3" in text
    assert "reported estimates are from model 1" in text
    assert "have not been fitted" in text
    assert "no health coefficients are invented" in text
    for phrase in BANNED:
        assert phrase not in text
    for num in REQUIRED_NUMBERS:
        assert num in _essay()
    assert "gate 3" not in text
    assert "stroke series was named" in text or "stroke series was not delivered" in text


def test_essay_word_count_in_programme_band():
    n = _intro_to_conclusion_words()
    assert 2000 <= n <= 3000, n


def test_poster_is_model1_shown_model23_specified():
    tex = _poster()
    low = tex.lower()
    assert "Model 1" in tex
    assert "Model 2" in tex and "Model 3" in tex
    assert "specified, not shown" in low or "specified, not shown" in tex.lower()
    for phrase in BANNED:
        assert phrase not in low
    assert "machine-validated" not in low
    assert "privacy-protected" not in low
    assert "shenrll@connect.hku.hk" in tex or "shen ruililin" in low
    assert "1.022" in tex and "1.073" in tex
    assert "0.192" in tex


def test_pdfs_exist_and_match_copies():
    assert REPORT_PDF.is_file() and POSTER_PDF.is_file()
    assert REPORT_COPY.read_bytes() == REPORT_PDF.read_bytes()
    assert POSTER_COPY.read_bytes() == POSTER_PDF.read_bytes()


def test_pdf_hashes_after_rebuild():
    if REPORT_SHA_PREFIX.startswith("PENDING"):
        return
    report = hashlib.sha256(REPORT_PDF.read_bytes()).hexdigest()
    poster = hashlib.sha256(POSTER_PDF.read_bytes()).hexdigest()
    assert report.startswith(REPORT_SHA_PREFIX)
    assert poster.startswith(POSTER_SHA_PREFIX)


def test_poster_pdf_is_one_a0_page():
    if not POSTER_PDF.is_file():
        raise AssertionError("poster PDF missing")
    info = subprocess.check_output(["pdfinfo", str(POSTER_PDF)], text=True)
    assert re.search(r"Pages:\s+1\b", info)
    # ISO A0 portrait is 841 x 1189 mm; pdfinfo reports bp.
    m = re.search(r"Page size:\s+([0-9.]+)\s+x\s+([0-9.]+)", info)
    assert m, info
    w, h = float(m.group(1)), float(m.group(2))
    assert 2300 < w < 2500, w
    assert 3300 < h < 3500, h
    assert h > w
