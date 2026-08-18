# Evidence and citation ledger — 15 August 2026 independent verification

Base inventory: [`../claim_ledger.md`](../claim_ledger.md). This file records **re-verification**, not a second set of numbers. Status: `verified` (primary source or project CSV this session) · `retained Hogan bibliography` · `do not cite as this study`.

## Project numbers (HA_APPROVED_AGGREGATE or REAL)

| Claim | Display | Source this session | Status |
|---|---|---|---|
| Table 2 twelve NW6 ratios, *p*, *q* | as in live Table 2 | `outputs/release_chd_hf/tables/table2_core_models.csv`; all 12 display strings match | verified |
| Min core *q* | 0.192 | `q_value_core_bh` minimum 0.192239 | verified |
| Table 3 ladder | CHD HN Model 1.022 (0.995–1.049); HC1 (0.997–1.047); NW3 (1.0003–1.0439 unrounded 1.000253–1.043860); NW6 (1.002–1.042). HF CD all four exclude 1 | `table4_uncertainty_ladder.csv` | verified |
| Trend range CHD HN / HF CD | 1.011–1.025 / 1.043–1.113 | `table3_robustness_summary.csv` mins/maxes rounded | verified |
| Events | CHD 156,156 (mean 1,183.0); HF 29,681 (224.9) | `table1_outcome_summary.csv`; 156156/132 = 1183.0 | verified |
| Annual 2013→2023 / 2020 trough | CHD 23,830→12,323 (10,237); HF 4,336→2,296 (1,964) | `cvd_descriptive_annual_totals.csv` | verified |
| C&SD 35+ rise | 17% (5,188,660 / 4,430,186) | same file `mean_population` CHD 2013 vs 2023 = 0.1712 | verified |
| Cold days DJF | 141 of 145 (Dec 40, Jan 54, Feb 47; Mar 4) | `temperature_monthly_panel_2013_2023.csv` | verified |
| July 2013 / July 2022 hot nights | 1 / 25; Jun–Sep every month ≥1 in 11/11 years | `hot_nights_by_month_year.csv` | verified |
| HKO annual HN/VHD/CD | 2013 10/17/14; 2021 61/54/13; 2023 56/54/14 | `hko_annual_extremes_validation.csv` 33/33 MATCH; HKO Year’s Weather 2013 primary page | verified |
| 2013 HN vs 1981–2010 normal | “about seven days below” | HKO Year’s Weather 2013: “only ten Hot Nights … about seven days below normal”; table normal 17.8 | verified |
| EPD 2013→2023 general stations | NO₂ 53.7→32.1; PM2.5 30.8→14.6; O₃ 42.6→58.3 | project CSV 53.72, 32.08, 30.83, 14.56, 42.61, 58.31. GIA annex integers 54→32, 31→15, 43→58 (direction only) | verified for 2013–2023; **not** a 2000–2009 reconstruction |
| ERA5 monthly Tmin / HN counts | r = 0.986, slope 1.032; HN slope 0.045 (SE 0.007); 57 vs 9 months | `monthly_station_grid_bridge.json` 0.9861, 1.0324, 0.0453, 0.0074 | verified |
| Archive flu CHD | 1.673 (1.249–2.243), n = 121 | `combined_pathway_panel_estimates.csv` P14; offset **`population_x_days`**, not days-only | verified; live Discussion now states the offset |
| Medication | not measured | variable dictionary + release outputs | verified absent |

**Not re-fitted.** Analysis panels absent. Coefficients above are from already-written release tables.

## Literature (sentence-level)

| Live sentence / number | Primary check 15 Aug | Status |
|---|---|---|
| Goggins et al. 2013: 1 °C below ~24 °C → 3.7% AMI HK, lags 0–13; no significant heat in HK/Taipei/Kaohsiung; same-day NO₂ strongest pollutant | ORA/IJC abstract: 3.7% (avg lag 0–13) HK; 2.6% Taipei; 4.0% Kaohsiung; “No significant heat effects were observed.” Author Chun-Yuh Yang → `Yang CY` | verified |
| Goggins 2012 stroke: inverse HS vs temperature; weaker IS below ~22 °C | ORA abstract: HS 2.7% per 1 °C lower lags 0–4; IS 1.6% per 1 °C below 22 °C lags 0–13. Live file does not quote those percentages (history only) | verified direction |
| Goggins and Chan 2017 HF: cum RR 2.63 (2.43–2.84) for 11 °C vs 25 °C, lags to 23 d, 2002–2011 | IJC abstract | verified |
| Guo et al. 2024: official HNday28 excess RR −0.2% (−1.2 to 0.7) lag 0–4 after mean-T adjustment; extreme HNe +3.1% (1.5–4.8) | Primary PDF Table 3 (ORA file): All −0.2 (−1.2, 0.7) vs HNe 3.1 (1.5, 4.8). Study is hot-season NCNE hospitalisation, not first CHD/HF | verified |
| Liu et al. 2020: cold AF 4.72% vs heat 0.16%; moderate 4.25% vs extreme 0.63% | ClimaHealth record of SCS 2020 abstract; DOI 10.1016/j.scs.2020.102131 exists | verified at abstract level (full PDF still not in repo) |
| Liu et al. 2026: 1,455–3,238 excess heat deaths 2014–2023 | medRxiv 10.64898/2026.03.05.26347683 v1 abstract | verified as complementary mortality, not our ratios |
| Ye 2012; Bhaskaran 2013 | Standard reviews; used as mechanism/methods citations, not as measured covariates | retained |
| Greenland & Morgenstern 1989; Basagaña–Ballester 2024/2026; Newey–West 1987; BH 1995 | Method citations; no new coefficients attached | retained |
| Yang Z et al. 2025 flu/stroke | Motivates influenza as a covariate class; **not** a stroke result of this study | retained as motivation only |

## Hogan bibliography 1–8

Refs 1, 2, 4, 6, 7, 8 are attached to live sentences (C&SD split as [8], repairing the skeleton’s “[8]” glued onto [7]).

Refs **3** (Year’s Weather 2017) and **5** (Year’s Weather 2024) are **retained Hogan bibliography**. They are not currently attached to a body sentence. Do not attach 2024 as a health year (after the 132-month window). Optional climate-only sentence lives in `optional_2024_climate_sentence.md` if Hogan asks.

## Explicit non-claims (do not promote)

Stroke coefficients; AMI as this study’s endpoint; cohort incidence; daily DLNM; Gate 3 freeze; CNS-journal *acceptance*; housing/behaviour/medication as controlled factors; 0.045 as health attenuation; daily Jaccard 0.031; 449 vs 17 nights; identifying-share percentages in the live body; HM/CM confirmatory estimates.
