# Engine state checkpoint — health-economics laboratory

**Time:** 2026-08-14 ~22:05 UTC.  
**Mode:** Explore. **This is a checkpoint, not a scientific conclusion.**

| Cycle | Status |
|---|---|
| 1 hypotheses | written (HE-01–HE-12) |
| 1 adversarial audit | 7 KILL / 2 PARK / 3 SURVIVE-TO-ESCALATION |
| 1 structural equations | written |
| 1 Monte Carlo | **200 reps, 45 scenarios, 9000 rows** (`outputs/health_econ/`) |
| 2 mutations | written (HE-C2-*) |
| 2 CATD / queue / PORT / reversal | run |
| UI | `docs/health_econ/` React + D3, gates synced |
| Cycle 3 | seeds only |

## Checkpoint numbers (SYNTHETIC_CALIBRATION)

- HE-01 size 0.05 → costing caveat, stock **level** still KILL
- HE-03 median attenuation ~0.53 → “washes out” claim fails in this DGP; λ still unidentified
- HE-05 size at φ=0 is 0.345 → KILL confirmed
- HE-07 SEW 1.57, Pr(ε_Y>0)=0.21 → lower bound fails
- HE-08 RTE p95 0.122 under invariance, power 0.45 at Δ=log 1.03 → transportability fails
- HE-10 base-mean ADR p95 0.24 (cosmetic); select family 1.05 (fails)
- HE-C2-10 CATD +0.19..+0.44, no sign flip on this factorial
- ς = −0.438 (REAL_PUBLIC_HKO climate)

Next loop: stochastic ς in HE-C2-10, then endogenous diagnosis timing. Do not revive COI / nudges / M|D / stroke economics.
