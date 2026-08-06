# Plan — 2026-08-06

**Today's one thing:** ship the one-line direct-edit to disable `agi-tracker` in `aeon.yml:188` before Mon 2026-08-10 13:00Z (6th silent-risk slot) — planner-adjacent, needs no PR, dodges the operator-toggle meta-block.

I'm running for the first time in 4 days (last success 2026-08-02T07:59:51Z). Today's 06:30Z slot fired ~51min late at 07:21Z — squarely inside the late pocket per [[morning-pocket-splits-into-two-de-facto-clusters]]. That breaks the 3-day silent streak from 08-03/04/05 but doesn't fix the migration; treat this run as an unreliable slot, not a return to normal.

## Ranked
1. **Direct-edit `enabled: false` on `aeon.yml:188` for `agi-tracker`** — 6th silent-risk Monday slot is 4 days away (2026-08-10 13:00Z). Per [[agi-tracker-missing-skill-md-dispatches-no-op]] the skill will dispatch to a no-op again unless SKILL.md is authored (larger scope) OR the enabled flag flips. Direct-edit is one line, no operator dependency, doesn't need the merge queue to unblock — this is the only rank-1 candidate I can actually move today. Promoting from rank-2/3 where it's sat with zero forward motion for 3 weeks. Skill or step: any editor with commit rights on main; folded under `skill-repair` if it wakes on the agi-tracker miss, else operator (or a fleet-repair skill) hand-edits.
2. **Repo Settings toggle OR PAT provisioning** — same meta-blocker, streak-6 by run / streak-13 by calendar. Unblocks ≥26 staged branches + 6 stalled fleet fixes (pr-tracker 42d-overdue patch, ISS-006 fix path, docs/status.md stage-fix, ISS-021 draft, agi-tracker branch merge). Format escalation only per [[planner-silenced-by-its-own-escalation-target]]: today's notify puts the single operator ask up top as the first line — no long context, one link, one command. If this run's ask also lands unread, next planner's notify becomes text-first, link-second.
3. **Populate `memory/watched-repos.md` (or disable the 6 dependent skills)** — trivial low-friction. 08-05 log shows 3 same-day short-circuits (issue-triage + github-monitor + code-health); weekly-shiplog + changelog + repo-revive also silently no-op. Path (a) add 3–5 watched repos; path (b) `enabled: false` on all 6 to stop wasting workflow slots. Either is planner-adjacent (`aeon.yml` edit). Serves fleet health + goal-tracker signal.

## Holding / watching
- **ISS-006 messages.yml fix (per-slot crons)** — blocked by rank-2 for branch merge; today's late-window fire adds one more data point but doesn't change the fix scope. Trigger to move: operator toggle lands, OR a 4-day silent streak recurs (would justify a workaround-branch push).
- **pr-tracker SKILL.md patch batch (8 items, 42d overdue)** — every path lands via merged PR = rank-2 blocker. Not thrashing.
- **ISS-021 draft (never-dispatched)** — 18th-day carryover for `ai-framework-watch` + `run-frequency-guard` (29d silent each). Fix is same shape as rank-1's `enabled: false` — folding under it rather than filing a duplicate.
- **docs/status.md snapshot-rebase clobber** — 20d past urgency; 10th consecutive regen. Non-critical while heartbeat keeps regenerating wholesale.
- **`.pending-disclosure/` queue (4 items, +4d aging)** — operator submits out-of-band; nothing I can do.
- **swarm PR queue byte-identical day-13** — 32 pr-review invocations of structural stasis; 24 confirming invocations of [[aeon-app-no-write-on-swarm-repo]]. No new signal today.

## Fleet note
0 broken, 0 in-flight, 38 DEGRADED (ISS-001 OAuth residue day 47, all `last_status: success` cf=0), 4 HEALTHY, 2 NO_DATA (ai-framework-watch + run-frequency-guard, 29th silent day). skill-health hash `e27c0ac60367e7e5` — 41st consecutive steady-state day. 18 open issues in tracker. Today's fresh signal: my own run broke the 3-day silent streak but arrived 51min late.

## Sources
- `memory/MEMORY.md` (60 lines, index-only — no `## Goals` section; priorities derived from `## Current focus` + `## Pointers`)
- `memory/state/planner-state.json` (last run 2026-08-02T07:55:00Z; top_priority streak-5 by run)
- `memory/cron-state.json` (42 skills tracked, 0 with cf ≥ 2, all last_status=success)
- `memory/logs/2026-08-04.md` + `memory/logs/2026-08-05.md`
- `memory/issues/INDEX.md` (18 open)
- `gh pr list` → 1 (dependabot #8, unchanged since 2026-08-03T01:08Z)
- `gh issue list` → 0 open in-repo
