#!/usr/bin/env python3
"""Build a pandoc reference.docx matching the 15 Aug collab-draft look (A4)."""
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor, Twips
from docx.oxml import OxmlElement


def set_run_font(style, ascii_font, east_asia=None, size_pt=None, bold=None):
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    rFonts.set(qn("w:ascii"), ascii_font)
    rFonts.set(qn("w:hAnsi"), ascii_font)
    rFonts.set(qn("w:cs"), ascii_font)
    if east_asia:
        rFonts.set(qn("w:eastAsia"), east_asia)
    if size_pt is not None:
        sz = rPr.find(qn("w:sz"))
        if sz is None:
            sz = OxmlElement("w:sz")
            rPr.append(sz)
        sz.set(qn("w:val"), str(int(size_pt * 2)))
        szCs = rPr.find(qn("w:szCs"))
        if szCs is None:
            szCs = OxmlElement("w:szCs")
            rPr.append(szCs)
        szCs.set(qn("w:val"), str(int(size_pt * 2)))
    if bold is not None:
        b = rPr.find(qn("w:b"))
        if bold:
            if b is None:
                b = OxmlElement("w:b")
                rPr.append(b)
        else:
            if b is not None:
                rPr.remove(b)
    style.font.name = ascii_font
    if size_pt is not None:
        style.font.size = Pt(size_pt)
    if bold is not None:
        style.font.bold = bold
    style.font.color.rgb = RGBColor(0, 0, 0)


def set_spacing(style, before=0, after=0, line=1.15, align=None, first_line=None):
    pf = style.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = line
    if align is not None:
        pf.alignment = align
    if first_line is not None:
        pf.first_line_indent = Cm(first_line)


def main():
    out = Path("reports/laidlaw_stage3/stage3_reference.docx")
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.left_margin = Cm(2.5)
    sec.right_margin = Cm(2.5)
    sec.top_margin = Cm(2.5)
    sec.bottom_margin = Cm(2.5)
    sec.header_distance = Cm(1.25)
    sec.footer_distance = Cm(1.25)

    body = "Liberation Serif"
    head = "Liberation Sans"

    styles = doc.styles
    set_run_font(styles["Normal"], body, size_pt=11)
    set_spacing(styles["Normal"], before=0, after=8, line=1.15, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

    set_run_font(styles["Title"], head, size_pt=16, bold=True)
    set_spacing(styles["Title"], before=0, after=6, line=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
    styles["Title"].font.color.rgb = RGBColor(0, 0, 0)

    # Subtitle may or may not exist
    try:
        st = styles["Subtitle"]
        set_run_font(st, body, size_pt=12, bold=False)
        st.font.italic = True
        set_spacing(st, before=0, after=10, line=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
        st.font.color.rgb = RGBColor(0, 0, 0)
    except KeyError:
        pass

    for name, size, before, after in (
        ("Author", 11, 0, 0),
        ("Date", 10, 0, 12),
        ("Abstract", 11, 0, 8),
    ):
        try:
            st = styles[name]
            set_run_font(st, body, size_pt=size)
            set_spacing(st, before=before, after=after, line=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
        except KeyError:
            pass

    set_run_font(styles["Heading 1"], head, size_pt=13, bold=True)
    set_spacing(styles["Heading 1"], before=16, after=6, line=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
    styles["Heading 1"].font.color.rgb = RGBColor(0, 0, 0)

    set_run_font(styles["Heading 2"], head, size_pt=12, bold=True)
    set_spacing(styles["Heading 2"], before=12, after=4, line=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
    styles["Heading 2"].font.color.rgb = RGBColor(0, 0, 0)

    try:
        set_run_font(styles["Heading 3"], head, size_pt=11, bold=True)
        styles["Heading 3"].font.italic = True
        set_spacing(styles["Heading 3"], before=10, after=4, line=1.15)
        styles["Heading 3"].font.color.rgb = RGBColor(0, 0, 0)
    except KeyError:
        pass

    for name in ("Caption", "Image Caption", "Table Caption"):
        if name in [s.name for s in styles]:
            set_run_font(styles[name], body, size_pt=9, bold=True)
            set_spacing(styles[name], before=6, after=8, line=1.1, align=WD_ALIGN_PARAGRAPH.LEFT)

    if "Footnote Text" in [s.name for s in styles]:
        set_run_font(styles["Footnote Text"], body, size_pt=9)
        set_spacing(styles["Footnote Text"], before=0, after=2, line=1.1)

    # First paragraph / compact used by pandoc
    for name in ("First Paragraph", "Body Text", "Compact", "Block Text"):
        try:
            st = styles[name]
            set_run_font(st, body, size_pt=11)
            set_spacing(st, before=0, after=8, line=1.15, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        except KeyError:
            pass

    # Placeholder paragraph so Word saves the theme
    doc.add_paragraph("Reference document for Laidlaw Stage 3 (pandoc).")
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out)
    print("wrote", out, out.stat().st_size)


if __name__ == "__main__":
    main()
