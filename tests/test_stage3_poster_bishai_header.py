"""Stage 3 poster: Professor Bishai on the header, collaborators off the footer.

Bob authorised this authorship-only rebuild on 15 September 2026.
Science, figures, and the Stage 3 essay PDF are unchanged.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "reports" / "poster" / "Laidlaw_Stage3_A0_portrait.tex"
PDF = ROOT / "outputs" / "ShenRuililin_Laidlaw_Stage3Poster.pdf"
PDF_A0 = ROOT / "reports" / "poster" / "Laidlaw_Stage3_A0_portrait.pdf"
PDF_COPY = ROOT / "reports" / "poster" / "ShenRuililin_Laidlaw_Stage3Poster.pdf"
POSTER_SHA_PREFIX = "340f39cc301622bb"


def _header_tex() -> str:
    tex = TEX.read_text(encoding="utf-8")
    return tex.split("\\begin{tcolorbox}[", 1)[1].split("\\end{tcolorbox}", 1)[0]


def test_tex_puts_bishai_in_header_larger_than_student():
    header = _header_tex()
    assert "Professor David Bishai" in header
    assert "SupervisorFont" in header
    assert "\\fontsize{48}{56}" in TEX.read_text(encoding="utf-8")
    assert header.index("Shen Ruililin") < header.index("Professor David Bishai")
    footer = TEX.read_text(encoding="utf-8").split("REFERENCES", 1)[1]
    assert "Collaborators:" not in footer
    assert "Hogan" not in footer
    assert "Zhenyuan" not in footer
    assert "shenrll@connect.hku.hk" in footer


def test_pdf_header_shows_larger_bishai_and_drops_collaborators():
    assert PDF.read_bytes() == PDF_A0.read_bytes() == PDF_COPY.read_bytes()
    digest = hashlib.sha256(PDF.read_bytes()).hexdigest()
    assert digest.startswith(POSTER_SHA_PREFIX)

    doc = pymupdf.open(PDF)
    assert doc.page_count == 1
    page = doc[0]
    text = page.get_text()
    assert "Professor David Bishai" in text
    assert "Shen Ruililin" in text
    assert "Hogan" not in text
    assert "Zhenyuan" not in text
    assert "Collaborators" not in text
    assert "shenrll@connect.hku.hk" in text

    shen = page.search_for("Shen Ruililin")[0]
    bishai = page.search_for("Professor David Bishai")[0]
    assert bishai.y0 < 400, bishai
    assert shen.y0 < bishai.y0 < 400
    assert bishai.height > shen.height
    assert bishai.height > 40

    info = subprocess.check_output(["pdfinfo", str(PDF)], text=True)
    assert re.search(r"Pages:\s+1\b", info)
    m = re.search(r"Page size:\s+([0-9.]+)\s+x\s+([0-9.]+)", info)
    w, h = float(m.group(1)), float(m.group(2))
    assert 2300 < w < 2500 and 3300 < h < 3500 and h > w


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("OK", name)
