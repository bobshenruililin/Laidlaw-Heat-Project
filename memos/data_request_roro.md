# Data request memo — Hospital Authority extract (Roro)

**To:** Roro  
**From:** Project analysis team (Bob / supporting AI pipeline)  
**Subject:** Request for aggregate monthly Hospital Authority cardiovascular admissions extract, 2013–2023  
**Date:** 2026-07-10  

## Status — 12 July 2026

Roro confirmed: **ICD-9** (DAE records included — definition TBD); **patient-level complete admissions**; **no ED-to-inpatient** episodes in this extract; age bands including **65–69 and 70–74** supported; HPC access after **wet-ink signatures from Bob and Hogan**. IRB update raised for discussion. Bishai (12 Jul) directed next step: merge monthly Tmax/Tmin (+ lag) to AMI/stroke admission risk; covariates include age, sex, diuretics, beta blockers, metformin, SGLT2is, BMI; next write-up needs Table 1. Still open: principal diagnosis, meds/BMI field availability, DAE meaning, admission-risk denominator. Lab meeting 17 July 2026.

---

Dear Roro,

We are preparing a retrospective ecological time-series study of thermal extremes and cardiovascular hospital burden in Hong Kong. We would be grateful for your advice and, if feasible, an aggregate monthly Hospital Authority extract for **January 2013 through December 2023**, with **January–December 2024 as an optional extension** that should not delay the core extract.

## Study framing

> Thermal extremes, aging, pollution, and cardiovascular hospital burden in Hong Kong, 2013–2023.

Primary scientific interest: associations of officially defined hot nights and cold days with AMI, ischemic stroke, and hemorrhagic stroke admissions among residents aged 35+, with attention to older age groups and COVID-period disruption.

## Requested unit of observation

One row per:

```text
admission_month × age_group × sex × diagnosis_group × care_setting
```

Please base the month on the **date of admission or ED presentation**, rather than discharge date.

## Primary outcome

Monthly number of **inpatient admissions with the cardiovascular condition recorded as the principal diagnosis**, preferably restricted to **emergency or unplanned** admissions if admission type is available.

## Secondary outcomes (if feasible)

- ED attendances
- ED-only attendances not followed by admission
- Number of unique patients
- In-hospital deaths
- Bed-days
- Total all-cause emergency inpatient admissions by age and sex
- Total all-cause ED attendances by age and sex

The all-cause series would help characterize COVID-era disruptions in care-seeking and hospital utilization.

## Preferred age groups

```text
35–39, 40–44, 45–49, 50–54, 55–59, 60–64,
65–69, 70–74, 75–79, 80–84, 85+
```

If five-year groups are not possible, minimum acceptable grouping:

```text
35–44, 45–54, 55–64, 65–69, 70–74, 75–84, 85+
```

Separating **65–69** from **70–74** is a priority.

## Diagnosis groups and coding questions

Please confirm the coding system and version used during each year of the study period.

### Provisional ICD-9-CM

| Group | Codes | Notes |
|---|---|---|
| AMI | 410.x | Exclude old MI 412 |
| Hemorrhagic stroke | 430, 431, provisionally 432.x | Sensitivity: 430–431 only |
| Ischemic stroke | 433.x1, 434.x1, 436 | Sensitivity: with/without 436 |
| Exclude | TIA 435.x; stroke sequelae 438.x; old MI 412 | |

### ICD-10 backup

| Group | Codes |
|---|---|
| AMI | I21–I22 |
| Hemorrhagic stroke | I60–I62 |
| Ischemic stroke | I63 |
| Unspecified stroke | I64 only in sensitivity |
| Exclude TIA | G45 |

Please advise whether any local HA coding modifications or coding transitions apply during 2013–2023.

## Requested fields

```text
year
month
month_id
age_group
sex
diagnosis_group
care_setting
admission_type          # if available
n_events
n_patients
n_deaths_in_hospital
bed_days
suppression_flag
coding_system
coding_version
data_revision_date
```

## Clarifying questions

1. Can principal diagnosis be distinguished from secondary diagnoses?
2. Are counts admissions, discharges, completed episodes, or unique patients?
3. Can inter-hospital transfers or transfers between specialties be joined into one episode?
4. Are same-day admissions and readmissions counted separately?
5. Can ED-only events be separated from ED visits followed by admission?
6. Are emergency and elective admissions distinguishable?
7. Do the records include only Hong Kong residents, and how is residency defined?
8. Did coding practices or hospital coverage change during 2013–2023?
9. What small-cell suppression threshold is used?
10. Is complementary suppression applied?
11. Can coarser age or diagnosis strata be supplied if detailed cells are suppressed?
12. Would 2024 be available without delaying the 2013–2023 extract?

## Data security and format

No personal identifiers are requested. Preferred delivery is a de-identified aggregate CSV or Excel file with a data dictionary, code list, and a small mock or masked sample before the full extract.

Many thanks for your help.

Best regards,  
Bob / analysis team
