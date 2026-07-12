# Assumption Ledger

Audit-friendly record of working assumptions for the Hong Kong thermal extremes and cardiovascular admissions project (2013–2023). Update this file whenever the human team confirms or revises a decision.

| ID | Assumption or decision | Current working choice | Uncertainty | Why it matters | How to confirm | Owner |
|---|---|---|---|---|---|---|
| A01 | Study period | January 2013–December 2023 (132 months) | Low | Defines exposure and outcome window | Confirm with Bishai/Bob | Team |
| A02 | 2024 extension | Optional; request but do not delay core analysis | Medium | Adds high-heat contrast (~9% more months) | Confirm HA availability with Roro | Roro/Team |
| A03 | HA coding system | **Confirmed ICD-9** (Roro, 12 Jul 2026); DAE records included — DAE definition TBD | Low (coding) / Medium (DAE) | Determines diagnosis algorithms | Clarify DAE at 17 Jul meeting | Roro |
| A04 | Principal diagnosis | Required for primary outcomes | High | Reduces incidental comorbidity coding | Confirm field availability at meeting | Roro |
| A05 | Event month | Month of admission / ED presentation, not discharge | High | Aligns exposure timing with event onset | Confirm date field used in extract | Roro |
| A06 | Admission type | Prefer emergency/unplanned inpatient admissions | High | Elective admissions may create artificial seasonality | Confirm admission-type field | Roro |
| A07 | Episode rule | Remove/combine transfers; retain true readmissions | High | Prevents double-counting episodes | Confirm transfer linkage feasibility | Roro |
| A08 | ED/inpatient overlap | **No ED-to-inpatient episodes in this extract** (Roro, 12 Jul 2026) | Low | Clarifies scope of admissions file | Confirm whether standalone ED series exists separately | Roro |
| A09 | Age-group availability | Prefer 5-year bands through 85+ | Low | Needed for aging hypotheses | **Affirmed:** HA supports stratification | Roro |
| A10 | 65–69 and 70–74 | **Confirmed separable** (Roro, 12 Jul 2026) | Low | Intervention-relevant cohorts | Locked | Roro |
| A11 | Population denominator source | C&SD Table 110-01001 MDT (mid-year age×sex); 110-01002 archived | Low | Supplies age-sex denominators with 65–69 / 70–74 split | Bob validates MDT import / QC totals | Bob |
| A12 | Population interpolation | Linear interpolation between mid-year estimates to month midpoints | Medium | Avoids step changes at year boundaries | Team approval; calendar-year assignment as sensitivity | Team |
| A13 | Population universe | Match HA resident/eligibility definition | High | Prevents denominator mismatch | Align with Roro/C&SD notes; FDH exclusion sensitivity | Roro/Bob |
| A14 | Weather station choice | HKO Headquarters primary | Medium | Matches official extreme-day definitions | Confirm with Hogan; multi-station sensitivity | Hogan |
| A15 | Weather spatial sensitivity | Fixed multi-station composite if feasible | Medium | Tests territorial representativeness | Hogan prepares alternative file | Hogan |
| A16 | Weather completeness | Months with <90% daily completeness flagged; extremes set to NA | Low | Missing days must not count as non-extremes | Review flagged months | Hogan/Bob |
| A17 | Spell boundary | Report within-month run length and full spell touching month | Medium | Spells may cross month boundaries | Implement both metrics | Hogan/Bob |
| A18 | Pollution station choice | General stations primary; roadside separate | Medium | Roadside ≠ territory-wide background | Confirm station list with Hogan | Hogan |
| A19 | Station aggregation | Unweighted mean of valid general stations; balanced-panel sensitivity | Medium | Network composition changed over time | Document openings/closures | Hogan |
| A20 | O3 metric | Monthly mean + peak-oriented MDA8-style metric if available | Medium | Mean O3 may miss photochemical peaks | Request both from Hogan/EPD | Hogan |
| A21 | Pollution completeness | Station-month valid if ≥75% expected observations | Medium | Limits biased means | Apply in build script | Hogan/Bob |
| A22 | COVID phases | pre_covid; early_covid; fifth_wave; late_2022; post_reopening (see config.yml) | Medium | Results may depend on cut-points | Adjust to HK policy dates if needed | Team |
| A23 | Influenza adjustment | Sensitivity model initially (not primary) | Medium | May confound or mediate cold effects | Bishai decision | Bishai |
| A24 | Public holidays | Number of holiday days + Chinese New Year indicator | Medium | Affects admissions; CNY shifts by month | Bob constructs calendar | Bob |
| A25 | Small-cell suppression | Never treat suppressed values as zero | High | Biases younger/rare-diagnosis strata | Confirm threshold and complementary suppression | Roro |
| A26 | District data | Out of scope for first paper unless readily available | Medium | Adds exposure/denominator complexity | Team decision | Team |
| A27 | Clinical covariates | **Working direction (Bishai, 12 Jul 2026):** age, sex, diuretics, beta blockers, metformin, SGLT2is, BMI | High (field availability) | Reframes near-term model beyond ecological-only | Confirm fields on HPC extract at meeting | Bishai/Roro |
| A28 | Unknown sex | Retain for QC; exclude/combine only after review | Medium | Denominator alignment | Review cell counts | Bob/Roro |
| A29 | Synthetic data labeling | Always `data_status = "SYNTHETIC"` | Low | Prevents accidental substantive reporting | Enforce in scripts | Bob |
| A30 | Primary heat / temperature model | **Near-term primary (Bishai, 12 Jul):** monthly Tmax/Tmin (+ lag) → AMI/stroke risk; official extremes secondary | Medium | Aligns with 12 Jul instruction | Confirm lag-1 month default at meeting | Bishai/Bob |
| A31 | Ozone role | Staged; may confound, modify, or partly mediate heat | High | Mis-adjustment can attenuate heat associations | Report total vs pathway-adjusted effects | Team |
| A32 | Historical comparison | Qualitative unless methods harmonized with older daily studies | High | Monthly vs daily DLNM coefficients not directly comparable | Avoid “regime shift” claims | Team |
| A33 | Official hot-night null | Compatible with Guo 2024; does not close nighttime-heat question | Medium | Binary policy metric ≠ intensity biology | Prespecify spell/intensity alternatives | Team |
| A34 | Absolute humidity | Prefer AH (Tetens) over RH alone for humidity pathways | Medium | RH entangled with temperature | Built in weather script; use in flu/cold sensitivities | Bob |
| A35 | Spell / 2D3N metrics | Secondary exposures alongside continuous temperature | Medium | Sequence discarded by monthly totals | Model as alternatives after primary temp+lag merge | Bob |
| A36 | Pooled stroke endpoint | Not primary; analyze IS and HS separately | Low | Subtypes differ biologically and historically | Enforce in modelling scripts | Bob |
| A37 | HA data grain | **Patient-level complete admissions** (Roro, 12 Jul 2026), not aggregate CSV first | Medium | Changes merge and covariate strategy | Onboard to HPC after wet-ink signatures | Roro/Bob |
| A38 | HA / HPC access | Wet-ink signatures from Bob and Hogan required before server access | Low | Blocks analysis start | Sign and return; Roro onboards Bob | Bob/Hogan/Roro |
| A39 | IRB protocol update | Raised by Roro (12 Jul 2026) because HA data used for additional work | High | Compliance | **PI decision** (Bishai) at/after 17 Jul meeting | Bishai |

## Human confirmation checklist

**Updated 12 July 2026 after Roro + Bishai notes. Still open for 17 July meeting:**

1. IRB protocol update needed for this HA use? (PI)
2. What does “DAE records included” mean?
3. Is principal diagnosis available / required in the patient-level file?
4. Are diuretics, beta blockers, metformin, SGLT2is, and BMI on the approved extract?
5. Is lag-1 month the default temperature lag?
6. Keep official hot nights / cold days as secondary exposures beside Tmax/Tmin?
7. Should the core period remain January 2013–December 2023?
8. Should 2024 be requested as an optional extension?
9. How should COVID phases be defined?
10. Confirm that formal historical-effect comparisons remain qualitative unless methods are harmonized?
