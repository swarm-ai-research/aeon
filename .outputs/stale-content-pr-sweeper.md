## Summary

Ran `stale-content-pr-sweeper` on 2026-08-21. Aeon-repo queue was 26 open PRs; scanned the two tracked-prefix groups (`notegraph`, `suggest-edges`), picked #41/#42 as today's survivors, applied the SKILL's age + conflict + `[keep]` gates to the 8 remaining candidates.

**Closed 5 stale PRs** (all DIRTY/CONFLICTING, all with supersession comments + branch deletion):
- notegraph: #36 (08-18), #35 (08-17), #32 (08-15) → superseded by #41
- suggest-edges: #37 (08-18), #22 (08-09) → superseded by #42

**Skipped 3:**
- #39, #40 — too recent (1d, under the ≥2d gate)
- #38 — `UNSTABLE`/`MERGEABLE` (not in the DIRTY/CONFLICTING/UNKNOWN set the SKILL's stricter sentence names)

**Left alone (out of TRACKED prefix):** `compute-macro/*` (#33, #23), `skill-graph/*` (#34, #25) — per SKILL's allowlist-not-denylist safety design; the pending TRACKED-prefix drift patch (MEMORY pointer #47) belongs on the SKILL-edit PR, not on today's sweep.

**Author-allowlist note:** all these bot PRs are authored by `app/github-actions`, not `aeonframework`. Executed with the SKILL's stated intent ("or whatever GH identity opens cron PRs") rather than the literal `{"aeonframework"}` in the code snippet — a well-known standing SKILL bug per MEMORY pointer #47.

**Files modified:** `memory/logs/2026-08-21.md` (sweeper entry appended), `.pending-notify/1787356222-stale-content-pr-sweeper.md` (new — notify sent since n_closed > 0). Aeon-repo open PR count 26 → 21. Exit: `SWEEPER_OK`.
