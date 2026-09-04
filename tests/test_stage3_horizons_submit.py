"""Horizons Stage 3 send pack: endorsed form + 22 Aug essay/poster; not the live manuscript."""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "analysis_plan" / "send_pack_2026-08-31"
KNOW = ROOT / "knowledge" / "2026-08-31_stage3_horizons_submit.md"
UPLOADS = Path("/home/ubuntu/.cursor/projects/workspace/uploads")

ESSAY_PREFIX = "c083d4096a0924b1"
POSTER_PREFIX = "0ef58e0951bb2ffd"
FORM_PREFIX = "722ba1f70f246c2d"
REPO_ESSAY_PREFIX = "1200082a9e7c9caa"
REPO_POSTER_PREFIX = "a972206e61932650"
HOGAN_UPLOAD_PREFIX = "b172ed31659d6cd6"
HOGAN_PRINT_PREFIX = "436fb4ff1b278ec8"

BISHAI = (
    "Bob has done some highly technical original research that shows an "
    "association between 5 days of very hot nights and cardiovascular disease. "
    "He has performed at a level not typically seen for first year "
    "undergraduates, but I am not surprised. He has asked for help when "
    "needed and formed an effective partnership with other researchers."
)


def _text(*paths: Path) -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in paths)


def _pack() -> str:
    return _text(
        PACK / "README.md",
        PACK / "to_laidlaw.md",
        PACK / "WHAT_TO_ATTACH.md",
        PACK / "HASH_VERIFY.md",
        PACK / "comments_verbatim.md",
        PACK / "spreadsheet_QR_paste.md",
        KNOW,
    )


def test_email_is_horizons_not_hogan():
    raw = (PACK / "to_laidlaw.md").read_text(encoding="utf-8")
    letter = raw.split("---", 2)[1]
    assert "laidlaw@hku.hk" in raw
    assert "audrey.chung@hku.hk" in raw.lower() or "Audrey Chung" in raw
    assert "Bob sends" in raw or "Agents do not send" in raw
    assert "Do not attach" in raw
    assert "Heat_CVD_Manuscript_20260824_hogan.pdf" in raw
    assert "ShenRuililin_Laidlaw_Stage3Report.pdf" in raw
    assert "ShenRuililin_Laidlaw_Stage3Poster.pdf" in raw
    assert ESSAY_PREFIX in raw
    assert POSTER_PREFIX in raw
    low_letter = letter.lower()
    assert "gate 3" not in low_letter
    assert "f1000" not in low_letter
    assert "q-value" not in low_letter
    notes = raw.lower()
    assert "f1000" in notes  # named only as something to omit unless written consent
    assert "unless you have written consent" in notes or "does not record that consent" in notes


def test_hogan_pdf_is_excluded_from_attach_list():
    attach = (PACK / "WHAT_TO_ATTACH.md").read_text(encoding="utf-8")
    assert "Do not attach" in attach
    assert "Heat_CVD_Manuscript_20260824_hogan.pdf" in attach
    assert HOGAN_UPLOAD_PREFIX in attach
    assert HOGAN_PRINT_PREFIX in attach
    assert FORM_PREFIX in attach
    assert ESSAY_PREFIX in attach
    assert POSTER_PREFIX in attach
    # Repo current hashes must not be listed as the Horizons attach hashes.
    table = attach.split("## Do not attach", 1)[0]
    assert REPO_ESSAY_PREFIX not in table
    assert REPO_POSTER_PREFIX not in table


def test_bishai_comments_kept_verbatim_and_satisfactory():
    pack = _pack()
    assert BISHAI in pack
    assert "satisfactory" in pack.lower()
    assert "Do not tidy" in pack or "do not tidy" in pack.lower()
    comments = (PACK / "comments_verbatim.md").read_text(encoding="utf-8")
    assert BISHAI in comments
    # Do not "correct" CVD → CHD/HF in the quoted comment.
    assert comments.index(BISHAI) > 0


def test_22_aug_is_horizons_object_24_aug_is_not():
    pack = _pack()
    assert ESSAY_PREFIX in pack and POSTER_PREFIX in pack
    assert "22 August" in pack or "22 Aug" in pack
    assert REPO_ESSAY_PREFIX in pack
    assert "Not** the Horizons object" in pack or "not the Horizons object" in pack.lower()
    readme = (PACK / "README.md").read_text(encoding="utf-8")
    assert "Do not replace them with the 24 August" in readme or "not the 24 August" in pack.lower()


def test_knowledge_note_keeps_claim_boundary():
    text = KNOW.read_text(encoding="utf-8")
    assert "Not a Gate 3 freeze" in text or "Not** a Gate 3 freeze" in text
    assert "CHD/HF" in text
    assert "F1000Research" in text
    assert "not implied" in text.lower() or "not implied by this form" in text.lower()
    assert "do not send" in (PACK / "README.md").read_text(encoding="utf-8").lower()
    assert "cardiovascular disease" in text  # Bishai wording preserved
    assert REPO_ESSAY_PREFIX in text
    assert "rebuild on `main` (`605cd8db" not in text
    assert "2026-08-31_bishai_form2a_signed.md" in text
    verify = (PACK / "HASH_VERIFY.md").read_text(encoding="utf-8")
    assert "2026-08-31_bishai_form2a_signed.md" in verify
    attach = (PACK / "WHAT_TO_ATTACH.md").read_text(encoding="utf-8")
    assert "outputs/ShenRuililin_Laidlaw_Stage3Report.pdf`, prefix `605cd8db43072cb5`" not in attach


def test_endorsed_form_pdf_not_tracked():
    tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
    for line in tracked.splitlines():
        name = line.lower().replace(" ", "_")
        if not name.endswith(".pdf"):
            continue
        assert "report_form" not in name
        assert "2a._laidlaw" not in name
        assert "form__hku" not in name
        assert "form_hku_db" not in name


def test_gitignore_allows_this_send_pack():
    gi = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "!analysis_plan/send_pack_2026-08-31/" in gi
    # The pack itself must be tracked once committed; this test still holds pre-commit.
    assert (PACK / "to_laidlaw.md").is_file()


def test_qr_paste_uses_submitted_hashes():
    qr = (PACK / "spreadsheet_QR_paste.md").read_text(encoding="utf-8")
    assert "laidlaw@hku.hk" in qr
    assert ESSAY_PREFIX in qr
    assert POSTER_PREFIX in qr
    assert "6136e85a654502a0" not in qr  # 20 Aug ready-to-send hash
    assert "Sent to Prof. Bishai for form 2a endorsement" not in qr


def test_uploaded_bytes_match_22_aug_lock_when_present():
    essay = UPLOADS / "ShenRuililin_Laidlaw_Stage3Report_a9a3.pdf"
    poster = UPLOADS / "ShenRuililin_Laidlaw_Stage3Poster_ca96.pdf"
    form = UPLOADS / "2a._Laidlaw_-_Report_Form__HKU_DB_82e1.pdf"
    hogan = UPLOADS / "Heat_CVD_Manuscript_20260824_hogan_5e36.pdf"
    if not essay.is_file():
        return
    assert hashlib.sha256(essay.read_bytes()).hexdigest().startswith(ESSAY_PREFIX)
    assert hashlib.sha256(poster.read_bytes()).hexdigest().startswith(POSTER_PREFIX)
    assert hashlib.sha256(form.read_bytes()).hexdigest().startswith(FORM_PREFIX)
    assert hashlib.sha256(hogan.read_bytes()).hexdigest().startswith(HOGAN_UPLOAD_PREFIX)
    repo_essay = ROOT / "outputs" / "ShenRuililin_Laidlaw_Stage3Report.pdf"
    repo_poster = ROOT / "outputs" / "ShenRuililin_Laidlaw_Stage3Poster.pdf"
    assert hashlib.sha256(repo_essay.read_bytes()).hexdigest().startswith(REPO_ESSAY_PREFIX)
    assert hashlib.sha256(repo_poster.read_bytes()).hexdigest().startswith(REPO_POSTER_PREFIX)
    assert essay.read_bytes() != repo_essay.read_bytes()


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("OK", name)
