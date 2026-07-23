# Hot-month and cold-month definition catalogue

**Purpose:** Answer Dr Bishai's next-week request to spin out many defensible ways to identify hot and cold months for the Hong Kong monthly thermal exposure × stroke aggregate study, 2013–2023.

**Team roles:** Hogan leads weather and heat framing; Roro leads Hospital Authority stroke outcomes and event timing; Dr Bishai set the multi-method and Jasmine-extension questions.

**Status:** Definition catalogue only. No stroke association has been estimated or is claimed here. Synthetic runs, if used later, are plumbing checks rather than findings.

---

## 0. Scientific prompt and confirmed paper family

“Jasmine’s paper” is confirmed as Jingwen Liu et al. (2020), “Cause-specific mortality attributable to cold and hot ambient temperatures in Hong Kong: a time-series study, 2006–2016,” *Sustainable Cities and Society* 57:102131, DOI `10.1016/j.scs.2020.102131`.

Confirmed source facts motivate a symmetric panel: the study used a DLNM integrated with quasi-Poisson regression, found a reversed J-shaped association, and reported cold AF 4.72% versus heat AF 0.16%, with moderate-temperature AF 4.25% versus extreme-temperature AF 0.63%. Those are mortality AFs, not stroke coefficients.

Dr Bishai’s recollection that hotter-side tests were more often non-significant than colder-side tests remains a research prompt until the full Jasmine PDF/supplement identifies the relevant table and complete test universe.

### Related team baseline

Zhenyuan Liu, Chao Ren, Jingwen Liu, Kawasaki Yurika and David Bishai’s 2026 medRxiv v1 paper (DOI `10.64898/2026.03.05.26347683`) uses RRs from Jasmine and Wang/Ren to estimate 2014–2023 excess heat deaths under mean-temperature, maximum-temperature, minimum-temperature and combined day–night definitions. Its definitions should be represented through 2023 as a labelled team-baseline family, but its mortality RRs must not be used as stroke coefficients.

Use **definition-harmonised extension**, not replication, when daily mortality definitions are transported to monthly stroke aggregates. See `literature/jasmine_liu2020_confirmed.md`, `literature/roro_manuscript_deep_read.md` and `analysis_plan/jasmine_extension_protocol.md`.

---

## 1. Common notation and coding rules

### 1.1 Daily seeds

- `HN`: hot night, daily minimum temperature (`Tmin`) ≥ 28°C.
- `VHD`: very hot day, daily maximum temperature (`Tmax`) ≥ 33°C.
- `EHD`: extremely hot day, `Tmax` ≥ 35°C.
- `CD12`: cold day, `Tmin` ≤ 12°C.
- `CD10`: severe-cold sensitivity day, `Tmin` ≤ 10°C. The 10°C value is a Bishai discussion prompt, not an asserted biological threshold.
- `Li-HW`: the event rule in Li et al., *Atmospheric Research* 315 (2025) 107845: during May–September, `Tmax` exceeds its calendar-day 90th-percentile threshold for at least three consecutive days; the published construction uses a 15-day moving calendar window and joins events separated by no more than two days.

### 1.2 Reference periods and event assignment

Before outcomes are opened, freeze:

1. the threshold reference period;
2. whether percentiles use all months or a named season;
3. whether a percentile threshold is empirical, interpolated or tie-inclusive;
4. event treatment at month and year boundaries;
5. missing-day tolerance; and
6. whether a cross-month event is assigned by **touch**, **start month**, or fractional/event-day burden.

For the Jasmine extension, reproduce the source paper's original reference period first. A 2013–2023 recalibrated threshold may be reported only as a labelled sensitivity because it changes the definition.

### 1.3 Core dependencies

- HKO daily series with `date`, `Tmax`, `Tmin` and daily mean temperature where required.
- HKO monthly aggregates, or monthly values derived reproducibly from the daily series.
- At least December 2012 for lag/persistence coding at the January 2013 boundary.
- Optional compound layers: EPD pollution, absolute humidity/wind, CHP influenza and HKO warning history.

Nested definitions should generally be fitted in separate models. Every fitted definition must report exposed-month count, missingness and the months selected before any coefficient is interpreted.

---

## 2. Hot-month definitions

### 2.1 Absolute, percentile and multimetric definitions

| ID | Short name | Operational rule | Main dependency / note |
|---|---|---|---|
| HM01 | Any hot night | Monthly HN count ≥ 1 | HKO daily `Tmin` |
| HM02 | Frequent hot nights | Monthly HN count ≥ 5 | HKO daily `Tmin` |
| HM03 | Heavy hot nights | Monthly HN count ≥ 10 | HKO daily `Tmin` |
| HM04 | Any very hot day | Monthly VHD count ≥ 1 | HKO daily `Tmax` |
| HM05 | Frequent very hot days | Monthly VHD count ≥ 5 | HKO daily `Tmax` |
| HM06 | Any extremely hot day | Monthly EHD count ≥ 1 | HKO daily `Tmax` |
| HM07 | Repeated extremely hot days | Monthly EHD count ≥ 3 | May be sparse; inspect exposure count |
| HM08 | Upper-decile mean temperature | Monthly mean temperature ≥ p90 over the frozen monthly reference distribution | Existing P07-compatible measure |
| HM09 | Upper-5% mean temperature | Monthly mean temperature ≥ p95 | Fit separately from HM08 |
| HM10 | Upper-2.5% mean temperature | Monthly mean temperature ≥ p97.5 | Tail sensitivity |
| HM11 | Upper-decile mean Tmax | Monthly mean of daily `Tmax` ≥ p90 | Daytime-relative |
| HM12 | Upper-decile mean Tmin | Monthly mean of daily `Tmin` ≥ p90 | Nighttime-relative |
| HM13 | Multimetric hot month | At least two of monthly mean temperature, mean `Tmax`, and mean `Tmin` are at or above their p90 thresholds | Composite; do not co-fit components |

### 2.2 Spell and combined day–night definitions

| ID | Short name | Operational rule | Main dependency / note |
|---|---|---|---|
| HM14 | Two-day VHD spell touch | Month contains any day in a run of ≥2 consecutive VHDs | Preserve runs across month boundaries |
| HM15 | Five-day VHD spell touch | Month contains any day in a run of ≥5 consecutive VHDs | Wang/Ren form |
| HM16 | Three-night HN spell touch | Month contains any day in a run of ≥3 consecutive HNs | Night persistence |
| HM17 | Five-night HN spell touch | Month contains any day in a run of ≥5 consecutive HNs | Wang/Ren form |
| HM18 | Exceptional hot-run month | Longest HN or VHD run touching the month ≥ p90 of warm-season monthly longest-run values | Relative spell tail |
| HM19 | Any 2D3N month | Month touches a Wang/Ren-style two-hot-day/three-hot-night window | Freeze exact overlap algorithm |
| HM20 | High 2D3N burden | At least five calendar days in the month belong to a 2D3N window | Also retain continuous burden |

### 2.3 Hogan / *Atmospheric Research* event-count family

This family credits Hogan's hot-month recipe. Li et al. supply the atmospheric heatwave event definition; **counting those events by month and flagging the upper tail is Hogan's project-level monthly adaptation**, not a claim about the health analysis in the atmospheric paper.

| ID | Short name | Operational rule | Main dependency / note |
|---|---|---|---|
| HM21 | Li-HW touch month | Month contains at least one Li-HW day | Published event form; DOI `10.1016/j.atmosres.2024.107845` |
| HM22 | Li-HW start month | At least one Li-HW event starts in the month | One assignment per event |
| HM23 | Hogan p90 event-count month | Monthly Li-HW start count ≥ p90 among May–September months in the frozen reference period | Core Hogan starter; discrete ties must be documented |
| HM24 | Hogan p95 event-count month | Monthly Li-HW start count ≥ p95 among May–September months | Tail sensitivity |
| HM25 | Multiple-event month | At least two Li-HW events start in the month | Absolute count alternative |
| HM26 | Upper-tail heatwave-day month | Monthly Li-HW day count ≥ p90 among May–September months | Burden rather than event starts |

### 2.4 Intensity, compound, anomaly and transition definitions

| ID | Short name | Operational rule | Main dependency / note |
|---|---|---|---|
| HM27 | Night heat-degree month | `Σ max(0, Tmin−28)` ≥ p75 among May–October months | Keep degree-days continuous too |
| HM28 | Day heat-degree month | `Σ max(0, Tmax−33)` ≥ p75 among May–October months | VHD intensity |
| HM29 | Extreme heat-degree month | `Σ max(0, Tmax−35)` ≥ p75 among months with any EHD | Conditional tail; declare denominator |
| HM30 | Li-HW cumulative-intensity month | Sum of `Tmax` excess above the moving p90 threshold on Li-HW days ≥ warm-season p90 | Intensity × duration |
| HM31 | Peak three-day heat | Maximum rolling three-day mean `Tmax` in month ≥ warm-season p90 | Windows may cross month boundaries |
| HM32 | Hot plus high ozone | HM08 and warm-season monthly O₃ ≥ p75 | Compound; include main effects |
| HM33 | Hot plus humid | HM12 and warm-season absolute humidity ≥ p75 | Compound; requires humidity |
| HM34 | Hottest quartile in warm season | Monthly mean temperature ≥ p75 among May–October months | Months outside season coded not applicable |
| HM35 | Calendar-month hot anomaly | Same-calendar-month temperature anomaly z-score ≥ 1 against a frozen external or pre-study climatology | Do not estimate climatology from 11 values if avoidable |
| HM36 | Fixed-baseline +1°C anomaly | Monthly mean temperature ≥ corresponding 2013–2019 calendar-month mean +1°C | Baseline sensitivity |
| HM37 | Calendar warm season | Month is May–October | Seasonal comparator, not an extreme definition |
| HM38 | Wang EHWE composite | Month touches a 5VHD, 5HN or 2D3N event | Published-definition extension candidate |
| HM39 | Daily-mean p90 spell | Daily mean temperature exceeds its calendar-day p90 for ≥3 consecutive days touching the month | Separate from Tmax-based Li-HW |
| HM40 | p90 × 2-day grid cell | Daily temperature exceeds frozen calendar-day p90 for ≥2 consecutive days touching month | Grid family |
| HM41 | p95 × 3-day grid cell | Daily temperature exceeds frozen calendar-day p95 for ≥3 consecutive days touching month | Grid family |
| HM42 | p97.5 × 4-day grid cell | Daily temperature exceeds frozen calendar-day p97.5 for ≥4 consecutive days touching month | Sparse-tail sensitivity |
| HM43 | Long-duration Li-HW month | Maximum duration of a Li-HW touching the month ≥ p90 of event durations | Event-level tail mapped to month |
| HM44 | High-intensity Li-HW month | Maximum mean threshold exceedance of a Li-HW touching the month ≥ p90 of event intensities | Event-level intensity |
| HM45 | High heatwave-day proportion | Li-HW days / days in month ≥ 0.10 | Length-standardised |
| HM46 | Persistent two-month heat | HM08 is true in both current and previous month | Requires December 2012 only if January can qualify |
| HM47 | Hot-period onset month | HM08 is true and was false in the previous month | Transition indicator |
| HM48 | Rapid warming month | Current minus previous monthly mean temperature ≥ p90 of positive month-to-month changes in the frozen reference period | Transition, not absolute heat |
| HM49 | Very Hot Weather Warning month | HKO Very Hot Weather Warning is active on at least one calendar day in the month | Public-health operational definition; requires warning history |
| HM50 | Sustained very-hot warning month | HKO Very Hot Weather Warning is active on ≥3 distinct calendar days in the month | Warning-duration sensitivity; not equivalent to realised temperature |

---

## 3. Cold-month definitions

### 3.1 Absolute, percentile and multimetric definitions

| ID | Short name | Operational rule | Main dependency / note |
|---|---|---|---|
| CM01 | Any cold day | Monthly CD12 count ≥ 1 | HKO daily `Tmin` |
| CM02 | Repeated cold days | Monthly CD12 count ≥ 3 | HKO daily `Tmin` |
| CM03 | Frequent cold days | Monthly CD12 count ≥ 5 | Core starter |
| CM04 | Heavy cold days | Monthly CD12 count ≥ 10 | May be sparse; inspect exposure count |
| CM05 | Any ≤10°C day | Monthly CD10 count ≥ 1 | Bishai discussion threshold; not a biological cutoff |
| CM06 | Repeated ≤10°C days | Monthly CD10 count ≥ 3 | Severe-cold sensitivity |
| CM07 | Any ≤7°C day | At least one day has `Tmin` ≤ 7°C | Tail sensitivity |
| CM08 | Lower-5% mean temperature | Monthly mean temperature ≤ p05 over the frozen monthly reference distribution | Existing P18-compatible measure |
| CM09 | Lower-decile mean temperature | Monthly mean temperature ≤ p10 | Higher-prevalence relative definition |
| CM10 | Lower-5% mean Tmin | Monthly mean of daily `Tmin` ≤ p05 | Nighttime-relative |
| CM11 | Lower-decile mean Tmin | Monthly mean of daily `Tmin` ≤ p10 | Nighttime-relative |
| CM12 | Lower-decile mean Tmax | Monthly mean of daily `Tmax` ≤ p10 | Daytime-relative |
| CM13 | Multimetric cold month | At least two of monthly mean temperature, mean `Tmax`, and mean `Tmin` are at or below their p10 thresholds | Composite; do not co-fit components |

### 3.2 Spell and event-count definitions

| ID | Short name | Operational rule | Main dependency / note |
|---|---|---|---|
| CM14 | Two-day CD12 spell touch | Month contains any day in a run of ≥2 consecutive CD12 days | Preserve runs across boundaries |
| CM15 | Three-day CD12 spell touch | Month contains any day in a run of ≥3 consecutive CD12 days | Core starter |
| CM16 | Five-day CD12 spell touch | Month contains any day in a run of ≥5 consecutive CD12 days | Prolonged-cold sensitivity |
| CM17 | Two-day CD10 spell touch | Month contains any day in a run of ≥2 consecutive CD10 days | Severe-cold persistence |
| CM18 | Exceptional cold-run month | Longest CD12 run touching month ≥ p90 of November–March monthly longest-run values | Relative spell tail |
| CM19 | Multiple cold-event starts | At least two distinct ≥2-day CD12 events start in the month | Freeze event-gap rule |
| CM20 | p90 cold-event-count month | Monthly starts of ≥2-day CD12 events ≥ p90 among November–March months | Hogan-style cold analogue |
| CM21 | p95 cold-event-count month | Monthly cold-event start count ≥ winter p95 | Tail sensitivity |
| CM22 | Upper-tail CD12-count month | Monthly CD12 count ≥ p90 among November–March months | Day burden |
| CM23 | High cold-day proportion | CD12 days / days in month ≥ 0.20 | Length-standardised |

### 3.3 Intensity, compound, anomaly and warning definitions

| ID | Short name | Operational rule | Main dependency / note |
|---|---|---|---|
| CM24 | Cold degree-days below 12°C | `Σ max(0, 12−Tmin)` ≥ p75 among November–March months | Keep continuous too |
| CM25 | Cold degree-days below 10°C | `Σ max(0, 10−Tmin)` ≥ p75 among November–March months | Bishai-threshold sensitivity |
| CM26 | Spell cumulative cold intensity | Sum of `12−Tmin` on days belonging to ≥2-day CD12 spells ≥ winter p75 | Intensity × duration |
| CM27 | Deepest cold excursion | `12−min(Tmin)` ≥ p90 among November–March months | Peak severity |
| CM28 | Abrupt two-day cooling | Largest two-day fall in `Tmin` ≥ p90 of November–March falls | Daily transition |
| CM29 | Sharp month-to-month cooling | Previous minus current monthly mean temperature ≥ p90 of positive cooling changes | Monthly transition |
| CM30 | Cold plus high influenza | CM09 and monthly influenza activity ≥ p75 within the available series | Compound; report missing months |
| CM31 | ≤10°C plus high influenza | CM05 and influenza activity ≥ p75 | Severe compound sensitivity |
| CM32 | Cold plus low absolute humidity | CM09 and winter absolute humidity ≤ p25 | Compound; include main effects |
| CM33 | Cold plus high NO₂ | CM09 and winter NO₂ ≥ p75 | Pollution compound; staged |
| CM34 | Coldest quartile in cool season | Monthly mean temperature ≤ p25 among November–March months | Cool-season relative |
| CM35 | Coldest quartile in DJF | Monthly mean temperature ≤ p25 among December–February months | Core-winter relative |
| CM36 | Calendar-month cold anomaly | Same-calendar-month temperature anomaly z-score ≤ −1 against a frozen external or pre-study climatology | Avoid an 11-value climatology if possible |
| CM37 | Fixed-baseline −1°C anomaly | Monthly mean temperature ≤ corresponding 2013–2019 calendar-month mean −1°C | Baseline sensitivity |
| CM38 | Out-of-season cold anomaly | April–October month satisfies CM36 | Anomaly, not HKO cold-day rule |
| CM39 | Calendar DJF | Month is December–February | Seasonal comparator, not an extreme definition |
| CM40 | Cold shoulder month | November or March with monthly mean temperature ≤ that calendar month's frozen p25 | Transition-season cold |
| CM41 | Composite severe cold | CM03 or CM15 or CM24 is true | Freeze before outcomes; do not co-fit components |
| CM42 | Persistent two-month cold | CM09 is true in both current and previous month | Persistence |
| CM43 | Cold-period onset month | CM09 is true and was false in the previous month | Transition indicator |
| CM44 | High daily-relative cold proportion | At least 20% of days have daily mean temperature below the calendar-day p10 | Relative to time of year |
| CM45 | Daily-relative p10 cold spell | Daily mean temperature below calendar-day p10 for ≥3 consecutive days touching month | Calendar-relative event |
| CM46 | Daily-relative p05 cold spell | Daily mean temperature below calendar-day p05 for ≥3 consecutive days touching month | Tail sensitivity |
| CM47 | Cold Weather Warning month | HKO Cold Weather Warning is active on at least one day in the month | Public-health operational definition |
| CM48 | Sustained warning month | HKO Cold Weather Warning is active on ≥3 days in the month | Warning-duration sensitivity |

---

## 4. Analysis pathways

All pathways sit beside, not in place of, the existing P01–P18 panel. The default outcome is Roro's true stroke-event month aggregate. The default count-model skeleton is negative binomial or quasi-Poisson with a population × days offset where appropriate, calendar-month seasonality, a pre-specified smooth time trend, and staged covariates. Model choice must follow diagnostics and the released aggregate grain.

### Heat pathways H01–H12

| ID | Pathway | Definition set | Analysis intent |
|---|---|---|---|
| H01 | Official absolute hot months | HM01–HM07, HM49–HM50 | Compare policy-recognisable count thresholds and warning-based definitions in separate models |
| H02 | Monthly percentile heat | HM08–HM13 | Test robustness to relative monthly thresholds |
| H03 | Day/night spell heat | HM14–HM18 | Separate persistence from isolated days |
| H04 | Combined day–night heat | HM19–HM20 | Extend Wang/Ren 2D3N coding |
| H05 | Hogan atmospheric count-to-tail | HM21–HM26 | Translate published Li-HW events into monthly count/burden flags |
| H06 | Percentile × duration grid | HM39–HM42 | Treat the grid as one family, not independent discoveries |
| H07 | Heat intensity | HM27–HM31, HM43–HM45 | Compare degree-day, peak and event-intensity measures |
| H08 | Heat compound exposures | HM32–HM33 | Estimate compound indicator with component main effects |
| H09 | Seasonal and anomaly heat | HM34–HM37 | Distinguish climatological anomaly from calendar season |
| H10 | Persistence and onset | HM46–HM48 | Examine transition/persistence separately from level |
| H11 | Jasmine-definition heat extension | Exact Liu et al. (2020) daily-mean-temperature contrast/lag, pending full-PDF manifest; monthly collapse labelled explicitly | Reconstruct source coding, then extend unchanged through 2023 |
| H12 | Frozen hot co-primary | One team-selected member of H05 or H11 | Gate 3 choice; all alternatives labelled sensitivity |

### Cold pathways C01–C12

| ID | Pathway | Definition set | Analysis intent |
|---|---|---|---|
| C01 | Official cold-day months | CM01–CM04 | Compare absolute HKO-based monthly counts |
| C02 | Bishai ~10°C severe-cold sensitivity | CM05–CM07 | Test a discussion-motivated exposure without calling it biological |
| C03 | Monthly percentile cold | CM08–CM13 | Relative monthly cold, linked to P18 |
| C04 | Cold spells | CM14–CM18 | Separate persistence from isolated cold days |
| C05 | Cold event count-to-tail | CM19–CM23 | Symmetric monthly event-count and burden family |
| C06 | Cold intensity | CM24–CM27 | Compare degree-day and peak-severity measures |
| C07 | Cooling transitions | CM28–CM29, CM43 | Test rapid cooling/onset separately from cold level |
| C08 | Cold–influenza compound | CM30–CM31 | Compound sensitivity with transparent missingness |
| C09 | Cold–humidity/pollution compound | CM32–CM33 | Include component main effects; stage pollution |
| C10 | Season, anomaly and persistence | CM34–CM42 | Distinguish calendar winter, anomaly and persistence |
| C11 | Jasmine-definition cold extension | Exact Liu et al. (2020) daily-mean-temperature contrast/lag, pending full-PDF manifest; monthly collapse labelled explicitly | Reconstruct source coding, then extend unchanged through 2023 |
| C12 | Frozen cold co-primary | One team-selected member of C01, C03 or C04 | Gate 3 choice; all alternatives labelled sensitivity |

### Shared reporting discipline

- Freeze thresholds and model universe before inspecting stroke associations.
- Fit nested hot or cold thresholds separately unless a contrast was pre-specified.
- Report effect estimate, confidence interval, exposed-month count, selected months, missingness and diagnostics for every model.
- Treat “number of p-values below/above 0.05” as a secondary pattern description only; use a global heterogeneity test and planned hot-versus-cold contrasts for inference.
- Keep daily mortality/DLNM estimands distinct from monthly stroke aggregate estimands.

---

## 5. Starter sets

### Core next-week run list

| Order | Code | Reason |
|---|---|---|
| 1 | **HM23** | Hogan's Li-HW event count → upper-tail hot-month proposal |
| 2 | **HM08** | Simple relative monthly temperature; compatible with P07 |
| 3 | **HM15** | Wang/Ren five-VHD persistence |
| 4 | **HM17** | Wang/Ren five-HN persistence |
| 5 | **HM19** | Wang/Ren combined 2D3N form |
| 6 | **CM03** | Interpretable absolute cold-day burden |
| 7 | **CM08** | Existing P18-compatible lower-tail month |
| 8 | **CM15** | Interpretable persistent cold spell |

### First-wave additions

| Code | Reason |
|---|---|
| **HM27** | Nighttime heat intensity rather than a binary HN flag |
| **HM32** | Pre-labelled heat–ozone compound sensitivity |
| **CM05** | Directly operationalises the ~10°C discussion prompt |
| **CM30** | Pre-labelled cold–influenza compound sensitivity |

The companion registry `analysis_plan/hot_cold_month_registry.yml` enables these 12 starters. Before Gate 3, Hogan and the team should freeze the Li-HW threshold/reference implementation, season window, cross-month assignment, and one hot/one cold co-primary.

---

## 6. Definition-harmonised Jasmine extension

The full procedure is in `analysis_plan/jasmine_extension_protocol.md`. In brief:

1. use the locked Liu et al. (2020) citation and ingest the full paper/supplement;
2. transcribe its exact reference, temperature and lag basis into a versioned specification without consulting the new stroke outcome;
3. verify exposure coding in the 2013–2016 overlap with the published window;
4. apply the unchanged definition through December 2023;
5. distinguish a same-outcome replication from a definition-only extension into monthly stroke aggregates; and
6. report coefficients only after real data are analysed, with estimates and intervals rather than a significance count alone.

In parallel, preserve Roro’s four 2014–2023 heatwave definitions as a separate team-baseline overlay: `HWD_Tavg` (30.60°C mean-temperature trigger with long lag phases), `HWD_Tmax`, `HWD_Tmin` and `HWD_Tcombined` (2D3N). Exact operators, run lengths and overlap handling must follow the final source manifest; Roro medRxiv v1 contains wording ambiguities that should not be silently resolved.

---

## 7. Honesty box

- **No stroke findings exist yet.** This document specifies candidate exposures and analyses only.
- **“Jasmine’s paper” is identified as Jingwen Liu et al. (2020).** The full PDF/supplement still needs method extraction.
- **The confirmed cold-greater-than-heat AF does not prove Dr Bishai’s recalled p-value pattern.**
- **The ~10°C idea is a hypothesis prompt, not a discovered threshold.**
- **South China heat resistance, including any genetic/adaptation explanation, is discussion-only.** A monthly ecological Hong Kong study cannot identify genetic effects. Acclimatisation, housing, air conditioning, behaviour, occupation, health care, age structure and selection are alternative explanations; avoid causal or ethnic-essentialist language.
- Monthly stroke burden, daily mortality, DLNM risk curves and excess-death estimates are different estimands.
- First GOPC mention is not automatically the stroke-event date; outcome timing remains Roro's domain.
- Synthetic outcomes are never findings.

---

## 8. Selected anchors

- Li C, Wei W, Chan PW, Huang J. “Heatwaves in Hong Kong and their influence on pollution and extreme precipitation.” *Atmospheric Research*. 2025;315:107845. DOI `10.1016/j.atmosres.2024.107845`. **Hogan-recommended weather family.**
- Liu J, Hansen A, Varghese B, et al. “Cause-specific mortality attributable to cold and hot ambient temperatures in Hong Kong: a time-series study, 2006–2016.” *Sustainable Cities and Society*. 2020;57:102131. DOI `10.1016/j.scs.2020.102131`. **Confirmed Jasmine paper.**
- Liu Z, Ren C, Liu J, Kawasaki Yurika, Bishai DM. “Modelling the Excess Mortality Associated with Heat Waves in Hong Kong: 2014–2023.” *medRxiv*. 2026. DOI `10.64898/2026.03.05.26347683`. **Team excess-mortality baseline; medRxiv v1.**
- Wang D, Lau KKL, Ren C, et al. “The impact of extremely hot weather events on all-cause mortality in a highly urbanized and densely populated subtropical city: A 10-year time-series study (2006–2015).” *Science of the Total Environment*. 2019;690:923–931. DOI `10.1016/j.scitotenv.2019.07.039`.
- Liu S, Chan EYY, Goggins WB, Huang Z. “The Mortality Risk and Socioeconomic Vulnerability Associated with High and Low Temperature in Hong Kong.” *International Journal of Environmental Research and Public Health*. 2020;17:7326. DOI `10.3390/ijerph17197326`. **Adjacent lead only; not presumed to be Jasmine's paper.**
