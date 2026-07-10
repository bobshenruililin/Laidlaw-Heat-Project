# First-Stage Progress Report: Temperature and Cardiovascular Admissions in Hong Kong

**Prepared by:** Bob Shen  
**Supervisor:** Professor David Bishai  
**Collaborators:** Hogan (environment), Roro (HA data access)  
**Date:** 10 July 2026  
**Repository / PR:** https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/1  

> **Central message:** The environmental and coding infrastructure is substantially prepared, but the cardiovascular models have so far been tested only on synthetic outcomes. The next scientific milestone is to finalize outcome definitions and securely obtain the real HA data, C&SD denominators, and EPD pollution files.

---

# Executive Summary

I completed a first-stage reproducible pipeline for a planned ecological time-series study of thermal extremes and cardiovascular hospital admissions among Hong Kong residents aged 35+ from 2013–2023. Real HKO daily climate data were transformed into monthly extreme-day counts using official definitions. A synthetic HA-like panel was used only to test offsets, models, diagnostics, and reporting. Population denominators and pollution series are not yet real. **No real association between temperature and cardiovascular admissions has been estimated.**

Recommended framing for the project remains:

> Thermal extremes and cardiovascular hospital burden in an aging Hong Kong.

---

# 1. What I Did

## 1.1 Project setup and reproducibility

I organized the repository into raw data, processed data, scripts, outputs, memos, reports, and manuscript folders; added `config.yml` for study dates and thresholds; and wrote scripts `00`–`13` plus `run_pipeline.R`. Real, placeholder, and synthetic files are labeled in-file (`data_status` or equivalent). Session information and a pipeline status file were recorded after execution.

## 1.2 HKO climate-data processing

I downloaded HKO Headquarters daily extracts for 2012–2024 and built:

- `data_processed/climate_monthly_2013_2023.csv` (132 months)
- `data_processed/climate_monthly_2013_2024.csv` (optional extension)

Official definitions implemented:

| Metric | Definition |
|---|---|
| Hot night | Daily minimum temperature ≥ 28°C |
| Very hot day | Daily maximum temperature ≥ 33°C |
| Extremely hot day | Daily maximum temperature ≥ 35°C |
| Cold day | Daily minimum temperature ≤ 12°C |

I also constructed spell-length metrics and monthly means for temperature, relative humidity, rainfall, and dew point. Completeness was checked; for 2013–2023, daily completeness was 100% in the processed Headquarters series.

## 1.3 Synthetic HA-like outcome construction

Because HA data are not available, I simulated a monthly panel of AMI, ischemic stroke, and hemorrhagic stroke counts by age and sex, labeled `data_status = "SYNTHETIC"`. This panel exists only to test the analysis workflow.

## 1.4 Statistical workflow tested

On synthetic data only, I tested:

- Negative Binomial as default count model;
- Poisson comparison and overdispersion assessment;
- offsets of the form `log(population × days_in_month)`;
- month fixed effects, smooth time trend, and COVID-phase indicators;
- primary heat model (hot nights + cold days) and alternative heat model (very hot days + cold days);
- continuous mean daily minimum temperature model;
- age and diagnosis interaction templates;
- staged ozone interaction template;
- residual ACF/PACF and related diagnostics;
- automatic table/figure export.

## 1.5 Draft research documents prepared

- Assumption ledger
- HA data-request memo for Roro
- Environmental data-request memo for Hogan
- Literature baseline memo
- First-stage exploratory report
- Draft Methods section
- This progress package for Professor Bishai

---

# 2. What We Can Learn So Far

## 2.1 Verified public-data observations

These are **Category A** descriptive findings from the processed HKO Headquarters series.

| Year | Hot nights | Very hot days | Extremely hot days | Cold days |
|---:|---:|---:|---:|---:|
| 2013 | 10 | 17 | 0 | 14 |
| 2014 | 34 | 33 | 0 | 21 |
| 2015 | 37 | 28 | 1 | 7 |
| 2016 | 36 | 38 | 6 | 21 |
| 2017 | 41 | 29 | 1 | 9 |
| 2018 | 26 | 36 | 5 | 21 |
| 2019 | 46 | 33 | 2 | 1 |
| 2020 | 50 | 47 | 3 | 11 |
| 2021 | 61 | 54 | 4 | 13 |
| 2022 | 52 | 52 | 15 | 13 |
| 2023 | 56 | 54 | 4 | 14 |

Summary comparisons:

- **2013–2018 averages:** ~30.7 hot nights, ~30.2 very hot days, ~15.5 cold days per year.
- **2019–2023 averages:** ~53.0 hot nights, ~48.0 very hot days, ~10.4 cold days per year.
- Peak hot-night year in the core window: **2021 (61)**.
- Peak extremely hot-day year: **2022 (15)**.
- Cold days are **variable**, not steadily disappearing.
- Monthly hot nights and very hot days are strongly correlated (**r ≈ 0.88**).

Optional 2024 extract (descriptive only; not required for core analysis): 50 hot nights, 52 very hot days, 2 extremely hot days, 11 cold days.

These observations support including hot nights as a primary heat metric. They do **not** demonstrate a change in cardiovascular risk.

## 2.2 Lessons from synthetic pipeline testing

These are **Category B** workflow findings only:

- The end-to-end pipeline runs and writes labeled outputs.
- The synthetic panel has 8,712 unique month × age × sex × diagnosis rows and no duplicate keys.
- Poisson overdispersion is severe in the synthetic example (Pearson dispersion ≈ 57), supporting Negative Binomial as the default family for testing.
- Negative Binomial models converged in the synthetic run.
- The synthetic data-generating process planted a stronger cold than heat signal; the fitted synthetic models recovered that qualitative pattern. This shows the workflow can detect a planted signal; it is **not** evidence about Hong Kong admissions.
- Diagnostics (ACF/PACF of monthly mean residuals) are generated and remind us that serial correlation must be checked on real data.
- Highly collinear heat metrics should not enter one default model together.

## 2.3 What cannot yet be concluded

- No real HA heat–AMI or heat–stroke association has been estimated.
- No real cold-burden comparison with historical Goggins-era findings has been quantified.
- No pollutant-adjusted result exists while EPD data remain placeholders.
- No population-adjusted admission rates exist while denominators remain synthetic.
- No “regime shift” from cold-dominant to heat-dominant risk has been demonstrated.
- Causal claims are not appropriate for this ecological design even after real data arrive.

---

# 3. Code Walkthrough in Plain Language

## 3.1 Inputs

- **Real:** HKO daily climate extracts and open-data temperature CSVs.
- **Placeholder:** EPD pollution monthly series until Hogan deposits EPIC files.
- **Synthetic:** C&SD-like population scaffold and HA-like outcomes.
- **Provisional:** COVID phases, holiday scaffold, flu slot.

## 3.2 Data construction

Daily HKO observations are classified using official thresholds, aggregated to months, and enriched with spell metrics. Population and pollution scripts are ready to import real CSVs when available. Synthetic outcomes are merged with exposures and confounders into an analysis panel with an offset of `log(population × days_in_month)`.

## 3.3 Quality checks

Checks include unique keys, full month coverage for 2013–2023, non-missing population in the current scaffold, extreme counts within 0–days_in_month, and refusal to run synthetic modeling scripts unless `data_status = "SYNTHETIC"`.

## 3.4 Models

Planned primary model (to be applied to real HA data later): Negative Binomial of event counts on hot nights (per 5) and cold days (per 5), with age, sex, diagnosis, month effects, time trend, COVID phases, and the population-time offset. Alternative models replace hot nights with very hot days or use continuous temperature. Interactions and pollution staging are templates, not yet substantive analyses.

## 3.5 Diagnostics

Overdispersion, convergence, residual-versus-fitted plots, monthly residual time series, and ACF/PACF are produced for the synthetic run. On real data, clustered standard errors and possibly GEE/GLARMA will be considered if residual dependence persists.

## 3.6 Outputs

Tables, figures, model objects, table shells, and report-support files are written under `outputs/`. Weather figures based on real HKO data are available; pollution and population figures currently reflect placeholder/synthetic inputs and must be refreshed after real deposits.

---

# 4. Data and Decisions Still Needed

| Workstream | Status | What exists | What is still needed | Owner |
|---|---|---|---|---|
| HKO climate exposures | Complete for first stage | Monthly extremes 2013–2023 (+2024 file) | Confirm Headquarters vs multi-station strategy | Hogan / Bishai |
| EPD pollution | Blocked / placeholder | Import scripts + placeholder series | Real general-station EPIC files; station metadata | Hogan |
| C&SD denominators | In progress (scaffold) | Import script + synthetic denominators | Real age-sex mid-year file (Table 110-01002 or equivalent) | Bob |
| HA outcomes | Blocked | Request memo + synthetic panel | Aggregate extract + coding/episode/ED rules | Roro |
| COVID / flu / holidays | In progress | COVID phases in config; holiday scaffold | Confirm phases; load CHP flu; finalize holiday calendar | Bishai / Bob |
| Pre-analysis plan freeze | Awaiting decision | Assumption ledger + Methods draft | Team approval of defaults before HA modeling | Bishai |
| Secure transfer rules | Awaiting decision | Governance questions drafted | Roro confirmation of allowed channels and vetting | Roro |

---

# 5. Scientific Risks and How I Propose to Address Them

1. **Monthly aggregation may blunt short-lag heat effects.** Use extreme-day and spell metrics; interpret null heat findings cautiously; consider future daily analysis if data allow.
2. **Only 132 independent exposure months.** Do not treat thousands of stratum-rows as independent climate observations; use variance methods that respect shared monthly exposure.
3. **Outcome-definition uncertainty.** Freeze coding, principal diagnosis, episode, and ED rules with Roro before modeling.
4. **Heat-metric collinearity and single-station exposure.** Keep hot nights and very hot days in separate models; review multi-station sensitivity with Hogan.
5. **COVID disruption and ozone pathway ambiguity.** Pre-specify COVID sensitivities; stage pollution models; report total thermal associations separately from pathway-adjusted models.
6. **Historical comparison.** Keep comparisons with earlier Goggins studies qualitative unless estimands are harmonized.

---

# 6. Proposed Next Analysis Stage

1. Confirm decisions on the one-page sheet.
2. Obtain real C&SD and EPD files; re-run descriptive public-data sections.
3. Obtain HA aggregate extract through the approved secure process.
4. Freeze the pre-analysis plan (primary model, sensitivities, interaction priority).
5. Run real-data descriptive admission summaries, then primary models, then pre-specified sensitivities.
6. Only then interpret contemporary cold vs heat patterns relative to historical Hong Kong evidence.

---

# 7. Questions for the Team

1. Do you approve 2013–2023 as the core window, with 2024 optional?
2. Is emergency/unplanned inpatient principal-diagnosis the correct primary outcome?
3. Can HA separate 65–69 and 70–74?
4. Should influenza enter the primary model or only sensitivity analyses?
5. Is HKO Headquarters acceptable as the primary exposure series?
6. Should district analysis remain out of scope for the first paper?
7. What secure transfer and output-vetting rules apply to HA materials?

---

# 8. Recommended Meeting and Agenda

Please see `communications/proposed_meeting_agenda.md` for a 30–45 minute meeting proposal with Professor Bishai, Hogan, Roro, and Bob.

---

# 9. Immediate Action Items

| Person | Action | Timing |
|---|---|---|
| Bob | Send this package + email draft to Professor Bishai; download real C&SD population file | This week |
| Bob | Do **not** email HA data; wait for Roro’s governance guidance | Ongoing |
| Roro | Confirm HA extract feasibility, coding, age bands, ED/inpatient rules, suppression, transfer route | Before modeling |
| Hogan | Deposit/review EPD general-station files; review HKO station and spell construction | Before modeling |
| Professor Bishai | Advise on study window, primary outcome, flu/COVID defaults, and meeting time | Next meeting |

---

## Internal audit snapshot

| Item | Claimed status | Verified status | Evidence/file | Issue or action |
|---|---|---|---|---|
| Scripts 00–13 + runner | Built | Verified present | `scripts/` | Keep as first-stage code |
| HKO monthly extremes | Real, processed | Verified 132 months | `climate_monthly_2013_2023.csv` | Confirm station choice |
| Annual extreme counts | Match HKO summaries | Verified in processed annual table | `weather_annual_extremes_2013_2023.csv` | OK for descriptive reporting |
| Pollution | Placeholder | Verified `PLACEHOLDER_NOT_FOR_INFERENCE` | `pollution_monthly_2013_2023.csv` | Replace with EPIC |
| Population | Synthetic scaffold | Verified `SYNTHETIC_DENOMINATOR` | `population_monthly_age_sex_2013_2023.csv` | Replace with C&SD |
| HA outcomes | Synthetic only | Verified `SYNTHETIC` | `synthetic_analysis_panel.csv` | Await HA extract |
| Synthetic models | Workflow only | Verified labeled SYNTHETIC | `synthetic_model_results.csv` | Do not cite as findings |
| Pipeline execution | Completed | Status file present | `outputs/pipeline_status.txt` | Re-run after real deposits |
| Literature / Methods drafts | Prepared | Present | `memos/`, `manuscript/` | Verify remaining provisional citations |
| HA secure data in repo | None | Verified placeholder only | `data_raw/ha_secure_placeholder/` | Keep empty of real HA data |
