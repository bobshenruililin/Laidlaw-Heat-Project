# Same-night three thermometers — 14 August 2026

**Mode:** Ship. Public companion, not form 2a.  
**Provenance:** `REAL_PUBLIC`. HKO Headquarters daily Tmin; Open-Meteo ERA5-Land dry-bulb and apparent Tmin at the Hong Kong coordinate. 4,017 matched days.  
**Not:** a reconstructed HKO series, a harm ranking, or a fifth Leaflet.

Rebuild: `python3 scripts/59_same_night_three_thermometers.py`.  
Tests: `python3 scripts/test_59_same_night.py`.  
Page: `docs/demo/index.html` (scrubber; hash `#t=28&d=2015-08-08`). Slim JSON of **452** union nights, not another 4,017-day blob.

## Punchline

| Set at 28°C | Nights |
|---|---:|
| HKO-only | 435 |
| Both | **14** |
| ERA5-only | 3 |
| Station nights ≥29°C that ERA5 still calls <28°C | **71** |

Hottest overlap: **8 August 2015**, HKO 30.0°C / ERA5 28.7°C / apparent 34.1°C.  
Hottest miss: **14 September 2022**, HKO 29.6°C / ERA5 25.6°C.  
Widest gap: **22 September 2023**, HKO 28.4°C / ERA5 23.1°C (5.3°C).  
ERA5-only: 24 July 2014 (HKO 27.9), 9 August 2015 (26.9), 9 July 2016 (26.4).

They agree only when Headquarters is already well past the line. Apparent temperature is a third encoding, not a correction. Keyboard `[` `]` steps nights; arrows still move the threshold.

Static figure: `figures/threshold_demo/same_night_three_thermometers.svg`.
