"""Evidence harness for the Opus 5 PR69-vs-PR70 verdict.

Checks every load-bearing factual claim in
`manuscript/live_collaborative/opus5_verdict_pr69_vs_pr70.md` against the actual
files, then demonstrates that rewrites R1-R3 satisfy the proposed locks while the
blocker locks survive.

Read-only. Fits no health model and reads no governed HA panel. Requires the
PR 69 ref `origin/cursor/hogan-methods-rewrite-1754` to be fetched.
"""
from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path

ROOT = Path("/workspace")
PASS: list[str] = []
FAIL: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    (PASS if cond else FAIL).append(f"{name}" + (f"  [{detail}]" if detail else ""))


def git_show(ref: str, path: str) -> str:
    return subprocess.run(
        ["git", "show", f"{ref}:{path}"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout


PR69 = "origin/cursor/hogan-methods-rewrite-1754"
PRE_PIVOT_REF = "637eb6b"
MS = "manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md"

pr69_ms = git_show(PR69, MS)
pr70_ms = git_show(PRE_PIVOT_REF, MS)
pr69_test = git_show(PR69, "tests/test_hogan_methods_rewrite.py")
pr70_test = git_show(PRE_PIVOT_REF, "tests/test_hogan_methods_rewrite.py")


def methods(text: str) -> str:
    return text.split("## Methods", 1)[1].split("## Results", 1)[0]


def abstract_methods(text: str) -> str:
    abs_block = text.split("## Abstract", 1)[1].split("## Introduction", 1)[0]
    return re.search(r"\*\*Methods\.\*\*(.+?)\*\*Results\.\*\*", abs_block, re.S).group(1)


# ---------------------------------------------------------------- L1 ethics
import pymupdf  # noqa: E402

pdf = pymupdf.open(ROOT / "Commented_Heat_CVD_Manuscript_20260824.pdf")
pdf_text = "".join(p.get_text() for p in pdf)

check("L1 circulated PDF body contains 'UW XX-XXX'", "UW XX-XXX" in pdf_text)
check(
    "L1 placeholder precedes the 'Health data' heading (start of Methods)",
    pdf_text.index("UW XX-XXX") < pdf_text.index("Health data"),
)
check("L1 KW10 anchors the one-sentence ethics instruction", "You only need one sentence" in pdf_text)
check("L1 KW11 asks Roro for the IRB number 'here'", "Can you input the IRB" in pdf_text)
check("L1 PR69 keeps the placeholder in Methods", "UW XX-XXX" in methods(pr69_ms))
check("L1 PR70 deletes the placeholder (fails)", "UW XX-XXX" not in pr70_ms)
check(
    "L1 PR70 test enforces the wrong lock",
    'assert "UW XX-XXX" not in methods' in pr70_test,
)
check(
    "L1 PR69 test enforces retention",
    'assert "UW XX-XXX" in methods' in pr69_test,
)
check(
    "L1 PR70 places ethics after the software paragraph",
    pr70_ms.index("Analyses were run in R 4.3.3")
    < pr70_ms.index("This study was approved by the Institutional Review Board"),
)

# ------------------------------------------------- L2 no invented coefficients
for label, text in (("PR69", pr69_ms), ("PR70", pr70_ms)):
    body = text.split("## Results", 1)[1]
    check(f"L2 {label} Table 2 rows unchanged (CHD hot nights 1.022)", "1.022 (1.002–1.042)" in body)
    check(f"L2 {label} Table 2 rows unchanged (HF cold days 1.073)", "1.073 (1.006–1.144)" in body)
    check(f"L2 {label} no invented IRB number", not re.search(r"UW \d", text))
check("L2 PR69 Table 2 caption names Model 1", "**Table 2. Model 1:" in pr69_ms)
check("L2 PR70 Table 2 caption omits Model 1 (weaker)", "**Table 2. Model 1:" not in pr70_ms)

# ------------------------------------------- L3 Abstract Methods free of results
check(
    "L3 PR70 Abstract Methods states a calibration result (fails)",
    "failed simulation calibration" in abstract_methods(pr70_ms),
)
check(
    "L3 PR69 Abstract Methods is calibration-free",
    "calibration" not in abstract_methods(pr69_ms).lower()
    and "failed" not in abstract_methods(pr69_ms).lower(),
)
check(
    "L3 PR70 test scope cannot see the Abstract",
    "_abstract" not in pr70_test and "_abstract_methods" in pr69_test,
)

# ----------------------------------------------------- L4 tense on unfitted models
check(
    "L4 PR69 Abstract uses past tense for Model 2 (defect)",
    "Model 2 added" in abstract_methods(pr69_ms),
)
check(
    "L4 PR69 Methods uses past tense for Model 2 (defect)",
    "Model 2 additionally included" in methods(pr69_ms),
)
check(
    "L4 PR69 Abstract 'Model 3 used' also implies fits (defect)",
    "Model 3 used counts" in abstract_methods(pr69_ms),
)
check(
    "L4 PR69 Methods 'Model 3 counted' describes the built weather series, not a fit",
    "Model 3 counted, for each month" in methods(pr69_ms)
    and "Model 3 is specified and is not reported in Table 2" in methods(pr69_ms),
)
check("L4 PR70 uses present tense for Model 2", "Model 2 adds" in methods(pr70_ms))
check(
    "L4 PR70 uses present tense for Model 3 in both sections",
    "Model 3 replaces" in abstract_methods(pr70_ms) and "Model 3 uses" in methods(pr70_ms),
)
check(
    "L4 PR70 miscounts Model 3 fits as twelve",
    "the same twelve fits" in methods(pr70_ms),
)

# ------------------------------------------------------------- L5 no WIP in body
WIP = ["outcome co-investigator", "chd_inpatient", "hf_inpatient", "named in correspondence",
       "External dissemination", "Author order after the first and last"]
for term in WIP:
    check(f"L5 PR70 body carries WIP: {term!r} (fails)", term.lower() in pr70_ms.lower())
    check(f"L5 PR69 body free of WIP: {term!r}", term.lower() not in pr69_ms.lower())

# ------------------------------------------------------- L6 Hogan weather verbatim
HOGAN_AVG = "All monthly data were derived by taking the average of daily data in each calendar month."
for label, text in (("PR69", pr69_ms), ("PR70", pr70_ms)):
    check(f"L6 {label} keeps Hogan's averaging sentence verbatim", HOGAN_AVG in text)
    check(f"L6 {label} does not contradict it in the body", "not an average" not in text.lower())

# -------------------------------------------------------------- L7 citations
check("L7 PR69 cites [21] for humidity", "relative humidity [21]" in methods(pr69_ms))
check("L7 PR69 cites [22] for rainfall", "rainfall [22]" in methods(pr69_ms))
check("L7 PR69 carries the [22] reference", "10.2471/BLT.12.113035" in pr69_ms)
check("L7 PR70 leaves rainfall uncited", "rainfall [22]" not in pr70_ms and "[22]" not in pr70_ms)
check(
    "L7 neither PR claims Goggins 2017 used rainfall",
    all("rainfall [21]" not in t for t in (pr69_ms, pr70_ms)),
)
check(
    "L7 PR69 flattens the both-tails humidity finding (defect)",
    "both high and low" not in methods(pr69_ms).lower(),
)

# Primary-source quotes are recorded durably in the literature note so this
# harness does not depend on a transient web fetch.
LIT = (ROOT / "literature" / "goggins2017_chan2013_humidity_rainfall_confirmed.md").read_text(
    encoding="utf-8"
)
check(
    "L7 [21] predictors recorded verbatim: temperature, humidity, wind speed",
    "**daily mean temperature, humidity, and wind speed** as predictors" in LIT,
)
check(
    "L7 [21] humidity finding recorded as both-tails and modest",
    "**Both high and low relative humidity were modestly associated with more admissions.**" in LIT,
)
check(
    "L7 [22] deterrence hypothesis recorded verbatim",
    "based on the hypothesis that heavy rain would deter people from going to hospital" in LIT,
)
check(
    "L7 [22] rainfall recorded as same-day and square-root transformed",
    "Same-day rainfall (square-root-transformed)" in LIT,
)
check(
    "L7 literature note carries both DOIs",
    "10.1016/j.ijcard.2016.11.106" in LIT and "10.2471/BLT.12.113035" in LIT,
)
check(
    "L7 literature note forbids a rainfall-effect claim",
    'never "was associated with"' in LIT,
)

# ---------------------------------------------------------------- L8 Model 3
check("L8 PR69 labels max/min counts as sensitivities",
      "sensitivity analyses" in methods(pr69_ms) and "daily maximum and minimum" in methods(pr69_ms))
check("L8 PR69 states the tie rule", "Equal values were counted as neither" in methods(pr69_ms))
check("L8 PR70 omits the tie rule", "counted as neither" not in methods(pr70_ms))

clim70 = list(csv.DictReader((ROOT / "data_processed" / "hogan_climatology_day_counts_2013_2023.csv").open()))
ties = sum(
    int(r["n_days"]) - int(r["days_warmer_than_climatology"]) - int(r["days_cooler_than_climatology"])
    for r in clim70
)
tie_months = sum(
    1 for r in clim70
    if int(r["n_days"]) != int(r["days_warmer_than_climatology"]) + int(r["days_cooler_than_climatology"])
)
check("L8 tie days are material", ties == 12 and tie_months == 10, f"{ties} days in {tie_months} months")
check("L8 neither PR puts six counts in one model",
      "six counts" not in pr70_ms.lower() and "six counts" not in pr69_ms.lower())

# ----------------------------------------------------------- L9 core/panel residue
res69 = re.findall(r"core (?:panel|count|models)|exploratory panel|complete panel", pr69_ms, re.I)
res70 = re.findall(r"core (?:panel|count|models)|exploratory panel|complete panel", pr70_ms, re.I)
check("L9 PR69 has no core/panel residue", not res69, f"{res69}")
check("L9 PR70 retains core/panel residue", len(res70) == 3, f"{res70}")
check("L9 'core' was the phrase Hogan asked us to retire", "as the core panel" in pdf_text)

# ------------------------------------------------------- L10 Abstract exposures
check("L10 PR70 Abstract names the day counts",
      "hot nights" in abstract_methods(pr70_ms) and "cold days" in abstract_methods(pr70_ms))
check("L10 PR69 Abstract mislabels day counts as temperature measures",
      "Each temperature measure entered" in abstract_methods(pr69_ms))

# ------------------------------------------------- L11 Methods antecedent for joint models
check("L11 PR70 Results report joint VIF models", "variance inflation factor of 4.66" in pr70_ms)
check("L11 PR70 Methods never declare them (fails)",
      "in one model" not in methods(pr70_ms) and "jointly" not in methods(pr70_ms))
check("L11 PR69 Methods declare them", "in one model" in methods(pr69_ms))

# --------------------------------------------------------- L12 extremely hot days
check("L12 PR69 explains the unused 35C count",
      "was not used as a temperature variable in Model 1" in methods(pr69_ms))
check("L12 PR70 omits that explanation",
      "not used as a temperature variable" not in methods(pr70_ms))

# ------------------------------------------------------------------ L13 / S9
inv = (ROOT / "manuscript" / "live_collaborative" / "supplement_inventory.md").read_text()
check("L13 S9 is the pollution-staged archive table", "Supplementary Table S9" in inv and "P11" in inv)
check("L13 S9 used joint Tmax/Tmin and a population-days offset",
      "joint Tmax/Tmin; population×days offset" in inv)
check("L13 PR70 states the reason S9 is not adjusted Model 1",
      "general-population offset and joint maximum and minimum temperature" in pr70_ms)
check("L13 PR69 states only the conclusion",
      "are sensitivities, not replacements for Model 1" in pr69_ms)
check("L13 S1 is the residual ACF, so both PRs cite it correctly",
      "Residual ACF" in inv and "Supplementary Figure S1" in pr69_ms and "Supplementary Figure S1" in pr70_ms)

# ------------------------------------------------------------------- L14 KW18
kw18 = pdf_text.index("Commented [KW18]")
check("L14 KW18 'Good.' anchors to Table 1, not Software",
      "Table 1. Outcome summary." in pdf_text[kw18 - 1200:kw18]
      and "MASS::glm.nb" not in pdf_text[kw18 - 1200:kw18])
check("L14 PR69 inventory mis-attributes KW18 to Software",
      "| KW18 | Software |" in git_show(PR69, "manuscript/live_collaborative/hogan_20260824_comment_inventory.md"))

# --------------------------------------------------------------- L15 provenance
check("L15 PR70 file carries provenance columns",
      {"climatology_rule", "n_clim_years_min", "data_status"} <= set(clim70[0]))
check("L15 PR70 provenance is REAL_PUBLIC_HKO with a stated rule",
      clim70[0]["data_status"] == "REAL_PUBLIC_HKO"
      and clim70[0]["climatology_rule"] == "leave_one_year_out_same_calendar_day_2012_2023")
clim69 = list(csv.DictReader(git_show(PR69, "data_processed/hogan_abnormal_day_counts_2013_2023.csv").splitlines()))
check("L15 PR69 file has six symmetric counts",
      len([k for k in clim69[0] if k.startswith("n_days_t")]) == 6)
check("L15 PR69 file lacks provenance columns",
      not {"climatology_rule", "data_status"} & set(clim69[0]))
check("L15 PR70 file is asymmetric (four counts)",
      len([k for k in clim70[0] if k.startswith("days_")]) == 4)
check("L15 both series are 132 months", len(clim69) == 132 and len(clim70) == 132)

# ----------------------------------------------------------- L16 script numbers
main_scripts = subprocess.run(
    ["git", "ls-tree", "-r", "--name-only", "origin/main"], cwd=ROOT,
    capture_output=True, text=True, check=True).stdout
check("L16 scripts/52_ and 53_ already taken on main",
      "scripts/52_public_outcome_ceiling_search.py" in main_scripts
      and "scripts/53_mde_from_uncertainty_ladder.py" in main_scripts)
pr69_files = subprocess.run(
    ["git", "ls-tree", "-r", "--name-only", PR69], cwd=ROOT,
    capture_output=True, text=True, check=True).stdout
check("L16 PR69 collides at 52 and 53",
      "scripts/52_hogan_abnormal_day_counts.py" in pr69_files
      and "scripts/53_hogan_models_rh_rain.R" in pr69_files)
check("L16 PR70 avoids the collision with 61/62/63",
      (ROOT / "scripts" / "61_hogan_climatology_day_counts.py").is_file()
      and (ROOT / "scripts" / "62_fit_hogan_model2_model3.py").is_file())

# --------------------------------------------------------------- L17 deliverable
check("L17 PR69 ships a full manuscript Word and PDF",
      "Heat_CVD_Manuscript_20260824_hogan.docx" in pr69_files
      and "Heat_CVD_Manuscript_20260824_hogan.pdf" in pr69_files)
check("L17 PR70 ships a Methods-only paste",
      (ROOT / "manuscript" / "live_collaborative" / "Heat_CVD_Methods_20260824_paste.docx").is_file())

# ------------------------------------------------------------------ L18 tests
check("L18 PR69 suite is materially larger",
      pr69_test.count("def test_") == 11 and pr70_test.count("def test_") == 6,
      f"PR69 {pr69_test.count('def test_')} vs PR70 {pr70_test.count('def test_')}")
check("L18 PR70 suite is green while L1/L3/L5 are violated",
      subprocess.run(["python3", "tests/test_hogan_methods_rewrite.py"], cwd=ROOT,
                     capture_output=True, text=True).returncode == 0)

# ============================ rewrites R1-R3 satisfy the proposed locks =========
R1 = (
    "Model 2 adds monthly mean relative humidity and monthly total rainfall to Model 1. "
    "Goggins and Chan entered daily mean temperature, humidity, and wind speed as predictors "
    "of daily heart-failure admissions and deaths in Hong Kong, and reported that both high and "
    "low relative humidity were modestly associated with more admissions [21]. Chan et al. "
    "included same-day rainfall in Hong Kong hospital-admission models on the hypothesis that "
    "heavy rain deters people from going to hospital [22]. Both papers fitted daily values, so a "
    "monthly mean and a monthly total are coarser than the terms they used. Table 2 reports Model 1."
)
R2 = (
    " Model 1 is a separate negative-binomial model for each of three continuous temperature "
    "measures and the official counts of hot nights, very hot days, and cold days, with "
    "calendar-month indicators, a 4-df time spline, and an offset for the number of days in the "
    "month. Model 2 adds monthly mean relative humidity and monthly total rainfall. Model 3 "
    "replaces the official extreme-day counts with counts of days warmer or cooler than the "
    "same-calendar-day historical mean. Reported estimates are from Model 1."
)
R3 = (
    "Model 3 counts, for each month, the days whose daily mean temperature was above or below the "
    "historical average for that day of the year. For 15 July 2018, for example, that average is "
    "the mean of every other 15 July in the Hong Kong Observatory daily series for 2012–2023, "
    "leaving 2018 out. Days equal to that average were counted as neither. The same counts built "
    "from daily maximum and daily minimum temperature are sensitivity analyses. Table 2 reports Model 1."
)

merged = pr69_ms
old_m2 = re.search(r"Model 2 additionally included.*?\n", merged).group(0)
merged = merged.replace(old_m2, R1 + "\n")
old_m3 = re.search(r"Model 3 counted, for each month.*?\n", merged).group(0)
merged = merged.replace(old_m3, R3 + "\n")
old_am = re.search(
    r"Each temperature measure entered.*?Reported estimates are from Model 1\.", merged, re.S).group(0)
merged = merged.replace(old_am, R2.strip())

m_meth, m_am = methods(merged), abstract_methods(merged)

# proposed test_unfitted_models_are_present_tense
for blob in (m_meth, m_am):
    check("R+ present tense for Model 2", "Model 2 adds" in blob)
    check("R+ no past-tense Model 2", "Model 2 added" not in blob
          and "Model 2 additionally included" not in blob)
    check("R+ no past-tense Model 3", "Model 3 used" not in blob)
check("R+ no 'same twelve fits' for Model 3", "the same twelve fits" not in m_meth)

# proposed test_rainfall_citation_claims_hypothesis_not_effect
check("R+ [22] carries a hypothesis", "deters people from going to hospital [22]" in m_meth)
for bad in ("rainfall was associated", "effect of rainfall", "rainfall predicted",
            "goggins and chan entered rainfall"):
    check(f"R+ no rainfall-effect claim: {bad!r}", bad not in m_meth.lower())
check("R+ humidity keeps its both-tails shape", "both high and low relative humidity" in m_meth)

# proposed test_abstract_names_model1_exposures_precisely
check("R+ Abstract names hot nights and cold days", "hot nights" in m_am and "cold days" in m_am)
check("R+ Abstract drops the mislabel", "Each temperature measure entered" not in m_am)

# proposed test_methods_declare_every_reported_model
check("R+ joint models declared", "in one model" in m_meth or "jointly" in m_meth)
check("R+ quasi-Poisson declared", "quasi-Poisson" in m_meth)
check("R+ residual diagnostics declared", "Ljung" in m_meth or "autocorrelation" in m_meth)

# locks that must survive the rewrite
check("R+ L1 survives: ethics placeholder still in Methods", "UW XX-XXX" in m_meth)
check("R+ L3 survives: Abstract Methods calibration-free",
      "calibration" not in m_am.lower() and "failed" not in m_am.lower())
check("R+ L6 survives: Hogan averaging sentence verbatim", HOGAN_AVG in m_meth)
check("R+ L8 survives: tie rule and sensitivity labelling",
      "counted as neither" in m_meth and "sensitivity analyses" in m_meth)
check("R+ L9 survives: no core/panel residue",
      not re.findall(r"core (?:panel|count|models)|exploratory panel|complete panel", merged, re.I))
check("R+ L2 survives: Table 2 still Model 1 with unchanged rows",
      "**Table 2. Model 1:" in merged and "1.073 (1.006–1.144)" in merged)
check("R+ no Model 2 or Model 3 coefficient introduced",
      not re.search(r"Model [23][^.]{0,120}\d\.\d{2,3} \(", merged)
      and not re.search(r"\d\.\d{2,3} \([^)]*\)[^.]{0,120}Model [23]", merged))
check("R+ rewrite adds no new estimate anywhere",
      len(re.findall(r"\d\.\d{3} \(", merged)) == len(re.findall(r"\d\.\d{3} \(", pr69_ms)))
check("R+ R1 note: existing test split anchor must move off 'Model 2 additionally'",
      'methods.split("Model 2 additionally", 1)' in pr69_test and "Model 2 additionally" not in m_meth)

# ---------------------------------------------------------------------- report
print(f"\n{'=' * 74}\nOPUS 5 VERDICT EVIDENCE HARNESS\n{'=' * 74}")
for line in PASS:
    print(f"  CONFIRMED  {line}")
if FAIL:
    print(f"\n{'-' * 74}\nUNCONFIRMED CLAIMS ({len(FAIL)}):")
    for line in FAIL:
        print(f"  UNCONFIRMED  {line}")
print(f"\n{'=' * 74}\n{len(PASS)} confirmed, {len(FAIL)} unconfirmed\n{'=' * 74}")
raise SystemExit(1 if FAIL else 0)
