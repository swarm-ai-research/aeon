---
id: compute-futures-eda-wallet-sum-pnl-correlations-are-float-dust
created: 2026-07-09
type: lesson
links: [[compute-futures-12-seed-sample-too-small]], [[compute-futures-seed-padding-bug]]
---
# compute-futures-eda |r|≥0.8 crossings involving `wallet_sum_pnl` are float-dust artifacts of settlement volume, not P&L signal

The `wallet_sum_pnl` column carries σ ≈ 6e-12 (conservation-preserved sum of a zero-sum ledger), so any correlation between it and a volume-scale column (`settlementLegs`, `realizedAbs`, `x402Total`) reflects float-dust cancellation ordering, not strategy P&L structure — the numerator is dominated by rounding noise while the denominator is real. Observed twice in 3 days: 07-07 spread `realizedAbs × wallet_sum_pnl` r = −0.752 (near-leader) collapsed to +0.190 on 07-08; 07-09 synthetic/x402 `wallet_sum_pnl × settlementLegs` r = −0.874 (first-ever |r|≥0.8 crossing in the run window), expected to collapse on the next 12-seed rotation. Interpretation rule: **drop any wallet_sum_pnl-column |r| finding from the LOW/MEDIUM/HIGH ladder unless σ(wallet_sum_pnl) > 1e-6** — otherwise it is guaranteed to self-clear and trains the reader to ignore genuine signal.
