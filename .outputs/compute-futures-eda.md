## Summary

Ran the `compute-futures-eda` skill against the freshest deployer proof (`memory/gitlawb-compute-futures-proofs/2026-07-10.csv`).

**Files:**
- created `memory/topics/compute-futures-eda/2026-07-10.md` (findings summary)
- created `memory/logs/2026-07-11.md` (daily log entry)
- created `.pending-notify/1783752083-compute-futures-eda.md` (notification for post-run delivery)
- ran EDA scripts into `out/programmatic-eda/compute-futures-2026-07-10/`
- committed to main: `380b61c chore(compute-futures-eda): findings 2026-07-10`

**Top findings (2026-07-10 sweep, 144 rows, 4 modes):**
1. **[MEDIUM] basket `settlementLegs` 25%** — 9/36 outside IQR [76.8, 82.8] (3×73, 6×83); first fire for this (mode, column) since 06-28. Alarm-without-signal until it repeats.
2. **[MEDIUM] spread `minSpot` 16.67%** — 6/36 low-tail rows below $41.10 whisker; first-ever fire in the run window.
3. **[LOW] Yesterday's `x402 wallet_sum_pnl × x402Total` +0.881 → +0.088** — third consecutive-day validation of [[compute-futures-eda-wallet-sum-pnl-correlations-are-float-dust]]. **Zero |r|≥0.8 pairs today** (first zero-crossing run since 07-07).
4. **[PASS] Conservation healthy in every mode** (all 12+ orders below gates); schema intact; synthetic ≡ x402 role-level max|diff|=0.0 reconfirmed.

**Follow-ups:** watch basket `settlementLegs` and spread `minSpot` tomorrow — if either recurs >10%, escalate from alarm-without-signal to signal candidate.
