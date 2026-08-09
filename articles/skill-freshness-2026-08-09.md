# Skill Freshness — 2026-08-09

**Verdict:** ✅ FRESHNESS_OK — all enabled consumers' dependencies are within freshness thresholds

*Audited 44 enabled skills · 2 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — all dependencies are within threshold. No action required.)*

## What this means per consumer

All 44 enabled consumers passed. No consumer is reading a stale upstream file.

## Healthy consumers

- planner — 1 dep (memory/state/planner-state.json), all fresh.
- compute-macro-correlate — 2 deps (memory/topics/compute-pulse.md, memory/topics/surplus-pulse.md), all fresh.
- notegraph — 1 dep (memory/state/notegraph.json), all fresh.
- suggest-edges — 1 dep (memory/state/suggest-edges.json), all fresh.
- skillpacks — 1 dep (memory/state/skillpacks.json), all fresh.
- fleet-control — 1 dep (memory/state/fleet-control-state.json), all fresh.
- surplus-pulse — 1 dep (memory/topics/surplus-pulse.md), all fresh.
- compute-futures-eda — 1 dep (memory/topics/compute-futures-eda/{prev}.md), all fresh.

+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: 153 entries, 44 enabled
- Implicit references discovered: 2
- Explicit `chains: consume:` edges: 0 (all chains commented out)
- Files not yet on disk (skipped — implicit references that never existed): 3 (articles/token-report-*.md × 2 consumers [disabled producer], articles/push-recap-*.md × 1 consumer [disabled producer])

### Environment note

`articles/` directory was absent at start of run (created this run). All `articles/{producer}-${today}.md` references in enabled SKILL.md files are either (a) self-output paths, (b) optional/graceful-fallback reads that degrade cleanly when absent, or (c) references to disabled producers. None qualify as canonical cross-skill MISSING under the spec. Per [[skill-freshness-mtime-blind-in-gha]], git log timestamps were used for accuracy — all tracked files last committed at 2026-08-09T07:41:09Z (compute-macro-correlate success commit), well within every class threshold.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
