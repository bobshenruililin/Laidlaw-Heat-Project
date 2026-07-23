# Roro manuscript deep-read — medRxiv v1 baseline

## Version and provenance

**Working source:** Liu Z, Ren C, Liu J, Kawasaki Yurika, Bishai DM. “Modelling the Excess Mortality Associated with Heat Waves in Hong Kong: 2014–2023.” *medRxiv*, posted 6 March 2026. DOI [`10.64898/2026.03.05.26347683`](https://doi.org/10.64898/2026.03.05.26347683).

**Version boundary:** this is a deep-read of **medRxiv v1**, checked against both the recovered PDF-to-text extraction in `literature/source_pdfs/roro_liu2026_medrxiv_heatwave_excess.txt` and the supplied HTML extraction. The user’s Mac file, `revised manuscript_clean.pdf`, has **not yet been ingested in the cloud**. Any revised wording, analyses or tables remain pending comparison with that PDF.

This preprint is a team baseline, not a result of the monthly stroke project. It estimates model-based excess **mortality** under heatwave scenarios; our project will estimate associations with monthly stroke-event aggregates.

## One-paragraph read

The manuscript converts published Hong Kong heat–mortality relative risks (RRs) into absolute excess-death estimates for 2014–2023. It applies four local heatwave definitions to Hong Kong Observatory (HKO) temperatures, constructs counterfactual expected daily deaths from age–sex life-table rates and population, combines age- and sex-specific RRs on the log scale, propagates RR uncertainty through 1,000 Monte Carlo draws, and reports excess deaths and age-standardized rates. Depending on the heatwave definition, it estimates **1,455 (95% CI 1,098–1,812) to 3,238 (3,234–3,242)** excess deaths over ten years. In 2023, the reported age-standardized excess-death rates range from **2.95 (2.41–3.50) to 5.09 (5.07–5.12) per 100,000**. The policy argument is that a preventable heat burden of this scale is comparable to diabetes mortality and warrants a Hong Kong Heat Action Plan (HAP), particularly for men and older adults.

## Manuscript architecture and argumentative intent

1. **Introduction — translate risk into burden.** Prior Hong Kong studies establish temperature–mortality RRs and attributable fractions, but absolute death counts are easier to communicate. The manuscript positions excess deaths as a way to include direct and indirect heat effects that death certificates may not label as heat-related.
2. **Methods — transport local RRs into 2014–2023 burden scenarios.** Four definitions represent distinct heat dimensions: high mean temperature with a long lag, prolonged hot days, prolonged hot nights, and combined hot days and nights.
3. **Results — definition sensitivity is substantive.** Event counts, exposed days and excess deaths differ sharply by definition. The range is therefore part of the result, not merely a sensitivity footnote.
4. **Discussion — make the burden legible.** Diabetes mortality is used as a policy benchmark; age, cooling behavior, energy cost and housing ventilation motivate targeted prevention.
5. **Policy conclusion — build a HAP.** The paper calls for a territory-wide, multisectoral plan with warnings, public advice, clinical counseling and social-care outreach.

## Data and target quantity

| Component | What the manuscript uses |
|---|---|
| Study window | 1 January 2014–31 December 2023 |
| Exposure | HKO daily temperature series from one station |
| Baseline deaths | Expected age–sex daily deaths from Hong Kong Life Tables and corresponding C&SD population |
| Effect inputs | Published local heat–mortality RRs from Jingwen Liu et al. (2020) and Wang, Ren et al. (2019) |
| Output | Model-based excess heat-related deaths (EHDs), totals and annual age-standardized rates per 100,000 |
| Uncertainty | 1,000 simulated RR draws; 95% CIs reported using the manuscript’s stated normal-approximation/bootstrap procedure |
| Software | Stata SE 18 |

The calculation is not a new daily time-series regression of observed 2014–2023 deaths on temperature. It applies transported RRs to counterfactual expected deaths. “Excess deaths” should therefore be read as **RR-based attributable excess under the stated scenarios**, not as a classical observed-minus-forecast excess-mortality series.

## The four heatwave definitions

| Label | Operational intent in medRxiv v1 | RR and lag source |
|---|---|---|
| `HWD_Tavg` | A 20-day period starts when daily mean temperature crosses the 99th-percentile threshold of **30.60°C**. The table writes `≥30.60°C`, while the prose says “exceeds.” An event start must be at least 20 days from the last threshold-exceeding day. | Jingwen Liu et al. (2020). Daily RRs are grouped into day 0, days 1–5 and days 6–21. |
| `HWD_Tmax` | A very hot day has daily maximum temperature **≥33°C**; consecutive VHDs form a prolonged 5HD/5VHD pattern. The table also says a run “longer than 5 days,” which should be resolved before exact recoding. | Wang, Ren et al. (2019). Daily RR; the manuscript says no detailed post-event lag statistics are supplied for this pattern. |
| `HWD_Tmin` | A very hot night has daily minimum temperature **≥28°C**; consecutive VHNs form a prolonged 5HN pattern. The same “longer than 5 days” wording appears. | Wang, Ren et al. (2019). Daily RR; no detailed post-event lag statistics are supplied in the table. |
| `HWD_Tcombined` | A 2D3N event combines two consecutive days with maximum temperature **≥33°C** and three consecutive nights with minimum temperature **≥28°C**. | Wang, Ren et al. (2019). RR phases cover event days and the subsequent five days. |

The definitions are not four labels for one exposure. They vary in threshold variable, persistence, lag coverage and imported RR. Differences in estimated deaths therefore reflect both **how exposure is counted** and **which effect estimate is transported**.

## Equations: what each is trying to do

### 1. Construct an age-by-sex RR

\[
\log(RR_{\mathrm{age,sex}})
=
\log(RR_{\mathrm{age}})
+
\log(RR_{\mathrm{sex}})
-
\log(RR_{\mathrm{all}}).
\]

The intent is to synthesize separately published age and sex RRs into the age–sex cells required by the life tables. Subtracting the overall log-RR avoids counting the common population effect twice. This imposes additivity on the log scale; it is not a directly estimated age-by-sex interaction.

### 2. Draw uncertain RRs on a log-normal scale

\[
RR
=
\exp\left[
\operatorname{invnorm}\{\operatorname{uniform}(\mathrm{rand})\}
\times \log SD
+ \log RR
\right].
\]

The intent is to sample 1,000 positive RR values using a normal draw on the log scale and then exponentiate. The resulting simulation propagates uncertainty from the imported RR inputs. The medRxiv notation calls the spread term `logSD`; implementation details should be checked in the revised manuscript or code before reproduction.

### 3. Convert an RR into excess deaths for a heatwave phase

\[
EHD_{ij}
=
(RR_{ijt}-1)\times DD_{ij}\times L_t,
\]

where \(i\) indexes sex, \(j\) age, \(t\) the heatwave phase, \(DD_{ij}\) the expected daily deaths without a heatwave, and \(L_t\) the phase duration in days. The equation asks: if baseline deaths are \(DD\), how many additional deaths arise when risk is multiplied by \(RR\) for \(L\) days? Simulated cell-level EHDs are aggregated across heatwave occurrences, years, age and sex.

The manuscript then age-standardizes rates to the WHO 2001 world standard population. Counts are presented without time discounting or normative age weighting; that burden-valuation choice is distinct from statistical age standardization of rates.

## Results: tables and figures in narrative

### Exposure frequency

| Definition | Events, 2014–2023 | Heatwave days |
|---|---:|---:|
| `HWD_Tavg` | 18 | 360 |
| `HWD_Tmax` | 25 | 183 |
| `HWD_Tmin` | 26 | 190 |
| `HWD_Tcombined` | 38 | 365 |

`HWD_Tcombined` is most frequent and covers the most days. `HWD_Tavg` covers almost as many days but packages them into only 18 long lag windows. `HWD_Tmax` has the fewest exposed days.

### Total and 2023 burden

| Definition | Ten-year excess deaths (95% CI) | 2023 excess deaths (95% CI) | 2023 age-standardized rate per 100,000 (95% CI) |
|---|---:|---:|---:|
| `HWD_Tavg` | 1,455 (1,098–1,812) | 257 (193–322) | 2.95 (2.41–3.50) |
| `HWD_Tmax` | 2,262 (2,170–2,353) | 282 (271–293) | 2.63 (2.52–2.75) |
| `HWD_Tmin` | 1,553 (1,549–1,557) | 213 (203–224) | 2.05 (2.04–2.07) |
| `HWD_Tcombined` | 3,238 (3,234–3,242) | 575 (562–589) | 5.09 (5.07–5.12) |

The combined definition yields more than twice the ten-year estimate from the mean-temperature definition. Annual counts do not move identically: `HWD_Tmin` is zero in 2018, `HWD_Tmax` peaks at 496 deaths in 2022, and `HWD_Tcombined` reaches 538, 547 and 575 in 2021, 2022 and 2023. The rising recent combined-definition series carries much of the policy force.

Table 3 compares annual age-standardized heat estimates with diabetes mortality. The manuscript describes heat as comparable to diabetes and states that the `HWD_Tmax` and `HWD_Tcombined` scenarios exceed diabetes in nearly half the study period, concentrated in 2020–2023. The row-level comparisons are definition- and year-specific; they should not be compressed into “heat always exceeds diabetes.” In 2023, for example, the table reports diabetes at 2.8 per 100,000, below `HWD_Tavg` and `HWD_Tcombined` but above `HWD_Tmax` and `HWD_Tmin`.

### Demographic pattern

- Males carry nearly twice the estimated burden of females for most definitions; the nighttime definition is the exception.
- People aged **65 years or older** are disproportionately affected.
- The **85+** group has the largest burden under `HWD_Tmax`, `HWD_Tmin` and `HWD_Tcombined`; the mean-temperature scenario is an exception in Supplementary Table S3.
- These subgroup patterns inherit the published RR inputs and the life-table population/death structure. They are not newly estimated effect modification from individual 2014–2023 mortality records.

## Strong contributions

1. **Policy translation.** Absolute deaths and rates are more legible than RRs alone.
2. **Local evidence chain.** HKO temperatures, Hong Kong population/life tables and Hong Kong RRs avoid importing effects from a different climate.
3. **Definition pluralism.** Four scenarios honestly show that heatwave burden depends on exposure construction.
4. **Uncertainty propagation.** Monte Carlo draws carry RR uncertainty into burden intervals instead of reporting point calculations only.
5. **Demographic focus.** Sex and age patterns make the prevention target concrete, especially for the oldest residents.
6. **Actionable endpoint.** The HAP recommendation connects warnings, clinical counseling, energy poverty, housing and outreach.
7. **Team continuity.** Jingwen Liu (“Jasmine”) and Chao Ren connect the 2020 RR study to this burden analysis; Zhenyuan Liu (“Roro”) turns that evidence into a 2014–2023 policy metric.

## Gaps and questions to resolve

These are opportunities for clearer estimation, not reasons to dismiss the paper.

1. **Transport rather than re-estimation.** RRs from 2006–2016 and 2006–2015 are assumed to apply through 2023. Adaptation, population change, care, housing and the COVID period could alter the relationship.
2. **Meaning of “excess.”** Expected deaths come from life-table rates × population rather than an observed-death time-series counterfactual fitted for 2014–2023. The manuscript should foreground that distinction.
3. **Combined age–sex assumption.** Equation 1 synthesizes marginal RRs; it does not estimate joint effect modification.
4. **Uncertainty scope.** Intervals appear to propagate RR uncertainty, but not definition choice, threshold estimation, baseline mortality, population projections, exposure error or model transport. Very narrow intervals for some definitions should not be mistaken for total uncertainty.
5. **Operational ambiguities.** `≥` versus “exceeds,” “5HD” versus “longer than 5 days,” threshold reference-period construction, and event overlap rules need executable definitions.
6. **Single territory exposure.** One HKO station and equal exposure for all residents omit urban heat-island, housing, occupation and district differences.
7. **No spatial socioeconomic analysis.** The limitations acknowledge education, occupation, SES and physical condition, but the estimates cannot locate inequitable risk.
8. **Heat only.** The design does not quantify cold, despite Jasmine’s cold-dominant attributable fraction.
9. **Mortality only.** It cannot show nonfatal stroke morbidity, hospital burden or service demand.
10. **Coarse/mismatched source age bands.** RR strata differ across source definitions, limiting direct comparisons and targeted inference.
11. **Reporting checks.** Table 3 prints the 2017 `HWD_Tavg` rate as 0.88 with CI (1.74, 0.87), which cannot be an ordered confidence interval. Supplementary Table S3 includes negative EHDs in some cells. These may follow RR values below 1 or be transcription issues, but should be explained rather than silently cleaned.
12. **Reproducibility.** The paper says data are public and in the manuscript/supporting information; sharing executable heatwave and Monte Carlo code would make the scenario calculations easier to audit.

## How the monthly stroke project can exceed this baseline without competing with it

- **Add morbidity:** estimate associations with real monthly stroke-event aggregates rather than relabeling mortality coefficients as stroke effects.
- **Treat hot and cold symmetrically:** run paired HM/CM definitions, including continuous burden, spells and selected thresholds, rather than heat-only scenarios.
- **Use the later window directly:** estimate the project’s 2013–2023 association from its own outcome series; do not assume the 2006–2016 RR is unchanged.
- **Sharpen age actionability:** preserve ages 65–69 and 70–74 if Roro’s approved aggregates support them, while retaining older bands.
- **Stage pollution and influenza:** separate base thermal estimates from pre-specified pollution, humidity and influenza sensitivities; do not let adjustment sets drift with significance.
- **Audit definitions before outcomes:** publish selected-month lists, event counts, threshold reference periods, overlap handling and missingness.
- **Report the right estimand:** monthly stroke rate/count associations are neither Jasmine’s daily distributed-lag AFs nor Roro’s model-based excess deaths.
- **Keep equity ambitions honest:** use spatial or SES strata only if approved data support them; otherwise name the gap rather than implying it has been closed.

The strongest paper family is cumulative: Jasmine establishes the cold/heat mortality surface and attributable fractions; Roro translates selected heat RRs into absolute policy burden; the stroke panel adds later-period morbidity, symmetric heat/cold definitions and clinically actionable age structure.

## Authorship credit

The medRxiv manuscript reports:

- **Concept or design:** David Makram Bishai
- **Data acquisition:** Jingwen Liu and Chao Ren
- **Analysis or interpretation:** Zhenyuan Liu
- **Drafting:** Zhenyuan Liu and Kawasaki Yurika
- **Critical revision:** Chao Ren, Jingwen Liu and David Makram Bishai

That division of work should remain visible whenever the paper is used as the project baseline.
