# Fable — one limitation sentence for the live manuscript — 14 August 2026

**Mode:** Decide.
**Provenance:** `REAL_PUBLIC` (HKO Headquarters daily Tmin; ERA5-Land at the Hong Kong coordinate; monthly bridge from `scripts/54_monthly_station_grid_bridge.py`, 132 months; daily anchors from `scripts/53_threshold_does_not_travel.py`).
**Not:** a health finding, an attenuation factor, a change to Hogan's weather paragraph, or a new citation. Paste is a human step; Hogan sees it first.

Target location: the live manuscript Limitations, immediately after
"All exposures were measured at a single Observatory station and applied territory-wide; within-territory exposure variation was not modelled."

---

## 1. The one sentence (paste-ready)

> Over the same 132 months, ERA5-Land reanalysis at the Observatory coordinate closely tracked monthly mean minimum temperature (correlation 0.986, slope 1.032) but not the monthly count of official hot nights (slope 0.045, standard error 0.007; 57 hot-night months at the station against 9 in the reanalysis), so the mean-temperature exposures are corroborated by an independent gridded source while the hot-night exposure rests on the Headquarters record alone.

Every number is monthly, at the paper's grain, from script 54. No citation is needed: the check is our own calibration, and the fragility of the official flag as a health metric is already carried by the preceding Guo sentence [17].

## 2. Optional second sentence

None. The sentence is complete as one contrast. The two candidate riders both fail the test of necessity: the Guo point [17] is already the sentence before the target, and the identification share (0.29 of hot-night sum of squares between-year within calendar month; six calendar months with any variation) is a separate limitation about thin identification, not about measurement source, and would need its own decision.

## 3. Hogan-facing note (two sentences)

> This sentence reports a post-hoc check of the exposure source at the paper's own monthly grain — it changes no exposure definition, no model, and none of your weather Methods — which is why it belongs in Limitations rather than Methods. It is also the first mention of ERA5-Land anywhere in the paper, so please read it before it is pasted and strike it if you would rather keep the single-station limitation qualitative.

## 4. What NOT to paste

- The daily diagnostics: 449 vs 17 nights, Jaccard 0.031, max Jaccard 0.471 at 26.3°C, the 26.4°C count-match (448 nights, not the same days), and the −1.47°C mean Tmin bias. They are day-grain objects; pasting them invites a daily-exposure discussion the paper has already refused.
- The apparent-temperature count (1,453 nights). It is a third encoding and would blur dry-bulb with apparent temperature in a paragraph that uses only dry-bulb.
- Any reading of 0.045 as the factor by which a CHD or HF coefficient would shrink. No outcome entered the calibration.
- The Mistry et al. 2022 citation. The sentence stands on our own numbers, and no new citation is locked.
- The identification share (0.29; six calendar months with any SD). Real, but a different limitation; do not let it ride along.
- ERA5 monthly hot-night counts as substitutes for HKO flags anywhere in the paper. The 9 reanalysis hot-night months all sit inside the station's 57; the reanalysis sees fewer months, not different ones.
- Any suggestion that the calibration rescues or corrects the CHD or HF estimates.

## 5. The one sentence Bishai should remember

Keep as drafted:

> "We measured our own largest limitation before a reviewer could, and the measurement defends the design."

It survives the monthly numbers unchanged. "Measured" is slope 0.045 (SE 0.007) and 57 against 9 at the paper's grain; "defends the design" is correlation 0.986 on means plus the fact that no alternative source reproduces the official flag, so Headquarters was the only record that could carry the official definition.
