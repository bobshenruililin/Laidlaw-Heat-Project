#!/usr/bin/env python3
"""SYNTHETIC_CALIBRATION Monte Carlo for the health-economics laboratory.

Twin of scripts/48_health_econ_monte_carlo.R (MASS::glm.nb). This Python engine
runs where Rscript is absent. Family: Poisson GLM with month FE + patsy cr(time, df=4)
+ exposure + log(days) offset. Not identical to glm.nb; documented as such.

Uses REAL_PUBLIC_HKO exposures. Generates SYNTHETIC counts. Reads no HA health files.
"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from patsy import dmatrices, cr  # noqa: F401  (cr used in formulas)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "health_econ"
DOCS = ROOT / "docs" / "health_econ"
OUT.mkdir(parents=True, exist_ok=True)

PROVENANCE = "SYNTHETIC_CALIBRATION"
N_REPS = int(os.environ.get("HE_MC_REPS", "200"))
MASTER_SEED = int(os.environ.get("HE_MC_SEED", "20260814"))
SCENARIOS = os.environ.get("HE_MC_SCENARIOS", "all")
NB_THETA = float(os.environ.get("HE_MC_THETA", "50"))
CI_HF_COLD_LOG = math.log(1.144) - math.log(1.006)
CI_CHD_HN_LOG = math.log(1.042) - math.log(1.002)
SEW_TOL = math.log(1.10)
EPS_TRANSPORT = math.log(1.05)


def want(tag: str) -> bool:
    if SCENARIOS == "all":
        return True
    if SCENARIOS == "survivors":
        return tag in {"HE-07", "HE-08", "HE-10", "HE-C2-10"}
    if SCENARIOS == "cycle2":
        return tag in {"HE-C2-10", "HE-C2-02", "HE-08"}
    if SCENARIOS == "smoke":
        return tag in {"HE-01", "HE-10", "HE-C2-10"}
    return True


def rnb(mu, rng, theta=NB_THETA):
    mu = np.maximum(np.asarray(mu, dtype=float), 1e-8)
    p = theta / (theta + mu)
    return rng.negative_binomial(theta, p)


def fit_aor(y, x, month, time_index, days, extra=None):
    df = pd.DataFrame(
        {
            "y": np.asarray(y, dtype=float),
            "x": np.asarray(x, dtype=float),
            "month": np.asarray(month, dtype=int),
            "time_index": np.asarray(time_index, dtype=float),
            "days": np.asarray(days, dtype=float),
        }
    )
    if extra:
        for k, v in extra.items():
            df[k] = np.asarray(v)
    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    df = df[(df["days"] > 0) & (df["y"] >= 0)]
    if len(df) < 80 or df["month"].nunique() < 8:
        return {"ok": False, "est": np.nan, "se": np.nan, "n": len(df)}
    rhs = "C(month) + cr(time_index, df=4) + x"
    if extra:
        rhs += " + " + " + ".join(extra.keys())
    try:
        yv, X = dmatrices(f"y ~ {rhs}", df, return_type="dataframe")
        offset = np.log(df["days"].to_numpy())
        res = sm.GLM(
            yv, X, family=sm.families.Poisson(), offset=offset
        ).fit(disp=False, maxiter=80)
        if "x" not in res.params.index:
            return {"ok": False, "est": np.nan, "se": np.nan, "n": len(df)}
        est = float(res.params["x"])
        se = float(res.bse["x"])
        ok = np.isfinite(est) and np.isfinite(se) and se > 0
        return {"ok": ok, "est": est, "se": se, "n": len(df)}
    except Exception:
        return {"ok": False, "est": np.nan, "se": np.nan, "n": len(df)}


def fit_aor_lags(y, x, month, time_index, days):
    x = np.asarray(x, dtype=float)
    n = len(x)
    x1 = np.r_[np.nan, x[:-1]]
    x2 = np.r_[np.nan, np.nan, x[:-2]]
    df = pd.DataFrame(
        {
            "y": np.asarray(y, dtype=float),
            "x": x,
            "x1": x1,
            "x2": x2,
            "month": np.asarray(month, dtype=int),
            "time_index": np.asarray(time_index, dtype=float),
            "days": np.asarray(days, dtype=float),
        }
    ).dropna()
    if len(df) < 80:
        return {"ok": False, "b0": np.nan, "b1": np.nan, "b2": np.nan, "se0": np.nan}
    try:
        yv, X = dmatrices(
            "y ~ C(month) + cr(time_index, df=4) + x + x1 + x2",
            df,
            return_type="dataframe",
        )
        offset = np.log(df["days"].to_numpy())
        res = sm.GLM(yv, X, family=sm.families.Poisson(), offset=offset).fit(
            disp=False, maxiter=80
        )
        return {
            "ok": True,
            "b0": float(res.params["x"]),
            "b1": float(res.params["x1"]),
            "b2": float(res.params["x2"]),
            "se0": float(res.bse["x"]),
        }
    except Exception:
        return {"ok": False, "b0": np.nan, "b1": np.nan, "b2": np.nan, "se0": np.nan}


def fit_regime(y, x, R, month, time_index, days):
    df = pd.DataFrame(
        {
            "y": np.asarray(y, dtype=float),
            "x": np.asarray(x, dtype=float),
            "R": np.asarray(R, dtype=float),
            "xR": np.asarray(x, dtype=float) * np.asarray(R, dtype=float),
            "month": np.asarray(month, dtype=int),
            "time_index": np.asarray(time_index, dtype=float),
            "days": np.asarray(days, dtype=float),
        }
    ).replace([np.inf, -np.inf], np.nan).dropna()
    df = df[(df["days"] > 0) & (df["y"] >= 0)]
    if len(df) < 80:
        return {"ok": False, "b0": np.nan, "dtheta": np.nan, "se_d": np.nan}
    try:
        yv, X = dmatrices(
            "y ~ C(month) + cr(time_index, df=4) + x + R + xR",
            df,
            return_type="dataframe",
        )
        offset = np.log(df["days"].to_numpy())
        res = sm.GLM(yv, X, family=sm.families.Poisson(), offset=offset).fit(
            disp=False, maxiter=80
        )
        return {
            "ok": True,
            "b0": float(res.params["x"]),
            "dtheta": float(res.params["xR"]),
            "se_d": float(res.bse["xR"]),
        }
    except Exception:
        return {"ok": False, "b0": np.nan, "dtheta": np.nan, "se_d": np.nan}


def macro_shock(n, is_202002, is_202202, seed, xi=math.log(1.20)):
    rng = np.random.default_rng(seed)
    e = np.zeros(n)
    nu = rng.normal(0, 0.25, n)
    for t in range(n):
        prev = 0.0 if t == 0 else e[t - 1]
        e[t] = 0.4 * prev + nu[t]
    return xi * is_202002 + xi * is_202202 + e


def mnar_keep(y, x, seed, frac_drop=0.10):
    rng = np.random.default_rng(seed)
    y = np.asarray(y, dtype=float)
    x = np.asarray(x, dtype=float)
    z = (np.log1p(np.maximum(y, 0)) - np.nanmean(np.log1p(np.maximum(y, 0)))) / (
        np.nanstd(np.log1p(np.maximum(y, 0))) + 1e-8
    ) + np.abs(x - np.nanmean(x)) / (np.nanstd(x) + 1e-8)

    def mean_keep(a0):
        return np.mean(1 / (1 + np.exp(-(a0 - 0.8 * z))))

    lo, hi = -8.0, 8.0
    target = 1 - frac_drop
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if mean_keep(mid) > target:
            hi = mid
        else:
            lo = mid
    p = 1 / (1 + np.exp(-(0.5 * (lo + hi) - 0.8 * z)))
    return rng.random(len(y)) < p


def g_daily(tmean, a, bc, bh, mmt=26.0):
    tmean = np.asarray(tmean, dtype=float)
    return np.exp(a + bc * np.maximum(mmt - tmean, 0) ** 2 + bh * np.maximum(tmean - mmt, 0) ** 2)


def load_monthly():
    d = pd.read_csv(ROOT / "data_processed" / "exposures_monthly_2013_2023.csv")
    d["month_date"] = pd.to_datetime(d["month_date"])
    d["days"] = d["expected_days"].astype(float)
    d["hn5"] = d["hot_nights"] / 5.0
    d["cd5"] = d["cold_days"] / 5.0
    d["covid_R"] = (
        (d["month_date"] >= "2020-03-01") & (d["month_date"] <= "2022-12-01")
    ).astype(int)
    d["is_202002"] = (d["month_id"] == "2020-02").astype(float)
    d["is_202202"] = (d["month_id"] == "2022-02").astype(float)
    return d


def load_daily():
    d = pd.read_csv(ROOT / "data_processed" / "md_daily_weather_design_2013_2023.csv")
    d["month_id"] = d["month_id"].astype(str)
    return d


def row_base(scenario, hypothesis, rep, **kw):
    out = {
        "scenario": scenario,
        "hypothesis": hypothesis,
        "rep": int(rep),
        "ok": False,
        "est": np.nan,
        "se": np.nan,
        "reject05": np.nan,
        "covers_true": np.nan,
        "true_theta": np.nan,
        "stat_name": "",
        "stat_value": np.nan,
        "data_status": PROVENANCE,
    }
    out.update(kw)
    return out


def main():
    monthly = load_monthly()
    daily = load_daily()
    n = len(monthly)
    assert n == 132, n
    season_hf = 0.18 * np.cos(2 * math.pi * (monthly["month"].to_numpy() - 1) / 12)
    results = []

    # ---- HE-01 ----
    if want("HE-01"):
        print("HE-01", flush=True)
        x = monthly["cd5"].to_numpy()
        month = monthly["month"].to_numpy()
        time_index = monthly["time_index"].to_numpy()
        days = monthly["days"].to_numpy()
        year = monthly["year"].to_numpy()
        for rho in (0.6, 0.8, 1.0):
            for kink in (False, True):
                if rho != 0.6 and kink:
                    continue
                scen = f"HE01_size_rho{int(rho*10):02d}" + ("_kink2020" if kink else "")
                for r in range(1, N_REPS + 1):
                    rng = np.random.default_rng(MASTER_SEED + 1000 + r + int(rho * 100) + 17 * kink)
                    S = 220 * 80.0
                    h0 = 220 / (S * days.mean())
                    y = np.zeros(n)
                    freeze = kink & (year == 2020)
                    for t in range(n):
                        h = h0 * math.exp(season_hf[t])
                        p = min(max(1 - math.exp(-days[t] * h), 1e-8), 0.5)
                        y[t] = rng.binomial(max(int(round(S)), 1), p)
                        inflow = 0.0 if freeze[t] else rho * S * p
                        S = max(S - y[t] + rng.poisson(inflow), 1.0)
                    fit = fit_aor(y, x, month, time_index, days)
                    rej = abs(fit["est"] / fit["se"]) > 1.96 if fit["ok"] else np.nan
                    results.append(
                        row_base(
                            scen,
                            "HE-01",
                            r,
                            ok=fit["ok"],
                            est=fit["est"],
                            se=fit["se"],
                            true_theta=0.0,
                            reject05=rej,
                            covers_true=abs(fit["est"]) <= 1.96 * fit["se"] if fit["ok"] else np.nan,
                            stat_name="size_reject",
                            stat_value=float(rej) if fit["ok"] else np.nan,
                            rho=rho,
                            kink2020=int(kink),
                        )
                    )

    # ---- HE-03 ----
    if want("HE-03"):
        print("HE-03", flush=True)
        daily_base = 220 / monthly["days"].mean()
        theta_true = math.log(1.07)
        month = monthly["month"].to_numpy()
        time_index = monthly["time_index"].to_numpy()
        days = monthly["days"].to_numpy()
        cd5 = monthly["cd5"].to_numpy()
        for u in (0.85, 0.95, 0.99):
            scen = f"HE03_u{int(u*100):03d}"
            K = math.ceil(daily_base / u)
            lam = daily_base * np.exp(
                theta_true * daily["cold_day"].to_numpy()
                + 0.18 * np.cos(2 * math.pi * (daily["month"].to_numpy() - 1) / 12)
            )
            for r in range(1, N_REPS + 1):
                rng = np.random.default_rng(MASTER_SEED + 2000 + r + int(u * 1000))
                D = rng.poisson(lam)
                Q = np.minimum(D, K)
                y_c = pd.Series(Q).groupby(daily["month_id"].to_numpy()).sum().reindex(monthly["month_id"]).to_numpy()
                y_u = pd.Series(D).groupby(daily["month_id"].to_numpy()).sum().reindex(monthly["month_id"]).to_numpy()
                fit_c = fit_aor(y_c, cd5, month, time_index, days)
                fit_u = fit_aor(y_u, cd5, month, time_index, days)
                att = (
                    1 - fit_c["est"] / fit_u["est"]
                    if fit_c["ok"] and fit_u["ok"] and abs(fit_u["est"]) > 1e-8
                    else np.nan
                )
                results.append(
                    row_base(
                        scen,
                        "HE-03",
                        r,
                        ok=fit_c["ok"],
                        est=fit_c["est"],
                        se=fit_c["se"],
                        true_theta=theta_true,
                        reject05=abs(fit_c["est"] / fit_c["se"]) > 1.96 if fit_c["ok"] else np.nan,
                        covers_true=abs(fit_c["est"] - theta_true) <= 1.96 * fit_c["se"] if fit_c["ok"] else np.nan,
                        stat_name="relative_attenuation",
                        stat_value=att,
                        utilisation=u,
                    )
                )

    # ---- HE-05 ----
    if want("HE-05"):
        print("HE-05", flush=True)
        theta0 = math.log(1.07)
        x = monthly["cd5"].to_numpy()
        x1 = np.r_[x.mean(), x[:-1]]
        x2 = np.r_[x.mean(), x.mean(), x[:-2]][:n]
        month = monthly["month"].to_numpy()
        time_index = monthly["time_index"].to_numpy()
        days = monthly["days"].to_numpy()
        for phi in (0.0, 0.3, 0.6):
            scen = f"HE05_phi{int(phi*10):02d}"
            b0, b1, b2 = theta0, -0.60 * phi * theta0, -0.40 * phi * theta0
            for r in range(1, N_REPS + 1):
                rng = np.random.default_rng(MASTER_SEED + 3000 + r + int(phi * 100))
                mu = 220 * np.exp(season_hf + b0 * x + b1 * x1 + b2 * x2)
                y = rnb(mu, rng)
                fit = fit_aor_lags(y, x, month, time_index, days)
                bsum = fit["b0"] + fit["b1"] + fit["b2"] if fit["ok"] else np.nan
                phi_hat = 1 - bsum / fit["b0"] if fit["ok"] and abs(fit["b0"]) > 1e-8 else np.nan
                rej = (fit["b1"] + fit["b2"]) < -1.64 * abs(fit["se0"]) * 0.5 if fit["ok"] else np.nan
                results.append(
                    row_base(
                        scen,
                        "HE-05",
                        r,
                        ok=fit["ok"],
                        est=bsum,
                        se=fit["se0"],
                        true_theta=(1 - phi) * theta0,
                        reject05=rej,
                        covers_true=abs(bsum - (1 - phi) * theta0) <= 1.96 * abs(fit["se0"]) if fit["ok"] else np.nan,
                        stat_name="phi_hat",
                        stat_value=phi_hat,
                        phi_true=phi,
                    )
                )

    # ---- HE-07 ----
    if want("HE-07"):
        print("HE-07", flush=True)
        alpha_T = math.log(1.07)
        omega0 = 0.20
        z0 = float(sm.distributions.norm.ppf(1 - omega0)) if False else float(
            __import__("scipy").stats.norm.ppf(1 - omega0)
        )
        phi_z = float(__import__("scipy").stats.norm.pdf(z0))
        x = monthly["cd5"].to_numpy()
        x_s = (x - x.mean()) / (x.std() + 1e-8)
        month = monthly["month"].to_numpy()
        time_index = monthly["time_index"].to_numpy()
        days = monthly["days"].to_numpy()
        is20 = monthly["is_202002"].to_numpy()
        is22 = monthly["is_202202"].to_numpy()
        idx = 0
        for cT in (0.0, 0.15, 0.30, 0.45):
            for stress in ("base", "macro", "mnar"):
                scen = f"HE07_cT{int(cT*100):02d}_{stress}"
                for r in range(1, N_REPS + 1):
                    idx += 1
                    rng = np.random.default_rng(MASTER_SEED + 4000 + idx)
                    mu_m = (220 / omega0) * np.exp(season_hf + alpha_T * x)
                    M = rnb(mu_m, rng)
                    z = z0 + cT * x_s
                    omega = np.clip(1 - __import__("scipy").stats.norm.cdf(z), 0.02, 0.95)
                    y = rng.binomial(np.maximum(M, 0).astype(int), omega)
                    if stress == "macro":
                        U = macro_shock(n, is20, is22, MASTER_SEED + 4100 + r)
                        y = rnb(np.maximum(y, 1) * np.exp(U), rng)
                    if stress == "mnar":
                        keep = mnar_keep(y, x, MASTER_SEED + 4200 + r)
                        y = np.where(keep, y, np.nan)
                    fit = fit_aor(y, x, month, time_index, days)
                    gap = alpha_T - fit["est"] if fit["ok"] else np.nan
                    results.append(
                        row_base(
                            scen,
                            "HE-07",
                            r,
                            ok=fit["ok"],
                            est=fit["est"],
                            se=fit["se"],
                            true_theta=alpha_T,
                            reject05=abs(fit["est"] / fit["se"]) > 1.96 if fit["ok"] else np.nan,
                            covers_true=abs(fit["est"] - alpha_T) <= 1.96 * fit["se"] if fit["ok"] else np.nan,
                            stat_name="epsM_minus_epsY",
                            stat_value=gap,
                            cT=cT,
                            stress=stress,
                        )
                    )

    # ---- HE-08 ----
    if want("HE-08"):
        print("HE-08", flush=True)
        theta0 = math.log(1.07)
        x = monthly["cd5"].to_numpy()
        R = monthly["covid_R"].to_numpy()
        month = monthly["month"].to_numpy()
        time_index = monthly["time_index"].to_numpy()
        days = monthly["days"].to_numpy()
        is20 = monthly["is_202002"].to_numpy()
        is22 = monthly["is_202202"].to_numpy()
        for dth in (0.0, math.log(1.03), -math.log(1.03)):
            for stress in ("base", "macro", "mnar"):
                scen = f"HE08_d{dth*100:+03.0f}_{stress}"
                for r in range(1, N_REPS + 1):
                    rng = np.random.default_rng(MASTER_SEED + 5000 + r + int(dth * 1000) + len(stress))
                    theta_t = theta0 + dth * R
                    mu = 220 * np.exp(season_hf + theta_t * x - 0.15 * R)
                    y = rnb(mu, rng)
                    if stress == "macro":
                        U = macro_shock(n, is20, is22, MASTER_SEED + 5100 + r)
                        y = rnb(mu * np.exp(U), rng)
                    if stress == "mnar":
                        keep = mnar_keep(y, x, MASTER_SEED + 5200 + r)
                        y = np.where(keep, y, np.nan)
                    pooled = fit_aor(y, x, month, time_index, days)
                    reg = fit_regime(y, x, R, month, time_index, days)
                    rte = abs(reg["dtheta"]) if reg["ok"] else np.nan
                    results.append(
                        row_base(
                            scen,
                            "HE-08",
                            r,
                            ok=pooled["ok"],
                            est=pooled["est"],
                            se=pooled["se"],
                            true_theta=theta0,
                            reject05=abs(reg["dtheta"] / reg["se_d"]) > 1.96 if reg["ok"] else np.nan,
                            covers_true=abs(pooled["est"] - theta0) <= 1.96 * pooled["se"] if pooled["ok"] else np.nan,
                            stat_name="RTE",
                            stat_value=rte,
                            delta_true=dth,
                            stress=stress,
                        )
                    )

    # ---- HE-10 ----
    beta_target = np.nan
    if want("HE-10") or want("HE-C2-10"):
        print("calibrate g()", flush=True)
        theta_cold = math.log(1.07)
        bc = theta_cold / 25
        bh = theta_cold / 100

        def loss(a):
            gy = g_daily(daily["tmean"], a, bc, bh)
            mu_m = pd.Series(gy, index=daily["month_id"]).groupby(level=0).sum()
            return (mu_m.mean() - 220.0) ** 2

        grid = np.linspace(-8, 8, 81)
        a_hat = float(grid[int(np.argmin([loss(a) for a in grid]))])
        gy = g_daily(daily["tmean"], a_hat, bc, bh)
        mu_month = (
            pd.Series(gy, index=daily["month_id"]).groupby(level=0).sum().reindex(monthly["month_id"]).to_numpy()
        )
        g_bar = g_daily(monthly["mean_temp"], a_hat, bc, bh)
        mu_rep = monthly["days"].to_numpy() * g_bar
        month = monthly["month"].to_numpy()
        time_index = monthly["time_index"].to_numpy()
        days = monthly["days"].to_numpy()
        target_agg = fit_aor(mu_month, monthly["mean_temp"], month, time_index, days)
        target_rep = fit_aor(mu_rep, monthly["mean_temp"], month, time_index, days)
        beta_target = target_agg["est"]
        beta_rep = target_rep["est"]
        print(f"HE-10 noiseless beta_agg={beta_target} beta_rep={beta_rep}", flush=True)

    if want("HE-10"):
        print("HE-10", flush=True)
        month = monthly["month"].to_numpy()
        time_index = monthly["time_index"].to_numpy()
        days = monthly["days"].to_numpy()
        is20 = monthly["is_202002"].to_numpy()
        is22 = monthly["is_202202"].to_numpy()
        for stress in ("base", "macro", "mnar", "select"):
            scen = f"HE10_mean_{stress}"
            for r in range(1, N_REPS + 1):
                rng = np.random.default_rng(MASTER_SEED + 6000 + r + len(stress))
                y_day = rng.poisson(gy)
                if stress == "select":
                    z = (daily["tmean"] - daily["tmean"].mean()) / (daily["tmean"].std() + 1e-8)
                    keep_p = np.clip(__import__("scipy").stats.norm.cdf(-0.4 * z), 0.2, 0.95)
                    y_day = rng.binomial(y_day, keep_p)
                y = pd.Series(y_day, index=daily["month_id"]).groupby(level=0).sum().reindex(monthly["month_id"]).to_numpy()
                if stress == "macro":
                    U = macro_shock(n, is20, is22, MASTER_SEED + 6100 + r)
                    y = rnb(np.maximum(y, 1) * np.exp(U), rng)
                if stress == "mnar":
                    keep = mnar_keep(y, monthly["mean_temp"], MASTER_SEED + 6200 + r)
                    y = np.where(keep, y, np.nan)
                fit = fit_aor(y, monthly["mean_temp"], month, time_index, days)
                adr = abs(fit["est"] - beta_target) / (0.5 * CI_HF_COLD_LOG) if fit["ok"] and np.isfinite(beta_target) else np.nan
                results.append(
                    row_base(
                        scen,
                        "HE-10",
                        r,
                        ok=fit["ok"],
                        est=fit["est"],
                        se=fit["se"],
                        true_theta=beta_target,
                        covers_true=abs(fit["est"] - beta_target) <= 1.96 * fit["se"] if fit["ok"] and np.isfinite(beta_target) else np.nan,
                        stat_name="ADR",
                        stat_value=adr,
                        stress=stress,
                        beta_rep=beta_rep,
                    )
                )
        tgt_cd = fit_aor(mu_month, monthly["cd5"], month, time_index, days)["est"]
        for stress in ("base", "mnar"):
            scen = f"HE10_cold_{stress}"
            for r in range(1, N_REPS + 1):
                rng = np.random.default_rng(MASTER_SEED + 6300 + r + len(stress))
                y_day = rng.poisson(gy)
                y = pd.Series(y_day, index=daily["month_id"]).groupby(level=0).sum().reindex(monthly["month_id"]).to_numpy()
                if stress == "mnar":
                    keep = mnar_keep(y, monthly["cd5"], MASTER_SEED + 6400 + r)
                    y = np.where(keep, y, np.nan)
                fit = fit_aor(y, monthly["cd5"], month, time_index, days)
                adr = abs(fit["est"] - tgt_cd) / (0.5 * CI_HF_COLD_LOG) if fit["ok"] and np.isfinite(tgt_cd) else np.nan
                results.append(
                    row_base(
                        scen,
                        "HE-10",
                        r,
                        ok=fit["ok"],
                        est=fit["est"],
                        se=fit["se"],
                        true_theta=tgt_cd,
                        covers_true=abs(fit["est"] - tgt_cd) <= 1.96 * fit["se"] if fit["ok"] and np.isfinite(tgt_cd) else np.nan,
                        stat_name="ADR",
                        stat_value=adr,
                        stress=stress,
                        exposure_family="cold_days_per5",
                    )
                )

    # ---- HE-C2-10 ----
    if want("HE-C2-10"):
        print("HE-C2-10", flush=True)
        month = monthly["month"].to_numpy()
        time_index = monthly["time_index"].to_numpy()
        days = monthly["days"].to_numpy()
        daily_base = float(np.mean(gy))
        for u in (0.85, 0.95, 1.05):
            for seasonal_k in (False, True):
                scen = f"HEC210_u{int(u*100):03d}_{'Kseason' if seasonal_k else 'Kflat'}"
                K_flat = daily_base / u
                for r in range(1, N_REPS + 1):
                    rng = np.random.default_rng(MASTER_SEED + 7000 + r + int(u * 100) + 11 * seasonal_k)
                    if seasonal_k:
                        K = K_flat * np.exp(0.12 * np.cos(2 * math.pi * (daily["month"].to_numpy() - 1) / 12))
                    else:
                        K = np.full(len(daily), K_flat)
                    D = rng.poisson(gy)
                    Q = np.minimum(D, K)
                    y = pd.Series(Q, index=daily["month_id"]).groupby(level=0).sum().reindex(monthly["month_id"]).to_numpy()
                    fit = fit_aor(y, monthly["mean_temp"], month, time_index, days)
                    catd = (fit["est"] - beta_target) / (0.5 * CI_HF_COLD_LOG) if fit["ok"] and np.isfinite(beta_target) else np.nan
                    results.append(
                        row_base(
                            scen,
                            "HE-C2-10",
                            r,
                            ok=fit["ok"],
                            est=fit["est"],
                            se=fit["se"],
                            true_theta=beta_target,
                            covers_true=abs(fit["est"] - beta_target) <= 1.96 * fit["se"] if fit["ok"] and np.isfinite(beta_target) else np.nan,
                            stat_name="CATD",
                            stat_value=catd,
                            utilisation=u,
                            K_seasonal=int(seasonal_k),
                        )
                    )

    # ---- HE-C2-02 ----
    if want("HE-C2-02"):
        print("HE-C2-02", flush=True)
        daily_base = 220 / monthly["days"].mean()
        theta_true = math.log(1.07)
        lam = daily_base * np.exp(
            theta_true * daily["cold_day"].to_numpy()
            + 0.18 * np.cos(2 * math.pi * (daily["month"].to_numpy() - 1) / 12)
        )
        month = monthly["month"].to_numpy()
        time_index = monthly["time_index"].to_numpy()
        days = monthly["days"].to_numpy()
        cd5 = monthly["cd5"].to_numpy()
        K = daily_base / 0.85
        for family in ("demand", "queue"):
            scen = f"HEC202_{family}"
            for r in range(1, N_REPS + 1):
                rng = np.random.default_rng(MASTER_SEED + 8000 + r + len(family))
                D = rng.poisson(lam)
                A = np.minimum(D, K) if family == "queue" else D
                y = pd.Series(A, index=daily["month_id"]).groupby(level=0).sum().reindex(monthly["month_id"]).to_numpy()
                fit = fit_aor(y, cd5, month, time_index, days)
                slope = np.nan
                try:
                    df = pd.DataFrame(
                        {
                            "y": y,
                            "x": cd5,
                            "month": month,
                            "time_index": time_index,
                            "days": days,
                        }
                    )
                    yv, X = dmatrices(
                        "y ~ C(month) + cr(time_index, df=4) + x",
                        df,
                        return_type="dataframe",
                    )
                    res = sm.GLM(
                        yv, X, family=sm.families.Poisson(), offset=np.log(df["days"])
                    ).fit(disp=False, maxiter=80)
                    mu = np.asarray(res.fittedvalues)
                    pr = (y - mu) ** 2 / np.maximum(mu, 1e-6)
                    slope = float(np.polyfit(mu, pr, 1)[0])
                except Exception:
                    slope = np.nan
                results.append(
                    row_base(
                        scen,
                        "HE-C2-02",
                        r,
                        ok=fit["ok"],
                        est=fit["est"],
                        se=fit["se"],
                        true_theta=theta_true,
                        stat_name="dispersion_slope",
                        stat_value=slope,
                        family=family,
                    )
                )

    raw = pd.DataFrame(results)
    raw["master_seed"] = MASTER_SEED
    raw["n_reps_requested"] = N_REPS
    raw["run_scenarios"] = SCENARIOS
    raw_path = OUT / "cycle1_mc_raw.csv"
    raw.to_csv(raw_path, index=False)

    def summarise(d):
        ok = d[d["ok"] == True]  # noqa: E712
        sv = pd.to_numeric(ok["stat_value"], errors="coerce")
        est = pd.to_numeric(ok["est"], errors="coerce")
        return pd.Series(
            {
                "hypothesis": d["hypothesis"].iloc[0],
                "n_reps": len(d),
                "n_ok": len(ok),
                "frac_ok": len(ok) / max(len(d), 1),
                "mean_est": est.mean(),
                "mean_se": pd.to_numeric(ok["se"], errors="coerce").mean(),
                "est_p05": est.quantile(0.05) if len(est) else np.nan,
                "est_p50": est.median() if len(est) else np.nan,
                "est_p95": est.quantile(0.95) if len(est) else np.nan,
                "mean_stat": sv.mean(),
                "stat_p05": sv.quantile(0.05) if len(sv) else np.nan,
                "stat_p50": sv.median() if len(sv) else np.nan,
                "stat_p95": sv.quantile(0.95) if len(sv) else np.nan,
                "empirical_size_or_power": pd.to_numeric(ok["reject05"], errors="coerce").mean(),
                "coverage": pd.to_numeric(ok["covers_true"], errors="coerce").mean(),
                "stat_name": d["stat_name"].dropna().iloc[0] if d["stat_name"].notna().any() else "",
                "data_status": PROVENANCE,
            }
        )

    summ = raw.groupby("scenario", sort=True).apply(summarise, include_groups=False).reset_index()
    summ.to_csv(OUT / "cycle1_mc_summary.csv", index=False)

    def geth(h):
        return raw[(raw["hypothesis"] == h) & (raw["ok"] == True)]  # noqa: E712

    he01, he03, he05 = geth("HE-01"), geth("HE-03"), geth("HE-05")
    he07, he08, he10 = geth("HE-07"), geth("HE-08"), geth("HE-10")
    c210, c202 = geth("HE-C2-10"), geth("HE-C2-02")

    sew = np.nan
    ss = np.nan
    if len(he07):
        v = pd.to_numeric(he07["stat_value"], errors="coerce").dropna()
        if len(v):
            sew = float(v.quantile(0.975) - v.quantile(0.025))
        ss = float((pd.to_numeric(he07["est"], errors="coerce") > 0).mean())

    adr95 = float(pd.to_numeric(he10["stat_value"], errors="coerce").quantile(0.95)) if len(he10) else np.nan

    def scen_stat(name, q=None, mean_rej=False):
        d = raw[(raw["scenario"] == name) & (raw["ok"] == True)]  # noqa: E712
        if not len(d):
            return np.nan
        if mean_rej:
            return float(pd.to_numeric(d["reject05"], errors="coerce").mean())
        v = pd.to_numeric(d["stat_value"], errors="coerce")
        return float(v.quantile(q)) if q is not None else float(v.mean())

    catd = pd.to_numeric(c210["stat_value"], errors="coerce") if len(c210) else pd.Series(dtype=float)
    q05 = float(catd.quantile(0.05)) if len(catd) else np.nan
    q95 = float(catd.quantile(0.95)) if len(catd) else np.nan

    gates = {
        "provenance": PROVENANCE,
        "engine": "python_poisson_glm_patsy_cr_df4",
        "r_twin": "scripts/48_health_econ_monte_carlo.R",
        "family_note": "Poisson GLM, not MASS::glm.nb. Same mean structure: month FE + cr(time,4) + x + log(days) offset.",
        "master_seed": MASTER_SEED,
        "n_reps": N_REPS,
        "scenarios": SCENARIOS,
        "monetisation_permitted": False,
        "gate3_input": False,
        "existing_interval_widths_log": {
            "hf_cold_days": CI_HF_COLD_LOG,
            "chd_hot_nights": CI_CHD_HN_LOG,
            "source": "EXISTING_EXPLORATORY_INTERVAL",
        },
        "HE01_size": float(pd.to_numeric(he01["reject05"], errors="coerce").mean()) if len(he01) else None,
        "HE01_size_gate": (
            "size_nominal_costing_caveat_only"
            if len(he01) and pd.to_numeric(he01["reject05"], errors="coerce").mean() <= 0.10
            else ("size_inflated_identification_leak" if len(he01) else "not_run")
        ),
        "HE03_median_attenuation": float(pd.to_numeric(he03["stat_value"], errors="coerce").median()) if len(he03) else None,
        "HE05_power_phi06": scen_stat("HE05_phi06", mean_rej=True),
        "HE07_SEW": sew if np.isfinite(sew) else None,
        "HE07_SS": ss if np.isfinite(ss) else None,
        "HE07_gate": (
            "lower_bound_passes_synthetic_grid"
            if np.isfinite(sew) and np.isfinite(ss) and ss >= 0.95 and sew <= SEW_TOL
            else ("lower_bound_fails" if np.isfinite(sew) else "not_run")
        ),
        "HE08_RTE_p95_when_delta0": scen_stat("HE08_d+000_base", q=0.95),
        "HE08_power_when_delta_log103": scen_stat("HE08_d+003_base", mean_rej=True),
        "HE10_ADR_p95": adr95 if np.isfinite(adr95) else None,
        "HE10_gate": (
            "cosmetic_under_imposed_g"
            if np.isfinite(adr95) and adr95 < 1
            else ("projection_validity_fails" if np.isfinite(adr95) else "not_run")
        ),
        "HEC210_CATD_p05": q05 if np.isfinite(q05) else None,
        "HEC210_CATD_p95": q95 if np.isfinite(q95) else None,
        "HEC210_sign_flip": bool(np.isfinite(q05) and np.isfinite(q95) and q05 * q95 < 0),
        "HEC202_demand_slope": float(pd.to_numeric(c202.loc[c202.get("family", "") == "demand", "stat_value"], errors="coerce").mean()) if "family" in c202.columns and len(c202) else None,
        "HEC202_queue_slope": float(pd.to_numeric(c202.loc[c202.get("family", "") == "queue", "stat_value"], errors="coerce").mean()) if "family" in c202.columns and len(c202) else None,
        "notes": [
            "All count series are SYNTHETIC. Exposure path is REAL_PUBLIC_HKO.",
            "No HA microdata were read. No stroke file. No currency.",
            "A passing size test does not revive a KILL on an unobserved stock level.",
            "ADR/CATD are conditional on an imposed daily g; they do not recover a daily coefficient.",
        ],
    }
    if "family" in raw.columns:
        dem = raw[(raw["hypothesis"] == "HE-C2-02") & (raw["family"] == "demand") & (raw["ok"] == True)]
        que = raw[(raw["hypothesis"] == "HE-C2-02") & (raw["family"] == "queue") & (raw["ok"] == True)]
        gates["HEC202_demand_slope"] = float(pd.to_numeric(dem["stat_value"], errors="coerce").mean()) if len(dem) else None
        gates["HEC202_queue_slope"] = float(pd.to_numeric(que["stat_value"], errors="coerce").mean()) if len(que) else None

    (OUT / "cycle1_mc_gates.json").write_text(json.dumps(gates, indent=2, default=str))
    pd.DataFrame(
        [
            {
                "timestamp": pd.Timestamp.now("UTC").isoformat(),
                "status": "ok",
                "n_rows": len(raw),
                "n_scenarios": int(raw["scenario"].nunique()) if len(raw) else 0,
                "n_reps": N_REPS,
                "scenarios": SCENARIOS,
                "master_seed": MASTER_SEED,
                "data_status": PROVENANCE,
                "engine": "python",
            }
        ]
    ).to_csv(OUT / "cycle1_mc_status.csv", index=False)

    # Sync UI payloads
    ui = {
        "gates": gates,
        "summary": json.loads(summ.to_json(orient="records")),
    }
    (DOCS / "results.json").write_text(json.dumps(ui, indent=2, default=str))
    for src, dest in [
        (OUT / "varsigma_hko.json", DOCS / "varsigma.json"),
        (OUT / "he_c2_port_matrix.json", DOCS / "port.json"),
    ]:
        if src.exists():
            dest.write_text(src.read_text())

    print("Wrote", raw_path, "rows", len(raw), "scenarios", raw["scenario"].nunique() if len(raw) else 0, flush=True)
    print(json.dumps({k: gates[k] for k in gates if k.endswith("gate") or k in {"HE01_size", "HE10_ADR_p95", "HEC210_sign_flip", "HE07_SEW"}}, indent=2), flush=True)


if __name__ == "__main__":
    main()
