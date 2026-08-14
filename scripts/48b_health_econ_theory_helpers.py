#!/usr/bin/env python3
"""SYNTHETIC_THEORY helpers for the health-economics laboratory.

Does not read HA health files. Does not invent findings or currency results.
"""
from __future__ import annotations

import csv
import json
import math
import os
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "health_econ"
OUT.mkdir(parents=True, exist_ok=True)
DOCS = ROOT / "docs" / "health_econ"
DOCS.mkdir(parents=True, exist_ok=True)

PROVENANCE = "SYNTHETIC_THEORY"
SEED = 20260814


def load_daily():
    path = ROOT / "data_processed" / "md_daily_weather_design_2013_2023.csv"
    rows = []
    with path.open() as f:
        for rec in csv.DictReader(f):
            rows.append(
                {
                    "month_id": rec["month_id"],
                    "tmean": float(rec["tmean"]),
                    "cold_day": int(float(rec["cold_day"])),
                    "hot_night": int(float(rec["hot_night"])),
                    "month": int(rec["month"]),
                    "year": int(rec["year"]),
                }
            )
    return rows


def variance_gradient(daily):
    """REAL_PUBLIC_HKO: within-month tmean variance vs monthly mean."""
    buckets = defaultdict(list)
    for r in daily:
        buckets[r["month_id"]].append(r["tmean"])
    months = []
    for mid, vals in sorted(buckets.items()):
        n = len(vals)
        mean = sum(vals) / n
        var = sum((v - mean) ** 2 for v in vals) / max(n - 1, 1)
        months.append({"month_id": mid, "tbar": mean, "s2": var, "n": n})
    # OLS: s2 = a + b * tbar
    n = len(months)
    mx = sum(m["tbar"] for m in months) / n
    my = sum(m["s2"] for m in months) / n
    sxx = sum((m["tbar"] - mx) ** 2 for m in months)
    sxy = sum((m["tbar"] - mx) * (m["s2"] - my) for m in months)
    b = sxy / sxx if sxx else float("nan")
    a = my - b * mx
    resid = [(m["s2"] - (a + b * m["tbar"])) for m in months]
    sse = sum(r ** 2 for r in resid)
    sst = sum((m["s2"] - my) ** 2 for m in months)
    r2 = 1 - sse / sst if sst else float("nan")
    return {
        "data_status": "REAL_PUBLIC_HKO",
        "quantity": "varsigma = ds2/dTbar from monthly OLS on daily HKO tmean",
        "n_months": n,
        "intercept": a,
        "varsigma": b,
        "r2": r2,
        "mean_s2": my,
        "mean_tbar": mx,
        "note": "Climate statistic only. Not a health finding. Sign expected negative in a subtropical year.",
        "months": months,
    }


def evpi_tree():
    """HE-04 SYNTHETIC decision tree. All utilities are dimensionless."""
    # theta_S ~ N(0, 0.05^2); signal ~ N(theta, 0.03^2)
    # actions: proceed (a=0) or wait (a=1)
    # U = -1{a != a*} - 0.10 1{wait} + 0.15 1{person-time licenses IRR}
    draws = 8000
    # Box-Muller
    import random

    rng = random.Random(SEED)
    wait_cost = 0.10
    irr_bonus = 0.15
    threshold = math.log(1.05)

    def sample_norm(mu, sd):
        u1 = rng.random() or 1e-12
        u2 = rng.random()
        z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2 * math.pi * u2)
        return mu + sd * z

    def a_star(th):
        return 1 if abs(th) >= threshold else 0

    def u(a, th, has_irr):
        return (
            -float(a != a_star(th))
            - wait_cost * a
            + irr_bonus * float(has_irr)
        )

    # Prior EVPI for stroke-like theta_S (wait vs proceed), no IRR
    us_proceed = []
    us_wait = []
    us_perfect = []
    for _ in range(draws):
        th = sample_norm(0.0, 0.05)
        us_proceed.append(u(0, th, False))
        us_wait.append(u(1, th, False))
        us_perfect.append(max(u(0, th, False), u(1, th, False)))
    ev_proceed = sum(us_proceed) / draws
    ev_wait = sum(us_wait) / draws
    ev_best = max(ev_proceed, ev_wait)
    evpi_stroke = sum(us_perfect) / draws - ev_best

    # Person-time: claim-set bonus even if posterior unchanged
    us_pt = [u(0, sample_norm(0.0, 0.05), True) for _ in range(draws)]
    # reuse independent draws already consumed; recompute cleanly
    rng = random.Random(SEED + 1)
    gap_claim = []
    for _ in range(draws):
        th = sample_norm(0.0, 0.05)
        gap_claim.append(u(0, th, True) - u(0, th, False))
    claim_set_value = sum(gap_claim) / draws  # = irr_bonus by construction

    return {
        "data_status": PROVENANCE,
        "hypothesis": "HE-04",
        "verdict_parent": "KILL",
        "note": "Utilities are dimensionless SYNTHETIC knobs, not currency. EVPI is prior-dependent by construction.",
        "knobs": {
            "wait_cost": wait_cost,
            "irr_claim_bonus": irr_bonus,
            "threshold_abs_logRR": threshold,
            "prior_sd": 0.05,
            "draws": draws,
        },
        "EV_proceed": ev_proceed,
        "EV_wait": ev_wait,
        "chosen_without_info": "proceed" if ev_proceed >= ev_wait else "wait",
        "EVPI_stroke_file": evpi_stroke,
        "claim_set_value_person_time": claim_set_value,
        "interpretation": (
            "Under Option A (no confirmatory primary) the stroke-file EVPI is the value of "
            "changing wait/proceed, which is small when the prior is centred at zero. "
            "Person-time value is almost entirely the IRR claim-set bonus, independent of the posterior."
        ),
    }


def preference_reversal():
    """HE-C2-04: prior-free reversal over payoff orderings. Not an estimate."""
    # Actions: proceed now (P) vs wait (W). Payoffs (now, later).
    # Naive hyperbolic: U = now + beta * later. Exponential planner: now + later
    # (delta absorbed into 'later' units).
    orderings = [
        {"id": "wait_backloaded", "P": (1.0, 0.2), "W": (0.1, 1.2)},
        {"id": "proceed_frontloaded", "P": (1.2, 0.3), "W": (0.2, 0.8)},
        {"id": "wait_dominates", "P": (0.4, 0.4), "W": (0.5, 0.9)},
        {"id": "proceed_dominates", "P": (0.9, 0.9), "W": (0.2, 0.3)},
        {"id": "incomparable_equal", "P": (0.6, 0.6), "W": (0.6, 0.6)},
    ]
    betas = [1.0, 0.8, 0.6, 0.4]
    rows = []
    nonempty = False
    for o in orderings:
        row = {"ordering": o["id"], "P": o["P"], "W": o["W"], "choices": {}}
        planner = "P" if sum(o["P"]) > sum(o["W"]) else ("W" if sum(o["W"]) > sum(o["P"]) else "tie")
        row["exponential_planner"] = planner
        for b in betas:
            uP = o["P"][0] + b * o["P"][1]
            uW = o["W"][0] + b * o["W"][1]
            choice = "P" if uP > uW else ("W" if uW > uP else "tie")
            row["choices"][str(b)] = choice
            if b < 1 and planner not in ("tie", choice) and choice != "tie":
                nonempty = True
                row["reversal_at_beta"] = b
        rows.append(row)

    devices = [
        {
            "device": "Gate 3 written Option A recommendation",
            "written_before_information": True,
            "third_party_observable": True,
            "costly_to_revoke": "human_owned_unknown",
            "commitment": "incomplete",
        },
        {
            "device": "SAP / Playbook 03 pre-specification",
            "written_before_information": True,
            "third_party_observable": True,
            "costly_to_revoke": "human_owned_unknown",
            "commitment": "incomplete",
        },
        {
            "device": "Stage 3 PDF byte-lock",
            "written_before_information": True,
            "third_party_observable": True,
            "costly_to_revoke": "repository_enforced",
            "commitment": "programme_surface_only",
        },
        {
            "device": "this Explore cycle itself",
            "written_before_information": False,
            "third_party_observable": True,
            "costly_to_revoke": False,
            "commitment": "cheap_talk",
        },
    ]
    return {
        "data_status": PROVENANCE,
        "hypothesis": "HE-C2-04",
        "reversal_set_nonempty_under_enumerated_orderings": nonempty,
        "orderings": rows,
        "revocability_audit": devices,
        "note": "No EVPI number. No currency. Gate 3 is not moved.",
    }


def portfolio_matrix():
    """HE-C2-PORT identification-status ledger. Does not assert data exist."""
    params = [
        "lambda_bed_shadow",
        "Delta_adaptation_capital_wedge",
        "theta_h_household_capital",
        "varsigma_cluster_variance_gradient",
        "sigma_public_share",
    ]
    elements = [
        "cluster_monthly_counts",
        "bedday_capacity_occupancy",
        "elective_cancellations",
        "cluster_capital_recurrent_budgets",
        "catchment_housing_mix",
        "private_inpatient_volumes",
    ]
    # Analyst judgement: none of these is asserted to exist.
    # Cells: 0 = still unidentified, 1 = identified under strong assumptions.
    cells = {
        "lambda_bed_shadow": {
            "cluster_monthly_counts": 0,
            "bedday_capacity_occupancy": 0,
            "elective_cancellations": 0,
            "cluster_capital_recurrent_budgets": 0,
            "catchment_housing_mix": 0,
            "private_inpatient_volumes": 0,
            "full_bundle": 0,
            "note": "Capacity remains endogenous to anticipated weather even at cluster grain.",
        },
        "Delta_adaptation_capital_wedge": {
            "cluster_monthly_counts": 0,
            "bedday_capacity_occupancy": 0,
            "elective_cancellations": 0,
            "cluster_capital_recurrent_budgets": 0,
            "catchment_housing_mix": 0,
            "private_inpatient_volumes": 0,
            "full_bundle": 1,
            "note": "Counts + budgets + capital vintage together; no singleton flips the row.",
        },
        "theta_h_household_capital": {
            "cluster_monthly_counts": 0,
            "bedday_capacity_occupancy": 0,
            "elective_cancellations": 0,
            "cluster_capital_recurrent_budgets": 0,
            "catchment_housing_mix": 0,
            "private_inpatient_volumes": 0,
            "full_bundle": 1,
            "note": "Counts + housing mix; still a strong between-cluster assumption.",
        },
        "varsigma_cluster_variance_gradient": {
            "cluster_monthly_counts": 0,
            "bedday_capacity_occupancy": 0,
            "elective_cancellations": 0,
            "cluster_capital_recurrent_budgets": 0,
            "catchment_housing_mix": 0,
            "private_inpatient_volumes": 0,
            "full_bundle": 0,
            "note": "varsigma is already computable from public HKO at territory grain; cluster weather would help, not HA counts.",
        },
        "sigma_public_share": {
            "cluster_monthly_counts": 0,
            "bedday_capacity_occupancy": 0,
            "elective_cancellations": 0,
            "cluster_capital_recurrent_budgets": 0,
            "catchment_housing_mix": 0,
            "private_inpatient_volumes": 0,
            "full_bundle": 1,
            "note": "Private volumes are the singleton that would flip this row IF they exist monthly and are comparable — unverified.",
        },
    }
    # Private volumes actually would flip sigma alone — record that honestly.
    cells["sigma_public_share"]["private_inpatient_volumes"] = 1
    singleton_flips = []
    for p, row in cells.items():
        for e in elements:
            if row.get(e) == 1:
                singleton_flips.append({"parameter": p, "element": e})
    return {
        "data_status": PROVENANCE,
        "hypothesis": "HE-C2-PORT",
        "asserts_data_exist": False,
        "parameters": params,
        "elements": elements,
        "cells": cells,
        "singleton_flips": singleton_flips,
        "supermodularity": (
            "Most rows flip only as a bundle. sigma_public_share is the exception: "
            "comparable monthly private volumes would flip it alone. lambda remains "
            "unflipped even under the full bundle."
        ),
        "governance_unit": "integer_human_asks_not_currency",
        "smallest_useful_bundle": [
            "cluster_monthly_counts",
            "cluster_capital_recurrent_budgets",
            "catchment_housing_mix",
        ],
        "human_decision": "Whether to ask is owned by Roro/Bishai/governance. This matrix does not ask.",
    }


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2))
    print("wrote", path)


def main():
    daily = load_daily()
    vargrad = variance_gradient(daily)
    # Store months separately (large)
    months = vargrad.pop("months")
    write_json(OUT / "varsigma_hko.json", vargrad)
    write_json(OUT / "he04_evpi_synthetic.json", evpi_tree())
    write_json(OUT / "he_c2_04_reversal.json", preference_reversal())
    write_json(OUT / "he_c2_port_matrix.json", portfolio_matrix())
    write_json(OUT / "varsigma_hko_months.csv.json", {"data_status": "REAL_PUBLIC_HKO", "months": months})
    print("varsigma", round(vargrad["varsigma"], 4), "r2", round(vargrad["r2"], 3))


if __name__ == "__main__":
    main()
