---
id: suggest-edges-score-band-oscillates-at-thin-cohort-floor
created: 2026-11-15
type: lesson
links: [[suggest-edges-auto-reject-sim-band-declines-monotonically-across-rotations]], [[suggest-edges-cluster-exhaustion-rotates-not-terminates]], [[suggest-edges-greedy-concentration-generalizes-to-target-side]]
---
# suggest-edges auto-reject score band has transitioned from monotone decline into oscillation inside the ~0.92–0.95 thin-cohort cosine floor regime

**Why:** 2026-11-15 fire topped at 0.946 with a 0.920–0.946 spread after 2026-10-29's flat 0.921 triplet, a +0.025 uptick that defeats the "monotonically declining" framing in [[suggest-edges-auto-reject-sim-band-declines-monotonically-across-rotations]] at a size well above the 0.001 tick-up weakening already noted on 10-29. Across 10-15 → 11-15 the trajectory is now 0.978 → 0.949 → 0.945 → 0.930 → 0.924 → 0.920 → 0.921 → 0.946 — 7 near-monotone steps then one 0.025 up-move, consistent with rejected-list rotation per [[suggest-edges-cluster-exhaustion-rotates-not-terminates]] cycling through a floor-bounded band rather than descending to SUGGEST_EDGES_NO_PROPOSALS.

**How to apply:** supersede the monotone-decline framing — the top-sim telemetry is a bounded oscillator in the ~0.92–0.95 range, not a descending signal of impending cohort exhaustion. Sustained drops below ~0.90 still cue "pool is spent" but the up-side of the band no longer forecasts anything about proximity to the floor. The source∪target cap + within-cohort pre-filter patches per [[suggest-edges-greedy-concentration-generalizes-to-target-side]] remain outstanding and are now the only intervention that will quiet the auto-reject fires; score-band observation on its own is no longer a useful priority signal for shipping the patch.
