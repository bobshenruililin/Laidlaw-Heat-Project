# Paste-ready replies — Hogan 24 August 2026 (KW and email)

Copy into the matching balloons in the shared live file. Do not email these. Do not resolve threads until Hogan has read them. 28 July H1–H6 / H21 replies remain in `hogan_comment_paste_replies.md`.

---

**KW7 — “dependent variable”**

Changed. The dependent variable is the monthly first-hospitalisation count (CHD in Models 1–6; HF in Models 7–12).

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

Kept there, using your rewrite, with Models 1–12 in place of “core panel”.

---

**KW13 — why influenza is not in the main models**

January–October 2013 are missing. Influenza is a sensitivity on the 121 months with data, not a covariate in Models 1–12.

---

**KW14 and email — relative humidity and rainfall**

Monthly mean RH and monthly total rainfall now enter every one of Models 1–12, following Goggins and Chan 2017. The daily series were already in the HKO dailyExtract files; monthly mean RH and monthly total rainfall are in `data_processed/climate_monthly_2013_2023.csv`. Table 2 still needs a refit: on a machine with the governed panel, `Rscript scripts/53_hogan_models_rh_rain.R` writes `outputs/tables/table2_models_1_12_rh_rain.csv`. I will not type new coefficients by hand. I have left a Word comment on Table 2 to that effect.

Live-file comment on your averaging sentence: in our pipeline rainfall is a monthly total (mm), extreme days are counts, and humidity is a monthly mean. I have not overwritten your sentence.

---

**KW15 — five days vs three vs one**

Primary models keep per five days so the coefficient is a five-day contrast rather than a single extreme day. The term is linear on the log mean, so the per-1-day count ratio is the per-5-day ratio to the power 1/5 (confidence limits transformed the same way); per 3 days is the 3/5 power. I will still report the refitted per-1-day and per-3-day numbers as a software check of that identity.

---

**KW16 — cold days in December–February**

Removed from Methods. It stays in Results / Figure 2. Your note that this is a limitation of monthly matching is in the Discussion.

---

**KW17 — “roadside reserved”**

Rewritten: roadside stations were not used for the territory-wide monthly mean.

---

**KW18 — Software**

Left as is.

---

**KW19 — Acknowledgements**

Removed the named co-author thanks. There is no Acknowledgements section until someone who is not a co-author needs one.

---

**KW20 — Data and code**

Now: code is at https://github.com/bobshenruililin/Laidlaw-Heat-Project. Access to Hospital Authority data is governed by the data-sharing agreement and ethics approval.

---

**Email — numbered models; no Results in Methods; section order**

Methods are now: Data sources (health, then weather) → Statistical analysis (equation, symbol table, Models 1–12) → Sensitivity analysis. “Core panel” / “twelve core contrasts” are out of Methods, Results headings, and the Abstract.

---

**Email — Jingjing TV days**

Not used. TV is an index without a threshold, so I have not counted “TV days” per month.

Instead, as you suggested: for each day of the year I took the historical average of daily mean, max, and min temperature, then counted how many days in each calendar month sat above or below that same-day average (`scripts/52_hogan_abnormal_day_counts.py`; `data_processed/hogan_abnormal_day_counts_2013_2023.csv`). I used a leave-one-year-out average so that 15 January 2018 is not judged against a mean that already includes 15 January 2018. Ties count as neither. If you instead meant days above the historical record maximum or below the record minimum for that calendar date, say so and I will recode.

This is a sensitivity only. Models 1–12 still use the official HKO thresholds. These counts will not winter-peak the way your TV lag 0–1 series does: about half the days in both January and July sit below the day-of-year mean (January mean 12.7 days below; July mean 12.1). That is expected for a day-of-year anomaly count. It is not a TV replicate, and I will not sell it as one.

---

**Email — work in the shared document**

This pack is for pasting into the live file, not a parallel emailed Word manuscript.

---

**Email — work-in-progress ethics / author order**

Removed from the body. Author-order confirmation with Professor Bishai is a live-file comment, not a manuscript sentence. IRB number is still your `UW XX-XXX` until Roro fills it.

---

**Table 2 and Abstract (not KW balloons)**

Word comment on Table 2:

> These count ratios are from Models 1–12 before monthly mean relative humidity and monthly total rainfall were entered. They will be replaced after the governed panel is refit. No new coefficients have been typed by hand.

Word comment on the Abstract (and, if space, Tables 3 and Figure 3):

> All count ratios in this document — Abstract, Tables 2–3, Figure 3, and the sensitivity text — are from Models 1–12 before monthly mean relative humidity and monthly total rainfall were entered. The Abstract Methods sentence still describes that earlier specification. Everything will be replaced together after the governed panel is refit (`scripts/53_hogan_models_rh_rain.R`). No new coefficients have been typed by hand.

Also delete the daily-recovery failure sentence from Abstract Methods if it is still there from the 15 August paste. That result stays in Results.
