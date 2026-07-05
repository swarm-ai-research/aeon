# Plan — 2026-07-05

**Today's one thing:** Draft `.github/workflows/messages.yml` per-slot cron rewrite on `fix/iss-006-per-slot-crons` — third consecutive planner run with this as top priority, and the 2026-07-03 plan's "draft the diff" step never landed (no branch exists locally or on origin). Stuck-goal escalation: stop restating and actually write the diff in this run, then flag that the queue-a-branch path is itself capped at 6 stalled branches until the operator provisions a cross-repo PAT.

## Ranked
1. **Draft messages.yml per-slot cron rewrite on `fix/iss-006-per-slot-crons`** — top priority for the 3rd run running (2026-06-27 → 07-03 → 07-05, streak 3). Concrete unblock, not restatement: replace the single `*/15 * * * *` tick with explicit per-slot crons covering every timeslot in `aeon.yml` (per [[gha-messages-yml-cron-underdelivery]]) and stage the branch. Meta-flag: this becomes the 7th `.pending-*` queued branch — the actual durable unblock is operator PAT provisioning, not another draft.
2. **Sunday-batch fire watch (05:30 → 06:30 UTC window)** — janitor, skillpacks, compute-macro-correlate all at 2× weekly threshold today; their fire/miss is fresh signal on whether ISS-006 has Sunday-cadence variance vs the weekday pocket-swap pattern. Planner's own 06:30 slot already missed today (running catch-up ~07:44Z), so at least one Sunday morning pocket is cold.
3. **pr-tracker step-5 trigger patch** — Agent-Reach#436 stale + kage#66 silent close only coincidentally tripped notify yesterday (first fire in 15 daily runs); the durable ask per [[pr-tracker-step-5-misses-fresh-bot-prs]] is a 4th trigger for "N≥1 fresh bot PR in last 24h". Two bot PRs (2h/11h) silently landed 2026-07-03 without notify.

## Holding / watching
- ISS-005 reclassify — dropped from top-3 in favor of the streak-3 escalation; still worth 5 minutes when the ISS-006 branch is staged.
- Agent-Reach#436 — crossed 7d 2026-07-03T19:24Z, pr-tracker flagged + notified 2026-07-04; nothing more to do until the operator pings or closes it.
- Five staged branches queued for operator PR-open (agi-tracker 06-29, notegraph 06-29/07-01/07-02/07-04, fix/workflow-security-audit 06-21/06-28, skill-graph 06-28) — all blocked by "GitHub Actions is not permitted to create or approve pull requests" repo policy; trigger to un-hold = operator provisions PAT.
- compute-pulse Saturday 2026-07-04 11:00 fire — if missed, skill-freshness tips WARN on compute-pulse.md (currently 98.2% of 7d threshold per [[skill-freshness-mtime-blind-in-gha]]).
- `.pending-disclosure/` torlink (`ip@2.0.1` HIGH unpatchable + esbuild LOW) — vuln-scanner cannot fork upstream with runtime token; trigger to un-hold = operator PAT.

## Fleet note
0 broken · 0 stuck (no `consecutive_failures ≥ 2`) · 38 degrading (ISS-001 OAuth-residue denominator burn-down, benign — every skill `last_status: success`) · 6 weekly/biweekly at 2× threshold (janitor / skillpacks / compute-macro-correlate Sun, milestone-tracker / cost-report Mon, memory-structural-dedupe even-DOM). Planner's own 06:30 slot missed today — running catch-up ~07:44Z.

## Source footer
- MEMORY.md `## Next priorities` (12 items) — no `## Goals` section; used priorities-list as goal source per skill fallback.
- `memory/cron-state.json` — 42 entries scanned; 0 at `consecutive_failures ≥ 2`.
- `memory/logs/2026-07-03.md`, `2026-07-04.md`, `2026-07-05.md` — reviewed.
- `memory/issues/INDEX.md` — 4 open (ISS-001, 002, 005, 006).
- `gh pr list` = 0, `gh issue list` = 0 (empty, not unavailable).
- Prior plan `memory/state/planner-state.json` — top_priority unchanged, streak 2 → 3.
