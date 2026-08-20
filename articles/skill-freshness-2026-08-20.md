# Skill Freshness — 2026-08-20

**Verdict:** ✅ FRESHNESS_OK — all tracked dependencies are fresh

*Audited 44 enabled skills · 2 dependencies checked · 0 flagged*

## Flagged dependencies

None. All tracked dependencies scored OK.

## What this means per consumer

No consumers flagged. Every enabled skill with a tracked file dependency is reading data within its expected freshness window.

## Healthy consumers

- stale-content-pr-sweeper — 1 dep (`memory/state/notegraph.json`), fresh (age 0.1h, threshold 720h).
- notegraph — 1 dep (`memory/state/notegraph.json`), fresh (age 0.1h, threshold 720h).
- planner — 0 tracked deps, all fresh.
- batch-health — 0 tracked deps, all fresh.
- memory-flush — 0 tracked deps, all fresh.
- memory-structural-dedupe — 0 tracked deps, all fresh.
- heartbeat — 0 tracked deps, all fresh.
- skill-health — 0 tracked deps, all fresh.
+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: ~120 entries, 44 enabled
- Implicit references discovered: 2 (after self-ref filtering and code-block exclusion)
- Explicit `chains: consume:` edges: 0 (all chains commented out)
- Files not yet on disk (skipped — implicit references that never existed): 13

### Notes

- `articles/` directory has no files. All `articles/{skill}-${today}.md` references in enabled SKILL.md files are self-writes (each skill writes its own output); after self-ref filtering, zero cross-skill article reads remain — no MISSING flags generated.
- `.outputs/github-trending.md` referenced by `vuln-scanner` and `skill-evals` as optional fallback input; file does not exist (github-trending is disabled) — implicit MISSING, not flagged per methodology.
- 13 `memory/topics/` and `memory/state/` files referenced by enabled SKILL.md files do not exist on disk (e.g. `memory/topics/watched-repos.md`, `memory/topics/pr-review-rules.md`, `memory/state/skill-repair-history.json`) — all implicit, all skipped.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
