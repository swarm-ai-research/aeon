## Summary

Ran `stale-content-pr-sweeper` on 2026-08-18. Scanned 21 open aeon-repo PRs; **5 matched tracked-prefix + ISO-date** (#37 suggest-edges/2026-08-18, #36 notegraph/2026-08-18, #35 notegraph/2026-08-17, #32 notegraph/2026-08-15, #22 suggest-edges/2026-08-09). **All 5 rejected by the `ALLOWED_AUTHORS = {"aeonframework"}` gate** — every match is authored by `app/github-actions`. Zero groups reached the supersession pass, **0 PRs closed**, notify suppressed (steady-state n_closed === 0). Idempotent no-op **streak-13** for the sweeper allowlist patch already tracked in MEMORY.md Pointers line 47.

Under the patched allowlist (planner rank-3 fix bundle), today's practical outcome would be **2 closes**: #32 notegraph/2026-08-15 → superseded by #36, and #22 suggest-edges/2026-08-09 → superseded by #37; #35 notegraph/2026-08-17 would be skipped by the 2-day min-age gate.

**Files modified:** `memory/logs/2026-08-18.md` (Stale Content PR Sweeper section appended).

**Follow-up:** unchanged — land the `ALLOWED_AUTHORS ∪ {"app/github-actions"}` + `TRACKED ∪ {"compute-macro"}` patch (planner rank-3, streak-13) to make this skill do actual work; also reconcile MEMORY.md line 47 to reflect today's advance (streak-12 → 13).
