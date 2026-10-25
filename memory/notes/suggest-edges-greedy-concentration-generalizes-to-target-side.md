---
id: suggest-edges-greedy-concentration-generalizes-to-target-side
created: 2026-10-25
type: lesson
links: [[suggest-edges-greedy-concentrates-on-single-source-under-cohort-exhaustion]], [[suggest-edges-cluster-exhaustion-rotates-not-terminates]], [[suggest-edges-flags-templated-corpora-as-sim-1-noise]]
---
# suggest-edges greedy concentration is side-agnostic — it clusters on whichever node (source OR target) has the most unlinked partners remaining in the cohort, not specifically the source

**Why:** 2026-10-25 suggest-edges fire (10th within-cohort, 5th consecutive auto-reject) produced three proposals inside `memory/gitlawb-compute-futures-proofs/` with **three distinct sources** (`2026-08-22.md`, `2026-06-27.md`, `2026-08-03.md`) but new target `2026-08-31.md` appeared **2×** out of 3 (proposals 1 + 2) — the mirror image of 2026-10-18's single-source clustering (`2026-06-27.md` as source in all 3 proposals). Both fires fit the same mechanism from [[suggest-edges-greedy-concentrates-on-single-source-under-cohort-exhaustion]]: the greedy score-ordered walk picks the top-3 pairs by similarity and whichever node has accumulated the most rejected-list memberships has monotonically more unlinked partners left; which *side* that node sits on is incidental.

**How to apply:** the per-source cap floated in [[suggest-edges-greedy-concentrates-on-single-source-under-cohort-exhaustion]] is only half the fix — the SKILL patch must land a symmetric **per-node cap** (`≤1 proposal per node, source or target, per run`) alongside the templated-corpus pre-filter. A source-only cap would have passed today's fire untouched because no source repeats, yet the proposal set still exhibits the pathology; the generalization defeats that false-sense-of-safety. Score band (0.923–0.924) is below both the 09-26 cluster (0.945–0.978) and the 2026-08 sim≈1.00 cluster, consistent with cohort exhaustion driving the walk to lower-score pairs.
