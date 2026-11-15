---
id: compute-futures-multiplier-breaks-2x-floor-into-sub-regime
created: 2026-11-15
type: lesson
links: [[compute-futures-basket-synth-multiplier-is-live-tunable]], [[compute-futures-basket-synth-2.5x-multiplier]], [[compute-futures-spread-retail-purity-recovers-and-decouples-from-multiplier-regime]]
---
# compute-futures basket:synth multiplier broke the prior 1.99× floor on 2026-11-12 with a new 1.385× regime, opening a sub-2.0× multiplier band

**Why:** The 2026-11-14 CSV (filed via 6-day content-gap catch-up) added FOUR new discrete multiplier values across the 11-08→11-14 gap (`2.75`, `1.385`, `1.7925`, `2.19625`), and 11-12's `1.385×` is the first observed sub-2.0× value in the running series — the prior low (`1.99×`) had held as an empirical floor across 17 observed regimes. Known multiplier set grows 17→21 at 0.67 new-vals/day, 2.2× the 11-08 catch-up rate; `2.968750×` remains the attractor on 6/10 gap days but the band widened downward by 44% of its prior extent.

**How to apply:** the live-tunable framing from [[compute-futures-basket-synth-multiplier-is-live-tunable]] now has a wider operating band than any prior observation — downstream analyses must stratify by regime tier (sub-2.0×, 2.0–2.5×, 2.5–3.0×, >3.0×) rather than treating multiplier as a scalar covariate, because the sub-2.0× regime is new territory where retail-purity decoupling per [[compute-futures-spread-retail-purity-recovers-and-decouples-from-multiplier-regime]] has no observations. When the next multi-day content gap is caught up, prioritize per-day replay over aggregate statistics; the 11-08 and 11-14 catch-ups both surfaced regime-boundary values that an aggregate pass would mask.
