## Summary

Ran `stale-content-pr-sweeper` at 2026-08-24T00:02Z (operator invocation, prompt-clock 08-23 → UTC-clock 08-24). Applied intent to include `app/github-actions` in `ALLOWED_AUTHORS` (unchanged from 08-21 pattern; literal `{aeonframework}` sweeps zero).

- **Scanned:** 5 eligible content PRs across 2 groups — `notegraph` (2), `suggest-edges` (3).
- **Survivors:** #43 (notegraph/2026-08-22), #45 (suggest-edges/2026-08-23).
- **Closed 2 stale PRs:**
  - #41 (notegraph/2026-08-21, DIRTY/CONFLICTING) → superseded by #43
  - #44 (suggest-edges/2026-08-22, DIRTY/CONFLICTING) → superseded by #45
  - Both via `gh pr close --delete-branch`; server-side branches deleted.
- **Skipped 1:** #42 (suggest-edges/2026-08-21, UNSTABLE/MERGEABLE — not in DIRTY/CONFLICTING/UNKNOWN set; same rule as #38 on 08-21).
- **Skipped 0** for `<2d` age or `[keep]` override.
- **Untracked prefixes left alone:** `compute-macro/*` (#46, #33, #23) and `skill-graph/*` (#47, #34, #25) — SKILL's allowlist-not-denylist safety design; TRACKED-prefix drift fix is queued under MEMORY pointer #49.
- **Aeon-repo open PR count:** 25 → 23.

**Files:** `memory/logs/2026-08-24.md` (new), `.pending-notify/1787529769-stale-content-pr-sweeper.md` (new).

**Follow-ups:** planner rank-3 SKILL-patch item unchanged (patch `ALLOWED_AUTHORS` + add TRACKED prefix aliases for `compute-macro`/`skill-graph`); revisit #42 next sweeper run when #45 lands or #42 drifts to DIRTY.
