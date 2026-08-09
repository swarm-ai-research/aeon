# Plan — 2026-08-09

**Today's one thing:** Ship the `agi-tracker` `enabled: false` PR on `aeon.yml:188` now. Deadline (Mon 2026-08-10 13:00Z) is ~29h away, the aeon-repo queue is 14 PRs deep with **0 merged in 48h+ since the 08-07 unblock**, and merges are manual — the PR needs to sit visible for a full day to give operator any real chance to merge before the 6th silent-risk agi-tracker slot fires.

## Ranked

1. **Ship `agi-tracker: { enabled: false }` PR** (streak-3, deadline-critical) — one-line change on `aeon.yml:188`. `skills/agi-tracker/` confirmed missing (verified this run), so weekly Mon-13:00Z fires are silent no-ops per [[agi-tracker-missing-skill-md-dispatches-no-op]]. Ship on a branch so it joins the queue; even if it doesn't merge in time, it's staged. Alt path (author full SKILL.md matching the [[agi-tracker]] MOC's frontier-agent scoring shape) is strictly higher-friction with the same effect on Mon deadline — reject unless operator asks.

2. **Escalate queue-depth to operator via the same notify** (per MEMORY.md line 42 trigger: "if no merges by 2026-08-09, planner escalates queue-depth to rank-1"). Concrete asks: (a) merge one low-risk PR to prove the flow — #10 (notegraph orphan flag, 50h old, no dependencies), or the twin `suggest-edges` #21+#22; (b) then merge the agi-tracker PR when it lands. All 14 open PRs show `mergeStateStatus: UNKNOWN` and `statusCheckRollup: []` — no CI or branch protections are gating.

3. **Ship `stale-content-pr-sweeper` `ALLOWED_AUTHORS` patch** (streak-2). Yesterday's #21 + today's #22 form the first n=2 `suggest-edges` group; the sweeper's hardcoded `{"aeonframework"}` allowlist now silently fails to prune duplicates. One-line map extension adds `"app/github-actions"`.

## Holding / watching

- `watched-repos` populate-or-disable (streak-4) — 5 same-day short-circuits on 08-08. Chronic but non-urgent.
- `pr-tracker` SKILL.md patch batch (46d overdue) — subordinate to the Mon deadline. Escalate when queue drains and merge-flow is proven.
- ISS-006 messages.yml multi-pocket cron rewrite — subordinate.
- `docs/status.md` snapshot-rebase clobber gate — 23d past urgency; 13th consecutive rebase-clobber-then-regen expected tonight.
- swarm-repo App-perm gap — distinct from aeon-repo unblock; 27th confirming invocation coming. Out of scope for planner.

## Fleet note

0 broken · 0 in-flight · 38 DEGRADED (ISS-001 day 50) · 4 HEALTHY · 2 NO_DATA (32nd silent day per [[enabled-skills-can-never-dispatch]]) · 18 open issues · skill-health hash unchanged 44th steady-state day.

## Notes

- Mode: `${var}` empty → plan-only, no dispatch.
- Fire time 2026-08-09T07:35Z, user-triggered (not cron). Scheduled 06:30Z slot not yet observed via `./scripts/skill-runs` — no ISS-006 late-pocket signal in this run.
- Yesterday's rank-1 (`agi-tracker-enabled-false-via-pr`) HOLDS at rank-1 with streak-3. Yesterday's rank-2 (`stale-content-pr-sweeper-allowed-authors-patch`) advances to rank-3 with streak-2 (reordered: queue-escalate slotted between them as the newly-triggered pointer per MEMORY.md line 42). Yesterday's rank-3 (`watched-repos-population-or-disable`) drops to `holding` at streak-4.
