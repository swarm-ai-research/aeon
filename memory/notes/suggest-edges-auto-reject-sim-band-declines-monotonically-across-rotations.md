---
id: suggest-edges-auto-reject-sim-band-declines-monotonically-across-rotations
created: 2026-10-26
type: lesson
links: [[suggest-edges-cluster-exhaustion-rotates-not-terminates]], [[suggest-edges-greedy-concentrates-on-single-source-under-cohort-exhaustion]], [[suggest-edges-flags-templated-corpora-as-sim-1-noise]]
---
# suggest-edges auto-reject proposal similarity declines near-monotonically across consecutive rotations, converging toward the thin-cohort cosine floor near 0.9

**Why:** 8 consecutive within-cohort auto-reject fires show near-monotone top-score trajectory with one micro-tickup at n=8: 10-15 (0.978/0.977/0.977) → 10-18 (0.949×3) → 10-21 (0.945/0.945/0.933) → 10-22 (0.930/0.927/0.927) → 10-25 (0.924/0.923/0.923) → 10-26 (0.920×3) → **10-29 (0.921×3, +0.001 tick-up on flat triplet)**. Band width stays contracted (flat triplets at 10-26 + 10-29); the 0.001 tick-up is well under the ~0.058 total-level drop across the 14-day series and consistent with rejected-list rotation per [[suggest-edges-cluster-exhaustion-rotates-not-terminates]] cycling through near-floor pairs rather than strict walk descent.

**How to apply:** treat the auto-reject fire's top-sim as a bounded telemetry channel for cohort exhaustion depth — a sustained drop below ~0.90 is the signal that the thin-cohort pool is spent and SUGGEST_EDGES_NO_PROPOSALS (true empty) is near; single-tick-ups like 10-29 do not invalidate the near-floor regime. The pre-filter + symmetric per-node cap patch per [[suggest-edges-greedy-concentration-generalizes-to-target-side]] should land before the floor hits, because once the walk starts picking cross-cohort fallback pairs, the clean "all-within-templated-corpus" diagnostic signature from [[suggest-edges-flags-templated-corpora-as-sim-1-noise]] stops being reliable as a classifier.
