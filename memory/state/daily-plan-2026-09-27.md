# Plan — 2026-09-27

**Today's one thing:** Ship `enabled: false` on `aeon.yml:188` for `agi-tracker` **before 2026-09-28T13:00Z** — T-1 to the 13th silent-Monday, and the fix has been rank-1 for 18 planner runs without landing. This is the day the streak either ends or crosses into indefensible.

## Ranked

1. **`agi-tracker` — land `enabled: false` PR today (T-1 hard deadline)** — Streak-18 stuck goal. `skills/agi-tracker/` directory still absent; `aeon.yml:188` still `enabled: true schedule: "0 13 * * 1"`. If tomorrow's 13:00Z Mon slot fires unpatched, we book the 13th consecutive silent-Mon per [[agi-tracker-missing-skill-md-dispatches-no-op]]. Ship the one-character `enabled: false` change; author the missing SKILL.md later — the deadline is the disable, not the restore. No goal-health signal beats "will produce a preventable failure in ~30h."

2. **08Z-pocket collapse day-2 — force a heartbeat dispatch and get `docs/status.md` un-STALE** — Heartbeat + batch-health + skill-freshness + gitlawb-fleet-metrics all last_success 2026-09-25T09:5xZ (~45h). Per [[heartbeat-self-check-invisible-while-heartbeat-is-silent]] the >36h self-check can't fire while heartbeat is silent — we're blind to our own outage. Dispatch heartbeat manually to (a) refresh `docs/status.md`, (b) trip its self-check, (c) let batch-health file the 09-26 ISS-006 tributary that couldn't be filed yesterday. Novel today: the pocket is now n=4 durable per [[iss-006-08z-pocket-collapses-day-4-after-3-day-drift]].

3. **ISS-006 per-slot messages.yml rewrite — streak-34, escalate to branched WIP** — Root cause behind the 06Z 7-day dead streak, the 08Z pocket collapse (2), and 11 filed tributaries (ISS-019–ISS-029). A month at rank-2/3 with no landed change is not "carrying" — it's stalled. Escalation this run: open a WIP branch with the 8-regime per-slot cron scaffold (coherent-late, decoupled-slow, 06:30Z gap, weekend Sat 11Z / Sun 06:30Z, daily-dead 06Z, 08Z widening, drifting-then-silent day-4 collapse), even without the exact cron values filled in. A branch converts the goal from "known fix" to "reviewable artifact."

4. **PR #26 ShellCheck diagnosis (Day-49)** — mergeStateStatus UNSTABLE since dependabot force-rebase 2026-09-14T01:07:51Z. Blocks the "click merge" path per [[pr-creation-toggle-is-distinct-from-merge-capability]]. Read the ShellCheck failure log and either fix or explicitly `wontfix`.

5. **`watched-repos.md` — decide populate vs. disable (streak-57)** — Six dependents (code-health, issue-triage, github-monitor, changelog, weekly-shiplog, repo-revive) short-circuit daily. Path mismatch persists (repo-revive → `memory/topics/watched-repos.md`, others → `memory/watched-repos.md`). Not urgent, but 57 days is the age at which "streak" stops being a metric and starts being an admission.

## Holding / watching

- **pr-tracker close-actor fetch** for openai/openai-agents-python#4829 (23d-post-open close, 09-25 18:49Z) and the 09-17 14:30Z 23-entry bulk-close batch — pr-tracker's own next 10:00Z scan will pick up the former; the latter rolls off in ~4 days, so this becomes urgent by 09-30. Not doing today.
- **suggest-edges within-`gitlawb-compute-futures-proofs/` pre-filter** — Day-54 recurrence, PR #81 opened 09-26. The pre-filter is the root fix; deferring while operator processes the current PR queue (#70/#71/#74/#78/#81).
- **ISS-030 (identity blackout, resolved Day-4) + ISS-031 (never-dispatch class) self-review filings** — Self-review's beat, not planner's. Deferring until self-review next dispatches.
- **`stale-content-pr-sweeper` ALLOWED_AUTHORS patch** — Streak-27, closes zero PRs per [[stale-content-pr-sweeper-default-author-filter-closes-zero-prs]] — real cost is bounded (43 harmless open content PRs), so not competing with today's binding deadlines.
- **`skill-repair` 87d silent** — Reactive skill, wakes on cf≥3; today's fleet has 0 at cf≥2. Not a bug until a hard-fail signal arrives.

## Fleet note

0 broken (cf≥2), 38 DEGRADED (all ISS-001 residue Day-99 — historical OAuth-outage denominator drag, not live regression), 25 heartbeat/batch/status skills silent inside the 08Z-pocket collapse (~45h+, day-2). 25 open issues in INDEX.md. Planner itself was 6-day dead in 06Z pocket before this fire.

## Sources

- `memory/MEMORY.md` — Current focus + Action queue read.
- `memory/cron-state.json` — 42 skills; 0 broken, 38 degraded, 25 stale >72h.
- `memory/logs/2026-09-26.md` + `memory/logs/2026-09-25.md` — recent activity, no 09-27 log yet.
- `memory/issues/INDEX.md` — 25 open, 4 resolved.
- `memory/state/planner-state.json` — last run 2026-09-20T06:30Z, 6 planner runs missed in between (06Z pocket casualty).
- `gh pr list` — 31 open on this repo, dominated by notegraph/suggest-edges cohorts.
- `gh issue list` — not queried this cycle; MEMORY action queue is authoritative.
- Soul directory absent → first-person direct voice.
- `${var}` empty → plan-only, no dispatch.

## Summary

Today's one thing: ship agi-tracker `enabled: false` before tomorrow 13:00Z. Ranked 5. Plan-only (no dispatch — `${var}` empty). Fleet: 0 broken, 38 degraded (Day-99 ISS-001 residue), 25 stale >72h, 08Z-pocket cluster silent 45h+ (day-2 collapse), planner itself 6-day dead in 06Z pocket.
