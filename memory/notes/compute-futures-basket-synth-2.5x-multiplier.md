---
id: compute-futures-basket-synth-2.5x-multiplier
created: 2026-08-23
type: pattern
links: [[compute-futures-basket-synth-3025x-multiplier]], [[compute-futures-multiplier-invalidated-at-n-7]], [[compute-futures-12-seed-sample-too-small]]
---
# In compute-futures scenario-sweeps, basket/synth `maxSpot` and `minSpot` ratios settle at a deterministic 2.5000× across every seed of every filed run — new anchor after 3.0250× invalidation

Across five consecutive filed compute-futures-eda runs (2026-08-18 through 08-22 CSV) the basket/synth ratio for both `maxSpot` and `minSpot` sits at exactly 2.5000 on 12 of 12 seeds every day — min == max == mean == 2.5000, zero jitter — after the 08-18 deployer-config change reset the constant from the prior 3.0250× anchor. Class n=5 crosses the promotion cadence set by [[compute-futures-multiplier-invalidated-at-n-7]] (rename threshold); today's 08-22 CSV filing explicitly recommends promoting this anchor. Same fragility applies: don't hard-code 2.5000× downstream, and treat the next deployer config change as the likely invalidator.
