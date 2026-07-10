# Assumption Ledger

Audit-friendly record of working assumptions for the Hong Kong thermal extremes and cardiovascular admissions project (2013–2023). Update this file whenever the human team confirms or revises a decision.

| ID | Assumption or decision | Current working choice | Uncertainty | Why it matters | How to confirm | Owner |
|---|---|---|---|---|---|---|
| A01 | Study period | January 2013–December 2023 (132 months) | Low | Defines exposure and outcome window | Confirm with Bishai/Bob | Team |
| A02 | 2024 extension | Optional; request but do not delay core analysis | Medium | Adds high-heat contrast (~9% more months) | Confirm HA availability with Roro | Roro/Team |
| A03 | HA coding system | Unknown; ICD-9-CM provisional; ICD-10 backup prepared | High | Determines diagnosis algorithms | Request coding system/version by year | Roro |
| A04 | Principal diagnosis | Required for primary outcomes | High | Reduces incidental comorbidity coding | Confirm field availability | Roro |
| A05 | Event month | Month of admission / ED presentation, not discharge | High | Aligns exposure timing with event onset | Confirm date field used in extract | Roro |
| A06 | Admission type | Prefer emergency/unplanned inpatient admissions | High | Elective admissions may create artificial seasonality | Confirm admission-type field | Roro |
| A07 | Episode rule | Remove/combine transfers; retain true readmissions | High | Prevents double-counting episodes | Confirm transfer linkage feasibility | Roro |
| A08 | ED/inpatient overlap | Analyze separately; do not pool unless mutually exclusive | High | Avoids double-counting | Confirm ED-only flag | Roro |
| A09 | Age-group availability | Prefer 5-year bands through 85+ | Medium | Needed for aging hypotheses | Confirm extract strata | Roro |
| A10 | 65–69 and 70–74 | Must remain separate if feasible | Low | Intervention-relevant cohorts grew substantially | Confirm with Roro | Roro/Hogan note |
| A11 | Population denominator source | C&SD Table 110-01002 (sex × age) | Low | Supplies age-sex denominators | Bob validates download/API | Bob |
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
| A27 | Comorbidity | Not required for first ecological paper | High | Aggregate data may not support adjustment | Confirm with Roro | Roro |
| A28 | Unknown sex | Retain for QC; exclude/combine only after review | Medium | Denominator alignment | Review cell counts | Bob/Roro |
| A29 | Synthetic data labeling | Always `data_status = "SYNTHETIC"` | Low | Prevents accidental substantive reporting | Enforce in scripts | Bob |
| A30 | Primary heat model | Hot nights + cold days (not all heat metrics together) | Medium | Collinearity among heat metrics | Follow modeling plan | Bob |
| A31 | Ozone role | Staged; may confound, modify, or partly mediate heat | High | Mis-adjustment can attenuate heat associations | Report total vs pathway-adjusted effects | Team |
| A32 | Historical comparison | Qualitative unless methods harmonized with older daily studies | High | Monthly vs daily DLNM coefficients not directly comparable | Avoid “regime shift” claims | Team |

## Human confirmation checklist

1. Should the core period remain January 2013–December 2023?
2. Should 2024 be requested as an optional extension?
3. Can HA provide principal diagnosis?
4. Is HA coding ICD-9-CM, ICD-10, or mixed?
5. Can HA provide 5-year age bands?
6. Can 65–69 and 70–74 be separated?
7. Can transfers and duplicate admissions be removed?
8. Can ED-only events be separated from admissions?
9. Should in-hospital deaths and bed-days be requested?
10. Which HKO station or data product should define territory-wide exposure?
11. Which EPD monitoring stations should be used?
12. Should roadside pollution stations be excluded from primary analysis?
13. How should COVID phases be defined?
14. Should influenza be included in the primary model or sensitivity model?
15. Is district-level analysis out of scope for the first paper?
16. Prefer emergency/unplanned inpatient admissions as primary outcome?
17. Confirm that formal historical-effect comparisons remain qualitative unless methods are harmonized?
