# Identification crucible — public-climate diagnostics

**Date:** 2026-08-14  
**Mode:** Explore (no new health models)  
**Provenance:** `REAL` HKO monthly climate + already-paid `HA_APPROVED_AGGREGATE` coefficients.

This folder does **not** contain governed CHD/HF counts. It answers a linear-algebra question: after calendar-month indicators and a 4-df time spline, how much independent thermal variation remains, and what Gate 3 claims that residual variation can license.

Rebuild:

```bash
python3 scripts/48_identification_crucible.py
python3 scripts/test_48_identification_crucible.py
```

Parent remainder: `reports/identification_crucible_2026-08-14.md`.  
Audit: `knowledge/crucible_adversarial_audit.md`.
