# Peer-city thermal atlas — 13–14 August 2026

**Mode:** Explore + Ship.  
**Provenance:** `REAL_PUBLIC` (Open-Meteo ERA5-Land daily 2 m and apparent temperatures plus precipitation, 2013-01-01 to 2023-12-31; HKO Headquarters open data already in this repo).  
**Not:** health findings, CHD/HF coefficients, stroke, Gate 3, or a live-manuscript paste.

Interactive page: [`docs/peers/index.html`](../docs/peers/index.html).  
Static figures: [`figures/peer_cities/climate_space_2013_2023.svg`](../figures/peer_cities/climate_space_2013_2023.svg), [`figures/peer_cities/hk_station_vs_era5.svg`](../figures/peer_cities/hk_station_vs_era5.svg).  
Rebuild: `python3 scripts/48_peer_cities_thermal_atlas.py` (or `--skip-fetch` from cache).  
Tests: `python3 scripts/test_48_peer_cities_thermal_atlas.py`.

---

## What this is

Hong Kong is often discussed as a “hot Asian city.” That sentence hides a climate, a station, and a threshold. This atlas does four engineering jobs the live paper cannot do while Gate 3 is open:

1. Place Hong Kong next to fifteen cities on **one** public daily temperature source.
2. Transport HKO’s official flags (`Tmin ≥ 28`, `Tmax ≥ 33`, `Tmin ≤ 12`) onto that source and watch them break.
3. Show that **apparent temperature** on the same grid is a third object, not a reconstruction of the station.
4. Point at published heat–CVD work in those cities **without borrowing their coefficients**.

## Cities

| Role | Cities |
|---|---|
| Reference | Hong Kong |
| Pearl River Delta peers | Shenzhen, Guangzhou |
| Humid-subtropical peers | Taipei, Naha, Hanoi, Miami, Houston, Brisbane (JJA winter) |
| Tropical contrasts | Singapore, Manila, Haikou |
| Temperate East-Asian contrasts | Shanghai, Fukuoka, Seoul |
| Dry-heat contrast | Phoenix |

Nearest neighbours in standardised thermal space (mean T, seasonal amplitude, ERA5 counts of 28°C nights and 12°C days): **Taipei (0.18), Shenzhen (0.20), Guangzhou (0.47)**. Singapore is not a cousin. Neither is Phoenix or Seoul.

## The calibration that matters

On 4,017 matched days at the Hong Kong coordinate:

| Encoding | Hot nights (`≥ 28°C`) | Very hot days (`≥ 33°C`) | Cold days (`≤ 12°C`) |
|---|---:|---:|---:|
| HKO Headquarters (live paper) | **449** | 421 | 145 |
| ERA5-Land dry-bulb | **17** | 19 | 296 |
| ERA5-Land + 1.47°C night offset | 378 | 106 | 186 |
| ERA5-Land apparent temperature | **1,453** | 1,368 | 589 |

| | |
|---|---|
| Tmin RMSE | 1.97 °C |
| Tmin bias (grid − station) | **−1.47 °C** |
| Hot-night Jaccard (dry-bulb vs HKO) | 0.031 |

A 1.5 °C cold bias in night minima, sitting next to a 28 °C step, collapses the official hot-night flag. Adding the bias back recovers 378 hot nights, not 449. Apparent temperature does not repair that. In humid Hong Kong it **overshoots** the station: 1,453 nights feel at least 28 °C on the grid. Three objects. None of them are interchangeable.

Percentile encodings on the same grid (~200 days/city by construction) travel; absolute HKO thresholds do not.

This is the operational version of Guo’s point: an official hot-night *flag* is not an hourly measure of how hot the night was, and it is not a reanalysis object.

**Use HKO for the live paper. Use ERA5 only for same-source cross-city ranks.**

## Singapore is the useful contrast

On this grid Singapore records **zero** HKO-cold days and **zero** HKO-hot nights on dry-bulb. Mean temperature 26.7 °C; seasonal amplitude **1.5 °C**. Hong Kong’s amplitude is 12.1 °C. Apparent temperature then records **3,317** nights ≥28 °C. Humidity without winter is not Hong Kong’s climate.

The Singapore NSTEMI paper (Seah et al. 2022) still finds a *relative* cool effect inside a tropical envelope. That is a different estimand and a different climate. It is a warning not to delete winter, not a coefficient to paste.

## Taipei and Shenzhen are the useful cousins

Same humid-subtropical envelope, similar mean and amplitude. Jingesi, Yin, Huang et al. (2024) report a reverse-J for Shenzhen ambulance CVD, with thermal-stress AF 10.81% of which cold 10.42% versus heat 0.39%. Daily UTCI, not our monthly first-event counts. The shape is family-resemblance, not a result.

## Phoenix is the useful foil

ERA5 very-hot days (`Tmax ≥ 33`) : **1,733** in Phoenix versus **19** in Hong Kong. Annual rainfall 286 mm versus 2,097 mm. Distance 4.57. Hong Kong is not a desert heatwave city, and exporting Phoenix heat-health language would be a climate error of the same family as exporting Singapore’s missing winter.

## What this does not license

- Transporting our CHD/HF count ratios to Taipei, Miami, Phoenix, or anywhere else.
- Quoting ERA5 flag totals as HKO yearbook numbers.
- A Guangzhou health claim (no city-specific paper was locked here).
- A stroke analysis.
- Treating apparent-temperature flags as HKO reconstructions.

## Files

- `scripts/48_peer_cities_thermal_atlas.py`
- `scripts/test_48_peer_cities_thermal_atlas.py`
- `data_processed/peer_cities/cache/*_daily.csv`
- `outputs/peer_cities/`
- `docs/peers/`
- `figures/peer_cities/`
- `reports/hogan_peer_cities_one_pager_2026-08-14.md`
