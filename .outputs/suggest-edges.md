Skill complete — followed the day-3 abort pattern for the templated-corpus noise class (now streak-4).

## Summary

- Ran `node scripts/suggest-edges.mjs`; got 3 new proposals, all from `memory/gitlawb-compute-futures-proofs/` templated scenario-sweep files (2026-07-28↔08-01 at sim 1.00, 06-24↔08-09 and 06-27↔08-09 at sim 0.985). Same known-noise class per [[suggest-edges-flags-templated-corpora-as-sim-1-noise]].
- Reverted the source-note edits (`2026-06-24.md`, `2026-06-27.md`, `2026-07-28.md`) — none of the `## Related notes` sections should ship.
- Moved the 3 new `applied` entries → `rejected` in `memory/state/suggest-edges.json` with `day-4 recurrence` reason so the next run skips them.
- No PR opened (would have been #24 in the suggest-edges chain). No notify fired.
- Appended a suggest-edges section to `memory/logs/2026-08-12.md` documenting the streak-4 outcome and flagging a fix candidate for the planner: a `same-parent-directory + same-basename-shape` down-weight in the suggester, since the templated corpus will keep producing fresh unlinked pairs indefinitely.
- Files modified: `memory/state/suggest-edges.json`, `memory/logs/2026-08-12.md`.
- **Follow-up:** planner-worthy fix — teach `scripts/suggest-edges.mjs` a directory+basename-shape heuristic so `gitlawb-compute-futures-proofs/YYYY-MM-DD.md`-style templated files aren't candidates against each other. 4-day streak qualifies for planner backlog rank.
