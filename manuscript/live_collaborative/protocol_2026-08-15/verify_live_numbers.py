#!/usr/bin/env python3
"""Check live manuscript Table 2/3 displays against release CSVs. No new models."""
import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
MS = ROOT / "manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md"
CORE = ROOT / "outputs/release_chd_hf/tables/table2_core_models.csv"
LADDER = ROOT / "outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv"

text = MS.read_text(encoding="utf-8")
text_norm = text.replace("\u2013", "-").replace("\u2212", "-")
failures = []

for row in csv.DictReader(CORE.open(encoding="utf-8-sig")):
    ci = row["count_ratio_95CI"]
    if ci not in text_norm:
        failures.append(f"missing Table 2 CI {row['outcome']} {row['exposure']}: {ci}")

need = [
    (("chd", "hot_nights", "model"), "1.022 (0.995-1.049)"),
    (("chd", "hot_nights", "HC1"), "1.022 (0.997-1.047)"),
    (("chd", "hot_nights", "NeweyWest_lag6"), "1.022 (1.002-1.042)"),
    (("hf", "cold_days", "model"), "1.073 (1.023-1.125)"),
    (("hf", "cold_days", "NeweyWest_lag6"), "1.073 (1.006-1.144)"),
]
ladder = {(r["outcome"], r["exposure"], r["se_method"]): r for r in csv.DictReader(LADDER.open(encoding="utf-8-sig"))}
for key, expected in need:
    display = ladder[key]["count_ratio_95CI"]
    if display != expected:
        failures.append(f"ladder CSV {key} is {display}, expected {expected}")
    if display not in text_norm:
        failures.append(f"missing ladder display {display}")

if "Meteorological data was obtained from the HKO." not in text:
    failures.append("Hogan weather sentence missing or edited")
if "pathway variable" in text or "lie on its pathway" in text:
    failures.append("causal ozone pathway language still present")
if "The authors declare no competing interests." in text:
    failures.append("invented competing-interest none still present")
if re.search(r"medication|housing|behavioural adaptation|air-conditioning", text, re.I):
    # Acknowledgements may mention guidance only; flag body hits
    failures.append("unmeasured factor named (check context)")

if failures:
    print("FAIL")
    for f in failures:
        print("-", f)
    sys.exit(1)
print("PASS: live Table 2/3 displays match CSVs; Hogan weather intact; ozone/COI guards ok")
