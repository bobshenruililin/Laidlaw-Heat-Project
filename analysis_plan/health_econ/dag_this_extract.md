# DAG sketch — this extract (teaching, not a finding)

**Provenance:** `SYNTHETIC_THEORY` / methods teaching. Not estimated. Not Gate 3.

Nodes are coarse on purpose. The design is a **selected** diagnosed T2D/HTN population observed as **territory-month counts**, not a person-level claims DiD.

```
Seasonality / calendar month ──► official-day counts (hot nights, cold days, very hot days)
                              └─► first-hospitalisation counts

Secular trend / COVID era ──► care-seeking and coding ──► counts
                           └─► weather anomalies (selection of years)

Unobserved frailty / housing / indoor T ──► counts
                                         └─► (unmeasured; not in this file)

Relative humidity, rainfall ──► counts (Model 2; specified, not fitted)
Pollution, flu (121/132 months) ──► counts (sensitivities; flu never zero-filled)

Diagnosed T2D/HTN cohort ──► at-risk set (person-time **absent**) ──► counts
```

## Colliders and selection

- **Entering the cohort** requires a diabetes or hypertension diagnosis and subsequent CHD/HF diagnosis. Conditioning on diagnosis can open paths through health-care use.
- **Hospitalisation as the event** is not community incidence. Heat and cold may change both biology and the decision to present.

## Bad controls (do not add blindly)

- Variables affected by the same month’s heat that also affect admission (for example indoor cooling behaviour) are not in the file and must not be invented.
- Zero-filling flu for the 11 missing months is already forbidden (A-series: flu covers 121/132).

## What staggered DiD would have required

A treatment date, a control series, and a parallel-trends story. This panel has **weather variation within calendar month across years**, not a policy rollout. Callaway & Sant'Anna is the wrong default estimator.

## Falsification ideas that do not need new HA rows

1. Use already-published pre-2020 intervals (do not re-fit without panels).
2. Use already-published spline-df 8 interval that includes 1 for HF cold days.
3. Placebo *calendar* structure: the month factor is the seasonality control; do not interpret residual season as a heatwave duration.
