# Adversarial audit — COVID-period angle (10 September 2026)

**Auditor:** Grok 4.6 on this extract. Sol 5.6 Max was quota-blocked. Not a finding. Gate 3 open.

## 1. What Hogan’s sentence can and cannot mean

**Can mean (file-supported):**

- Pre-2020 cold-day count ratios are larger than the 132-month estimates (HF 1.113 vs 1.073; CHD 1.036 excludes 1 only before 2020).
- First-event **counts** fell, including a 2020 dip.
- Thermal Table 2 is a poor headline if the interesting structure is **window dependence**.

**Cannot mean (without new data or a new freeze):**

- Cold days **improved** hearts after COVID (physiology).
- A post-2020 CR below 1 for official cold days (HF full-sample interval still excludes 1 on the high side).
- Labs, person-time, or admission cause.
- Weather proven irrelevant. Official hot nights rose across the window; CHD hot nights **need** 2020–2023.

## 2. Three rival stories (monthly NB, not TWFE)

Shared skeleton:

\[
\log \mathrm{E}(Y_t)=\log d_t+\alpha+\beta X_t+\sum_{m=2}^{12}\gamma_m I(\mathrm{month}_t=m)+s(t;4).
\]

**S1. Constant \(\beta\), utilisation shock.** \(Y_t\) is scaled by an unobserved \(u_t<1\) after 2020. Period-split \(\hat\beta\) can move even if \(\beta\) is constant. SYNTHETIC Monte Carlo: `scripts/72_synthetic_utilisation_shock.py`.

**S2. Depletion.** The first-event risk set shrinks. Days-in-month \(d_t\) is not person-time. \(\hat\beta\) is a count ratio, not an incidence-rate ratio.

**S3. Weather as time-varying \(X_t\).** Official extremes are not constant. A heat residual that appears only when 2020–2023 is included is entangled with the years when nights peaked and care-seeking changed (already in the parked Discussion).

A stacked interaction \(X_t\times I(t\ge 2020)\) would be a **new** labelled sensitivity, not a confirmatory primary, and is not fitted here.

## 3. How each fails

| Shock | What breaks |
|---|---|
| Missing person-time | All three. Cannot separate incidence from depletion. |
| Unobserved utilisation | S1 is observationally similar to a smaller \(\beta\). Xin 2022 is the local neighbour (counts down, deaths up). |
| Cohort selection (diagnosed T2D/HTN) | The sample is already selected. COVID may change who reaches a first recorded hospitalisation. |
| 48-month post-only fit | Month factors + 4-df spline on 48 points is thin. Do not mint Table 2. |

## 4. What a weather-falsification exhibit can honestly show

It can show: the **same** official-day encoding, under the **same** Model 1 skeleton, yields window-dependent CRs; mean temperature and official days are not interchangeable (pre-2020 mean T CRs for CHD/HF sit below 1). It cannot show: “weather is not the reason” as a proof. That would require a decomposition we do not have (person-time, utilisation, cause of admission).

## 5. Kill list (never promote)

Physiological improvement from a count drop; TWFE/Callaway/Medicaid; QALY/cartel/nudge; labs from outdoor T; post-only confirmatory primary; admissions averted; React dashboard as the paper; synthetic Monte Carlo as a Hong Kong result.

## 6. Night-cycle follow-up (read-only audit, then patched)

Independent Grok read: forbidden-phrase PASS; Hogan weather character-identical; CR numerals match NW6 rounding. Gaps closed here: 2020 dips and C&SD 17% entered the claim ledger; *q* = 0.192 attached to both CHD hot nights and HF cold days; literature memo first authors corrected (Wai, not Hung/Wong, on those two DOIs). X-and-Y MNAR added to `scripts/73_synthetic_mnar_selection.py`. Still not a finding.
