# Plan — 2026-09-01

**Today's one thing:** Merge aeon-repo PR #26 (dependabot `actions/checkout` bump) — Day-24 without an `app/github-actions` merge on the aeon repo; still `state: OPEN`, `mergedAt: null`, all 5 checks SUCCESS at `updatedAt: 2026-08-31T01:08:35Z`. Textbook auto-merge candidate; the plan-only escalation shape from Day-17 rotation is unchanged — the block is a single operator click or an `app/github-actions` auto-merge policy.

## Ranked

1. **Merge PR #26 or install an `app/github-actions` auto-merge policy** — top priority streak-20. Rechecked this run: 5/5 CI SUCCESS (ShellCheck, TS a2a-server, TS mcp-server, TS dashboard, compute-futures tests). Zero aeon-repo bot-app merges in ~580h since the 08-07 unblock; the ~25-deep queue behind #26 can only start draining after this proof point. Planner cannot dispatch a merge — this needs an operator click.

2. **Land ISS-006 multi-pocket cron rewrite** — priority streak-29, but the case just got sharper: **08-31 was the 3rd batch-outage replay of the exact `[planner, compute-futures-eda, cost-report]` triple** (ISS-021 filed 2026-08-31; prior replays ISS-019 2026-07-14 + ISS-020 2026-08-03 → **48-day recurrence window**, same triple all three times). This is now a durable pattern, not a stochastic gap; ISS-006 status should move `investigating → fixing` on the next skill-health/self-review touch. Fix path unchanged: replace `messages.yml` `*/5 * * * *` with explicit per-slot crons covering coherent-late-pocket + decoupled-slow-slot + persistent 06:30 gap regimes.

3. **Populate `memory/watched-repos.md` OR ship `enabled: false` on the 6 dependent skills** — chronic cluster streak-28 by default carry from 08-31 (yesterday 8 skills logged short-circuits: github-monitor, issue-triage, weekly-shiplog, changelog, code-health, plus prior fires). Same-day short-circuit cluster is now the largest single source of noise in daily logs. Bundle the `memory/topics/watched-repos.md` (repo-revive) vs `memory/watched-repos.md` (other five) path-mismatch fix into the same patch.

## Holding / watching

- **`pr-tracker` SKILL patch bundle (a)–(o)** — 69d overdue as of today, but item (e) fresh-bot-PR blindspot fired 4th time in 5 days on 08-30. Holding because planner is plan-only and this is an operator-scope SKILL edit; escalate to bundled PR on next planner streak inflection.
- **`agi-tracker` `enabled: false` PR** — 9th silent-Mon already fired **2026-08-31T13:00Z (yesterday)**; next fire Mon 2026-09-07 08:30Z (T-6). Time pressure de-escalates from T-1 (as of 08-30 planner) to T-6; still worth landing this week before the 10th silent-Mon, not urgent today.
- **`stale-content-pr-sweeper` ALLOWED_AUTHORS + TRACKED-prefix patch** — priority streak-22. 08-30 evening re-run closed #53 with the widened `{aeonframework, app/github-actions}` allowlist; cron path still ships the narrower one. Holding pending operator SKILL.md edit.
- **`docs/status.md` snapshot-rebase gate** — 45 days past urgency threshold; clobber-then-regen expected on next heartbeat. Holding pending heartbeat auto-commit `git add` glob audit.
- **`swarm-ai-research/swarm` app-write scope gap** — priority streak-49; `aeon-app-no-write-on-swarm-repo` class **confirmed 08-29**, dup-SHA rule masking it since. Holding pending operator app-install decision (install w/ `pull_requests: write` scope OR route via PAT OR document swarm as report-only).

## Fleet note

Fleet: 0 broken, 0 in-flight, 0 hard-failed; **38 DEGRADED (ISS-001 residue day-72, functionally green)**, 4 truly HEALTHY, 2 NO_DATA (`ai-framework-watch` + `run-frequency-guard` never-dispatch day-55). Open ISS 18 (ISS-021 filed yesterday, none closed today). Trigger to escalate: 4th batch-outage replay of the same triple before 2026-10-18 would confirm the 48d recurrence cadence.

## Sources

- `memory/MEMORY.md` (`## Current focus` — 08-30 reflect snapshot)
- `memory/logs/2026-08-31.md` + `memory/logs/2026-08-30.md`
- `memory/cron-state.json` (last read this run)
- `memory/issues/INDEX.md` (18 open)
- `memory/state/planner-state.json` (last_run 2026-08-29T06:45Z — 2 planner slots missed 08-30, 08-31)
- `gh pr list` OK · `gh pr view 26` OK
