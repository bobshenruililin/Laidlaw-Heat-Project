"""Thursday 27 Aug form 2a overlay: Hogan does not gate the signature."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "analysis_plan" / "send_pack_2026-08-25"
MEMO = ROOT / "knowledge" / "2026-08-25_bishai_form2a_thursday.md"
COMMENTS = ROOT / "analysis_plan" / "send_pack_2026-08-24" / "suggested_supervisor_comments.md"
EMAIL_A = ROOT / "analysis_plan" / "send_pack_2026-08-24" / "to_bishai.md"
TODAY = PACK / "to_bishai_today.md"
NUDGE = PACK / "to_bishai_nudge.md"
BRIEFING = PACK / "thursday_meeting_briefing.md"
ASKS = PACK / "if_he_asks.md"
PRINT = PACK / "print_checklist.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_overlay_files_exist():
    for path in (
        PACK / "README.md",
        TODAY,
        NUDGE,
        BRIEFING,
        ASKS,
        PRINT,
        PACK / "after_signature.md",
        PACK / "START_HERE.md",
        PACK / "bob_pocket_card.html",
        PACK / "bob_pocket_card.pdf",
        PACK / "supervisor_one_pager.pdf",
        PACK / "supervisor_one_pager.html",
        PACK / "thursday_table_stack.pdf",
        PACK / "spreadsheet_QR_paste.md",
        MEMO,
        COMMENTS,
        EMAIL_A,
    ):
        assert path.is_file(), path


def test_hogan_does_not_gate_or_sign():
    blob = "\n".join(
        _read(p)
        for p in (MEMO, BRIEFING, PACK / "README.md", PACK / "bob_pocket_card.html")
    )
    low = blob.lower()
    assert "does not gate" in low or "does **not** gate" in low
    assert "does not sign" in low
    assert "do not say that he will sign" in low
    assert "will definitely" not in low
    assert "guaranteed to sign" not in low


def test_supervisor_paste_is_exploratory_model1():
    text = _read(COMMENTS)
    short = text.split("## Slightly longer", 1)[0]
    assert "Model 1" in short
    assert "q-values exceed 0.19" in short or "*q*-values exceed 0.19" in short
    assert "does not claim a confirmatory thermal effect" in short
    assert "stroke data were not delivered" in short
    assert "I rate the student’s performance as satisfactory" in short
    assert "1,455" not in text
    assert "Do not add Roro’s excess-death totals" in text
    assert "AMI/stroke findings" in text


def test_email_tree_forbids_nudge_instead_of_email_a():
    today = _read(TODAY)
    assert "Do not send both Email A and a nudge" in today
    assert "send_pack_2026-08-24/to_bishai.md" in today
    nudge = _read(NUDGE)
    assert "updated 24 August" in nudge
    assert "Do not re-attach the essay unless the first message bounced" in nudge


def test_briefing_keeps_form_first_and_24_aug_pdf():
    briefing = _read(BRIEFING)
    assert "First ten minutes" in briefing
    assert "605cd8db43072cb5" in briefing
    assert "live manuscript" in briefing.lower()
    assert "Friday 28 August" in briefing
    print_txt = _read(PRINT)
    assert "c083d4096a0924b1" in print_txt
    assert "Do not print for this meeting" in print_txt


def test_memo_answers_the_three_questions():
    memo = _read(MEMO)
    assert "Is he likely to sign?" in memo
    assert "What can he write?" in memo
    assert "What to do before Thursday" in memo
    assert "If Email A with the **24 August** PDF has not gone, send it now" in memo
    assert "Wait for another Hogan review" in memo


def test_print_sheets_are_one_a4_page():
    import re
    import subprocess

    for name in ("supervisor_one_pager.pdf", "bob_pocket_card.pdf"):
        info = subprocess.check_output(["pdfinfo", str(PACK / name)], text=True)
        assert re.search(r"Pages:\s+1\b", info), info
        m = re.search(r"Page size:\s+([0-9.]+)\s+x\s+([0-9.]+)", info)
        assert m, info
        w, h = float(m.group(1)), float(m.group(2))
        assert 580 < w < 620, w
        assert 820 < h < 860, h


def test_start_here_answers_the_three_questions():
    text = _read(PACK / "START_HERE.md")
    assert "Will Professor Bishai sign?" in text
    assert "What can he write?" in text
    assert "Before Thursday" in text
    assert "does not sign" in text.lower()
    assert "to_bishai.md" in text
    assert "thursday_table_stack.pdf" in text


def test_table_stack_is_four_a4_pages_from_locked_essay():
    import re
    import subprocess

    path = PACK / "thursday_table_stack.pdf"
    info = subprocess.check_output(["pdfinfo", str(path)], text=True)
    assert re.search(r"Pages:\s+4\b", info), info
    text = subprocess.check_output(["pdftotext", str(path), "-"], text=True)
    assert "Laidlaw Stage 3 endorsement" in text
    assert "1.022 (1.002" in text
    assert "1.073 (1.006" in text
    assert "hypotheses, not proof of thermal effects" in text
    assert "I have examined the research report" in text
    assert "I rate the student’s performance as satisfactory" in text
    assert "live manuscript" in text.lower()


def test_print_bundle_script_refuses_wrong_essay_hash(tmp_path, monkeypatch):
    import hashlib
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "print_bundle", ROOT / "scripts" / "65_bishai_thursday_print_bundle.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    fake = tmp_path / "fake.pdf"
    fake.write_bytes(b"%PDF-1.4\n%\n")
    monkeypatch.setattr(mod, "ESSAY", fake)
    monkeypatch.setattr(mod, "OUT", tmp_path / "out.pdf")
    assert not hashlib.sha256(fake.read_bytes()).hexdigest().startswith(
        mod.ESSAY_SHA_PREFIX
    )
    assert mod.main() == 1
