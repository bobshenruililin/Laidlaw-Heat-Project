"""Contract checks for the 24 Aug Hogan Methods rewrite.

Does not fit health models. Does not read governed HA panels.
"""
from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MS = ROOT / "manuscript" / "live_collaborative" / "Heat_CVD_Manuscript_live_update.md"
CLIM = ROOT / "data_processed" / "hogan_climatology_day_counts_2013_2023.csv"
STAGE3_REPORT = ROOT / "outputs" / "ShenRuililin_Laidlaw_Stage3Report.pdf"
STAGE3_POSTER = ROOT / "outputs" / "ShenRuililin_Laidlaw_Stage3Poster.pdf"


def _methods() -> str:
    text = MS.read_text(encoding="utf-8")
    return text.split("## Methods", 1)[1].split("## Results", 1)[0]


def test_hogan_weather_sentence_copied():
    methods = _methods()
    assert methods.count("Meteorological data was obtained from the HKO.") == 1
    assert "relative humidity, total rainfall" in methods
    assert "All monthly data were derived by taking the average of daily data in each calendar month." in methods


def test_numbered_models_and_equation_symbols():
    methods = _methods()
    assert "Model 1" in methods and "Model 2" in methods and "Model 3" in methods
    assert "core panel" not in methods.lower()
    assert "twelve core" not in methods.lower()
    assert "dependent variable" in methods
    assert "number of days in the month" in methods or "number of days in month" in methods
    assert r"\gamma_m" in methods or "gamma_m" in methods or r"\gamma_m" in methods
    assert "monthly total rainfall" in methods
    assert "relative humidity" in methods
    assert "[21]" in methods
    assert "historical" in methods.lower()
    assert ("same-date" in methods) or ("same calendar day" in methods)


def test_no_results_or_wip_in_methods():
    methods = _methods()
    assert "UW XX-XXX" not in methods
    assert "authors will determine" not in methods.lower()
    assert "protocol may need" not in methods.lower()
    assert "type i" not in methods.lower()
    assert "141 of 145" not in methods
    assert "Roadside monitors were not used." in methods or "Roadside monitors were not used" in methods


def test_acknowledgements_and_code_url():
    text = MS.read_text(encoding="utf-8")
    assert re.search(r"## Acknowledgements\n\nNone\.", text)
    assert "https://github.com/bobshenruililin/Laidlaw-Heat-Project" in text
    assert "Scientific roles are recorded in the Acknowledgements" not in text


def test_climatology_series_is_weather_only():
    rows = list(csv.DictReader(CLIM.open(encoding="utf-8")))
    assert len(rows) == 132
    assert rows[0]["month_id"] == "2013-01"
    assert rows[-1]["month_id"] == "2023-12"
    assert "chd" not in CLIM.read_text(encoding="utf-8").lower()
    assert "hf" not in {k.lower() for k in rows[0].keys()}
    warm = sum(int(r["days_warmer_than_climatology"]) for r in rows) / 132
    cool = sum(int(r["days_cooler_than_climatology"]) for r in rows) / 132
    assert 14 < warm < 19
    assert 11 < cool < 16


def test_stage3_pdfs_not_rebuilt():
    report = hashlib.sha256(STAGE3_REPORT.read_bytes()).hexdigest()
    poster = hashlib.sha256(STAGE3_POSTER.read_bytes()).hexdigest()
    # Byte-lock of the Stage 3 PDFs now on disk. Do not rebuild them.
    assert report.startswith("c083d4096a0924b1")
    assert poster.startswith("0ef58e0951bb2ffd")


if __name__ == "__main__":
    tests = [
        test_hogan_weather_sentence_copied,
        test_numbered_models_and_equation_symbols,
        test_no_results_or_wip_in_methods,
        test_acknowledgements_and_code_url,
        test_climatology_series_is_weather_only,
        test_stage3_pdfs_not_rebuilt,
    ]
    for fn in tests:
        fn()
        print("ok", fn.__name__)
    print("all passed")

