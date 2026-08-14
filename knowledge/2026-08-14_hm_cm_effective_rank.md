# First-wave HM/CM effective rank — 14 August 2026

**Mode:** Ship. Hogan lock gift. Not a Bishai object.  
**Provenance:** `REAL` flags in `data_processed/hm_cm_month_flags_2013_2023.csv` (132 months).  
**Not:** a licence to refit the catalogue, a health finding, or Gate 3.

Rebuild: `python3 scripts/58_hm_cm_effective_rank.py`.  
Tests: `python3 scripts/test_58_hm_cm_effective_rank.py`.

## Punchline

The on-disk file is **twelve** named binaries plus HM23 event starts, **not** 98 tests. CM05 is all zeros. Eleven live flags have correlation-matrix participation ratio **3.92**. PC1+PC2 hold **67%**. Heat never co-fires with cold (max Jaccard 0).

Nested (strict inner ⊂ outer): HM15 ⊂ HM08 ⊂ HM32; HM17, HM19, HM23 ⊂ HM32; CM08 ⊂ CM03; CM15 ⊂ CM30. An inner flag is not an independent sensitivity.

HM23 event starts: 30 months with a start, 38 starts in total, at most 3 in a month. Excluded from the binary rank because it is a count.

## Why this exists

An unlocked catalogue can look like 98 independent tests. The fitted first-wave set is about four effective dimensions and two orthogonal seasons. Adding the next ID is not a new test unless it leaves this span. Do not reopen the outcome panel because the rank is small.

Figure: `figures/hm_cm_rank/hm_cm_scree.svg`.
