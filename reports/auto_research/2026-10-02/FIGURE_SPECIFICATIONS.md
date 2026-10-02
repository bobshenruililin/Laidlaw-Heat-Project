# Evidence figure specifications and coverage

**Date:** 2 October 2026. The four figures use released `HA_APPROVED_AGGREGATE` summary tables or explicitly conceptual relationships. No secure input, new model fit, reconstructed monthly series, fabricated incidence or clinical measurement is involved. Source snapshots and SHA-256 provenance are supplied beside the figures. Build with `scripts/84_covid_evidence_figures.py` using Python with Matplotlib.

## Current manuscript figures

### Main Figure 1 — conceptual observation process

**File stem:** `figures/covid_period/figure_observation_process_20261002`.

**Caption:** Candidate pathways linking pandemic-era context to recorded first hospitalisations after a CHD or HF diagnosis record. Underlying clinical state can affect both diagnosis and hospital contact, while eligibility, prior events, exits and competing death can change the population contributing a recorded stay. The hospitalisation cause is unavailable. Arrows specify possible relationships for study design, without their signs or an identified causal effect. The diagram is a partial conceptual schematic, not a confirmed cohort flow or complete causal adjustment graph.

**Source and visual contract:** the August receipt supports the event boundary. All edges in the accompanying CSV carry `CONCEPTUAL_HYPOTHESIS`. No cohort size or event-free denominator is supplied. Only the recorded-count node has a blue border, distinguishing the observed endpoint from candidate mechanisms.

### Main Figure 2 — recorded annual burden

**File stem:** `figures/covid_period/figure_annual_counts_20261002`.

**Caption:** Annual recorded first hospitalisations after first CHD diagnosis (left) or first HF diagnosis (right), 2013–2023. Counts declined before 2020, reached a further trough in 2020 and approached 2019 totals by 2023. Grey shading denotes calendar years 2020–2023; it does not establish a causal intervention. Panel vertical scales differ. Counts describe the extraction, rather than incidence in an eligible cohort.

**Source and numerical contract:** exactly 22 annual rows, 12 months per row. Copy only outcome, year, total count, number of months and provenance into the figure source CSV. Do not use legacy territory-population rates, which are not eligible-cohort incidence. Markers and colours distinguish outcomes, while zero-based axes preserve count interpretation. The stable PNG replaces the earlier 2013-index chart; the briefing retains an editable index chart from the same counts.

### Main Figure 3 — calendar and start-window model criticism

**File stem:** `figures/covid_period/figure_calendar_sensitivity_20261002`.

**Caption:** Count ratios per five official cold days for HF (left) and five hot nights for CHD (right), with Newey–West lag-6 95% intervals, under the baseline model and six calendar/start-window checks. Calendar splines use 3, 4, 6 or 8 degrees of freedom; remaining checks use year fixed effects or omit the initial 12 or 24 months. The HF cold-day interval includes one under several checks. These two historically discussed contrasts are selected diagnostic displays, not a new multiplicity family. Full source results and the phase-adjusted intercept specification remain in Supplement Table S3. Panel horizontal ranges differ.

**Source and numerical contract:** 14 exact rows from the released trend-depletion table; no refitting. Include baseline plus all six specified checks, without retaining only intervals excluding one. Preserve scenario-specific month counts in the source snapshot. The log axis shows declared decimal ticks and suppresses automatic minor tick labels. Other exposures remain in the complete released panel.

### Supplement Figure S1 — overlapping window associations

**File stem:** `figures/covid_period/figure_nested_window_associations_20261002`.

**Caption:** Existing cold-day, very-hot-day and hot-night count ratios per five official days for hospitalisations after CHD diagnosis (left) and HF diagnosis (right). Blue circles represent 2013–2019 and orange squares represent 2013–2023; horizontal bars are Newey–West lag-6 95% intervals. The 84-month series is nested within the 132-month series, and the spline bases were reconstructed separately. These estimates are dependent and cannot be treated as an independent pre/post contrast. A separate post-period coefficient and formal difference test are unavailable. The full twelve-contrast primary exploratory family has Benjamini–Hochberg q-values above 0.19.

**Source and numerical contract:** exactly twelve rows from two outcomes, three exposures and two scenarios. Both panels use the same log count-ratio scale and a reference line at one. No arrows linking points, difference coefficients, significance stars or post-period markers are drawn.

## Six planned figure functions: actual availability

1. **Study design/observation process — AVAILABLE CONCEPTUAL ONLY.** Event semantics require query confirmation. Confirmed cohort flow awaits governed construction counts.
2. **Longitudinal burden — AVAILABLE COUNTS ONLY.** Eligible population, incidence and mortality panels require new evidence and are not drawn.
3. **Clinical and care trajectories — REQUIRES NEW GOVERNED DATA.** No laboratory, treatment or care-contact trajectory is invented.
4. **Weather contrasts — EXISTING OVERLAPPING FITS ONLY.** Formal common-basis period interactions are NOT ESTIMATED. Supplement Figure S1 visualises the existing limited object.
5. **Model criticism — AVAILABLE FIXED RELEASED SENSITIVITIES.** The present figure is calendar/start-window criticism. New-plan calibration and justified falsification tests are not claimed as executed.
6. **Validation — REQUIRES HARMONISED INDEPENDENT EVIDENCE.** Published comparator studies provide context, not a replication estimate of this extract.

## Provenance, reproducibility and review

Every figure has PNG, vector PDF and editable-text SVG exports, a minimal source CSV and an entry in `figures/covid_period/evidence_figures_manifest_20261002.json`. The manifest binds source-file and output hashes. Colour choices follow distinct blue/orange tones and marker shapes; interval panels have an explicit reference at one.

The first visual inspection found overlapping legend placement in the nested-window panel and unwanted scientific notation from automatic log-axis minor ticks. Both were repaired and all four figures re-rendered. Independent parent-agent inspection found readable bounds and labels, no clipped intervals, and an appropriately conceptual observation diagram. Subsequent metadata revision clarified that the model-criticism display includes baseline plus six checks, while phase adjustment remains in the supplement.

The same ten-slide internal Research State Briefing is updated, with editable tables and the annual index chart. It identifies the 2025 diabetes and hypertension precedents and 2026 care-continuity paper, their access limits in speaker notes, the feasible current claims, the absent mechanism data, and the novelty/data gate. No journal acceptance, governance approval, new clinical analysis or external validation is implied.

The briefing source is `scripts/85_covid_research_briefing.mjs`. It uses the bundled Artifact Tool, retains the original 1280 × 720 layout and Arial typography, verifies six native table owner slides and an editable chart with an embedded source workbook, and updates the same PPTX. Runtime paths have `LAIDLAW_` overrides. Rebuild its PDF using the bundled `dependencies/bin/override/soffice` converter, never an installed desktop LibreOffice. Its annual index is rounded to six decimals for workbook portability; counts in the manuscript figure remain integer totals.

All ten pages of the final bundled-renderer PDF were inspected individually. The first deck pass exposed close spacing between the rival-table caption and source footer; reducing that table's height restored spacing, followed by regeneration and inspection of the final page. Technical finalisation records remain in the ignored build directory, separate from the deliverable.
