#!/usr/bin/env python3
"""Demonstrate that public Hong Kong files cannot replace the governed HA extract.

This intern-owned search is evidence, not a new health finding. It does not
download Hospital Authority microdata. It records the grain of what a public
web search actually returns.

Run from the repository root:

    python3 scripts/52_public_outcome_ceiling_search.py
"""

from __future__ import annotations

import csv
import io
import json
import ssl
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "outputs" / "auto_research" / "public_outcome_ceiling_search.json"
OUT_MD = ROOT / "reports" / "public_data_ceiling_search_2026-08-18.md"
EXCERPT_DIR = ROOT / "outputs" / "auto_research" / "public_ceiling_excerpts"

UA = "LaidlawHeatProject-public-grain-check/2026-08-18 (research assistant; no HA microdata)"
TIMEOUT = 40
CTX = ssl.create_default_context()


def fetch(url: str, dest: Path | None = None) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    rec = {
        "url": url,
        "ok": False,
        "http_status": None,
        "bytes": 0,
        "error": None,
        "content_type": None,
    }
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=CTX) as resp:
            body = resp.read()
            rec["ok"] = True
            rec["http_status"] = getattr(resp, "status", 200)
            rec["bytes"] = len(body)
            rec["content_type"] = resp.headers.get("Content-Type")
            rec["final_url"] = resp.geturl()
            if dest is not None:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(body)
            rec["_body"] = body
            head = body[:400].decode("utf-8", "replace")
            rec["body_head"] = head
            if "<title>404 Not Found</title>" in head or "404 Not Found" in head[:200]:
                rec["ok"] = False
                rec["error"] = "HTTP 200 wrapping an HTML 404 page"
    except urllib.error.HTTPError as e:
        rec["http_status"] = e.code
        rec["error"] = f"HTTPError {e.code}"
        rec["bytes"] = len(e.read() or b"")
    except Exception as e:  # noqa: BLE001 — intern log must record timeouts too
        rec["error"] = f"{type(e).__name__}: {e}"
    return rec


def json_load(body: bytes):
    return json.loads(body.decode("utf-8-sig"))


def main() -> None:
    EXCERPT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    checks: list[dict] = []

    # --- 1. HA open-data throughput (financial year × hospital) ---
    ha = fetch("https://www.ha.org.hk/opendata/ipdpdd-en.json")
    ha_summary = {k: ha[k] for k in ha if k != "_body"}
    if ha.get("ok"):
        rows = json_load(ha["_body"])
        years = sorted({r.get("Financial Year") for r in rows})
        sample = rows[0]
        excerpt = EXCERPT_DIR / "ha_ipdpdd_en_head.json"
        excerpt.write_text(json.dumps(rows[:3], ensure_ascii=False, indent=2), encoding="utf-8")
        ha_summary.update(
            {
                "n_rows": len(rows),
                "keys": sorted(sample.keys()),
                "sample_row": sample,
                "financial_years": years,
                "n_financial_years": len(years),
                "has_month_field": any("month" in k.lower() for k in sample),
                "has_icd_field": any("icd" in k.lower() or "diagnos" in k.lower() for k in sample),
                "grain": "financial year × cluster × hospital; inpatient/day-patient discharges and deaths; no ICD; no month; not a T2D/HTN first-event series",
                "excerpt": str(excerpt.relative_to(ROOT)),
            }
        )
    checks.append({"id": "HA_IPDPDD_JSON", "needed_for": "monthly first-event CHD/HF among T2D/HTN", **ha_summary})

    ha_age = fetch("https://www.ha.org.hk/opendata/ipdpdd-age-gender-en.json")
    ha_age_s = {k: ha_age[k] for k in ha_age if k != "_body"}
    if ha_age.get("ok"):
        rows = json_load(ha_age["_body"])
        sample = rows[0]
        ha_age_s.update(
            {
                "n_rows": len(rows),
                "keys": sorted(sample.keys()),
                "sample_row": sample,
                "grain": "financial year × age group × gender; still no ICD, month, cohort, or first-event rule",
            }
        )
    checks.append({"id": "HA_IPDPDD_AGE_GENDER", **ha_age_s})

    # Guessed disease-group JSON names (document 404s).
    for guess in (
        "https://www.ha.org.hk/opendata/ipdpdd-disease-en.json",
        "https://www.ha.org.hk/opendata/ipdp-disease-en.json",
        "https://www.ha.org.hk/opendata/ipdpdd-diseasegroup-en.json",
    ):
        rec = fetch(guess)
        checks.append(
            {
                "id": "HA_DISEASE_GROUP_JSON_GUESS",
                "url": rec["url"],
                "ok": rec["ok"],
                "http_status": rec["http_status"],
                "error": rec["error"],
                "note": "DATA.GOV.HK inpatient-throughput dataset lists beds/discharges/ALOS, not this filename. HA Major Statistics names a disease-group table; no matching public JSON was found at these guessed paths.",
            }
        )

    # --- 2. DH annual inpatient-by-disease CSV ---
    dh_url = (
        "https://www.dh.gov.hk/datagovhk/ncdd/"
        + urllib.parse.quote("Inpatient Discharges and Deaths in All Hospitals Classified by Disease, 2023 (EN).csv")
    )
    dh = fetch(dh_url, dest=EXCERPT_DIR / "dh_2023_all_hospitals_by_disease.csv")
    dh_s = {k: dh[k] for k in dh if k != "_body"}
    if dh.get("ok"):
        text = dh["_body"].decode("utf-8-sig")
        reader = csv.reader(io.StringIO(text))
        rows = list(reader)
        circulatory = [r for r in rows if r and r[0].startswith("I00")]
        notes = [r for r in rows if r and r[0].lower().startswith("notes")]
        dh_s.update(
            {
                "n_csv_rows": len(rows),
                "header_block": rows[:4],
                "circulatory_row": circulatory[0] if circulatory else None,
                "notes_row": notes[0] if notes else None,
                "has_month_column": any("month" in ",".join(r).lower() for r in rows[:6]),
                "grain": "one calendar year; ICD-10 chapter totals; episode basis including day inpatients; all hospitals; not first hospitalisation after first CHD/HF diagnosis; not restricted to T2D/HTN",
            }
        )
    checks.append({"id": "DH_2023_INPATIENT_BY_DISEASE", **dh_s})

    # --- 3. CKAN: is there any public monthly hospitalisation series? ---
    ckan_q = "https://data.gov.hk/en-data/api/3/action/package_search?q={}&rows=20".format(
        urllib.parse.quote("inpatient OR hospitalisation OR hospitalization")
    )
    ckan = fetch(ckan_q)
    ckan_s = {k: ckan[k] for k in ckan if k != "_body"}
    if ckan.get("ok"):
        payload = json_load(ckan["_body"])
        result = payload.get("result") or {}
        titles = []
        for pkg in result.get("results") or []:
            extras = {e.get("key"): e.get("value") for e in pkg.get("extras") or []}
            titles.append(
                {
                    "title": pkg.get("title"),
                    "name": pkg.get("name"),
                    "org": (pkg.get("organization") or {}).get("name"),
                    "update_frequency": extras.get("update_frequency") or extras.get("frequency"),
                }
            )
        ckan_s.update(
            {
                "ckan_success": payload.get("success"),
                "count": result.get("count"),
                "packages": titles,
                "grain": "CKAN returned C&SD Table 930-92087 (HA inpatient services, quarterly throughput), not monthly ICD first-events in a chronic-disease cohort",
            }
        )
    checks.append({"id": "CKAN_INPATIENT_SEARCH", **ckan_s})

    ckan2 = fetch(
        "https://data.gov.hk/en-data/api/3/action/package_search?q={}&rows=10".format(
            urllib.parse.quote("disease group hospital authority")
        )
    )
    ckan2_s = {k: ckan2[k] for k in ckan2 if k != "_body"}
    if ckan2.get("ok"):
        payload = json_load(ckan2["_body"])
        ckan2_s["count"] = (payload.get("result") or {}).get("count")
        ckan2_s["titles"] = [
            p.get("title") for p in (payload.get("result") or {}).get("results") or []
        ]
    checks.append({"id": "CKAN_DISEASE_GROUP_SEARCH", **ckan2_s})

    # --- 4. HKO daily temperature (this intern CAN fetch; lock is endorsement) ---
    hko = fetch(
        "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php"
        "?dataType=CLMTEMP&rformat=csv&station=HKO&year=2013",
        dest=EXCERPT_DIR / "hko_2013_daily_mean_temp.csv",
    )
    hko_s = {k: hko[k] for k in hko if k != "_body"}
    if hko.get("ok"):
        text = hko["_body"].decode("utf-8-sig")
        lines = [ln for ln in text.splitlines() if ln and ln[0].isdigit()]
        hko_s.update(
            {
                "n_daily_rows": len(lines),
                "first_data_line": lines[0] if lines else None,
                "last_data_line": lines[-1] if lines else None,
                "grain": "public daily mean temperature at HKO Headquarters; intern-accessible; does not supply outcomes or Hogan's encoding lock",
            }
        )
    checks.append({"id": "HKO_DAILY_MEAN_2013", **hko_s})

    hko_bad = fetch(
        "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php"
        "?dataType=HHOT&rformat=csv&station=HKO&year=2013&month=8"
    )
    checks.append(
        {
            "id": "HKO_HOURLY_TEMP_WRONG_DATATYPE",
            "url": hko_bad["url"],
            "ok": hko_bad["ok"],
            "http_status": hko_bad["http_status"],
            "snippet": (hko_bad.get("_body") or b"")[:240].decode("utf-8", "replace"),
            "note": "HHOT is hourly astronomical tides in the HKO Open Data API, not hourly air temperature. A 2013–2023 hourly temperature archive was not found on this endpoint.",
        }
    )

    # --- 5. HA research-request pages (PI path, not intern path) ---
    for cid, url in (
        ("HA_PROVISION_INDEX", "https://www3.ha.org.hk/data/Provision/Index/"),
        ("HA_APPLICATION_PROCEDURE", "https://www3.ha.org.hk/data/Provision/ApplicationProcedure"),
        ("HA_SUBMISSION", "https://www3.ha.org.hk/data/Provision/Submission"),
        ("HA_FORM_A_GN", "https://www3.ha.org.hk/Data/Home/File?path=%2FProvision+of+HA+data+for+Research%2FDRAF%28A%29_GN.pdf"),
        ("HA_STANDARD_PROCEDURES", "https://www3.ha.org.hk/Data/Home/File?path=%2FProvision+of+HA+data+for+Research%2FSP.pdf"),
        ("HA_UNDERTAKING", "https://www3.ha.org.hk/Data/Home/File?path=%2FProvision+of+HA+data+for+Research%2FUF.pdf"),
        ("EHPDCL_ACCESS", "https://ehpdigital.com/data-service/accessingdcl/"),
        ("HKU_EHPDCL", "https://www.med.hku.hk/en/research/facilities-and-services/hku-ehpdcl"),
        ("CHP_HEART_DISEASES", "https://www.chp.gov.hk/en/healthtopics/content/25/57.html"),
        ("CHP_CEREBROVASCULAR", "https://www.chp.gov.hk/en/healthtopics/content/25/58.html"),
        ("HA_MAJOR_STATISTICS", "https://www3.ha.org.hk/Data/HAStatistics/MajorReport"),
    ):
        rec = fetch(url)
        checks.append(
            {
                "id": cid,
                "url": rec["url"],
                "ok": rec["ok"],
                "http_status": rec["http_status"],
                "bytes": rec["bytes"],
                "error": rec["error"],
                "content_type": rec.get("content_type"),
            }
        )

    verdict = {
        "question": "Can a lab intern replace the governed monthly CHD/HF first-hospitalisation series among people with T2D and/or HTN using only public Hong Kong files?",
        "answer": "No. Public files are annual or financial-year episode throughput, survey prevalence, or weather. They are not a 132-month first-event series in the T2D/HTN cohort, they do not carry admission cause, and they do not supply still-at-risk person-time.",
        "what_intern_can_fetch": [
            "HKO daily temperature (demonstrated for 2013)",
            "HA financial-year discharges and beds by hospital/cluster/age-sex",
            "DH annual ICD-chapter episode discharges",
            "CHP annual heart-disease episode discharges and registered deaths",
            "C&SD half-yearly/annual population by age-sex",
            "CHP Health Behaviour Survey 2023 point prevalence (HTN 21.3%, DM 9.2% among persons aged 15+)",
        ],
        "what_requires_a_PI": [
            "HA Central Panel Form A (expedited aggregates; typically HK$15,000+) or Form B (customised/patient-based; typically HK$60,000+)",
            "EHPDCL DARE/EXPERT named-user access under an institutional agreement, ethics, and fees",
            "A further governed extract from the existing collaboration (stroke file, ICD list, inpatient vs DAE, person-time, age bands)",
        ],
    }

    payload = {
        "fetched_at_utc": fetched_at,
        "script": "scripts/52_public_outcome_ceiling_search.py",
        "provenance": "PUBLIC_WEB_FETCH — not HA microdata; not a health finding",
        "verdict": verdict,
        "checks": [{k: v for k, v in c.items() if k != "_body"} for c in checks],
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(payload)
    print(f"Wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")


def write_markdown(payload: dict) -> None:
    lines = [
        "# Public-file ceiling search — 18 August 2026",
        "",
        f"**Fetched (UTC):** {payload['fetched_at_utc']}  ",
        "**Script:** `scripts/52_public_outcome_ceiling_search.py`  ",
        "**Provenance:** `PUBLIC_WEB_FETCH`. Not Hospital Authority microdata. Not a coefficient.",
        "",
        "## Verdict",
        "",
        payload["verdict"]["question"],
        "",
        payload["verdict"]["answer"],
        "",
        "## What each fetch actually contained",
        "",
        "| ID | HTTP | Bytes | Grain / note |",
        "|---|---:|---:|---|",
    ]
    for c in payload["checks"]:
        note = c.get("grain") or c.get("note") or c.get("error") or c.get("snippet") or ""
        note = " ".join(str(note).split())
        if len(note) > 220:
            note = note[:217] + "..."
        lines.append(
            f"| `{c['id']}` | {c.get('http_status')} | {c.get('bytes', '')} | {note} |"
        )
    lines.extend(
        [
            "",
            "## HA throughput sample (first row of `ipdpdd-en.json`)",
            "",
        ]
    )
    ha = next(c for c in payload["checks"] if c["id"] == "HA_IPDPDD_JSON")
    if ha.get("sample_row"):
        lines.append("```json")
        lines.append(json.dumps(ha["sample_row"], ensure_ascii=False, indent=2))
        lines.append("```")
        lines.append("")
        lines.append(
            f"Rows: {ha.get('n_rows')}. Financial years: {ha.get('financial_years')}. "
            f"Month field: {ha.get('has_month_field')}. ICD field: {ha.get('has_icd_field')}."
        )
    dh = next(c for c in payload["checks"] if c["id"] == "DH_2023_INPATIENT_BY_DISEASE")
    lines.extend(["", "## DH 2023 circulatory chapter row", ""])
    if dh.get("circulatory_row"):
        lines.append("`" + " | ".join(dh["circulatory_row"]) + "`")
        lines.append("")
        lines.append(str(dh.get("grain")))
    hko = next(c for c in payload["checks"] if c["id"] == "HKO_DAILY_MEAN_2013")
    lines.extend(
        [
            "",
            "## HKO daily mean temperature, 2013 (public; intern can fetch)",
            "",
            f"Daily rows: {hko.get('n_daily_rows')}. First: `{hko.get('first_data_line')}`. Last: `{hko.get('last_data_line')}`.",
            "",
            "This is the opposite of the outcome ceiling. Weather is public. Hogan's remaining job is to lock how monthly tails are defined, not to unlock the CSV.",
            "",
            "## Machine JSON",
            "",
            "`outputs/auto_research/public_outcome_ceiling_search.json`",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
