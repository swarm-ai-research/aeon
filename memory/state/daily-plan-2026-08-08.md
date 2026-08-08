# Plan — 2026-08-08

**Today's one thing:** Ship the `agi-tracker` `enabled: false` PR on `aeon.yml:188` **today** (Sat) — Mon 2026-08-10 13:00Z is 2 days away and the aeon PR queue **isn't auto-merging** (12 `app/github-actions` PRs sitting >24h post-unblock, oldest #10 from 05:18Z 08-07). I want max review-and-merge window before the 6th silent slot fires.

## Ranked
1. **Land agi-tracker `enabled: false` via PR on `aeon.yml:188`** — planner rank-1 for the 3rd consecutive run (streak-2 under this name, streak-3 counting yesterday's `-direct-edit` framing). Deadline unchanged: Mon 2026-08-10 13:00Z (6th silent slot). Path viable end-to-end since 08-07 unblock; queue depth of 12 shows merges are still manual, so ship today to give operator two full days. Alt: author a real SKILL.md matching [[agi-tracker]] MOC (weekly frontier-agent scoring shape). Same-branch PR from `aeon/agi-tracker-disable-2026-08-08`.
2. **Patch `stale-content-pr-sweeper` `ALLOWED_AUTHORS` to include `app/github-actions`** — 08-07 sweeper log explicitly flagged this: hardcoded `{"aeonframework"}` no longer matches the post-unblock author. Right now no supersessions collide (each date-stamped group has 1 entry), but today's `suggest-edges/2026-08-08` (#21) already makes that group n=2 vs 08-07's #14; tomorrow's `notegraph/2026-08-08` will do the same vs #10. Next same-day rerun will fail to prune the older PR. One-line map extension; ships as PR.
3. **Populate `memory/watched-repos.md` OR disable the 6 dependent skills** — rank-3 carry, streak-3. Yesterday's log shows the 4th same-day short-circuit trio (issue-triage + github-monitor + code-health). Trivial `aeon.yml` edit or one-file create; ships as PR via the same authoring channel now confirmed durable.

## Holding / watching
- **pr-tracker SKILL.md patch batch (9 items, 45d overdue)** — durability now confirmed by 12-PR queue, so this is finally actionable. Deferring until agi-tracker lands so the queue doesn't get another concurrent PR competing for review attention.
- **12-PR queue merge** — pure operator action (`gh pr merge` requires review); not a planner-executable item. If none merge by tomorrow's planner slot, escalate to "queue-depth is an emergent problem post-unblock" rank-1.
- **ISS-006 messages.yml multi-pocket fix** — held, viable now, but subordinate to Mon deadline.
- **`docs/status.md` snapshot-rebase clobber** — 22 days past urgency, 12th consecutive rebase-clobber-then-regen expected at tonight's heartbeat. Non-critical.
- **Mechanism confirmation (Settings toggle vs `AEON_GH_PAT`)** — grep of `.github/workflows/` shows `GH_GLOBAL` PAT already wired (no `AEON_GH_PAT`). Most likely mechanism was the Repo Settings toggle, since `GH_GLOBAL` predates the unblock. Low-value confirmation; not spending a rank on it.
- **swarm-repo App-perm gap** — distinct from aeon-repo, still requires operator App-perm bump or PAT. 26th confirming invocation per [[aeon-app-no-write-on-swarm-repo]]. Out of scope for this planner.

## Fleet note
0 broken · 0 in-flight · 38 DEGRADED (ISS-001 residue day 49, skill-health hash `e27c0ac60367e7e5` 43rd steady-state day) · 4 HEALTHY · 2 NO_DATA (`ai-framework-watch` + `run-frequency-guard` 31st silent day per [[enabled-skills-can-never-dispatch]]) · 18 open issues.

## Source footer
- `memory/MEMORY.md` (60 lines, pointer-only through 08-07 evening reflect; derived priorities from `## Current focus` + `## Pointers` — no `## Goals` section)
- `memory/state/planner-state.json` (last run 2026-08-07T06:35:54Z, top_priority `agi-tracker-enabled-false-via-pr` streak-1)
- `memory/cron-state.json` (42 skills; 0 with cf ≥ 2; 38 with `success_rate < 0.5` all at `last_status=success` per ISS-001 residue; 0 in flight)
- `memory/logs/2026-08-06.md` + `memory/logs/2026-08-07.md` + `memory/logs/2026-08-08.md` (notegraph entry, deterministic no-op)
- `memory/issues/INDEX.md` (18 open, unchanged since ISS-020 filed 08-03)
- `gh pr list --state open` → **13 open** (12 `app/github-actions` + 1 `app/freebuff-web`; 0 `aeonframework`; 0 `dependabot`)
- `gh issue list --state open` → 0 open
