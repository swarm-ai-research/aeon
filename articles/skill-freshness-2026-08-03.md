# Skill Freshness — 2026-08-03

**Verdict:** ✅ FRESHNESS_OK — all tracked dependencies are fresh

*Audited 44 enabled skills · 7 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — every tracked dependency is within its freshness threshold.)*

## What this means per consumer

No consumer's verdict exceeded OK. No action required.

## Healthy consumers

- planner — 1 dep, all fresh. (`memory/state/planner-state.json`, age ~6min, threshold 720h)
- vuln-scanner — 1 dep, all fresh. (`.outputs/github-trending.md`, age ~6min, threshold 4h)
- pr-tracker — 1 dep, all fresh. (`memory/topics/pr-status.md`, age ~6min, threshold 168h)
- surplus-pulse — 1 dep, all fresh. (`memory/topics/surplus-pulse.md`, age ~6min, threshold 168h)
- compute-pulse — 1 dep, all fresh. (`memory/topics/compute-pulse.md`, age ~6min, threshold 168h)
- notegraph — 1 dep, all fresh. (`memory/state/notegraph.json`, age ~6min, threshold 720h)
- skillpacks — 1 dep, all fresh. (`memory/state/skillpacks.json`, age ~6min, threshold 720h)
+ 37 more all-fresh consumers (no tracked dependencies on disk).

## Source status

- `aeon.yml`: 156 entries, 44 enabled
- Implicit references discovered: 13
- Explicit `chains: consume:` edges: 0 (chains block is fully commented out)
- Files not yet on disk (skipped — implicit references that never existed): 6
  - `memory/topics/compute-futures-macro-correlations.md` (compute-macro-correlate)
  - `memory/topics/framework-watch-state.json` (ai-framework-watch)
  - `memory/topics/skill-graph-state.json` (skill-graph)
  - `memory/state/fleet-control-state.json` (fleet-control)
  - `memory/state/skill-repair-history.json` (skill-repair)
  - `memory/state/suggest-edges.json` (suggest-edges)

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
