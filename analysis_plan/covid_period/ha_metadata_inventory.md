# HA metadata inventory — what came with the admissions panel

**Date:** 10 September 2026. **Trigger:** Hogan asked whether other metadata, especially lab tests, came with the panel.

**Rule:** DUA — this note does not open governed panels. Column names from the synthetic schema, the 7 August receipt, and Roro ask lists only.

## HAVE (this transfer)

- CHD: `year`, `month`, `chd_inpatient` — 132 months.
- HF: `year`, `month`, `hf_inpatient` — 132 months.
- Event: first recorded hospitalisation after first CHD/HF diagnosis among T2D/HTN.
- Merged in-repo (not HA labs): HKO monthly climate and official extremes; EPD pollution; Flu Express 121/132 months; days-in-month.

Schema names: [`data_processed/samples/SYNTHETIC_chd_hf_schema.csv`](../../data_processed/samples/SYNTHETIC_chd_hf_schema.csv). Required columns: [`scripts/final_model_helpers.R`](../../scripts/final_model_helpers.R) `.panel_required_columns`.

Receipt: [`reports/data_receipt_2026-08-07.md`](../../reports/data_receipt_2026-08-07.md).

## ASK RORO (already ranked; not labs)

1. Stroke monthly file (named, not attached).
2. Still-at-risk T2D/HTN person-time by month.
3. Age bands 65–69 / 70–74 / 75+ monthly counts.
4. ICD list + inpatient vs DAE in writing.

Source: [`analysis_plan/roro_missing_data_asks.md`](../roro_missing_data_asks.md).

## NEVER PROMISED / not in this transfer

| Item | Status |
|---|---|
| Lab tests (HbA1c, lipids, BNP, NT-proBNP, creatinine, eGFR, troponin, glucose) | **Zero hits** in schema, receipt, correspondence contract, or ranked asks. Other HKU CDARS papers can have labs; that is a **new extract**. |
| Admission cause / principal diagnosis | Absent (A04). Do not ask again. |
| Medications, BMI | Desired once (A27); ranked list says do not ask from the July thread. |
| Housing, indoor temperature, sleep, blood pressure as panel variables | Unmeasured. |
| Patient-level microdata with this aggregate transfer | Not supported. |

## What to tell Hogan

The admissions panel that arrived is three columns per outcome. Lab metadata did not come with it. Asking for labs is a new governance conversation, not a merge.

**Default until Bishai agrees:** do not add labs to the Roro ask list.
