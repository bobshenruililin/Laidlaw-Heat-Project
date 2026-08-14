# Identification laboratory outputs

**Provenance:** `REAL_PUBLIC`. HKO Headquarters daily and monthly Tmin; Open-Meteo ERA5-Land at the Hong Kong coordinate. Exposure descriptives only.

| File | What |
|---|---|
| `identification_lab.json` | Anchors, reliability bins, fourteen-night spells, identification profile |
| `identification_profile.csv` | Six-row supplement table |
| `luna_calibration.json` | Independent Luna cut; same 449/17/14 anchors |

Rebuild: `python3 scripts/60_identification_laboratory.py`.  
Luna cut: `python3 scripts/60_luna_calibration.py`.

Do not treat these files as health findings.
