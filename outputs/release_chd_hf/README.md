# CHD/HF manuscript release package

This directory contains disclosure-minimised aggregate tables and figures for the internal manuscript draft.

- Outcomes: first hospitalisation after a CHD or HF diagnosis record among people with T2D and/or HTN.
- Main model: separate exposure, negative binomial, month factor, natural spline of time (4 df), days-in-month offset.
- Inference: Newey-West lag-6 confidence intervals.
- All health inputs used for this package carry `HA_APPROVED_AGGREGATE`.
- No source monthly HA count file or merged health panel is included.
- External submission still requires team dissemination confirmation.

## Final augmentation (script 38)

- Tables 1–3 and Figures 1–4 are unchanged from the script-33 analysis of record.
- Table 4 (`tables/table4_uncertainty_ladder.csv`) shows Model/HC1/NW3/NW6 for the 12 core contrasts.
- Figure 5 (`figures/figure5_se_method_ladder.*`) is the SE-method ladder forest.
- `tables/analysis_availability.csv` records ensemble, prediction, and M|D blockers as non-completed analyses.
- `tables/claim_ledger_v2.csv` extends the existing claim ledger with claim tier,
  post-outcome, multiplicity, and SE context. No new real claims were added without real outputs.
- `supplement/methods_feasibility/` holds public weather audits and
  `SYNTHETIC_CALIBRATION` method-validation materials only.
- Calibration outputs are never health findings for CHD/HF.
- Health provenance remains `HA_APPROVED_AGGREGATE` (never renamed to REAL).

See `RELEASE_INDEX.md` for the file map.
