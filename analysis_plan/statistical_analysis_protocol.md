# Statistical Analysis Protocol (SAP) — monthly stroke × thermal panel

**Version:** 1.0 · **Date:** 2026-07-21  
**Study:** Thermal extremes and stroke admission aggregates, Hong Kong, 2013–2023  
**Status:** Pre-outcome freeze. Real coefficients forbidden until Gates 1–2 close; headline claim after Gate 3.

This SAP is the scientist-facing contract for the executable pathway panel (`analysis_plan/pathway_registry.yml`, `scripts/20_fit_pathway_panel.R`).

---

## 1. Scientific question

Among Hong Kong residents (age ≥35 unless the aggregate grain differs), how do **monthly** thermal exposures — continuous temperature, official extreme-day counts, Ren/Wang spell / 2D3N burden, and multi-definition heatwave-month indicators — associate with **stroke admission aggregates**, and how stable are associations across a pre-labelled panel of specifications?

**Estimand class:** ecological monthly burden associations (rate ratios from count models with population×days offset).  
**Not estimands:** daily DLNM triggering; heatwave excess deaths; individual causality; AMI from files without admission reasons.

---

## 2. Data contracts

| Layer | Source | Contract |
|---|---|---|
| Outcome | HA stroke aggregates (pending) | `schemas/ha_stroke_aggregate.schema.json` |
| Climate | HKO Headquarters daily → monthly | `climate_monthly_2013_2023.csv` + lag-1 via Dec 2012 |
| Pollution | EPD EPIC monthly general means | NO₂, O₃, PM₂.₅, PM₁₀ |
| Denominator | C&SD Table 110-01001 | Age–sex mid-year → monthly interpolation |
| Flu | CHP Flu Express monthly positivity | Optional P14; incomplete early-2013 |
| Holidays | Deterministic scaffold v2 | Sensitivity only until gazette scrape |

Provenance labels (`REAL`, `SYNTHETIC`, `HA_APPROVED_AGGREGATE`, …) travel with every row.

---

## 3. Primary and secondary pathways

**Headline proposal (Gate 3 default):** **P02** (same-month Tmax + Tmin) and **P04** (official extreme-day counts, scaled per 5 days).

| Tier | IDs | Role |
|---|---|---|
| Core continuous | P01–P03 | Classical Tmean / Tmax–Tmin / lag-1 |
| Extremes & heatwaves | P04–P07 | HKO counts; spells; 2D3N; multi-def HW-month |
| Cold | P08, P18 | Cold-day / cold-spell; cold-month indicator |
| Structure | P09, P17 | Age band; sex stratum |
| Confounding ladder | P10–P12, P14 | COVID/holidays; pollution staged; AH; flu |
| Subtype | P13 | Enable only if IS/HS present |
| Sensitivity | P15–P16 | Temperature variability proxy; pre-COVID window |

All estimates carry `pathway_id`. Report as one **panel**, not ten discoveries.

---

## 4. Model form (prespecified)

For each enabled pathway:

\[
\log \mathbb{E}[Y_{t,s}] = \beta' X_t + \gamma_{\text{month}} + ns(\text{time}, df=4) + \text{stratum terms} + \log(N_{t,s} \cdot D_t)
\]

- Family: negative binomial (`MASS::glm.nb`); quasi-Poisson fallback on NB failure.
- \(Y\): stroke event counts; \(N\): population; \(D\): days in month.
- Seasonality: calendar-month factor; trend: natural spline df = 4 (config).
- Stratified grain: add age_group + sex; cluster-robust SEs by `month_id` (HC1 / `vcovCL`).
- Territory grain: HC1 robust SEs.
- Effect measure: incidence rate ratio (exp(β)) with 95% CI.

**Pollution staging (P11):** none → NO₂ → PM₂.₅ → O₃ → multi. Interpret attenuation carefully (especially O₃–heat collinearity).

**Flu (P14):** complete-case on months with non-missing `flu_indicator` (document early-2013 gap).

---

## 5. Multiplicity and honesty

1. Panel reporting is the multiplicity strategy — not Bonferroni-hunting across pathways.
2. Gate 3 freezes the headline pair **after** real descriptives, before primary claims.
3. Synthetic dry-runs prove plumbing only; coefficients labelled `SYNTHETIC` are never findings.
4. Monthly coefficients must not be equated to daily DLNM or mortality excess-death estimates.

---

## 6. Analysis sequence when data arrive

1. Place approved CSV in `data_raw/ha_secure_placeholder/`.
2. `PATHWAY_MODE=real Rscript scripts/run_pathway_pipeline.R`
3. Review `outputs/reports/stroke_data_qc_receipt.md` (Gate 2).
4. Descriptives + pathway panel + forest + diagnostics.
5. Gate 3 freeze note in assumption ledger.
6. Manuscript tables from `scripts/22_make_pathway_manuscript_tables.R` (already chained).

---

## 7. Software

R (≥4.x): `MASS`, `splines`, `sandwich`, `lmtest`, `dplyr`, `yaml`. Orchestrator: `scripts/run_pathway_pipeline.R`.

---

## 8. Amendments

Amendments after Gate 3 require a dated ledger entry and a new pathway ID (do not silently redefine P02/P04).
