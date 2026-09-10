# Skill Freshness — 2026-09-10

**Verdict:** ✅ FRESHNESS_OK — all tracked dependencies are within their freshness windows

*Audited 43 enabled consumers · 36 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — all dependencies are fresh.)*

## What this means per consumer

No enabled consumer has a flagged dependency. All tracked file classes (articles/, .outputs/ chain edges, memory/topics/, memory/state/) are within threshold.

## Healthy consumers

- planner — 1 dep (memory/state/planner-state.json), all fresh. (Last success 2026-09-08T07:53Z; state threshold 30d/720h; age ~50h.)
- pr-tracker — 1 dep (memory/topics/pr-status.md), all fresh. (Last success 2026-09-05T10:40Z; topic threshold 7d/168h; age ~115h — within 168h window.)
- skill-freshness — 1 dep (memory/topics/skill-freshness-state.json), all fresh. (Last success 2026-09-09T09:32Z; topic threshold 7d/168h; age ~24.5h.)
- notegraph — 0 cross-skill deps (memory/state/notegraph.json is self-read, filtered), all fresh.
- surplus-pulse — 0 cross-skill deps (memory/topics/surplus-pulse.md is self-read, filtered), all fresh.
- compute-pulse — 0 cross-skill deps (memory/topics/compute-pulse.md is self-read, filtered), all fresh.
- batch-health — 0 cross-skill deps tracked, all fresh.
- compute-futures-eda — 0 cross-skill deps tracked, all fresh.

+ 35 more all-fresh consumers.

## Notable producer staleness (informational — no enabled consumer reads these cross-skill)

The following enabled producers have missed recent runs; no flag fires because no currently enabled consumer reads their outputs via a tracked cross-skill dependency:

| Producer | Last Success | Age | Daily Threshold | Note |
|----------|-------------|-----|-----------------|------|
| suggest-edges | 2026-09-05T06:06Z | ~120h | 28h | 4+ missed daily runs (ISS-006 area) |
| pr-tracker | 2026-09-05T10:40Z | ~115h | 28h | 5-day scan gap, same pocket |
| pr-triage | 2026-09-05T10:37Z | ~115h | 28h | Same pocket |
| planner | 2026-09-08T07:53Z | ~50h | 28h | 2-day gap, ISS-006 06:30Z slot |
| compute-futures-eda | 2026-09-08T07:55Z | ~50h | 28h | 06:00Z pocket dead streak |
| skill-health | 2026-09-08T19:48Z | ~38h | 28h | 1 missed day |
| reflect | 2026-09-08T19:50Z | ~38h | 28h | 1 missed day |

These are tracked by skill-health (consecutive failures) and batch-health (morning batch audit), not by this skill.

## Source status

- `aeon.yml`: 250+ entries, 43 enabled consumers (44 enabled total; skill-repair excluded as reactive/on_demand)
- Implicit references discovered: 36 (across articles/, .outputs/, memory/topics/, memory/state/ path classes)
- Explicit `chains: consume:` edges: 0 (all chain definitions are commented out in aeon.yml)
- Files not yet on disk (skipped — implicit references that never existed): 5 (memory/topics/projects.md, memory/topics/watched-repos.md, memory/topics/stale-models.md, memory/topics/pr-review-rules.md, memory/topics/compute-tokens.md)

## Dedup status

Fingerprint identical to 2026-09-09 run (da39a3ee — SHA1 of empty flagged set). Status: FRESHNESS_NO_CHANGE. Notification suppressed. Re-emit window resets after 7 days of no change (2026-09-16).

## Data quality note

GHA shallow clone (depth=1) causes `git log -1 --format=%ct` to return the HEAD commit timestamp (2026-09-10T05:22:10Z, the notegraph run) for all tracked files — per-file ages are indistinguishable. This run used `memory/cron-state.json` `last_success` values as producer freshness proxies (same approach as 2026-09-09 run). The known fix ([[skill-freshness-mtime-blind-in-gha]]) remains pending.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: producer ages derived from cron-state.json last_success timestamps (GHA mtime-blind workaround) — this skill measures nothing it does not also report.*
