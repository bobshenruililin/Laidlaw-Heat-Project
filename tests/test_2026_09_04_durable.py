"""Durable pointers for the 4 September 2026 conference + Hogan pack.

Does not fit health models. Does not freeze Gate 3.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_compound_log_header_restored():
    text = (ROOT / "analysis_plan" / "context_compound_log.md").read_text(encoding="utf-8")
    assert text.startswith("# Context compound log")
    assert "\n| 2026-09-04 |" in text
    assert "\n| 2026-08-31 |" in text
    # The 4 Sep and 31 Aug rows must not be concatenated.
    assert "` || 2026-08-31 |" not in text


def test_ledger_and_project_state():
    state = (ROOT / "analysis_plan" / "PROJECT_STATE.md").read_text(encoding="utf-8")
    ledger = (ROOT / "analysis_plan" / "assumption_ledger.md").read_text(encoding="utf-8")
    gates = (ROOT / "analysis_plan" / "decision_gates.md").read_text(encoding="utf-8")
    assert "0y." in state
    assert "laidlaw_conference_2026" in state
    assert "hogan_2026-09-04/BRIEFING.md" in state
    assert "| A69 |" in ledger
    assert "| A70 |" in ledger
    assert "4 Sep 2026" in gates
    g = gates.lower()
    assert "do **not** close gate 3" in g or "do not close gate 3" in g


def test_knowledge_entries_indexed():
    index = (ROOT / "knowledge" / "INDEX.md").read_text(encoding="utf-8")
    boot = (ROOT / "knowledge" / "CONTEXT_BOOTSTRAP.md").read_text(encoding="utf-8")
    conf = ROOT / "knowledge" / "2026-09-04_laidlaw_conference_abstract.md"
    hog = ROOT / "knowledge" / "2026-09-04_hogan_physiology_briefing.md"
    assert conf.is_file()
    assert hog.is_file()
    assert "2026-09-04_laidlaw_conference_abstract.md" in index
    assert "2026-09-04_hogan_physiology_briefing.md" in index
    assert "laidlaw_conference_2026" in boot
    assert "BRIEFING.md" in boot


if __name__ == "__main__":
    for fn in (
        test_compound_log_header_restored,
        test_ledger_and_project_state,
        test_knowledge_entries_indexed,
    ):
        fn()
        print("ok", fn.__name__)
    print("all passed")
