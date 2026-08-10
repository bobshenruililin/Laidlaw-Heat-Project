# Independent review reconciliation — CHD/HF amended release

**Date:** 7 August 2026  
**Reviewers:** two independent Grok agents (numerical re-fit; SAP/manuscript consistency)

## Verdict

Both reviews: **all checks PASS**. One cosmetic fix applied (HF monthly mean 225 → 224.9 to match Table 1).

## Numerical re-fit

| Model | Independent NW6 count ratio (95% CI) | Table 2 |
|---|---|---|
| CHD hot nights / 5 | 1.021824 (1.001854–1.042193) | exact match |
| HF cold days / 5 | 1.072800 (1.006454–1.143520) | exact match |

Claim ledger matches Table 2; BH q-values reproduce `p.adjust(..., "BH")`. Release validation 9/9 PASS; no SYNTHETIC provenance in release package.

## Consistency

Estimand, days-only offset, NW lag-6, separate vs joint roles, open Gate 3, no stroke claims, and dissemination boundary are aligned across SAP A1, Gate 3 packet, knowledge note, and manuscript.

## Residual note retained

CHD Pearson residual ACF(1) ≈ 0.51 under baseline NB; manuscript correctly keeps Newey–West lag-6 as primary uncertainty and reports INGARCH sensitivity.
