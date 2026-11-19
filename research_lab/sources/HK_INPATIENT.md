# Hong Kong inpatient service activity, 2013–2023

The public source is the Hong Kong Census and Statistics Department's *Hong Kong Annual Digest of Statistics*. Its inpatient tables credit the Department of Health and Hospital Authority. The file `hk_inpatient_digest_cells.csv` transcribes the selected calendar-year cells from four published editions. Each row identifies both the publication year and the year of service. The following page numbers are printed on the pages.

| Digest edition | Study years transcribed | Table 13.9 | Table 13.10, all areas |
|---|---|---:|---:|
| [2019](https://www.statistics.gov.hk/pub/B10100032019AN19B0100.pdf) | 2013–18 | 380 | 382 |
| [2021](https://www.censtatd.gov.hk/en/data/stat_report/product/B1010003/att/B10100032021AN21B0100.pdf#page=416) | 2015–20 | 384 | 386 |
| [2024](https://www.censtatd.gov.hk/en/data/stat_report/product/B1010003/att/B10100032024AN24B0100.pdf) | 2013, 2018–23 | 372 | 374 |
| [2025](https://www.censtatd.gov.hk/en/data/stat_report/product/B1010003/att/B10100032025AN25B0100.pdf) | 2014, 2019–23 | 354 | 356 |

| CSV field | Table and row | Meaning |
|---|---|---|
| `all_hospital_episodes` | 13.9, Total | Inpatient discharges and deaths across HA, private and correctional-institution hospitals |
| `circulatory_episodes` | 13.9, Diseases of the circulatory system | The ICD-10 circulatory chapter within the same hospitals |
| `ha_episodes` | 13.10, All areas, Hospital Authority hospitals | All-cause throughput restricted to HA hospitals |
| `private_episodes` | 13.10, All areas, Private hospitals | Component for verification |
| `correctional_episodes` | 13.10, All areas, Hospitals in correctional institutions | Component for verification |

The 2019 and 2024 editions cover the full study period together. The 2021 and 2025 editions provide additional overlapping years. The runner reconciles all 25 edition/year rows, requires agreement across at least two editions for every year and checks that the three provider components in Table 13.10 add to the all-cause total in Table 13.9. Table 13.10 also lists nursing homes separately for earlier years. Summing the three named hospital sectors keeps the institutional coverage consistent throughout. The Department of Health's separate 2023 tabulation also reports 1,905,905 HA episodes and 2,266,303 across the three hospital sectors. These publications share upstream providers. [Department of Health, *Tables on Health Status and Health Services 2023*, Table A19, total row](https://www.dh.gov.hk/english/pub_rec/pub_rec_ar/pdf/2324/supplementary_table2023.pdf).

The unit is an episode ending in discharge or death, including day inpatients. The annual volume can include repeated episodes for an individual. The official tables also record a 2014 change to HA disease classification that reduced uncoded diagnoses, and service changes beginning in 2020 followed by gradual resumption in 2023. The circulatory chapter is broader than either cohort diagnosis. Cohort stays are first recorded hospitalisations after diagnosis, have unspecified admission cause and may overlap with the service totals. Index each series to its own 2019 count. Eligible person-time, a disease-specific comparator cohort and a causal counterfactual require different data.

The source cells were checked on 19 November 2026. SHA-256 of the transcribed CSV is `3c0d328399fdc1afbd2519e94e8724448ea2fd7d304f8807a6f4fbaa2c26ece1`. This digest identifies the transcription. It is separate from the published PDFs.
