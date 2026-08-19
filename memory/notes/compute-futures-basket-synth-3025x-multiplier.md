---
id: compute-futures-basket-synth-3025x-multiplier
created: 2026-08-14
updated: 2026-08-19
type: pattern
status: superseded
links: [[compute-futures-multiplier-invalidated-at-n-7]], [[compute-futures-spread-retail-loss-concentration]], [[compute-futures-12-seed-sample-too-small]], [[compute-futures-seed-padding-bug]]
---
# In compute-futures scenario-sweeps, basket/synth `maxSpot` and `minSpot` ratios are a deterministic 3.0250× across every seed of every filed run — INVALIDATED 2026-08-18

Across seven consecutive filed compute-futures-eda runs (2026-08-10 through 08-17) the basket/synth ratio for both `maxSpot` and `minSpot` was exactly 3.0250 on 12 of 12 seeds every day — min == max == mean == 3.0250, zero jitter. **On 2026-08-18 the multiplier broke to 2.5000× and held at 2.5000× on 08-19 (n=2 at the new value)** — an upstream deployer config change reset the constant without touching schema; see [[compute-futures-multiplier-invalidated-at-n-7]] for the promotion-criterion lesson. Treat this note as historical: don't hard-code 3.0250× downstream.
