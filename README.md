# Thermal Extremes and Cardiovascular Hospital Burden in Hong Kong, 2013–2023

Laidlaw Scholars research project, The University of Hong Kong.  
Supervisor: Professor David Bishai. Analyst: Bob Shen Ruililin.  
Collaborators: Hogan (environmental data); Roro (Hospital Authority access).

## Research question

In Hong Kong from 2013 to 2023, how do officially defined thermal extremes—especially hot nights and cold days—relate to cardiovascular hospital admissions in an aging population, and do contemporary patterns differ from the historically cold-dominant risk profile reported in earlier local studies?

This is an ecological monthly time-series design. It does not claim individual-level causality, and it does not claim to be the first Hong Kong temperature–CVD or hot-night hospitalization study.

## Current status

| Domain | Status | Notes |
|---|---|---|
| HKO weather exposures | **Real** | Daily extracts processed; annual extremes validated 33/33 against HKO *Year’s Weather* |
| C&SD population denominators | **Real (MDT)** | Table 110-01001 mid-year age×sex; monthly linear interpolation |
| Air pollution | Placeholder | Import scripts ready; replace with EPIC/EPD series before inference |
| HA cardiovascular outcomes | **Not available** | Dev track uses synthetic panels only |
| First-stage research note | Available | `reports/First_Stage_Research_Note.pdf` |

**Do not interpret synthetic model coefficients as empirical findings.**

## How to run

From the repository root:

```bash
Rscript scripts/00_setup.R
Rscript scripts/run_pipeline_dev.R    # default: synthetic HA dry-run + smoke checks
# or
Rscript scripts/run_pipeline.R       # alias for dev
```

Real-HA track (fails until an approved aggregate is present):

```bash
Rscript scripts/run_pipeline_real.R
```

Pipeline toggles live in `config.yml` under `pipeline:` (`mode`, `weather_cache`, `refresh_csd`, `include_2024_extension`).

Or run scripts individually in order (`00` through `15`). Script `14` rebuilds the validated annual extremes figure under `figures/`. Script `15` runs smoke checks (HKO 33/33, C&SD import, schemas).

To recompile the research note or literature review:

```bash
cd reports/latex
pdflatex -interaction=nonstopmode first_stage_research_note.tex
pdflatex -interaction=nonstopmode literature_review_critical.tex
bibtex literature_review_critical
pdflatex -interaction=nonstopmode literature_review_critical.tex
pdflatex -interaction=nonstopmode literature_review_critical.tex
# copy PDFs to reports/ if desired
```

## Repository layout

```text
.
├── README.md
├── config.yml                 # Study window, thresholds, pipeline mode, paths, seeds
├── schemas/                   # HA / EPD / C&SD input contracts
├── analysis_plan/             # Assumption ledger and confirmation checklist
├── scripts/                   # Numbered R pipeline (00–15) + run_pipeline_{dev,real}.R
├── data_raw/                  # Immutable source files (HKO, EPD, C&SD MDT, HA placeholder)
├── data_processed/            # Monthly climate, pollution, population, panels
├── figures/                   # Manuscript-ready validated HKO figure
├── outputs/
│   ├── tables/                # Descriptive and (synthetic) model tables
│   ├── figures/exploratory/   # Pipeline check plots (not manuscript figures)
│   ├── figures/synthetic_diagnostic_plots/
│   └── table_shells/          # Empty shells for eventual HA results
├── literature/                # Evidence matrix, bibliography, comparison tables
├── memos/                     # Data requests to Roro (HA) and Hogan (environment)
├── reports/                   # Research note, validation note, literature memo
└── manuscript/                # Draft Introduction, literature review, Methods
```

Correspondence and personal emails are intentionally excluded from this repository.

## Exposure definitions (HKO Headquarters)

| Metric | Official definition |
|---|---|
| Hot night | Daily minimum temperature ≥ 28°C |
| Very hot day | Daily maximum temperature ≥ 33°C |
| Extremely hot day | Daily maximum temperature ≥ 35°C |
| Cold day | Daily minimum temperature ≤ 12°C |

Primary planned heat exposure: monthly count of hot nights. Cold days are retained as a co-primary exposure. Effective exposure sample for the core window: **132 months** (January 2013–December 2023).

## Principal outputs

| Output | Path |
|---|---|
| First-stage research note | `reports/First_Stage_Research_Note.pdf` |
| Exposure & aging context note | `reports/Exposure_Aging_Context_Note.pdf` |
| Critical literature review | `reports/Literature_Review_Critical.pdf` |
| Validated annual extremes figure | `figures/hko_annual_extremes_2013_2023.pdf` |
| Exposure–aging figures | `figures/exposure_aging/` |
| Figure validation note | `reports/hko_figure_validation_note.md` |
| Monthly climate panel | `data_processed/climate_monthly_2013_2023.csv` |
| C&SD population monthly | `data_processed/population_monthly_age_sex_2013_2023.csv` |
| Input schemas | `schemas/` |
| Assumption ledger | `analysis_plan/assumption_ledger.md` |
| HA data request | `memos/data_request_roro.md` |
| Environmental data request | `memos/environmental_data_request_hogan.md` |
| Literature memo / matrix | `reports/literature_review_findings_memo.md`, `literature/` |
| Methods draft | `manuscript/methods_draft.md` |

## Analytical standards

1. Label data provenance explicitly (`REAL`, `PLACEHOLDER_NOT_FOR_INFERENCE`, `SYNTHETIC`, `SYNTHETIC_DENOMINATOR`, `CSD_IMPORTED`).
2. Never commit real Hospital Authority microdata; use `data_raw/ha_secure_placeholder/` only as a local staging reminder.
3. Preserve `data_raw/`; processed files are rebuilt by scripts.
4. Prefer staged pollution models; treat ozone cautiously as a potential pathway variable.
5. Record unresolved design choices in the assumption ledger with `[TO CONFIRM]` tags in Methods.
6. Use `run_pipeline_dev.R` until HA arrives; `run_pipeline_real.R` refuses synthetic outcomes.

## Scientific framing notes

- Earlier Hong Kong daily studies (e.g. Goggins et al.) found cold-dominant cardiovascular associations; heat remains an open empirical question for this monthly design.
- Guo et al. (2024) examined hot nights and hospitalization in Hong Kong: official binary hot nights were not associated with excess risk, whereas hot-night *intensity* was. Novelty claims must respect that overlap.
- The scientific question is whether an emerging heat burden coexists with persistent cold risk in an aging city—not whether heat has simply replaced cold.
- See `reports/Literature_Review_Critical.pdf` for the Adds / Inspires / Debates / Implementation map.
