#!/usr/bin/env python3
"""SYNTHETIC utilisation-shock Monte Carlo for the COVID-period lab.

Playbook 08. Not a Hong Kong finding. Does not open governed panels.

Question: can a constant cold-day coefficient look attenuated in a full-window
fit if an unobserved utilisation multiplier hits 2020 onward?

Answer this script is allowed to give: yes, on SYNTHETIC data. It does not
estimate beta on the HA panel.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "health_econ" / "synthetic_utilisation_shock_2026-09-10.json"
RNG = np.random.default_rng(20260910)

N_MONTHS = 132
PRE = 84  # Jan 2013–Dec 2019
TRUE_BETA = np.log(1.10)  # count ratio 1.10 per five synthetic cold days
N_REPS = 200


def _design() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    month = np.arange(N_MONTHS) % 12
    cold = np.zeros(N_MONTHS)
    for t in range(N_MONTHS):
        m = t % 12
        lam = 3.0 if m in (11, 0, 1) else 0.4
        cold[t] = RNG.poisson(lam)
    x = cold / 5.0
    days = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] * 11)
    return x, days.astype(float), month


def _mu(x: np.ndarray, days: np.ndarray, month: np.ndarray, u: np.ndarray) -> np.ndarray:
    # intercept chosen so mean counts are hospital-like in scale, not HA truth
    seasonal = 0.15 * np.sin(2 * np.pi * month / 12.0)
    eta = np.log(days) - 0.2 + TRUE_BETA * x + seasonal + np.log(u)
    return np.exp(eta)


def _poisson_glm_beta(y: np.ndarray, x: np.ndarray, days: np.ndarray) -> float:
    """One-parameter Poisson GLM for beta via IRLS on offset+intercept+x (no month FE).

    Intentionally simpler than Model 1. SYNTHETIC demonstration only.
    """
    offset = np.log(days)
    n = y.size
    z = np.column_stack([np.ones(n), x])
    beta = np.zeros(2)
    for _ in range(25):
        eta = offset + z @ beta
        mu = np.exp(np.clip(eta, -20, 20))
        w = mu
        z_adj = eta - offset + (y - mu) / np.maximum(mu, 1e-8)
        # weighted least squares
        sw = np.sqrt(w)[:, None]
        try:
            beta = np.linalg.lstsq(sw * z, sw[:, 0] * z_adj, rcond=None)[0]
        except np.linalg.LinAlgError:
            return float("nan")
    return float(beta[1])


def main() -> None:
    x, days, month = _design()
    u = np.ones(N_MONTHS)
    u[PRE:] = 0.55  # utilisation drop after 2019
    pre_betas = []
    full_betas = []
    for _ in range(N_REPS):
        mu = _mu(x, days, month, u)
        y = RNG.poisson(mu)
        pre_betas.append(_poisson_glm_beta(y[:PRE], x[:PRE], days[:PRE]))
        full_betas.append(_poisson_glm_beta(y, x, days))
    pre = np.exp(np.array(pre_betas))
    full = np.exp(np.array(full_betas))
    payload = {
        "data_status": "SYNTHETIC",
        "n_reps": N_REPS,
        "true_count_ratio": float(np.exp(TRUE_BETA)),
        "utilisation_multiplier_from_2020": 0.55,
        "mean_pre_window_cr": float(np.nanmean(pre)),
        "mean_full_window_cr": float(np.nanmean(full)),
        "median_pre_minus_full": float(np.nanmedian(pre - full)),
        "note": (
            "SYNTHETIC. Constant true beta; utilisation shock after month 84. "
            "Not HA. Not a physiology result. Playbook 08."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
