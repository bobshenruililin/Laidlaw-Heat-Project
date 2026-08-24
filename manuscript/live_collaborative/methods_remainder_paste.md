# Methods remainder — 24 August 2026 (paste around Hogan’s weather paragraph)

Wording authority: `Heat_CVD_Manuscript_live_update.md`.
Final Word/PDF: `Heat_CVD_Manuscript_20260824_hogan.docx` / `.pdf` (built by `scripts/64_hogan_20260824_manuscript_docx.py`).

**Leave Hogan’s HKO paragraph in the live file.** Do not paste the weather block below over it. Paste the opening, Health data, then his existing paragraph, then the short processing paragraph, then Population → Statistical analysis → Sensitivity → Software.

Do **not** paste “core panel”, “twelve core contrasts”, Results (141 of 145 cold days; VIF; overdispersion as a finding) into Methods, or “authors will determine ethics”.

Numbering is nested **Model 1 / Model 2 / Model 3**. Table 2 reports Model 1. Do not rename the twelve thermal fits as Models 1–12.

---

### Opening (replaces Study design)

The study is an ecological territory-month time series for January 2013 through December 2023 (132 months). It cannot show effects for individual people, the cause of any admission, or day-level triggering [14]. In line with ethical requirements, the study was approved by the Institutional Review Board (IRB) of the HKU/Hospital Authority HK West Cluster (IRB reference number: UW XX-XXX).

Live-file comment @Roro (KW11): please replace `UW XX-XXX` with the actual IRB reference number. Do not invent a number.

Live-file comment (author line, not body): author order after the first and last positions remains to be confirmed with Professor Bishai.

### Health data

The dependent variable is the monthly count of first hospitalisations after a first diagnosis of coronary heart disease (CHD), and separately of heart failure (HF), among people with type 2 diabetes and/or hypertension in Hong Kong. The cohort is people diagnosed with type 2 diabetes and/or hypertension during 2013–2023. For each person, the event is the first recorded hospitalisation after that person’s first CHD diagnosis or first HF diagnosis. Admission cause was not recorded. Monthly counts were supplied from Hospital Authority records. Age and sex strata were not included.

Monthly influenza activity from November 2013 through December 2023 was obtained from Centre for Health Protection Flu Express summaries. January–October 2013 had no influenza values. Those months were left missing and were not coded as zero. Influenza was therefore not entered in Model 1; it is a sensitivity on the 121 months with data.

Live-file comment @Roro: replace ICD lists and timing if they differ. Inpatient-only meaning is his to confirm — do not put that confirmation sentence in the body.

### Weather — his paragraph (do not overwrite)

Leave this text as Hogan wrote it:

> Meteorological data was obtained from the HKO. The monthly variables included: temperature (mean, minimum, maximum), relative humidity, total rainfall, the number of hot nights (Tmin ≥ 28°C), the number of very hot days (Tmax ≥ 33°C), the number of extremely hot days (Tmax ≥ 35°C), and the number of cold days (Tmin ≤ 12°C). Monthly mean pollutant levels for nitrogen dioxide (NO2), sulfur dioxide (SO2), and ozone (O3) were obtained from the Hong Kong Environmental Protection Department (EPD). All monthly data were derived by taking the average of daily data in each calendar month.

### Weather — processing paragraph (paste after his paragraph)

A station-month entered a pollutant mean only when at least 75% of expected observations were present. Missing measurements were not coded as zero. Territory-wide monthly pollutant concentrations are unweighted means of general EPD stations. Roadside monitors were not used for those means. Fine particulate matter (PM2.5) from the same general stations was assembled for sensitivity analysis only.

Live-file comment @Hogan: in our pipeline, rainfall is a monthly **total** (mm), not an average of daily totals; official extreme days are **counts**; humidity is a **monthly mean**. The averaging sentence above is yours; we have not overwritten it.

Do **not** paste the December–February cold-day observation here (KW16 → Results).

### Population

Mid-year age- and sex-specific population estimates from the Census and Statistics Department (Table 110-01001) were interpolated to month mid-points [8]. Those figures describe the general population, not the diabetes or hypertension group still at risk of a first CHD or HF hospitalisation. Model 1 therefore uses the number of days in the month as the offset and is read as a monthly count ratio, not as a cohort incidence rate [14]. A population × days offset is a sensitivity only. It does not turn the estimate into cohort incidence.

### Statistical analysis

Paste from `Heat_CVD_Manuscript_live_update.md` (Model 1 equation **without** RH/rain; words after the equation define every symbol; Model 2 adds rainfall and humidity with [21] on humidity only; Model 3 is the leave-one-year-out same-calendar-day counts). Table 2 reports Model 1.

### Sensitivity analysis / Software

Paste from the live_update. KW15 is a rescaling of the Model 1 extreme-day coefficient (*R*^(3/5) and *R*^(1/5)), not a new model. Keep Software version numbers (KW18: Good).

### Delete from the live file

- “specified after the outcome series were available” (KW9)
- Long Ethics and governance paragraph about confirmation / protocol amendment (email + KW10)
- Author-order italic in the body (H2 → comment only)
- Acknowledgements that name co-authors (KW19 → section reads `None.`)
- Data-availability sentence that only says “external submission requires team confirmation” (KW20 → GitHub link + HA/IRB sentence)
- “core panel” / “twelve core contrasts” / Results heading “Models 1–12”
- Daily-recovery calibration failure in Abstract Methods

### Table 2 and Abstract (Word comments, not body text)

Table 2 reports **Model 1** (thermal variables only). Model 2 (monthly mean RH + monthly total rainfall) and Model 3 (climatology day counts) are specified in Methods. **Do not invent Model 2 or Model 3 health coefficients.** On a machine with the governed panel, `Rscript scripts/53_hogan_models_rh_rain.R` writes Model 2.

If Hogan’s Abstract Methods still mentions the daily-recovery calibration failure, delete that sentence. It stays in Results.

Suggested Word comments: copy from `hogan_20260824_paste_replies.md` (Table 2 and Abstract).
