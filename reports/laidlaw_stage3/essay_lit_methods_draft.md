# Thermal Extremes and Stroke in Hong Kong, 2013–2023

**A Laidlaw research essay draft (literature and methods)**  
Bob Shen · Laidlaw Scholars Programme, The University of Hong Kong  
With **Hogan** (weather and heat) and **Roro (Zhenyuan Liu)** (Hospital Authority outcomes)  
Supervisor: **Professor David Bishai**  
Version: July 2026 · *No stroke association estimates yet*

---

## 1. Introduction

Stroke remains a leading cause of death, disability, and long-term care demand. Its proximal causes are clinical, but the timing of events can also respond to environmental stress. Temperature influences blood pressure, vasoconstriction, viscosity, dehydration, and cardiovascular strain; air pollution adds inflammatory and oxidative pathways. Together, heat, cold, and pollution are plausible short-term contributors to cerebrovascular risk—especially among older adults.

Hong Kong is a consequential setting for this question. It combines a humid subtropical climate, dense urban form, and rapid population ageing. Official Hong Kong Observatory (HKO) metrics show that hot nights and very hot days have become more common, while cold days have not vanished. A warmer average climate therefore does not imply that cold-related risk is obsolete; it may instead reweight a mixture of hazards: more frequent upper-tail heat, lingering winter cold, temperature variability, and compound heat–pollution days.

The project also takes a modest cue from Michael Marmot’s work on health inequalities. Environmental hazards are unevenly borne. Older adults often face poorer thermoregulation, more comorbidity, and more constrained housing and mobility. Citywide averages can hide who is most exposed and least able to adapt. Our ecological monthly design cannot identify individual socioeconomic effects, but it does justify careful attention to older age bands—an emphasis Hogan strengthened early by pointing to the actionable 65–69 and 70–74 cohorts.

Professor Bishai framed the collaboration in December 2025 as a team plan: Roro would prepare monthly hospital outcomes; Hogan would prepare monthly climate exposures and advise on interpretation; analysis would follow. After the 17 July 2026 lab meeting, the near-term estimand was narrowed to what the available Hospital Authority (HA) path can honestly support: **monthly stroke event aggregates**, not acute myocardial infarction (AMI) from a general extract that does not specify reasons for admission.

---

## 2. Literature review

### 2.1 Hong Kong baselines: Goggins and the evolutionary question

Goggins et al. (2012) analysed daily public-hospital stroke admissions in Hong Kong (1999–2006), separating haemorrhagic and ischaemic stroke. Lower temperature was associated with higher haemorrhagic stroke across the observed range; ischaemic stroke showed a weaker association below about 22°C. Effects differed by age and sex. Goggins et al. (2013) reported cold-dominant AMI associations and highlighted nitrogen dioxide among pollutants.

Hogan brought these papers into the January 2026 exchange as both foundation and challenge: cold–CVD associations in Hong Kong are already well documented, so novelty must be carefully framed. The discussion that followed treated 2013–2023 less as a “discovery” study and more as an **evolutionary** comparison against the Goggins-era baseline—later heat extremes, an older population, and a changed pollutant mix (declining primary pollutants such as NO₂ alongside a different ozone trajectory). That framing remains the project’s intellectual spine on the weather–disease side. It does **not** license claims of a proven “regime shift” before real stroke aggregates are analysed.

### 2.2 Hot nights, spells, and contested heatwave definitions

Guo et al. (2024) showed that official binary hot-night flags can be weak for hospitalisation risk relative to measures of nighttime heat *intensity*, with circulatory admissions among sensitive outcomes. Wang, Ren and colleagues (2019) defined extremely hot weather events using very hot days (Tmax ≥ 33°C), hot nights (Tmin ≥ 28°C), spell structure, and combined day–night windows such as 2D3N. Guo, Gasparrini et al. (2017) demonstrated across many communities that heatwave–mortality estimates depend on percentile × duration definitions—there is no single natural heatwave rule.

Hogan’s later guidance on “hot months” fits this tradition: define heatwaves, count them within each month, then flag months in the upper tail of that count distribution (or use a simple count threshold). He pointed to atmospheric heatwave work on Hong Kong (Li et al., *Atmospheric Research*, DOI 10.1016/j.atmosres.2024.107845) as a reference for how heatwaves are operationalised as evolving events. In a monthly stroke study, that becomes a named exposure pathway alongside official HKO day counts and Ren/Wang spell metrics—not a silent replacement for them.

### 2.3 Cold, influenza, variability, and pollution

Yang, Chong and colleagues (2025) linked weekly cold and influenza activity to stroke admissions over two decades in Hong Kong. Tian/Qiu et al. (2023) associated short-term temperature variability with circulatory hospitalisations. Guo et al. (2025) found that pollution can amplify temperature–hospitalisation associations. Sipilä (2017) and Lorking (2020) remind us that seasonality is not temperature alone. Collectively these papers motivate cold co-primary pathways, influenza sensitivity, variability metrics, and staged pollution adjustment—especially entering ozone last given its correlation with hot sunny weather.

---

## 3. Objectives (post–17 July)

1. Construct monthly stroke-event aggregates for 2013–2023 with Roro, using a timing rule that recovers the true event month from clinical chronology.  
2. Quantify monthly thermal exposures with Hogan: continuous temperature, official extremes, spells/2D3N, and hot-month definitions.  
3. Assemble concurrent EPD pollution and C&SD population denominators.  
4. Estimate associations using a pre-labelled multi-specification panel, with a headline pair frozen only after team review (Gate 3).  
5. Report honestly what monthly ecological models can and cannot claim.

---

## 4. Methods

### 4.1 Design

Ecological monthly time series, January 2013–December 2023 (`N = 132` months). Unit of analysis: territory-month or month × age × sex, depending on the aggregate grain Roro can release.

### 4.2 Temperature and heat metrics (Hogan’s domain)

Daily HKO Headquarters observations are aggregated to months. Core constructs include monthly mean / Tmax / Tmin; lag-1 month temperature (requiring December 2012 for January 2013); official extreme-day counts (hot nights Tmin ≥ 28°C; very hot days Tmax ≥ 33°C; cold days Tmin ≤ 12°C); spell-length and days-in-spell metrics; Ren/Wang-style 2D3N burden; and heatwave-month indicators (study-period percentiles and Hogan’s count→upper-tail proposal).

Hogan offered in January to prepare the monthly climate **X** file under the original plan. Weather definitions should be finalised with him—not unilaterally.

### 4.3 Pollution (EPD EPIC)

Official monthly averages are obtained from the Environmental Protection Department EPIC portal (`cd.epic.epd.gov.hk/EPICDI/air/yearly/`), for NO₂, O₃, PM₂.₅ (fine suspended particulates), and PM₁₀ (respirable suspended particulates). The primary series uses **general** monitoring stations; roadside extracts are archived only for sensitivity, because near-road microenvironments are not interchangeable with citywide background.

EPIC limits the length of a single monthly request, so downloads are chunked across the 2013–2023 window and then concatenated. For each pollutant–station–month, completeness is assessed against expected observations; months below the project threshold (default ≥75%) are set to missing before any average is taken. Citywide monthly means are unweighted across contributing general stations. Missingness is never coerced to zero. These choices matter for trend description: the assembled series show declining NO₂ and particulate matter alongside a different, generally rising ozone pattern—precisely the pollutant-mix shift discussed in the January exchange when comparing a later period to the Goggins-era NO₂-dominant results.

In regression, pollutants enter in stages (none → NO₂ → PM₂.₅ → O₃ → multi-pollutant). Ozone is last because it co-varies with hot, sunny weather; naive joint adjustment can attenuate heat associations for the wrong reason.

### 4.4 Population denominators

C&SD mid-year age–sex population (Table 110-01001) is interpolated to months. Models use `log(population × days_in_month)` as an offset where counts are analysed. Hogan’s January note on the changing age distribution—especially growth in reachable older bands—motivates keeping 65–69 and 70–74 visible whenever Roro’s aggregates allow.

### 4.5 Stroke outcomes (Roro’s domain)

**Working understanding (to confirm with Roro):** the general HA path available here does not provide reasons for admission, so AMI/principal-dx CVD from that file is out of scope. Stroke work uses aggregates. A first General Out-patient Clinic (GOPC) mention of stroke functions as a **marker**: the actual stroke and associated hospitalisation generally occur earlier. Later (second) mentions are ignored for initial event identification. The analytical task is to locate the true stroke-event timing and assign it to the correct month before aggregation. Field names and exact algorithms remain Roro’s to specify; this paragraph records intent, not invented schema. Small-cell suppression and transfer rules also sit with Roro and PI governance.

Without that chronology, monthly “stroke” counts risk mixing incident events with follow-up mentions. Getting the timing right is therefore not a clerical detail—it is the outcome definition.

### 4.6 Statistical approach: a labelled pathway panel

Negative binomial (or quasi-Poisson) count models with calendar-month factors and a smooth time trend; cluster-robust standard errors when stratified. Results are reported as a **panel of labelled pathways**, not as many independent discoveries. Proposed headline pair for Gate 3 (team freeze): **P02** (same-month Tmax and Tmin) and **P04** (official extreme-day counts). Synthetic code dry-runs are plumbing checks only—they are not findings.

| ID | Focus | Literature / design anchor |
|---|---|---|
| P01 | Monthly mean temperature | Classical T–health series; Goggins; Gasparrini 2015 |
| P02 | Tmax and Tmin (headline candidate) | Day/night separation; supervisor monthly merge request |
| P03 | Lag-1 temperature | Prior-month burden; original Bishai lag note |
| P04 | Official extreme-day counts (headline candidate) | HKO metrics; Guo 2024 (binary vs intensity) |
| P05–P06 | Spell and 2D3N burden | Wang/Ren 2019 |
| P07 | Multi-definition heatwave-month | Guo/Gasparrini 2017; Hogan hot-month idea |
| P08, P18 | Cold-primary / cold-month | Goggins 2012; Yang/Chong 2025 |
| P09, P17 | Age / sex structure | Hogan 65–69 & 70–74; Goggins sex/age patterns |
| P11 | Pollution-staged | Goggins 2013; Guo 2025 |
| P14 | Flu co-exposure | Yang/Chong 2025 |
| P15 | Temperature variability | Tian/Qiu 2023 |
| P13 | IS vs HS (if available) | Goggins 2012; disabled until subtype exists |

### 4.7 Hot and cold months: plural definitions and a harmonised extension

Professor Bishai recalled a pattern from “Jasmine's paper”: many non-significant (“null”) p-values on the hotter side, but fewer on the colder side. The source has not yet been identified, so this recollection is a research prompt rather than a citable result. Two leads remain explicitly unconfirmed. Wang, Ren and colleagues (2019) studied Hong Kong all-cause mortality during 2006–2015 and operationalised extremely hot weather through very hot days (daily maximum temperature ≥33°C), hot nights (daily minimum temperature ≥28°C), prolonged 5VHD and 5HN events, and combined 2D3N windows. A second meeting-note lead—“Liu et al. 2020, South China cold/hot attributable fraction, 2006–2016, *Sustainable Cities and Society*”—still requires a full citation and DOI. A nearby verifiable study by Sida Liu et al. (2020) examined high- and low-temperature mortality in Hong Kong during 2007–2015, but it should not be assumed to be Jasmine's paper.

This uncertainty reinforces a broader measurement point: a “hot month” or “cold month” is not a natural binary. Candidate hot-month families include absolute Hong Kong Observatory (HKO) hot-night and very-hot-day counts; upper-tail monthly mean, maximum and minimum temperatures; persistent day/night spells; 2D3N events; heat-degree burden; anomalies; compound heat–ozone months; and HKO Very Hot Weather Warning months. Cold-month families mirror these through HKO days with minimum temperature ≤12°C, a hypothesis-motivated ≤10°C sensitivity, lower-tail monthly temperatures, cold spells, cold degree-days, abrupt cooling, influenza co-exposure and HKO Cold Weather Warnings. The catalogue therefore retains fifty hot and forty-eight cold definitions, organised as pathways H01–H12 and C01–C12, rather than presenting each model as an independent discovery. Full IDs live in `analysis_plan/hot_cold_month_catalogue.md`.

Hogan's proposed hot-month recipe forms one named family. Li et al. (*Atmospheric Research*, 2025; DOI `10.1016/j.atmosres.2024.107845`) identify May–September heatwaves when daily maximum temperature exceeds a calendar-day 90th-percentile threshold for at least three consecutive days. For this monthly project, Hogan's adaptation is to count event starts within each month and flag upper-tail event-count months. This construction will sit beside, not replace, the HKO and Wang/Ren definitions. The starter set is HM23 (Hogan p90 event-count month), HM08 (monthly mean temperature ≥p90), HM15 (5VHD), HM17 (5HN), HM19 (2D3N), CM03 (at least five ≤12°C days), CM08 (monthly mean temperature ≤p05) and CM15 (three-day cold spell).

Once Dr Bishai confirms the source, its exposure definition, reference period, lag, outcome, covariates and complete test universe will be transcribed before stroke associations are inspected. Coding will first be checked in the overlap with the published window, then applied unchanged through December 2023. If the source used daily mortality while this study uses Roro's monthly true stroke-event aggregates, the exercise will be described as a **definition-harmonised extension**, not an exact replication. A pooled interaction model and a pre-specified hot-versus-cold contrast will be primary; counts of p-values above or below 0.05 will be secondary because non-significance is not evidence of no effect.

Finally, the suggestion that South China populations may be relatively heat-adapted yet vulnerable around 10°C is a discussion hypothesis only. Monthly ecological data cannot identify genetic effects or causal adaptation. Acclimatisation, housing, air conditioning, behaviour, occupation, health care and population age are competing explanations. The 10°C value is therefore an exposure sensitivity, not a biological threshold. No stroke coefficients are yet available, and synthetic outputs are not findings.

---

## 5. Current status (environmental only)

Descriptive HKO series: hot nights and very hot days rose in the later years of 2013–2023; cold days persist. EPD general-station means show declining NO₂/PM and rising O₃—consistent with the January discussion of a shifting pollutant mix. **No validated stroke coefficients are available.** The next evidence step is Roro’s aggregates aligned to Hogan’s climate definitions.

---

## 6. Closing and Stage 3 trajectory

Laidlaw Stage 3 asks for a 2000–3000 word research essay, an A0 **portrait** poster (841 × 1189 mm), and the HKU report form with supervisor endorsement, ahead of the HKU Laidlaw Society showcase in early November 2026 and the Annual Laidlaw Student Conference. This draft supplies literature and methods. Results panels on the poster should remain environmental and process-honest until stroke aggregates arrive.

Lab peers are already modelling the value of writing early. Parallel Hong Kong heat initiatives—community representatives, heat summits, and possible LegCo hearings—also underline why clear, public-facing thermal–health evidence matters. Those efforts are not this study’s results; they are the civic context in which careful measurement earns its keep.

The near-term team asks are small and concrete: Dr Bishai—confirm which paper is “Jasmine's” and which table carries the hotter-null / colder-signal pattern; Hogan—lock heatwave / hot-month / cold-month starters together; Roro—confirm first-GOPC→true-stroke timing and the aggregate transfer path. Going far requires going together.

---

## References (selected)

Goggins WB et al. (2012). Weather, season, and daily stroke admissions in Hong Kong. *Int J Biometeorol*.  
Goggins WB et al. (2013). Weather, pollution and AMI in Hong Kong and Taiwan. *Int J Cardiol*.  
Guo Y et al. (2017). Heat wave and mortality: multicountry study. *Environ Health Perspect*.  
Guo YT et al. (2024). Hot nights and hospitalisation in Hong Kong. *Lancet Reg Health West Pac*.  
Guo YT et al. (2025). Temperature amid elevated air pollution and emergency hospitalisations. *Environ Sci Technol*.  
Li C et al. (2025). Heatwaves in Hong Kong… *Atmos Res* 315:107845. DOI 10.1016/j.atmosres.2024.107845.  
Tian/Qiu et al. (2023). Temperature variability and hospitalisations in Hong Kong. *J Glob Health*.  
Wang D, Ren C et al. (2019). Extremely hot weather events and mortality in Hong Kong. *Sci Total Environ*.  
Liu S, Chan EYY, Goggins WB, Huang Z. (2020). High and low temperature mortality in Hong Kong. *Int J Environ Res Public Health* (adjacent Jasmine lead only).  
Yang Z, Chong et al. (2025). Cold weather, influenza, and stroke. *Int J Biometeorol*.  
Marmot M et al. (2010). *Fair Society, Healthy Lives*.
