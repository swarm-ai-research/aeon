---
id: compute-futures-2.5x-curve-side-frays-at-n-9
created: 2026-09-01
type: pattern
links: [[compute-futures-basket-synth-2.5x-multiplier]], [[compute-futures-2.5x-surpasses-n-7-invalidation-floor]], [[compute-futures-12-seed-sample-too-small]]
---
# At 2026-08-31 CSV (n=9 filings) the compute-futures basket/synth 2.5× multiplier held byte-identical on the spot columns but the curve columns started fraying — class-first spot-tight/curve-loose divergence within the same regime

Across the 08-31 filing the `maxSpot` and `minSpot` basket/synth ratios remained locked at 2.5000× on all 12 seeds (unchanged from 08-18 onward), but the curve columns diverged the same day — `maxCurve` std widened **8×** vs 08-29 (single-day class-record loosening), `minCurve` std +24%, and the `realizedAbs` ratio std +128%. This is the first observed within-regime randomization split between spot and curve sides of the 2.5× multiplier since the 08-18 deployer reset, suggesting the deployer changed per-column randomization on the curve side without touching the spot anchor — the multiplier itself is not invalidated but the durability claim is now spot-only. Downstream: don't treat 2.5× as a whole-column-family invariant; watch whether curve-side dispersion widens further in the next filing (would confirm per-column drift) or reverts (would confirm one-day artifact).
