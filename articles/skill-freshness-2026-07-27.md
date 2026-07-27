# Skill Freshness — 2026-07-27

**Verdict:** ✅ FRESHNESS_OK — all checked dependencies are within their freshness windows

*Audited 44 enabled skills · 6 dependencies checked · 0 flagged*

## Flagged dependencies

*(none — all surviving non-self-referential dependencies are within threshold or not subject to MISSING flagging)*

## What this means per consumer

All 44 enabled consumers have clean dependency profiles for this run. No consumer is at risk of silently acting on stale upstream data.

**Notes on implicit-missing references (not flagged, informational):**

These files were referenced in enabled SKILL.md files but do not exist on disk. Per skill rules, implicit references to files that never existed are not flagged as MISSING — they represent optional inputs, graceful-fallback patterns, or files from disabled producers.

| Consumer | Missing implicit dep | Class | Status |
|----------|---------------------|-------|--------|
| `compute-pulse` | `memory/topics/compute-tokens.md` | topics | implicit, not flagged — optional watchlist |
| `compute-macro-correlate` | `memory/topics/compute-futures-macro-correlations.md` | topics | implicit, not flagged — first run creates it |
| `surplus-pulse` | `memory/topics/projects.md` | topics | implicit, not flagged — hand-maintained, skip on absent |
| `heartbeat` | `articles/token-report-*.md` | articles | implicit, not flagged — producer disabled; heartbeat skips silently |
| `repo-revive` | `memory/topics/watched-repos.md` | topics | implicit, not flagged — logs REPO_REVIVE_NO_CONFIG and exits cleanly |
| `repo-revive` | `memory/topics/stale-models.md` | topics | implicit, not flagged — optional scoring input |

These are not freshness violations — they are bootstrap gaps or intentionally optional inputs that the consuming skills handle gracefully.

## Healthy consumers

All 44 enabled consumers are all-fresh. Showing first 8:

- planner — 1 dep (memory/state/planner-state.json), fresh
- batch-health — 0 file-class deps; reads memory/logs/ directly
- memory-flush — 0 file-class deps; operates on memory/ directly
- memory-structural-dedupe — 0 file-class deps; operates on MEMORY.md directly
- surplus-pulse — 1 dep (memory/topics/surplus-pulse.md), fresh
- compute-pulse — 1 dep (memory/topics/compute-pulse.md), fresh
- compute-futures-eda — 0 cross-skill deps (self-contained; reads deployer CSV from fleet-state branch)
- compute-macro-correlate — 0 on-disk cross-skill deps (fetches macro prices live; Track B via git fetch fleet-state)

+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: ~120 skill entries, 44 enabled
- Implicit references discovered: 6 (after self-referential filtering)
- Explicit `chains: consume:` edges: 0 (all chain definitions are commented out)
- Files not yet on disk (skipped — implicit references that never existed): 6

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report. Known limitation: in GitHub Actions, file mtimes reflect checkout time, not content date; git log timestamps were used as the authoritative source per the pending fix in [[skill-freshness-mtime-blind-in-gha]].*
