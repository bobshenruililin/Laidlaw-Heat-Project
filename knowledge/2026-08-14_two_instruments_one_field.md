# Two instruments, one field — 14 August 2026

**Mode:** Ship.  
**Provenance:** `REAL_PUBLIC` HKO Headquarters and Open-Meteo ERA5-Land, 2013–2023. Scripts 51–59.  
**Not:** health findings, q-values, Gate 3, or form 2a.

The internship maps looked like a second paper. They are not. They are the identification of the first.

## The insight

EOF1 of de-seasoned Pearl River Delta Tmin holds about **92%** of daily anomaly variance. The basin’s temperature field is nearly one degree of freedom. A well-sited station is therefore enough for **means**.

Jaccard of the official 28°C night, station vs ERA5 at the same coordinate, is **0.031**. Frequency can be matched by moving ERA5 to 26.4°C (448 nights). The nights cannot (max Jaccard **0.471** at 26.3°C). A station is therefore **not** enough to export the **flag**.

The live paper uses both encodings: monthly means and official count flags. That is the contribution. The maps do not rescue all core *q* > 0.19. They show why a twelve-contrast panel can be well specified and still be thinly identified.

## What is new tonight, not map tourism

1. **Intensive vs extensive** (script 57). After month indicators, **95.4%** of remaining hot-night sum of squares is *how many* nights an already-hot month contained. June–September recorded at least one official hot night in **every** year of 2013–2023. Every June had at least six. July 2013 had **1** night; July 2022 had **25**; July alone is **44%** of the identifying residual. May and October are the only mixed months. Cold days have **no** always-on winter month (38.8% of their identifying SS is years with zero events). Mean temperature has no extensive margin at all: its 4% residual is intensity of the monthly mean.

2. **First-wave HM/CM rank** (script 58). The on-disk file is **twelve** named binaries plus HM23 event starts, not 98 tests. CM05 is a zero column. Eleven live flags have correlation effective rank **3.92**. Heat never co-fires with cold (Jaccard 0). Nested inner flags (HM15 ⊂ HM08 ⊂ HM32; CM08 ⊂ CM03; CM15 ⊂ CM30) are not independent sensitivities. An effective-rank statement is not a licence to refit the catalogue.

3. **The 14 nights** (script 59). The two dry-bulb thermometers agree on fourteen dates. They agree when Headquarters is already well past 28°C (hottest overlap: 8 August 2015, HKO 30.0°C). They miss 71 station nights that were already ≥29°C, including 14 September 2022 (HKO 29.6°C, ERA5 25.6°C) and a 5.3°C gap on 22 September 2023. ERA5’s three unique nights are nights Headquarters still called ordinary (27.9, 26.9, 26.4°C). Apparent temperature is a third encoding, not a correction.

Together: Guo 2024 = wrong *metric*; Mistry 2022 = means usually travel; this internship = wrong *instrument and place*; tonight = the flag’s remaining identification is intensity inside an always-on summer, and the two thermometers only clasp on the extreme tail.

## Paper sentences (Hogan sees them first)

Already parked for Limitations (monthly grain only): [`../manuscript/live_collaborative/limitation_station_grid_bridge.md`](../manuscript/live_collaborative/limitation_station_grid_bridge.md).

Optional second limitation, a different claim, also Hogan-first: [`../manuscript/live_collaborative/limitation_intensive_margin.md`](../manuscript/live_collaborative/limitation_intensive_margin.md).

Do not paste daily Jaccard, the 14 nights, or 0.045-as-attenuation into the live file.

## Supervisor one-liner (unchanged)

We measured our own largest limitation before a reviewer could, and the measurement defends the design.

## Claim boundaries

No hospital counts entered these scripts. Do not treat 0.045, 0.954, 3.92, or 14 overlapping nights as health results. Live paper stays on Headquarters. Gate 3 stays open. Form 2a is a different object.
