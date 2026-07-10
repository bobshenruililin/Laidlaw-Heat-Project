# One-Page Decisions and Data Needs

**Project:** Thermal extremes and cardiovascular hospital burden in an aging Hong Kong  
**Prepared by:** Bob Shen | **Date:** 10 July 2026  
**Audience:** Professor Bishai, Hogan, Roro  

> Status check: HKO climate exposures are real and processed. Population and pollution files are not yet real. HA outcomes are not available. No real CVD association has been estimated.

---

## Decisions required

| Decision | Recommended default | Who should confirm | Why it matters |
|---|---|---|---|
| Study window | Core **Jan 2013–Dec 2023**; request **2024 as optional extension** without delaying core | Bishai / Roro | Defines 132 vs 144 months; 2024 adds heat contrast but is not required to start |
| Primary outcome | Emergency/unplanned **inpatient** admissions with **principal diagnosis** | Bishai / Roro | Avoids elective seasonality and incidental coding |
| Diagnosis groups | AMI; ischemic stroke; hemorrhagic stroke | Bishai / Roro | Matches historical Hong Kong literature and policy relevance |
| Coding system | Confirm ICD-9-CM / ICD-10 / mixed by year | Roro | Determines code lists; currently provisional only |
| Age bands | Prefer 5-year bands; **separate 65–69 and 70–74**; keep 75–79, 80–84, 85+ if possible | Roro / Hogan note | Aging hypothesis and intervention targeting |
| Episode rule | Combine transfers; retain true readmissions; month = admission/presentation month | Roro | Prevents double-counting |
| ED vs inpatient | Analyze separately unless mutually exclusive ED-only events available | Roro | Avoids double-counting care pathways |
| HKO exposure | HKO Headquarters primary; multi-station sensitivity if feasible | Hogan / Bishai | Matches official extreme definitions; representativeness remains to be confirmed |
| EPD stations | **General stations primary**; roadside sensitivity only | Hogan / Bishai | Territory-wide background vs roadside exposure |
| Influenza | Sensitivity model initially (not primary) | Bishai | May confound or mediate cold effects |
| COVID phases | Full-period with phases + pre-COVID + exclude 2020–2022 | Bishai | Utilization disruption; phase cut-points remain to be confirmed |
| District analysis | Out of scope for first paper | Bishai | Adds exposure/denominator complexity |

---

## Data needed

| Dataset | Exact need | Current status | Proposed provider | Proposed transfer/access route |
|---|---|---|---|---|
| HA CVD admissions | Monthly aggregate: `month × age × sex × diagnosis × care_setting`; principal diagnosis; n_events (± patients, deaths, bed-days); coding system; suppression flag | **Blocked — not available** | Roro / HA | **Secure HA/HKU channel only** until Roro confirms whether aggregates may leave the environment and whether output vetting is required |
| HA utilization context | Optional all-cause emergency admissions / ED by age-sex for COVID disruption | Not requested yet | Roro / HA | Same secure process |
| C&SD population | Mid-year (or half-yearly) population by sex and age for 2012–2024, constructable into preferred age bands | Import path ready; current file is **SYNTHETIC_DENOMINATOR** | Bob (download) / C&SD Table 110-01002 | Ordinary institutional email / public download OK |
| EPD pollution | Monthly (or daily→monthly) NO₂, O₃, PM2.5, PM10 from **general** stations, 2013–2023 (±2024); completeness metadata; roadside separate | Portal documented; current file is **PLACEHOLDER_NOT_FOR_INFERENCE** | Hogan / EPD EPIC | Public files OK by ordinary channels once downloaded |
| HKO climate | Daily Tmin/Tmax/Tmean, RH, rainfall; monthly extremes already built | **Complete for first stage** (HKO Headquarters) | Hogan review / Bob | Public; already in repo |
| CHP influenza | Monthly flu activity indicator aligned to study months | Path prepared; not loaded | Bob / CHP | Public surveillance files, subject to source terms |
| Holiday / typhoon calendars | Public-holiday day counts; CNY indicator; optional typhoon-signal days | Provisional holiday scaffold only | Bob / Hogan | Public calendars OK |

---

## What Bob will not do until confirmed

- Will not treat synthetic model coefficients as study findings.  
- Will not email HA data or unvetted secure outputs.  
- Will not freeze a “regime shift” claim before real HA analysis.  
- Will not put highly collinear heat metrics into one default model without team approval.
