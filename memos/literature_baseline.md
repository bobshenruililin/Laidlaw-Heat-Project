# Literature baseline memo

Audit-friendly summary of key literature informing the Hong Kong thermal extremes and cardiovascular admissions project. Prefer primary sources; verify any provisional citations before manuscript submission.

## 1. Older Hong Kong AMI and stroke evidence

### AMI, temperature, and pollution (Goggins et al.)

Goggins and colleagues analyzed daily AMI hospitalizations for 2000–2009 in Hong Kong and two Taiwanese cities using Poisson GAMs with smooths for temperature and humidity. In Hong Kong, cooler temperatures below an estimated ~24°C threshold were associated with higher AMI admissions; no significant heat effect was observed in that study period; same-day NO2 was the strongest pollutant predictor among those examined.

- PubMed: https://pubmed.ncbi.nlm.nih.gov/23041014/
- ORA record: https://ora.ox.ac.uk/objects/uuid:a18d41ec-ea9c-493b-a224-c09d53f2cac9
- Implication for this project: cold-dominant AMI risk is the historical baseline; contemporary reassessment should not treat a cold-dominant result as failure.

### Stroke admissions (Goggins et al.; provisional)

User-provided summary of earlier Hong Kong work indicates a strong negative association of temperature with ischemic stroke admissions (stronger in older adults and females), with hemorrhagic stroke showing more seasonal patterning and weaker temperature associations, and limited pollutant associations for stroke. **Exact citation and numerical estimates should be verified by Bob in PubMed / investigator publication list before manuscript use.**

Related recent Hong Kong stroke evidence (cold and influenza):

- Association of cold weather and influenza infection with stroke admissions (1998–2019 time-series): https://link.springer.com/article/10.1007/s00484-025-02870-2

### Temperature and AMI among diabetes patients

A Hong Kong DLNM study (2002–2011) found stronger cold-season AMI associations among patients with diabetes, and some hot-season sensitivity in that subgroup.

- https://doi.org/10.1371/journal.pmed.1002612
- https://pubmed.ncbi.nlm.nih.gov/30016318/

### Winter excess morbidity/mortality in subtropical Hong Kong

- Excess winter ischemic-heart-disease hospitalization among older adults supports continued attention to cold-related burden: https://pubmed.ncbi.nlm.nih.gov/24714058/
- Excess winter-versus-summer mortality for IHD and cerebrovascular disease (1976–2010): https://pubmed.ncbi.nlm.nih.gov/25993635/
- Extreme-cold vulnerability especially among ages 85+: https://pubmed.ncbi.nlm.nih.gov/26370114/

**Takeaway:** Historically, Hong Kong cardiovascular weather risk has often been cold-dominant despite a subtropical climate. The current project asks whether 2013–2023 patterns remain consistent with that profile under warming, aging, and changing pollution.

## 2. Monthly time-series feasibility

Monthly aggregation can detect broad seasonal and multi-day thermal burden patterns, but will blunt acute short-lag heat effects that daily DLNMs capture.

Local precedent:

- Hong Kong monthly mortality–weather analysis (1980–1994) found winter peaks in circulatory/respiratory mortality and inverse associations with minimum temperature: https://pubmed.ncbi.nlm.nih.gov/10626765/

**Implication:** Monthly data are acceptable for a publishable ecological reassessment if exposures include extreme-day counts and spell metrics, and if null heat findings are interpreted cautiously.

## 3. Hot nights and heat spells

HKO definitions used in this project:

- Hot night: Tmin ≥ 28°C
- Very hot day: Tmax ≥ 33°C
- Extremely hot day: Tmax ≥ 35°C
- Cold day: Tmin ≤ 12°C

Official context:

- HKO climate-change projections for hot nights / very hot days / cold days: https://www.hko.gov.hk/en/climate_change/proj_hk_annual_vhot_days.htm
- Daily temperature open data: https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-temperature-info-hko

Mortality evidence supporting consecutive hot nights / very hot days as informative extreme-event metrics in Hong Kong (2006–2015):

- https://pubmed.ncbi.nlm.nih.gov/31302556/

**Implication:** Prefer monthly hot-night counts and spell-length metrics over monthly mean temperature alone.

## 4. Tropical / subtropical winter-excess literature

Warm-climate settings can still show substantial cold-related cardiovascular burden because:

- absolute winter temperatures need not be extreme by temperate-zone standards to trigger physiological stress;
- housing, clothing, and behavioral adaptation may be less oriented to cold;
- influenza and other winter infections may co-occur with cold.

Hong Kong-specific winter-excess papers above support this framing. The project should therefore treat a cold-dominant contemporary result as scientifically and policy-relevant.

## 5. Administrative-data validation literature

ICD-coded stroke algorithms generally show high positive predictive values for SAH, ICH, and ischemic stroke, but validity varies by code set and algorithm.

- Systematic review of stroke coding validity: https://pubmed.ncbi.nlm.nih.gov/26292280/

**Implication for this project:**

- Prefer principal diagnosis.
- Confirm ICD-9-CM vs ICD-10 vs mixed coding at HA.
- Sensitivity analyses around unspecified stroke (`436` / `I64`) and hemorrhagic `432.x`.
- Exclude TIA and stroke sequelae from primary definitions.

## 6. Pollution–temperature interaction literature

### Historical Hong Kong AMI work

NO2 was a strong same-day predictor in the earlier Goggins AMI analysis (see above).

### Contemporary Hong Kong pollution context

EPD reporting indicates long-term declines in ambient PM10, PM2.5, and NO2, while ozone remains a concern / upward trajectory in recent years (see EPD Air Quality Reports, e.g. 2023):

- https://www.aqhi.gov.hk/ (Air Quality Reports / AQHI portal)
- EPIC historical data portal: https://cd.epic.epd.gov.hk/EPICDI/air/

### Ozone and cardiovascular admissions

Recent evidence supports short-term O3 associations with MI and stroke admissions, generally with small effect sizes and heterogeneity:

- Example review/meta-analysis entry point: https://pubmed.ncbi.nlm.nih.gov/40878994/

**Analytical implication:** Stage pollution models. Do not treat O3 solely as a conventional confounder; it may be correlated with, interact with, or partly mediate hot sunny conditions. Report total thermal associations (no O3) separately from pathway-adjusted associations.

## 7. Design implications for the present study

| Historical finding | Contemporary design response |
|---|---|
| Cold-dominant AMI/stroke risk | Keep cold days as co-primary exposure; do not frame cold results as failure |
| Little heat effect in earlier eras | Test hot nights / VHD / spells; interpret nulls cautiously given monthly aggregation |
| NO2 important for AMI | Include NO2 in staged models; expect changing pollution mix |
| Aging modifies risk | Separate 65–69, 70–74, 75–84, 85+ |
| Daily DLNM vs monthly counts | Avoid direct coefficient comparison with 2000–2009 daily studies unless harmonized |

## 8. Outstanding bibliographic tasks for Bob

1. Verify exact citation and estimates for the earlier Goggins ischemic/hemorrhagic stroke admissions paper.
2. Confirm HA coding-era literature or internal documentation for ICD transitions.
3. Add CHP influenza surveillance citations once flu adjustment is finalized.
4. Add Clean Air Plan for Hong Kong policy citations for pollution-context paragraphs.
5. Update 2024 HKO “hottest year” citation if 2024 is used descriptively: https://www.hko.gov.hk/en/wxinfo/pastwx/2024/ywx2024.htm
