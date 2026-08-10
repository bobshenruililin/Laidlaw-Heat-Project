# Gate 2 QC close — CHD and HF first-hospitalisation aggregates

**Date:** 7 August 2026  
**Playbook:** 02 → Gate 2  
**Provenance:** `HA_APPROVED_AGGREGATE`

## Coverage

| Check | CHD | HF |
|---|---|---|
| Months vs 2013–2023 | 132 / 132 | 132 / 132 |
| Missing months | 0 | 0 |
| Negative counts | none | none |
| Suppression flags | none in file | none in file |
| Grain | territory-month | territory-month |
| Age × sex | not provided | not provided |
| Total events | 156,156 | 29,681 |
| Mean / month | 1,183 | 225 |
| Secular pattern | strong decline | strong decline |

Annual totals and seasonality: `outputs/tables/cvd_descriptive_*.csv` and `outputs/reports/cvd_descriptives_note.md`.

## Definition confirmed from sender

- Cohort: T2D and/or HTN, 2013–2023.
- Event: first inpatient hospitalisation after first diagnosis record for CHD or HF.
- Admission cause not recorded in the underlying patient extract.
- Stroke file referenced in email but **not delivered** in this upload.

## Merge integrity

- Joined to HKO exposures, EPD pollution, C&SD population 35+, holidays, flu, COVID phase.
- Offset: `log(population_35plus × days_in_month)` with documented mismatch to cohort at-risk.
- Days-only offset sensitivity completed (`outputs/tables/cvd_offset_sensitivity.csv`).

## Disposition

| Item | Decision |
|---|---|
| CHD / HF modelling | **Gate 2 closed** for territory-month first-event aggregates |
| Stroke | **Gate 2 open** — file absent |
| Denominator | Proceed with ecological C&SD offset + explicit limitation |
| Age / sex / subtype pathways | Skipped (P09, P13, P17) until stratified release |
| Small cells | Not applicable at territory-month counts observed |

Gate 2 close does **not** freeze a headline specification (Gate 3).
