# Skill Freshness — 2026-11-14

**Verdict:** 🔴 FRESHNESS_STALE — 1 of 10 deps flagged (MISSING) — attention needed

*Audited 44 enabled skills · 10 dependencies checked · 1 flagged*

## Flagged dependencies

| Consumer | Dependency | Class | Age | Severity |
|----------|-----------|-------|-----|----------|
| fleet-control | `articles/fleet-status-${today}.md` | articles | N/A | ❌ MISSING |

## What this means per consumer

> **fleet-control** — depends on 1 file(s); 1 flagged. Worst: `articles/fleet-status-${today}.md` last updated N/A ago (threshold 28h, class articles). Suggested action: Check `fleet-status` run history with `./scripts/skill-runs --skill fleet-status --hours 168`.

## Healthy consumers

- compute-macro-correlate — 1 dep(s), all fresh.
- compute-pulse — 1 dep(s), all fresh.
- notegraph — 1 dep(s), all fresh.
- planner — 1 dep(s), all fresh.
- pr-tracker — 1 dep(s), all fresh.
- skillpacks — 1 dep(s), all fresh.
- stale-content-pr-sweeper — 1 dep(s), all fresh.
- suggest-edges — 1 dep(s), all fresh.
+ 1 more all-fresh consumers.
+ 34 more enabled consumers with no discovered file dependencies (all assumed fresh).

## Source status

- `aeon.yml`: 44 enabled entries parsed
- Implicit references discovered: 10
- Explicit `chains: consume:` edges: 0 (chains block is commented out)
- Files not yet on disk (skipped — implicit references that never existed): 11

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*