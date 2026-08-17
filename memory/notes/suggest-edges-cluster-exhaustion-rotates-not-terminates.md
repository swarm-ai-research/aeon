---
id: suggest-edges-cluster-exhaustion-rotates-not-terminates
created: 2026-08-17
type: lesson
links: [[suggest-edges-flags-templated-corpora-as-sim-1-noise]], [[skill-state-on-blocked-pr-branch-is-lost]]
---
# Rejecting one templated-corpus triple does not drain the greedy top-3 — a second cluster rotates in the same corpus

Days 3–8 of the 2026-08 `suggest-edges` templated-corpus streak locked on source triple `{06-24, 06-27, 07-04}` × shared terms `[cash, darkbloom, synthetic, basket, spread]`, target date advancing daily; on 2026-08-17 (day 9) the greedy top-3 rotated onto a completely different in-corpus triple `{05-25, 05-26, 05-27}` × shared terms `[sha, settlement, task, physical, cash]` at sim 1.000, all three pair-edges internal to the new triple. Rejecting each combination of the first triple did not exhaust the noise class — the greedy planner surfaces the next-highest-scoring cluster from the same `gitlawb-compute-futures-proofs/` subtree once the prior cluster's cross-combos land in state. Fix path: the pre-filter in `scripts/suggest-edges.mjs` must catch any within-subtree pair sharing a scenario-sweep tokenization signature, not blacklist a specific triple; single-cluster hardcode skips guarantee day-N+1 rotation.
