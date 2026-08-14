---
id: compute-futures-basket-synth-3025x-multiplier
created: 2026-08-14
type: pattern
links: [[compute-futures-spread-retail-loss-concentration]], [[compute-futures-12-seed-sample-too-small]], [[compute-futures-seed-padding-bug]]
---
# In compute-futures scenario-sweeps, basket/synth `maxSpot` and `minSpot` ratios are a deterministic 3.0250× across every seed of every filed run

Across four consecutive filed compute-futures-eda runs (2026-08-10, 08-11, 08-12, 08-13) the basket/synth ratio for both `maxSpot` and `minSpot` is exactly 3.0250 on 12 of 12 seeds every day — min == max == mean == 3.0250, zero jitter. `maxCurve` / `minCurve` / `realizedAbs` ratios sit near 3.02 but with per-seed spread (~3.00–3.44), so the constant lives specifically in the spot columns; it is not an artifact of the 12-seed sample cap flagged by [[compute-futures-12-seed-sample-too-small]], since a deterministic-across-seeds constant survives any n. Meets the n=3 promotion criterion (hit on 08-12) and is now confirmed at n=4 — treat basket-mode spot columns as `3.0250 × synth-mode` upstream and drop redundant reporting from EDA outputs.
