# Cycle 1–2 Monte Carlo report — SYNTHETIC_CALIBRATION

**Engine:** Python Poisson GLM, month FE + `cr(time, 4)` + exposure + `log(days)` offset.  
R twin `scripts/48_health_econ_monte_carlo.R` is the MASS::glm.nb version for machines with R.  
**Seed:** 20260814. **Reps:** 200. **Rows:** 9000. **Scenarios:** 45.  
**Exposures:** `REAL_PUBLIC_HKO`. **Counts:** synthetic. **HA microdata:** not read.  
**Monetisation:** forbidden. **Gate 3:** not an input.

## Gates (not findings)

| Object | Statistic | Result | Disposition |
|---|---|---|---|
| HE-01 | Empirical size of \(H_0:\theta=0\) | 0.05 overall; kink-2020 0.07 | Size is nominal. **Level** of the stock remains KILL. Costing caveat only. |
| HE-03 | Median relative attenuation | 0.44–0.55 at \(u\in\{0.85,0.95,0.99\}\) | Cycle 1 “washes out in months” **fails** in this DGP. \(\lambda\) still unidentified. |
| HE-05 | Size at \(\phi=0\) / power at \(\phi=0.6\) | 0.345 / 0.675 | Power above 0.5 is uninterpretable because size is inflated. KILL confirmed. |
| HE-07 | SEW / Pr(\(\varepsilon_Y>0\)) | 1.57 / 0.21 | Lower-bound reading **fails**. Observed elasticity can change sign under threshold movement. |
| HE-08 | RTE p95 under true invariance / power at \(\Delta=\log 1.03\) | 0.122 / 0.45 | Size 0.41 when \(\Delta=0\). Transportability **fails**. Binary split is noisy and anti-conservative. |
| HE-10 | ADR p95 (base mean / select / overall) | 0.24 / 1.05 / 0.93 | Cosmetic **only** for the imposed reversed-J on monthly means. Selection stress fails the gate. Not M\|D recovery. |
| HE-C2-10 | Signed CATD 5–95 | +0.19 to +0.44 | No sign flip on this factorial. Distortion same-signed; coverage of \(\beta_{\mathrm{target}}\) collapses. Cancellation region not hit for this \(g\). |
| HE-C2-02 | Dispersion slope demand vs queue | −0.0008 vs −0.0070 | Second-moment gap in the predicted direction. Detection candidate, not a shadow price. |

## Climate-only (not health)

HKO Headquarters daily \(T_{\mathrm{mean}}\), 132 months: OLS \(\varsigma=\partial s^2/\partial\bar T = -0.438\) (\(R^2=0.39\)). Negative variance gradient, as a subtropical year should show. `REAL_PUBLIC_HKO`.

Noiseless aggregation vs representative-day slopes under the imposed reversed-J: \(\beta_{\mathrm{agg}}=-0.036\), \(\beta_{\mathrm{rep}}=-0.031\). Small index-number gap relative to the HF cold-day interval width (~0.129); the gap is not small relative to the CHD hot-night interval width (~0.039).

## Theory helpers (dimensionless)

- HE-04 SYNTHETIC tree: proceed beats wait under the stated knobs; person-time claim-set bonus equals the IRR bonus by construction. Still KILL as an estimated parameter.
- HE-C2-04: reversal set nonempty for the back-loaded-wait ordering at \(\beta\le 0.8\). Gate 3 / SAP commitment incomplete (`costly_to_revoke` is human-owned). This cycle is cheap talk.
- HE-C2-PORT: only singleton flip is comparable monthly private volumes → public share. \(\lambda\) unflipped even under the full bundle. Does not assert those files exist.

## Cycle 3 (seeds, not run)

Stochastic volatility of \(\varsigma\); endogenous diagnosis timing (risk-set entry as a health-system output); dual-agency mechanism design; Knightian max-min over \(g\).

Do not revive naive cost-of-illness, nudges, M\|D, or stroke economics.
