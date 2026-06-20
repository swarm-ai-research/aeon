# Skill Freshness — 2026-06-20

**Verdict:** ✅ FRESHNESS_OK — all 9 tracked dependencies are fresh

*Audited 44 enabled skills · 9 dependencies checked · 0 flagged*

## Flagged dependencies

None. Every tracked dependency is within its freshness threshold.

## What this means per consumer

All enabled consumers with tracked upstream dependencies are reading fresh files. No action needed.

## Healthy consumers

- agi-tracker — 1 dep, all fresh.
- compute-pulse — 1 dep, all fresh.
- notegraph — 1 dep, all fresh.
- planner — 1 dep, all fresh.
- pr-tracker — 1 dep, all fresh.
- skillpacks — 1 dep, all fresh.
- stale-content-pr-sweeper — 1 dep, all fresh.
- surplus-pulse — 1 dep, all fresh.
+ 1 more all-fresh consumer (vuln-scanner).

*35 additional enabled consumers have no discovered implicit deps — no cross-skill file reads detected in their SKILL.md.*

## Source status

- `aeon.yml`: ~174 entries on disk, 44 enabled
- Implicit references discovered: 9 (8 unique consumers; stale-content-pr-sweeper and notegraph share one state file)
- Explicit `chains: consume:` edges: 0 (daily-routine chain is inactive/commented out)
- Files not yet on disk (skipped — implicit references that never existed): 20

### Dependency detail

| Consumer | Dependency | Class | Age | Threshold | Severity |
|----------|-----------|-------|-----|-----------|----------|
| agi-tracker | `memory/topics/agi-tracker.md` | topics | 0h | 168h | ✅ OK |
| compute-pulse | `memory/topics/compute-pulse.md` | topics | 0h | 168h | ✅ OK |
| notegraph | `memory/state/notegraph.json` | state | 0h | 720h | ✅ OK |
| planner | `memory/state/planner-state.json` | state | 0h | 720h | ✅ OK |
| pr-tracker | `memory/topics/pr-status.md` | topics | 0h | 168h | ✅ OK |
| skillpacks | `memory/state/skillpacks.json` | state | 0h | 720h | ✅ OK |
| stale-content-pr-sweeper | `memory/state/notegraph.json` | state | 0h | 720h | ✅ OK |
| surplus-pulse | `memory/topics/surplus-pulse.md` | topics | 0h | 168h | ✅ OK |
| vuln-scanner | `articles/vuln-scan-2026-06-20.md` | articles | 0h | 28h | ✅ OK |

*All file ages are effectively 0h because this run occurs shortly after git checkout populates the working tree. All thresholds are safely met.*

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
