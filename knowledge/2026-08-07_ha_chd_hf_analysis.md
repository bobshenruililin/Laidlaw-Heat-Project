# HA CHD/HF real analysis — 7 August 2026

Roro delivered monthly CHD and HF first-hospitalisation aggregates for the T2D/HTN cohort (first hospitalisation after first CVD diagnosis). Stroke was named in the email but not attached.

## Status

| Gate | CHD/HF | Stroke |
|---|---|---|
| 1 Schema | Conditional close | Open |
| 2 QC | Closed | Open |
| 3 Headline | Open (amended packet ready) | Open |

## Key paths

- Receipt: [`../reports/data_receipt_2026-08-07.md`](../reports/data_receipt_2026-08-07.md)
- Gate 3 packet: [`../reports/gate3_decision_packet_2026-08-07.md`](../reports/gate3_decision_packet_2026-08-07.md)
- Results panel: [`../reports/laidlaw_stage3/results_panel_chd_hf_2026-08-07.md`](../reports/laidlaw_stage3/results_panel_chd_hf_2026-08-07.md)
- Manuscript: [`../manuscript/chd_hf_thermal_associations_2013_2023.md`](../manuscript/chd_hf_thermal_associations_2013_2023.md)
- Release: [`../outputs/release_chd_hf/`](../outputs/release_chd_hf/)
- Runner: `PATHWAY_MODE=real OUTCOMES=chd,hf Rscript scripts/run_cvd_full_analysis.R`

## Amended core pattern (not frozen; SAP A1)

Separate exposures; days-only offset; Newey–West lag-6:

- CHD: hot nights /5 → count ratio **1.022 (1.002–1.042)**; q = 0.192
- HF: cold days /5 → count ratio **1.073 (1.006–1.144)**; q = 0.192

Do **not** quote the earlier joint P04 CHD hot-night IRR 1.044 as the amended core result (joint model inflates vs separate). Denominator for amended core is days-in-month (count ratios), not T2D/HTN cohort person-time.
