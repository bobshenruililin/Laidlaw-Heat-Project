# Peer-city ERA5-Land cache

**Provenance:** `REAL_PUBLIC`. Daily 2 m and apparent temperatures plus precipitation from the Open-Meteo ERA5-Land archive, 2013-01-01 to 2023-12-31, local timezone of each city.

These files are **not** HKO Headquarters observations. They exist so `python3 scripts/48_peer_cities_thermal_atlas.py --skip-fetch` can rebuild the atlas without a network call.

Do not quote flag totals from this cache as HKO yearbook numbers. Do not merge health outcomes into these files.
