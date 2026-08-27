#!/usr/bin/env python3
"""Extract PDF markup comments (sticky notes, highlights, text boxes).

Usage:
  python3 scripts/extract_pdf_annotations.py PATH.pdf

Prints one record per annotation. Exit 2 if the file is missing.
Does not invent comments: empty output means no readable markup.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pymupdf


def _content(annot: pymupdf.Annot) -> str:
    parts = []
    for attr in ("info",):
        info = getattr(annot, attr, None) or {}
        if isinstance(info, dict):
            for key in ("content", "title", "subject", "name"):
                val = info.get(key)
                if val:
                    parts.append(f"{key}: {val}")
    # Fallback fields used by some Acrobat exports
    for key in ("content",):
        val = getattr(annot, key, None)
        if val and str(val) not in "".join(parts):
            parts.append(str(val))
    return "\n".join(parts).strip()


def extract(path: Path) -> list[dict]:
    doc = pymupdf.open(path)
    rows = []
    for page_i, page in enumerate(doc, start=1):
        annot = page.first_annot
        while annot:
            info = annot.info or {}
            rect = annot.rect
            # Words under a highlight/underline, if any
            under = page.get_text("text", clip=rect) or ""
            rows.append(
                {
                    "page": page_i,
                    "type": annot.type[1] if annot.type else None,
                    "author": info.get("title") or "",
                    "subject": info.get("subject") or "",
                    "content": (info.get("content") or "").strip(),
                    "marked_text": " ".join(under.split()),
                }
            )
            annot = annot.next
    doc.close()
    return rows


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: extract_pdf_annotations.py PATH.pdf", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"MISSING: {path}", file=sys.stderr)
        return 2
    rows = extract(path)
    print(json.dumps({"path": str(path), "n_annotations": len(rows), "annotations": rows}, indent=2, ensure_ascii=False))
    if not rows:
        print(
            "NO_ANNOTATIONS: file opened but no markup comments were readable.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
