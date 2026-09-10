#!/usr/bin/env python3
"""SYNTHETIC influenza-collapse Monte Carlo for the COVID-period lab.

Playbook 08. Next legal mutation after utilisation shock and MNAR. Not a
Hong Kong finding. Does not open governed panels.

Question: can a constant cold-day coefficient look attenuated in a full-window
fit if an influenza-like winter term collapses after month 84, with or without
the utilisation drop already shown in script 72?

Answer this script is allowed to give: yes, on SYNTHETIC data. It does not
estimate beta on the HA panel.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from importlib.machinery import SourceFileLoader

ROOT = Path(__file__).resolve().parents[1]
HELPER = SourceFileLoader(
    "shock72", str(ROOT / "scripts" / "72_synthetic_utilisation_shock.py")
).load_module()
OUT = ROOT / "outputs" / "health_econ" / "synthetic_flu_collapse_2026-09-10.json"
RNG = np.random.default_rng(20260912)

N_REPS = 200
PRE = HELPER.PRE
N_MONTHS = HELPER.N_MONTHS
TRUE_BETA = HELPER.TRUE_BETA
FLU_COEF = np.log(1.08)  # winter influenza-like multiplier on counts


def _flu_term() -> np.ndarray:
    """Winter-peaked co-circulation that collapses after month 84."""
    flu = np.zeros(N_MONTHS)
    for t in range(N_MONTHS):
        m = t % 12
        winter = 1.0 if m in (11, 0, 1) else 0.15
        flu[t] = winter if t < PRE else 0.05 * winter
    return flu


def _mu_flu(
    x: np.ndarray,
    days: np.ndarray,
    month: np.ndarray,
    u: np.ndarray,
    flu: np.ndarray,
) -> np.ndarray:
    seasonal = 0.15 * np.sin(2 * np.pi * month / 12.0)
    eta = np.log(days) - 0.2 + TRUE_BETA * x + seasonal + np.log(u) + FLU_COEF * flu
    return np.exp(eta)


def _scenario_crs(
    x: np.ndarray,
    days: np.ndarray,
    month: np.ndarray,
    u: np.ndarray,
    flu: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    pre_betas = []
    full_betas = []
    for _ in range(N_REPS):
        mu = _mu_flu(x, days, month, u, flu)
        y = RNG.poisson(mu)
        pre_betas.append(HELPER._poisson_glm_beta(y[:PRE], x[:PRE], days[:PRE]))
        full_betas.append(HELPER._poisson_glm_beta(y, x, days))
    pre = np.exp(np.array(pre_betas))
    full = np.exp(np.array(full_betas))
    return pre, full


def _pack(pre: np.ndarray, full: np.ndarray) -> dict:
    return {
        "mean_pre_window_cr": float(np.nanmean(pre)),
        "mean_full_window_cr": float(np.nanmean(full)),
        "median_pre_minus_full": float(np.nanmedian(pre - full)),
    }


def main() -> None:
    x, days, month = HELPER._design()
    flu = _flu_term()
    u_one = np.ones(N_MONTHS)
    u_drop = np.ones(N_MONTHS)
    u_drop[PRE:] = 0.55

    flu_only_pre, flu_only_full = _scenario_crs(x, days, month, u_one, flu)
    both_pre, both_full = _scenario_crs(x, days, month, u_drop, flu)
    util_pre, util_full = _scenario_crs(x, days, month, u_drop, np.zeros(N_MONTHS))

    payload = {
        "data_status": "SYNTHETIC",
        "n_reps": N_REPS,
        "true_count_ratio": float(np.exp(TRUE_BETA)),
        "flu_coef_count_ratio": float(np.exp(FLU_COEF)),
        "utilisation_multiplier_from_2020": 0.55,
        "scenarios": {
            "flu_collapse_only": _pack(flu_only_pre, flu_only_full),
            "utilisation_only": _pack(util_pre, util_full),
            "flu_plus_utilisation": _pack(both_pre, both_full),
        },
        "note": (
            "SYNTHETIC. Constant true beta; influenza-like term collapses after "
            "month 84. Optional utilisation multiplier 0.55 from month 85. "
            "Not HA. Not a physiology result. Playbook 08. Do not quote as a "
            "Hong Kong count ratio."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
