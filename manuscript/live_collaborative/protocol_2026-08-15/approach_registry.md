# Approach registry — thesis, analysis, covariates, external data, future ideas

Mark: `active` · `blocked` · `rejected` · `deferred` · `promoted`.

## Manuscript thesis variants (none is a Gate 3 freeze)

| ID | Formulation | Mark | Reason |
|---|---|---|---|
| T1 | Methods-honest exploratory panel: monthly official thermal encodings are not sufficient for a multiplicity-protected CHD-heat vs HF-cold claim; identification of remaining variation is the contribution | `active` (current live file) | Matches *q* > 0.19, SE discordance, missing admission cause and person-time |
| T2 | Identification paper: after calendar-month indicators, hot-night coefficients are summer intensity (1 vs 25) and cold-day coefficients are between-winter | `active` as supporting spine | Already in Abstract/Results/Discussion; not a substitute for T1 |
| T3 | “Has heat replaced cold in contemporary Hong Kong cardiac admissions?” | `deferred` | Hogan’s original question; cannot be answered as a yes/no from this estimand |
| T4 | Heat has replaced cold | `rejected` | Not supported; cold days persist; HF–cold residual exists; no protected primary |
| T5 | Restore AMI / ischaemic / haemorrhagic stroke among residents 35+ as the study question | `rejected` | File that arrived is CHD/HF first hospitalisation; stroke unattached |
| T6 | Causal effect of hot nights on CHD hospitalisation | `rejected` | Ecological monthly counts; no admission cause; no individual exposure |

## Analysis strategies

| ID | Strategy | Mark | Reason |
|---|---|---|---|
| A1 | Twelve separate NB models, days offset, month + ns(time,4), NW6 reporting with full SE ladder | `promoted` as analysis of record | Already fitted; exploratory |
| A2 | Joint extreme-day / Tmax+Tmin models | `active` as collinearity diagnostics only | VIF 4.66 / ~1.96; not preferred estimates |
| A3 | Pollution- or flu-adjusted “core” | `rejected` as adjusted Table 2 | Archive models are a different spec; flu P14 uses population×days |
| A4 | Daily DLNM on real health | `blocked` | Daily outcomes not delivered; M\|D recovery failed calibration |
| A5 | Refit health models this session | `blocked` | Panels absent |
| A6 | Health-economic CEA / cost-effectiveness | `rejected` for this paper | No costs, no intervention comparator, no QALYs; utilisation counts are epidemiological |

## Covariates / unmeasured factors

| Factor | Mark in live paper | Reason |
|---|---|---|
| Calendar month + time spline | `promoted` | Core |
| Days-in-month offset | `promoted` | Analysis of record |
| C&SD 35+ × days | `active` as sensitivity only | Not cohort person-time |
| NO₂, PM2.5, O₃ | `active` as staged archive / context | Not interchangeable with temperature |
| Influenza | `active` as archive / limitation | 121/132 months; never zero-filled |
| Housing, behaviour, AC | `rejected` for naming in Intro | Unmeasured; Hogan comment 4 |
| Medication | `rejected` for naming in Intro | Unmeasured in aggregates; same dangling-factor problem |
| Age/sex strata | `blocked` | Not delivered |

## External-data candidates

See [`external_data_feasibility.md`](external_data_feasibility.md). None merged into the primary model this session.
