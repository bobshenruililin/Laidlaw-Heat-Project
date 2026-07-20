# Assumption Ledger

Audit-friendly record of working assumptions for the Hong Kong thermal extremes and cardiovascular admissions project (2013–2023). Update this file whenever the human team confirms or revises a decision.

| ID | Assumption or decision | Current working choice | Uncertainty | Why it matters | How to confirm | Owner |
|---|---|---|---|---|---|---|
| A01 | Study period | January 2013–December 2023 (132 months) | Low | Defines exposure and outcome window | Confirm with Bishai/Bob | Team |
| A02 | 2024 extension | Optional; request but do not delay core analysis | Medium | Adds high-heat contrast (~9% more months) | Confirm HA availability with Roro | Roro/Team |
| A03 | HA coding system | **Confirmed ICD-9** (Roro, 12 Jul 2026); DAE records included — DAE definition TBD | Low (coding) / Medium (DAE) | Determines diagnosis algorithms | Clarify DAE at 17 Jul meeting | Roro |
| A04 | Principal diagnosis / admission reason | **Revised 17 Jul:** general HA extract **does not specify reasons for admission**; principal-dx AMI/CVD from that file is not available as previously hoped | Low (limitation stated) / High (stroke-file detail TBD) | Changes feasible endpoints | Confirm stroke-file fields on data arrival | Roro/Bob |
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
| A30 | Primary heat / temperature model | **Revised 17 Jul:** monthly temperature + multi-method (~10) panel → **stroke aggregates**; Tmax/Tmin/lag remain core continuous specs; extremes / Ren-style heatwave metrics co-equal exploration family | Medium | Meeting strategy + data limits | Freeze headline method after Gate 3 | Bishai/Bob |
| A31 | Ozone role | Staged; may confound, modify, or partly mediate heat | High | Mis-adjustment can attenuate heat associations | Report total vs pathway-adjusted effects | Team |
| A32 | Historical comparison | Qualitative unless methods harmonized with older daily studies | High | Monthly vs daily DLNM coefficients not directly comparable | Avoid “regime shift” claims | Team |
| A33 | Official hot-night null | Compatible with Guo 2024; does not close nighttime-heat question | Medium | Binary policy metric ≠ intensity biology | Prespecify spell/intensity alternatives | Team |
| A34 | Absolute humidity | Prefer AH (Tetens) over RH alone for humidity pathways | Medium | RH entangled with temperature | Built in weather script; use in flu/cold sensitivities | Bob |
| A35 | Spell / 2D3N metrics | Secondary exposures alongside continuous temperature | Medium | Sequence discarded by monthly totals | Model as alternatives after primary temp+lag merge | Bob |
| A36 | Pooled stroke endpoint | **Revised 17 Jul:** pooled stroke aggregates are the **near-term primary** unless the stroke extract supports IS/HS split; do not invent subtypes | Medium | Historical biology still prefers subtypes when available | Inspect stroke file on arrival | Bob/Roro |
| A37 | HA data grain | **Revised 17 Jul:** near-term work uses **aggregates** (esp. stroke); general HA reasons for admission unavailable; patient-level path remains secondary if still accessible later | Medium | Changes merge scripts and covariate feasibility | Confirm on file receipt | Roro/Bob |
| A38 | HA / HPC access | Wet-ink signatures from Bob and Hogan required before server access (if patient-level still needed); aggregate transfer path TBD with PI | Medium | Blocks some analyses | Sign if needed; follow PI transfer rules for aggregates | Bob/Hogan/Roro |
| A39 | IRB protocol update | Raised by Roro (12 Jul 2026); still needs PI determination after 17 Jul meeting | High | Compliance | **PI decision** (Bishai) | Bishai |
| A40 | AMI as primary endpoint | **Demoted 17 Jul** for general HA file (no admission reasons). Reinstate only if a separate AMI series is confirmed | Low given meeting | Prevents over-claiming diagnosis-specific CVD | Confirm any AMI extract | Bishai/Roro |
| A41 | Multi-method program | Explore ~10 labelled specifications (continuous T, lag, official extremes, Ren/Wang spells & 2D3N, heatwave-month indicators, cold-side, age strata, sensitivities) | Medium | Insight under definition uncertainty; risk of multiple-testing narrative | Pre-specify headline pair at Gate 3; report as panel | Bob/Bishai |
| A42 | Chao Ren heatwave alignment | Prefer Ren/Wang EHWE-style metrics (VHD/HN spells, combined day–night) alongside official HKO counts | Low | Matches meeting guidance and existing climate constructs | Keep climate build; cite Wang et al. 2019 | Bob |
| A43 | Lab daily heatwave–mortality study | Liu/Ren/Bishai-type daily excess-mortality work (through 2023, multi-definition) is **complementary context**, not this project’s estimand | Low | Avoid duplicating mortality claims or mixing estimands | Cite carefully; keep admissions/aggregate framing | Team |
| A44 | Analysis temperature grain | Monthly only for association models (daily HKO used to build monthly metrics, not daily admissions models) | Low | Stated meeting constraint | Enforce in analysis scripts | Bob |

## Human confirmation checklist

**Updated 17 July 2026 after lab meeting. Open items:**

1. IRB / governance determination for stroke-aggregate (and any remaining HA) use? (PI)
2. Exact stroke aggregate grain (territory-month vs month × age × sex)?
3. Does the stroke file distinguish ischemic vs hemorrhagic stroke?
4. Is any AMI series available outside the general “no reason” HA file?
5. Which method is the headline among the ~10 after QC (Gate 3)?
6. Medication / BMI availability given aggregate outcomes?
7. Small-cell suppression rules before releasing tables?
8. Should the core period remain January 2013–December 2023?
9. Should 2024 be requested as an optional extension?
10. Confirm that formal historical-effect comparisons remain qualitative unless methods are harmonized?
