# Research-idea registry (Exploration Lab)

Unconstrained wondering. **Not in the live manuscript** unless promoted after data, adversarial review, and author scope.

| ID | Research question | Mechanism | Estimand | Required data | Identification | Major threats | Novelty | Feasible now? | Where it belongs |
|---|---|---|---|---|---|---|---|---|---|
| E1 | Does hourly nighttime excess heat (Guo HNe) associate with first CHD hospitalisation? | Nighttime intensity vs official flag | Daily RR, hot season | Daily HA + hourly T | DLNM, adjust multi-day mean T | Admission cause still missing | Local first-event vs Guo NCNE | **No** (daily HA absent) | Future paper |
| E2 | Stroke after the CHD/HF file | Separate vascular beds | Monthly or daily stroke counts | Stroke attachment from Roro | Same panel architecture | Still no admission cause unless delivered | Completes Hogan skeleton | **No** | Future / supplement if attached |
| E3 | Cohort incidence with still-at-risk person-time | Depletion vs incidence | IRR not count ratio | Monthly risk-set | Offset = log(person-time) | Misclassified diagnosis dates | Changes the estimand | **No** | Future; would replace A1 interpretation |
| E4 | Age 65–69 / 70–74 / 75+ | Vulnerability | Stratum-specific count ratios | Age-band aggregates | Same models by band | Sparse HF | Hogan has asked | **No** until delivered | Supplement |
| E5 | Medication as effect modifier | Beta-blockers / diuretics / ACEi | Interaction or stratified RR | Time-varying drugs | Needs timing relative to event | Indication bias | Answers Hogan comment 4 properly | **No** | Future; do not name in Intro now |
| E6 | Housing / AC / behavioural adaptation | Exposure misclassification | Bias analysis or individual exposure | Housing, AC, time-activity | Not identified from HQ Tmin | Residual confounding | Hogan forbade dangling it | **No** | Future; omit from current Intro |
| E7 | Health-economic burden of thermal admissions | Utilisation × unit cost | Cost of illness or policy CEA | Costs, LOS, comparator (warning, cooling centre) | Decision model, not this regression | No prices in HA file | Would be a second paper | **No** for *this* paper | Passion / future; see brief |
| E8 | Official-flag vs reanalysis-flag as instruments | Measurement | Encoding contrast, not health attenuation | Already have monthly bridge | Do not treat slope 0.045 as attenuation of 1.022 | Ecological | Identification lab already done | **Yes** as Explore | Stay out of Results |
| E9 | Between-winter cold-day natural experiment | 2019 had 1 cold day | Descriptive exposure only | Already have | Not a health experiment | One year, COVID adjacent | Tempting but false | Exposure natural history only | Do not promote 2019 as an experiment |
| E10 | Dynamic adaptation / declining heat RR over 2013–2023 | Behavioural acclimatisation | Time-varying β | Same monthly file | Interaction with year | Depletion confounding | Related to Li-HW / Hogan tails | Fragile on 132 months | Explore memo only |
| E11 | Spatial spillovers / district heat | Intra-HK exposure | Small-area RR | District health (restricted) + LST | Ecological spatial | Confidentiality; transport of HQ ratios | Peer-cities atlas is exposure-only | **No** for live paper | Geospatial stays exposure-only |
| E12 | Policy threshold: 28 °C night vs 29.5 °C | Calibration of official definition | P(HKO flag \| Tmin) already measured | Public HKO | Not a health model | Reliability ≠ attenuation | Luna calibration exists | **Yes** Explore | Hogan W03 card; not Methods body |

Promotion rule: data exist + survives Sol/Fable red-team + fits agreed scope. None of E1–E7, E9–E11 is promoted today.
