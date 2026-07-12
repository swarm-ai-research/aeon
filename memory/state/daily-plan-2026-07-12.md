# Plan — 2026-07-12

**Today's one thing:** Ping the operator for a `repo`-scoped PAT — Day 2 as top priority, 11 branches still parked, and ISS-006's 3-consecutive-clean-day close clock enters Day-1-of-3 tonight if today's 06:00 / 08:00 pockets deliver.

## Ranked

1. **Operator PAT provisioning ping (streak → 2).** Every landing path for the six stalled fleet fixes and every content-skill output route through the same `gh pr create` 403 per [[github-actions-cannot-create-prs]]. Staged queue is 11 branches (agi-tracker/2026-06-29, notegraph/2026-07-06 + 07-11, workflow-security-audit ×3, skill-graph/2026-06-28, skillpacks/2026-07-05, suggest-edges/2026-07-07 + 07-10 + 07-11) — nothing new landed since yesterday's ping, but a `repo`-scoped PAT unblocks all of them in one shot AND unblocks item 2's staged branch before it queues as #12. Frame the ping for the operator in close-clock terms — if today's pockets go clean, ISS-006 Day-1-of-3 starts tonight, and a PAT that lands the `messages.yml` per-slot-cron rewrite closes the incident outright rather than waiting on two more clean-day rolls. Serves goal `open-queued-branches-via-pat` (14 activity days, sole BLOCKED status per `memory/goal-state.json`).

2. **compute-futures-eda `wallet_sum_pnl` σ<1e-6 filter — draft the patch, stage the branch.** Three consecutive float-dust validation days per [[compute-futures-eda-wallet-sum-pnl-correlations-are-float-dust]] (07-09 first flag, 07-10 x402 wallet_sum_pnl × x402Total +0.881 → 07-11 +0.088 crossing collapse, 07-11 zero |r|≥0.8 in any mode). Highest-signal self-actionable item on the board. Patch lands in the correlation stage of `prototypes/compute-futures/*.mjs` — one σ-gate that filters any variable with σ<1e-6 before correlating. Stage the branch even though the PR will 403; if item 1 lands the PAT same-day the branch is ready to open, and even if it doesn't, the diff exists for review the moment a PAT arrives.

3. **Pre-read `messages.yml` + `aeon.yml` for the enabled-but-never-dispatched skills.** Tonight's daily 23:00 UTC `run-frequency-guard` slot and tomorrow's weekly Mon 08:30 UTC `ai-framework-watch` slot are the two natural data points for [[enabled-skills-can-never-dispatch]]. Both are `enabled: true` with `SKILL.md` present yet zero entries in `cron-state.json`; heartbeat P3 novel-scan flagged them yesterday. Reading the workflow wiring today means tomorrow morning's diagnosis is delta-based (did the slot fire?) rather than start-from-scratch. Investigation, not a fix — but the fix likely lives one commit deep once the mismatch is identified, and it clears two enabled-but-silent skills off the fleet board.

## Holding / watching

- **ISS-006 per-slot-cron rewrite** — no 4th parked branch until (a) PAT lands and the existing 11 open, OR (b) today + Mon + Tue pockets all deliver, closing ISS-006 outright via the [[iss-006-pocket-recovery-is-noise]] 3-clean-day rule.
- **ISS-005 swarm-safety-eval close** — permanent-limitation reclass drafted; fleet-ops cleanup, waits.
- **notegraph `generatedAt` mask** — yesterday's genuine +2n/+38e corpus growth broke the 4-day silent-exit streak, and the Node-based sha1 fingerprint (07-10 swap) worked as designed. Watch whether today's extractor silent-exits again or grows again; the local mask patch isn't urgent enough to jump item 2.
- **5 watched-repos-dependent silent-skippers** (code-health / github-monitor / issue-triage / changelog / weekly-shiplog) — steady daily NO_CONFIG exit; operator populate-or-disable call, no planner-drivable move.
- **pr-review / pr-triage 15th/14th-day 403 on `swarm-ai-research/swarm`** — same cross-org Aeon-App write gap per [[aeon-app-no-write-on-swarm-repo]]; waits on cross-org app install with write, not something a planner run moves.
- **PR-tracker Vibe-Trading#390 calendar rolloff at 2026-07-12T15:33:53Z (today)** — expected transition; hash-guard should NOT suppress the resulting `merged: 1 → 0` snapshot at the 11:00 UTC pr-tracker slot. Watching, not planning around.

## Fleet note

0 broken (cf ≥ 2 = none — `skill-repair` rung untouched). 38 historic-DEGRADED all systemic OAuth-burn denominator per ISS-001 (Day 22). At-2× stale worsens by one tick: **janitor 22d / 3.14×** (was 3.00× yesterday; Sun 05:30 slot silent again today per empty `2026-07-12.md` entry), **cost-report 22d / 3.14×** (next Mon slot 07-13), planner recovered day-2 (fired 06:33 UTC today, this run). 08:00 pocket close-clock: Day-1-of-3 tonight if the batch-health / heartbeat / skill-freshness / gitlawb-fleet-metrics quartet all fire today.

## Sources

- `memory/MEMORY.md` — `## Next priorities` (13 items — no `## Goals` header, fallback path per skill spec).
- `memory/cron-state.json` — 44 skills, ranked stale.
- `memory/logs/2026-07-11.md` (planner run, notegraph +2n corpus growth, pr-review APPROVE 5/5, skill-health DEGRADED(38) day-15, reflect 3 new atomic notes) and `2026-07-10.md` (memory-flush day-counter bumps).
- `memory/issues/INDEX.md` — 6 open (ISS-001/002/005/006/007/008).
- `memory/state/planner-state.json` — yesterday's top `operator-pat-provisioning` streak-1, preserved `iss-006-messages-yml-per-slot-crons` streak-3.
- `memory/goal-state.json` — 13 goals, 1 BLOCKED (`open-queued-branches-via-pat`, blocker text bumped 10 → 11 yesterday).
- `gh pr list --state open` → **PR_LIST_UNAVAILABLE** in this environment (empty stdout, no error surfaced). `gh issue list --state open` → **ISSUE_LIST_UNAVAILABLE** likewise. Falling back to local state per skill sandbox note (the 11-branch staged queue is org-internal to `swarm-ai-research/aeon` and not visible via this repo's `gh pr list` anyway).
- `soul/` — absent; using clear, direct, first-person voice per CLAUDE.md.
