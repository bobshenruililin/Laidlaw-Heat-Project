# Final integrated CHD/HF reanalysis — durable handoff

**Date:** 10 August 2026  
**Mode:** Ship + Explore + Decide (agent decisions only; human gates remain open)  
**Branch:** `cursor/cns-integrated-final-1754`

## Why this entry exists

Bob asked for a first-principles, CNS-calibre integrated report using the direct
email chain, the revised group heatwave-mortality manuscript, the governed
CHD/HF release, and the full analysis exchange. The work produced a
supervisor-facing report and a journal-facing manuscript, but did not
manufacture a Cell/Nature/Science-level biological claim from exploratory
monthly aggregates.

## Direct evidence added

- The supplied 21 April–6 August email thread confirms the T2D/HTN cohort,
  absent admission cause, proposed daily-weather/monthly-health framing,
  collaborator roles, CHD/HF delivery, and missing stroke attachment.
- The two supplied revised mortality-manuscript PDFs were byte-identical. They
  are private audit sources, not citable replacements for medRxiv v1.
- The redacted scientific contract is
  `knowledge/2026-08-10_correspondence_scientific_contract.md`.
- The revised mortality audit is
  `literature/roro_revised_manuscript_audit_2026-08-10.md`.

Raw correspondence and private PDFs were not committed.

## Analysis of record

Outcome: territory-month counts of the first recorded hospitalisation after a
first CHD or HF diagnosis record among people diagnosed with T2D and/or HTN
during 2013–2023. Admission cause is not recorded. The `*_inpatient` labels
still require semantic confirmation. Stroke was not delivered.

The continuity model is separate-exposure negative binomial with
calendar-month factors, `ns(time,4)`, and a days-in-month offset. It estimates
monthly count ratios, not cohort incidence.

Key exploratory estimates:

- CHD hot nights / 5: 1.022; Model 0.995–1.049; HC1 0.997–1.047;
  NW3 1.0003–1.0439; NW6 1.002–1.042; BH q = 0.192.
- HF cold days / 5: 1.073; Model 1.023–1.125; HC1 1.011–1.138;
  NW3 1.007–1.143; NW6 1.006–1.144; BH q = 0.192.

All twelve core q-values exceed 0.19. CHD residual ACF1 is approximately 0.51;
HF approximately 0.15. HF cold-day intervals are concordant across SE methods
but q-unprotected. CHD hot-night inference changes across SE constructions.
There is no protected differential CHD-hot/HF-cold claim.

## Source-locked weather morphology

The final exposure engine replaces an approximate 2D3N proxy with Wang's exact
`NDNDN` pattern and builds calendar-spillover exposure phases. Five
primary-source reproduction checks pass exactly:

- Li heatwaves 1980–2023: 57/57;
- Wang VHD days 2006–2015: 204/204;
- Wang HN days: 230/230;
- Wang VHD days in ≥5-day runs: 48/48; and
- Wang HN days in ≥5-night runs: 56/56.

Li/Hogan upper-tail monthly classification remains human-unlocked and
supplementary.

## M|D methods feasibility

A clean-room Basagaña–Ballester aggregated likelihood was implemented from the
published equation; unlicensed repository code was not copied.

- F1.0 (100 replicates): one-harmonic nuisance seasonality failed HF-like
  null calibration (Type I 0.62–0.75).
- F1.1: calendar-month indicators replaced the harmonic within the 20-parameter
  cap.
- F1.2: 500 replicates × 36 core cells used worst-cell gates.

Final decision: `FAIL_METHODS_FEASIBILITY_ONLY`.

- Null Type I: 0.048–0.150 (required 0.03–0.08).
- Minimum coverage: 0.840 (required ≥0.90).
- Maximum non-null relative bias: 32.77 (required ≤0.20).
- Maximum moderate false-sign: 0.808 (required ≤0.10).
- Minimum stress coverage: 0.842 (required ≥0.85).

No real daily-exposure coefficient was admitted. This is a negative methods
result, not unfinished analysis.

## Final artifacts

- Integrated report:
  `reports/bishai_integrated_report/integrated_project_report.md` and `.pdf`.
- Journal manuscript:
  `manuscript/chd_hf_thermal_associations_2013_2023.md` and `.pdf`.
- Supplement:
  `manuscript/chd_hf_supplement.md` and `.pdf`.
- Authorship/governance decision record:
  `manuscript/authorship_and_governance_decisions.md`.
- Release:
  `outputs/release_chd_hf/` (29/29 checks; 79-file hash manifest).
- Final calibration decision:
  `outputs/calibration_md/md_calibration_f1_2_decision_report.md`.
- Verified literature map:
  `literature/final_methods_evidence_map.md`.

## Lead recommendation

Recommend Gate 3 Option A: explicit no confirmatory primary and a
methods-focused exploratory paper. Report the full panel, SE ladder,
multiplicity, residual dependence, source validation, and failed daily-recovery
calibration. Do not headline a differential thermal mechanism.

## Human decisions still required

1. Gate 3 approval of Option A/B/C.
2. Written external-dissemination authority from Roro/Bishai.
3. PI IRB/protocol determination.
4. Exact ICD lists and `*_inpatient` semantics.
5. Stroke delivery or explicit removal from this paper.
6. T2D/HTN monthly still-at-risk denominator.
7. Hogan weather/HM-CM lock.
8. Final authorship, co-first, corresponding-author, and Zhou role.

## Reproducibility boundary

The public branch contains disclosure-minimised outputs but not governed
CHD/HF panels. New ensemble/prediction fits are therefore recorded as blocked.
A full real rerun requires secure local inputs matching the receipt hashes.
No raw monthly-count figures or tracked synthetic stroke panels remain in the
git tree.
