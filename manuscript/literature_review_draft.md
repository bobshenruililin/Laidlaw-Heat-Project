# Literature Review (draft)

**Project:** Thermal extremes and cardiovascular hospital burden in Hong Kong  
**Author:** Bob Shen  
**Date:** 10 July 2026  
**Status:** Working draft for supervisor review. Citations marked provisional must be verified before manuscript submission.

This review is organized by scientific theme rather than as an annotated bibliography. For each major source used below, the review distinguishes population, period, temporal resolution, outcome, exposure, lag structure, model, main result, relevance, and limitation for comparison with the present monthly 2013–2023 design.

---

## 1. Temperature and AMI

**Key verified source:** Goggins et al., weather/pollution and AMI in Hong Kong and Taiwan (daily data, ~2000–2009).  
- PubMed: https://pubmed.ncbi.nlm.nih.gov/23041014/

| Element | Detail |
|---|---|
| Population / setting | AMI hospitalizations in Hong Kong and two Taiwanese cities |
| Period | Approximately 2000–2009 |
| Temporal resolution | Daily |
| Outcome | AMI admissions |
| Exposure | Temperature (with humidity); pollutants |
| Lag / model | Multi-day average lags in GAM / related Poisson framework |
| Main result | In Hong Kong, cooler temperatures below an estimated ~24°C threshold associated with higher AMI admissions; no significant heat effect reported in that study; same-day NO₂ among strongest pollutant predictors |
| Relevance | Establishes the historical cold-dominant AMI baseline for Hong Kong |
| Limitation for comparison | Daily distributed-lag design and earlier decade; coefficients not directly comparable to monthly extreme-day counts in 2013–2023 |

**Related verified source:** Temperature and AMI among diabetes vs non-diabetes patients in Hong Kong (2002–2011), DLNM.  
- https://doi.org/10.1371/journal.pmed.1002612  
- https://pubmed.ncbi.nlm.nih.gov/30016318/

| Element | Detail |
|---|---|
| Outcome / exposure | Daily AMI admissions vs mean temperature |
| Main result | Stronger cold-season associations among patients with diabetes; some hot-season sensitivity in that subgroup |
| Relevance | Suggests effect modification by comorbidity; supports stratified thinking |
| Limitation | Individual comorbidity may not be available in aggregate HA extracts for the first paper |

**Implication for this project:** AMI models should treat cold days as co-primary and interpret null heat findings cautiously under monthly aggregation.

---

## 2. Temperature and ischemic stroke

**Provisional historical source:** Earlier Goggins Hong Kong stroke admissions work (user-provided summary: strong inverse temperature association for ischemic stroke, stronger in older adults/females).  
**Status:** Exact citation and numerical estimates **remain to be confirmed** in PubMed / investigator publication list before manuscript use.

**Related verified source:** Cold weather and influenza with stroke admissions in Hong Kong, 1998–2019.  
- https://link.springer.com/article/10.1007/s00484-025-02870-2

| Element | Detail |
|---|---|
| Temporal resolution | Weekly (reported) |
| Outcome | Stroke admissions |
| Main result | Elevated stroke admission risk at colder temperatures; influenza activity also associated |
| Relevance | Supports continued cold sensitivity and possible infection pathway in a long contemporary window |
| Limitation | Weekly resolution and influenza mediation/confounding issues differ from monthly extreme-day models |

**Implication:** Ischemic stroke is a priority diagnosis stratum; influenza should be handled carefully (likely sensitivity first).

---

## 3. Temperature and hemorrhagic stroke

Historical Hong Kong summaries (including provisional Goggins stroke work) suggest hemorrhagic stroke may show stronger seasonality and weaker continuous temperature associations than ischemic stroke. **This remains to be confirmed** against the primary paper before firm statements.

**Implication:** Hemorrhagic stroke should be modeled separately rather than pooled with ischemic stroke. Sensitivity around traumatic/unspecified hemorrhage codes is needed once coding is confirmed.

---

## 4. Hot nights and humid heat

Official HKO definitions and climate-change communications emphasize hot nights, very hot days, extremely hot days, and cold days as operational extremes.  
- https://www.hko.gov.hk/en/climate_change/proj_hk_annual_vhot_days.htm

**Verified mortality source:** Hong Kong study of consecutive very hot days and hot nights (2006–2015).  
- https://pubmed.ncbi.nlm.nih.gov/31302556/

| Element | Detail |
|---|---|
| Outcome | Mortality (not admissions) |
| Exposure | Consecutive extreme hot-weather events |
| Relevance | Supports spell-duration metrics and hot nights as biologically/policy-relevant exposures |
| Limitation | Mortality ≠ hospital admissions; daily event definitions differ from monthly counts |

**Hypothesis (not a finding):** Hot nights may capture lack of overnight recovery better than monthly mean temperature in dense housing. This is a design rationale, not yet an empirical admissions result.

---

## 5. Older adults and demographic aging

Hong Kong winter-excess and cold-vulnerability studies indicate elevated cold-season burdens among older adults, including ages 85+.

Verified entry points:

- Excess winter IHD hospitalization among older adults: https://pubmed.ncbi.nlm.nih.gov/24714058/
- Excess winter-versus-summer mortality for IHD and cerebrovascular disease (1976–2010): https://pubmed.ncbi.nlm.nih.gov/25993635/
- Extreme-cold vulnerability, especially 85+: https://pubmed.ncbi.nlm.nih.gov/26370114/

| Relevance | Limitation |
|---|---|
| Supports age-stratified models and separation of oldest groups | Mortality/hospitalization endpoints and periods differ; demographic growth must be handled with population offsets, not mistaken for environmental effects |

**Design response:** Prefer five-year age bands and separate 65–69 from 70–74 if HA data allow; always include age-sex population denominators.

---

## 6. Temperature–pollution relationships

In the earlier Goggins AMI analysis, NO₂ was an important short-term predictor. Contemporary Hong Kong air-quality reporting indicates long-term declines in some pollutants alongside ongoing ozone concern (see EPD/AQHI reports; exact year-to-year figures to be taken from real EPD extracts once deposited).

Recent evidence also links short-term ozone to cardiovascular admissions in broader literature, generally with small and heterogeneous effects (example entry point: https://pubmed.ncbi.nlm.nih.gov/40878994/). **Effect sizes and applicability to Hong Kong monthly models remain to be confirmed in the final citation set.**

**Analytical principle:** Stage pollution models. Do not automatically treat ozone as a conventional confounder; it may correlate with, modify, or partly mediate hot sunny conditions. Report total thermal associations separately from pathway-adjusted associations.

---

## 7. Monthly versus daily study designs

Daily DLNMs and GAMs can resolve short lags; monthly models capture broader seasonal and multi-day burden but blunt acute heat spikes.

Local monthly precedent:

- Hong Kong monthly mortality–weather analysis (1980–1994): winter peaks in circulatory/respiratory mortality; inverse association with minimum temperature. https://pubmed.ncbi.nlm.nih.gov/10626765/

| Relevance | Limitation |
|---|---|
| Shows monthly designs can detect broad thermal–circulatory patterns in Hong Kong | Mortality endpoint; older period; does not justify ignoring attenuation of short-lag heat effects |

**Design response:** Use extreme-day counts and spells; interpret null heat findings cautiously; avoid direct coefficient comparison with daily historical studies unless estimands are harmonized.

---

## 8. Hong Kong evidence and the remaining gap

Taken together, the verified literature supports four statements:

1. Hong Kong has a documented history of cold-related cardiovascular burden despite a subtropical climate.  
2. Heat effects were limited or absent in several earlier AMI analyses, but hot nights and heat spells are increasingly relevant exposures.  
3. Aging and pollution change are plausible modifiers of the contemporary risk profile.  
4. No published analysis identified in this first-stage package yet answers, with 2013–2023 monthly extreme-day metrics and age-sex offsets, whether the hospital-admission pattern has changed.

**Gap addressed by this study:** a transparent reassessment of associations between officially defined monthly thermal extremes and AMI/stroke admissions in an aging Hong Kong, with staged pollution handling and explicit COVID sensitivities—without presuming a regime shift.

---

## Bibliographic tasks still open for Bob

1. Verify the exact earlier Goggins ischemic/hemorrhagic stroke admissions citation and estimates.  
2. Confirm HA coding-era documentation for ICD transitions.  
3. Finalize CHP influenza and Clean Air Plan citations for the pollution-context paragraphs.  
4. Replace any provisional numeric claims with primary-source quotations before journal submission.
