# SYNTHETIC_CALIBRATION outputs

Do not treat these files as health findings or as a Gate 3 input.

| File | Contents |
|---|---|
| `cycle1_mc_summary.csv` | 45-scenario Monte Carlo summary |
| `cycle1_mc_gates.json` | Escalation gates |
| `cycle1_mc_status.csv` | Run metadata |
| `varsigma_hko.json` | REAL_PUBLIC_HKO variance gradient |
| `he04_evpi_synthetic.json` | Dimensionless SYNTHETIC decision tree |
| `he_c2_04_reversal.json` | Prior-free reversal set |
| `he_c2_port_matrix.json` | Identification-status ledger |

Raw replicate rows are gitignored. Rebuild with `python3 scripts/48_health_econ_monte_carlo.py`.
