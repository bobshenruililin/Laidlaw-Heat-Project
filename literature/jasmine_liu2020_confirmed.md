# Jasmine paper — confirmed and locked

## Identity

“Jasmine’s paper” is now identified as:

> Liu, Jingwen; Hansen, Alana; Varghese, Blesson; Liu, Zhidong; Tong, Michael; Qiu, Hong; Tian, Linwei; Lau, Kevin Ka-Lun; Ng, Edward; Ren, Chao; Bi, Peng. “Cause-specific mortality attributable to cold and hot ambient temperatures in Hong Kong: a time-series study, 2006–2016.” *Sustainable Cities and Society* 57 (2020): 102131. DOI [`10.1016/j.scs.2020.102131`](https://doi.org/10.1016/j.scs.2020.102131).

**Locked identification:** Jasmine = **Jingwen Liu**, first author. Do not revert this paper to an “unconfirmed candidate.”

## What is confirmed

| Element | Confirmed information |
|---|---|
| Setting and window | Hong Kong daily mortality, 2006–2016 |
| Outcome framing | Total and cause-specific mortality attributable to non-optimal daily mean temperature |
| Model | Distributed lag non-linear model (DLNM) integrated with quasi-Poisson regression |
| Shape | Reversed J-shaped temperature–total mortality association |
| Overall cold vs heat AF | **4.72% cold** vs **0.16% heat** |
| Moderate vs extreme AF | **4.25% moderate** vs **0.63% extreme** |
| Highest reported extreme-cold RR | Injury mortality: **RR 2.18 (95% CI 1.03–4.62), lag 0–21 days** |
| Qualitative cause pattern | Extreme cold produced the highest risk; respiratory and circulatory mortality followed injury in the reported lag 0–21 comparison |

Two distinctions matter:

1. **Cold ≫ heat AF** means the estimated population burden attributable to cold was much larger than the burden attributable to heat under this paper’s exposure distribution, reference and lag model.
2. **Moderate ≫ extreme AF** means most attributable mortality arose from more common moderate non-optimal temperatures, not only rare extremes.

Neither contrast is a stroke result. Neither establishes a genetic mechanism. The AFs must not be converted into coefficients for the 2013–2023 monthly panel.

## What still requires the full Jasmine PDF and supplement

The bibliographic identity and headline findings are locked, but the full source PDF has not yet been ingested into this workspace. Before source-faithful reproduction or detailed methods writing, extract:

- the exact minimum-mortality/reference temperature and its uncertainty;
- the numerical boundaries for moderate cold, extreme cold, moderate heat and extreme heat;
- temperature and lag spline degrees of freedom, knot locations and lag maximum;
- seasonality, long-term trend, day-of-week, humidity, pollution and other model controls;
- mortality source, ICD cause groupings, exclusions and missing-data handling;
- age groups and every reported subgroup AF/RR;
- the precise attributable-risk calculation and uncertainty procedure;
- all tables/figures behind the recalled hot-side versus cold-side significance pattern;
- the complete universe of tests, rather than a selected count of significant results; and
- the exact derivation of the 30.60°C threshold and lag-phase RRs later used by Roro.

Until those items are transcribed from the paper and supplement, do not invent spline parameters, reference temperatures, cause-specific coefficients or p-values.

## Direct link to the Roro manuscript

Roro’s 2026 medRxiv paper, *Modelling the Excess Mortality Associated with Heat Waves in Hong Kong: 2014–2023*, explicitly imports heat RRs from **Liu et al. (2020)** and Wang, Ren et al. (2019).

For Roro’s `HWD_Tavg` scenario:

- a daily mean-temperature threshold at the 99th percentile (**30.60°C**) starts a long heat/lag window;
- RRs are represented in phases for day 0, days 1–5 and days 6–21; and
- those published RRs are combined with expected age–sex deaths and propagated through Monte Carlo simulation to estimate absolute excess deaths.

That description is confirmed from Roro’s medRxiv v1. The full Jasmine PDF is still needed to independently verify Roro’s transcription against the original methods and tables.

Jingwen Liu is a coauthor of the Roro manuscript and is credited there with data acquisition and critical revision. Chao Ren is also an author of both papers. This is a continuous team evidence chain:

**Jingwen Liu et al. 2020 daily mortality RRs/AFs → Zhenyuan Liu et al. 2026 multi-definition heatwave excess deaths.**

## Rule for the stroke extension

Our 2013–2023 monthly stroke analysis may transport clearly specified temperature definitions, but it is not an exact replication:

- Jasmine: daily mortality, DLNM/quasi-Poisson, distributed-lag RRs and AFs.
- Roro: RR-transported model-based excess heat deaths.
- Our project: monthly stroke-event aggregate associations under paired hot/cold definitions.

Report those estimands separately. The proposed gene/adaptation interpretation and the approximately 10°C idea remain hypotheses only.
