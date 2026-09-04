#!/usr/bin/env python3
"""Build the Thursday table-stack PDF for Professor Bishai.

Does not rebuild the Stage 3 essay. Reads the locked 24 August PDF and the
already-rendered supervisor one-pager, then writes a 4-page A4 staple:

1. supervisor one-pager (optional comments paste)
2. essay title / Abstract (page 1)
3. Model 1 Table 2 (page 6)
4. Conclusion + Acknowledgements (page 9)

Run from the repository root:

    python3 scripts/65_bishai_thursday_print_bundle.py

Bob still prints form 2a from his local Word file. Do not attach the live
manuscript. Hogan does not sign this stack.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
ESSAY = ROOT / "outputs" / "ShenRuililin_Laidlaw_Stage3Report.pdf"
ONEPAGER = ROOT / "analysis_plan" / "send_pack_2026-08-25" / "supervisor_one_pager.pdf"
OUT = ROOT / "analysis_plan" / "send_pack_2026-08-25" / "thursday_table_stack.pdf"
ESSAY_SHA_PREFIX = "605cd8db43072cb5"
# 1-based pages in the locked essay.
ESSAY_PAGES = (1, 6, 9)


def main() -> int:
    if not ESSAY.is_file():
        print(f"missing {ESSAY}", file=sys.stderr)
        return 1
    if not ONEPAGER.is_file():
        print(f"missing {ONEPAGER}", file=sys.stderr)
        return 1
    digest = hashlib.sha256(ESSAY.read_bytes()).hexdigest()
    if not digest.startswith(ESSAY_SHA_PREFIX):
        print(
            f"essay SHA prefix {digest[:16]} != {ESSAY_SHA_PREFIX}; "
            "refusing to slice a different PDF",
            file=sys.stderr,
        )
        return 1

    out = pymupdf.open()
    one = pymupdf.open(ONEPAGER)
    if one.page_count != 1:
        print(f"one-pager has {one.page_count} pages, expected 1", file=sys.stderr)
        return 1
    out.insert_pdf(one)
    one.close()

    essay = pymupdf.open(ESSAY)
    for page_no in ESSAY_PAGES:
        idx = page_no - 1
        if idx < 0 or idx >= essay.page_count:
            print(f"essay has no page {page_no}", file=sys.stderr)
            return 1
        out.insert_pdf(essay, from_page=idx, to_page=idx)
    essay.close()

    if out.page_count != 4:
        print(f"stack has {out.page_count} pages, expected 4", file=sys.stderr)
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.save(OUT, deflate=True, garbage=4)
    out.close()
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
