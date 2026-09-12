#!/usr/bin/env python3
"""Build the covid_period candidate manuscript (Word, PDF, page map).

Wording authority: manuscript/covid_period/Manuscript_covid_period_draft.md

Print contract (differs from scripts/77_hogan_20260910_live_docx.py, which forces
a page break after every table and every figure):

  1. No unconditional page break after a float.
  2. A caption is kept with the float it introduces, and the prose paragraph that
     names the float is kept with the caption.
  3. A table stays whole: rows cannot split, and every row but the last keeps with
     the next row, so Word/LibreOffice moves the caption and table together to the
     next page only when they do not fit on the current one.
  4. Only the reference list may start a new page, and only when FLOAT_CONTRACT
     says so.

The script reads no governed panel and fits no health model. Hogan's HKO paragraph
is copied verbatim and asserted, including the averaging sentence. It writes only
inside manuscript/covid_period/ and never into manuscript/live_collaborative/ or
manuscript/archive/.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Mm, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
COVID_DIR = ROOT / "manuscript" / "covid_period"
MAIN_MD = COVID_DIR / "Manuscript_covid_period_draft.md"
MAIN_DOCX = COVID_DIR / "Heat_CVD_Manuscript_covid_period.docx"
MAIN_PDF = COVID_DIR / "Heat_CVD_Manuscript_covid_period.pdf"
PAGE_MAP = COVID_DIR / "PRINT_PAGE_MAP.md"
LIVE_PDF = ROOT / "manuscript" / "live_collaborative" / "Heat_CVD_Manuscript_20260910_hogan.pdf"

RUNNING_TITLE = "Window dependence of first CHD/HF hospitalisation"

# A4 with 2.54 cm margins: the text column is the page height less both margins.
PAGE_MARGIN_PT = 72.0

HOGAN_OPEN = "Meteorological data was obtained from the HKO."
HOGAN_AVG = (
    "All monthly data were derived by taking the average of daily data in each calendar month."
)

FORBIDDEN_BODY = (
    "Gate 3",
    "Hogan asked",
    "health improved",
    "admissions averted",
    "failing left ventricle",
    "TWFE",
    "Callaway",
    "QALY",
    "SYNTHETIC_THEORY",
)

# Structural page breaks this builder is allowed to emit. Both are off: the word
# processor decides where pages end, guided by keep-with-next and keep-together.
FLOAT_CONTRACT = {"page_break_before_references": False}

# Rendered height caps in inches, chosen so that a caption and its figure fit under
# body text rather than claiming a page of their own.
FIGURE_MAX_HEIGHT = {"Figure 1.": 4.4, "Figure 2.": 4.4, "Figure 3.": 4.2}
FIGURE_DEFAULT_MAX_HEIGHT = 4.4

TOKEN = re.compile(
    r"(\*\*.+?\*\*|T~min~|T~max~|NO~2~|SO~2~|O~3~|PM~2\.5~|"
    r"\^[^\s^]{1,10}\^|\\\(.+?\\\)|`[^`]+`|\*[^*]+\*)"
)


def set_run_font(
    run,
    *,
    italic: bool = False,
    bold: bool = False,
    size: float = 12,
    color=None,
    superscript: bool = False,
    subscript: bool = False,
) -> None:
    run.italic = italic
    run.bold = bold
    run.font.name = "Times New Roman"
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "Times New Roman")
    run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = color
    run.font.superscript = superscript
    run.font.subscript = subscript


def set_paragraph_format(
    paragraph,
    *,
    first_line: bool = True,
    space_after: float = 8,
    space_before: float = 0,
    align: str = "left",
) -> None:
    pf = paragraph.paragraph_format
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    pf.first_line_indent = Cm(1.27) if first_line else Cm(0)
    if align == "center":
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == "justify":
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    elif align == "right":
        paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    else:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT


def add_page_number(paragraph) -> None:
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    finish = OxmlElement("w:fldChar")
    finish.set(qn("w:fldCharType"), "end")
    run._r.extend((begin, instr, finish))
    set_run_font(run, size=10, italic=True)


def configure_document(doc: Document, header_text: str, *, body_size: float) -> None:
    section = doc.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)
    section.header_distance = Cm(1.25)
    section.footer_distance = Cm(1.25)

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    normal.font.size = Pt(body_size)

    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    hp.clear()
    set_paragraph_format(hp, first_line=False, space_after=0)
    run = hp.add_run(header_text)
    set_run_font(run, italic=True, size=10, color=RGBColor(0x55, 0x55, 0x55))
    tab_run = hp.add_run("\t")
    set_run_font(tab_run, size=10)
    add_page_number(hp)
    tabs = OxmlElement("w:tabs")
    tab = OxmlElement("w:tab")
    tab.set(qn("w:val"), "right")
    tab.set(qn("w:pos"), "9360")
    tabs.append(tab)
    hp._p.get_or_add_pPr().append(tabs)


def _inline_math(text: str) -> str:
    text = re.sub(r"\\mathrm\{([^}]+)\}", r"\1", text)
    return text.replace("\\,", "").replace("\\", "")


def add_rich_runs(paragraph, text: str, *, size: float, italic: bool = False):
    subs = {
        "T~min~": ("T", "min"),
        "T~max~": ("T", "max"),
        "NO~2~": ("NO", "2"),
        "SO~2~": ("SO", "2"),
        "O~3~": ("O", "3"),
        "PM~2.5~": ("PM", "2.5"),
    }
    runs = []
    pos = 0
    for match in TOKEN.finditer(text):
        if match.start() > pos:
            run = paragraph.add_run(text[pos : match.start()])
            set_run_font(run, size=size, italic=italic)
            runs.append(run)
        token = match.group(0)
        if token in subs:
            base, sub = subs[token]
            base_run = paragraph.add_run(base)
            set_run_font(base_run, size=size, italic=italic)
            sub_run = paragraph.add_run(sub)
            set_run_font(sub_run, size=size, italic=italic, subscript=True)
            runs.extend((base_run, sub_run))
        elif token.startswith("**") and token.endswith("**"):
            run = paragraph.add_run(token[2:-2])
            set_run_font(run, size=size, bold=True, italic=italic)
            runs.append(run)
        elif token.startswith("^") and token.endswith("^"):
            run = paragraph.add_run(token[1:-1])
            set_run_font(run, size=size, superscript=True, italic=italic)
            runs.append(run)
        elif token.startswith(r"\(") and token.endswith(r"\)"):
            run = paragraph.add_run(_inline_math(token[2:-2]))
            set_run_font(run, size=size, italic=True)
            runs.append(run)
        elif token.startswith("`") and token.endswith("`"):
            run = paragraph.add_run(token[1:-1])
            set_run_font(run, size=size, italic=True)
            runs.append(run)
        elif token.startswith("*") and token.endswith("*"):
            run = paragraph.add_run(token[1:-1])
            set_run_font(run, size=size, italic=True)
            runs.append(run)
        else:
            run = paragraph.add_run(token)
            set_run_font(run, size=size, italic=italic)
            runs.append(run)
        pos = match.end()
    if pos < len(text):
        run = paragraph.add_run(text[pos:])
        set_run_font(run, size=size, italic=italic)
        runs.append(run)
    return runs


def add_body(
    doc: Document,
    text: str,
    *,
    size: float,
    first_line: bool = True,
    italic: bool = False,
    align: str = "justify",
):
    p = doc.add_paragraph()
    set_paragraph_format(p, first_line=first_line, space_after=8, align=align)
    runs = add_rich_runs(p, text, size=size, italic=italic)
    return p, runs


def add_heading(doc: Document, text: str, level: int, *, size: float, new_page: bool = False):
    p = doc.add_paragraph()
    set_paragraph_format(
        p,
        first_line=False,
        space_before=0 if new_page else (12 if level == 1 else 8),
        space_after=6,
    )
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.keep_together = True
    if new_page:
        p.paragraph_format.page_break_before = True
    run = p.add_run(text)
    if level == 1:
        set_run_font(run, bold=True, size=size + 2)
    elif level == 2:
        set_run_font(run, bold=True, size=size)
    else:
        set_run_font(run, bold=True, italic=True, size=size)
    return p, run


def add_caption(doc: Document, text: str, *, size: float):
    """A caption never forces a page break; it travels with its float."""
    p = doc.add_paragraph()
    set_paragraph_format(p, first_line=False, space_after=6)
    p.paragraph_format.keep_together = True
    p.paragraph_format.keep_with_next = True
    runs = add_rich_runs(p, text, size=size, italic=True)
    return p, runs


def _set_cell_margins(cell, top=40, bottom=40, left=55, right=55) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = OxmlElement("w:tcMar")
    for edge, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        node = OxmlElement(f"w:{edge}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tc_mar.append(node)
    tc_pr.append(tc_mar)


def _row_cant_split(row) -> None:
    row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))


def _row_repeat_header(row) -> None:
    row._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))


def clean_cell(text: str) -> str:
    text = text.replace("**", "").replace("`", "")
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = text.replace("T~min~", "Tmin").replace("T~max~", "Tmax")
    text = text.replace("NO~2~", "NO₂").replace("SO~2~", "SO₂")
    text = text.replace("O~3~", "O₃").replace("PM~2.5~", "PM₂.₅")
    return text.strip()


def parse_table(lines: list[str]) -> tuple[list[str], list[list[str]]]:
    content = [line for line in lines if set(line.strip()) - set("|:- ")]
    rows = [
        [clean_cell(cell) for cell in line.strip().strip("|").split("|")] for line in content
    ]
    if len(rows) < 2:
        raise ValueError(f"invalid markdown table: {lines!r}")
    return rows[0], rows[1:]


def add_table(
    doc: Document,
    headers: list[str],
    rows: list[list[str]],
    *,
    font_size: float,
    widths: list[float] | None = None,
) -> None:
    """Emit a table that stays whole rather than one that owns a page.

    Rows cannot split, and every row but the last keeps with the following row.
    The word processor therefore moves the caption and the table together onto the
    next page only when they do not fit below the paragraph that names them.
    """
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.autofit = False
    tbl_pr = table._tbl.tblPr
    for child in list(tbl_pr):
        if child.tag == qn("w:tblW"):
            tbl_pr.remove(child)
    tbl_w = OxmlElement("w:tblW")
    tbl_w.set(qn("w:w"), "5000")
    tbl_w.set(qn("w:type"), "pct")
    tbl_pr.append(tbl_w)
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tbl_pr.append(layout)

    if widths and len(widths) == len(headers):
        grid = table._tbl.find(qn("w:tblGrid"))
        if grid is not None:
            table._tbl.remove(grid)
        grid = OxmlElement("w:tblGrid")
        for width in widths:
            col = OxmlElement("w:gridCol")
            col.set(qn("w:w"), str(int(width * 1440)))
            grid.append(col)
        table._tbl.tblPr.addnext(grid)

    all_rows = [headers] + rows
    last_index = len(all_rows) - 1
    for row_idx, (row, values) in enumerate(zip(table.rows, all_rows)):
        _row_cant_split(row)
        if row_idx == 0:
            _row_repeat_header(row)
        for col_idx, value in enumerate(values):
            cell = row.cells[col_idx]
            cell.text = ""
            _set_cell_margins(cell)
            if widths and len(widths) == len(headers):
                cell.width = Inches(widths[col_idx])
            p = cell.paragraphs[0]
            set_paragraph_format(p, first_line=False, space_after=1, space_before=1)
            p.paragraph_format.keep_together = True
            p.paragraph_format.keep_with_next = row_idx < last_index
            run = p.add_run(value)
            set_run_font(run, bold=row_idx == 0, size=font_size)
    # A thin separator keeps the following caption off the table border without
    # spending a full body line of vertical space.
    spacer = doc.add_paragraph()
    set_paragraph_format(spacer, first_line=False, space_after=6)
    set_run_font(spacer.add_run(""), size=2)


def add_picture(doc: Document, path: Path, *, width: float, max_height: float) -> None:
    """Place a figure inline. The picture paragraph is never followed by a break."""
    from PIL import Image

    with Image.open(path) as image:
        px_w, px_h = image.size
    final_width = width
    if final_width * px_h / px_w > max_height:
        final_width = max_height * px_w / px_h
    p = doc.add_paragraph()
    set_paragraph_format(p, first_line=False, space_after=8, align="center")
    p.paragraph_format.keep_together = True
    run = p.add_run()
    run.add_picture(str(path), width=Inches(final_width))


def parse_blocks(markdown: str) -> list[tuple[str, list[str]]]:
    lines = markdown.splitlines()
    blocks: list[tuple[str, list[str]]] = []
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        if not line.strip():
            idx += 1
            continue
        for prefix, kind in (("#### ", "h3"), ("### ", "h2"), ("## ", "h1"), ("# ", "h0")):
            if line.startswith(prefix):
                blocks.append((kind, [line[len(prefix) :].strip()]))
                idx += 1
                break
        else:
            if line.startswith("!["):
                blocks.append(("image", [line]))
                idx += 1
                continue
            if line.startswith("|"):
                table_lines = []
                while idx < len(lines) and lines[idx].startswith("|"):
                    table_lines.append(lines[idx])
                    idx += 1
                blocks.append(("table", table_lines))
                continue
            if line.startswith("\\["):
                equation_lines = [line]
                idx += 1
                while idx < len(lines) and not lines[idx].strip().endswith("\\]"):
                    equation_lines.append(lines[idx])
                    idx += 1
                if idx < len(lines):
                    equation_lines.append(lines[idx])
                    idx += 1
                blocks.append(("equation", equation_lines))
                continue
            paragraph = [line]
            idx += 1
            while (
                idx < len(lines)
                and lines[idx].strip()
                and not lines[idx].startswith(("#", "|", "![", "\\["))
            ):
                paragraph.append(lines[idx])
                idx += 1
            blocks.append(("paragraph", paragraph))
    return blocks


def _comment(doc: Document, run, text: str) -> None:
    doc.add_comment(run, text, author="Bob Shen", initials="BS")


def _find_run(runs, needle: str):
    return next((run for run in runs if needle in run.text), runs[0] if runs else None)


def _table_widths(caption_text: str, columns: int) -> list[float] | None:
    if caption_text.startswith("Table 1."):
        return [1.25, 0.75, 0.45, 0.80, 0.70, 2.15]
    if caption_text.startswith("Table 2."):
        return [0.85, 1.45, 1.90, 1.90]
    if caption_text.startswith("Table 3."):
        return [0.85, 2.05, 1.55, 0.85, 0.80]
    if caption_text.startswith("Table 5."):
        return [0.80, 1.55, 1.25, 1.25, 1.25]
    if columns:
        return [6.1 / columns] * columns
    return None


def _equation_text(_lines: list[str]) -> str:
    return (
        "log E(Yₜ) = log(dₜ) + α + βXₜ + "
        "Σₘ₌₂¹² γₘ I(monthₜ = m) + s(t; 4 df).    (1)"
    )


BODY_WIDTH_IN = 6.27
CAPTION_CHARS_PER_LINE = 95
CAPTION_LINE_IN = 0.16
TABLE_ROW_IN = 0.17
CHAIN_LIMIT_IN = 3.5


def _caption_height(text: str) -> float:
    lines = max(1, -(-len(text) // CAPTION_CHARS_PER_LINE))
    return lines * CAPTION_LINE_IN + 0.1


def _image_height(path: Path, *, width: float, max_height: float) -> float:
    from PIL import Image

    with Image.open(path) as image:
        px_w, px_h = image.size
    return min(width * px_h / px_w, max_height)


def _float_block_height(blocks: list[tuple[str, list[str]]], caption_index: int) -> float:
    """Estimate the printed height of a caption plus the float it introduces."""
    kind, lines = blocks[caption_index]
    caption = clean_cell(" ".join(line.strip() for line in lines))
    height = _caption_height(caption)
    if caption_index + 1 >= len(blocks):
        return height
    next_kind, next_lines = blocks[caption_index + 1]
    if next_kind == "table":
        headers, rows = parse_table(next_lines)
        height += (1 + len(rows)) * TABLE_ROW_IN + 0.15
    elif next_kind == "image":
        match = re.search(r"!\[([^\]]*)\]\(([^)]+)\)", next_lines[0])
        if match:
            path = (MAIN_MD.parent / match.group(2)).resolve()
            cap = next(
                (v for label, v in FIGURE_MAX_HEIGHT.items() if caption.startswith(label)),
                FIGURE_DEFAULT_MAX_HEIGHT,
            )
            if path.is_file():
                height += _image_height(path, width=6.1, max_height=cap) + 0.15
    return height


def _chain_with_caption(blocks: list[tuple[str, list[str]]], index: int) -> bool:
    """Should this paragraph be kept on the same page as the float it names?

    Yes for a short float, so the reader meets the table beside the sentence that
    introduces it. No for a tall float, because an unbreakable chain of prose plus a
    full-width figure is what strands a third of a page.
    """
    if index + 1 >= len(blocks):
        return False
    kind, lines = blocks[index + 1]
    if kind != "paragraph":
        return False
    caption = clean_cell(" ".join(line.strip() for line in lines))
    if not caption.startswith(("Table ", "Figure ")):
        return False
    return _float_block_height(blocks, index + 1) <= CHAIN_LIMIT_IN


def build_main() -> None:
    markdown = MAIN_MD.read_text(encoding="utf-8")
    if HOGAN_OPEN not in markdown or HOGAN_AVG not in markdown:
        raise AssertionError("Hogan weather paragraph drifted")
    for phrase in FORBIDDEN_BODY:
        if phrase.lower() in markdown.lower():
            raise AssertionError(f"forbidden main-body phrase: {phrase}")

    doc = Document()
    configure_document(doc, RUNNING_TITLE, body_size=12)

    blocks = parse_blocks(markdown)
    pending_caption = ""
    references = False

    for index, (kind, lines) in enumerate(blocks):
        if kind == "h0":
            p = doc.add_paragraph()
            set_paragraph_format(p, first_line=False, space_after=6, align="center")
            p.paragraph_format.keep_with_next = True
            run = p.add_run(lines[0])
            set_run_font(run, bold=True, size=16)
            continue

        if kind == "h1":
            text = lines[0]
            references = text == "References"
            new_page = references and FLOAT_CONTRACT["page_break_before_references"]
            add_heading(doc, text, 1, size=12, new_page=new_page)
            continue

        if kind in ("h2", "h3"):
            add_heading(doc, lines[0], 2 if kind == "h2" else 3, size=12)
            continue

        if kind == "equation":
            p = doc.add_paragraph()
            set_paragraph_format(p, first_line=False, space_after=8, align="center")
            run = p.add_run(_equation_text(lines))
            set_run_font(run, italic=True, size=12)
            continue

        if kind == "table":
            headers, rows = parse_table(lines)
            add_table(
                doc,
                headers,
                rows,
                font_size=9,
                widths=_table_widths(pending_caption, len(headers)),
            )
            pending_caption = ""
            continue

        if kind == "image":
            match = re.search(r"!\[([^\]]*)\]\(([^)]+)\)", lines[0])
            if not match:
                raise ValueError(f"invalid image markdown: {lines[0]}")
            path = (MAIN_MD.parent / match.group(2)).resolve()
            if not path.is_file():
                raise FileNotFoundError(path)
            max_height = next(
                (cap for label, cap in FIGURE_MAX_HEIGHT.items() if pending_caption.startswith(label)),
                FIGURE_DEFAULT_MAX_HEIGHT,
            )
            add_picture(doc, path, width=6.1, max_height=max_height)
            pending_caption = ""
            continue

        text = " ".join(line.strip() for line in lines)
        plain = clean_cell(text)

        if plain.startswith("Running title:"):
            add_body(doc, plain, size=11, first_line=False, italic=True, align="center")
            continue

        if plain.startswith("Candidate article."):
            add_body(doc, plain, size=10.5, first_line=False, italic=True, align="center")
            continue

        if plain.startswith("Bob Ruililin Shen"):
            _, runs = add_body(doc, text, size=12, first_line=False, align="center")
            author_run = _find_run(runs, "Author 2")
            if author_run is not None:
                _comment(
                    doc,
                    author_run,
                    "Author order after the first and last positions remains for "
                    "Professor Bishai and the team to confirm.",
                )
            continue

        if plain.startswith("1 School of Public Health"):
            add_body(doc, text, size=10, first_line=False, italic=True, align="center")
            continue

        if plain.startswith(("Table ", "Figure ")):
            _, runs = add_caption(doc, plain, size=11)
            pending_caption = plain
            if plain.startswith("Table 2.") and runs:
                _comment(
                    doc,
                    runs[0],
                    "The 84-month window is contained in the full window. These are "
                    "nested sensitivity fits, not independent period estimates.",
                )
            continue

        if references and re.match(r"^\d+\.", plain):
            p = doc.add_paragraph()
            set_paragraph_format(p, first_line=False, space_after=3, align="left")
            p.paragraph_format.left_indent = Cm(0.75)
            p.paragraph_format.first_line_indent = Cm(-0.75)
            add_rich_runs(p, text, size=11)
            continue

        first_line = not text.startswith("**")
        p, runs = add_body(doc, text, size=12, first_line=first_line)
        # Keep the last line of a paragraph with the short float it introduces.
        p.paragraph_format.keep_with_next = _chain_with_caption(blocks, index)
        low = plain.lower()
        if plain.startswith("Methods.") and runs:
            _comment(
                doc,
                runs[0],
                "The 84-month fit is a nested-window sensitivity. No 2020–2023-only "
                "Model 1 and no exposure-by-period interaction is reported.",
            )
        if "uw xx-xxx" in low and runs:
            _comment(
                doc,
                _find_run(runs, "UW XX-XXX"),
                "Professor Bishai should replace the IRB reference UW XX-XXX with the "
                "approved number before submission.",
            )
        if plain.startswith("The dependent variable is") and runs:
            _comment(
                doc,
                runs[0],
                "Roro should confirm the written ICD inclusion list, first-event timing, "
                "and inpatient-versus-DAE construction before submission.",
            )
        if HOGAN_OPEN in plain and runs:
            _comment(
                doc,
                runs[0],
                "Hogan's meteorological wording is retained verbatim, including the "
                "averaging sentence.",
            )
        if plain.startswith("Model 2 additionally") and runs:
            _comment(
                doc,
                runs[0],
                "Model 2 and Model 3 are specified; no new coefficients are added "
                "because the governed panels are not present here.",
            )
        if "laboratory measurements were not in the transfer" in low and runs:
            _comment(
                doc,
                runs[0],
                "Laboratory, infection, vaccination, and serology fields would require a "
                "new governed extract if Professor Bishai opens that scope.",
            )
        if plain.startswith("Read as the ruling-out exhibit") and runs:
            _comment(
                doc,
                runs[0],
                "Interval overlap between the nested and full windows is not a formal "
                "test of a coefficient difference.",
            )

    MAIN_DOCX.parent.mkdir(parents=True, exist_ok=True)
    doc.save(MAIN_DOCX)
    print(f"wrote {MAIN_DOCX} ({MAIN_DOCX.stat().st_size} bytes)")


def _office_binary() -> str:
    binary = shutil.which("soffice") or shutil.which("libreoffice")
    if binary is None:
        raise SystemExit(
            "LibreOffice is required to build the PDF. Install libreoffice-writer and rerun."
        )
    return binary


def convert_pdf(docx_path: Path, pdf_path: Path) -> None:
    binary = _office_binary()
    if pdf_path.exists():
        pdf_path.unlink()
    with tempfile.TemporaryDirectory(prefix=f"lo-{docx_path.stem}-") as profile:
        cmd = [
            binary,
            f"-env:UserInstallation=file://{profile}",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(pdf_path.parent),
            str(docx_path),
        ]
        proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if proc.returncode != 0 or not pdf_path.is_file():
        raise SystemExit(
            f"LibreOffice conversion failed ({proc.returncode}): {proc.stdout}\n{proc.stderr}"
        )
    print(f"wrote {pdf_path} ({pdf_path.stat().st_size} bytes)")


def _norm(text: str) -> str:
    return " ".join(text.replace("\u00ad", "").split()).replace("–", "-").replace("—", "-")


@dataclass
class PageFacts:
    number: int
    fill: float
    floats: list[str]
    opens_with: str
    images: int


FLOAT_LABELS = (
    "Table 1.",
    "Table 2.",
    "Table 3.",
    "Table 4.",
    "Table 5.",
    "Figure 1.",
    "Figure 2.",
    "Figure 3.",
)


def page_facts(pdf_path: Path) -> list[PageFacts]:
    """Measure how much of each page carries content.

    Text blocks and image blocks both count, so a page holding only a figure is not
    scored as empty. The running header sits in the top 6% of the page and is excluded.
    """
    import pymupdf

    facts: list[PageFacts] = []
    with pymupdf.open(pdf_path) as pdf:
        for index, page in enumerate(pdf, start=1):
            height = page.rect.height
            boxes = [
                block["bbox"]
                for block in page.get_text("dict")["blocks"]
                if block["bbox"][1] > 0.06 * height
            ]
            boxes += [
                info["bbox"]
                for info in page.get_image_info()
                if info["bbox"][1] > 0.06 * height
            ]
            lowest = max((box[3] for box in boxes), default=0.0)
            highest = min((box[1] for box in boxes), default=0.0)
            column = height - 2 * PAGE_MARGIN_PT
            text = _norm(page.get_text())
            floats = [label for label in FLOAT_LABELS if label.replace(".", ".") in text]
            facts.append(
                PageFacts(
                    number=index,
                    fill=round((lowest - highest) / column, 3),
                    floats=floats,
                    opens_with=text[:70],
                    images=len(page.get_images(full=True)),
                )
            )
    return facts


def _fill_summary(facts: list[PageFacts]) -> dict:
    interior = facts[:-1] if len(facts) > 1 else facts
    fills = [f.fill for f in interior]
    return {
        "pages": len(facts),
        "mean_fill_interior": round(sum(fills) / len(fills), 3) if fills else 0.0,
        "min_fill_interior": min(fills) if fills else 0.0,
        "pages_below_60pct": [f.number for f in interior if f.fill < 0.60],
        "pages_below_45pct": [f.number for f in interior if f.fill < 0.45],
    }


def write_page_map() -> dict:
    facts = page_facts(MAIN_PDF)
    summary = _fill_summary(facts)

    lines: list[str] = []
    lines.append("# Print page map — covid_period candidate manuscript")
    lines.append("")
    lines.append(
        "Generated by [`../../scripts/78_covid_period_manuscript_docx.py`]"
        "(../../scripts/78_covid_period_manuscript_docx.py). Fill is the vertical span of "
        "text and image blocks on the page divided by page height, excluding the running "
        "header. It is a whitespace diagnostic, not a typesetting standard."
    )
    lines.append("")
    lines.append(f"**Source:** [`{MAIN_MD.name}`]({MAIN_MD.name}) → `{MAIN_DOCX.name}` → `{MAIN_PDF.name}`")
    lines.append("")
    lines.append(
        f"**Pages:** {summary['pages']}. **Mean fill (excluding the last page):** "
        f"{summary['mean_fill_interior']:.2f}. **Interior pages below 0.60 fill:** "
        f"{summary['pages_below_60pct'] or 'none'}. **Interior pages below 0.45 fill:** "
        f"{summary['pages_below_45pct'] or 'none'}."
    )
    lines.append("")
    lines.append("| Page | Fill | Floats on page | Opens with |")
    lines.append("|---:|---:|---|---|")
    for fact in facts:
        floats = ", ".join(fact.floats) if fact.floats else "—"
        lines.append(f"| {fact.number} | {fact.fill:.2f} | {floats} | {fact.opens_with.strip()} |")
    lines.append("")

    lines.append("## Float contract")
    lines.append("")
    lines.append(
        "- No page break is emitted after a table or a figure. The word processor breaks "
        "only when a caption plus its float will not fit."
    )
    lines.append("- Table rows cannot split, and every row but the last keeps with the next row.")
    lines.append("- A caption keeps with its float, and the paragraph that names the float keeps with the caption.")
    lines.append(
        "- The reference list is the only structural page break "
        f"(`FLOAT_CONTRACT['page_break_before_references'] = "
        f"{FLOAT_CONTRACT['page_break_before_references']}`)."
    )
    lines.append("")

    if LIVE_PDF.is_file():
        live = page_facts(LIVE_PDF)
        live_summary = _fill_summary(live)
        lines.append("## Comparison with the 10 September live PDF (read-only)")
        lines.append("")
        lines.append(
            "The live Hogan PDF is measured, not modified. It is built by "
            "`scripts/77_hogan_20260910_live_docx.py`, which forces a page break after "
            "every table and every figure."
        )
        lines.append("")
        lines.append("| PDF | Pages | Mean fill | Interior pages < 0.45 fill |")
        lines.append("|---|---:|---:|---:|")
        lines.append(
            f"| `{MAIN_PDF.name}` (this builder) | {summary['pages']} | "
            f"{summary['mean_fill_interior']:.2f} | {len(summary['pages_below_45pct'])} |"
        )
        lines.append(
            f"| `{LIVE_PDF.name}` (builder 77) | {live_summary['pages']} | "
            f"{live_summary['mean_fill_interior']:.2f} | {len(live_summary['pages_below_45pct'])} |"
        )
        lines.append("")
        summary["live_comparison"] = live_summary

    lines.append("## Limits")
    lines.append("")
    lines.append(
        "- Fill measures whitespace, not scientific quality. No numeral in the manuscript "
        "depends on this file."
    )
    lines.append(
        "- LibreOffice renders the Word file for this measurement. Word may break a page "
        "one line earlier or later; the float rules, not the exact page numbers, are the contract."
    )
    lines.append("- Nothing here was pasted into Hogan's shared Word file.")
    lines.append("")

    PAGE_MAP.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {PAGE_MAP}")
    return summary


def review_main(summary: dict) -> None:
    doc = Document(str(MAIN_DOCX))
    section = doc.sections[0]
    assert round(section.page_width.mm, 1) == 210.0
    assert round(section.page_height.mm, 1) == 297.0
    assert all(
        round(value.cm, 2) == 2.54
        for value in (
            section.top_margin,
            section.bottom_margin,
            section.left_margin,
            section.right_margin,
        )
    )
    assert len(list(doc.comments)) >= 6

    import pymupdf

    with pymupdf.open(MAIN_PDF) as pdf:
        page_texts = [_norm(page.get_text()) for page in pdf]
    full = "\n".join(page_texts)
    for required in (
        "Window dependence",
        HOGAN_OPEN,
        HOGAN_AVG,
        "Table 1. Outcome summary",
        "Table 2. Official-day count ratios",
        "Table 3. Model 1",
        "Table 4. Uncertainty ladder",
        "Table 5. Mean temperature",
        "Figure 1. First-event",
        "Figure 2. Official cold days",
        "Figure 3. Model 1 count ratios",
        "1.022 (1.002-1.042)",
        "1.073 (1.006-1.144)",
        "1.113 (1.053-1.176)",
        "not a measure of physiological improvement",
        "UW XX-XXX",
        "None.",
    ):
        assert required in full, required
    for forbidden in FORBIDDEN_BODY:
        assert forbidden.lower() not in full.lower(), forbidden

    def page_of(needle: str) -> int:
        hits = [idx for idx, text in enumerate(page_texts) if needle in text]
        assert hits, needle
        return hits[0]

    # A caption and its float share a page.
    for caption, marker in (
        ("Table 1. Outcome summary", "Coronary heart disease"),
        ("Table 2. Official-day count ratios", "Hot nights / 5 days"),
        ("Table 4. Uncertainty ladder", "CHD hot nights / 5 days"),
        ("Table 5. Mean temperature", "Mean temperature / 1 °C"),
    ):
        assert marker in page_texts[page_of(caption)], (caption, marker)

    # Tables are not split across pages.
    for label, first_cell, last_cell in (
        ("Table 1. Outcome summary", "Coronary heart disease", "Heart failure"),
        ("Table 2. Official-day count ratios", "Hot nights / 5 days", "Cold days / 5 days"),
        ("Table 3. Model 1", "Mean temperature / 1 °C", "Very hot days / 5 days"),
        ("Table 5. Mean temperature", "Mean temperature / 1 °C", "Cold days / 5 days"),
    ):
        page = page_of(label)
        assert first_cell in page_texts[page], (label, first_cell)
        assert last_cell in page_texts[page], (label, last_cell)

    assert summary["pages_below_45pct"] == [], summary["pages_below_45pct"]
    assert summary["mean_fill_interior"] >= 0.80, summary["mean_fill_interior"]
    print(
        f"main PDF checks passed ({summary['pages']} A4 pages, mean fill "
        f"{summary['mean_fill_interior']:.2f})"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-pdf",
        action="store_true",
        help="Build the Word file only (no LibreOffice, no page map).",
    )
    args = parser.parse_args(argv)
    build_main()
    if args.skip_pdf:
        return 0
    convert_pdf(MAIN_DOCX, MAIN_PDF)
    summary = write_page_map()
    review_main(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
