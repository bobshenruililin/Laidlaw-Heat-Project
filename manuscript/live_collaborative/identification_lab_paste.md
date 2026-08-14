# Optional Figure 4 and supplement paragraph — hot-night identification

**Status:** PROPOSED IN `Heat_CVD_Manuscript_live_update.md` (14 August CNS pass). Hogan can still strike Figure 4 or demote it to a supplement. Journal-track file; it does not touch his *Weather and pollutants data* paragraph. Exposure only; no health finding; no coefficient. ggplot PNG/PDF now exist (`figure_D_hot_night_identification.png` / `.pdf`); Python SVG remains the web analogue.

## 1. Figure 4 caption (optional)

**Figure 4. Official hot nights by year and month, Hong Kong Observatory Headquarters, 2013–2023.** Each cell is the monthly count of official hot nights; the layout matches Figure 2. June through September recorded at least one official hot night in every year of 2013–2023. Within those months, the between-year variation that identifies a hot-night coefficient once calendar-month indicators are included is therefore how many nights a month contained rather than whether the month was a hot-night month: July 2013 contained 1 night and July 2022 contained 25, the largest monthly count in the window. Provenance: REAL HKO official flags (Tmin ≥ 28 °C) rolled to calendar months.

**The colour-scale maximum is 25 (July 2022),** from the same `hot_nights` column Figure 2’s panel uses. A Python analogue already exists at `figures/live_identification/figure_D_hot_night_identification.svg` (script 60). A ggplot rebuild inside `scripts/47_live_identification_figures.R` remains polish so the two heatmaps share axes and palette exactly; it is not a new finding. Do not substitute `figures/identifying_months/intensive_extensive.svg`; that panel reports sums of squares and is method-speak for this document.

## 2. Optional supplement paragraph — design, not only multiplicity

Every core model contains calendar-month indicators and a smooth function of time, so the contrast between summer and winter is absorbed before any exposure enters and each of the twelve contrasts is identified on differences between years within the same calendar month. What survives that residualisation differs by encoding. For mean temperature and its daily maximum and minimum counterparts, every month contributes, but only a narrow year-to-year deviation about its own monthly mean. For the official extreme-day counts the exposure is seasonally confined, and inside the months that carry it the surviving contrast is intensive rather than extensive: June through September recorded at least one official hot night in every year of 2013–2023, so the identifying variation is how many nights those months contained (July 2013, one night; July 2022, twenty-five). For cold days the concentration is sharper, with 141 of 145 days falling in December through February. A model set can therefore be correctly specified — the month indicators are required to keep seasonal differences in admissions out of the exposure coefficient — while its extreme-day contrasts rest on identifying variation carried by a minority of the 132 months. Reporting Benjamini–Hochberg *q* above 0.19 for all twelve core contrasts is consistent with that design. It describes how much independent variation the design leaves, and how many contrasts were examined; it is not evidence about the magnitude or existence of any thermal association.

## 3. What must not be pasted into the live file

- Daily Jaccard 0.031, the 14 overlapping nights, and the other daily station-versus-grid diagnostics. This paper’s exposure is a monthly count.
- The monthly hot-night slope 0.045 read as an attenuation factor. It bounds a hypothetical reanalysis-based analysis; it does not rescale a Headquarters estimate.
- ERA5-Land night counts anywhere they could be read as the official flag. Nothing here argues for moving the paper off Headquarters.
- HM/CM effective rank, or any HM/CM definition or coefficient, in Results. That family is unlocked and belongs to the weather lock.
- Sum-of-squares shares, identifying-share percentages, or any reading in which thin identification decides what the association is.

## 4. For Hogan

Figure 4 duplicates Figure 2’s construction on the other tail, and the pair makes one point: after month indicators, cold days are identified on a handful of winter months and hot nights on summer intensity. Does the pair belong in the main text, so the reader meets the identification argument before Tables 2 and 3, or is one heatmap enough there, with the hot-night panel in the supplement and referenced from Limitations? Either placement is defensible, and the choice is yours.
