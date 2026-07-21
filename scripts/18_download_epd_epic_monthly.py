#!/usr/bin/env python3
"""Download official EPD EPIC monthly air-quality CSVs for Hong Kong.

Pollutants (literature / config): NO2, O3, PM2.5 (FSP), PM10 (RSP).
Primary extract: general stations. Optional roadside extract.

EPIC portal: https://cd.epic.epd.gov.hk/EPICDI/air/yearly/
Monthly requests are limited to 120 months; this script chunks the study window.

Usage (from repo root):
  python3 scripts/18_download_epd_epic_monthly.py
  python3 scripts/18_download_epd_epic_monthly.py --include-roadside
"""

from __future__ import annotations

import argparse
import csv
import re
import time
import uuid
import http.cookiejar
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://cd.epic.epd.gov.hk"
PAGE = f"{BASE}/EPICDI/air/yearly/?lang=en"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data_raw" / "epd"

# Form indices observed on EPIC yearly download page (2026-07).
POLLUTANTS = {
    "PM25": 1,  # Fine Suspended Particulates
    "NO2": 2,  # Nitrogen Dioxide
    "O3": 4,  # Ozone
    "PM10": 5,  # Respirable Suspended Particulates
}
N_GENERAL = 15  # j_id_4w:0..14
N_ROADSIDE = 3  # j_id_59:0..2


def make_opener() -> urllib.request.OpenerDirector:
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [
        (
            "User-Agent",
            "Mozilla/5.0 (compatible; LaidlawHeatProject/1.0; research download)",
        )
    ]
    return opener


def get_viewstate(html: str) -> str:
    m = re.search(r'name="jakarta\.faces\.ViewState"[^>]*value="([^"]+)"', html)
    if not m:
        raise RuntimeError("Could not find jakarta.faces.ViewState on EPIC page")
    return m.group(1)


def month_chunks(start_y: int, start_m: int, end_y: int, end_m: int, max_months: int = 60):
    """Yield (fy, fm, ty, tm) inclusive chunks of at most max_months."""
    y, m = start_y, start_m
    while (y, m) <= (end_y, end_m):
        fy, fm = y, m
        # advance max_months-1 months
        total = (y * 12 + (m - 1)) + (max_months - 1)
        ty, tm = divmod(total, 12)
        tm += 1
        if (ty, tm) > (end_y, end_m):
            ty, tm = end_y, end_m
        yield fy, fm, ty, tm
        # next month after ty/tm
        if tm == 12:
            y, m = ty + 1, 1
        else:
            y, m = ty, tm + 1


def download_chunk(
    opener: urllib.request.OpenerDirector,
    *,
    from_year: int,
    from_month: int,
    to_year: int,
    to_month: int,
    general: bool = True,
    roadside: bool = False,
    retries: int = 3,
) -> bytes:
    html = opener.open(PAGE, timeout=60).read().decode("utf-8", "replace")
    vs = get_viewstate(html)
    token = str(uuid.uuid4())

    fields: list[tuple[str, str]] = [("requestType", "download")]
    for idx in POLLUTANTS.values():
        fields.append((f"j_id_4a:{idx}:parameters", "true"))
    if general:
        for i in range(N_GENERAL):
            fields.append((f"j_id_4w:{i}:stations", "true"))
    if roadside:
        for i in range(N_ROADSIDE):
            fields.append((f"j_id_59:{i}:stations", "true"))
    fields += [
        ("timerange", "monthly"),
        ("monthlyFromYear", str(from_year)),
        ("monthlyFromMonth", str(from_month)),
        ("monthlyToYear", str(to_year)),
        ("monthlyToMonth", str(to_month)),
        ("downloadToken", token),
        ("form_SUBMIT", "1"),
        ("jakarta.faces.ViewState", vs),
        ("form:_idcl", "excel"),  # Download CSV (By Parameter)
    ]
    data = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(
        PAGE,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": PAGE,
            "Origin": BASE,
        },
    )
    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            resp = opener.open(req, timeout=180)
            body = resp.read()
            ctype = (resp.headers.get("Content-Type") or "").lower()
            if b"YEAR,POLLUTANT,STATION" not in body[:500] and "octet-stream" not in ctype:
                raise RuntimeError(
                    f"Unexpected response (ctype={ctype!r}, head={body[:120]!r})"
                )
            return body
        except Exception as e:
            last_err = e
            time.sleep(2 * attempt)
    raise RuntimeError(f"Download failed after {retries} tries: {last_err}")


def write_bytes(path: Path, body: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(body)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start-year", type=int, default=2013)
    ap.add_argument("--start-month", type=int, default=1)
    ap.add_argument("--end-year", type=int, default=2023)
    ap.add_argument("--end-month", type=int, default=12)
    ap.add_argument("--include-roadside", action="store_true")
    ap.add_argument("--chunk-months", type=int, default=60)
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    opener = make_opener()
    written: list[str] = []

    for fy, fm, ty, tm in month_chunks(
        args.start_year, args.start_month, args.end_year, args.end_month, args.chunk_months
    ):
        label = f"{fy}{fm:02d}_{ty}{tm:02d}"
        path = OUT_DIR / f"epd_general_monthly_{label}.csv"
        print(f"Downloading general monthly {fy}-{fm:02d} .. {ty}-{tm:02d} -> {path.name}")
        body = download_chunk(
            opener, from_year=fy, from_month=fm, to_year=ty, to_month=tm, general=True, roadside=False
        )
        write_bytes(path, body)
        written.append(path.name)
        time.sleep(1.5)

    if args.include_roadside:
        for fy, fm, ty, tm in month_chunks(
            args.start_year, args.start_month, args.end_year, args.end_month, args.chunk_months
        ):
            label = f"{fy}{fm:02d}_{ty}{tm:02d}"
            path = OUT_DIR / f"epd_roadside_monthly_{label}.csv"
            print(f"Downloading roadside monthly {fy}-{fm:02d} .. {ty}-{tm:02d} -> {path.name}")
            body = download_chunk(
                opener,
                from_year=fy,
                from_month=fm,
                to_year=ty,
                to_month=tm,
                general=False,
                roadside=True,
            )
            write_bytes(path, body)
            written.append(path.name)
            time.sleep(1.5)

    # Manifest
    manifest = OUT_DIR / "download_manifest.txt"
    manifest.write_text(
        "\n".join(
            [
                "source: EPD EPIC Air Quality Data Download (monthly average)",
                f"portal: {PAGE}",
                "pollutants: NO2, O3, PM2.5 (FSP), PM10 (RSP)",
                "station_set_primary: general (15 stations)",
                f"window: {args.start_year}-{args.start_month:02d} .. {args.end_year}-{args.end_month:02d}",
                f"files: {'; '.join(written)}",
                "units: ug/m3 (per EPIC CSV remarks)",
                "note: Official validated monthly averages from EPIC; replace placeholders.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(written)} files. Manifest: {manifest}")


if __name__ == "__main__":
    main()
