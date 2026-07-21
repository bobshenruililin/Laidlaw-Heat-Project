# Thermal extremes and stroke hospital burden in Hong Kong, 2013–2023

Laidlaw Scholars project · The University of Hong Kong  
**Bob Shen Ruililin** · Supervisor: **Professor David Bishai**

This repository is the working home for a monthly climate–health analysis: how temperature and defined heatwave / cold extremes relate to **stroke admission aggregates** in Hong Kong, 2013–2023. The README is the primary orientation document; code and data sit underneath it.

---

## What this project is (now)

| | |
|---|---|
| **Design** | Ecological **monthly** time series (132 months, Jan 2013–Dec 2023) |
| **Exposures** | HKO Headquarters temperature (mean / Tmax / Tmin, lags) plus official extreme-day counts and Ren/Wang-style heatwave-burden metrics (spells, 2D3N) |
| **Outcome (near-term)** | **Stroke admission aggregates** (files pending) |
| **Not available** | General HA extract **does not specify reasons for admission** — no AMI / principal-dx CVD panel from that file |
| **Strategy** | Explore a labelled panel of ~10 specifications (continuous temperature, lags, extremes, heatwave definitions, cold-side, strata, sensitivities) |
| **Not claimed** | Individual causality; daily DLNM triggering; excess-death estimates from the lab’s separate heatwave–mortality work |

Full post-meeting recalibration: [`reports/meeting_debrief_2026-07-17.md`](reports/meeting_debrief_2026-07-17.md).

---

## Current status

| Domain | Status |
|---|---|
| HKO weather (monthly panel + extremes / spells) | **Ready** — annual extremes validated 33/33 vs HKO *Year’s Weather* |
| C&SD age–sex denominators | **Ready** (Table 110-01001 MDT) |
| Air pollution | **Ready (EPD EPIC)** | Monthly NO₂, O₃, PM₂.₅, PM₁₀ — general-station means; roadside archived for sensitivity |
| Stroke / HA aggregates | **Awaiting data transfer** |
| Association estimates | **None yet** — no coefficients until QC + merge |

Do not treat any synthetic practice runs as results.

---

## Quick start

```bash
Rscript scripts/00_setup.R
Rscript scripts/run_pipeline_dev.R   # weather / population / dry-run path
```

Pollution (official EPD EPIC monthly averages):

```bash
python3 scripts/18_download_epd_epic_monthly.py --include-roadside
Rscript scripts/04_build_pollution_monthly.R
```

Real-outcome track (expects an approved aggregate file):

```bash
Rscript scripts/run_pipeline_real.R
```

Config lives in `config.yml`. Rebuild the validated annual extremes figure with `scripts/14_hko_annual_extremes_figure.R`.

---

## Repository map

```text
README.md                 ← start here
config.yml
analysis_plan/            assumption ledger + decision gates
scripts/                  numbered R pipeline
data_raw/                 HKO, C&SD, EPD placeholder (no real HA microdata)
data_processed/           monthly climate, population, confounders
figures/                  validated extremes + exposure/aging figures
outputs/tables/           descriptive tables from the public pipeline
literature/               bibliography + evidence matrix
reports/                  meeting debrief, literature review PDF, validation note
schemas/                  input contracts for future aggregates
```

Correspondence, emails, and meeting slide drafts are **not** kept in this repo.

---

## Exposure definitions (HKO Headquarters)

| Metric | Definition |
|---|---|
| Hot night | Daily Tmin ≥ 28°C |
| Very hot day | Daily Tmax ≥ 33°C |
| Extremely hot day | Daily Tmax ≥ 35°C |
| Cold day | Daily Tmin ≤ 12°C |

Monthly spell / combined day–night metrics (including 2D3N-style windows) are built in `data_processed/climate_monthly_2013_2023.csv` for the multi-method heatwave family.

---

## Key files

| What | Where |
|---|---|
| Post-meeting strategy + next actions | `reports/meeting_debrief_2026-07-17.md` |
| Assumption ledger | `analysis_plan/assumption_ledger.md` |
| Decision gates | `analysis_plan/decision_gates.md` |
| Monthly climate panel | `data_processed/climate_monthly_2013_2023.csv` |
| Monthly pollution panel | `data_processed/pollution_monthly_2013_2023.csv` |
| Literature review (PDF) | `reports/Literature_Review_Critical.pdf` |
| HKO extremes figure | `figures/hko_annual_extremes_2013_2023.pdf` |
| Exposure & aging note | `reports/Exposure_Aging_Context_Note.pdf` |
| Figure validation | `reports/hko_figure_validation_note.md` |

---

## Rules of the road

1. Label provenance (`REAL`, `PLACEHOLDER_NOT_FOR_INFERENCE`, `SYNTHETIC`, …).
2. Never commit Hospital Authority microdata.
3. Prefer rebuilding processed files from `data_raw/` via scripts.
4. Monthly associations ≠ daily DLNM coefficients ≠ excess-death mortality counts.
5. Record open design choices in the assumption ledger; freeze a headline method only after Gate 3.

---

## Scientific context (short)

Earlier Hong Kong daily studies (e.g. Goggins) reported cold-dominant cardiovascular admission patterns. Guo et al. (2024) found official binary hot nights alone were weak for hospitalization risk relative to nighttime heat *intensity*. Wang/Ren-style EHWE definitions (very hot days, hot nights, combined windows) matter for heatwave specification. A related lab line of work quantifies **daily multi-definition heatwave excess mortality**; this project is complementary: **monthly stroke-aggregate burden**, not a duplicate of that mortality analysis.

See `reports/Literature_Review_Critical.pdf` for the literature map.
