# Two long pitches — Bishai (research) and Altman (passion) — 14 August 2026

**Status:** Not sent. Written because Bob asked to be pitched as if he were Professor Bishai or Sam Altman, at length. First person is Shen Ruililin (Bob). Analysis is the internship’s. Hogan provided weather data and guidance; Zhenyuan Liu (“Roro”) provided governed HA aggregates and regression guidance; Professor Bishai provided the multi-method frame and remains PI. No email. Not form 2a. Gate 3 open.

---

## I. To Professor David Bishai

Professor Bishai —

You asked, last December and again in July, for multi-method work and a Table 1 of temperature. You also said to go far together. This is what the internship actually produced, what it can honestly claim, and what it still needs from you as PI rather than as a reader of maps.

I will not ask you to freeze Gate 3 in this note. I will not ask you to sign form 2a in this note. Those are separate human acts. If you only do one thing for Laidlaw this month, it should be the 2a. This letter is the science.

### The one sentence

We measured our own largest limitation before a reviewer could, and the measurement defends the design.

The limitation is already in the live paper: every thermal exposure comes from one Observatory garden and is applied to the whole territory. The measurement is a calibration, not a slogan. On 4,017 matched nights at the same coordinate, Headquarters flags 449 nights with Tmin ≥ 28°C; ERA5-Land dry-bulb flags 17; both flag 14; Jaccard is 0.031. Apparent temperature on the same grid flags 1,453 nights and is a third object, not a reconstruction of the station. You can move the grid’s threshold to 26.4°C and recover the *count* of 449. You cannot recover the *nights*: the maximum Jaccard against the fixed Headquarters 28°C set is 0.47, at 26.3°C. Staying on Headquarters is therefore a supported decision, not a habit.

### What the question became

The family you care about is already three layers deep, and they are not the same estimand.

Jingwen Liu (“Jasmine”) and colleagues (2020, *Sustainable Cities and Society*) estimated daily all-cause mortality attributable fractions in Hong Kong, 2006–2016, with a DLNM. They reported cold AF 4.72% versus heat 0.16%, and moderate-temperature AF 4.25% versus extreme 0.63%. That is mortality, daily, with a reversed-J curve.

Roro’s medRxiv paper (2026), on which you are a co-author, takes local relative risks and produces model-based excess deaths under four heatwave definitions for 2014–2023, in the range 1,455–3,238 deaths depending on the operator. That is mortality again, but a scenario count, not a new morbidity coefficient.

This internship was supposed to add a morbidity layer. The original stroke file did not arrive. What Roro did deliver, on 6–7 August, is territory-month counts of first recorded hospitalisation after first CHD diagnosis, and after first HF diagnosis, among people already diagnosed with type 2 diabetes and/or hypertension, January 2013–December 2023: 132 months. Admission cause is absent. The event is not principal-diagnosis CHD or HF, not AMI, not incidence in a still-at-risk cohort, and not a daily trigger. Stroke remains named and unattached. I have not invented a stroke row.

The continuity estimand is therefore an ecological monthly count ratio. Separate negative-binomial models, calendar-month indicators, a natural spline on time with four degrees of freedom, a days-in-month offset, and a four-construction uncertainty ladder: model-based, HC1, Newey–West lag 3, Newey–West lag 6. Twelve core contrasts: CHD and HF × mean temperature, mean Tmax, mean Tmin, official hot nights, official cold days, official very hot days.

That is the paper you can supervise. It is smaller than the December ambition. It is also honest.

### What the health panel actually says

All twelve core Benjamini–Hochberg q-values exceed 0.19. There is no protected confirmatory primary. My lead recommendation remains Gate 3 Option A: an explicit no-confirmatory-primary, methods-focused exploratory paper. That freeze is yours, with Hogan and Roro, not mine.

Two intervals are worth knowing so that nobody later “discovers” them as headlines.

CHD and hot nights, per five nights, Newey–West lag 6: 1.022 (1.002–1.042). The interval is SE-sensitive. Newey–West lag 3 still excludes 1 at the edge; other constructions do not always. It is not a triumph.

HF and cold days, per five days, Newey–West lag 6: 1.073 (1.006–1.144). The interval is SE-concordant across the ladder and still q-unprotected. It is not a biological cold threshold, and it is not the ~10°C discussion prompt converted into a gene.

First-event totals fall across the decade while the broad 35+ population rises. CHD annual first-hospitalisations go from 23,830 in 2013 to 12,323 in 2023. That is the shape of a first-event construction inside a 2013–2023 diagnosis window, plus pandemic care-seeking. Without still-at-risk person-time these are not incidence rates. Roro would have to supply a cohort denominator before anyone should speak of rates.

A clean-room attempt to recover daily exposure information from monthly health sums (Basagaña–Ballester M|D) failed its 500-replicate calibration gates. I did not then admit a real daily coefficient. That refusal is part of the result.

Hogan’s weather morphology, implemented from Wang/Li and Li’s heatwave event, reproduces five source-count anchors. The unlocked hot/cold-month catalogue (HM01–HM50, CM01–CM48) is a structured panel, not ten discoveries. On the first-wave file actually on disk, eleven live binary flags have correlation effective rank 3.92; heat never co-fires with cold; CM05 is a column of zeros. Rank is a reason not to fit the next catalogue ID. It is not a licence to refit outcomes, and it does not lock HM23. Hogan still has to tick reference period, percentile, ties, gaps, missingness, and month assignment. I wrote him a checkbox card. I did not tick it for him.

Flu covers 121 of 132 months and was never zero-filled. Pollution is EPD, not a placeholder. The live manuscript’s weather Methods remain Hogan’s prose. I do not overwrite them.

### Why a quiet health panel is not a failed internship

You asked for multi-method. The mistake would have been to treat twelve contrasts as twelve press releases, or to go hunting in the catalogue until something starred.

The more useful second method is identification of the exposure.

With calendar-month indicators in the health model, a coefficient is identified only on the variation that survives those indicators: between years, within calendar month. I computed that share on the Headquarters monthly file, without touching hospital counts.

Mean temperature: 4.2% of 132-month sum of squares is identifying. Mean Tmax: 5.3%. Mean Tmin: 4.4%. Official hot nights: 28.8%, and only May–October have any residual. Official very hot days: 33.1%. Official cold days: 46.9%, December–March.

That is why a null-ish hot-night interval is not only a multiplicity story. After month indicators, a hot-night coefficient is mostly asking how many nights an already-hot month contained. June–September always had at least one official hot night in all eleven years. 95.4% of the remaining identifying sum of squares is intensity, not on/off. July 2013 had 1 night. July 2022 had 25. That year×month map is now Figure D, built in ggplot from the same monthly file as the live paper’s cold-day Figure 2.

Guo et al. 2024 already told the live draft that the official 28°C *flag* is a coarse metric next to hourly night-heat excess (their HNday28 association with emergency hospitalisation was null after mean-temperature adjustment; intensity was not). Mistry et al. 2022 told the field that ERA5-Land *means* are often good enough for temperature–mortality curves, with weaker performance in tropical heat tails. This internship added the missing piece: the official flag is also the wrong *instrument and place* if you try to replace Headquarters with a grid.

At the paper’s own 132-month grain, ERA5 monthly mean Tmin tracks Headquarters (r = 0.986, slope 1.032). Monthly 28°C-night *counts* do not (slope 0.045). Headquarters has a positive hot-night count in 57 months; ERA5 in 9. Forty-eight of those fifty-seven official months contain no ERA5 28°C night at all. Daily Jaccard 0.031 is therefore not an aggregation artefact. Means travel. The flag does not.

The reliability curve makes the same fact an integrand. Among 365 Headquarters nights in [28, 29)°C, ERA5 calls 28°C once (rate 0.003). Among 16 nights ≥29.5°C the rate is 0.44 (7/16). The curve is companion-only. I will not paste it into your health table. I will not invert P(Headquarters | ERA5) to impute flags onto Pearl River Delta cells. I will not treat 0.045 as a measurement-error correction of 1.022. Those would be misconduct.

The cold side has the opposite bias, which is why I do not sell a general “ERA5 is too cold” slogan. When Headquarters is already 8–12°C, ERA5 is ≤12°C on 127 of 128 nights. The grid over-fires cold months (36 versus 29). Heat and cold are not symmetric measurement errors.

### Place, not only instrument

A 28°C night is a location even inside Hong Kong.

On the 0.1° ERA5 lattice, the Waglan cell records 252 nights ≥28°C; the Headquarters cell records 17. That is the same grid, not a station comparison. OLS of mean Tmin on elevation and coast has R² 0.55; adding lat and lon raises R² to 0.88; residual Moran’s I stays positive. I did not overlay CHD or HF on districts.

On the 0.2° Pearl River Delta mosaic, marine-south cells average 353 such nights; Guangzhou’s box 12; Huizhou 0.2. A spatial lag remains (SAR ρ 0.45). Getis-Ord hotspots sit on the water. Exporting the official 28°C flag up the river is a larger spatial act than exporting it across the harbour. I did not transport Hong Kong hospitalisation ratios to Shenzhen or Guangzhou.

The de-seasoned Tmin field has almost one degree of freedom. EOF1 holds 92% of variance and anti-correlates with hot-night counts (r = −0.93). A basin-wide pulse is not a hot-night map. Theil–Sen on eleven annual means looks like a trend map until you FDR it: 0 of 90 cells survive Benjamini–Hochberg at 10%. I killed that choropleth as a finding.

Peer cities, same ERA5 product: Taipei, Shenzhen, and Guangzhou are thermal cousins of Hong Kong’s grid box. Singapore has no winter. Phoenix is dry heat. None of them is a licence to paste 28/33/12 onto reanalysis and call it HKO.

### The last unfinished objects, now mostly measured

You should know what was parked on purpose, and what I finished without inventing a lock.

Public HKO open data, not ERA5, for King’s Park and Waglan, 2013–2023, completeness C. Headquarters 449 hot nights; King’s Park 160; Waglan 107. On days both complete, every King’s Park hot night is also a Headquarters hot night, but Headquarters has 177 more; Jaccard 0.47. Waglan Jaccard 0.21. Nearby siting is not the same instrument. The ERA5 Waglan cell (252 nights) is a different object again. The live paper stays on Headquarters.

WorldPop 2020 1 km unconstrained ASCII, summed onto the thirty ERA5 0.1° cells. Southern cells at or below 22.25°N hold 1,937 of 2,935 unweighted 28°C cell-nights (66%) and 19% of the WorldPop mass in the lattice. Population-weighted night share: 22%. People are not where the marine flag is. That is not a Marmot hospitalisation result. C&SD in this repo is not spatial. I did not put counts on cells.

A twelve-month shift of a seasonal count flag does not collapse identifying share. Hot nights go from 0.288 to 0.318. That share is a calendar-month property. The useful negative control is health in year *t* against exposure in year *t−1*. I wrote the re-fit. I did not run it, because the monthly HA analysis panels are gitignored and not on disk in this workspace. I will not reconstruct 132 months of counts from annual totals. If the panels return, the diagnostic is labelled Gate-3-open and cannot upgrade any q.

Hogan’s HM23 lock is still his. Rank 3.92 does not replace it.

### What this is, in your language

One health panel. One identification panel. One refusal to mix them.

The health panel is exploratory. The identification panel explains why Headquarters was the right encoding *and* why a quiet hot-night interval is not a surprise. That is multi-method as you meant it in July: not a pile of models, but more than one way of seeing the same design.

Jasmine remains the mortality AF layer. Roro remains the excess-death scenario layer. This internship is the monthly CHD/HF first-hospitalisation layer, with the exposure instrument priced. Stroke is still the missing morbidity sequel. I would rather leave that hole visible than fill it with a coefficient.

### What I am not asking you for in this letter

Not a Gate 3 freeze. Not a signature on 2a. Not permission to put hospitals on a map. Not a claim that 1.022 is the finding. Not a rewrite of Hogan’s weather paragraph. Not a rebuild of the frozen Stage 3 PDF.

When you want the programme object: the unchanged essay whose SHA prefix is `6136e85a654502a0`, and your own block on form 2a, blank until you fill it. When you want the science object later: one figure, one URL, the sentence that we measured the single-station limitation. If you answer only one email this month, it must be the 2a.

I am glad I got to do this under your supervision. The work is the internship’s. The weather is Hogan’s. The outcomes are Roro’s. The decision to keep the methods honest when the file that arrived was not the file we named in December is the part I can own.

Shen Ruililin

---

## II. To Sam Altman

Sam —

I became obsessed with a fact that sounds small until you sit with it.

Hong Kong publishes an official “hot night”: Tmin at the Observatory ≥ 28°C. The live epidemiology paper I am on uses the monthly count of those nights as if it were the city’s night. I wanted to know whether that was a thermometer, a garden, or a slogan.

It is a garden.

### The obsession

I am a Laidlaw Scholar at HKU. The project is thermal extremes and cardiovascular hospitalisation. My supervisor is David Bishai. The weather co-investigator is Hogan. The Hospital Authority outcomes came from Zhenyuan Liu. I do the analysis plumbing, the identification, the writing that has to survive a methods editor.

The passion is not “climate and health,” which is a conference track. The passion is: **before you trust a coefficient, price the instrument.**

Most people in this field download a reanalysis, pick a threshold that has a government logo on it, and run a model. Some of them are careful. Almost none of them will tell you, on the same 4,017 nights, what three thermometers at one coordinate actually disagreed about.

I did.

Headquarters: 449 hot nights. ERA5-Land dry-bulb at the same point: 17. Apparent temperature on that grid: 1,453. Intersection of the first two: 14. Jaccard: 0.031.

You can slide the grid’s threshold until the *count* matches 449. That happens at 26.4°C, and you get 448 nights that are not the same 449 days. The best overlap you can buy against the official set, at any threshold, is Jaccard 0.47. Half the nights are still the wrong nights.

That is the demo. Not a dashboard. One slider, one field, one sentence: the same nights are 449, 17, or 1,453 hot depending on the thermometer, and you cannot recode your way back.

### What I did with it

I refused the product that would have been easy.

Easy would have been a choropleth of hospitalisations on districts. Easy would have been “ERA5 is biased, here is the correction factor 0.045, apply it to the relative risk.” Easy would have been fourteen Leaflet maps and a request that my supervisor freeze the headline because the maps looked expensive. Easy would have been fitting the next fifty heatwave definitions until one starred.

I did not do those. They would have ended the project’s credibility with the three people whose names are on the work.

What I built instead is an identification laboratory.

At the paper’s grain — 132 months, not 4,017 days — monthly mean temperature travels from station to grid (r = 0.986). The official 28°C *count* does not (slope 0.045; 57 months versus 9). So the daily embarrassment is not an averaging artefact. Means are one family. Flags are another.

After you put calendar-month indicators in the health model, which we did because this is a monthly paper, almost all of mean temperature is already explained by season. Four percent remains. Hot nights keep 29%, and it is not “summer versus winter”: June–September always had at least one such night, every year. The remaining variation is how *many* — 1 versus 25 in July. That is the paper object. I drew it as a year×month heatmap that shares construction with the cold-day figure already in the manuscript.

Then I asked where the 28°C night lives when you stop pretending the city is a point.

On a 0.1° grid, Waglan Island’s cell lights 252 times; Headquarters’ cell lights 17. On a 0.2° mosaic of the Pearl River Delta, the water holds the flag and Guangzhou almost does not. Unweighted, 66% of those cell-nights sit in the southern two rows. Weight them by WorldPop 2020 and the share falls to 22%. The marine mass is not where the people are. I still did not put a hospital on a cell. Marmot is a reason to care who is exposed. It is not a finding I have earned from a 1 km population grid and a health file that has no coordinates.

I fetched the official King’s Park and Waglan *station* series, not the ERA5 cells. King’s Park, a park next door, has 160 complete hot nights against Headquarters’ 449. Jaccard 0.47. Every complete King’s Park hot night is also a Headquarters hot night; Headquarters has many more. Waglan’s official series has 107, Jaccard 0.21. The ERA5 Waglan cell’s 252 is a third number. Siting is not instrument is not reanalysis.

The cold side of the reliability curve is the control on my own rhetoric. ERA5 is not “always too cold.” When Headquarters is 8–12°C, ERA5 is already ≤12°C on 127 of 128 nights. Opposite bias. If I had only shipped the heat curve, I would have been selling a vibe.

I also learned a negative result about my own cleverness. Someone suggested a year-shifted flag would collapse identifying share. It does not. A twelve-month permutation of a seasonal count is still a seasonal count. Identifying share of hot nights moves from 0.288 to 0.318. The test that would matter is whether last year’s heat predicts this year’s hospitalisations. I wrote that model. I did not fake the monthly counts to run it. The health file is governed and gitignored. Passion that invents rows is not passion.

### Why this is the kind of work I want to be known for

I like finishing. I like finishing *honestly*.

The Laidlaw programme has a 31 August essay, a 15 September poster, a form my supervisor has to sign. Those are real. They are also the wrong god. The frozen essay is a programme object. The live paper is Hogan’s file. The maps are a companion. If you mix them, you get a student who asked for a signature inside a demo, and a reviewer who thinks the coefficient came from the map.

I want to be the person who, given a government threshold and a reanalysis, measures the Jaccard, finds 0.03, and does not then “fix” the epidemiology with a fudge factor. I want to be the person who ships the ggplot twin so the figure in the paper and the figure on the wall are the same construction. I want to be the person who writes the lock card for the weather co-investigator and leaves the boxes empty.

The health results are quiet. All q > 0.19. I am not embarrassed. A quiet coefficient after you have priced the instrument is more adult than a loud coefficient on an unexamined flag.

The family of papers I am in is cumulative: Jasmine’s daily mortality curve, Roro’s multi-definition excess deaths, this monthly first-hospitalisation panel. Stroke never arrived. I left the hole. That is also finishing.

### If you ask what I would build next

Not a fifth map.

If the governed monthly panels are restored, the year-shifted health diagnostic, labelled exploratory, not a headline. If Hogan ticks the lock, a rebuild of HM23 from a named climatology, not from a default I pretended was his. If Roro sends stroke, the morbidity sequel we named in December — with the same identification discipline, not a reset to Week-1 AMI theatre.

If someone offers me a satellite night-heat product and a city-wide health file with coordinates, I would want the same laboratory: three thermometers, a Jaccard as a function of threshold, a monthly bridge, an intensive/extensive split, a population weight that is not allowed to become a disparity claim until the outcome grain matches. The product is the discipline, not the tiles.

### The sentence I would put on a slide if I had one slide

The same 4,017 Hong Kong nights are 449, 17, or 1,453 hot depending on the thermometer. You can match the count. You cannot match the nights. So the paper stays on the garden, and the garden has been priced.

That is what I did with the passion. The work is mine and the internship’s. The data and the guidance are Hogan’s, Roro’s, and Bishai’s. I am not going to sell you a hospital map.

Shen Ruililin
