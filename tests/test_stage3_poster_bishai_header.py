"""Stage 3 poster: Prof. David Bishai after Shen, same size; no collaborator footer.

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
POSTER_SHA_PREFIX = "7881d3a3e6f19640"


def _header_tex() -> str:
    tex = TEX.read_text(encoding="utf-8")
    return tex.split("\\begin{tcolorbox}[", 1)[1].split("\\end{tcolorbox}", 1)[0]


def test_tex_puts_bishai_after_shen_same_author_font():
    header = _header_tex()
    assert "Prof.~David Bishai" in header
    assert "SupervisorFont" not in TEX.read_text(encoding="utf-8")
    assert "Laidlaw Scholars Programme" not in header
    assert header.index("Shen Ruililin") < header.index("Prof.~David Bishai")
    footer = TEX.read_text(encoding="utf-8").split("REFERENCES", 1)[1]
    assert "Collaborators:" not in footer
    assert "Hogan" not in footer
    assert "Zhenyuan" not in footer
    assert "shenrll@connect.hku.hk" in footer


def test_pdf_header_shows_same_size_names_and_drops_collaborators():
    assert PDF.read_bytes() == PDF_A0.read_bytes() == PDF_COPY.read_bytes()
    digest = hashlib.sha256(PDF.read_bytes()).hexdigest()
    assert digest.startswith(POSTER_SHA_PREFIX)

    doc = pymupdf.open(PDF)
    assert doc.page_count == 1
    page = doc[0]
    text = page.get_text()
    assert "Prof. David Bishai" in text
    assert "Shen Ruililin" in text
    assert "Laidlaw Scholars" not in text
    assert "Hogan" not in text
    assert "Zhenyuan" not in text
    assert "Collaborators" not in text
    assert "shenrll@connect.hku.hk" in text
    assert "School of Public Health" in text

    shen = page.search_for("Shen Ruililin")[0]
    bishai = page.search_for("Prof. David Bishai")[0]
    assert shen.x0 < bishai.x0
    assert abs(shen.y0 - bishai.y0) < 1
    assert abs(shen.height - bishai.height) < 0.5
    assert shen.y0 < 400

    sizes = {}
    for block in page.get_text("dict")["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            for span in line["spans"]:
                if span["text"] in ("Shen Ruililin", "Prof. David Bishai"):
                    sizes[span["text"]] = span["size"]
    assert sizes["Shen Ruililin"] == sizes["Prof. David Bishai"]

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
