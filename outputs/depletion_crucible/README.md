# Depletion crucible — absorbing risk set versus a days-in-month offset

**Date:** 2026-08-14
**Mode:** Explore (no new health models)
**Parent memo:** `knowledge/crucible_agent_beta_depletion.md`

This folder contains no governed CHD/HF counts. It asks what an absorbing
first-event risk set does to a log-link monthly count model that offsets
`log(days_in_month)` instead of still-at-risk person-time (assumption `A48`).

Provenance of every column is carried in the tables:

| Label | Meaning |
|---|---|
| `REAL` | Public HKO monthly climate, 2013-01..2023-12 |
| `HA_APPROVED_AGGREGATE` | Approved annual first-event totals and released scenario coefficients |
| `ILLUSTRATIVE_ALGEBRA` | Monotone log-risk-set shapes used only to evaluate a projection; no cohort size, inflow rate, or HA row count is asserted |

## Files

| File | Question |
|---|---|
| `count_weighted_information.csv` | Where does each exposure's identifying variance sit, once weighted by the risk-set-scale proxy that drives Fisher information? |
| `depletion_path_absorption.csv` | How much of a depletion path does `month FE + ns(time,4)` remove? |
| `omitted_logr_bias.csv` | If `log R_t` is omitted, what bias transfers to each exposure's reporting step? |
| `interaction_absorption.csv` | Can the control space represent a depletion path *interacted* with an exposure? |
| `riskset_fatness_ladder.csv` | Already-paid scenario coefficients placed against the mean monthly approved count of their estimation window. |
| `riskset_fatness_ladder_stats.csv` | Rank association between window risk-set fatness and \|log RR\|, all twelve core contrasts. |
| `covid_kink_amplitude_inversion.csv` | What non-smooth care-seeking amplitude reproduces the already-paid `covid_phase_adjusted` coefficient shift? |
| `annual_trend_collinearity.csv` | Annual correlation between each exposure and the depleting approved count series. |
| `depletion_summary.json` | Headline quantities plus provenance flags. |

## Rebuild

```bash
python3 scripts/49_depletion_crucible.py
python3 scripts/test_49_depletion_crucible.py
```

## What these tables do not license

They produce no corrected coefficient, no incidence rate, no cohort size, and no
person-time denominator. The amplitude inversion returns a care-seeking
amplitude implied by a released coefficient shift; it is not a repaired
estimate. Sister folder `outputs/identification_crucible/` holds the
residual-variation and multiplicity diagnostics.
