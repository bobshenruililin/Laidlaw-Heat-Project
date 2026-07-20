# Decision gates — Temperature–CVD / stroke project

Working decision gates after the **17 July 2026** lab meeting. Full recalibration: `reports/meeting_debrief_2026-07-17.md`.

**Principle:** Do not invent diagnosis-specific endpoints the data cannot support. Do not inspect substantive coefficients before Gates 1–2 are closed for the **files actually received**. Multi-method exploration (~10 specs) is allowed after Gate 2, with Gate 3 locking the **headline** specification before treating any single estimate as primary.

Owners and dates use placeholders where still open.

---

## Gate 1 — Schema and access (revised for aggregates)

**Required before treating outcomes as analysis-ready.**

| Prerequisite | Status | Owner | Stop condition |
|---|---|---|---|
| Stroke / HA aggregate files received under approved transfer path | Pending (user sending next) | Bob / PI | No invented row counts |
| Data dictionary or field list for aggregates | Pending | Roro / sender | Do not invent field meanings |
| Outcome definition (what “stroke admission” means in the file) | Open | Roro / Bob | Do not model until defined |
| Aggregate grain (month only vs month × age × sex) | Open | On file inspection | Determines denominator strategy |
| Subtype availability (IS / HS) | Open | On file inspection | Default to pooled stroke if absent |
| General HA “reasons for admission” | **Confirmed unavailable** (17 Jul) | — | Do not use general HA for AMI/principal-dx CVD |
| Ethics / governance for current use | Open | **PI (Bishai)** | Follow PI determination |
| Small-cell / release rules | Open | Roro | Do not release suppressed cells as zero |
| Medication / BMI (if claimed) | Likely limited for aggregates | Roro | Descriptive only if present |

**Exit criterion:** Files in hand + written understanding of stroke outcome definition and grain + PI-approved use path.

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

---

## Gate 3 — Analysis-plan freeze (headline among ~10)

**Lock the headline specification before treating any coefficient as the primary result.** Multi-method exploration may run after Gate 2, but results are labelled as a **panel** until this gate closes.

| Item | Proposed default (pending confirmation) | Owner |
|---|---|---|
| Primary outcome | Stroke admission **aggregates** (pooled unless subtypes available) | Bishai / team |
| AMI / general CVD principal-dx | **Out of scope** for general HA file | Meeting 17 Jul |
| Primary denominator | C&SD age–sex person-time if strata exist; else documented population offset / rate construction | Bishai / Bob |
| Continuous exposures | Same-month Tmax / Tmin (and/or Tmean); lag-1 as paired spec | Bishai |
| Heatwave / extreme family | Official counts + Ren/Wang spell & 2D3N metrics; optional heatwave-month indicators | Bob / Bishai |
| Multi-method panel | ~10 labelled methods (see debrief §4); one headline pair frozen here | Team |
| Seasonality / trend | Prespecify before calling a primary result | Team / Bishai |
| COVID / humidity / holidays | Sensitivity ladder | Team |
| Medication / BMI model role | Only if structure supports; else omit from models | Bishai / Roro |

**Exit criterion:** Short freeze note (ledger update) after descriptives, naming the headline method ID(s).

---

## Gate 4 — Multi-method association runs

**Run only after Gates 1–2.** Headline claim only after Gate 3.

Allowed:

- Count / rate regressions with appropriate offsets under the aggregate design.
- Labelled M1–M10 panel reporting.
- Cold-side and heatwave-definition comparisons.

Not allowed before Gate 2 (and for primary claim, Gate 3):

- Interpreting temperature coefficients as findings in public write-ups
- Equating monthly associations with daily DLNM or with excess-death mortality estimates
- Inventing AMI / subtype results from files that lack those fields

**Stop condition:** Schema or outcome definition changes → return to Gate 1–2.

---

## Gate 5 — Extensions

**Only after the core monthly stroke–temperature panel is documented.**

- Pollution (placeholder until real series)
- Influenza
- Multi-station weather
- District analysis
- 2024 extension
- Patient-level / medication–BMI pathway work **if** a suitable extract later exists
- Harmonized comparison to daily historical studies (methods must match)

---

## Immediate work that does **not** wait on files

1. Keep climate monthly file + Ren-style spell / 2D3N metrics ready.  
2. Extend weather build to December 2012 for lag-1.  
3. Prepare ingest stubs for aggregate stroke merge.  
4. Keep ledger / gates / debrief current (this update).  

---

## Related documents

- `README.md`
- `reports/meeting_debrief_2026-07-17.md`
- `analysis_plan/assumption_ledger.md`
