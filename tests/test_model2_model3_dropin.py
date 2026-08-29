"""Model 2/3 drop-in contract.

Fits are blocked without governed panels. Reconstruction from figures is forbidden.
CONTROL_TERM_MAP must accept relative_humidity and rainfall so script 53 can run
after panels land.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPERS = (ROOT / "scripts" / "final_model_helpers.R").read_text(encoding="utf-8")
SCRIPT53 = (ROOT / "scripts" / "53_hogan_models_rh_rain.R").read_text(encoding="utf-8")
SCRIPT68 = (ROOT / "scripts" / "68_hogan_model3_climatology.R").read_text(encoding="utf-8")
REGISTRY = (ROOT / "analysis_plan" / "final_model_registry.yml").read_text(encoding="utf-8")
LIVE = (ROOT / "manuscript" / "live_collaborative" / "Heat_CVD_Manuscript_live_update.md").read_text(
    encoding="utf-8"
)


def test_control_map_accepts_hogan_model2_covariates():
    assert "relative_humidity = \"relative_humidity\"" in HELPERS
    assert "rainfall = \"rainfall\"" in HELPERS
    assert "relative_humidity" in SCRIPT53
    assert "rainfall" in SCRIPT53
    assert "Hogan_RH_rain" in REGISTRY


def test_model3_script_uses_climatology_file_and_refuses_missing_panels():
    assert "hogan_climatology_day_counts_2013_2023.csv" in SCRIPT68
    assert "days_warmer_than_climatology" in SCRIPT68
    assert "days_cooler_than_climatology" in SCRIPT68
    assert "missing_governed_panel_blocker" in SCRIPT68
    assert "table2_core_models.csv" not in SCRIPT68
    assert "M3W" in REGISTRY and "M3C" in REGISTRY


def test_panels_absent_and_live_file_does_not_invent_coefficients():
    assert not (ROOT / "data_processed" / "chd_analysis_panel.csv").exists()
    assert not (ROOT / "data_processed" / "hf_analysis_panel.csv").exists()
    methods = LIVE.split("## Methods", 1)[1].split("## Results", 1)[0]
    assert "No Model 3 health coefficients are reported" in methods
    results = LIVE.split("## Results", 1)[1].split("## Discussion", 1)[0]
    assert "days_warmer_than_climatology" not in results
    assert "Model 2 count ratio" not in results


def test_figure1_reconstruction_is_not_an_analysis_path():
    stub = (ROOT / "scripts" / "62_fit_hogan_model2_model3.py").read_text(encoding="utf-8")
    assert "Do not digitize Figure 1" in stub
    assert "68_hogan_model3_climatology.R" in stub
