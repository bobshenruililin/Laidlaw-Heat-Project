"""COVID-period redirection (Hogan 10 Sep 2026): park thermal; new track; rails.

Does not open governed HA panels. Does not freeze Gate 3.
Does not treat Playbook 08 SYNTHETIC JSON as a Hong Kong finding.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "manuscript" / "live_collaborative" / "Heat_CVD_Manuscript_live_update.md"
COVID = ROOT / "manuscript" / "covid_period" / "Manuscript_covid_period_draft.md"
PARK = ROOT / "manuscript" / "archive" / "thermal_extremes_2026-08"
THERMAL_SNAPSHOT = PARK / "live_collaborative_snapshot"
LEDGER = ROOT / "analysis_plan" / "assumption_ledger.md"
LEDGER_COVID = ROOT / "manuscript" / "covid_period" / "claim_ledger.yml"
GATES = ROOT / "analysis_plan" / "decision_gates.md"
INVENTORY = ROOT / "analysis_plan" / "covid_period" / "ha_metadata_inventory.md"
MEMO = ROOT / "literature" / "covid_period_mechanism_memo.md"
REGISTRY = ROOT / "analysis_plan" / "covid_period" / "hypothesis_registry.yml"
LAB = ROOT / "analysis_plan" / "health_econ" / "lab_note_2026-09-10.md"
JSON72 = ROOT / "outputs" / "health_econ" / "synthetic_utilisation_shock_2026-09-10.json"
JSON73 = ROOT / "outputs" / "health_econ" / "synthetic_mnar_selection_2026-09-10.json"
JSON75 = ROOT / "outputs" / "health_econ" / "synthetic_flu_collapse_2026-09-10.json"
DOCX = ROOT / "manuscript" / "covid_period" / "Heat_CVD_Manuscript_covid_period.docx"
HOGAN_OPEN = "Meteorological data was obtained from the HKO."
HOGAN_AVG = (
    "All monthly data were derived by taking the average of daily data in each calendar month."
)
FORBIDDEN_COVID = (
    "health improved",
    "gate 3 is closed",
    "TWFE",
    "Callaway",
    "QALY",
    "admissions averted",
    "failing left ventricle",
)


def _covid() -> str:
    return COVID.read_text(encoding="utf-8")


def _live() -> str:
    return LIVE.read_text(encoding="utf-8")


def test_park_readme_exists_and_does_not_freeze_gate3():
    readme = (PARK / "README.md").read_text(encoding="utf-8")
    cover = (PARK / "COVER_NOTE_as_flown.md").read_text(encoding="utf-8")
    assert "PARKED" in readme
    assert "covid_period" in readme
    assert "Gate 3" in readme.lower() or "open" in readme.lower()
    assert (PARK / "Heat_CVD_Manuscript_live_update.md").is_file()
    assert (PARK / "claim_ledger.yml").is_file()
    assert "96b69b7b7ba38513" in cover
    assert "not a gate 3 freeze" in cover.lower()


def test_archived_thermal_file_uncut():
    archived = (
        THERMAL_SNAPSHOT / "Heat_CVD_Manuscript_live_update.md"
    ).read_text(encoding="utf-8")
    assert "confinement study of seven men" in archived
    assert HOGAN_OPEN in archived
    assert HOGAN_AVG in archived
    methods = archived.split("## Methods", 1)[1].split("## Results", 1)[0]
    assert methods.count(HOGAN_OPEN) == 1


def test_covid_period_imrd_keeps_hogan_weather_and_refuses_improvement():
    text = _covid()
    assert HOGAN_OPEN in text
    assert HOGAN_AVG in text
    low = text.lower()
    for phrase in FORBIDDEN_COVID:
        assert phrase.lower() not in low, phrase
    assert "placeholder" not in low
    assert "hogan asked" not in low
    assert "gate 3" not in text
    assert "not a measure of physiological improvement" in text
    assert "I(\\mathrm{count}/5)" in text or r"I(\mathrm{count}/5)" in text
    assert text.split("## Abstract", 1)[0].count("Window dependence") >= 1
    assert "Wai AKC" in text
    assert "10.1016/j.annemergmed.2021.09.424" in text
    hung_block = text.split("10.1016/j.annemergmed.2021.09.424")[0][-120:]
    assert "Hung KK" not in hung_block
    assert "Hung et al. 2022" not in text
    assert "10.2196/41792" in text
    assert "Xin H" in text
    assert "insufficient" in low and "not irrelevant" in low
    assert "Figure 3" in text and "main identification" in text.lower()


def test_live_authority_is_analysis_window_sensitivity_not_prepost_effect():
    text = _live()
    low = text.lower()
    assert text.startswith("# Analysis-window sensitivity")
    assert HOGAN_OPEN in text
    assert HOGAN_AVG in text
    assert "nested fits do not estimate a pre/post effect" in low
    assert "no interaction between thermal exposure and period was fitted" in low
    assert "these nested-window intervals overlap" in low
    assert "do not supply a complete explanation" in low
    assert "not evidence that weather was irrelevant" in low
    assert "improved cardiovascular health" in low  # explicit negation only
    assert "Supplementary Table S9" in text
    assert "Supplementary Table S10" in text
    for forbidden in (
        "health improved",
        "cold days became protective",
        "Hogan asked",
        "Gate 3",
        "candidate article",
        "admissions averted",
    ):
        assert forbidden.lower() not in low


def test_ledger_a69_a71_and_gate3_still_open():
    ledger = LEDGER.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    assert "| A69 |" in ledger and "covid_period" in ledger
    assert "| A70 |" in ledger and "Never promised, never delivered" in ledger
    assert "| A71 |" in ledger and "not physiology" in ledger
    assert "Still OPEN" in gates
    assert "10 Sep 2026" in gates
    assert "manuscript/covid_period/" in gates


def test_labs_never_delivered_and_xin_is_neighbour():
    inv = INVENTORY.read_text(encoding="utf-8")
    memo = MEMO.read_text(encoding="utf-8")
    assert "Never promised" in inv or "NEVER PROMISED" in inv
    assert "HbA1c" in inv
    assert "do not add labs" in inv.lower()
    assert "10.1016/j.lanwpc.2022.100645" in memo
    assert "Do not import Xin" in memo or "Do not import Xin’s" in memo
    assert "hospitalisations down" in memo.lower() or "fewer" in memo.lower()
    assert "Wai AKC" in memo
    assert "10.1016/j.annemergmed.2021.09.424" in memo
    hung_block = memo.split("10.1016/j.annemergmed.2021.09.424")[0][-80:]
    assert "Hung KK" not in hung_block
    assert "Wong ELY, et al. The effect of the COVID-19 pandemic on non" not in memo
    assert "10.34172/ijhpm.2020.183" in memo


def test_hypothesis_registry_kills_twfe_physiology_react():
    reg = REGISTRY.read_text(encoding="utf-8")
    assert "physiological_improvement_from_count_drop" in reg
    assert "TWFE_Callaway_Medicaid" in reg
    assert "react_dashboard_as_paper" in reg
    assert "health_econ_night_engine_in_live_file" in reg


def test_playbook_08_synthetic_json_labelled_and_not_in_covid_draft_as_finding():
    assert JSON72.is_file(), "run python3 scripts/72_synthetic_utilisation_shock.py"
    assert JSON73.is_file(), "run python3 scripts/73_synthetic_mnar_selection.py"
    assert JSON75.is_file(), "run python3 scripts/75_synthetic_flu_collapse.py"
    p72 = json.loads(JSON72.read_text(encoding="utf-8"))
    p73 = json.loads(JSON73.read_text(encoding="utf-8"))
    p75 = json.loads(JSON75.read_text(encoding="utf-8"))
    assert "xy_mnar" in p73.get("scenarios", {})
    assert p75["data_status"] == "SYNTHETIC"
    assert "flu_collapse_only" in p75.get("scenarios", {})
    covid = _covid()
    assert "mean_pre_window_cr" not in covid
    assert str(p72["mean_full_window_cr"]) not in covid
    flu_full = str(p75["scenarios"]["flu_collapse_only"]["mean_full_window_cr"])
    assert flu_full not in covid
    lab = LAB.read_text(encoding="utf-8")
    assert "SYNTHETIC" in lab
    assert "Not copied into" in lab or "not a finding" in lab.lower() or "Not HA" in lab
    assert "flu" in lab.lower()


def test_covid_period_docx_exists_and_keeps_hogan_weather():
    assert DOCX.is_file(), "run python3 scripts/74_covid_period_manuscript_docx.py"
    from docx import Document

    doc = Document(str(DOCX))
    joined = "\n".join(p.text for p in doc.paragraphs)
    assert HOGAN_OPEN in joined
    assert HOGAN_AVG in joined
    assert "Gate 3" not in joined
    assert "placeholder" not in joined.lower()
    assert "Wai AKC" in joined
    assert "Window dependence" in joined


def test_covid_claim_ledger_covers_headline_numerals():
    ledger = LEDGER_COVID.read_text(encoding="utf-8")
    text = _covid()
    for needle in (
        "1.022 (1.002–1.042)",
        "1.073 (1.006–1.144)",
        "1.113 (1.053–1.176)",
        "1.011 (0.991–1.032)",
        "0.980 (0.970–0.990)",
        "0.945 (0.927–0.963)",
        "0.192",
        "1.036 (1.007–1.067)",
    ):
        assert needle in ledger, needle
        assert needle in text, needle


def test_mechanism_review_leftover_is_not_the_covid_sendable():
    sendable = (ROOT / "send_pack_2026-09-10" / "reply_to_hogan.md").read_text(encoding="utf-8")
    debrief = (ROOT / "reports" / "meeting_debrief_2026-09-10.md").read_text(encoding="utf-8")
    assert "Do not send" in debrief or "Do not send the archive" in debrief
    assert "mechanism_review" not in sendable
    leftover = ROOT / "reports" / "hogan_2026-09-04" / "mechanism_review"
    # Untracked leftover from another branch must not be required.
    assert not (ROOT / "manuscript" / "covid_period" / "REVIEW.pdf").exists()
    assert leftover.name != "covid_period"


def test_search_tree_f08_and_killed_children():
    tree = (ROOT / "analysis_plan" / "scientific_search" / "search_tree.yml").read_text(
        encoding="utf-8"
    )
    killed = (ROOT / "analysis_plan" / "scientific_search" / "killed_registry.yml").read_text(
        encoding="utf-8"
    )
    assert "id: F08\n" in tree or "- id: F08" in tree
    assert "F08-physiology-from-counts" in killed
    assert "F08-post-only-primary" in killed
    assert "F08-react-dashboard-as-paper" in killed
    assert "P-covid-period" in tree
    mem = (ROOT / "analysis_plan" / "scientific_search" / "memory.yml").read_text(encoding="utf-8")
    assert "id: L14" in mem
    assert "id: D10" in mem


def test_thermal_archive_hashes_are_byte_preserved():
    """The pre-pivot thermal object stays byte-preserved after the live rewrite."""
    import hashlib

    expected = {
        "Heat_CVD_Manuscript_live_update.md": "21c024bda975f9f5",
        "Heat_CVD_Manuscript_20260824_hogan.docx": "852702ded2c4e968",
        "Heat_CVD_Manuscript_20260824_hogan.pdf": "96b69b7b7ba38513",
        "claim_ledger.yml": "28a8cf48fd5b3268",
    }
    for name, want in expected.items():
        got = hashlib.sha256((THERMAL_SNAPSHOT / name).read_bytes()).hexdigest()[:16]
        assert got == want, (name, got, want)
    builder = PARK / "builder_snapshot" / "64_hogan_20260824_manuscript_docx.py"
    assert hashlib.sha256(builder.read_bytes()).hexdigest()[:16] == "57e772ec74662999"


def test_scientific_search_tree_memory_rails_green():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "ssc60", ROOT / "scripts" / "60_scientific_search_cycle.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    tree = mod.load_yaml(mod.DEFAULT_TREE)
    memory = mod.load_yaml(mod.DEFAULT_MEMORY)
    live = _live()
    fails = (
        mod.validate_tree(tree)
        + mod.validate_memory(memory)
        + mod.rails_checks(tree, live)
        + mod.harness_debt(tree, memory)
    )
    assert fails == [], fails


def test_live_claim_ledger_auditor_is_green():
    proc = subprocess.run(
        ["python3", str(ROOT / "scripts" / "50_audit_live_claim_ledger.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    audit = json.loads(
        (ROOT / "outputs" / "auto_research" / "claim_ledger_audit.json").read_text(
            encoding="utf-8"
        )
    )
    assert audit["n_fail"] == 0
