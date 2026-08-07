# Decision gates — Temperature–CVD / stroke project

Working decision gates after the **17 July 2026** lab meeting. Full recalibration: `reports/meeting_debrief_2026-07-17.md`.

**Principle:** Do not invent diagnosis-specific endpoints the data cannot support. Do not inspect substantive coefficients before Gates 1–2 are closed for the **files actually received**. Multi-method exploration (~10 specs) is allowed after Gate 2, with Gate 3 locking the **headline** specification before treating any single estimate as primary.

Owners and dates use placeholders where still open.

---

## Gate 1 — Schema and access (revised for aggregates)

**Required before treating outcomes as analysis-ready.**

| Prerequisite | Status | Owner | Stop condition |
|---|---|---|---|
| Stroke / HA aggregate files received under approved transfer path | **Partial — CHD+HF received 7 Aug 2026; stroke file not attached** | Bob / Roro | No invented row counts |
| Data dictionary or field list for aggregates | **Partial — email definition recorded; ICD lists still to confirm** | Roro / sender | Do not invent field meanings |
| Outcome definition (what “stroke admission” means in the file) | **CHD/HF defined:** first inpatient hosp. after first CVD dx in T2D/HTN cohort; stroke pending | Roro / Bob | Do not model until defined |
| Aggregate grain (month only vs month × age × sex) | **Territory-month (CHD, HF)** | On file inspection | Determines denominator strategy |
| Subtype availability (IS / HS) | Absent in CHD/HF release | On file inspection | Default to pooled stroke if absent |
| General HA “reasons for admission” | **Confirmed unavailable** (17 Jul); Roro construction substitutes first-post-diagnosis hospitalisation | — | Do not claim principal-dx from general HA |
| Ethics / governance for current use | Open | **PI (Bishai)** | Follow PI determination |
| Small-cell / release rules | No suppression flags in territory-month files | Roro | Do not release suppressed cells as zero |
| Medication / BMI (if claimed) | Not in monthly files | Roro | Descriptive only if present |

**Exit criterion:** Files in hand + written understanding of stroke outcome definition and grain + PI-approved use path.

**7 Aug 2026:** Gate 1 **conditionally closed for CHD and HF**; remains **open for stroke** until the file arrives. Receipt: `reports/data_receipt_2026-08-07.md`.

---

## Gate 2 — Outcome-data QC

**Required before regression / multi-method association runs.**

| Check | Purpose | Stop condition |
|---|---|---|
| Month coverage vs 2013–2023 climate | Align panels | Large gaps unexplained → pause |
| Missingness / suppression codes | Bound usable sample | Unknown codes → pause |
| Implausible counts | Catch extract errors | Resolve before modelling |
| Age / sex completeness (if stratified) | Denominator alignment | Missing bands → escalate or collapse |
| Seasonality / COVID-era patterns | Care-seeking shocks | Flag; do not over-interpret |
| External plausibility vs any published HA stroke totals | Sanity | Large unexplained gaps → pause |

**Exit criterion:** Short QC / data-receipt note + merged monthly climate–outcome panel reviewed.

**7 Aug 2026:** Gate 2 **closed for CHD and HF** (`reports/gate2_qc_close_2026-08-07.md`). Gate 2 **open for stroke**.

---

## Gate 3 — Analysis-plan freeze (headline among ~10)

**Lock the headline specification before treating any coefficient as the primary result.** Multi-method exploration may run after Gate 2, but results are labelled as a **panel** until this gate closes.

| Item | Proposed default (pending confirmation) | Owner |
|---|---|---|
| Primary outcome | **Team decision needed:** CHD and/or HF first hospitalisations (T2D/HTN cohort) now runnable; stroke pending file | Bishai / team |
| AMI / general CVD principal-dx | General HA still lacks admission reasons; Roro’s CHD/HF files are **first-event** constructions, not principal-dx from general HA | Meeting 17 Jul + 7 Aug receipt |
| Primary denominator | C&SD 35+ ecological offset **with cohort mismatch caveat** until T2D/HTN denominators exist | Bishai / Bob |
| Continuous exposures | Same-month Tmax / Tmin (and/or Tmean); lag-1 as paired spec | Bishai |
| Heatwave / extreme family | Official counts + Ren/Wang spell & 2D3N metrics; provisional HM/CM until Hogan lock | Bob / Bishai |
| Multi-method panel | P01–P18 + provisional HM/CM **completed for CHD/HF**; packet in `reports/gate3_decision_packet_2026-08-07.md` | Team |
| Seasonality / trend | Month factors + ns(time, 4) used in panel | Team / Bishai |
| COVID / humidity / holidays | Sensitivity ladder run (P10–P12, P14, P16) | Team |
| Medication / BMI model role | Not available | Bishai / Roro |

**Exit criterion:** Short freeze note (ledger update) after descriptives, naming the headline method ID(s).

**7 Aug 2026:** Gate 3 **OPEN**. Complete panel + decision packet ready; freeze requires Hogan / Roro / Bishai / Bob.

---

## Gate 4 — Multi-method association runs

**Run only after Gates 1–2.** Headline claim only after Gate 3.

Allowed:

- Count / rate regressions with appropriate offsets under the aggregate design.
- Labelled **P01–P18** pathway panel (`pathway_registry.yml`); ~10+ core specs plus extensions.
- Cold-side and heatwave-definition comparisons; staged pollution; flu complete-case.

Not allowed before Gate 2 (and for primary claim, Gate 3):

- Interpreting temperature coefficients as findings in public write-ups
- Equating monthly associations with daily DLNM or with excess-death mortality estimates
- Inventing AMI / subtype results from files that lack those fields

**Stop condition:** Schema or outcome definition changes → return to Gate 1–2.

---

## Gate 5 — Extensions

**Only after the core monthly stroke–temperature panel is documented.**

- Influenza (CHP Flu Express) — already wired as P14 when series loaded
- Official holiday gazette (replace scaffold)
- Roadside pollution sensitivity
- Multi-station weather / district analysis
- 2024 extension
- Patient-level / medication–BMI pathway work **if** a suitable extract later exists
- Harmonized comparison to daily historical studies (methods must match)

---

## Immediate work that does **not** wait on files

1. Keep climate + exposure file with lag-1 and HW-month indicators ready.  
2. Run pathway dry-run: `Rscript scripts/run_pathway_pipeline.R`.  
3. Drop real stroke aggregates into `data_raw/ha_secure_placeholder/` then `PATHWAY_MODE=real`.  
4. Keep ledger / gates / pathway registry / SAP current.  

---

## Related documents

- `README.md`
- `reports/meeting_debrief_2026-07-17.md`
- `analysis_plan/assumption_ledger.md`
- `analysis_plan/pathway_catalogue.md`
- `analysis_plan/pathway_registry.yml`
- `analysis_plan/statistical_analysis_protocol.md`
- `analysis_plan/gap_analysis_readiness.md`
