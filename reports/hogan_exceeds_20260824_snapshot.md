# Hogan Word+PDF vs 24 August snapshot

**Date:** 2 September 2026 (S9 restore). First exceed recorded 31 August 2026.  
**Snapshot:** Bob Desktop `Heat_CVD_Manuscript_20260824_hogan.pdf` (upload SHA-256 prefix `b172ed31659d6cd6`, 14 pages, 679 857 bytes).  
**Current attachable files:**

| File | SHA-256 prefix | Size | Pages |
|---|---|---|---|
| `manuscript/live_collaborative/Heat_CVD_Manuscript_20260824_hogan.pdf` | `306e084824de6b0e` | 868 629 | 22 |
| `manuscript/live_collaborative/Heat_CVD_Manuscript_20260824_hogan.docx` | `afff1fcc7b079e1f` | 792 210 | — |

Verified by `tests/test_hogan_exceeds_20260824_snapshot.py`, `tests/test_hogan_methods_rewrite.py`, `tests/test_storm_physio_hhap.py`, `tests/test_hhap_companion_2026-09-02.py`, and `scripts/71_objective_audit_tripwires.py`. Claim-ledger auditor 161/0.

This is not a Gate 3 freeze. Model 2/3 remain specified and unfitted. Table 2 remains Model 1.

## Scorecard

| Dimension | 24 Aug snapshot | Current Word+PDF | Result |
|---|---|---|---|
| Model 1 numbers (CHD hot nights 1.022; HF cold days 1.073; *q* min 0.192) | Present | Unchanged | Equal (required) |
| Event counts (CHD 156,156; HF 29,681; 132 months) | Present | Unchanged | Equal (required) |
| Hogan HKO sentences (`HOGAN_OPEN`, `HOGAN_AVG`) | Verbatim | Verbatim | Equal (required) |
| Ethics placeholder / Acknowledgements | `UW XX-XXX`; `None.` | Same | Equal (required) |
| Models 1/2/3 named; Table 2 = Model 1 | Yes | Yes | Equal (required) |
| `housing` / `medication` in Hogan PDF | Absent | Absent | Equal (required) |
| Print: Table 1, Table 2, Table 3, Figures 1–3 each on their own page | Table 1 shares with Figure 1; Table 2 shares with Table 3; Figure 3 shares with Discussion | Six separate pages | Exceeds |
| Figure 3 identification | Caption: all twelve Model 1 fits across nine specifications | Official-count forest; per-five-day scale; 3/6/8-df labelled as spline df not duration; S6 for continuous T | Exceeds |
| Named 6-df robustness | Absent | Named; 8-df opens HF cold days onto 1 | Exceeds |
| Consecutive-days guardrail | Absent | Reporting scale, not a consecutive-day trigger; warnings not evaluated | Exceeds |
| Night/CHD physiology | Absent | Hypothesis; indoor T unmeasured | Exceeds |
| HF/cold physiology | Absent | Haemodynamic hypothesis; Goggins neighbour not imported | Exceeds |
| WHO 2026 × HK instruments | Absent | Mapping only; Prolonged Heat Special Alert; no admissions averted | Exceeds |
| Supplementary Table S9 in Discussion | Absent from 24 Aug snapshot body | Restored 2 Sep (archive P11; not core-adjusted) | Exceeds |
| Discussion close (Liu, pollution, contribution, Conclusion) | Complete on 14 pages | Complete on 22 pages (no truncated Discussion) | Exceeds |
| References 23–33 (Chevance through HAD shelters) | Absent | Present | Exceeds |
| Hogan-facing Word comments | Not scored on the PDF | No paste / circulate / pipeline / Rscript | Exceeds |
| Orphan nearly-empty text pages | None | None (layout assert `<220` chars unless a table/figure page) | Equal |
| Page count | 14 (floats packed) | 22 (floats unpacked + added Discussion) | Longer because of print contract and added science, not padding |
| Gate 3 / Model 2/3 health coefficients | Open / unfitted | Open / unfitted | Equal (honest) |

## What was not claimed

No new Hospital Authority coefficients. No IRB number. No stroke series. No evaluation of VHWW, Cold Weather Warning, or HHAP. No 5-day consecutive trigger.
