# M|D calibration F1.2 decision report

- Raw source: F1.1 500-rep raw metrics at /workspace/outputs/calibration_md/md_calibration_raw_metrics.csv (untouched; n_rows=105000)
- Protocol amendment: F1.2 (worst-cell gates; admissible M|D; comparator noncomparability)
- Admission decision: FAIL_METHODS_FEASIBILITY_ONLY
- All gates passed: FALSE
- Provenance: SYNTHETIC_CALIBRATION

## Gate table

| gate_id | passed | value | detail |
| --- | --- | --- | --- |
| convergence_min | TRUE | 1 | min_core_convergence=1.0000 (need >=0.95); failing=none |
| type1_range | FALSE | 0.15 | null_type1 min=0.0480 max=0.1500 (need [0.03, 0.08]); failing=CORE_05,CORE_06,CORE_19,CORE_20,CORE_21,CORE_22,CORE_23,CORE_24 |
| coverage_min | FALSE | 0.84 | min_core_coverage=0.8400 (need >=0.90); failing=CORE_05,CORE_11,CORE_12,CORE_18,CORE_19,CORE_20,CORE_21,CORE_22,CORE_23,CORE_25,CORE_26,CORE_27,...(+7) |
| relative_bias_max | FALSE | 32.77 | max_nonnull_abs_rel_bias=32.7742 (need <=0.20); failing=CORE_07,CORE_08,CORE_09,CORE_10,CORE_11,CORE_12,CORE_13,CORE_14,CORE_15,CORE_16,CORE_17,CORE_18,...(+12) |
| false_sign_max | FALSE | 0.808 | max_moderate_false_sign=0.8080 (need <=0.10); failing=CORE_13,CORE_14,CORE_15,CORE_16,CORE_17,CORE_18,CORE_31,CORE_32,CORE_33,CORE_34,CORE_35,CORE_36 |
| hessian_condition_max | TRUE | 1822 | max_core_hessian_cond_median=1.82e+03 (need <1e+08); failing=none |
| divergent_fit_max | TRUE | 0 | max_core_divergent_rate=0.0000 (need <0.05); failing=none |
| stress_coverage_min | FALSE | 0.842 | min_stress_coverage=0.8420 (need >=0.85; stress=AR-on core + EDGE_depletion/covid/stress); failing=CORE_34 |

## Per-cell null Type I and coverage (M|D core)

| scenario_id | outcome | kernel | AR | type1 | coverage |
| --- | --- | --- | --- | --- | --- |
| CORE_01 | chd | same_day | none | 0.0480 | 0.9520 |
| CORE_02 | chd | same_day | outcome_matched | 0.0500 | 0.9500 |
| CORE_03 | chd | cumulative_0_5 | none | 0.0580 | 0.9420 |
| CORE_04 | chd | cumulative_0_5 | outcome_matched | 0.0720 | 0.9280 |
| CORE_05 | chd | cumulative_0_21 | none | 0.1180 | 0.8820 |
| CORE_06 | chd | cumulative_0_21 | outcome_matched | 0.1000 | 0.9000 |
| CORE_19 | hf | same_day | none | 0.1500 | 0.8500 |
| CORE_20 | hf | same_day | outcome_matched | 0.1480 | 0.8520 |
| CORE_21 | hf | cumulative_0_5 | none | 0.1360 | 0.8640 |
| CORE_22 | hf | cumulative_0_5 | outcome_matched | 0.1420 | 0.8580 |
| CORE_23 | hf | cumulative_0_21 | none | 0.1020 | 0.8980 |
| CORE_24 | hf | cumulative_0_21 | outcome_matched | 0.0860 | 0.9140 |

Null Type I range: CHD/HF pooled min=0.0480 max=0.1500
Null coverage range: min=0.8500 max=0.9520

## Binding non-null diagnostics (core M|D)

- Max abs relative bias (non-null): 32.7742
- Max false-sign (moderate): 0.8080

Final decision must remain methods-feasibility only unless every F1.2 gate passes.

