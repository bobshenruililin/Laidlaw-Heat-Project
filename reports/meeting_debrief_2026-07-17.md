# Meeting debrief — 17 July 2026

**Status:** Working strategy after lab meeting. Outcome data files not yet received.  
**Purpose:** Recalibrate the analysis plan from meeting feedback without inventing schema details or coefficients.  
**Audience:** Internal project note (Bob / next analysis steps).

---

## 1. What changed (plain reading of the feedback)

| Pre-meeting working assumption | Meeting feedback | Implication |
|---|---|---|
| General HA extract supports diagnosis-specific AMI / IS / HS (principal dx TBD) | Hospital Authority data available for this project **does not specify reasons for admission** | Full CVD principal-diagnosis panel is **not** available from the general HA file as previously hoped |
| Primary endpoints: AMI, ischemic stroke, hemorrhagic stroke separately | **Some stroke admission data** are available; work will use **aggregates** | Near-term outcome focus shifts to **stroke aggregates** (grain and subtype split TBD when files arrive) |
| Exposure analysis can use daily HKO internally, but supervisory merge was monthly Tmax/Tmin | Analysis remains constrained to **monthly temperature** (and monthly summaries built from daily HKO) | Keep monthly burden design; do not claim a daily admissions DLNM |
| One primary model + staged sensitivities | Explore **~10 different methods** for insight breadth | Multi-specification program is now an explicit strategy, not a distraction |
| Lab context was mainly historical Goggins daily admissions | Prof. Bishai / lab have **daily-scale heatwave work covering through 2023** (mortality burden; multi-definition) | Situate this project as **complementary** (monthly stroke admissions / aggregates), not a duplicate of that mortality study |
| Heatwave definitions already of interest via Wang/Ren 2019 | Dr **Chao Ren**’s team research on **defined heatwaves** is relevant (meeting: “Chao Ran” → Chao Ren) | Align heatwave-method family with Ren / Wang EHWE and with the lab’s multi-definition mortality work |

Nothing in this note invents coefficients, row counts, or field names for data that have not yet arrived.

---

## 2. Lab context that matters (without over-claiming)

### 2.1 Bishai / Liu / Ren daily heatwave–mortality work (2014–2023)

A recent lab-linked preprint quantifies **excess mortality** under **four heatwave definitions** in Hong Kong, 2014–2023 (Liu, Ren, …, Bishai; medRxiv). It uses:

- daily age–sex mortality / life-table expected deaths;
- HKO daily temperature;
- multiple heatwave definitions because **no single universal definition** exists;
- published local RRs (including Liu et al. 2020; Wang et al. 2019) rather than re-estimating admissions models.

That study answers: *how many excess deaths under alternative heatwave definitions?*  
This Laidlaw project, given current data limits, answers a different question: *how do monthly temperature / heatwave-burden metrics associate with stroke admission aggregates?*

**Do not** treat mortality excess-death estimates as substitutes for admission associations. **Do** borrow the lab’s rationale for **multi-definition** heat exposure and the Ren/Wang combined-threshold tradition.

### 2.2 Chao Ren–linked heatwave definitions (Wang et al. 2019 EHWE)

Wang, Lau, **Ren**, Goggins, et al. (*Sci Total Environ* 2019) define extremely hot weather events using official-style thresholds and spell structure, including:

- very hot days (VHD): Tmax ≥ 33°C;
- hot nights (HN): Tmin ≥ 28°C;
- prolonged spells (e.g. 5VHD, 5HN);
- combined day–night windows (e.g. **2D3N**).

The processed monthly climate file already carries related constructs (`hot_nights`, `very_hot_days`, spell-length metrics, `days_in_2d3n_window`, `month_has_2d3n_window`, etc.). Those remain usable as **monthly heatwave-burden** exposures even when the outcome series is aggregate stroke.

---

## 3. Recalibrated scientific framing

### Working estimand (provisional until data dictionary arrives)

Among Hong Kong residents in the extract’s eligible population, estimate **monthly** associations between:

1. continuous monthly temperature (mean / Tmax / Tmin and lag-1), and  
2. heatwave- / extreme-day **monthly burden** metrics (official counts; Ren-style spell / combined metrics; optional percentile-based month indicators),

and **stroke admission aggregates** (exact series TBD: total stroke counts by month ± age/sex strata if provided).

### What is demoted until proven available

- Principal-diagnosis **AMI** as a primary endpoint from the general HA file.
- Diagnosis-stratified **IS vs HS** as primary endpoints **unless** the stroke extract itself supports subtype codes.
- Any claim that the general HA file can recreate Goggins-style diagnosis-specific daily designs.

### What remains primary

- **Stroke aggregates** + monthly climate merge.
- Descriptive **Table 1**-style environment panel (already largely buildable from HKO).
- A **multi-method (~10)** exploration ladder that treats specification diversity as a feature, with clear labeling of each method’s estimand.

---

## 4. Multi-method program (~10 methods)

Goal: generate structured insight under uncertainty about the “best” single model, while staying honest about monthly resolution and aggregate outcomes.

Suggested family (names are working labels; freeze after data QC):

| # | Method family | Exposure | Outcome grain | Notes |
|---|---|---|---|---|
| M1 | Continuous same-month Tmean | Monthly mean temperature | Stroke aggregate rate / count | Closest to classical temperature–health series |
| M2 | Continuous same-month Tmax / Tmin | Monthly mean Tmax, Tmin | Same | Aligns with 12 Jul supervisory merge request |
| M3 | Lag-1 temperature | Prior-month Tmean or Tmax/Tmin | Same | Requires Dec 2012 weather for Jan 2013 |
| M4 | Official extreme-day counts | Hot nights, cold days, very hot days (month totals) | Same | Policy-linked HKO definitions |
| M5 | Ren/Wang spell burden | Days in ≥5 HN / ≥5 VHD spells; longest runs | Same | Sequence structure within month |
| M6 | Combined day–night (2D3N-style) | `days_in_2d3n_window` / binary month flag | Same | Direct link to Ren-team EHWE tradition |
| M7 | Heatwave-month indicator(s) | Month intersects ≥1 event under a chosen definition | Same | Bridges to Liu/Bishai multi-definition logic, monthly collapsed |
| M8 | Cold-side counterpart | Cold-day counts / cold-spell metrics | Same | Historical HK stroke literature is cold-relevant |
| M9 | Age-stratified rates (if aggregates allow) | Preferred exposure from M1–M8 | Age-band stroke aggregates | Aging / 65–69 & 70–74 if present |
| M10 | Seasonality / COVID / humidity sensitivities | Core exposure + AH, COVID phase, holiday days | Same | Sensitivity ladder, not a tenth “discovery” claim |

**Reporting rule:** present methods as a **panel of specifications**, not as ten independent discoveries. Prefer one pre-specified “headline” pair (e.g. M2 + M4 or M2 + M6) after Gate 3 freeze; treat the rest as structured exploration.

**Honesty rule:** monthly models estimate **hospital-burden associations**. They are not interchangeable with daily DLNM triggering coefficients (Goggins) or with excess-death counts (Liu/Ren/Bishai mortality preprint).

---

## 5. Data arrival readiness (when files are sent)

Expected near-term files (exact names TBD):

1. Stroke admission **aggregates** (monthly ± age/sex if available).  
2. Possibly other HA aggregates without diagnosis reasons — useful for context/QC, **not** for AMI/IS/HS endpoints.  
3. Any data dictionary / codebook for aggregate fields.

Immediate pipeline after receipt:

1. **Ingest + QC** — row counts, month coverage 2013–2023, missingness, suppression codes, age/sex completeness.  
2. **Merge** to `data_processed/climate_monthly_2013_2023.csv` (+ population denominators if strata match).  
3. **Descriptives** — stroke counts/rates over time; overlay temperature and extreme-day series; Table 1 environment + outcome panels.  
4. **Multi-method associations** — run M1–M10 under Gate discipline; label every estimate by method ID.  
5. **Do not** invent subtype or AMI results from files that lack diagnosis reasons.

Scripts already oriented to monthly merge: `08b_merge_real_ha_panel.R`, descriptive scripts, real-model stubs. They will need outcome-schema adaptation once aggregates arrive (current stubs still assume diagnosis-stratified counts).

---

## 6. Immediate actions

| Action | Status |
|---|---|
| Ingest stroke / HA aggregates when sent; write QC note | Waiting on files |
| Merge to monthly HKO climate (+ denominators if strata match) | After QC |
| Adapt merge scripts for aggregates (not diagnosis panel) | After schema known |
| Run labelled multi-method panel M1–M10 | After Gate 2 |
| Extend weather build to Dec 2012 (lag-1 for Jan 2013) | Can do anytime |
| IRB / governance determination (PI) | Open |

Assumption ledger and decision gates are updated in parallel. Literature map: `reports/Literature_Review_Critical.pdf`.

---

## 7. Open items when data arrive

1. Aggregate grain (territory-month vs month × age × sex).  
2. IS vs HS split, or pooled stroke only.  
3. Inpatient definition and which date sets the month.  
4. Small-cell suppression rules.  
5. Medication / BMI (likely limited for aggregates).  
6. Any separate AMI series (do not assume).  
7. IRB / governance for this use (PI).

---

## 8. One-sentence strategy

**Work with monthly climate and multi-definition heatwave-burden metrics (~10 specifications), centred on stroke admission aggregates, as a complementary admissions/burden study beside the lab’s daily multi-definition heatwave–mortality work — and wait for the incoming files before any coefficient claims.**
