# EPD pollution raw data

Official Hong Kong Environmental Protection Department air-quality monitoring data via EPIC.

Portal: https://cd.epic.epd.gov.hk/EPICDI/air/yearly/

## Automated download

From the repository root:

```bash
python3 scripts/18_download_epd_epic_monthly.py              # general stations
python3 scripts/18_download_epd_epic_monthly.py --include-roadside
Rscript scripts/04_build_pollution_monthly.R
```

This pulls **monthly averages** for NO₂, O₃, PM₂.₅ (FSP), and PM₁₀ (RSP) in chunks of ≤60 months (EPIC limit is 120).

## Files

| Pattern | Content |
|---|---|
| `epd_general_monthly_YYYYMM_YYYYMM.csv` | General stations (primary) |
| `epd_roadside_monthly_YYYYMM_YYYYMM.csv` | Roadside stations (sensitivity only) |
| `download_manifest.txt` | Download provenance |
| `import_status.txt` | Last build status |

## Aggregation rule (primary series)

- Unweighted mean across **general** stations.
- Completeness: fraction of that calendar year’s active general stations reporting the month; months below `pollution.completeness_threshold` in `config.yml` (default 0.75) are set to NA.
- Roadside is **not** mixed into the primary panel.
- Units: µg/m³ (per EPIC CSV remarks).

## Literature alignment

Goggins (AMI) emphasized NO₂; Guo et al. (2025) use PM₂.₅, NO₂, O₃ with temperature. Ozone is retained but should enter models in a **staged** way (possible pathway / collinearity with heat).

Do not overwrite raw EPIC downloads; re-run the download script to refresh.
