# HA CHD/HF real analysis — 7 August 2026

Roro delivered monthly CHD and HF first-hospitalisation aggregates for the T2D/HTN cohort (first hospitalisation after first CVD diagnosis). Stroke was named in the email but not attached.

## Status

| Gate | CHD/HF | Stroke |
|---|---|---|
| 1 Schema | Conditional close | Open |
| 2 QC | Closed | Open |
| 3 Headline | Open (packet ready) | Open |

## Key paths

- Receipt: [`../reports/data_receipt_2026-08-07.md`](../reports/data_receipt_2026-08-07.md)
- Gate 3 packet: [`../reports/gate3_decision_packet_2026-08-07.md`](../reports/gate3_decision_packet_2026-08-07.md)
- Results panel: [`../reports/laidlaw_stage3/results_panel_chd_hf_2026-08-07.md`](../reports/laidlaw_stage3/results_panel_chd_hf_2026-08-07.md)
- Runner: `PATHWAY_MODE=real OUTCOMES=chd,hf Rscript scripts/run_cvd_full_analysis.R`
- Temperature share: [`../outputs/share_for_roro/`](../outputs/share_for_roro/)

## Panel pattern (not frozen)

- CHD: hot nights /5 → RR 1.044 (1.012–1.077)
- HF: cold days /5 → RR 1.073 (1.011–1.138); mean_tmin → RR 0.958 (0.919–0.998)

Denominator is C&SD 35+ ecological person-time, not cohort at-risk.
