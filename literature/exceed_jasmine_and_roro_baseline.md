# Exceeding the Jasmine and Roro baselines — writing and science plan

## The standard to exceed

“Exceed” means adding a defensible scientific layer while crediting and preserving the earlier estimands. It does **not** mean claiming that monthly stroke data supersede daily mortality work.

| Evidence layer | What it already does well | Boundary our project should not blur |
|---|---|---|
| **Jingwen Liu et al. 2020 (“Jasmine”)** | Daily 2006–2016 temperature–mortality surface; DLNM/quasi-Poisson; cause-specific RRs and AFs; cold/heat and moderate/extreme decomposition | Daily mortality AFs are not monthly stroke coefficients |
| **Zhenyuan Liu et al. 2026 (“Roro”), medRxiv v1** | Converts local RRs into 2014–2023 absolute excess heat deaths under four definitions; age/sex burden; HAP argument | RR-based excess mortality is not observed monthly stroke morbidity |
| **Bob/Hogan/Roro monthly panel** | Can directly study 2013–2023 stroke-event aggregates using a symmetric, auditable hot/cold exposure panel | Monthly ecological associations cannot identify daily triggering, individual causality, genes or excess deaths |

The family contribution is cumulative:

- Jasmine establishes **how non-optimal temperature relates to mortality**, with cold burden much larger than heat burden in 2006–2016.
- Roro establishes **how large heat-attributable excess mortality may be in absolute terms** under alternative 2014–2023 heatwave scenarios.
- The stroke project can establish **whether later-period monthly stroke morbidity covaries with pre-specified hot and cold burdens**, and for whom, without borrowing a mortality coefficient.

## Six ways the stroke project can add genuinely new science

### 1. Move from mortality to morbidity

Use Roro’s approved stroke aggregates assigned to the **true stroke-event month**. First GOPC mention is a marker, not automatically the event date. This adds nonfatal clinical burden and service demand that neither mortality paper estimates.

Primary writing rule:

> We estimate monthly associations with stroke-event aggregates; we do not estimate daily triggers, attributable fractions or excess deaths.

If subtype is absent, report pooled stroke. If subtype is present and approved, enable the pre-labelled subtype pathway rather than retrofitting it after results.

### 2. Make hot and cold exposure symmetric

Jasmine shows why cold cannot be a token sensitivity; Roro shows why heat definitions cannot be singular. The project should pre-specify matched hot-month (`HM`) and cold-month (`CM`) families:

- continuous mean, maximum and minimum temperature;
- official extreme-day counts;
- hot and cold spell duration/burden;
- relative upper- and lower-tail months;
- event starts versus event-day burden;
- onset and persistence; and
- clearly labelled compound definitions.

Symmetry means parallel coding, exposure audits, reporting and multiplicity discipline. It does not require thresholds to be numerically mirror images when physiology or official definitions differ.

The `H11`/`C11` source-definition pathways should preserve Jasmine’s exact rules only after the full PDF/supplement is transcribed. Roro’s four heatwave definitions belong in a separately labelled burden-definition family. No definition should be promoted because it produces the smallest p-value.

### 3. Directly estimate the later period

Fit the monthly stroke models on **January 2013–December 2023** rather than assuming that an RR estimated in 2006–2016 transports unchanged. This can address a later morbidity estimand while acknowledging:

- only 132 monthly observations;
- seasonality and long-term trend;
- COVID-era changes in care and population;
- possible adaptation or exposure change; and
- the loss of daily temporal resolution.

Use the overlap with Jasmine’s window to validate exposure coding only unless source mortality outcomes are available. Do not call a definition transport an exact replication.

### 4. Stage pollution, humidity and influenza transparently

Pre-specify adjustment ladders:

1. thermal exposure + seasonality + long-term trend + appropriate offset;
2. add humidity/absolute humidity where available;
3. add pollution in fixed stages (for example NO₂/PM₂.₅ before O₃);
4. add influenza for cold-side sensitivity; and
5. run a labelled pre-COVID sensitivity.

Pollution and influenza can be confounders, co-exposures or pathway markers depending on the question. Do not automatically adjust away plausible pathways, and do not switch covariates to rescue significance. Report how estimates and uncertainty change across the pre-declared stages.

### 5. Preserve actionable older-age bands

If Roro’s governed aggregates support the requested granularity, retain:

- **65–69 years**
- **70–74 years**
- older groups consistent with disclosure control

This improves on a single 65+ category by aligning prevention with clinically and socially actionable age bands. If small-cell suppression or the delivered schema prevents those strata, say so; do not derive them from unavailable microdata.

### 6. Treat definition uncertainty as part of the result

For every HM/CM model, report:

- exact executable rule and threshold reference period;
- exposed-month count and complete selected-month list;
- missingness and cross-month event handling;
- model estimand and offset;
- effect estimate with interval, not significance alone;
- fixed multiplicity family;
- fit and residual diagnostics; and
- whether the output is primary, sensitivity or exploratory.

A compact coefficient panel, specification curve or multiverse summary can show stability without turning dozens of related models into independent discoveries. Primary inference should use a small frozen contrast; counts of “null” p-values are secondary.

## Honest estimands

| Quantity | Interpretable statement | Prohibited shortcut |
|---|---|---|
| Jasmine AF | Fraction of deaths attributable to modeled non-optimal temperature over the source period | “Cold causes 4.72% of strokes” |
| Jasmine RR | Distributed-lag mortality risk at a specified temperature contrast | Reusing it as a monthly morbidity RR |
| Roro EHD | Model-based additional deaths under baseline deaths × transported RR × exposed duration | Calling it observed heat-coded deaths |
| Monthly stroke coefficient | Association between a monthly exposure contrast and aggregate stroke count/rate under the specified model | Calling it a daily trigger, individual causal effect or excess-death count |
| HM/CM significance pattern | Secondary description of a frozen model universe | Treating p ≥ 0.05 as proof of no effect |

This table should inform the abstract, methods, results and discussion—not sit only in limitations.

## A manuscript structure that reads stronger

1. **Introduction:** begin with the family evidence chain, then name the missing morbidity/cold-symmetric question.
2. **Methods:** separate outcome construction, exposure reconstruction, estimand, model stages and multiplicity.
3. **Exposure audit:** show definitions and selected months before any association results.
4. **Primary results:** one frozen hot/cold pair with effect sizes and diagnostics.
5. **Structured robustness:** HM/CM family panel, pollution/flu stages and period sensitivity.
6. **Age results:** 65–69 and 70–74 only if delivered and disclosure-safe.
7. **Discussion:** compare questions and estimands, not coefficient magnitudes that are incommensurable.
8. **Policy:** connect mortality prevention and stroke-service burden without converting either into the other.
9. **Limitations:** monthly ecological resolution, exposure assignment, outcome timing, spatial/SES absence and low power for interactions.

## Claims the project may earn, but does not yet have

The completed analysis may be able to say that a result is stable or unstable across definitions, that cold and hot monthly estimates differ, or that an older age band carries greater estimated burden. At present there are **no real stroke coefficients**. Therefore:

- do not write that heat has replaced cold;
- do not write that one age group is more vulnerable;
- do not write that pollution or influenza modifies an effect;
- do not write that 10°C is a biological threshold; and
- do not infer genetic or ancestral adaptation.

The gene/adaptation and approximately 10°C ideas may motivate pre-labelled discussion and sensitivity analyses only. Housing, cooling, behavior, occupation, health care, age structure and acclimatization remain alternative explanations.

## Team-first execution

- **Jingwen Liu and coauthors:** source daily mortality evidence.
- **Zhenyuan Liu, Chao Ren, Jingwen Liu, Kawasaki Yurika and David Bishai:** source excess-heat mortality baseline.
- **Hogan:** weather framing, HM/CM definition lock and 65–69/70–74 emphasis.
- **Roro:** governed stroke aggregates, dictionary and true-event-month semantics.
- **David Bishai:** family-level scientific framing and extension question.
- **Bob:** reproducible analysis, pollution assembly and careful writing.

The strongest contribution is complementarity: one coherent Hong Kong evidence family spanning daily mortality, absolute heat burden and later monthly stroke morbidity.
