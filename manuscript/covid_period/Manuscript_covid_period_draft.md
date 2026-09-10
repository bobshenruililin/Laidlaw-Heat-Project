# Window dependence of first CHD and HF hospitalisation counts in Hong Kong, 2013–2023

**Status:** skeleton. SYNTHETIC lab output is not cited. Gate 3 is open. Do not paste into Hogan’s Word until Bob sends.

**Candidate thesis.** In this monthly first-event panel, count ratios that look like cold-day harm are stronger before 2020 than in the full 2013–2023 window. Official thermal extremes are a ruling-out exhibit: they are not a sufficient account of that window dependence. Falling first-event totals are compatible with depletion of a closed diagnosis window and with pandemic care-seeking. They are not a measure of physiological improvement.

## Abstract (placeholder)

Do not freeze. Report the existing Newey–West lag-6 window panel. CHD hot nights / 5 days: 1.022 (1.002–1.042) over 132 months, *q* = 0.192; pre-2020 1.011 (0.991–1.032) includes 1. HF cold days / 5 days: 1.073 (1.006–1.144); pre-2020 1.113 (1.053–1.176). All twelve Model 1 *q*-values exceed 0.19. First-event counts halved from 2013 to 2023. Do not call this health improvement.

## Introduction

Hogan asked that the paper’s angle be the pre- versus post-COVID contrast, and that thermal extremes be used to say weather is not the reason the period difference appears. The extract remains an ecological monthly first-hospitalisation series among people with T2D and/or HTN. Admission cause is absent.

Neighbour literature on Hong Kong in 2020 reports **fewer** public hospitalisations and **more** deaths, including cardiovascular deaths (Xin et al. 2022). That is the opposite of a physiological-improvement story. Cite as context. Do not import their counts into Table 2.

## Methods

Separate negative-binomial models of monthly first-event counts \(Y_t\):

\[
\log \mathrm{E}(Y_t)=\log d_t + \alpha + \beta X_t + \sum_{m=2}^{12}\gamma_m I(\mathrm{month}_t=m)+s(t;4).
\]

\(d_t\) is days in the month. \(X_t\) is a same-month thermal series. Official-day models use \(I(\mathrm{count}/5)\) as a reporting scale.

**Weather paragraph (verbatim; do not rewrite):**

Meteorological data was obtained from the HKO. The monthly variables included: temperature (mean, minimum, maximum), relative humidity, total rainfall, the number of hot nights (T~min~ ≥ 28°C), the number of very hot days (T~max~ ≥ 33°C), the number of extremely hot days (T~max~ ≥ 35°C), and the number of cold days (T~min~ ≤ 12°C). Monthly mean pollutant levels for nitrogen dioxide (NO~2~), sulfur dioxide (SO~2~), and ozone (O~3~) were obtained from the Hong Kong Environmental Protection Department (EPD). All monthly data were derived by taking the average of daily data in each calendar month.

Pre-2020 is January 2013–December 2019 (84 months). COVID-phase indicators on the full sample are a labelled specification, not a post-only primary. Uncertainty: model-based, HC1, Newey–West lag-3, Newey–West lag-6. Do not pick an SE because its interval excludes 1.

## Results (from existing tables only)

Source: `outputs/tables/cvd_trend_depletion_sensitivity.csv` and live Table 1.

- CHD 156,156 first events; HF 29,681.
- Annual first-event totals about halved (CHD 23,830 to 12,323; HF 4,336 to 2,296) with a 2020 dip (CHD 10,237; HF 1,964). C&SD 35+ rose ~17%.
- HF cold days / 5 days stronger pre-2020 (1.113, 1.053–1.176) than full sample (1.073, 1.006–1.144).
- CHD cold days / 5 days exclude 1 only pre-2020 (1.036, 1.007–1.067).
- CHD hot nights / 5 days compatible with 1 pre-2020; full-sample 1.022 needs 2020–2023.

Figure 3 of the parked thermal paper is the candidate **main** figure of this track.

## Discussion

Do not say cold days improved hearts. Say the **cold-day count ratio is window-dependent**. Rival accounts that do not require labs: first-event depletion; care-seeking (Xin 2022; Hung et al. 2022); influenza coverage 121/132 months; NO2/PM2.5 decline already in the parked Introduction. Thermal extremes changed over the window (official hot nights rose); they cannot be ignored, but they do not identify a physiological COVID recovery.

Labs were not in the transfer. Person-time was not delivered. Gate 3 remains a human decision.

## Limitations

Same as the parked paper, plus: no post-only 48-month Model 1; no lab metadata; Hogan’s “improved” is not an estimand until he confirms the object (counts vs ratios).
