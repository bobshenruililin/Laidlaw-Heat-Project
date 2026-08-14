# Did stronger models matter? — 14 August 2026

**Question:** Does GPT 5.6 Luna, 5.6 Sol, or the parent (Grok 4.6) change what we should believe, or only the prose?  
**Kimi k3:** not in the launch list; no substitute.

Residues: Luna [`2026-08-14_luna_prd_second_cut.md`](2026-08-14_luna_prd_second_cut.md); Sol [`2026-08-14_sol_strong_model_pass.md`](2026-08-14_sol_strong_model_pass.md); Grok [`2026-08-14_grok_prd_second_cut.md`](2026-08-14_grok_prd_second_cut.md). Runnable lock: `scripts/52_prd_strong_cut.py`.

## Comparison

| Claim | Luna | Grok 4.6 | Sol | Decision |
|---|---|---|---|---|
| EOF1 ≈ 92% is a fluke of persistence or one year | No. Holdout r ≥ 0.999; block-bootstrap 0.915–0.926 | Same numbers independently | n/a (programme arm) | **Robust.** Keep. |
| 23/90 Theil–Sen CIs are detections | **0/90** at BH 10%; permutation min p ≈ 0.01 | **0/90**; MK min p = 0.013 | Would kill pasting them as findings | **Fragile.** Headline dropped. |
| Harmonic phase locked to mid-July | Marine 204.3 vs GZ 199.9 (4.4 d) | Identical | n/a | **Robust.** |
| Network r>0.90 is a new object | After removing EOF1: **26** edges | Verified in script 52 | n/a | **Dead as a discovery.** Keep as a check. |
| P(HN\|VHD) marine 0.43 | Unweighted cell mean; **pooled 0.31** | Pooled 0.314; added reverse P(VHD\|HN) | n/a | **Fix pooling.** Reverse conditional is the inland sentence. |
| Field-page lede (“a human PhD…”) | n/a | Did not catch | **Kill.** Self-congratulatory | **Fixed** to Sol’s spare sentence. |
| 31 August packing | n/a | Did not pack | Failure mode = delaying Bishai | **Human:** send 2a + frozen essay now. Field lab is not the deadline. |

## Did stronger models matter?

**Yes, on two axes.**

1. **Climate (Luna ≈ Grok).** The weak first pass already had the EOF story right. The strong cut changed the *trend* headline and the *network* claim. Luna additionally caught the unweighted vs pooled P(HN|VHD) and the residual-edge count. Grok additionally wrote the reverse conditional (inland hot nights are almost always hot days). Agreement on the FDR zero is the evidence that the model swap was not just longer prose.

2. **Programme (Sol).** A climate-stronger model does not move 31 August. Sol’s kill list was the difference: the PhD-flex lede, the “travels up the Pearl” causal verb, the garden metaphor, and the reminder that Bishai’s signature is the only serial human dependency. Worksheet/checklist needed no date correction.

**No, on Kimi k3.** It could not be launched here. Last week’s Kimi harvest already lives in `2026-08-13_kimi_web_weather_lit_harvest.md`.

## What was not a difference

EOF1 remaining ~92% after holdout and block bootstrap. Lag-0 HQ–Guangzhou. Mid-July phase. Frozen PDFs. Logos as print overlay.
