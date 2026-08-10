# M|D pilot F1.0 — failed nuisance-seasonality calibration

**Provenance:** `SYNTHETIC_CALIBRATION`  
**Run:** 100 replicates per scenario; 36 core cells plus six edge cells  
**Daily seasonality:** one annual sine/cosine pair  
**Decision:** `FAIL_METHODS_FEASIBILITY_ONLY`

This pilot used real HKO weather but synthetic daily outcomes constructed only
from disclosure-minimised annual and calendar-month summaries. It did not fit a
new model to governed CHD/HF counts.

## Why the pilot failed

The CHD-like null scenarios were calibrated or conservative:

- type-I error: 0.00–0.06;
- coverage: 0.94–1.00.

The HF-like null scenarios failed under every kernel:

| Kernel | Serial factor | Type-I error | Coverage |
|---|---|---:|---:|
| Same day | Off | 0.64 | 0.36 |
| Same day | Outcome-matched | 0.73 | 0.27 |
| Cumulative 0–5 | Off | 0.74 | 0.26 |
| Cumulative 0–5 | Outcome-matched | 0.62 | 0.38 |
| Cumulative 0–21 | Off | 0.75 | 0.25 |
| Cumulative 0–21 | Outcome-matched | 0.63 | 0.37 |

The daily nuisance model's single harmonic did not represent the disclosed HF
calendar-month profile. Residual cold-season structure was therefore assigned
to the cold exposure. This is a model-design failure, not evidence of a real HF
cold effect.

## Prespecified response

Protocol amendment F1.1 replaces the harmonic with calendar-month indicators,
matching the analysis-of-record seasonality. The full daily design remains at
the frozen 20-parameter cap. The 500-replicate core gate will determine whether
that correction is adequate. The F1.0 results are retained so the correction
cannot be mistaken for an unreported optimisation of real coefficients.
