# Manuscript scaffold — Methods outline for pathway panel paper

**Status:** Scaffold only. No real outcome coefficients.  
**Working title (provisional):** Monthly thermal extremes and stroke admission aggregates in Hong Kong, 2013–2023: a multi-specification analysis

---

## 1. Design

Ecological monthly time series, January 2013–December 2023 (N = 132 months). Unit of analysis: territory-month or month × age × sex, depending on the Hospital Authority aggregate grain.

## 2. Outcome

Stroke admission aggregates supplied under approved transfer. Pooled stroke is default; ischemic vs hemorrhagic modelled separately only if subtype fields exist (pathway P13). General HA files lacking admission reasons are not used for AMI endpoints.

## 3. Exposures

Hong Kong Observatory Headquarters daily series aggregated to months:

- Continuous mean / Tmax / Tmin and lag-1 month
- Official extreme-day counts (hot nights, very hot days, cold days)
- Ren/Wang-style spell and 2D3N burden metrics
- Heatwave-month indicators (study-period percentile and spell collapses)

Pollution: EPD EPIC monthly general-station means (NO₂, O₃, PM₂.₅, PM₁₀), entered in staged models.

## 4. Denominators and offset

C&SD mid-year age–sex population (Table 110-01001), linearly interpolated to months. Offset: `log(population × days_in_month)`.

## 5. Statistical approach

Negative binomial count models with calendar-month factors and natural spline in time. Cluster-robust standard errors by month when stratified. Results reported as a **labelled pathway panel** (P01–P16); one headline pair frozen at Gate 3 (proposal: P02 + P04).

## 6. What we will not claim

- Individual-level causality
- Equivalence to daily DLNM triggering estimates
- Equivalence to heatwave excess-death counts from mortality studies
- AMI findings from extracts without admission reasons

## 7. Reproducibility

`Rscript scripts/run_pathway_pipeline.R` (dev) or `PATHWAY_MODE=real Rscript scripts/run_pathway_pipeline.R` after placing aggregates in `data_raw/ha_secure_placeholder/`.
