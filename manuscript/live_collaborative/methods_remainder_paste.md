# Methods remainder — 24 August 2026 (paste around Hogan’s weather paragraph)

Wording authority: `Heat_CVD_Manuscript_live_update.md`.

**Leave Hogan’s HKO paragraph in the live file.** Do not paste the weather block below over it. Paste the opening, Health data, then his existing paragraph, then the short processing paragraph, then Statistical analysis → Sensitivity → Software.

Do **not** paste “core panel”, “twelve core contrasts”, Results (141 of 145 cold days; VIF; overdispersion as a finding) into Methods, or “authors will determine ethics”.

---

### Opening (replaces Study design)

The study is an ecological territory-month time series for January 2013 through December 2023 (132 months). It cannot show effects for individual people, the cause of any admission, or day-level triggering [14]. In line with ethical requirements, the study was approved by the Institutional Review Board (IRB) of the HKU/Hospital Authority HK West Cluster (IRB reference number: UW XX-XXX).

Live-file comment @Roro (KW11): please replace `UW XX-XXX` with the actual IRB reference number. Do not invent a number.

Live-file comment (author line, not body): author order after the first and last positions remains to be confirmed with Professor Bishai.

### Health data

The cohort is people diagnosed with type 2 diabetes and/or hypertension in Hong Kong during 2013–2023. For each person, the event is the first recorded hospitalisation after the first diagnosis of coronary heart disease (CHD) or of heart failure (HF). Admission cause was not recorded. Monthly counts were supplied from Hospital Authority records. Age and sex strata were not included. CHD is the dependent variable in Models 1–6; HF is the dependent variable in Models 7–12.

Monthly influenza activity from November 2013 through December 2023 was obtained from Centre for Health Protection Flu Express summaries. January–October 2013 had no influenza values. Those months were left missing and were not coded as zero. Influenza was therefore not entered in Models 1–12; it is a sensitivity on the 121 months with data.

Mid-year age- and sex-specific population estimates from the Census and Statistics Department (Table 110-01001) were interpolated to month mid-points [8]. Those figures describe the general population, not the diabetes or hypertension group still at risk of a first CHD or HF hospitalisation. They are not the offset in Models 1–12.

Live-file comment @Roro: replace ICD lists and timing if they differ. Inpatient-only meaning is his to confirm — do not put that confirmation sentence in the body.

### Weather — his paragraph (do not overwrite)

Leave this text as Hogan wrote it:

> Meteorological data was obtained from the HKO. The monthly variables included: temperature (mean, minimum, maximum), relative humidity, total rainfall, the number of hot nights (Tmin ≥ 28°C), the number of very hot days (Tmax ≥ 33°C), the number of extremely hot days (Tmax ≥ 35°C), and the number of cold days (Tmin ≤ 12°C). Monthly mean pollutant levels for nitrogen dioxide (NO2), sulfur dioxide (SO2), and ozone (O3) were obtained from the Hong Kong Environmental Protection Department (EPD). All monthly data were derived by taking the average of daily data in each calendar month.

### Weather — processing paragraph (paste after his paragraph)

A station-month entered a pollutant mean only when at least 75% of expected observations were present. Missing measurements were not coded as zero. Territory-wide monthly pollutant concentrations are unweighted means of general EPD stations. Roadside stations were not used for those means. Fine particulate matter (PM2.5) from the same general stations was assembled for sensitivity analysis only.

Live-file comment @Hogan: in our pipeline, rainfall is a monthly **total** (mm), not an average of daily totals; official extreme days are **counts**; humidity is a **monthly mean**. The averaging sentence above is yours; we have not overwritten it.

Do **not** paste the December–February cold-day observation here (KW16 → Results).

### Statistical analysis

The dependent variable Y_t is the monthly number of first hospitalisations in month t. For each outcome we fitted six models. Each model included one temperature measure: monthly mean temperature, mean daily maximum temperature, mean daily minimum temperature, hot nights, very hot days, or cold days. Extreme-day counts were expressed per five days. Every model also included monthly mean relative humidity and monthly total rainfall [21]. The official count of extremely hot days (Tmax ≥ 35°C) was obtained with the other monthly weather variables and was not used as a temperature variable in Models 1–12.

Models 1–12 use a negative-binomial likelihood [10]:

log E(Y_t) = log(d_t) + α + β X_t + δ1 RH_t + δ2 Rain_t + Σ_{m=2}^{12} γ_m I(month_t = m) + s(t; 4 df).

Paste the symbol table and the Models 1–12 table from `Heat_CVD_Manuscript_live_update.md` (every symbol is defined there).

Each model contains one temperature variable. Temperature terms are not entered together in Models 1–12. We used negative-binomial regression, which allows monthly counts to vary more than a Poisson model permits. Quasi-Poisson regression was examined in sensitivity analysis.

We report 95% confidence intervals in four ways: the model’s own standard errors, HC1, Newey–West with a lag of 3 months, and Newey–West with a lag of 6 months [19]. The main reported interval is Newey–West with lag 6. A q-value is a p-value adjusted for testing Models 1–12 together [20].

### Sensitivity analysis

We repeated Models 4–6 and 10–12 with official extreme-day counts entered per 1 day and per 3 days, not only per 5 days.

We also checked the time trend (3, 6, or 8 degrees of freedom, or year indicators); the study window (dropping the first 12 or 24 months, or stopping at December 2019); COVID-period indicators; temperature one or two months earlier; and dropping the most influential month.

Further checks used general-population × days as the offset (this is still a count ratio, not cohort incidence); maximum and minimum temperature in one model, or the three official extreme-day counts in one model; influenza on the 121 months with data; and nitrogen dioxide or PM2.5.

We also counted, in each calendar month, how many days were warmer or cooler than the historical average for that same day of the year. For each month-day (for example 15 January), the historical average of daily mean, maximum, and minimum temperature was the leave-one-year-out mean of that month-day across HKO daily records for 2012–2023. Each day in 2013–2023 was then classified as above or below that average. Equal values were counted as neither. This encoding does not replace the official HKO thresholds in Models 1–12.

Residual correlation was inspected with Pearson autocorrelation and Ljung–Box tests at lags 6 and 12.

Separately, we tested a published method for estimating daily temperature effects from monthly outcomes using simulated Hong Kong weather [15,16].

### Software (KW18: keep)

Analyses were conducted in R 4.3.3 (2024-02-29). Negative-binomial models used MASS::glm.nb (MASS 7.3-60.0.1). Newey–West and HC1 standard errors used sandwich 3.1.3. Natural cubic splines used splines::ns.

### Delete from the live file

- “specified after the outcome series were available” (KW9)
- Long Ethics and governance paragraph about confirmation / protocol amendment (email + KW10)
- Acknowledgements that name co-authors (KW19)
- Data-availability sentence that only says “external submission requires team confirmation” (KW20 → GitHub link + HA/IRB sentence)

### Table 2 and Abstract (Word comments, not body text)

Methods now include monthly mean relative humidity and monthly total rainfall in Models 1–12. The current Table 2 numbers are from the earlier specification **without** those two covariates. **Refit on the governed panel before leaving Table 2 uncommented.** Do not invent new coefficients. This checkout does not contain the governed analysis panel.

If Hogan’s Abstract Methods still mentions the daily-recovery calibration failure, delete that sentence. It stays in Results.

Suggested Word comments: copy from `hogan_20260824_paste_replies.md` (Table 2 and Abstract).

