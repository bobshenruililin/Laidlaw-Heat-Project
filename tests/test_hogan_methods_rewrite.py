"""Contract checks for the 24 Aug Hogan Methods rewrite (merged Model 1/2/3).

Does not fit health models. Does not read governed HA panels.
Stage 3 programme PDFs are rebuilt on a separate branch; this file does not freeze their hashes.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MS = ROOT / "manuscript" / "live_collaborative" / "Heat_CVD_Manuscript_live_update.md"
CLIM = ROOT / "data_processed" / "hogan_abnormal_day_counts_2013_2023.csv"
DOCX = ROOT / "manuscript" / "live_collaborative" / "Heat_CVD_Manuscript_20260824_hogan.docx"
PDF = ROOT / "manuscript" / "live_collaborative" / "Heat_CVD_Manuscript_20260824_hogan.pdf"

HOGAN_OPEN = "Meteorological data was obtained from the HKO."
HOGAN_AVG = (
    "All monthly data were derived by taking the average of daily data in each calendar month."
)


def _full() -> str:
    return MS.read_text(encoding="utf-8")


def _methods() -> str:
    text = _full()
    return text.split("## Methods", 1)[1].split("## Results", 1)[0]


def _abstract() -> str:
    text = _full()
    return text.split("## Abstract", 1)[1].split("## Introduction", 1)[0]


def _abstract_methods() -> str:
    abs_text = _abstract()
    m = re.search(r"\*\*Methods\.\*\*(.+?)\*\*Results\.\*\*", abs_text, re.S)
    assert m, "Abstract Methods block missing"
    return m.group(1)


def test_hogan_weather_sentence_copied():
    methods = _methods()
    assert methods.count(HOGAN_OPEN) == 1
    assert "relative humidity, total rainfall" in methods
    assert HOGAN_AVG in methods
    # Do not contradict Hogan's averaging sentence in the body.
    assert "rainfall is a monthly total" not in methods.lower()
    assert "not an average" not in methods.lower()


def test_numbered_models_and_equation_symbols():
    methods = _methods()
    assert "Model 1" in methods and "Model 2" in methods and "Model 3" in methods
    assert "core panel" not in methods.lower()
    assert "twelve core" not in methods.lower()
    assert "dependent variable" in methods
    assert "number of days in the month" in methods
    assert r"\gamma_m" in methods
    assert "monthly total rainfall" in methods
    assert "relative humidity" in methods
    assert "[21]" in methods
    assert "historical" in methods.lower()
    assert "day of the year" in methods.lower()
    assert "15 July 2018" in methods
    assert "No Model 3 health coefficients" in methods
    assert r"\tag{1}" in methods or "(1)" in methods
    assert "Model 2 additionally adds" in methods
    # Model 1 equation must not already contain RH/rain (those are Model 2).
    eq = methods.split("Model 2 additionally", 1)[0]
    assert "RH_t" not in eq and r"\mathrm{RH}" not in eq
    assert "Rain_t" not in eq and r"\mathrm{Rain}" not in eq


def test_goggins_citation_is_humidity_only():
    methods = _methods()
    assert "relative humidity [21]" in methods
    assert "rainfall [22]" in methods
    assert "Goggins and Chan included rainfall" not in methods
    assert "both high and low relative humidity" in methods
    assert "deters hospital attendance" in methods
    assert "12.113035" in _full()
    assert "Bull World Health Organ" in _full()


def test_no_results_or_wip_in_methods():
    methods = _methods()
    assert "UW XX-XXX" in methods  # Hogan typed this placeholder; Roro fills it.
    assert "authors will determine" not in methods.lower()
    assert "protocol may need" not in methods.lower()
    assert "type i" not in methods.lower()
    assert "141 of 145" not in methods
    assert "Roadside monitors were not used" in methods
    assert "outcome co-investigator" not in methods.lower()
    assert "chd_inpatient" not in methods
    assert "named in correspondence" not in methods.lower()
    assert "authors will determine" not in _full().lower()


def test_acknowledgements_ethics_and_code_url():
    text = _full()
    assert re.search(r"## Acknowledgements\n\nNone\.", text)
    assert "https://github.com/bobshenruililin/Laidlaw-Heat-Project" in text
    assert "data-sharing agreement" not in text.lower()
    assert "data sharing agreement" not in text.lower()
    assert "Scientific roles are recorded in the Acknowledgements" not in text
    assert "Author order after the first and last" not in text
    assert "We thank" not in text.split("## Acknowledgements", 1)[1].split("## Data", 1)[0]


def test_abstract_methods_names_models_without_calibration_failure():
    am = _abstract_methods()
    assert "Model 1" in am and "Model 2" in am and "Model 3" in am
    assert "Reported estimates are from Model 1" in am
    assert "Model 2 adds" in am
    assert "Model 3 replaces" in am
    assert "failed" not in am.lower()
    assert "calibration" not in am.lower()
    assert "not applied to the health series" not in am.lower()
    assert "core panel" not in am.lower()


def test_results_heading_is_model_1():
    text = _full()
    results = text.split("## Results", 1)[1].split("## Discussion", 1)[0]
    assert "### Model 1" in results
    assert "### Models 1–12" not in results
    assert "core count ratios" not in results.lower()
    assert "**Table 2. Model 1:" in results


def test_stroke_limitation_does_not_name_correspondence():
    lim = _full().split("**Limitations.**", 1)[1]
    assert "A corresponding stroke series was not available" in lim
    assert "named in correspondence" not in lim.lower()


def test_climatology_series_is_weather_only():
    rows = list(csv.DictReader(CLIM.open(encoding="utf-8")))
    assert len(rows) == 132
    assert rows[0]["month_id"] == "2013-01"
    assert rows[-1]["month_id"] == "2023-12"
    blob = CLIM.read_text(encoding="utf-8").lower()
    assert "chd" not in blob
    assert "hf" not in {k.lower() for k in rows[0].keys()}
    needed = {
        "n_days_tmean_above_doy",
        "n_days_tmean_below_doy",
        "n_days_tmax_above_doy",
        "n_days_tmax_below_doy",
        "n_days_tmin_above_doy",
        "n_days_tmin_below_doy",
    }
    assert needed <= set(rows[0].keys())
    warm = sum(int(r["n_days_tmean_above_doy"]) for r in rows) / 132
    cool = sum(int(r["n_days_tmean_below_doy"]) for r in rows) / 132
    assert 10 < warm < 20
    assert 10 < cool < 20



def test_final_docx_and_pdf_exist_when_built():
    """Builder writes both files. Skip-not: they must exist after script 64."""
    assert DOCX.is_file(), f"missing {DOCX}"
    assert PDF.is_file(), f"missing {PDF}"
    assert DOCX.stat().st_size > 50_000
    assert PDF.stat().st_size > 50_000
    from docx import Document

    d = Document(str(DOCX))
    texts = "\n".join(p.text for p in d.paragraphs)
    assert HOGAN_OPEN in texts
    assert HOGAN_AVG in texts
    assert "Model 1" in texts and "Model 2" in texts and "Model 3" in texts
    assert "core panel" not in texts.lower()
    assert "authors will determine" not in texts.lower()
    assert "141 of 145" not in texts.split("Results", 1)[0]
    assert "Table 2 reports Model 1" in texts
    assert "Paste into the shared live document" in texts
    assert "[22]" in texts
    assert "daily mean temperature" in texts
    assert "failed simulation calibration" not in texts.split("Results", 1)[0]
    comments = list(d.comments)
    assert len(comments) >= 4
    joined = " ".join(c.text for c in comments)
    assert "UW XX-XXX" in joined or "IRB" in joined
    assert "Model 2" in joined
    assert "rainfall" in joined.lower()


if __name__ == "__main__":
    tests = [
        test_hogan_weather_sentence_copied,
        test_numbered_models_and_equation_symbols,
        test_goggins_citation_is_humidity_only,
        test_no_results_or_wip_in_methods,
        test_acknowledgements_ethics_and_code_url,
        test_abstract_methods_names_models_without_calibration_failure,
        test_results_heading_is_model_1,
        test_stroke_limitation_does_not_name_correspondence,
        test_climatology_series_is_weather_only,
        test_final_docx_and_pdf_exist_when_built,
    ]
    for fn in tests:
        fn()
        print("ok", fn.__name__)
    print("all passed")
