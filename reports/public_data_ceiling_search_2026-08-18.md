# Public-file ceiling search — 18 August 2026

**Fetched (UTC):** 2026-08-18T18:40:26Z  
**Script:** `scripts/52_public_outcome_ceiling_search.py`  
**Provenance:** `PUBLIC_WEB_FETCH`. Not Hospital Authority microdata. Not a coefficient.

## Verdict

Can a lab intern replace the governed monthly CHD/HF first-hospitalisation series among people with T2D and/or HTN using only public Hong Kong files?

No. Public files are annual or financial-year episode throughput, survey prevalence, or weather. They are not a 132-month first-event series in the T2D/HTN cohort, they do not carry admission cause, and they do not supply still-at-risk person-time.

## What each fetch actually contained

| ID | HTTP | Bytes | Grain / note |
|---|---:|---:|---|
| `HA_IPDPDD_JSON` | 200 | 202936 | financial year × cluster × hospital; inpatient/day-patient discharges and deaths; no ICD; no month; not a T2D/HTN first-event series |
| `HA_IPDPDD_AGE_GENDER` | 200 | 33612 | financial year × age group × gender; still no ICD, month, cohort, or first-event rule |
| `HA_DISEASE_GROUP_JSON_GUESS` | 200 |  | DATA.GOV.HK inpatient-throughput dataset lists beds/discharges/ALOS, not this filename. HA Major Statistics names a disease-group table; no matching public JSON was found at these guessed paths. |
| `HA_DISEASE_GROUP_JSON_GUESS` | 200 |  | DATA.GOV.HK inpatient-throughput dataset lists beds/discharges/ALOS, not this filename. HA Major Statistics names a disease-group table; no matching public JSON was found at these guessed paths. |
| `HA_DISEASE_GROUP_JSON_GUESS` | 200 |  | DATA.GOV.HK inpatient-throughput dataset lists beds/discharges/ALOS, not this filename. HA Major Statistics names a disease-group table; no matching public JSON was found at these guessed paths. |
| `DH_2023_INPATIENT_BY_DISEASE` | 200 | 1858 | one calendar year; ICD-10 chapter totals; episode basis including day inpatients; all hospitals; not first hospitalisation after first CHD/HF diagnosis; not restricted to T2D/HTN |
| `CKAN_INPATIENT_SEARCH` | 200 | 9449 | CKAN returned C&SD Table 930-92087 (HA inpatient services, quarterly throughput), not monthly ICD first-events in a chronic-disease cohort |
| `CKAN_DISEASE_GROUP_SEARCH` | 200 | 219 |  |
| `HKO_DAILY_MEAN_2013` | 200 | 6477 | public daily mean temperature at HKO Headquarters; intern-accessible; does not supply outcomes or Hogan's encoding lock |
| `HKO_HOURLY_TEMP_WRONG_DATATYPE` | 200 |  | HHOT is hourly astronomical tides in the HKO Open Data API, not hourly air temperature. A 2013–2023 hourly temperature archive was not found on this endpoint. |
| `HA_PROVISION_INDEX` | 200 | 652789 |  |
| `HA_APPLICATION_PROCEDURE` | 200 | 633133 |  |
| `HA_SUBMISSION` | 200 | 628040 |  |
| `HA_FORM_A_GN` | 200 | 215997 |  |
| `HA_STANDARD_PROCEDURES` | 200 | 90728 |  |
| `HA_UNDERTAKING` | 200 | 215762 |  |
| `EHPDCL_ACCESS` | 200 | 44225 |  |
| `HKU_EHPDCL` | 200 | 42659 |  |
| `CHP_HEART_DISEASES` | 200 | 19708 |  |
| `CHP_CEREBROVASCULAR` | 200 |  | annual whole-population episode discharges (2024 ~27,100) and 2,911 registered deaths; not the project stroke aggregate |
| `HA_MAJOR_STATISTICS` | 200 | 739948 |  |

## HA throughput sample (first row of `ipdpdd-en.json`)

```json
{
  "Financial Year": "2008-09",
  "Cluster": "Hong Kong East Cluster",
  "Hospital": "Cheshire Home, Chung Hom Kok",
  "IP Discharges and Deaths": 246,
  "DP Discharges and Deaths": null,
  "IP and DP Discharges and Deaths": 246
}
```

Rows: 809. Financial years: ['2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20', '2020-21', '2021-22', '2022-23', '2023-24', '2024-25']. Month field: False. ICD field: False.

## DH 2023 circulatory chapter row

`I00-I99 | Diseases of the circulatory system | 162691 | 7.20%`

one calendar year; ICD-10 chapter totals; episode basis including day inpatients; all hospitals; not first hospitalisation after first CHD/HF diagnosis; not restricted to T2D/HTN

## HKO daily mean temperature, 2013 (public; intern can fetch)

Daily rows: 365. First: `2013,1,1,13.9,C`. Last: `2013,12,31,15.3,C`.

This is the opposite of the outcome ceiling. Weather is public. Hogan's remaining job is to lock how monthly tails are defined, not to unlock the CSV.

## Machine JSON

`outputs/auto_research/public_outcome_ceiling_search.json`

