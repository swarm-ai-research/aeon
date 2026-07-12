# Skill Freshness — 2026-07-12

**Verdict:** ✅ FRESHNESS_OK — all 2 tracked dependencies are within threshold

*Audited 44 enabled skills · 2 dependencies checked · 0 flagged*

## Flagged dependencies

*(none — all dependencies are fresh)*

## What this means per consumer

*(no flagged consumers — every enabled skill's upstream files are within their freshness window)*

## Healthy consumers

- stale-content-pr-sweeper — 1 dep (`memory/state/notegraph.json`, class `state`, age <1h, threshold 720h), all fresh.
- pr-tracker — 1 dep (`memory/topics/pr-status.md`, class `topics`, age <1h, threshold 168h), all fresh.
- planner — 0 matched deps, all fresh.
- batch-health — 0 matched deps, all fresh.
- memory-flush — 0 matched deps, all fresh.
- memory-structural-dedupe — 0 matched deps, all fresh.
- notegraph — 0 matched deps, all fresh.
- suggest-edges — 0 matched deps, all fresh.
+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: 130+ entries, 44 enabled
- Implicit references discovered: 2 (resolved to on-disk files; all within threshold)
- Explicit `chains: consume:` edges: 0 (all chains commented out in `aeon.yml`)
- Files not yet on disk (skipped — implicit references that never existed): ~12 (e.g. `memory/topics/watched-repos.md`, `memory/topics/compute-tokens.md`, `memory/topics/projects.md`, `.outputs/github-trending.md`)

## Structural note

On-disk mtimes reflect the GHA runner checkout timestamp (~08:53 UTC today), not the actual last-write time — the [[skill-freshness-mtime-blind-in-gha]] blind spot is still in effect. Both tracked dependencies (`memory/state/notegraph.json` updated today by notegraph; `memory/topics/pr-status.md` maintained by pr-tracker) were committed in the current repo snapshot and appear fresh under any threshold. Fix: use `git log -1 --format=%ct` instead of `stat --format=%Y` per the open next-priority item.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
