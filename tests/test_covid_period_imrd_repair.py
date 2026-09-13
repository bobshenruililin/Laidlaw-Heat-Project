"""covid_period IMRD repair rails (hostile-read pass).

Does not open governed HA panels. Does not freeze Gate 3.
Wraps scripts/79_covid_period_rails_checks.py so Vancouver order, Hogan
weather, forbidden phrases, and the five-heading Results scan fail in pytest.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COVID = ROOT / "manuscript" / "covid_period" / "Manuscript_covid_period_draft.md"
RAILS = ROOT / "scripts" / "79_covid_period_rails_checks.py"
OUT = ROOT / "outputs" / "covid_period" / "rails_checks.json"

RESULTS_HEADINGS = (
    "### Outcome series",
    "### Exposure context",
    "### Nested-window official-day panel",
    "### Twelve-fit thermal exhibit",
    "### Uncertainty ladder",
)


def test_covid_period_rails_checks_pass():
    proc = subprocess.run(
        ["python3", str(RAILS), "--out", str(OUT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = json.loads(OUT.read_text(encoding="utf-8"))
    assert report["ok"] is True
    assert report["n_fail"] == 0


def test_results_headings_are_one_imrd_scan():
    text = COVID.read_text(encoding="utf-8")
    body = text.split("## References", 1)[0]
    positions = [body.find(h) for h in RESULTS_HEADINGS]
    assert all(p >= 0 for p in positions), positions
    assert positions == sorted(positions)
    assert "## Strengths and limitations" in body
    assert body.find("## Strengths and limitations") < body.find("## Conclusion")
    assert "### Specification and diagnostic checks" not in body
    assert "The main reported interval is Newey–West" not in body
    assert "Nine of the twelve" not in body
    assert "left to the supplement" not in body
    assert "I(\\mathrm{count}/5)" in text or r"I(\mathrm{count}/5)" in text
    assert "Meteorological data was obtained from the HKO." in text
    assert (
        "All monthly data were derived by taking the average of daily data "
        "in each calendar month."
    ) in text
