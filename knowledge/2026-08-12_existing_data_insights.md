# Existing-data insights — 12 August 2026

**Mode:** Explore (no new models)  
**Rule:** Every number below already exists in `outputs/tables/` or the validated release. None is a Gate 3 freeze. Stroke remains undelivered.

Sol’s caution was right about **claim language**. It was too tight about **reading tables we already paid for**. This note is that reading.

## 1. The outcome is a depleting first-event pool, not a stable incidence series

Annual first-hospitalisation totals (`cvd_descriptive_annual_totals.csv`):

| Year | CHD | HF |
|---|---:|---:|
| 2013 | 23,830 | 4,336 |
| 2019 | 12,396 | 2,344 |
| 2020 | 10,237 | 1,964 |
| 2023 | 12,323 | 2,296 |

Both series fall by about half from 2013 to 2023. That is the expected shape of “first hospitalisation after first diagnosis” in a closed-ish 2013–2023 diagnosis window: people leave the risk set after the first event. `ns(time, 4)` absorbs most of this. Thermal coefficients are **residuals after depletion and season**, not crude winter peaks.

**Why it matters tonight:** Bishai’s July Table-1 instinct assumed a stable at-risk population. We do not have that. Asking Roro for monthly still-at-risk person-time is the single largest estimand upgrade that remains possible on monthly data.

## 2. Heat rose; cold did not vanish

HKO Headquarters annual extremes (`weather_annual_extremes_2013_2023.csv`):

- Hot nights: **10 in 2013 → 61 in 2021 → 56 in 2023**.
- Very hot days: **17 → 54**.
- Extremely hot days: **0 in 2013–14 → 15 in 2022**.
- Cold days: **14 in 2013, 1 in 2019, 14 in 2023**. 2019 was the anomaly, not the new climate.

This is the exposure-only version of Bishai’s Jasmine prompt (cold still matters) and Hogan’s coexistence framing. It does not require health coefficients.

## 3. Crude seasonality is strong; the model asks a harder question

Mean monthly events (`cvd_descriptive_seasonality_by_month.csv`):

- HF: January **287** vs September **196**.
- CHD: January **1,386** vs September **1,097**.

Crude Pearson correlations with mean temperature (`cvd_descriptive_temp_correlations.csv`): HF **r = −0.40**; CHD **r = −0.20**. After calendar-month indicators, those winter peaks are largely removed. Remaining thermal estimates ask whether a **January with more cold days** (or a **July with more hot nights**) differs from a typical January/July. That is a weaker, more honest question than “is winter bad for HF?”

## 4. HF cold is the more coherent residual pattern; CHD hot nights are SE-fragile

Amended core, days offset, NW6 (`table2_core_models.csv` / `table4_uncertainty_ladder.csv`):

- HF cold days / 5: **1.073 (1.006–1.144)**; Model/HC1/NW3/NW6 all exclude 1; q = 0.192.
- CHD hot nights / 5: **1.022**; NW3/NW6 exclude 1; **Model and HC1 include 1**.
- All twelve core BH q-values **> 0.19**.

HF residual ACF(1) ≈ **0.15** (Ljung–Box compatible with white noise). CHD ACF(1) ≈ **0.51** (Ljung–Box rejects). CHD serial correlation is why the SE ladder matters and why CHD must not be sold as a protected discovery.

## 5. Lag-1 HF is stronger than lag-0 — and still not a daily lag

From `cvd_lag_sensitivity.csv` (already run):

| Contrast | Lag 0 | Lag 1 |
|---|---|---|
| HF mean Tmin | 0.973 (0.947–1.000), p = 0.050 | **0.970 (0.950–0.990), p = 0.003** |
| HF mean temp | 0.974 (0.947–1.002), p = 0.069 | **0.973 (0.953–0.992), p = 0.006** |
| HF cold days / 5 | 1.073 (1.006–1.144), p = 0.031 | **1.073 (1.014–1.135), p = 0.014** |
| CHD hot nights / 5 | 1.022 (1.002–1.042), p = 0.032 | 1.010 (0.979–1.042), p = 0.53 |

Roro already wrote that a previous-month exposure is not biologically compelling for a 5–21-day heat window. Keep lag-1 as a **labelled monthly sensitivity**. It is consistent with delayed HF decompensation, leftover winter clustering, or incomplete seasonal control. Monthly data cannot tell those apart. Do not call it harvesting or a DLNM.

## 6. The influential months are pandemic shocks, not thermal extremes

Cook’s-distance leaders (`chd_pathway_influence_top10.csv`, `hf_pathway_influence_top10.csv`): **2020-02** and **2022-02** dominate both outcomes.

Excluding the worst month (`cvd_influence_sensitivity.csv`):

- HF cold days: **1.088 (1.034–1.144), p = 0.001** after dropping 2022-02.
- CHD hot nights: **1.021 (1.001–1.040), p = 0.035** after dropping 2020-02.

The thermal directions survive the months that most distort care-seeking. That is useful robustness. It is not multiplicity-protected confirmation.

## 7. Hogan’s monthly-tail family agrees on cold–HF; Li-HW `HM23` is currently null

Provisional HM/CM panel (`hf_hm_cm_panel_estimates.csv`, `chd_hm_cm_panel_estimates.csv`; **not Hogan-locked**):

- HF `CM08` (7 coldest months): **1.173 (1.049–1.312), p = 0.005**.
- HF `CM03`: **1.122 (1.023–1.230), p = 0.014**.
- CHD `HM19`: 1.044 (0.998–1.091), p = 0.061.
- `HM23` (Li daily events → Hogan monthly tail, lock pending): null for CHD and HF.
- `CM05` (`Tmin ≤ 10°C`): **zero months flagged** under the monthly-mean proxy. The ~10°C discussion prompt is not currently an executable monthly exposure.

Use this with Hogan as **definition-family coherence**, not as a new headline. Reference period and month-assignment still belong to him.

## 8. Offset choice barely moves the coefficients; it does move the sentence

`cvd_offset_sensitivity_wide.csv`: days-only vs population×days vs no offset leaves CHD hot nights at **1.022 / 1.021 / 1.022** and HF cold days at **1.073 / 1.073 / 1.075**.

C&SD age 35+ is the wrong risk set for a T2D/HTN first-event cohort, but it is empirically inert for these two contrasts. Cohort person-time would mainly **change what we are allowed to call the number** (incidence vs count ratio), unless the cohort’s seasonal risk-set differs from calendar days.

## 9. Strong co-predictors exist; they are not thermal findings

From the original (not amended-core) pathway table `combined_pathway_panel_estimates.csv`:

- Flu indicator with CHD: **1.67 (1.25–2.24)** on 121 months (P14). Winter infection is a real competing explanation for cold-month counts.
- NO₂ in staged P11 is a strong positive co-predictor of CHD counts; ozone is not. Do not promote P11 as a continuity-adjusted thermal estimate (different offset/joint structure). Do use it to justify **staged pollution language** in Methods.
- COVID phase indicators (P10) show large count drops in the fifth wave and late 2022. That matches the influence diagnostics.

Pollution annual means (`pollution_annual_means_general_2013_2023.csv`): NO₂ **53.7 → 32.1** µg/m³; PM2.5 **30.8 → 14.6**; ozone **42.6 → 58.3**. Clean Air Plan success plus rising ozone is the Hong Kong confounder story. It does not require a new model tonight.

## 10. What this does *not* license

- A confirmatory primary contrast.
- Disease-caused admission claims.
- Daily triggering, harvesting, or attributable fractions.
- Waiting to invent a stroke result.
- Rewriting Hogan’s weather Methods from `HM23` nulls.

## Build-better note (automation)

The unused value was not “run more models.” It was **a scheduled read of tables the pipeline already writes**. Future sessions should produce this kind of note after every full run, before anyone asks for new pathways.
