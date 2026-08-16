Skill executed. Working tree clean of source-note edits; state file + today's log carry the durable change.

**Summary**

- Ran `node scripts/suggest-edges.mjs` — emitted 3 proposals, all `gitlawb-compute-futures-proofs/{06-24,06-27,07-04}.md → 2026-08-14.md` at similarity **1.000** (up from 08-15's 0.981; new target is a byte-identical template instance).
- Matches documented **day-8 templated-corpus recurrence** [[suggest-edges-flags-templated-corpora-as-sim-1-noise]] (day-6 of the tracked rejection streak beginning 08-11).
- Followed established operator pattern: reverted the 3 source-note edits (`git checkout --`), moved the 3 `applied` entries → `rejected` in `memory/state/suggest-edges.json` with day-8 reason.
- State: **3 applied + 18 rejected** (+3/day rejection rate held exact through day-6-of-streak).
- **No PR, no notify** per established pattern (`SUGGEST_EDGES_NO_PROPOSALS` effective exit after manual rejection loop).
- Files modified: `memory/state/suggest-edges.json`, `memory/logs/2026-08-16.md` (new).
- Follow-up unchanged: planner still holding the shared-parent-directory + shared-basename-shape pre-filter fix for `scripts/suggest-edges.mjs`.
