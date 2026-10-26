---
id: suggest-edges-greedy-concentration-crosses-source-target-within-one-batch
created: 2026-10-26
type: lesson
links: [[suggest-edges-greedy-concentration-generalizes-to-target-side]], [[suggest-edges-greedy-concentrates-on-single-source-under-cohort-exhaustion]], [[suggest-edges-flags-templated-corpora-as-sim-1-noise]]
---
# suggest-edges greedy walk can concentrate on a single node across source/target orientations within one 3-pair batch

**Why:** 2026-10-26 fire (11th within-cohort auto-reject, series n=6) produced three proposals where `2026-08-03.md` appeared **as both source (pair #3: `2026-08-03 → 2026-08-09`) and target (pair #1: `2026-07-07 → 2026-08-03`)** inside the same 3-pair batch. This is distinct from 10-18's single-source clustering (one dominant source, 3 distinct targets) and 10-25's single-target clustering (one dominant target, 3 distinct sources) per [[suggest-edges-greedy-concentration-generalizes-to-target-side]] — those observations spanned different fires on the same mechanism; today's shows the mechanism can act *within* a single batch by picking the same node once as source and once as target when its cross-slot partner inventory dominates.

**How to apply:** the symmetric per-node cap floated in [[suggest-edges-greedy-concentration-generalizes-to-target-side]] must be enforced across the **union** of source and target slots within one run, not per-slot. A cap that counts source-appearances and target-appearances in separate buckets would still pass today's fire (`2026-08-03.md` appears 1× as source and 1× as target — both under a per-slot `≤1` cap) while the pathology is intact. The patch spec sharpens to: for each run, build a bag of all node slugs across all proposals' source and target fields; drop any proposal whose source OR target would push a bag count above 1.
