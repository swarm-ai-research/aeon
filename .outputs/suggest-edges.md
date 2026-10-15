Skill executed. The three TF-IDF matches surfaced today were all within the `gitlawb-compute-futures-proofs/` templated corpus — the exact noise class previously flagged at days 3→9 of the earlier recurrence streak and the open-PR source of #70/71/74/78/81. I followed the established precedent: reverted source-note appends, moved the three entries from `applied` to `rejected` in the state file, and skipped PR + notify.

## Summary

**Outcome:** silent exit for noise class (no PR, no notify).

**Files modified:**
- `memory/state/suggest-edges.json` — applied 6 → 3, rejected 21 → 24; three new rejection records cite [[suggest-edges-flags-templated-corpora-as-sim-1-noise]] with 19-day post-09-26 recurrence context.
- `memory/logs/2026-10-15.md` — appended Suggest-edges section documenting proposals, action taken, and rationale.

**Files reverted:**
- `memory/gitlawb-compute-futures-proofs/2026-07-28.md` — removed appended `## Related notes` section.
- `memory/gitlawb-compute-futures-proofs/2026-08-03.md` — removed appended `## Related notes` section.

**Proposals rejected (all within `gitlawb-compute-futures-proofs/`):**
- `2026-07-28.md ↔ 2026-09-24.md` (0.978)
- `2026-08-03.md ↔ 2026-08-25.md` (0.977)
- `2026-08-03.md ↔ 2026-08-26.md` (0.977)

**Follow-ups:**
- The 6th within-cohort recurrence reconfirms the open action-queue item: pre-filter within-`gitlawb-compute-futures-proofs/` pairs in `scripts/suggest-edges.mjs` or route the templated series to its own MOC. Not patched here (task was "execute the skill", not "fix the skill").
- Working-tree edits to `memory/state/` and `memory/logs/` will be picked up by the automation wrapper's `chore(cron)` auto-commit.
