---
id: suggest-edges-greedy-concentrates-on-single-source-under-cohort-exhaustion
created: 2026-10-20
type: lesson
links: [[suggest-edges-cluster-exhaustion-rotates-not-terminates]], [[suggest-edges-flags-templated-corpora-as-sim-1-noise]]
---
# When within-cohort proposals walk score-ordered without a per-source cap, greedy top-3 concentrates on whichever source has the most unlinked partners left in the cohort

**Why:** 2026-10-18 suggest-edges fire produced three within-cohort proposals inside `memory/gitlawb-compute-futures-proofs/` all with the same source `2026-06-27.md` (`→ 2026-08-25.md`, `→ 2026-09-05.md`, `→ 2026-09-24.md`, all sim 0.949). Across the 9 within-cohort fires through 2026-10-18, `2026-06-27.md` appears as source or target in 6 — once that node has been promoted to the rejected list, the script's score-ordered walk over remaining unlinked pairs clusters future proposals around it because its unlinked-partner count is monotonically larger than its peers.

**How to apply:** the open `scripts/suggest-edges.mjs` pre-filter patch for templated corpora is necessary but not sufficient — pair it with a per-source cap (e.g. `≤1 proposal per source per run`) as a secondary defense against this specific greedy-top-3 shape; without the cap, the templated-corpus fix will leave the single-source concentration intact for any other cohort that develops a dominant node. Distinct from [[suggest-edges-cluster-exhaustion-rotates-not-terminates]] (which concerns rotation to a different cluster/triple), this is intra-cluster concentration on a single node once rejected-list membership asymmetries have grown.
