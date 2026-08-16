# Skill Freshness — 2026-08-16

**Verdict:** ✅ FRESHNESS_OK — all enabled consumers' dependencies are within freshness thresholds

*Audited 44 enabled skills · 2 cross-skill dependencies checked · 0 flagged*

## Flagged dependencies

None — all enabled consumers' dependencies are within freshness thresholds this run.

> **Change from prior run (2026-08-15):** Prior run recorded verdict `FRESHNESS_STALE` with 2 flagged deps (`heartbeat → articles/token-report-*.md`, `weekly-shiplog → articles/push-recap-*.md`). Today's run re-classifies both as non-flaggable: both are implicit wildcard references to disabled producers (`token-report: enabled: false`, `push-recap: enabled: false`) whose article files have never been committed to this repository. Per SKILL.md rule — "Implicit grep-discovered references that simply never existed are not flagged" — neither triggers MISSING. The prior runs appear to have applied a different interpretation; this run follows the SKILL.md strictly.

## What this means per consumer

No consumers have non-OK verdicts this run.

## Healthy consumers

- heartbeat — 1 dep (articles/token-report-*.md), not flagged: implicit wildcard ref, producer disabled, files never existed.
- weekly-shiplog — 1 dep (articles/push-recap-*.md), not flagged: implicit wildcard ref, producer disabled, files never existed.
- fleet-control — 1 dep (articles/fleet-status-*.md), filtered: self-read of own prior output, not a cross-skill gap.
- planner — 0 external cross-skill deps, all fresh.
- code-health — 0 external cross-skill deps, all fresh.
- compute-futures-eda — 0 external cross-skill deps, all fresh.
- skill-health — 0 external cross-skill deps, all fresh.
- reflect — 0 external cross-skill deps, all fresh.
+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: 153 entries, 44 enabled
- Implicit references discovered: 2 (targeted scan across all enabled SKILL.md files; both are article-class wildcard refs)
- Explicit `chains: consume:` edges: 0 (all chain definitions are commented out in `aeon.yml`)
- Files not yet on disk (skipped — implicit references that never existed): 2 (`articles/token-report-*.md`, `articles/push-recap-*.md`)

### Methodology note — GHA mtime blindness

All on-disk files in this checkout show mtime `2026-08-16 08:38` (the GHA checkout timestamp), which makes all `memory/topics/`, `memory/state/`, and `.outputs/` files appear fresh regardless of when they were last written. This is the known structural blind spot per [[skill-freshness-mtime-blind-in-gha]]. A pending fix (use `git log -1 --format=%ct -- <file>` instead of `stat`) would give true write timestamps. Until that fix lands, the mtime-based scores for locally-present files are optimistic — they will always appear within threshold after a fresh checkout.

The article-class verdict above is unaffected by this limitation (no articles files exist at all, so no mtime to misread).

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
