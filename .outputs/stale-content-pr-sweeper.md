Ran `stale-content-pr-sweeper` per SKILL.md. Following the skill literally:

## Summary
- **Scanned:** 23 open PRs via `gh pr list`.
- **TRACKED-prefix + date-suffix matches:** 10 PRs (notegraph #10/#27/#28/#29/#30/#31, suggest-edges #14/#21/#22 — plus #23 `compute-macro/...` which fails TRACKED because SKILL lists full name `compute-macro-correlate`).
- **Passed `ALLOWED_AUTHORS = {"aeonframework"}`:** **0** — all 10 are authored by `app/github-actions` (bot).
- **Closures:** 0 PRs closed, 0 branches deleted.
- **Notify:** suppressed per SKILL step-6 "n_closed === 0 → no notify" rule.
- **Counterfactual (if the known-blocked allowlist patch landed):** 6 sweepable PRs today — notegraph #29/#28/#27/#10 + suggest-edges #21/#14 (chain lengths: notegraph 6, suggest-edges 3). #30 (08-13) blocked by <2d min-age gate.
- **Files modified:** `memory/logs/2026-08-14.md` (log entry only).
- **Follow-up:** planner rank-2 (streak-8) unchanged — SKILL.md needs `"app/github-actions"` in `ALLOWED_AUTHORS` and `"compute-macro"` added to `TRACKED` per MEMORY.md line 47.
