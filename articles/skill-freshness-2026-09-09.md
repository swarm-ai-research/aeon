# Skill Freshness — 2026-09-09

**Verdict:** ✅ FRESHNESS_OK — all tracked dependencies are within their freshness windows

*Audited 43 enabled consumers · 36 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — all dependencies are fresh.)*

## What this means per consumer

No enabled consumer has a flagged dependency. All tracked file classes (articles/, .outputs/ chain edges, memory/topics/, memory/state/) are within threshold.

## Healthy consumers

- planner — 1 dep (memory/state/planner-state.json), all fresh.
- batch-health — 0 cross-skill deps, all fresh.
- compute-futures-eda — 0 cross-skill deps tracked, all fresh.
- reflect — 0 specific file-pattern deps extracted (reads articles/ directory broadly, not a specific file pattern), all fresh.
- skill-health — 0 cross-skill deps, all fresh.
- surplus-pulse — 0 cross-skill deps (memory/topics/surplus-pulse.md is self-read, filtered), all fresh.
- goal-tracker — 0 cross-skill deps, all fresh.
- stale-content-pr-sweeper — 0 cross-skill deps, all fresh.

+ 35 more all-fresh consumers.

## Source status

- `aeon.yml`: 250+ entries, 43 enabled consumers (44 enabled total; skill-repair excluded as on_demand)
- Implicit references discovered: 36 (across articles/, .outputs/, memory/topics/, memory/state/ path classes)
- Explicit `chains: consume:` edges: 0 (all chain definitions are commented out in aeon.yml)
- Files not yet on disk (skipped — implicit references that never existed): 0

## Data quality note

GHA shallow clone (depth=1) causes `git log -1 --format=%ct` to return the HEAD commit timestamp (2026-09-09T00:17:18Z) for all tracked files — indistinguishable per-file ages. This run used `memory/cron-state.json` `last_success` values as producer freshness proxies. The known fix ([[skill-freshness-mtime-blind-in-gha]]) remains pending. Verdicts for weekly producers with long-since-passed last_success (e.g. compute-pulse last ran 2026-08-22, age ~430h) were not escalated because no enabled consumers read those files cross-skill.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from producer last_success timestamps in cron-state.json (GHA mtime-blind workaround) — this skill measures nothing it does not also report.*
