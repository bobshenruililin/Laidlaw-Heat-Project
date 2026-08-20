# Minimum detectable count ratio from the existing ladder — 18 August 2026

**Provenance:** derived from `outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv` (`HA_APPROVED_AGGREGATE`). Not a new fit. Not a primary.
**Rule:** Wald MDE at 80% power, two-sided 5%, SE from the reported 95% interval. Count-scale MDE is exp((1.96+0.84)×SE_log).

This table says what the 132-month design could have detected under each reported standard error, and did not protect at *q* < 0.05. It does not create person-time, stroke, or admission cause.

## Newey–West lag-6 (analysis-of-record display)

| Outcome | Contrast | Observed RR | MDE (80%) | Observed excludes 1 |
|---|---|---:|---:|---|
| chd | Mean temperature, per 1 C | 0.993 (0.976–1.010) | 1.0247 (2.47%) | false |
| chd | Mean maximum temperature, per 1 C | 0.993 (0.979–1.007) | 1.0202 (2.02%) | false |
| chd | Mean minimum temperature, per 1 C | 0.994 (0.977–1.012) | 1.0251 (2.51%) | false |
| chd | Hot nights, per 5 days | 1.022 (1.002–1.042) | 1.0286 (2.86%) | true |
| chd | Cold days, per 5 days | 0.995 (0.949–1.043) | 1.0698 (6.98%) | false |
| chd | Very hot days, per 5 days | 0.999 (0.974–1.025) | 1.0369 (3.69%) | false |
| hf | Mean temperature, per 1 C | 0.974 (0.947–1.002) | 1.0409 (4.09%) | false |
| hf | Mean maximum temperature, per 1 C | 0.981 (0.958–1.005) | 1.0343 (3.43%) | false |
| hf | Mean minimum temperature, per 1 C | 0.973 (0.947–1.000) | 1.0398 (3.98%) | false |
| hf | Hot nights, per 5 days | 1.003 (0.976–1.031) | 1.0401 (4.01%) | false |
| hf | Cold days, per 5 days | 1.073 (1.006–1.144) | 1.0955 (9.55%) | true |
| hf | Very hot days, per 5 days | 0.995 (0.963–1.028) | 1.0478 (4.78%) | false |

Machine table: `outputs/auto_research/mde_from_uncertainty_ladder.csv`.

Permutation and future-month negative-control checks are not in this file.
