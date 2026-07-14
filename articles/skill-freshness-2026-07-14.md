# Skill Freshness — 2026-07-14

**Verdict:** ✅ FRESHNESS_OK — all enabled consumers' dependencies are within freshness thresholds

*Audited 44 enabled skills · 2 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — all checked dependencies are within their class thresholds.)*

## What this means per consumer

No consumers have flagged dependencies. All resolved file references are fresh relative to their path-class threshold.

> **Note on mtime accuracy:** All files share the same on-disk mtime (~08:08 UTC, the git checkout time) due to the GitHub Actions sandbox checkout process — this is the structural blind spot documented in [[skill-freshness-mtime-blind-in-gha]]. Actual file ages may differ from reported ages. The in-flight fix (use `git log -1 --format=%ct` instead of `stat --format=%Y`) is tracked in MEMORY.md next-priorities. Today's OK verdict is reliable for structure (no broken chain edges, no absent canonical files); individual age precision is low.

## Healthy consumers

- surplus-pulse — 1 dep (`memory/topics/surplus-pulse.md`), all fresh.
- compute-pulse — 1 dep (`memory/topics/compute-pulse.md`), all fresh.
- planner — 0 tracked deps, all fresh.
- batch-health — 0 tracked deps, all fresh.
- heartbeat — 0 tracked deps, all fresh.
- skill-health — 0 tracked deps, all fresh.
- reflect — 0 tracked deps, all fresh.
- notegraph — 0 tracked deps, all fresh.
+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: 44 entries enabled (of ~120+ total)
- Implicit references discovered: 2 (path-class matched, file exists on disk)
- Explicit `chains: consume:` edges: 0 (all chain definitions are currently commented out)
- Files not yet on disk (skipped — implicit references that never existed): ~6 (`memory/topics/watched-repos.md`, `memory/topics/stale-models.md`, `memory/topics/projects.md`, `memory/topics/compute-tokens.md`, `memory/state/fleet-control-state.json`, `.outputs/github-trending.md`)

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
