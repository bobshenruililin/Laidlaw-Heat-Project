# Opus professor pass — natures of the deliverables, 14 August 2026

**Role:** senior environmental-epidemiology reader and methods editor, sitting on the 14 August board (`2026-08-14_yc_board_charter.md`).
**Mode:** Decide. Residue only — no code, no new numbers, no health claim, no freeze-lift.
**Rails observed:** monthly ecological CHD/HF first-hospitalisation count ratios, 132 months, T2D/HTN cohort, admission cause absent, stroke not attached, Gate 3 open, all core *q* > 0.19. Frozen PDFs stay frozen. Live paper stays on HKO Headquarters. Every numeral below already exists in a repo file; the three taken from the parent's in-flight threshold build are labelled where they appear.

---

## The intellectual product

(a) **Exposure geometry — this is the finding.** On 4,017 shared days at one coordinate, "a hot night" is 449 nights at HKO Headquarters, 17 on ERA5-Land dry-bulb, 1,453 on the same grid's apparent temperature, 252 in the Waglan cell. The grid flags only 17, so at most seventeen of the station's 449 can be the same night; Jaccard 0.031 says fewer.
Night bias is −1.47 °C; adding it back recovers 378 nights. **Whether it recovers the same nights was nowhere in the knowledge base when this pass was written, and that is the quantity the summer is missing.**
A methods editor knows reanalysis is biased. What is not standard is the operational demonstration that a threshold-defined *flag* can be recalibrated in frequency while remaining unrecoverable in timing — and that inside one territory the flag's geography is marine (Gi\* hotspots on water; Guangzhou box 12.1 nights, Huizhou 0.2).
Separately, EOF1 of de-seasoned Tmin holds 92%, holdout- and bootstrap-robust: the basin's daily anomaly field has about one degree of freedom, so extra cells add almost no independent exposure information.

(b) **CHD/HF associations — no discovery.** Twelve contrasts, all *q* > 0.19. The two intervals excluding 1 are fragile in opposite directions: CHD hot nights (1.022, 1.002–1.042) is confined to specifications including 2020–2023 (pre-2020: 1.011, 0.991–1.032) and rests on a robust variance smaller than the model variance; HF cold days (1.073, 1.006–1.144) is carried by three dozen winter months (141/145 cold days fall in December–February).
The honest product is a declared no-primary panel. The publishable sentence lives in (a); the panel's discipline is what keeps (a) credible.

---

## Natures of the scientific deliverables

| Object | Estimand / encoding | What it is allowed to claim | What a reviewer would reject | How to make it better without new HA data |
|---|---|---|---|---|
| **Stage 3 essay PDF** (`6136e85a…`) | No estimand of its own; a programme narration of the CHD/HF panel and its refusals | That a scholar built a governed panel, ran it, and declined to name a primary | Nothing — provided it is never cited as a results source | Do not touch it. Corrections belong in LSN/blog/live file. A frozen artefact that disagrees with a later manuscript is normal; a rebuilt one is a provenance incident |
| **Live manuscript** (Hogan's shared file) | Monthly count ratio, CHD/HF first hospitalisation after first diagnosis, T2D/HTN cohort, HKO Headquarters exposure, days offset, NB + month factor + `ns(time,4)` | Comparative panel description with explicit no-primary and BH *q* reported | The Newey–West rationale sentence (Table 3 narrows, contradicting it); asymmetric sensitivity reporting; the superlative Conclusion; no single-station limitation | Paste the three mandatory Fable edits; add the exposure-geometry limitation *with* 1.47 °C and Jaccard 0.031 instead of a qualitative hedge; swap Figure 3 for `figure4_trend_depletion_sensitivity` |
| **Repo manuscript** + supplement | Same estimand, fuller method and release validation (29/29) | Reproducibility of record | Being read as a second paper; any numeral that has drifted from the live file | Label it a supplement-of-record and keep a short diff note against the live file so the divergence is intentional, not accidental |
| **HKO vs ERA5 calibration** | Measurement-error characterisation of a threshold-defined binary exposure at one coordinate: bias −1.47 °C, RMSE 1.97 °C, Jaccard 0.031, count-recovery 378/449 | Station and same-coordinate reanalysis hot-night flags are not exchangeable in Hong Kong; count agreement and day agreement are different properties | "Validation of ERA5" from n = 1 coordinate; silence on the fact that the Headquarters pixel is a mixed land–sea harbour cell and near the worst case; silence on Open-Meteo's DEM/lapse downscaling; a Jaccard with no uncertainty on serially dependent nights | Add one or two further HKO open-data stations (public) as replicates; report sensitivity and positive predictive value of the grid flag against the station flag, not only Jaccard; state the site as a stated worst case rather than let a referee say it |
| **HK lattice** (`docs/geo/`) | Cross-sectional climatology of thirty 0.1° ERA5-Land cells; `Tmin ~ elevation (+ coast / lat / lon)`, R² 0.546 → 0.882 | Within-territory exposure heterogeneity is large relative to the distance between "cousin" cities; the station is one draw from a field | OLS inference at n = 30 with residual Moran's I 0.34–0.67; and the elevation coefficient (−0.0062 °C/m) is close to the lapse rate the downscaling imposes, so it partly measures the product | Say the elevation term is a diagnostic of the product, compare it to the standard environmental lapse rate, drop the regression's *p*-values, and keep the leave-one-out Headquarters error (0.28 °C) as the honest headline |
| **PRD mosaic** (`docs/prd/`) | 90-cell 0.2° climatology; OLS R² 0.890, SLX 0.906, SAR-2SLS ρ 0.45 (SE 0.12); Gi\* 17 hotspots, 0 coldspots | On this product the 28 °C night is a marine object; exporting the Headquarters flag up the river is a larger spatial act than exporting it across the harbour | SAR ρ on a smoothed reanalysis field as spatial spillover science — the input is already autocorrelated, so ρ is close to a property of the interpolation; an R² quoted for a 2SLS fit; Gi\* on 90 cells with no multiplicity or edge handling | Reframe SAR/SLX as descriptions of the product's smoothness. Then add the one thing that changes the argument: population-weighted hot-night counts, so the map speaks about people rather than pixels |
| **Field laboratory / EOF** (`docs/field/`) | Space-time decomposition of the same 4,017 × 90 de-seasoned Tmin cache | EOF1 92.1%, three EOFs 96.2%, harmonic peak day 198–207, HQ–Guangzhou anomaly *r* 0.89: the daily anomaly field is effectively one-dimensional | EOF1 as a hot-night map (it anti-correlates, *r* = −0.93) or as a health factor; Theil–Sen +0.29 °C/decade with 23/90 CIs as a trend detection (0/90 survive BH 10%); the *r* > 0.90 network as an object (26 edges once EOF1 is removed) | Translate 92% into a design statement: the number of independent daily exposure series in this basin is nearer one than ninety. That sentence constrains any future spatial heat-health design and costs nothing |
| **HM/CM catalogue** | A definition space: HM01–HM50, CM01–CM48, provisional study-window reference period | The choice set, and its function as a pre-specification device before outcomes are opened | Any coefficient from an unlocked family; a 98-definition menu fitted after seeing outcomes is a multiplicity machine, whatever the BH correction says | Lock a small core with Hogan and register the rest as sensitivity. Then measure the definition space on **exposure only**: how many months each definition flags, and how nearly collinear the 98 monthly series are. If they collapse to a handful of dimensions, the honest multiplicity is smaller than 98 and the *q* discussion changes |
| **Gate 3 packet** | A decision object, not an analysis | That no confirmatory primary was declared, and why | Nothing scientific; it becomes a liability only if a headline appears in public before the team closes it | Convert Option A from internal gate language into one manuscript design sentence: the family was treated as exploratory, no primary was pre-declared, and BH *q* is reported for all twelve |

---

## Verdict on "move the night"

**As proposed, it is a visualisation of a bias we have already stated.** Counts moving when a threshold moves is arithmetic. A slider showing 449, 17, 1,453, Waglan and Guangzhou changing together restates the calibration table with animation. Hogan cannot keep a slider, and a methods editor would call it a teaching aid.

**There is a real contribution inside it, and it is not the count.** The interesting quantity is the decoupling of *frequency* agreement from *set* agreement as the grid threshold moves. Three additions would make it a figure Hogan could keep:

1. **The count-equivalent threshold.** The ERA5 threshold *t\** at which the grid produces about 449 hot nights. Report *t\** and the implied offset, alongside the +1.47 °C mean-bias correction that produces 378. Two different recalibrations, two different thresholds, one honest comparison.
2. **Jaccard(*t*), and its maximum.** Agreement between the station's fixed 28 °C set and the grid set as a function of *t*. The claim worth making is about **max*_t_* Jaccard: if agreement is still low at its own optimum, then no monotone recalibration of a reanalysis threshold can reproduce the station's nights, because the two series disagree in rank order near the tail and not merely in level. That is a general statement about threshold-defined exposures, not a Hong Kong curiosity. If max*_t_* Jaccard turns out high, the finding reverses and bias correction is defensible — either way the figure earns its place. Do not assume the direction before running it.
3. **Sensitivity and PPV(*t*), and marine share of cell-nights at *t*.** Epidemiologists read misclassification as sensitivity and predictive value, not as Jaccard. And the marine share — what fraction of the 90-cell hot-night mass sits over water at threshold *t* — is the one line that connects the encoding argument to the geography argument.

**Ship only if** it carries the count-equivalent threshold and max*_t_* Jaccard (or the sensitivity/PPV pair), and ships as a static two-panel figure with axes first and an interactive version second. **Kill** the version that is only a slider over counts. Honesty constraints: exposure only, one coordinate, ERA5-Land via Open-Meteo with DEM lapse correction, no health series in the figure, and no implication that the live paper should move off Headquarters — the figure argues the opposite.

**Note on the in-flight build.** While this pass was being written the parent produced `scripts/53_threshold_does_not_travel.py` and `outputs/threshold_demo/` (untracked at the time of writing; I did not verify the computation). Its slim output already contains items 1 and 3: a count-equivalent ERA5 threshold of 26.4 °C giving 448 nights against HKO's 449 at 28 °C, the reverse match (HKO 29.5 °C ≈ ERA5's 17), Jaccard as a series over 25 coarse and 121 fine thresholds, and marine share of cell-nights (0.778 at 28 °C). That is the right skeleton. Two things remain before it is a figure Hogan can keep: **max*_t_* Jaccard must be extracted and named in the caption** — a curve a reader has to eyeball is not a claim — and **sensitivity/PPV of the grid flag against the station flag** should sit beside Jaccard, because that is the form a health referee reads. The reported intersection of 14 nights at 28 °C is also worth stating in words: the grid's seventeen hot nights are almost all real, and they are almost none of the station's.

---

## Ideas beyond a fifth map

Ranked by whether a journal reviewer would change a sentence because of them.

**1. Monthly-grain exposure agreement and the attenuation slope.** Our exposure is not a night; it is a *monthly count* of hot nights over 132 months. The right agreement statistic is therefore at monthly grain: correlate and regress the grid's monthly hot-night count on the station's, and report the slope. A slope below one is classical attenuation, and it says, without touching an outcome, by roughly how much any coefficient estimated on a reanalysis exposure would be biased toward the null. This converts the Limitations hedge into a number and is the single most useful thing that can be built from existing caches. *Constraints:* one coordinate, one product; it bounds a hypothetical grid-based analysis, not our HKO-based estimates; state that the failed clean-room daily-recovery calibration is why no daily version of this exists.

**2. Effective identifying months per contrast.** With calendar-month indicators plus `ns(time,4)`, each contrast is identified between years within month. Hot nights are a summer object and cold days are 141/145 December–February, so the effective information behind the twelve intervals is a few dozen months, not 132. Print, for all twelve contrasts, the number of months carrying exposure variation and the between-year within-month share of that variation. Most heat–health papers report *n* and never report this. It reframes *q* > 0.19 from a multiplicity accident into a design fact. *Constraints:* the month counts must be read off the exposure files, not asserted; the DJF figure from the night-explore note is still flagged EXPLORE-ONLY and needs verifying before it is quoted.

**3. Effective dimension of the HM/CM definition space.** Ninety-eight definitions is a menu, not a panel. Compute, on exposure only, the correlation structure of the 98 monthly series and its effective rank. The likely honest result is that the family collapses to a small number of dimensions, which simultaneously reduces the real multiplicity burden and tells Hogan which definitions are genuinely different from `HM23`. That is a direct input to his lock and it needs no outcome. *Constraints:* an effective-rank statement is not a licence to fit more definitions, and it must be produced before outcomes are re-opened, not after.

**4. A time-shifted negative-control exposure.** Re-fit the twelve core contrasts with the exposure series displaced by whole years (same calendar month, wrong year). Under the stated design, the month indicators and the trend spline should absorb a displaced exposure. If a displaced hot-night series reproduces a ratio near 1.022, the CHD result is a trend artefact and the paper should say so; if it does not, "confined to specifications including 2020–2023" becomes a test rather than an observation. Uses only governed aggregates already in hand. *Constraints:* this generates new numbers, so it needs a human nod and a Gate-3-open label; a pass does not upgrade any *q* and must not become a new headline.

**5. Population-weighted exposure geometry.** The Gi\* hotspots sit on the water and the highland cluster records zero hot nights. Weight the HK lattice and the PRD mosaic by public gridded population and report the population-weighted hot-night count next to the unweighted one. This is what turns four exposure maps into one argument about who is exposed, and it is the version a health-policy reader can use. *Constraints:* population weighting does not repair the 1.47 °C bias; the result stays a grid object; no health counts on cells, no transport of CHD/HF ratios.

---

## What would impress a professor in the room

Not the eight methods. The sentence they would quote:

> "At one coordinate, on the same 4,017 nights, the Observatory calls 449 nights hot and the reanalysis calls seventeen — so at most seventeen of them can be the same night."

The follow-up is what makes it research rather than a fact: adding back the 1.47 °C night bias recovers 378 nights, and the overlap between that recovered set and the station's has not been reported anywhere in the project. A professor will recognise that as a well-posed question with a cheap answer, which is the most flattering thing a piece of student work can be. The threshold demo is where it should be answered.

The second sentence, for the health side, is a refusal: twelve contrasts, no primary declared, and the reason printed in the paper rather than in a reviewer's report.

---

## What would impress YC without lying

**The honest wow.** A city's official heat definition is not portable, and the failure is measurable rather than rhetorical: same place, same nights, one threshold, a factor of twenty-six between instruments, and near-zero overlap in which nights were flagged. Every heat-health claim in the literature rests on an encoding, and almost none of them publish what changing the encoding would do. A tool that re-runs a heat definition against the instrument that produced it is a real product surface, and the demo is sixty seconds: move the threshold, watch the flag leave the city and settle on the water.

**The dishonest wow, all of which are available and all of which are off-limits.** "Hot nights raise heart attacks in Hong Kong." "AI ran eight spatial methods overnight." "92% of the delta's temperature variance explained." "+0.29 °C per decade in the Pearl River Delta." A health map with colour on it. Each of these would land better in a room and each would be the end of the project's credibility with Hogan, Roro, and Bishai — the three people whose judgement actually gates this work.

The discipline is the pitch. A team that can say which of its own numbers are not allowed to be findings is the team you would fund.

---

## Kill list

**Claims**

- Theil–Sen +0.29 °C/decade and "23 of 90 CIs exclude zero" anywhere except inside an explicit negative caveat. 0/90 survive BH at 10%.
- EOF1 92% quoted as a result rather than translated into "the field has about one degree of freedom." EOF1 as a hot-night map or a health factor.
- The *r* > 0.90 correlation network as an object. Twenty-six edges survive EOF1 removal; it is a check, not a discovery.
- SAR ρ 0.45 presented as spatial spillover science on a smoothed reanalysis field.
- k-means cluster labels used as neighbourhoods, catchments, or municipalities.
- P(HN | VHD) = 0.43 as *the* number; the pooled value is 0.31.
- Apparent-temperature counts (1,453; Singapore 3,317) quoted as hot nights.
- The superlative Conclusion in the live manuscript ("largest positive thermal association") — the panel cannot rank.
- The Newey–West "model-based intervals are too narrow" rationale, refuted by the paper's own ladder.
- "Continuity" as an undefined internal term, fifteen times.
- Any sentence implying the live paper could move off HKO Headquarters, or that ERA5 is a replacement station.

**Pages**

- A fifth Leaflet map. Four exposure companions already make one argument; a fifth makes none.
- The `docs/` set as four independent stories. Peers, geo, prd, and field are one claim about encoding, place, and dimension, and they should read as one.
- Any public page that acquires a coefficient.
- Reopening the frozen Stage 3 report or A0 poster to reconcile them with later prose.

**Analyses**

- New spatial methods on the same 90-cell cache. The cache has been read; the eighth method told us what the first did.
- Any further definition added to HM/CM before Hogan's lock.
- Any fitted object that requires stroke, daily outcomes, or admission cause.

**The dilution to watch.** The intellectual product this summer is a measurement-and-identification argument about what a hot night *is*, wrapped around a health panel honest enough to decline a headline. Everything that does not sharpen one of those two things is subtraction, however good it looks on a map.

---

*Residue: this memo. No other file was edited, no analysis was run, no number was created. Board context: `2026-08-14_yc_board_charter.md`. Companion passes: `2026-08-14_strong_model_synthesis.md`, `2026-08-13_fable_live_doc_critique.md`.*
