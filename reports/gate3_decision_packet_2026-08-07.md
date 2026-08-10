# Gate 3 decision packet — CHD / HF thermal panel (amended; team freeze pending)

**Date:** 7 August 2026 (amended reanalysis)  
**Playbook:** 03  
**Status:** Packet ready — **Gate 3 not closed by agent alone**

## What changed since the morning packet

| Before | After |
|---|---|
| Joint P02/P04 treated as headline candidates | Joint P02/P04 retained as exploratory collinearity diagnostics |
| Diagnostics contaminated by synthetic stroke panel | Outcome-specific real diagnostics only (`n=132`, `synthetic=FALSE`) |
| Population × days as default interpretation | Amended core uses **days-only** offset (count ratios); pop×days retained as sensitivity |
| Model / HC1 SEs for narrative | Amended core inference: **Newey–West lag-6** |
| Abstract-ready joint IRRs | Claim ledger CVD-01…12 from separate exposures; **no primary freeze** |

SAP Amendment A1 documents the non-pre-outcome timing of these corrections.

## What was run

`PATHWAY_MODE=real OUTCOMES=chd,hf Rscript scripts/run_cvd_full_analysis.R`

Complete pathway panel (P01–P18 family + amended A IDs), HM/CM starter panel, descriptives, offset/period sensitivities, amended single-exposure robustness (scripts 31–32), disclosure-minimised release package (33), and fatal provenance checks (34; 9/9 PASS).

## Amended core reading (exploratory; not frozen)

Negative binomial; month factor; ns(time, 4); days-in-month offset; Newey–West lag-6.

| Outcome | Spec | Contrast | Count ratio (95% CI) | p | BH q |
|---|---|---|---|---|---|
| CHD | P04A | Hot nights / 5 days | 1.022 (1.002–1.042) | 0.032 | 0.192 |
| CHD | P01A / P02A / P02B | Continuous temperatures | ~0.993–0.994 | >0.32 | >0.64 |
| CHD | P04B / P04C | Cold / very hot days | ~0.995–0.999 | >0.82 | >0.89 |
| HF | P04B | Cold days / 5 days | 1.073 (1.006–1.144) | 0.031 | 0.192 |
| HF | P02B | mean_tmin / °C | 0.973 (0.947–1.000) | 0.050 | 0.202 |
| HF | P04A / P04C | Hot / very hot days | ~1.003 / 0.995 | >0.76 | >0.89 |

Qualitative panel pattern: **CHD more hot-night associated; HF more cold associated**. All twelve core q-values > 0.19.

## Why joint P04 is not the headline

Under the same amended offset and NW lag-6, joint CHD hot nights rose to **1.045 (1.015–1.075)** versus separate **1.022**. Residualised VIF for Tmax/Tmin ≈ 4.66. Joint models stay diagnostic.

## Residual dependence

CHD baseline Pearson residual ACF(1) ≈ 0.51 (Ljung–Box rejects white noise). HF ACF(1) ≈ 0.15. NW lag-6 and INGARCH sensitivities are required context, not optional polish.

## Required human decisions before headline freeze

1. Confirm inpatient ICD inclusion lists for CHD and HF with Roro.
2. Accept days-only count-ratio interpretation, or supply cohort-at-risk denominators.
3. Hogan: freeze weather / HM–CM reference rules (Playbook 01).
4. Decide whether any single contrast is confirmatory given q > 0.19 for the exploratory family.
5. Stroke file arrival and role relative to this CHD/HF paper.
6. Roro/Bishai confirmation before external submission (aggregates reduce disclosure risk; they do not grant publication authority).

## Outputs index

- Release package: `outputs/release_chd_hf/` (tables, figures, supplement, claim ledger, validation)
- Manuscript draft: `manuscript/chd_hf_thermal_associations_2013_2023.md`
- Supplement: `manuscript/chd_hf_supplement.md`
- Validation note: `outputs/reports/cvd_real_release_validation.md`
- Receipt: `reports/data_receipt_2026-08-07.md`
