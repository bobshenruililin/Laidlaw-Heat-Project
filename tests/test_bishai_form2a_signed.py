"""Canonical Stage 3 hashes: signed foldback vs later outputs/ cut."""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMO = ROOT / "knowledge" / "2026-08-31_bishai_form2a_signed.md"
BOOT = ROOT / "knowledge" / "CONTEXT_BOOTSTRAP.md"
INDEX = ROOT / "knowledge" / "INDEX.md"
ESSAY = ROOT / "outputs" / "ShenRuililin_Laidlaw_Stage3Report.pdf"

SIGNED_ESSAY = "c083d4096a0924b1"
SIGNED_POSTER = "0ef58e0951bb2ffd"
HOGAN_ALIGN_ESSAY = "605cd8db43072cb5"
REPO_ESSAY = "1200082a9e7c9caa"
REPO_POSTER_PRE_LOGO = "a972206e61932650"


def test_hash_table_of_record():
    text = MEMO.read_text(encoding="utf-8")
    for prefix in (
        SIGNED_ESSAY,
        SIGNED_POSTER,
        HOGAN_ALIGN_ESSAY,
        REPO_ESSAY,
        REPO_POSTER_PRE_LOGO,
    ):
        assert prefix in text
    assert "Do not replace" in text
    assert "Gate 3" in text
    assert "Do not quote" in text
    assert "2026-08-31_bishai_form2a_signed.md" in INDEX.read_text(encoding="utf-8")


def test_bootstrap_points_at_memo():
    boot = BOOT.read_text(encoding="utf-8")
    assert "2026-08-31_bishai_form2a_signed.md" in boot
    assert "Form 2a is a human decision if already signed against" not in boot


def test_outputs_essay_is_later_cut_not_foldback():
    digest = hashlib.sha256(ESSAY.read_bytes()).hexdigest()
    assert digest.startswith(REPO_ESSAY)
    assert not digest.startswith(SIGNED_ESSAY)
    assert not digest.startswith(HOGAN_ALIGN_ESSAY)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("OK", name)
