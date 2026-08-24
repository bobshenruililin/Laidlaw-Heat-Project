# Paste-ready replies — Hogan 24 August 2026 (KW and email)

Copy into the matching balloons in the shared live file. Do not email these. Do not resolve threads until Hogan has read them. 28 July H1–H6 / H21 replies remain in `hogan_comment_paste_replies.md`.

The rebuilt Word/PDF (`Heat_CVD_Manuscript_20260824_hogan.docx` / `.pdf`) already contains these as Word comments where they belong. Paste that file into the shared document, then copy any balloon replies that did not transfer.

---

**KW7 — “dependent variable”**

Changed. The dependent variable is the monthly first-hospitalisation count (CHD or HF). Model 1 is fitted once for each diagnosis × weather variable.

---

**KW8 — “number of days in a month”**

Yes. The offset is the number of days in that month.

---

**KW9 — remove “specified after the outcome series were available”**

Removed.

---

**KW10 / KW11 — one ethics sentence; IRB number**

Methods now have your one approval sentence, including the `UW XX-XXX` placeholder you typed. @Roro: please replace that placeholder with the HKU/HA HK West Cluster IRB reference number. I have not invented a number.

---

**KW12 — influenza under Health data**

Kept there. Influenza is not in Model 1; it is a sensitivity on the 121 months with data.

---

**KW13 — why influenza is not in the main models**

January–October 2013 are missing. Influenza is a sensitivity on the 121 months with data, not a covariate in Model 1.

---

**KW14 and email — relative humidity and rainfall**

Both are in the monthly weather list you wrote. Model 2 adds monthly mean relative humidity and monthly total rainfall to Model 1. Table 2 reports Model 1 (the thermal fits you already have). I have not typed Model 2 coefficients by hand.

Goggins and Chan 2017 [21] entered humidity (with temperature and wind speed) for daily heart-failure admissions. I cite [21] for humidity only. Rainfall is in Model 2 because it is in your monthly list, not because that 2017 paper used rainfall.

Live-file comment on your averaging sentence: in our pipeline rainfall is a monthly total (mm), extreme days are counts, and humidity is a monthly mean. I have not overwritten your sentence.

---

**KW15 — five days vs three vs one**

Model 1 keeps per five days so the coefficient is a five-day contrast rather than a single extreme day. The term is linear on the log mean, so this is a rescaling, not a new model: if the count ratio per five days is *R*, the count ratio per three days is *R*^(3/5) and per one day is *R*^(1/5). Confidence limits transform the same way.

---

**KW16 — cold days in December–February**

Removed from Methods. It stays in Results / Figure 2. Your note that this is a limitation of monthly matching is in the Discussion.

---

**KW17 — “roadside reserved”**

Rewritten: roadside monitors were not used for the territory-wide monthly mean.

---

**KW18 — Software**

Left as is, including version numbers.

---

**KW19 — Acknowledgements**

The section now reads `None.` Co-authors are not listed there.

---

**KW20 — Data and code**

Now: code is at https://github.com/bobshenruililin/Laidlaw-Heat-Project. Access to Hospital Authority data is governed by the data-sharing agreement and ethics approval.

---

**Email — numbered models; no Results in Methods; section order**

Methods are now: Data sources (health, weather, population) → Statistical analysis (Model 1 equation, then Model 2, then Model 3) → Sensitivity analysis → Software. “Core panel” / “twelve core contrasts” are out. Table 2 reports Model 1.

---

**Email — Jingjing TV days**

Not used. TV is an index without a threshold, so I have not counted “TV days” per month.

Instead, as you suggested: for each day of the year I took the historical average of daily mean, max, and min temperature, then counted how many days in each calendar month sat above or below that same-day average (`scripts/52_hogan_abnormal_day_counts.py`; `data_processed/hogan_abnormal_day_counts_2013_2023.csv`). I used a leave-one-year-out average so that 15 January 2018 is not judged against a mean that already includes 15 January 2018. Ties count as neither. That encoding is Model 3. Table 2 still reports Model 1 (official HKO thresholds). If you instead meant days above the historical record maximum or below the record minimum for that calendar date, say so and I will recode.

These counts will not winter-peak the way your TV lag 0–1 series does: about half the days in both January and July sit below the day-of-year mean (January mean 12.7 days below; July mean 12.1). That is expected for a day-of-year anomaly count. It is not a TV replicate, and I will not sell it as one.

---

**Email — work in the shared document**

The Word/PDF is the paste source for the live file, not a parallel emailed manuscript unless you ask for the file.

---

**Email — work-in-progress ethics / author order**

Removed from the body. Author-order confirmation with Professor Bishai is a live-file comment, not a manuscript sentence. IRB number is still your `UW XX-XXX` until Roro fills it.

---

**Table 2 and Abstract (not KW balloons)**

Word comment on Table 2:

> Table 2 reports Model 1 (thermal variables only; no monthly rainfall or humidity). Model 2 adds those two covariates and is specified in Methods. On a machine with the governed panel, run `Rscript scripts/53_hogan_models_rh_rain.R` and paste Model 2 beside or after Table 2. No new coefficients have been typed by hand. Model 3 (climatology day counts) is also specified and not fitted here.

Word comment on the Abstract:

> Abstract Results numbers are Model 1. Model 2 and Model 3 are named in Abstract Methods and specified in Methods; they are not fitted in this file. The daily-recovery calibration failure is in Results, not Abstract Methods.
