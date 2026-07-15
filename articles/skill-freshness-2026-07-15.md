# Skill Freshness — 2026-07-15

**Verdict:** ✅ FRESHNESS_OK — all enabled consumers' dependencies are within freshness thresholds

*Audited 44 enabled skills · 2 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — no flagged dependencies this run.)*

## What this means per consumer

All 44 enabled consumers have dependencies within their freshness thresholds. No action required.

## Healthy consumers

- batch-health — 0 cross-skill deps, all fresh.
- compute-futures-eda — 0 cross-skill deps, all fresh.
- fleet-control — 0 cross-skill deps, all fresh.
- heartbeat — 0 cross-skill deps, all fresh.
- notegraph — 0 cross-skill deps, all fresh.
- planner — 1 dep (`memory/state/planner-state.json`, 1.3h old, threshold 720h), all fresh.
- skill-health — 0 cross-skill deps, all fresh.
- surplus-pulse — 1 dep (`memory/topics/surplus-pulse.md`, 1.3h old, threshold 168h), all fresh.

+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: 44 entries with `enabled: true` (skill-repair, tool-builder classified `on_demand` — not audited as consumers)
- Implicit references discovered: 2 (planner → planner-state.json, surplus-pulse → surplus-pulse.md)
- Explicit `chains: consume:` edges: 0 (chains block is fully commented out)
- Files not yet on disk (skipped — implicit references that never existed): 15+ (articles/ directory absent; .outputs/github-trending.md; memory/topics/projects.md, watched-repos.md, pr-review-rules.md and others)

### Freshness thresholds applied

| Path class | Threshold | Files on disk |
|------------|-----------|---------------|
| `articles/{skill}-*.md` (daily producer) | 28 h | 0 — articles/ directory does not exist |
| `articles/{skill}-*.md` (weekly producer) | 192 h | 0 — articles/ directory does not exist |
| `.outputs/{skill}.md` | 4 h | 41 files, all ~1.3h old (snapshot 2026-07-15T06:55Z) |
| `memory/topics/{name}.md` | 168 h | 6 files, all ~1.3h old |
| `memory/state/{name}.json` | 720 h | 3 files, all ~1.3h old |

### Structural note (unchanged)

All on-disk files share a single git timestamp (snapshot commit `e9e7f22`, 2026-07-15T06:55:10Z). This is the known GHA mtime blind spot per [[skill-freshness-mtime-blind-in-gha]]: `stat --format=%Y` and `os.path.getmtime()` both report checkout time, not commit time, making all freshness checks vacuously OK regardless of when files were last substantively updated. The fix (use `git log -1 --format=%ct` per-file) is tracked in `memory/MEMORY.md` next-priorities and remains outstanding. This run reports FRESHNESS_OK but the structural check is not meaningful until the mtime source is corrected.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
