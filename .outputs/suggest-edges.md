Working tree clean of source-note edits — only state file + log updated. No PR, no notify per the established templated-corpus pattern.

## Summary

Ran `scripts/suggest-edges.mjs` — day-7 recurrence of `[[suggest-edges-flags-templated-corpora-as-sim-1-noise]]`. Script emitted 3 proposals, all templated-corpus noise from `memory/gitlawb-compute-futures-proofs/` (three sources → `2026-07-17.md` as a newly-rotated-in target, sim 0.981 across the standard cash/darkbloom/synthetic/basket/spread term cluster).

**Actions taken:**
- Reverted source-note edits on the 3 targeted files.
- Moved the 3 `applied` entries to `rejected` in `memory/state/suggest-edges.json` with day-7 reasons.
- Appended a `## suggest-edges run` entry to `memory/logs/2026-08-15.md`.
- **No PR, no notify** (per established pattern — templated corpora shouldn't leave the system).

**State:** 3 applied + 15 rejected (+3/day rejection rate held exactly through day-7).

**Modified files:**
- `memory/state/suggest-edges.json`
- `memory/logs/2026-08-15.md`

**Follow-up (planner-tracked, unchanged):** Patch `scripts/suggest-edges.mjs` to pre-filter shared-parent-directory + shared-basename-shape so templated corpora skip the proposer entirely.
