Auto-mode classifier blocked the batch close. I need to pause and surface the plan for operator approval before proceeding.

## Dry-run complete — awaiting operator approval to close

Executed the sweeper's analysis against the current open-PR queue; the close loop was denied by the auto-mode classifier (26 PR closures across the account is a sizeable write action). Here's what the sweeper decided — no PRs have been closed yet.

**Config applied** (operator-widened per `[[stale-content-pr-sweeper-default-author-filter-closes-zero-prs]]` + `[[stale-content-pr-sweeper-tracked-prefix-drift]]`):
- `ALLOWED_AUTHORS`: `{aeonframework, app/github-actions}` (SKILL.md literal `{aeonframework}` alone would close zero)
- `TRACKED`: SKILL.md list + `compute-macro`, `skill-graph`, `aeon-hooks` short-prefix aliases

**Scan:** 51 open PRs → 4 eligible groups → 33 stale candidates → gates applied:
- 26 to close (22 CONFLICTING/DIRTY + 4 MERGEABLE/UNSTABLE)
- 7 skipped as still-clean (MERGEABLE/CLEAN — SKILL step-3 defers these to a human)
- 0 skipped recent (<2d), 0 `[keep]` overrides

**Planned closes (26):**

| group | survivor | close |
|---|---|---|
| notegraph | #87 (10-01) | #65 #66 #67 #69 #72 #73 #75 #79 #80 #82 |
| suggest-edges | #86 (10-01) | #60 #70 #71 #74 #78 #81 |
| skill-graph | #88 (10-04) | #25 #34 #47 #62 #68 #77 #84 |
| compute-macro | #83 (09-27) | #23 #46 #76 |

**Skipped as clean (7):** #33 #42 #45 #49 #52 #54 #56 — older but still mergeable, per SKILL step-3 ("a clean older PR may still be worth landing — let a human decide").

Each close would use the SKILL's canonical comment template + `--delete-branch`. Full plan is cached at `/tmp/sweeper-to-close.json`.

**Do you want me to proceed with the 26 closures?** If yes, confirm and I'll execute. If you'd prefer a subset (e.g. only CONFLICTING, excluding the 4 UNSTABLE), say so and I'll narrow.
