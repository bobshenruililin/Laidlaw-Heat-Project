#!/usr/bin/env python3
"""Invariant checks for scripts/49_depletion_crucible.py.

No governed monthly HA counts. Re-runs the diagnostic and asserts the algebraic
facts the depletion proof depends on, including the ones that cut against it.
"""

from __future__ import annotations

import csv
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "depletion_crucible"


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> int:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "49_depletion_crucible.py")],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    summary = json.loads((OUT / "depletion_summary.json").read_text())
    absorb = {r["path"]: r for r in _read(OUT / "depletion_path_absorption.csv")}
    bias = {
        (r["path"], r["exposure"]): r for r in _read(OUT / "omitted_logr_bias.csv")
    }
    inter = {
        (r["path"], r["exposure"]): r
        for r in _read(OUT / "interaction_absorption.csv")
    }
    weight = {
        (r["outcome"], r["exposure"]): r
        for r in _read(OUT / "count_weighted_information.csv")
    }
    ladder = _read(OUT / "riskset_fatness_ladder.csv")
    stats = {(r["outcome"], r["pathway_id"]): r for r in _read(OUT / "riskset_fatness_ladder_stats.csv")}
    inv = {(r["outcome"], r["pathway_id"]): r for r in _read(OUT / "covid_kink_amplitude_inversion.csv")}
    annual = {
        (r["exposure"], r["outcome"]): r
        for r in _read(OUT / "annual_trend_collinearity.csv")
    }

    assert summary["n_months"] == 132
    assert summary["provenance"]["new_health_models"] is False
    assert summary["provenance"]["governed_monthly_counts_read"] is False
    assert summary["provenance"]["cohort_risk_set_available"] is False
    assert summary["provenance"]["depletion_paths"] == "ILLUSTRATIVE_ALGEBRA"
    # Approved annual totals fall by roughly half.
    assert 1.85 < summary["implied_event_halving_ratio"] < 2.0

    # Concession the memo must make: a 4-df spline absorbs smooth depletion
    # almost perfectly, so the additive channel alone is not the argument.
    for path in ("front_loaded", "closed_pool"):
        assert float(absorb[path]["r2_absorbed_by_month_plus_ns4"]) > 0.999
        assert float(absorb[path]["share_surviving_controls"]) < 0.001
        for expo in ("hot_nights", "cold_days"):
            mult = float(bias[(path, expo)]["rr_multiplier_per_reporting_step"])
            assert abs(mult - 1.0) < 0.002, (path, expo, mult)

    # The claim the memo does make: a non-smooth care-seeking kink is not
    # absorbed, and it transfers oppositely onto heat and cold.
    assert float(absorb["covid_kink_0p10_only"]["share_surviving_controls"]) > 0.70
    hot_kink = float(bias[("covid_kink_0p10_only", "hot_nights")]["bias_per_reporting_step"])
    cold_kink = float(bias[("covid_kink_0p10_only", "cold_days")]["bias_per_reporting_step"])
    assert hot_kink > 0.005
    assert cold_kink < -0.003

    # ns(time,4) spans functions of time, not time interacted with exposure.
    for path in ("front_loaded", "closed_pool"):
        for expo in ("hot_nights", "cold_days"):
            assert (
                float(inter[(path, expo)]["share_of_residualised_product_surviving"])
                > 0.80
            ), (path, expo)
        assert float(inter[(path, "cold_days")]["share_of_interaction_surviving_controls"]) > 0.50

    # Depletion and the heat trend run in opposite directions; cold does not.
    assert float(annual[("hot_nights", "chd")]["pearson_annual_exposure_vs_events"]) < -0.80
    assert float(annual[("very_hot_days", "chd")]["pearson_annual_exposure_vs_events"]) < -0.75
    assert abs(float(annual[("cold_days", "chd")]["pearson_annual_exposure_vs_events"])) < 0.35

    # Cold-day identifying variance sits in the fat risk set; hot nights do not.
    cold = weight[("hf", "cold_days")]
    hot = weight[("chd", "hot_nights")]
    assert float(cold["count_weighted_info_share_2013_2018"]) > 0.62
    assert float(hot["count_weighted_info_share_2013_2018"]) < 0.51
    assert float(cold["count_weighted_info_share_2013_2018"]) > float(
        cold["residual_var_share_2013_2018"]
    )

    # Paid ladder: HF cold days rises monotonically with risk-set fatness.
    hf_cold_rows = {
        r["scenario"]: r
        for r in ladder
        if r["outcome"] == "hf" and r["pathway_id"] == "P04B"
    }
    assert math.isclose(float(hf_cold_rows["pre_covid"]["rr"]), 1.11283089052394, rel_tol=1e-9)
    assert math.isclose(
        float(hf_cold_rows["drop_first_24_months"]["rr"]), 1.04289295509967, rel_tol=1e-9
    )
    fat = [
        (
            float(hf_cold_rows[s]["mean_monthly_events_in_window"]),
            float(hf_cold_rows[s]["rr"]),
        )
        for s in (
            "drop_first_24_months",
            "drop_first_12_months",
            "baseline_ns4",
            "pre_covid",
        )
    ]
    assert fat == sorted(fat), fat  # both coordinates increase together
    assert math.isclose(
        float(stats[("hf", "P04B")]["spearman_fatness_vs_abs_log_rr"]), 1.0, abs_tol=1e-9
    )
    # And the counterexample inside the memo: CHD hot nights does not follow it.
    assert float(stats[("chd", "P04A")]["spearman_fatness_vs_abs_log_rr"]) < 0.0
    assert summary["riskset_fatness_ladder"]["n_core_contrasts"] == 12
    assert summary["riskset_fatness_ladder"]["n_with_abs_log_rr_rank_corr_ge_0p8"] == 7
    assert summary["riskset_fatness_ladder"]["n_with_abs_log_rr_rank_corr_le_0"] == 3

    # Changing only the secular time control moves most contrasts by more than
    # their own point estimate, and the four that stay put are exactly the four
    # whose magnitude tracks risk-set fatness.
    tcs = summary["time_control_sensitivity"]
    assert tcs["n_contrasts_width_ge_baseline_log_rr"] == 6
    assert tcs["n_contrasts_stable_width_lt_0p30"] == 4
    assert tcs["sets_identical"] is True
    assert tcs["stable_set"] == ["hf/P01A", "hf/P02A", "hf/P02B", "hf/P04B"]
    assert tcs["chd_hot_nights_width_share_of_baseline"] > 0.60
    assert tcs["hf_cold_days_width_share_of_baseline"] < 0.20
    assert tcs["chd_hot_nights_p_range"][1] > 0.30

    # Amplitude inversion coherence: five CHD contrasts with transfer
    # coefficients spread ~3x recover the same latent dip amplitude.
    assert summary["covid_kink_inversion"]["transfer_coefficient_spread_ratio"] > 2.5
    assert 0.10 < summary["covid_kink_inversion"]["chd_non_cold_amplitude_mean"] < 0.12
    assert summary["covid_kink_inversion"]["chd_non_cold_amplitude_sd"] < 0.01
    # HF cold days is the exception, as the memo states.
    assert float(inv[("hf", "P04B")]["implied_dip_log_amplitude"]) < 0.05

    # Bind the memo to the tables: every string below is formatted from a value
    # computed above, so a pipeline change that moves the algebra fails here
    # instead of silently leaving stale figures in the proof.
    memo = (ROOT / "knowledge" / "crucible_agent_beta_depletion.md").read_text()
    claims = {
        "smooth absorption": f"{float(absorb['front_loaded']['r2_absorbed_by_month_plus_ns4']):.4f}",
        "kink surviving": f"{100 * float(absorb['covid_kink_0p10_only']['share_surviving_controls']):.1f}\\%",
        "kink absorbed": f"{100 * float(absorb['covid_kink_0p10_only']['r2_absorbed_by_month_plus_ns4']):.1f}\\%",
        "hot transfer": f"{hot_kink:.5f}",
        "cold transfer": f"{cold_kink:.5f}",
        "amplitude mean": f"{summary['covid_kink_inversion']['chd_non_cold_amplitude_mean']:.4f}",
        "amplitude sd": f"{summary['covid_kink_inversion']['chd_non_cold_amplitude_sd']:.4f}",
        "interaction cold": f"{100 * float(inter[('front_loaded', 'cold_days')]['share_of_residualised_product_surviving']):.1f}\\%",
        "interaction hot": f"{100 * float(inter[('front_loaded', 'hot_nights')]['share_of_residualised_product_surviving']):.1f}\\%",
        "hot annual corr": f"{float(annual[('hot_nights', 'chd')]['pearson_annual_exposure_vs_events']):.3f}",
        "cold annual corr": f"{float(annual[('cold_days', 'chd')]['pearson_annual_exposure_vs_events']):+.3f}",
        "time control share": f"{100 * tcs['chd_hot_nights_width_share_of_baseline']:.0f}\\%",
        "cold info share": f"{100 * float(cold['count_weighted_info_share_2013_2018']):.1f}\\%",
        "hot info share": f"{100 * float(hot['count_weighted_info_share_2013_2018']):.1f}\\%",
    }
    missing = {k: v for k, v in claims.items() if v not in memo}
    assert not missing, f"memo out of sync with tables: {missing}"

    print("PASS scripts/test_49_depletion_crucible.py")
    print(f"  memo claims bound to tables: {len(claims)}")
    print(
        "  smooth depletion absorbed: front_loaded R2="
        f"{float(absorb['front_loaded']['r2_absorbed_by_month_plus_ns4']):.5f}"
    )
    print(
        "  same path x residual cold days surviving: "
        f"{float(inter[('front_loaded', 'cold_days')]['share_of_residualised_product_surviving']):.3f}"
    )
    print(
        "  kink surviving controls: "
        f"{float(absorb['covid_kink_0p10_only']['share_surviving_controls']):.3f}"
    )
    print(
        "  CHD latent dip amplitude: "
        f"{summary['covid_kink_inversion']['chd_non_cold_amplitude_mean']:.4f} "
        f"(SD {summary['covid_kink_inversion']['chd_non_cold_amplitude_sd']:.4f})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
