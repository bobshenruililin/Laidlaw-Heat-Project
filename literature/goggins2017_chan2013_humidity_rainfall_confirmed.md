# Confirmed citations — humidity `[21]` and rainfall `[22]` for Model 2

**Why this file exists.** Hogan's 24 August email asked us to add monthly rainfall and relative humidity and attributed both to Goggins and Chan 2017. That attribution is wrong for rainfall, and getting it wrong in the manuscript is the kind of error a supervisor catches on one read. Two parallel PRs handled it two different ways, so the underlying papers were checked against their published text rather than against either PR's summary. Verified 24 August 2026.

Provenance of this note: `REAL` published sources, verified against the publisher abstract and the archived WHO Bulletin full text. No coefficient here is a Laidlaw result.

---

## `[21]` Goggins and Chan 2017 — humidity, not rainfall

Goggins WB, Chan EYY. *A study of the short-term associations between hospital admissions and mortality from heart failure and meteorological variables in Hong Kong.* Int J Cardiol. 2017;228:537–542. `doi:10.1016/j.ijcard.2016.11.106`

Verbatim, from the published abstract:

> "Generalized additive (Poisson) regression models were used with daily HF admissions/mortality as outcomes and **daily mean temperature, humidity, and wind speed** as predictors, while controlling for pollutant levels, time trend, season, day of the week, and holiday."

> "**Both high and low relative humidity were modestly associated with more admissions.**"

> "…cumulative (to 23 days) relative risk (RR) (95% CI) for HF admissions of **2.63 (2.43, 2.84)** for an 11 °C vs. a 25 °C day, and cumulative (42 days) RR (95% CI) = **3.13 (1.90, 5.16)** for HF mortality."

**What this licenses.** Citing `[21]` for relative humidity as a meteorological predictor of daily HF admissions in Hong Kong. Citing the 2.63 cumulative RR as the historical daily HF cold association (already used in the Introduction and Discussion).

**What it does not license.**

- Citing `[21]` for rainfall. The paper has no rainfall term. This is the specific error Hogan's own email invited.
- Describing the humidity finding as if it were monotone. It is a **both-tails, modest** association. Our Model 2 enters a **linear monthly mean** relative-humidity term, which cannot represent a both-tails relation, so `[21]` motivates including humidity but our specification does not test what they found.
- Comparing 2.63 with the monthly count ratio 1.073 per five official cold days. Different estimand.

---

## `[22]` Chan, Goggins, Yue and Lee 2013 — the rainfall precedent

Chan EYY, Goggins WB, Yue JSK, Lee P. *Hospital admissions as a function of temperature, other weather phenomena and pollution levels in an urban setting in China.* Bull World Health Organ. 2013;91(8):576–584. `doi:10.2471/BLT.12.113035`

Verbatim, from the archived full text:

> "Meteorological variables, including mean daily temperature (MDT), mean daily relative humidity (MDRH), mean daily wind speed (MDWS), daily total global solar radiation (DTGSR) and **total daily rainfall (TDR)**, were obtained from the Hong Kong SAR Observatory."

> "**Same-day rainfall (square-root-transformed) was also included in all models based on the hypothesis that heavy rain would deter people from going to hospital.**"

Setting: Hong Kong Hospital Authority admissions, 1 January 1998 – 31 December 2009, 7,869,661 admissions, public hospitals covering 83% of all admissions. Circulatory disease was 15.1% of admissions and rose only during cold.

**What this licenses.** Citing `[22]` for the *hypothesis under which rainfall is entered* — that heavy rain may deter hospital attendance. This is a near-verbatim paraphrase of the authors' own stated rationale, in the same city, the same data source family, and the same outcome type as our series. It is the correct rainfall citation and it is not an overclaim.

**What it does not license.**

- Any claim that `[22]` found a rainfall effect on cardiovascular admissions. Rainfall was a **control term**, not a reported finding. Write "included … on the hypothesis that", never "was associated with".
- Calling rainfall a "predictor" in the sense of a variable of interest. Say "entered in" or "included in".
- Treating their rainfall term as equivalent to ours. Theirs is **same-day, square-root-transformed, daily**; ours is a **monthly total in millimetres**. A monthly total cannot represent same-day attendance deterrence. State this mismatch in Methods.

---

## Agreed Methods wording

> Model 2 adds monthly mean relative humidity and monthly total rainfall to Model 1. Goggins and Chan entered daily mean temperature, humidity, and wind speed as predictors of daily heart-failure admissions and deaths in Hong Kong, and reported that both high and low relative humidity were modestly associated with more admissions [21]. Chan et al. included same-day rainfall in Hong Kong hospital-admission models on the hypothesis that heavy rain deters people from going to hospital [22]. Both papers fitted daily values, so a monthly mean and a monthly total are coarser than the terms they used. Table 2 reports Model 1.

Listing what `[21]` actually entered makes the absence of rainfall self-evident without a body sentence that reads as a correction of the supervisor. The explicit correction belongs in a live-file comment:

> Rainfall precedent: Goggins and Chan 2017 [21] entered temperature, humidity, and wind speed, not rainfall. The rainfall-as-attendance-deterrent hypothesis is Chan et al. 2013, *Bull World Health Organ* 91:576–584, doi:10.2471/BLT.12.113035, where same-day square-root-transformed rainfall was a control term.

---

## Standing prohibition

Model 2 has **not** been fitted. No relative-humidity or rainfall coefficient for CHD or HF exists in this repository, and none may be typed by hand. Table 2 remains Model 1 until the governed refit runs on the machine holding the CHD/HF panel. Present tense ("Model 2 adds") is required wherever Model 2 or Model 3 health fits are described, so that specification is never read as result.

Cross-references: `literature/final_methods_evidence_map.md`, `literature/goggins_comparison_table.md`, `manuscript/live_collaborative/opus5_verdict_pr69_vs_pr70.md` §2.2–2.3.
