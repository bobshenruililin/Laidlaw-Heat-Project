"""Stage 3 poster logos: navy header, equal width, centred. Not a white plate."""
from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "reports" / "poster" / "Laidlaw_Stage3_A0_portrait.tex"
PDF = ROOT / "reports" / "poster" / "Laidlaw_Stage3_A0_portrait.pdf"
ESSAY = ROOT / "outputs" / "ShenRuililin_Laidlaw_Stage3Report.pdf"
REPO_ESSAY = "1200082a9e7c9caa"


def test_tex_navy_lockups_equal_width_centred():
    tex = TEX.read_text(encoding="utf-8")
    header = tex.split("\\begin{tcolorbox}[", 1)[1].split("\\end{tcolorbox}", 1)[0]
    assert "colback=Navy" in header
    assert "colframe=Navy" in header
    assert "white plate" not in header.lower() or "not a white plate" in tex.lower()
    assert header.count("width=0.88\\linewidth") == 2
    assert "\\centering" in header
    assert "assets/hku_logo.png" in header
    assert "assets/laidlaw_logo.png" in header
    assert "0.24\\linewidth" in header


def test_poster_pdf_one_a0_page_equal_logo_bboxes():
    info = subprocess.check_output(["pdfinfo", str(PDF)], text=True) if _has_pdfinfo() else ""
    doc = pymupdf.open(PDF)
    assert doc.page_count == 1
    page = doc[0]
    w, h = page.rect.width, page.rect.height
    assert 2300 < w < 2500, w
    assert 3300 < h < 3500, h
    assert h > w
    imgs = page.get_image_info(xrefs=True)
    # Header logos are the two rightmost images (largest x).
    logos = sorted(imgs, key=lambda b: b["bbox"][0], reverse=True)[:2]
    widths = [b["bbox"][2] - b["bbox"][0] for b in logos]
    mids = [(b["bbox"][0] + b["bbox"][2]) / 2 for b in logos]
    assert abs(widths[0] - widths[1]) < 0.5, widths
    assert abs(mids[0] - mids[1]) < 0.5, mids
    if info:
        assert re.search(r"Pages:\s+1\b", info)


def test_essay_pdf_untouched():
    digest = hashlib.sha256(ESSAY.read_bytes()).hexdigest()
    assert digest.startswith(REPO_ESSAY)


def _has_pdfinfo() -> bool:
    from shutil import which

    return which("pdfinfo") is not None


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("OK", name)
