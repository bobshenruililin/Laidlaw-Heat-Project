# CVD descriptives note (CHD / HF)

- Run at: 2026-08-07 09:04:37.233847
- Provenance: **HA_APPROVED_AGGREGATE**
- Stroke file: not delivered (excluded).
- Denominator caveat: C&SD population 35+ is ecological person-time, **not** T2D/HTN cohort at-risk.
- Month-level HA count tables are **not** printed here (summaries and figures only).

## Snapshot

| Outcome | Months | Years | Total events | Mean monthly |
|---|---:|---|---:|---:|
| chd | 132 | 2013-2023 | 156156 | 1183 |
| hf | 132 | 2013-2023 | 29681 | 224.9 |

## Temperature correlations (events vs exposure)

| Outcome | Exposure | Pearson r | p |
|---|---|---:|---:|
| chd | mean_temp | -0.204 | 0.0192 |
| chd | mean_tmax | -0.217 | 0.0123 |
| chd | mean_tmin | -0.201 | 0.021 |
| hf | mean_temp | -0.402 | 1.76e-06 |
| hf | mean_tmax | -0.409 | 1.09e-06 |
| hf | mean_tmin | -0.402 | 1.76e-06 |

## Outputs

- `outputs/tables/cvd_descriptive_*.csv`
- `outputs/figures/descriptives/cvd_*.png`

Gate 3 remains open; descriptives are not primary manuscript claims.
