#!/usr/bin/env python3
"""SYNTHETIC MNAR + selected-sample escalation of the utilisation-shock DGP.

Playbook 08 night-shift mutation. Not a Hong Kong finding. DUA: no HA panels.

Parent cycle: scripts/72_synthetic_utilisation_shock.py (constant beta, u_t drop
after month 84). This file does **not** introduce TWFE, cartels, QALY, nudges,
or a dashboard. It asks: if that utilisation DGP is further wrecked by MNAR
missing months or by truncating high post-2020 counts, does the full-window
count ratio still look attenuated relative to the pre-2020 fit?

Answer this script is allowed to give: a labelled SYNTHETIC comparison.
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
OUT = ROOT / "outputs" / "health_econ" / "synthetic_mnar_selection_2026-09-10.json"
RNG = np.random.default_rng(20260911)

N_REPS = 200
PRE = HELPER.PRE
N_MONTHS = HELPER.N_MONTHS


def _fit_pair(y: np.ndarray, x: np.ndarray, days: np.ndarray, mask: np.ndarray) -> tuple[float, float]:
    pre_m = mask & (np.arange(N_MONTHS) < PRE)
    full_m = mask
    if pre_m.sum() < 20 or full_m.sum() < 40:
        return float("nan"), float("nan")
    pre = np.exp(HELPER._poisson_glm_beta(y[pre_m], x[pre_m], days[pre_m]))
    full = np.exp(HELPER._poisson_glm_beta(y[full_m], x[full_m], days[full_m]))
    return pre, full


def _mnar_mask(y: np.ndarray) -> np.ndarray:
    """Post-2020 months more likely missing when counts are high (avoidance of peaks)."""
    mask = np.ones(N_MONTHS, dtype=bool)
    post = np.arange(N_MONTHS) >= PRE
    z = (y - y.mean()) / max(float(y.std()), 1e-6)
    p_miss = np.clip(0.15 + 0.25 * (1.0 / (1.0 + np.exp(-z))), 0.05, 0.6)
    drop = post & (RNG.uniform(size=N_MONTHS) < p_miss)
    mask[drop] = False
    return mask


def _truncation_mask(y: np.ndarray) -> np.ndarray:
    """Keep only post-2020 months below the pre-2020 75th percentile of y."""
    mask = np.ones(N_MONTHS, dtype=bool)
    cut = float(np.quantile(y[:PRE], 0.75))
    post = np.arange(N_MONTHS) >= PRE
    mask[post & (y > cut)] = False
    return mask


def main() -> None:
    x, days, month = HELPER._design()
    u = np.ones(N_MONTHS)
    u[PRE:] = 0.55
    scenarios = {
        "utilisation_only": {"pre": [], "full": []},
        "mnar_missing": {"pre": [], "full": []},
        "selected_truncation": {"pre": [], "full": []},
    }
    for _ in range(N_REPS):
        mu = HELPER._mu(x, days, month, u)
        y = RNG.poisson(mu).astype(float)
        complete = np.ones(N_MONTHS, dtype=bool)
        p0, f0 = _fit_pair(y, x, days, complete)
        p1, f1 = _fit_pair(y, x, days, _mnar_mask(y))
        p2, f2 = _fit_pair(y, x, days, _truncation_mask(y))
        scenarios["utilisation_only"]["pre"].append(p0)
        scenarios["utilisation_only"]["full"].append(f0)
        scenarios["mnar_missing"]["pre"].append(p1)
        scenarios["mnar_missing"]["full"].append(f1)
        scenarios["selected_truncation"]["pre"].append(p2)
        scenarios["selected_truncation"]["full"].append(f2)

    payload: dict = {
        "data_status": "SYNTHETIC",
        "parent": "scripts/72_synthetic_utilisation_shock.py",
        "n_reps": N_REPS,
        "true_count_ratio": float(np.exp(HELPER.TRUE_BETA)),
        "note": (
            "SYNTHETIC night-shift mutation. Constant true beta. "
            "Not HA. Not physiology. Not a cartel/QALY/TWFE model."
        ),
        "scenarios": {},
    }
    for name, store in scenarios.items():
        pre = np.array(store["pre"], dtype=float)
        full = np.array(store["full"], dtype=float)
        payload["scenarios"][name] = {
            "mean_pre_window_cr": float(np.nanmean(pre)),
            "mean_full_window_cr": float(np.nanmean(full)),
            "median_pre_minus_full": float(np.nanmedian(pre - full)),
            "n_finite": int(np.isfinite(pre - full).sum()),
        }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
