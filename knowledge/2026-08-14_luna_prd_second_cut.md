# PRD field laboratory — Luna second cut

**Mode:** Explore. **Provenance for every new number:** `REAL_PUBLIC` — the
90-cell, 4,017-day Open-Meteo ERA5-Land Tmin/Tmax cache, 2013–2023. NumPy-only
analysis; no HA data or coefficients.

## Fragile versus robust

| Script 51 claim | Assessment |
|---|---|
| EOF1 = 92.1%; all loadings positive | **Robust as a grid mode.** Leave-one-year pattern r = 0.9989–0.9999; variance fraction = 0.9179–0.9228; all 11 holdouts retained positive loadings after sign alignment. Positivity is a sign convention, not physics. |
| EOF1–latitude r = +0.78; EOF1–HN r = −0.93 | **Robust descriptively.** Holdout ranges were +0.768–+0.791 and −0.926–−0.932. Both remain grid- and threshold-dependent associations. |
| Theil–Sen +0.29°C/decade; 23/90 intervals exclude 0 | **Fragile inferentially.** A 50,000-shuffle common year permutation gave minimum p = 0.0097, but Benjamini–Hochberg FDR 0.10 retained **0/90** cells. The original 120 year-resampling intervals ignore spatial dependence. This remains a window slope, not climate-change evidence. |
| Harmonic peak day 198–207 | **Robust, narrow morphology.** Circular mean phase: marine south 204.3 days (SD 2.66), Guangzhou 199.9 (SD 0.17), highland 200.5 (SD 1.35). Marine–Guangzhou differs by 4.4 days, more than one day, although all are mid-July. |
| P(HN\|VHD) marine 0.43 versus Guangzhou 0.03 | **Fragile as aggregated.** The marine 0.43 is the mean of eight marine cells with at least one VHD, not a pooled probability. Pooling all cell-days gives marine 0.314 versus Guangzhou 0.0377. |
| 2,428 edges at r > 0.90 | **Coherence is robust; novelty is not.** Removing EOF1 leaves 26 such edges. The network is largely a thresholded common mode, not an independent spatial discovery. |
| North separation with n_eff ≈ 425 | **Separation is robust; n_eff is heuristic.** PC1 lag-1 gives 425, but squared-PC lag-1 gives 609; the sampling formula is not justified by PC1 lag alone. Ten-day block bootstrap gap/lambda1 5th–95th percentile = 0.965–0.970. |
| k-means names marine/estuary/highland/inland | **Interpretive only.** Seed sensitivity was modest (pairwise co-membership agreement 0.948–1.000; median 0.988), but `name_clusters()` assigns names after fitting by HN and elevation. These are not physical regimes, municipalities, or catchments. |

## New dependence checks

With 1,000 moving-block bootstrap replicates (10-day blocks), EOF1 variance
fraction had median **0.9205**, 5th–95th percentile **0.9146–0.9258**
(full sample 0.9207). Persistence does not explain away 92%.

For compound extremes, pooled 2×2 odds ratios (HN: Tmin ≥28°C; VHD:
Tmax ≥33°C) were: marine south **OR 4.80**, Guangzhou **OR 318.2**; highland
had zero HN days, so its OR is not estimable. Daily de-seasoned Tmin–Tmax
Spearman correlations (cell medians) were marine **0.783**, Guangzhou **0.638**,
and highland **0.639**. These are exposure co-occurrence results, not health
effects.

Lag convention: correlate HQ(t) with Guangzhou(t + lag), so positive lag means
HQ leads. Correlations for lags −3…+3 were **0.295, 0.458, 0.700, 0.892,
0.762, 0.537, 0.358**. The maximum is at lag 0; neither cell leads.

## Bugs, overclaims, and dead ends

The area weight is reasonable for this regular narrow-latitude lattice; its
0.05 floor is inactive. The main issues are inferential: North’s `n_eff` is
not a covariance-effective sample size; year bootstrap intervals are not
multiple-testing control; and network edges repeat EOF1. The conditional
probability needs its denominator and pooling rule stated. A Gaussian copula
would add a model without improving the OR/Spearman answer, so it was not run.

**Hogan sentence:** On this grid, a 28°C night is a marine threshold event
carried on a persistent basin-wide Tmin pulse, not an inland Guangdong or
hospital event.
