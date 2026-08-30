#!/usr/bin/env python3
"""Inherit-only objective-audit tripwires. WORSE is allowed. Does not freeze Gate 3.

Named Fable/Opus/Sol Max seats are optional. Run this whenever a live-file or
Stage 3 Discussion insert is proposed.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
KILL = yaml.safe_load(
    (ROOT / "analysis_plan" / "objective_audit" / "kill_list.yml").read_text(encoding="utf-8")
)
LIVE = (
    ROOT / "manuscript" / "live_collaborative" / "Heat_CVD_Manuscript_live_update.md"
).read_text(encoding="utf-8")
ESSAY = (ROOT / "reports" / "laidlaw_stage3" / "laidlaw_research_report_2026.md").read_text(
    encoding="utf-8"
)
GATES = (ROOT / "analysis_plan" / "decision_gates.md").read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    discussion = LIVE.split("## Discussion", 1)[-1] if "## Discussion" in LIVE else LIVE
    for phrase in KILL["live_discussion_forbidden"]:
        if phrase in discussion:
            errors.append(f"live Discussion contains forbidden phrase: {phrase!r}")
    for phrase in KILL["essay_forbidden"]:
        if phrase in ESSAY:
            errors.append(f"Stage 3 essay contains forbidden phrase: {phrase!r}")
    for phrase in ("we evaluated VHWW", "We evaluated VHWW"):
        if phrase in LIVE or phrase in ESSAY:
            errors.append(f"forbidden claim: {phrase!r}")
    if "admissions averted" in LIVE and "do not count admissions averted" not in LIVE:
        errors.append("live file mentions admissions averted without the required refusal")
    if "admissions averted" in ESSAY and "I do not count admissions averted" not in ESSAY:
        errors.append("essay mentions admissions averted without the required refusal")
    if "Gate 3 is closed" in LIVE or "Gate 3 is closed" in ESSAY:
        errors.append("live or essay claims Gate 3 is closed")
    if "Still OPEN" not in GATES:
        errors.append("decision_gates.md no longer states Gate 3 Still OPEN")
    for rel in KILL["require_absent_panels"]:
        if (ROOT / rel).exists():
            errors.append(f"governed panel unexpectedly present: {rel}")
    if errors:
        print("OBJECTIVE AUDIT TRIPWIRES: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("OBJECTIVE AUDIT TRIPWIRES: PASS")
    print("Gate 3 remains a human freeze. WORSE remains an allowed editorial verdict.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
