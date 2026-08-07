# CHD/HF manuscript release package

This directory contains disclosure-minimised aggregate tables and figures for the internal manuscript draft.

- Outcomes: first hospitalisation after a CHD or HF diagnosis record among people with T2D and/or HTN.
- Main model: separate exposure, negative binomial, month factor, natural spline of time (4 df), days-in-month offset.
- Inference: Newey-West lag-6 confidence intervals.
- All health inputs used for this package carry `HA_APPROVED_AGGREGATE`.
- No source monthly HA count file or merged health panel is included.
- External submission still requires team dissemination confirmation.
