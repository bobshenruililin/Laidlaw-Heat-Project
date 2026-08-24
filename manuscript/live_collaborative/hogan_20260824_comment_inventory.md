# Hogan 24 August 2026 commented PDF — inventory

**File:** `Commented_Heat_CVD_Manuscript_20260824.pdf` (repo root; 16 pp; author Hogan; Word export).  
**Acrobat `/Annot` markup:** none. Comments are Word balloons flattened into the text as `Commented [H…]` and `Commented [KW…]`. Extracted with `pdftotext -layout`. All 21 markers recovered: H1–H6, KW7–KW20, H21. Do not invent further balloons. `scripts/extract_pdf_annotations.py` returns empty on this file; that is not “no comments.”

**Email (same day), not in the PDF balloons:** Methods too complex (rewrite lines 108–175); drop “core panel” / “twelve core contrast” for numbered models a high-school reader can follow; no Results in Methods; order = data sources (health, weather), statistical analysis (equation + variable definitions), sensitivity analysis; no work-in-progress ethics in the body (use a comment); keep editing the shared live file; cold-day winter identification is a limitation and the interpretation is fine; add monthly rainfall and relative humidity (Goggins and Chan 2017); do not count “TV days”; instead count days above/below the day-of-year historical mean/max/min.

**Hogan weather paragraph in this PDF (leave in the live file; do not overwrite):**

> Meteorological data was obtained from the HKO. The monthly variables included: temperature (mean, minimum, maximum), relative humidity, total rainfall, the number of hot nights (Tmin ≥ 28°C), the number of very hot days (Tmax ≥ 33°C), the number of extremely hot days (Tmax ≥ 35°C), and the number of cold days (Tmin ≤ 12°C). … All monthly data were derived by taking the average of daily data in each calendar month.

Live-file comment only (not body text): rainfall in our pipeline is a **monthly total (mm)**; extreme days are **counts**; humidity is a **monthly mean**.

| ID | Locus in PDF | His text (verbatim sense) | Action |
|---|---|---|---|
| H1 | Title / running title | Running title proposed by Bob. Will need to be amended once results have been generated. | Keep running title now that CHD/HF results exist. |
| H2 | Authors | To be determined after discussion with Dr. Bishai. | Leave Author 2–4 placeholders. |
| H3 | Intro AMI/stroke sentence | Remove now since the scope of the study has changed? | Already removed as our endpoint in the 15 Aug Introduction. |
| H4 | Housing / behaviour / pollution | Cite the papers. If we don’t have housing and behavioural adaptation data, do not mention them; consider medication instead. Do not raise an uncontrolled factor. | Housing/behaviour/medication stay out. Cite only handled factors. |
| H5 | “environmental context has also evolved” | Sounds as if pollutants changed after Goggins 2009. If not, remove or rewrite. | 15 Aug pollution paragraph already rewrites this as 2013–2023 EPD means, not Goggins 2000–2009. |
| H6 | Thesis paragraph | Combine into one sentence after Results. | 15 Aug close is one sentence. |
| KW7 | Study design “target quantity” | Prefer “dependent variable.” | Use “dependent variable.” |
| KW8 | “days in month” | Do you mean “the number of days in a month”? | Yes; write it that way. |
| KW9 | “specified after the outcome series were available” | Once the outcome series is available, remove this sentence. | Delete. |
| KW10 | Ethics | One sentence that the study has ethics approval. Other stuff deleted. | One sentence. Do not paste the old “authors will determine” paragraph. Do not invent the IRB number. |
| KW11 | IRB number | @Roro: input the IRB reference number. | Live-file comment only. Leave `UW XX-XXX` if Hogan already typed it; we do not invent a number. |
| KW12 | Influenza | Moved into Health data and rewritten. | Keep influenza under Health data. |
| KW13 | Influenza not in the main models | Brief justification needed. | One sentence: influenza is missing for Jan–Oct 2013, so it is a sensitivity, not a primary covariate. |
| KW14 | RH and rainfall in the weather list | Include / take this data as well. | Obtain monthly mean RH and monthly total rainfall; **enter both in Models 1–12** (email + Goggins and Chan 2017). |
| KW15 | Per-five-day scale | Why five days and not three? How do values differ for a single extreme day? Sensitivity. | Primary: per 5 days. Sensitivity: per 1 day and per 3 days. Do not invent those coefficients until the governed panel is refit. |
| KW16 | Cold days in DJF in Methods | Remove. This is an observation → Results. | Move to Results (already there). Methods stay silent on 141/145. |
| KW17 | “Roadside stations were reserved” | Reserved for what? | Rewrite: roadside stations were **not used** for the territory-wide monthly mean. |
| KW18 | Software | Good. | Keep. |
| KW19 | Acknowledgements | Do not list co-authors. Section is for people who helped without intellectual contribution. At the moment, nobody to acknowledge. | Drop named co-author thanks. |
| KW20 | Data and code | Code: GitHub link. Data: check with Roro / IRB what can be shared. | Rewrite. No “external submission requires team confirmation” as body WIP. |
| H21 | Goggins 2013 | Yang C-Y → Yang CY | Keep Yang CY. |

**Cannot read:** no other balloons. Line-108–175 complexity is the email, not a balloon.

**Governed panel:** not in this checkout. Abnormal-day weather counts can be built from HKO daily files. Models 1–12 **with** RH and rainfall cannot be refit here. Do not invent new Table 2 numbers. Paste Methods as the specification Hogan asked for; Word-comment that Table 2 must be replaced after Bob refits on the governed panel.

**Not done in this pass:** Jingjing TV-day counts (Hogan rejected). AMI/stroke/principal-dx claims. Overwriting Hogan’s HKO weather sentence.
