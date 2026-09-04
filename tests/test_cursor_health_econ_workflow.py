"""Cursor health-econ workflow, DUA ignore, playbooks 07–08, PR board."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RULES = (ROOT / ".cursorrules").read_text(encoding="utf-8")
IDENT = (ROOT / ".cursor" / "rules" / "00-laidlaw-identification.mdc").read_text(encoding="utf-8")
DUA = (ROOT / ".cursor" / "rules" / "01-dua-zero-ingestion.mdc").read_text(encoding="utf-8")
IGNORE = (ROOT / ".cursorignore").read_text(encoding="utf-8")
PB07 = (ROOT / "analysis_plan" / "playbooks" / "07_pr_board.md").read_text(encoding="utf-8")
PB08 = (ROOT / "analysis_plan" / "playbooks" / "08_health_econ_identification_lab.md").read_text(
    encoding="utf-8"
)
GATES = (ROOT / "analysis_plan" / "decision_gates.md").read_text(encoding="utf-8")
AGENTS = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
SCHEMA = ROOT / "data_processed" / "samples" / "SYNTHETIC_chd_hf_schema.csv"
POLICY = yaml.safe_load(
    (ROOT / "analysis_plan" / "pr_board_policy.yml").read_text(encoding="utf-8")
)
LIVE = (
    ROOT / "manuscript" / "live_collaborative" / "Heat_CVD_Manuscript_live_update.md"
).read_text(encoding="utf-8")
MAP = (ROOT / "analysis_plan" / "health_econ" / "generic_advice_map.yml").read_text(encoding="utf-8")


def test_cursorignore_covers_governed_panels_and_keeps_samples():
    assert "data_processed/*_analysis_panel.csv" in IGNORE
    assert "data_raw/ha_secure_placeholder" in IGNORE
    assert "*.dta" in IGNORE
    assert "!data_processed/samples/" in IGNORE
    assert SCHEMA.is_file()


def test_rules_forbid_twfe_default_and_keep_this_estimand():
    blob = RULES + IDENT
    assert "Do **not** default to TWFE" in blob or "Do not default to TWFE" in blob or "do **not** default to TWFE" in blob.lower() or "Do **not** default to TWFE" in RULES
    assert "Callaway" in blob
    assert "Newey–West" in IDENT or "Newey-West" in IDENT or "Newey–West" in RULES
    assert "132 months" in IDENT
    assert "QALY" in RULES or "QALY" in IDENT
    assert "medicaid" not in IDENT.lower() or "Medicaid" in RULES  # mentioned only as forbidden
    assert "Do **not** write Medicaid" in RULES


def test_dua_rule_forbids_figure1_reconstruction():
    assert "Do not reconstruct" in DUA or "reconstruct" in DUA
    assert "chd_analysis_panel.csv" in DUA


def test_playbook_07_does_not_merge_or_freeze():
    assert "Do **not** run this playbook as a licence to merge" in PB07
    assert "CLOSE_SUPERSEDED" in PB07
    assert "Gate 3" in PB07
    assert (ROOT / ".cursor" / "skills" / "playbook-07-pr-board" / "SKILL.md").is_file()
    assert (ROOT / "scripts" / "69_pr_board.py").is_file()
    assert POLICY["living_science_pr"] == 82
    assert POLICY["living_science_ref"] == "origin/main"
    assert POLICY.get("living_science_merged") is True
    assert POLICY["do_not_merge"] is True
    assert POLICY["do_not_freeze_gate3"] is True
    close_nums = {row["number"] for row in POLICY["classified"] if row["action"] == "CLOSE_SUPERSEDED"}
    for n in (94, 93, 92, 91, 90, 89, 88, 87, 86, 85, 84, 83, 81, 80, 79, 78, 77, 75, 74, 73, 69, 68, 67, 66, 62, 61, 58, 53, 46):
        assert n in close_nums
    keep = {row["number"] for row in POLICY["classified"] if row["action"].startswith("KEEP")}
    assert 82 in keep
    assert keep == {82}


def test_playbook_08_never_writes_live_manuscript():
    assert "Never" in PB08 or "were not edited" in PB08
    assert "Heat_CVD_Manuscript_live_update.md" in PB08
    assert "TWFE" in PB08
    assert "PR 54" in PB08
    assert "SYNTHETIC" in PB08
    assert (ROOT / ".cursor" / "skills" / "playbook-08-health-econ-lab" / "SKILL.md").is_file()
    assert "Forbidden default" in MAP
    prompt = (ROOT / "analysis_plan" / "health_econ" / "identification_lab_prompt.txt").read_text(
        encoding="utf-8"
    )
    assert "Do not default to TWFE" in prompt


def test_synthetic_schema_is_short_and_labelled():
    rows = SCHEMA.read_text(encoding="utf-8").strip().splitlines()
    assert 2 <= len(rows) <= 11  # header + <=10
    header = rows[0]
    for col in (
        "month_id",
        "n_events",
        "data_status",
        "hot_nights",
        "cold_days",
        "very_hot_days",
        "relative_humidity",
        "rainfall",
    ):
        assert col in header
    for line in rows[1:]:
        assert "SYNTHETIC" in line


def test_gate3_still_open_and_cut_prose_absent():
    assert "Still OPEN" in GATES
    assert "can inform four" not in LIVE
    assert "sits with official" not in LIVE
    discussion = LIVE.split("## Discussion", 1)[1]
    assert "continued attention" not in discussion


def test_agents_md_lists_playbooks_07_and_08():
    assert "07_pr_board.md" in AGENTS
    assert "08_health_econ_identification_lab.md" in AGENTS
    assert "/playbook-07-pr-board" in AGENTS
    assert "/playbook-08-health-econ-lab" in AGENTS
    assert "/objective-audit" in AGENTS


def test_assumption_a67_locks_generic_health_econ_defaults():
    ledger = (ROOT / "analysis_plan" / "assumption_ledger.md").read_text(encoding="utf-8")
    assert "A67" in ledger
    assert "Callaway" in ledger
    assert "Playbook 08" in ledger


def test_tripwire_script_passes_on_current_live_file():
    import subprocess

    proc = subprocess.run(
        ["python3", str(ROOT / "scripts" / "71_objective_audit_tripwires.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "PASS" in proc.stdout


def test_objective_audit_skill_allows_worse():
    skill = (ROOT / ".cursor" / "skills" / "objective-audit" / "SKILL.md").read_text(encoding="utf-8")
    assert "WORSE is a valid" in skill or "WORSE is allowed" in skill
    assert "71_objective_audit_tripwires.py" in skill
    assert (ROOT / "scripts" / "71_objective_audit_tripwires.py").is_file()
    assert (ROOT / "analysis_plan" / "objective_audit" / "kill_list.yml").is_file()
