#!/usr/bin/env python3
"""Peer-city thermal atlas, 2013–2023.

Public ERA5-Land via Open-Meteo, calibrated against HKO Headquarters for
Hong Kong. Applies three encodings:

  1. HKO official flags transported as-is (Tmin>=28, Tmax>=33, Tmin<=12)
  2. City-specific study-window percentiles (p95 Tmax, p05 Tmin)
  3. The same HKO thresholds on Open-Meteo apparent temperature

EXPOSURE ONLY. No health coefficients. No HA rows. Literature cards are
other people's published findings and must not be read as this project's
CHD/HF results.

Usage:
  python3 scripts/48_peer_cities_thermal_atlas.py
  python3 scripts/48_peer_cities_thermal_atlas.py --skip-fetch
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data_processed" / "peer_cities" / "cache"
OUT_TAB = ROOT / "outputs" / "peer_cities"
OUT_DOCS = ROOT / "docs" / "peers"
OUT_FIG = ROOT / "figures" / "peer_cities"
HKO_DAILY = ROOT / "data_processed" / "md_daily_weather_design_2013_2023.csv"
HKO_MONTHLY = ROOT / "data_processed" / "climate_monthly_2013_2023.csv"

START = "2013-01-01"
END = "2023-12-31"
HN_C, VHD_C, CD_C = 28.0, 33.0, 12.0
ARCHIVE = "https://archive-api.open-meteo.com/v1/archive"
CACHE_FIELDS = [
    "date", "tmax", "tmin", "tmean", "atmax", "atmin", "atmean", "precip",
    "source", "city_id",
]
DAILY_VARS = (
    "temperature_2m_max,temperature_2m_min,temperature_2m_mean,"
    "apparent_temperature_max,apparent_temperature_min,apparent_temperature_mean,"
    "precipitation_sum"
)

CITIES = [
    {"id": "hong_kong", "name": "Hong Kong", "lat": 22.3022, "lon": 114.1742,
     "tz": "Asia/Hong_Kong", "role": "reference", "group": "Pearl River Delta",
     "hemisphere": "N"},
    {"id": "shenzhen", "name": "Shenzhen", "lat": 22.5431, "lon": 114.0579,
     "tz": "Asia/Shanghai", "role": "peer", "group": "Pearl River Delta",
     "hemisphere": "N"},
    {"id": "guangzhou", "name": "Guangzhou", "lat": 23.1291, "lon": 113.2644,
     "tz": "Asia/Shanghai", "role": "peer", "group": "Pearl River Delta",
     "hemisphere": "N"},
    {"id": "taipei", "name": "Taipei", "lat": 25.0375, "lon": 121.5637,
     "tz": "Asia/Taipei", "role": "peer", "group": "Humid subtropical",
     "hemisphere": "N"},
    {"id": "naha", "name": "Naha", "lat": 26.2123, "lon": 127.6792,
     "tz": "Asia/Tokyo", "role": "peer", "group": "Humid subtropical",
     "hemisphere": "N"},
    {"id": "hanoi", "name": "Hanoi", "lat": 21.0278, "lon": 105.8342,
     "tz": "Asia/Bangkok", "role": "peer", "group": "Humid subtropical",
     "hemisphere": "N"},
    {"id": "miami", "name": "Miami", "lat": 25.7617, "lon": -80.1918,
     "tz": "America/New_York", "role": "peer", "group": "Humid subtropical",
     "hemisphere": "N"},
    {"id": "houston", "name": "Houston", "lat": 29.7604, "lon": -95.3698,
     "tz": "America/Chicago", "role": "peer", "group": "Humid subtropical",
     "hemisphere": "N"},
    {"id": "brisbane", "name": "Brisbane", "lat": -27.4698, "lon": 153.0251,
     "tz": "Australia/Brisbane", "role": "peer", "group": "Humid subtropical",
     "hemisphere": "S"},
    {"id": "singapore", "name": "Singapore", "lat": 1.3521, "lon": 103.8198,
     "tz": "Asia/Singapore", "role": "contrast", "group": "Tropical",
     "hemisphere": "N"},
    {"id": "manila", "name": "Manila", "lat": 14.5995, "lon": 120.9842,
     "tz": "Asia/Manila", "role": "contrast", "group": "Tropical",
     "hemisphere": "N"},
    {"id": "haikou", "name": "Haikou", "lat": 20.0444, "lon": 110.1989,
     "tz": "Asia/Shanghai", "role": "contrast", "group": "Tropical",
     "hemisphere": "N"},
    {"id": "shanghai", "name": "Shanghai", "lat": 31.2304, "lon": 121.4737,
     "tz": "Asia/Shanghai", "role": "contrast", "group": "Humid temperate",
     "hemisphere": "N"},
    {"id": "fukuoka", "name": "Fukuoka", "lat": 33.5904, "lon": 130.4017,
     "tz": "Asia/Tokyo", "role": "contrast", "group": "Humid temperate",
     "hemisphere": "N"},
    {"id": "seoul", "name": "Seoul", "lat": 37.5665, "lon": 126.9780,
     "tz": "Asia/Seoul", "role": "contrast", "group": "Humid temperate",
     "hemisphere": "N"},
    {"id": "phoenix", "name": "Phoenix", "lat": 33.4484, "lon": -112.0740,
     "tz": "America/Phoenix", "role": "contrast", "group": "Hot desert",
     "hemisphere": "N"},
]


def winter_months(hemisphere: str) -> set[int]:
    return {12, 1, 2} if hemisphere == "N" else {6, 7, 8}


def percentile(xs: list[float], p: float) -> float:
    ys = sorted(xs)
    if not ys:
        raise ValueError("empty percentile")
    k = (len(ys) - 1) * (p / 100.0)
    f = int(math.floor(k))
    c = min(f + 1, len(ys) - 1)
    if f == c:
        return ys[f]
    return ys[f] + (ys[c] - ys[f]) * (k - f)


def rmse(pairs: list[tuple[float, float]]) -> float:
    if not pairs:
        return float("nan")
    return math.sqrt(sum((a - b) ** 2 for a, b in pairs) / len(pairs))


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else float("nan")


def _f(x) -> float | None:
    if x is None or x == "":
        return None
    return float(x)


def _fmt(x) -> str:
    return "" if x is None else f"{float(x):.2f}"


def cache_complete(path: Path) -> bool:
    if not path.exists():
        return False
    with path.open() as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return False
        if any(col not in reader.fieldnames for col in CACHE_FIELDS):
            return False
        n = sum(1 for _ in reader)
    return n >= 4000


def fetch_city(city: dict, skip: bool) -> list[dict]:
    CACHE.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE / f"{city['id']}_daily.csv"
    if skip and cache_complete(cache_path):
        return list(csv.DictReader(cache_path.open()))
    if skip and not cache_complete(cache_path):
        raise RuntimeError(
            f"Incomplete cache for {city['id']}; rerun without --skip-fetch"
        )
    params = {
        "latitude": f"{city['lat']:.4f}",
        "longitude": f"{city['lon']:.4f}",
        "start_date": START,
        "end_date": END,
        "daily": DAILY_VARS,
        "timezone": city["tz"],
        "temperature_unit": "celsius",
    }
    url = ARCHIVE + "?" + urllib.parse.urlencode(params)
    last_err = None
    body = None
    for attempt in range(5):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "Laidlaw-Heat-Project/peer-atlas"}
            )
            with urllib.request.urlopen(req, timeout=90) as resp:
                body = json.loads(resp.read().decode())
            break
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_err = exc
            time.sleep(2 ** attempt)
    if body is None:
        raise RuntimeError(f"Open-Meteo failed for {city['id']}: {last_err}")
    daily = body["daily"]
    rows = []
    for i, date in enumerate(daily["time"]):
        tmax = daily["temperature_2m_max"][i]
        tmin = daily["temperature_2m_min"][i]
        tmean = daily["temperature_2m_mean"][i]
        if tmax is None or tmin is None or tmean is None:
            continue
        rows.append({
            "date": date,
            "tmax": _fmt(tmax),
            "tmin": _fmt(tmin),
            "tmean": _fmt(tmean),
            "atmax": _fmt(daily["apparent_temperature_max"][i]),
            "atmin": _fmt(daily["apparent_temperature_min"][i]),
            "atmean": _fmt(daily["apparent_temperature_mean"][i]),
            "precip": _fmt(daily["precipitation_sum"][i] or 0.0),
            "source": "OPEN_METEO_ERA5_LAND",
            "city_id": city["id"],
        })
    with cache_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CACHE_FIELDS)
        w.writeheader()
        w.writerows(rows)
    time.sleep(0.45)
    return rows


def encode_days(rows: list[dict], p95_tmax: float, p05_tmin: float) -> list[dict]:
    out = []
    for r in rows:
        tmax = float(r["tmax"])
        tmin = float(r["tmin"])
        tmean = float(r["tmean"])
        atmax = _f(r.get("atmax"))
        atmin = _f(r.get("atmin"))
        atmean = _f(r.get("atmean"))
        precip = _f(r.get("precip")) or 0.0
        dt = datetime.strptime(r["date"], "%Y-%m-%d")
        out.append({
            "date": r["date"],
            "year": dt.year,
            "month": dt.month,
            "tmax": tmax,
            "tmin": tmin,
            "tmean": tmean,
            "atmax": atmax,
            "atmin": atmin,
            "atmean": atmean,
            "precip": precip,
            "hn_hko": int(tmin >= HN_C),
            "vhd_hko": int(tmax >= VHD_C),
            "cd_hko": int(tmin <= CD_C),
            "hn_at": int(atmin is not None and atmin >= HN_C),
            "vhd_at": int(atmax is not None and atmax >= VHD_C),
            "cd_at": int(atmin is not None and atmin <= CD_C),
            "hot_p95": int(tmax >= p95_tmax),
            "cold_p05": int(tmin <= p05_tmin),
        })
    return out


def month_id(year: int, month: int) -> str:
    return f"{year:04d}-{month:02d}"


def aggregate_monthly(days: list[dict], city: dict) -> list[dict]:
    buckets: dict[str, list[dict]] = defaultdict(list)
    for d in days:
        buckets[month_id(d["year"], d["month"])].append(d)
    winter = winter_months(city["hemisphere"])
    months = []
    for mid in sorted(buckets):
        chunk = buckets[mid]
        y, m = int(mid[:4]), int(mid[5:7])
        months.append({
            "city_id": city["id"],
            "month_id": mid,
            "year": y,
            "month": m,
            "n_days": len(chunk),
            "mean_t": round(mean([d["tmean"] for d in chunk]), 3),
            "mean_tmax": round(mean([d["tmax"] for d in chunk]), 3),
            "mean_tmin": round(mean([d["tmin"] for d in chunk]), 3),
            "mean_at": round(mean([d["atmean"] for d in chunk if d["atmean"] is not None]), 3),
            "precip_mm": round(sum(d["precip"] for d in chunk), 2),
            "hn_hko": sum(d["hn_hko"] for d in chunk),
            "vhd_hko": sum(d["vhd_hko"] for d in chunk),
            "cd_hko": sum(d["cd_hko"] for d in chunk),
            "hn_at": sum(d["hn_at"] for d in chunk),
            "vhd_at": sum(d["vhd_at"] for d in chunk),
            "cd_at": sum(d["cd_at"] for d in chunk),
            "hot_p95": sum(d["hot_p95"] for d in chunk),
            "cold_p05": sum(d["cold_p05"] for d in chunk),
            "is_local_winter": int(m in winter),
        })
    return months


def city_summary(city: dict, days: list[dict], months: list[dict], p95: float, p05: float) -> dict:
    winter = winter_months(city["hemisphere"])
    cd = sum(d["cd_hko"] for d in days)
    cd_w = sum(d["cd_hko"] for d in days if d["month"] in winter)
    hn = sum(d["hn_hko"] for d in days)
    vhd = sum(d["vhd_hko"] for d in days)
    climatology = []
    for m in range(1, 13):
        xs = [row["mean_t"] for row in months if row["month"] == m]
        climatology.append(round(mean(xs), 3) if xs else None)
    amp = max(x for x in climatology if x is not None) - min(x for x in climatology if x is not None)
    n_years = 11.0
    precip_year = sum(d["precip"] for d in days) / n_years
    ats = [d["atmean"] for d in days if d["atmean"] is not None]
    annual = []
    for y in range(2013, 2024):
        chunk = [d for d in days if d["year"] == y]
        annual.append({
            "year": y,
            "mean_t": round(mean([d["tmean"] for d in chunk]), 3),
            "hn_hko": sum(d["hn_hko"] for d in chunk),
            "vhd_hko": sum(d["vhd_hko"] for d in chunk),
            "cd_hko": sum(d["cd_hko"] for d in chunk),
            "hn_at": sum(d["hn_at"] for d in chunk),
            "vhd_at": sum(d["vhd_at"] for d in chunk),
            "hot_p95": sum(d["hot_p95"] for d in chunk),
            "cold_p05": sum(d["cold_p05"] for d in chunk),
            "precip_mm": round(sum(d["precip"] for d in chunk), 1),
        })
    return {
        **city,
        "n_days": len(days),
        "p95_tmax": round(p95, 3),
        "p05_tmin": round(p05, 3),
        "mean_t": round(mean([d["tmean"] for d in days]), 3),
        "mean_tmax": round(mean([d["tmax"] for d in days]), 3),
        "mean_tmin": round(mean([d["tmin"] for d in days]), 3),
        "mean_at": round(mean(ats), 3) if ats else None,
        "seasonal_amp": round(amp, 3),
        "precip_mm_year": round(precip_year, 1),
        "climatology_mean_t": climatology,
        "hn_hko_total": hn,
        "vhd_hko_total": vhd,
        "cd_hko_total": cd,
        "cd_hko_local_winter": cd_w,
        "cd_hko_winter_share": round(cd_w / cd, 4) if cd else None,
        "hn_at_total": sum(d["hn_at"] for d in days),
        "vhd_at_total": sum(d["vhd_at"] for d in days),
        "cd_at_total": sum(d["cd_at"] for d in days),
        "hot_p95_total": sum(d["hot_p95"] for d in days),
        "cold_p05_total": sum(d["cold_p05"] for d in days),
        "annual": annual,
        "provenance": "OPEN_METEO_ERA5_LAND_PUBLIC",
    }


def zscore_distance(features: dict[str, list[float]]) -> dict[str, float]:
    ids = list(features)
    keys = ["mean_t", "seasonal_amp", "hn_rate", "cd_rate"]
    mu = {k: mean([features[i][k] for i in ids]) for k in keys}
    sd = {}
    for k in keys:
        xs = [features[i][k] for i in ids]
        var = mean([(x - mu[k]) ** 2 for x in xs])
        sd[k] = math.sqrt(var) if var > 1e-12 else 1.0
    ref = features["hong_kong"]
    dist = {}
    for i in ids:
        acc = 0.0
        for k in keys:
            acc += ((features[i][k] - ref[k]) / sd[k]) ** 2
        dist[i] = round(math.sqrt(acc), 4)
    return dist


def load_hko_daily() -> dict[str, dict]:
    out = {}
    with HKO_DAILY.open() as f:
        for row in csv.DictReader(f):
            out[row["date"][:10]] = {
                "tmax": float(row["tmax"]),
                "tmin": float(row["tmin"]),
                "tmean": float(row["tmean"]),
                "hn": int(float(row["hot_night"])),
                "vhd": int(float(row["very_hot_day"])),
                "cd": int(float(row["cold_day"])),
            }
    return out


def _jaccard(a: int, b: int, both: int) -> float | None:
    denom = a + b - both
    return round(both / denom, 4) if denom else None


def calibrate(om_days: list[dict], hko: dict[str, dict]) -> dict:
    pairs_t, pairs_n, pairs_x = [], [], []
    om_hn = om_vhd = om_cd = 0
    hko_hn = hko_vhd = hko_cd = 0
    both_hn = both_vhd = both_cd = 0
    adj_hn = adj_vhd = adj_cd = 0
    at_hn = at_vhd = at_cd = 0
    n = 0
    for d in om_days:
        rec = hko.get(d["date"])
        if rec is None:
            continue
        n += 1
        pairs_t.append((d["tmean"], rec["tmean"]))
        pairs_n.append((d["tmin"], rec["tmin"]))
        pairs_x.append((d["tmax"], rec["tmax"]))
        om_hn += d["hn_hko"]
        om_vhd += d["vhd_hko"]
        om_cd += d["cd_hko"]
        hko_hn += rec["hn"]
        hko_vhd += rec["vhd"]
        hko_cd += rec["cd"]
        both_hn += int(d["hn_hko"] and rec["hn"])
        both_vhd += int(d["vhd_hko"] and rec["vhd"])
        both_cd += int(d["cd_hko"] and rec["cd"])
        at_hn += d["hn_at"]
        at_vhd += d["vhd_at"]
        at_cd += d["cd_at"]
    bias_tmin = mean([a - b for a, b in pairs_n]) if pairs_n else float("nan")
    for d in om_days:
        if d["date"] not in hko:
            continue
        tmin_a = d["tmin"] - bias_tmin
        tmax_a = d["tmax"] - bias_tmin
        adj_hn += int(tmin_a >= HN_C)
        adj_vhd += int(tmax_a >= VHD_C)
        adj_cd += int(tmin_a <= CD_C)
    return {
        "n_matched_days": n,
        "rmse_tmean": round(rmse(pairs_t), 3),
        "rmse_tmin": round(rmse(pairs_n), 3),
        "rmse_tmax": round(rmse(pairs_x), 3),
        "bias_openmeteo_minus_hko_tmin": round(bias_tmin, 3),
        "openmeteo_hn_total": om_hn,
        "hko_hn_total": hko_hn,
        "openmeteo_vhd_total": om_vhd,
        "hko_vhd_total": hko_vhd,
        "openmeteo_cd_total": om_cd,
        "hko_cd_total": hko_cd,
        "openmeteo_apparent_hn_total": at_hn,
        "openmeteo_apparent_vhd_total": at_vhd,
        "openmeteo_apparent_cd_total": at_cd,
        "jaccard_hn": _jaccard(om_hn, hko_hn, both_hn),
        "jaccard_vhd": _jaccard(om_vhd, hko_vhd, both_vhd),
        "jaccard_cd": _jaccard(om_cd, hko_cd, both_cd),
        "zero_agreement_is_misleading": True,
        "bias_adjusted_openmeteo_hn": adj_hn,
        "bias_adjusted_openmeteo_vhd": adj_vhd,
        "bias_adjusted_openmeteo_cd": adj_cd,
        "note": (
            "ERA5-Land grid vs HKO Headquarters station. A ~1.5 °C cold bias in "
            "night minima collapses HKO's 28 °C hot-night flag (17 vs 449) and "
            "inflates the 12 °C cold-day flag. Apparent temperature on the same "
            "grid is a third object and overshoots the station (thousands of "
            "nights ≥28 °C in humid cities). Use Open-Meteo for same-source "
            "cross-city ranks; use HKO for the live paper."
        ),
    }


LIT = [
    {
        "city_id": "hong_kong",
        "kind": "published_other_study",
        "citation": "Jingwen Liu et al. (2020), Sustainable Cities and Society 57:102131.",
        "doi": "10.1016/j.scs.2020.102131",
        "one_line": "Hong Kong daily mortality 2006–2016: cold-attributable fraction 4.72% vs heat 0.16%. Mortality AF, not this project's CHD/HF counts.",
    },
    {
        "city_id": "shenzhen",
        "kind": "published_other_study",
        "citation": "Jingesi, Yin, Huang et al. (2024), BMC Public Health 24:2861.",
        "doi": "10.1186/s12889-024-20144-1",
        "one_line": "Shenzhen ambulance CVD 2013–2019: reverse-J; thermal-stress AF 10.81%, of which cold 10.42% vs heat 0.39%. Daily UTCI, not our monthly first-event counts.",
    },
    {
        "city_id": "taipei",
        "kind": "published_other_study",
        "citation": "Wang et al. (2014), PLOS ONE 9(1):e82678.",
        "doi": "10.1371/journal.pone.0082678",
        "one_line": "Four Taiwan metros 1994–2007: prolonged cold raised CVD mortality more than heat (21-day lags). Daily mortality, not our monthly CHD/HF file.",
    },
    {
        "city_id": "singapore",
        "kind": "published_other_study",
        "citation": "Seah et al. (2022), Science of the Total Environment 850:158010.",
        "doi": "10.1016/j.scitotenv.2022.158010",
        "one_line": "Singapore NSTEMI 2009–2018: cooler temperatures raised risk over 10 days (RR 1.12 at the 10th percentile). Tropical daily AMI, not Hong Kong monthly first events.",
    },
    {
        "city_id": "brisbane",
        "kind": "published_other_study",
        "citation": "Yu et al. (2011), Heart 97:1089–1093.",
        "doi": "10.1136/hrt.2010.217166",
        "one_line": "Brisbane CVD deaths 1996–2004: heat effect lag 0–1; cold effect lag 10–15. Southern-hemisphere daily mortality, not our estimand.",
    },
    {
        "city_id": "miami",
        "kind": "published_other_study",
        "citation": "Karanja et al. (2024), Bulletin of the American Meteorological Society.",
        "doi": "10.1175/BAMS-D-23-0055.1",
        "one_line": "Miami-Dade summer 2015–2019 all-cause mortality: 7.8% of deaths on days with heat index >30 °C. All-cause, not CVD hospitalisation, not Hong Kong.",
    },
    {
        "city_id": "hanoi",
        "kind": "published_other_study",
        "citation": "Xuan et al. (2014), Global Health Action 7:23115.",
        "doi": "10.3402/gha.v7.23115",
        "one_line": "Hanoi older-adult mortality 2005–2010: deaths 21% higher in the cold season than the warm season. Monthly mortality, not our CHD/HF first-event counts.",
    },
    {
        "city_id": "houston",
        "kind": "published_other_study",
        "citation": "Zhang, Chen and Begley (2015), Environmental Health 14:11.",
        "doi": "10.1186/1476-069X-14-11",
        "one_line": "Houston 2011 heat wave: 3.6% excess emergency-department visits; all-cause mortality not significant. Event study, not a monthly first-hospitalisation panel.",
    },
    {
        "city_id": "manila",
        "kind": "published_other_study",
        "citation": "Seposo, Dang and Honda (2015), Int. J. Environ. Res. Public Health 12:6842–6857.",
        "doi": "10.3390/ijerph120606842",
        "one_line": "Manila City mortality 2006–2010: minimum-mortality temperature 30 °C. Tropical daily DLNM, not our estimand.",
    },
    {
        "city_id": "phoenix",
        "kind": "published_other_study",
        "citation": "Hondula, Georgescu and Balling (2014), Science of the Total Environment 490:488–496.",
        "doi": "10.1016/j.scitotenv.2014.04.130",
        "one_line": "Maricopa County (Phoenix) heat-mortality projections depend on whether Tmin, Tmean or Tmax is the exposure. Dry-heat desert, not humid-subtropical Hong Kong.",
    },
    {
        "city_id": "seoul",
        "kind": "published_other_study",
        "citation": "Ha, Shin and Kim (2011), Science of the Total Environment 409:3274–3280.",
        "doi": "10.1016/j.scitotenv.2011.05.034",
        "one_line": "Seoul, Daegu and Incheon summer mortality 1991–2008: heat effects persisted about five days. Temperate East-Asian daily mortality, not our monthly CHD/HF file.",
    },
    {
        "city_id": "_network",
        "kind": "published_other_study",
        "citation": "Gasparrini et al. (2015), The Lancet 386:369–375.",
        "doi": "10.1016/S0140-6736(14)62114-0",
        "one_line": "MCC network: across 384 locations, cold explained far more attributable mortality than heat. Cross-city mortality, not this project's CHD/HF panel.",
    },
]


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def _svg_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def write_climate_space_svg(summaries: list[dict], path: Path) -> None:
    w, h = 760, 460
    pad_l, pad_r, pad_t, pad_b = 64, 28, 28, 52
    amps = [s["seasonal_amp"] for s in summaries]
    means = [s["mean_t"] for s in summaries]
    x0, x1 = 0.0, max(amps) * 1.12
    y0, y1 = min(means) - 1.5, max(means) + 1.5

    def xx(v: float) -> float:
        return pad_l + (v - x0) / (x1 - x0) * (w - pad_l - pad_r)

    def yy(v: float) -> float:
        return pad_t + (y1 - v) / (y1 - y0) * (h - pad_t - pad_b)

    colour = {"reference": "#0c6b74", "peer": "#c24e16", "contrast": "#1f5f8a"}
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img">',
        '<rect width="100%" height="100%" fill="#fffdf8"/>',
        f'<text x="{w/2}" y="22" text-anchor="middle" font-family="Georgia, serif" font-size="16" fill="#12181f">Climate space, 2013–2023 · ERA5-Land</text>',
        f'<line x1="{pad_l}" y1="{h-pad_b}" x2="{w-pad_r}" y2="{h-pad_b}" stroke="#12181f" stroke-opacity=".35"/>',
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{h-pad_b}" stroke="#12181f" stroke-opacity=".35"/>',
        f'<text x="{(pad_l+w-pad_r)/2}" y="{h-14}" text-anchor="middle" font-size="12" fill="#5b6773" font-family="sans-serif">Seasonal amplitude (°C)</text>',
        f'<text x="18" y="{(pad_t+h-pad_b)/2}" text-anchor="middle" font-size="12" fill="#5b6773" font-family="sans-serif" transform="rotate(-90 18 {(pad_t+h-pad_b)/2})">Mean temperature (°C)</text>',
    ]
    for tick in range(int(math.floor(x0)), int(math.ceil(x1)) + 1, 5):
        parts.append(
            f'<text x="{xx(tick)}" y="{h-pad_b+16}" text-anchor="middle" font-size="11" fill="#5b6773" font-family="sans-serif">{tick}</text>'
        )
    for tick in range(int(math.ceil(y0)), int(math.floor(y1)) + 1, 4):
        parts.append(
            f'<text x="{pad_l-8}" y="{yy(tick)+4}" text-anchor="end" font-size="11" fill="#5b6773" font-family="sans-serif">{tick}</text>'
        )
    for s in summaries:
        r = 9 if s["id"] == "hong_kong" else 6
        parts.append(
            f'<circle cx="{xx(s["seasonal_amp"]):.1f}" cy="{yy(s["mean_t"]):.1f}" r="{r}" '
            f'fill="{colour[s["role"]]}" stroke="#fff" stroke-width="1.6"/>'
        )
        dx = 10 if s["lon"] >= 0 else -10
        anchor = "start" if dx > 0 else "end"
        parts.append(
            f'<text x="{xx(s["seasonal_amp"])+dx:.1f}" y="{yy(s["mean_t"])+4:.1f}" '
            f'text-anchor="{anchor}" font-size="11" font-family="sans-serif" fill="#12181f">{_svg_escape(s["name"])}</text>'
        )
    parts.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts) + "\n")


def write_calibration_svg(cal: dict, path: Path) -> None:
    w, h = 720, 280
    rows = [
        ("Hot nights", cal["hko_hn_total"], cal["openmeteo_hn_total"], "#c24e16"),
        ("Very hot days", cal["hko_vhd_total"], cal["openmeteo_vhd_total"], "#c9a227"),
        ("Cold days", cal["hko_cd_total"], cal["openmeteo_cd_total"], "#1f5f8a"),
    ]
    maxn = max(max(a, b) for _, a, b, _ in rows)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img">',
        '<rect width="100%" height="100%" fill="#fffdf8"/>',
        '<text x="360" y="24" text-anchor="middle" font-family="Georgia, serif" font-size="16" fill="#12181f">Hong Kong: HKO Headquarters vs ERA5-Land, same 28/33/12 °C rules</text>',
        '<text x="210" y="48" text-anchor="middle" font-size="12" fill="#5b6773" font-family="sans-serif">HKO station</text>',
        '<text x="510" y="48" text-anchor="middle" font-size="12" fill="#5b6773" font-family="sans-serif">ERA5-Land grid</text>',
    ]
    for i, (lab, a, b, col) in enumerate(rows):
        y = 72 + i * 64
        wa = 8 + 240 * (a / maxn)
        wb = 8 + 240 * (b / maxn)
        parts.append(f'<text x="24" y="{y+18}" font-size="13" font-family="sans-serif" fill="#12181f">{lab}</text>')
        parts.append(f'<rect x="{210-wa}" y="{y}" width="{wa}" height="22" rx="6" fill="{col}"/>')
        parts.append(f'<text x="{210-wa-8}" y="{y+16}" text-anchor="end" font-size="13" font-family="sans-serif">{a}</text>')
        parts.append(f'<rect x="510" y="{y}" width="{wb}" height="22" rx="6" fill="{col}" fill-opacity=".55"/>')
        parts.append(f'<text x="{510+wb+8}" y="{y+16}" font-size="13" font-family="sans-serif">{b}</text>')
    parts.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-fetch", action="store_true")
    args = parser.parse_args()
    skip = args.skip_fetch or os.environ.get("PEER_ATLAS_SKIP_FETCH") == "1"

    all_months = []
    summaries = []
    city_days: dict[str, list[dict]] = {}

    for city in CITIES:
        raw = fetch_city(city, skip=skip)
        tmaxs = [float(r["tmax"]) for r in raw]
        tmins = [float(r["tmin"]) for r in raw]
        p95 = percentile(tmaxs, 95)
        p05 = percentile(tmins, 5)
        days = encode_days(raw, p95, p05)
        city_days[city["id"]] = days
        months = aggregate_monthly(days, city)
        all_months.extend(months)
        summaries.append(city_summary(city, days, months, p95, p05))
        s = summaries[-1]
        print(
            f"{city['id']:12s} days={len(days):4d} meanT={s['mean_t']:.2f} "
            f"amp={s['seasonal_amp']:.1f} HN={s['hn_hko_total']:4d} "
            f"CD={s['cd_hko_total']:4d} AThn={s['hn_at_total']:4d} "
            f"P={s['precip_mm_year']:.0f}mm",
            flush=True,
        )

    features = {}
    n_years = 11.0
    for s in summaries:
        features[s["id"]] = {
            "mean_t": s["mean_t"],
            "seasonal_amp": s["seasonal_amp"],
            "hn_rate": s["hn_hko_total"] / n_years,
            "cd_rate": s["cd_hko_total"] / n_years,
        }
    dist = zscore_distance(features)
    for s in summaries:
        s["distance_to_hk_openmeteo"] = dist[s["id"]]

    hko = load_hko_daily()
    cal = calibrate(city_days["hong_kong"], hko)
    buckets: dict[int, list[float]] = defaultdict(list)
    with HKO_MONTHLY.open() as f:
        for row in csv.DictReader(f):
            buckets[int(row["month"])].append(float(row["mean_temp"]))
    hko_official_climatology = [round(mean(buckets[m]), 3) for m in range(1, 13)]

    rank = sorted(summaries, key=lambda s: s["distance_to_hk_openmeteo"])
    OUT_TAB.mkdir(parents=True, exist_ok=True)
    write_csv(OUT_TAB / "peer_city_month.csv", all_months)
    skip_keys = {"annual", "climatology_mean_t"}
    write_csv(OUT_TAB / "peer_city_summary.csv", [
        {k: v for k, v in s.items() if k not in skip_keys}
        for s in summaries
    ])
    write_csv(OUT_TAB / "hk_openmeteo_vs_hko_calibration.csv", [cal])

    payload = {
        "title": "Peer-city thermal atlas",
        "window": {"start": START, "end": END, "n_years": 11, "DATA_START": START, "DATA_END": END},
        "provenance": "REAL_PUBLIC. Open-Meteo ERA5-Land daily 2 m temperatures and apparent temperatures; HKO Headquarters for Hong Kong calibration. Exposure descriptives only. No health outcomes. No project coefficients.",
        "thresholds_hko": {
            "hot_night_tmin_ge": HN_C,
            "very_hot_day_tmax_ge": VHD_C,
            "cold_day_tmin_le": CD_C,
        },
        "percentile_note": "p95 Tmax and p05 Tmin are study-window (2013–2023) only; not Hogan-locked.",
        "calibration": cal,
        "hko_official": {
            "source": "REAL_PUBLIC_HKO_HEADQUARTERS",
            "hn_total": cal["hko_hn_total"],
            "vhd_total": cal["hko_vhd_total"],
            "cd_total": cal["hko_cd_total"],
            "climatology_mean_t": hko_official_climatology,
            "note": "These are the live paper's Hong Kong flags. They are not Open-Meteo counts.",
        },
        "cities": summaries,
        "months": all_months,
        "distance_rank": [
            {"id": s["id"], "name": s["name"], "d": s["distance_to_hk_openmeteo"], "role": s["role"]}
            for s in rank
        ],
        "literature": LIT,
        "claim_boundaries": [
            "Do not transport Hong Kong CHD/HF count ratios to another city.",
            "Do not treat Open-Meteo HKO-flag counts as official HKO yearbook numbers.",
            "Published papers cited here are other estimands (usually daily mortality or ambulance CVD).",
            "Stroke was not delivered for this project; this atlas does not analyse stroke.",
            "Apparent-temperature flags are still ERA5 objects, not HKO yearbook numbers.",
        ],
    }
    OUT_DOCS.mkdir(parents=True, exist_ok=True)
    slim = {k: v for k, v in payload.items() if k != "months"}
    js = "window.PEER_ATLAS = " + json.dumps(slim, separators=(",", ":")) + ";\n"
    (OUT_DOCS / "peers_embed.js").write_text(js)
    (OUT_TAB / "peer_atlas.json").write_text(json.dumps(payload, indent=2) + "\n")
    write_climate_space_svg(summaries, OUT_FIG / "climate_space_2013_2023.svg")
    write_climate_space_svg(summaries, OUT_DOCS / "climate_space.svg")
    write_calibration_svg(cal, OUT_FIG / "hk_station_vs_era5.svg")
    write_calibration_svg(cal, OUT_DOCS / "hk_station_vs_era5.svg")
    print("calibration", json.dumps(cal))
    print("wrote", OUT_DOCS / "peers_embed.js")
    return 0


if __name__ == "__main__":
    sys.exit(main())
