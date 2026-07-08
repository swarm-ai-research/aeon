# Skill Freshness — 2026-07-08

**Verdict:** ✅ FRESHNESS_OK — all enabled consumers' dependencies are fresh

*Audited 44 enabled skills · 6 dependencies checked · 0 flagged*

## Flagged dependencies

*(none — all dependencies within freshness thresholds)*

## What this means per consumer

All consumers with resolvable on-disk dependencies passed their freshness checks. No producer has silently stopped writing while a consumer continues reading a stale cached file.

## Healthy consumers

- planner — 1 dep (`memory/state/planner-state.json`, age ~74h, threshold 720h) ✅
- surplus-pulse — 1 dep (`memory/topics/surplus-pulse.md`, age ~17h, threshold 168h) ✅
- compute-pulse — 1 dep (`memory/topics/compute-pulse.md`, age ~96h, threshold 168h) ✅
- notegraph — 1 dep (`memory/state/notegraph.json`, age ~2h, threshold 720h) ✅
- skillpacks — 1 dep (`memory/state/skillpacks.json`, age ~74h, threshold 720h) ✅
- skill-freshness — 1 dep (`memory/topics/skill-freshness-state.json`, age ~24h, threshold 168h) ✅
- 38 more all-fresh consumers (no on-disk dependencies found or all dependencies are self-reads / from disabled producers).

## Source status

- `aeon.yml`: 44 enabled skills
- Implicit references discovered: 18
- Explicit `chains: consume:` edges: 0 (all chains commented out)
- Files not yet on disk (skipped — implicit references that never existed): 12

## Methodology note

All file ages in this run are derived from **content-embedded dates** (e.g. `last_run:` fields, dated headings), not filesystem mtimes or `git log` timestamps. The repo is a single-commit snapshot (`20d6a5c`) so both `stat --format=%Y` and `git log -1 --format=%ct` return identical checkout-time values for every file, rendering them useless for relative age ranking. Per [[skill-freshness-mtime-blind-in-gha]], the correct fix is `git log -1 --format=%ct` against a repo with real history — this workaround is a best-effort substitute until that fix is deployed.

This is the **10th consecutive FRESHNESS_OK** emit. Consecutive identical verdicts do not necessarily indicate the audit is running cleanly — in a snapshot-based GHA environment the structural mtime blindness means this metric is partially a function of content-embedded dates being present and readable, not a formal proof that no file is stale.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
