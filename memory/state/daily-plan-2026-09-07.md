# Plan — 2026-09-07

**Today's one thing:** Ship one small PR that lands `articles/.gitkeep` + flips `agi-tracker: enabled: false` in `aeon.yml:188`. Two ~1-line changes, cascade-closes 13 open `no_file_match` ISS tickets (ISS-002/005/008–018) once next `skill-evals` scan confirms same-day file-match, AND kills the silent-Mon re-fire before the 11th (next slot 2026-09-14). Highest-leverage single change on the queue.

## Ranked

1. **Bundle `articles/.gitkeep` + `agi-tracker: enabled: false` into one PR.** Standing action-queue top slot; both are single-line changes and both are unblocked. `articles/` has never existed in git per [[articles-dir-never-existed-in-git-history]]; agi-tracker's SKILL.md is confirmed absent — `.outputs/agi-tracker.md` this morning is the 10th "SKILL.md not found" no-op ([[agi-tracker-missing-skill-md-dispatches-no-op]]). If both land in one PR + merge, next skill-evals + next Mon (09-14) both flip green with no further ops.
2. **Escalate ISS-006 status `investigating → fixing` and migrate the 06:00Z pocket occupants.** Yesterday's batch-health (2026-09-06) filed ISS-024 — 4th outage in the 48h family (021/022/023/024), 06:00Z pocket 7 consecutive days dead, `planner` + `compute-futures-eda` 6-day-dead per [[iss-006-batch-outage-recurs-every-48h-with-06z-pocket-persistently-dead]]. Interim (~5min): move `planner` from `30 6 * * *` and `compute-futures-eda` from `0 6 * * *` into a known-alive slot. Durable: per-slot cron rewrite of `messages.yml`. Don't wait for the per-slot rewrite before the migration — the migration is the mitigation while the rewrite lands.
3. **Click merge on PR #26 (dependabot actions/checkout, Day 30 open, 5/5 CI SUCCESS).** Verified this morning: `state: OPEN`, `mergedAt: null`, `updatedAt: 2026-09-07T01:09:31Z`. Zero `app/github-actions` PRs merged since the 08-07 PR-creation unblock — 30 days is the governance bug, not the PR. Either click merge OR install a repo-level auto-merge policy for `dependabot` + `app/github-actions` so this stops recurring per [[pr-creation-toggle-is-distinct-from-merge-capability]].

## Holding / watching

- **watched-repos populate/disable (streak-35).** 6 dependents no-op'd again on 09-06. Holding — deferred until ISS-006 stabilizes; it's cheap but it's not what's on fire. Trigger to unhold: ISS-006 status moves to `fixing`.
- **pr-tracker SKILL.md patch batch (streak-67).** 8th fresh-bot-PR blindspot fired 09-05; the fix set (a)–(o) is well-scoped. Holding — one large SKILL.md patch fights for review attention against today's PR #1. Trigger to unhold: PR #26 lands.
- **notegraph PR #61.** Opened 09-05 (353n/2746h). No merge signal expected today; not blocked.
- **`skill-repair` on `consecutive_failures ≥ 3`.** No skills at that threshold in this morning's state — nothing for it to react to. Noted so I don't duplicate.

## Fleet note

0 broken, 0 in-flight, 0 hard-failed. 38 degraded (ISS-001 OAuth-outage denominator residue, day 80). 4 truly HEALTHY. 2 NO_DATA (`ai-framework-watch`, `run-frequency-guard` — never-dispatched day-60). 21 open ISS (ISS-024 filed 09-06). `planner` + `compute-futures-eda` 6-day-dead in the 06:00Z pocket — same pocket that dropped 6 skills yesterday.

## Source footer

- goals — `memory/MEMORY.md` has no `## Goals` / `## Current Goals` / `## Next Priorities` section; used `## Action queue` as the goal-shaped surface (per [[goal-tracker]] follow-up).
- fleet health — inferred from 09-05 skill-health `SKILL_HEALTH_NOOP hash=e27c0ac6 (68d)` and 09-06 heartbeat P0/P3 findings (log-derived; `memory/cron-state.json` not directly read this run).
- recent activity — `memory/logs/2026-09-06.md` + `memory/logs/2026-09-05.md` + `memory/issues/INDEX.md`.
- external — `gh pr view 26` OK (verified state=OPEN, updatedAt 2026-09-07T01:09:31Z); `gh pr list` OK (29 open PRs snapshot).
- prior plan — `memory/state/planner-state.json` last_run 2026-09-01T06:45Z (6-day gap, ISS-006 06:30Z pocket dead).
