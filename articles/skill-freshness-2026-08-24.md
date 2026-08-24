# Skill Freshness — 2026-08-24

**Verdict:** ✅ FRESHNESS_OK — all 8 checked dependencies are within threshold

*Audited 44 enabled skills · 8 dependencies checked · 0 flagged*

## Flagged dependencies

*(none — no dependency crossed its freshness threshold)*

## What this means per consumer

Every enabled consumer's resolved dependencies are fresh. No action required.

## Healthy consumers

- planner — 1 dep (`memory/state/planner-state.json`, state class), all fresh.
- surplus-pulse — 1 dep (`memory/topics/surplus-pulse.md`, topics class), all fresh.
- compute-pulse — 1 dep (`memory/topics/compute-pulse.md`, topics class), all fresh.
- notegraph — 1 dep (`memory/state/notegraph.json`, state class), all fresh.
- suggest-edges — 1 dep (`memory/state/suggest-edges.json`, state class), all fresh.
- pr-tracker — 1 dep (`memory/state/pr-tracker.json`, state class), all fresh.
- skillpacks — 1 dep (`memory/state/skillpacks.json`, state class), all fresh.
- compute-futures-eda — 1 dep (`memory/topics/compute-futures-eda/`, topics class), all fresh.

+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: 156 entries (with `enabled:` key), 44 enabled
- Implicit references discovered: 18
- Explicit `chains: consume:` edges: 0 (chains block is fully commented out)
- Files not yet on disk (skipped — implicit references that never existed): 10

### Notes on skipped references

The following implicit references were discovered but skipped because the files have never existed on disk (per [[skill-freshness-mtime-blind-in-gha]] methodology — only canonical explicit deps fire MISSING):

- `surplus-pulse` → `memory/topics/projects.md` (missing; create if compute-futures + Surplus integration status needs tracking)
- `compute-pulse` → `memory/topics/compute-tokens.md` (missing; optional operator-defined token watchlist)
- `ai-framework-watch` → `memory/topics/framework-watch-state.json` (missing; self-initializes on first run)
- `pr-review` → `memory/topics/pr-review-rules.md` (missing; per [[watched-repos config missing]] chronic class — same resolution path as `watched-repos.md`)
- `repo-revive` → `memory/topics/watched-repos.md` (missing; known chronic — 18-day streak per MEMORY)
- `repo-revive` → `memory/topics/stale-models.md` (missing; optional stale-model substitution list)
- `skill-evals` → `articles/skill-evals-*.md` (prior run; self-referencing, filtered)
- `swarm-safety-eval` → `articles/swarm-safety-eval-*.md` (prior run; self-referencing, filtered)
- `heartbeat` → `articles/token-report-*.md` (missing; producer `token-report` is `enabled: false` → on_demand cadence, not audited)
- `skill-graph` → `memory/topics/skill-graph-state.json` (missing; self-initializes on first run)

### All-green file ages (at run time 08:27Z; commit timestamp 2026-08-24T07:41:06Z, age ~0.8h)

| Dependency | Class | Age | Threshold | Verdict |
|-----------|-------|-----|-----------|---------|
| `memory/state/planner-state.json` | state | 0.8h | 720h | ✅ OK |
| `memory/topics/surplus-pulse.md` | topics | 0.8h | 168h | ✅ OK |
| `memory/topics/compute-pulse.md` | topics | 0.8h | 168h | ✅ OK |
| `memory/state/notegraph.json` | state | 0.8h | 720h | ✅ OK |
| `memory/state/suggest-edges.json` | state | 0.8h | 720h | ✅ OK |
| `memory/state/pr-tracker.json` | state | 0.8h | 720h | ✅ OK |
| `memory/state/skillpacks.json` | state | 0.8h | 720h | ✅ OK |
| `memory/topics/compute-futures-eda/` | topics | 0.8h | 168h | ✅ OK |

*All ages computed via `git log -1 --format=%ct` — the GHA-correct method per [[skill-freshness-mtime-blind-in-gha]]. All files land in the single bootstrap commit `b5994f0` (2026-08-24T07:41:06Z), so ages are identical this run.*

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from git commit timestamps — this skill measures nothing it does not also report.*
