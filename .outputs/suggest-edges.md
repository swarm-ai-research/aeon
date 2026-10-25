## Summary

Executed `skills/suggest-edges/SKILL.md`. The script surfaced 3 proposals, all within the `memory/gitlawb-compute-futures-proofs/` templated corpus (sim 0.923–0.924) — matching the auto-reject pattern established 10-15/10-18/10-21/10-22. This is the **10th within-cohort fire** post-last-PR.

**Actions taken:**
- Reverted `memory/gitlawb-compute-futures-proofs/{2026-06-27,2026-08-03,2026-08-22}.md` via `git checkout`.
- Moved the 3 just-applied entries from `applied` → `rejected` in `memory/state/suggest-edges.json` with rejection reason tagged (series n=5 of auto-reject regime; 10th within-cohort fire; 29 days post-09-26).
- Logged activity to `memory/logs/2026-10-25.md`.

**No PR, no notify** — expected silence on templated-corpus auto-reject per MEMORY.md guidance.

**State counters:** applied 6→3, rejected 33→36.

**Target-concentration variant observed:** 3 distinct sources but target `2026-08-31` appears 2× — mirror of the single-source clustering noted on 10-18; reinforces the per-source cap (and per-target cap) follow-up still owed on `scripts/suggest-edges.mjs`.

**Files modified:** `memory/state/suggest-edges.json`, `memory/logs/2026-10-25.md` (new).

**Follow-up (unchanged):** within-cohort pre-filter + per-source cap in `scripts/suggest-edges.mjs` — the auto-reject regime is now n=5 across 10 days, each run paying full script runtime + manual reversion cost.
