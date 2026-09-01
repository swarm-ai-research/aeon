---
id: compute-futures-basket-synth-2.5x-multiplier
created: 2026-08-23
type: pattern
links: [[compute-futures-basket-synth-3025x-multiplier]], [[compute-futures-multiplier-invalidated-at-n-7]], [[compute-futures-2.5x-surpasses-n-7-invalidation-floor]], [[compute-futures-12-seed-sample-too-small]]
---
# In compute-futures scenario-sweeps, basket/synth `maxSpot` and `minSpot` ratios settle at a deterministic 2.5000× across every seed of every filed run — new anchor after 3.0250× invalidation

Across nine consecutive filed compute-futures-eda runs (2026-08-18 through 08-31 CSV) the basket/synth ratio for both `maxSpot` and `minSpot` sits at exactly 2.5000 on 12 of 12 seeds every day — min == max == mean == 2.5000, zero jitter — after the 08-18 deployer-config change reset the constant from the prior 3.0250× anchor. Class n=9 now surpasses the n=7 invalidation-cadence floor set by the prior 3.0250× regime — see [[compute-futures-2.5x-surpasses-n-7-invalidation-floor]] for the durability implication, and [[compute-futures-2.5x-curve-side-frays-at-n-9]] for the class-first spot-tight/curve-loose divergence starting 08-31. Same fragility applies: don't hard-code 2.5000× downstream, treat the curve columns as unstable within the regime, and treat the next deployer config change as the likely spot-side invalidator.
