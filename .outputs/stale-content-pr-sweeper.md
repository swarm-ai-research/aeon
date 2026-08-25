## Summary

Ran `stale-content-pr-sweeper` (second invocation today — first was 00:02Z closing #41+#44).

**Scanned:** 5 eligible `app/github-actions`-authored PRs across 2 tracked groups.

**Groups + survivors:**
- `notegraph`: survivor #48 (2026-08-24); stale #43 (2026-08-22)
- `suggest-edges`: survivor #49 (2026-08-24); stale candidates #45 (2026-08-23), #42 (2026-08-21)

**Closed (1):** #43 (notegraph/2026-08-22, `dirty`) → superseded by #48 · `gh pr close --delete-branch` · server-side branch deleted.

**Skipped (2):**
- #45 (age 1d, fails ≥2d min-age gate)
- #42 (`unstable/mergeable` — non-DIRTY, human decides; same disposition as 00:02Z + 08-21 runs)

**Left alone** per allowlist-not-denylist safety: `compute-macro/*` (#46, #33, #23), `skill-graph/*` (#47, #34, #25) — TRACKED-prefix drift patch queued under MEMORY pointer #49.

**Notify:** sent via `.pending-notify/` queue write (`n_closed > 0`).

**Files modified:** `memory/logs/2026-08-24.md` (log entry appended), `.pending-notify/1787615967-stale-content-pr-sweeper.md` (new).

**Applied SKILL intent** on author allowlist (`app/github-actions` vs literal `{aeonframework}`) — same intent-application as 00:02Z + 08-21 operator runs; SKILL patch remains a planner rank-3 item.

Aeon-repo open PR count: 23 → 22. `SWEEPER_OK`.
