# Data receipt — HA CVD first-hospitalisation aggregates

**Date:** 7 August 2026  
**Sender:** Roro (Zhenyuan Liu)  
**Playbook:** 02 — HA data arrival  
**Authority:** Email attachment described as monthly counts of AMI-related admissions (CHD, heart failure, and stroke) among patients with T2D and/or HTN, 2013–2023.

## Files received in this upload

| Original upload name | Stored as (gitignored) | SHA-256 | Rows |
|---|---|---|---|
| `coronary_heart_disease_adm_5fcb.xlsx` | `data_raw/ha_secure_placeholder/coronary_heart_disease_adm.xlsx` | `8c717086b3acef51d0de2492c1adbc8da26e0d1f3f6e2593d4463620a742546b` | 132 months |
| `heart_failure_adm_5485.xlsx` | `data_raw/ha_secure_placeholder/heart_failure_adm.xlsx` | `ed8a70b9df04c8bfdcf833fa038390138cdde132a189f842904673c8f0954743` | 132 months |

**Stroke file:** mentioned in the email (“coronary heart disease, heart failure, and stroke”) but **not attached** in this upload. Stroke pathways remain blocked until the file arrives.

## Documented outcome definition (from Roro)

- **Cohort universe:** patients diagnosed with type 2 diabetes and/or hypertension during 2013–2023.
- **Admission cause:** not recorded in the patient-level extract.
- **Event construction:** first hospitalisation after the patient’s first diagnosis record for the relevant cardiovascular disease (CHD or HF). First-diagnosis records constructed with assistance from Dr Zhou.
- **Grain:** territory × calendar month (`year`, `month`, count).
- **Columns observed:**
  - CHD: `year`, `month`, `chd_inpatient`
  - HF: `year`, `month`, `hf_inpatient`
- **Provenance label for analysis CSVs:** `HA_APPROVED_AGGREGATE`
- **Care setting:** inpatient (inferred from column names `*_inpatient`; confirm with Roro if ED-inclusive)

## Inventory totals (from delivered files)

| Outcome | Months | Total events | 2013 annual | 2023 annual |
|---|---|---|---|---|
| CHD | 132 | 156,156 | (see QC receipt) | (see QC receipt) |
| HF | 132 | 29,681 | (see QC receipt) | (see QC receipt) |
| Stroke | — | **not delivered** | — | — |

## Estimand shift (Gate 1)

| Before (planned) | After (delivered) |
|---|---|
| Monthly stroke admission aggregates (general HA framing) | Monthly **first CVD hospitalisations** among **T2D/HTN** patients |
| Stroke as near-term primary | **CHD and HF** runnable now; stroke pending file |
| Admission-reason CVD panel from general HA | Still unavailable; Roro’s marker uses first post-diagnosis hospitalisation |

This is **not** a return to Week-1 AMI principal-diagnosis claims from the general HA file. It is a governed, cohort-restricted first-event construction supplied by Roro.

## Denominator

C&SD population aged 35+ × days-in-month is used as an **ecological offset**. It is **not** T2D/HTN cohort person-time among those still at risk of a first CVD hospitalisation. Rate ratios are therefore ecological associations under a mismatched denominator and must be interpreted with that caveat. A days-only offset sensitivity is available on the panel (`offset_log_days`).

## Governance / git

- Original xlsx and derived monthly CSVs remain under `data_raw/ha_secure_placeholder/` (**gitignored**).
- This receipt, QC notes, and model outputs may be committed; microdata and month-level HA counts must not.

## Gate status after receipt

| Gate | Status | Note |
|---|---|---|
| Gate 1 (schema) | **Conditionally closed for CHD/HF** | Stroke still open; confirm inpatient-only and ICD mapping with Roro when available |
| Gate 2 (QC) | **Proceeding** | Full month coverage 2013–2023; secular decline expected under first-event design |
| Gate 3 (headline) | **Open — team decision** | Panel results prepared; no agent-alone headline freeze |

## Temperature panel for Roro

Share pack: `outputs/share_for_roro/` (HKO monthly temperature + analysis exposures).
