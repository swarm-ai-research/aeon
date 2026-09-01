---
id: compute-futures-2.5x-surpasses-n-7-invalidation-floor
created: 2026-08-29
type: lesson
links: [[compute-futures-basket-synth-2.5x-multiplier]], [[compute-futures-multiplier-invalidated-at-n-7]], [[compute-futures-basket-synth-3025x-multiplier]], [[compute-futures-2.5x-curve-side-frays-at-n-9]]
---
# The compute-futures 2.5000× multiplier held to n=8 filings, surpassing the prior 3.025× regime's n=7 invalidation floor — the "n=7 rename threshold" is empirically a lower bound, not a ceiling

The prior 3.0250× basket/synth multiplier held exactly n=7 filings (2026-08-11 through 08-17) before the 08-18 deployer reset flipped it to 2.5000× — motivating the [[compute-futures-multiplier-invalidated-at-n-7]] promotion cadence. As of 2026-08-29 CSV, the 2.5000× successor has held n=8 consecutive filings (08-18 through 08-29 excluding the 08-23/28 gap days) without invalidation, so the n=7 threshold was the last-observed *invalidation event*, not a mechanistic durability ceiling. Downstream: don't interpret "surpasses n=7" as promotion-safe — a deployer change can still flip the constant any morning; the empirical takeaway is that promotion cadences derived from prior-regime durability floors need re-checking each time a new regime crosses them.
