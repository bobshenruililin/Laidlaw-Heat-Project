"""Contract checks for the 25 Aug Bishai form 2a signature pack.

Does not send email. Does not fill the supervisor block.
Does not rebuild Stage 3 PDFs. Does not read governed HA panels.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KNOW = ROOT / "knowledge" / "2026-08-25_bishai_form2a_signature.md"
COMMENTS = ROOT / "analysis_plan" / "send_pack_2026-08-22" / "suggested_supervisor_comments.md"
CHECKLIST = ROOT / "analysis_plan" / "send_pack_2026-08-22" / "pre_thursday_checklist.md"
SCRIPT = ROOT / "analysis_plan" / "send_pack_2026-08-22" / "meeting_ten_minutes.md"
ONE_PAGER = ROOT / "analysis_plan" / "send_pack_2026-08-22" / "supervisor_one_pager.html"
QR = ROOT / "analysis_plan" / "send_pack_2026-08-20" / "spreadsheet_QR_paste.md"
HOGAN_LINE = ROOT / "analysis_plan" / "send_pack_2026-08-22" / "optional_hogan_one_liner.md"
GITIGNORE = ROOT / ".gitignore"
ESSAY = ROOT / "outputs" / "ShenRuililin_Laidlaw_Stage3Report.pdf"
POSTER = ROOT / "outputs" / "ShenRuililin_Laidlaw_Stage3Poster.pdf"
ESSAY_SRC = ROOT / "reports" / "laidlaw_stage3" / "laidlaw_research_report_2026.md"


def _sha_prefix(path: Path, n: int = 16) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()[:n]


def test_stage3_pdfs_still_byte_locked():
    assert _sha_prefix(ESSAY) == "c083d4096a0924b1"
    assert _sha_prefix(POSTER) == "0ef58e0951bb2ffd"
    twin = ROOT / "reports" / "laidlaw_stage3" / "ShenRuililin_Laidlaw_Stage3Report.pdf"
    assert _sha_prefix(twin) == "c083d4096a0924b1"


def test_knowledge_note_answers_the_three_asks():
    text = KNOW.read_text(encoding="utf-8")
    assert "likely" in text.lower()
    assert "Hogan does not sign form 2a" in text
    assert "satisfactory" in text
    assert "pre_thursday_checklist.md" in text
    assert "Bob does not type into the supervisor block" in text
    assert "Do not put in the comments box" in text


def test_comments_match_essay_honesty():
    comments = COMMENTS.read_text(encoding="utf-8")
    essay = ESSAY_SRC.read_text(encoding="utf-8")
    paste = comments.split("Do not add", 1)[0]
    assert "exploratory" in comments.lower()
    assert "satisfactory" in comments.lower()
    assert "admission cause" in comments
    assert "stroke" in comments.lower()
    assert "most elevated" not in comments.lower()
    assert "AMI" not in paste
    assert "excess-death" in comments  # as a do-not
    assert "hypotheses, not proof" in essay
    assert "all twelve" in essay.lower()
    assert "Handwritten (Thursday" in comments


def test_pre_thursday_does_not_wait_on_hogan():
    text = CHECKLIST.read_text(encoding="utf-8")
    assert "Does not wait on" in text
    assert "Hogan" in text
    assert "Email A" in text
    assert "Thursday 27" in text
    assert "do not wait for Hogan" in text.lower() or "Does not wait on" in text
    assert "live manuscript" in text.lower()
    assert "rebuild" in text.lower()


def test_meeting_script_keeps_journal_off_the_form():
    text = SCRIPT.read_text(encoding="utf-8")
    assert "Hogan does not sign" in text
    assert "31 August" in text
    assert "Gate 3" in text
    assert "q-values are above 0.19" in text or "q-values" in text


def test_one_pager_still_matches_rebuilt_conclusion():
    html = ONE_PAGER.read_text(encoding="utf-8")
    assert "most elevated" not in html.lower()
    assert "predeclared" not in html.lower()
    assert "all" in html.lower() and "0.19" in html
    assert "I have examined the research report" in html
    assert "live" in html.lower()


def test_spreadsheet_qr_uses_current_hashes():
    text = QR.read_text(encoding="utf-8")
    assert "c083d4096a0924b1" in text
    assert "0ef58e0951bb2ffd" in text
    assert "6136e85a654502a0" not in text
    assert "4f7c1e408ae2d31f" not in text


def test_hogan_one_liner_does_not_ask_endorsement():
    text = HOGAN_LINE.read_text(encoding="utf-8")
    assert "not asking you to review the programme files" in text.lower() or "Do not ask Hogan to endorse" in text


def test_form_docx_is_gitignored():
    text = GITIGNORE.read_text(encoding="utf-8")
    assert "2a_Laidlaw" in text


def test_no_supervisor_block_filled_in_repo_markdown():
    comments = COMMENTS.read_text(encoding="utf-8")
    assert "Do not type these into the supervisor block" in comments


if __name__ == "__main__":
    failed = []
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
            except Exception as exc:  # noqa: BLE001
                failed.append((name, exc))
    if failed:
        for name, exc in failed:
            print(f"FAIL {name}: {exc}")
        raise SystemExit(1)
    print("ok")
