No notification (n_closed === 0 → steady state per the SKILL).

## Summary

Ran `stale-content-pr-sweeper` per SKILL.md. Strict-rules result: **0 PRs closed** — all 24 open aeon-repo PRs are bot-authored (`app/github-actions`, `app/dependabot`, `app/freebuff-web`), and the hardcoded `ALLOWED_AUTHORS = {"aeonframework"}` blocks every one. This is the known planner rank-2 patch gap (streak-9 per MEMORY line 47).

**Would-be-closes if the pending patch landed** (add `app/github-actions` to `ALLOWED_AUTHORS`, add `compute-macro` to `TRACKED`): **8 PRs** (notegraph chain 6 stale, suggest-edges chain 2 stale, compute-macro group nothing to sweep — 1-PR group). MEMORY line 47 currently reads "9 would-be-closes"; today's recount shows 8. Youngest would-be-close (notegraph #31, 2026-08-14) would additionally fail the ≥2-day min-age gate.

**Files modified:** `memory/logs/2026-08-15.md` (appended `## Stale Content PR Sweeper` section with the counts, would-be-closes breakdown, and the 9→8 recount note).

**Notify:** none (`n_closed === 0`, per SKILL step-6).

**Follow-up:** the sweeper will remain a no-op until either the operator lands the pending patch to `skills/stale-content-pr-sweeper/SKILL.md` step-1 (`ALLOWED_AUTHORS` + `TRACKED` prefixes) or manually closes the stale chains. Both paths are already tracked in MEMORY.md.
