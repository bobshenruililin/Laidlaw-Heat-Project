# Canon: weather-definition families

**Purpose:** durable map of the named weather families used in the Hong Kong monthly thermal–stroke project. This file records provenance and decision status; executable parameters remain in the registry after human lock.

## Status language

- **`locked`**: confirmed source identity, published convention or team decision. It does not automatically mean “chosen co-primary.”
- **`proposed`**: a project translation or sensitivity that has not been adopted as primary.
- **`pending Hogan`**: the weather role or monthly implementation must be settled with Hogan before Gate 3.

Where a source document itself is missing or ambiguous, that source dependency is stated separately rather than pretending it is a Hogan decision.

## 1. HKO absolute-extreme family

**Named rules**

- hot night (`HN`): daily `Tmin ≥28°C`;
- very hot day (`VHD`): daily `Tmax ≥33°C`;
- extremely hot day (`EHD`): daily `Tmax ≥35°C`;
- cold day (`CD12`): daily `Tmin ≤12°C`.

These are official Hong Kong Observatory operational/climatological conventions. Monthly counts and spell collapses are project exposures, not new HKO definitions.

- **Source:** [Hong Kong Observatory, projections of hot nights, very hot days and cold days](https://www.hko.gov.hk/en/climate_change/proj_hk_annual_vhot_days.htm).
- **DOI:** not applicable; HKO is an official institutional source.
- **Status:** `locked` for the absolute daily thresholds; `pending Hogan` for station choice, cross-month spell handling and their role in the Gate 3 pair.

## 2. Wang/Ren extremely-hot-weather-event family

**Published structures**

- `5VHD`: at least five consecutive days with `Tmax ≥33°C`;
- `5HN`: at least five consecutive nights with `Tmin ≥28°C`;
- `2D3N`: two consecutive very hot days combined with three hot nights.

The paper examined multiple lengths and day–night combinations and selected these as representative local EHWE forms. For monthly analysis, event start, event touch and event-day burden are different possible mappings and must not be conflated.

- **Source:** Wang D, Lau KKL, Ren C, Goggins WB, et al. (2019), *Science of the Total Environment* 690:923–931.
- **DOI:** [`10.1016/j.scitotenv.2019.07.039`](https://doi.org/10.1016/j.scitotenv.2019.07.039).
- **Status:** `locked` as a published daily mortality family; `pending Hogan` for the monthly mapping and co-primary/sensitivity role.

## 3. Jasmine MMT / attributable-fraction approach

Jingwen Liu (“Jasmine”) et al. model daily mean temperature against daily total and cause-specific mortality with a DLNM integrated with quasi-Poisson regression. The minimum-mortality temperature (MMT) is the reference for partitioning attributable burden below it (cold) and above it (heat), with source-specific moderate and extreme ranges.

**Locked facts**

- Hong Kong, 2006–2016;
- reversed J-shaped temperature–total mortality relationship;
- overall AF: **4.72% cold vs 0.16% heat**;
- AF: **4.25% moderate vs 0.63% extreme**.

The exact MMT, moderate/extreme boundaries, spline knots, lag basis and uncertainty procedure still require extraction from the full paper and supplement. Do not infer those values from the headline AFs or from Roro’s later transcription.

- **Source:** Liu J, Hansen A, Varghese B, et al. (2020), *Sustainable Cities and Society* 57:102131.
- **DOI:** [`10.1016/j.scs.2020.102131`](https://doi.org/10.1016/j.scs.2020.102131).
- **Status:** `locked` for paper identity, estimand, model family and headline AFs. A source-faithful executable definition is not yet available; this is pending full-PDF extraction, not a Hogan choice. Any monthly stroke transport remains `proposed`.

## 4. Hogan / Li-HW count-to-tail family

### Published Li-HW event

During May–September, daily `Tmax` exceeds its calendar-day p90 threshold for at least three consecutive days. The published construction uses a 15-day moving calendar window and joins events separated by no more than two days.

### Hogan’s project adaptation

Count Li-HW event starts by month, then flag months in the upper tail of the frozen event-count distribution. The p90 form is `HM23`.

**Credit rule:** Li et al. provide the atmospheric event definition; **Hogan proposed the monthly count → upper-tail adaptation for this project**. Never describe the whole `HM23` recipe as coming from Li alone.

- **Source:** Li C, Wei W, Chan PW, Huang J (2025), *Atmospheric Research* 315:107845.
- **DOI:** [`10.1016/j.atmosres.2024.107845`](https://doi.org/10.1016/j.atmosres.2024.107845).
- **Status:** `locked` for provenance and the published Li-HW structure; `pending Hogan` for reference period, percentile method, season confirmation, missing-day tolerance, event-gap handling, start/touch/burden mapping, monthly p90 denominator and tie rule.

## 5. Roro `HWD_*` family

Roro’s medRxiv v1 applies published local mortality RRs under four heatwave scenarios:

| Label | medRxiv v1 operational intent | Primary source family |
|---|---|---|
| `HWD_Tavg` | A 20-day window starts when daily mean temperature crosses the 99th-percentile value of 30.60°C; independent starts are separated by at least 20 days | Jasmine |
| `HWD_Tmax` | Prolonged very hot days based on `Tmax ≥33°C` | Wang/Ren |
| `HWD_Tmin` | Prolonged hot nights based on `Tmin ≥28°C` | Wang/Ren |
| `HWD_Tcombined` | Combined 2D3N day–night event | Wang/Ren |

MedRxiv v1 contains ambiguities including `≥` versus “exceeds,” five days versus “longer than five,” and overlap/reference-period handling. Do not resolve them silently. The revised manuscript must be compared before an executable source manifest is called final.

- **Source:** Liu Z, Ren C, Liu J, Kawasaki Yurika, Bishai DM (2026), *medRxiv* v1.
- **DOI:** [`10.64898/2026.03.05.26347683`](https://doi.org/10.64898/2026.03.05.26347683).
- **Status:** `locked` as Roro’s named four-scenario mortality baseline; exact operators are pending the revised-source comparison; their use as four monthly exposure siblings is `pending Hogan`. Mortality RRs are not transportable as stroke coefficients.

## 6. Project HM/CM starters

These are monthly exposure candidates. “Touch” means that at least one event day lies in the month; runs must be detected across month boundaries.

### Core starters

| Code | Working monthly rule | Provenance / DOI | Status |
|---|---|---|---|
| `HM23` | Li-HW event-start count ≥ frozen warm-season p90 | Hogan adaptation of Li; `10.1016/j.atmosres.2024.107845` | `pending Hogan` |
| `HM08` | Monthly mean temperature ≥ frozen p90 | Project relative-month family; no single source DOI | `proposed`; `pending Hogan` |
| `HM15` | Month touches ≥5 consecutive `Tmax ≥33°C` days | Wang/Ren; `10.1016/j.scitotenv.2019.07.039` | `proposed`; `pending Hogan` |
| `HM17` | Month touches ≥5 consecutive `Tmin ≥28°C` nights | Wang/Ren; `10.1016/j.scitotenv.2019.07.039` | `proposed`; `pending Hogan` |
| `HM19` | Month touches a Wang/Ren-style 2D3N window | Wang/Ren; `10.1016/j.scitotenv.2019.07.039` | `proposed`; `pending Hogan` |
| `CM03` | At least five days in month with `Tmin ≤12°C` | HKO threshold; no DOI | `proposed`; `pending Hogan` |
| `CM08` | Monthly mean temperature ≤ frozen p05 | Project relative-month family; no single source DOI | `proposed`; `pending Hogan` |
| `CM15` | Month touches ≥3 consecutive `Tmin ≤12°C` days | Project spell over HKO threshold; no DOI | `proposed`; `pending Hogan` |

### First-wave sensitivities

| Code | Working monthly rule | Rationale / DOI | Status |
|---|---|---|---|
| `HM27` | `Σ max(0, Tmin−28°C)` ≥ May–October p75 | Night-heat intensity; Guo 2024 `10.1016/j.lanwpc.2024.101168` motivates intensity but does not define this monthly cutoff | `proposed` |
| `HM32` | `HM08` plus warm-season ozone ≥ p75, with component main effects | Compound heat–pollution sensitivity; Guo 2025 `10.1021/acs.est.5c10594` | `proposed` |
| `CM05` | At least one day in month with `Tmin ≤10°C` | Bishai discussion prompt; no source DOI | `proposed` severe-cold sensitivity only |
| `CM30` | Lower-decile cold month plus influenza activity ≥ p75, with component main effects | Yang/Chong 2025 `10.1007/s00484-025-02870-2` motivates cold and influenza, not this exact monthly composite | `proposed` |

## Canonical decision rule

Before substantive stroke-association results are inspected, freeze one hot and one cold co-primary, all reference distributions, percentile/tie methods, event-boundary rules, missing-day tolerance and the selected-month audit. Keep the remaining definitions as a labelled family. A definition becomes primary by written Gate 3 decision, never because it later gives the largest or most significant stroke estimate.
