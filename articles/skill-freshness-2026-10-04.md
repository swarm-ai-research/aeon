# Skill Freshness — 2026-10-04

**Verdict:** ✅ FRESHNESS_OK — all 2 tracked dependencies are fresh

*Audited 44 enabled skills · 2 dependencies checked · 0 flagged*

## Flagged dependencies

*(none — all dependencies are within their freshness windows)*

## What this means per consumer

All enabled consumers with tracked dependencies are reading fresh files. No action required.

## Healthy consumers

- stale-content-pr-sweeper — 1 dep, all fresh. (`memory/state/notegraph.json` — 0h 6m old, threshold 720h)
- pr-tracker — 1 dep, all fresh. (`memory/topics/pr-status.md` — 0h 6m old, threshold 168h)
- + 42 more all-fresh consumers (0 tracked deps each — no cross-skill file reads detected).

## Source status

- `aeon.yml`: 73 entries, 44 enabled
- Implicit references discovered: 2
- Explicit `chains: consume:` edges: 0
- Files not yet on disk (skipped — implicit references that never existed): 11

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
