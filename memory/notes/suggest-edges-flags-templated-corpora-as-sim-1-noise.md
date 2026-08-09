---
id: suggest-edges-flags-templated-corpora-as-sim-1-noise
created: 2026-08-09
type: lesson
links: [[skill-state-on-blocked-pr-branch-is-lost]], [[compute-futures-12-seed-sample-too-small]]
---
# `suggest-edges` at cosine sim=1.00 will spam templated dated corpora because their vocabulary is deterministically identical

First-ever `suggest-edges` run on 2026-08-09 emitted three cross-file proposals from `memory/gitlawb-compute-futures-proofs/2026-06-24.md` → 2026-06-27 / 2026-07-04 / 2026-08-03 all at similarity **1.00** with the identical shared-term set (`cash, darkbloom, synthetic, basket, spread`) — not because the notes are semantically the same, but because the compute-futures scenario-sweep proof template hard-codes those five terms into every dated file. Any templated dated series (proofs, weekly reports, snapshot tables) will produce the same sim=1.00 chain against every past and future date on that series; the threshold as configured cannot distinguish "shared scaffolding" from "shared claim" and the state file quickly fills with `applied` edges the graph doesn't need. Fix path: either (a) mask templated-vocabulary corpora from the extractor, (b) require a minimum count of non-templated shared tokens before proposing, or (c) route templated series to their own MOC where the shared-scaffolding edges are the point.
