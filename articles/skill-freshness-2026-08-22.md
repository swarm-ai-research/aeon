# Skill Freshness — 2026-08-22

**Verdict:** ✅ FRESHNESS_OK — all 6 discovered dependencies are within threshold

*Audited 44 enabled skills · 6 dependencies checked · 0 flagged*

## Flagged dependencies

*(none — all dependencies within freshness thresholds)*

## What this means per consumer

All enabled consumers with discoverable file dependencies are reading fresh data. No producer appears to have gone silent or failed to write its output on schedule.

## Healthy consumers (sampled)

Implicit file dependencies discovered across enabled skills, all fresh (~1.6h old via git-log, committed by the 06:45 UTC planner batch):

| Consumer | Dependency | Class | Age (git) | Threshold | Severity |
|----------|-----------|-------|-----------|-----------|----------|
| planner | `memory/state/planner-state.json` | state | ~1.6h | 720h (30d) | ✅ OK |
| notegraph | `memory/state/notegraph.json` | state | ~1.6h | 720h (30d) | ✅ OK |
| suggest-edges | `memory/state/suggest-edges.json` | state | ~1.6h | 720h (30d) | ✅ OK |
| skillpacks | `memory/state/skillpacks.json` | state | ~1.6h | 720h (30d) | ✅ OK |
| surplus-pulse | `memory/topics/surplus-pulse.md` | topics | ~1.6h | 168h (7d) | ✅ OK |
| compute-pulse | `memory/topics/compute-pulse.md` | topics | ~1.6h | 168h (7d) | ✅ OK |

All 40 `.outputs/{skill}.md` files also exist and were last committed ~1.6h ago (well under the 4h chain-output threshold), though no active `chains: consume:` edges are wired (all chains commented out in `aeon.yml`).

The `articles/` directory has no committed entries. All article-class references in enabled SKILL.md files are either self-writes (each skill describing its own output path) or reference disabled producers — neither class triggers a MISSING flag.

+ 38 more all-fresh consumers (no explicit or canonical-pattern dependencies found after filtering self-reads and missing-file implicit refs).

## Source status

- `aeon.yml`: 175 entries, 44 enabled
- Implicit references discovered: ~60 across path classes (articles, .outputs, memory/topics, memory/state)
- After filtering (self-reads, missing implicit refs, disabled/on_demand producers): 6 checkable
- Explicit `chains: consume:` edges: 0 (chains block entirely commented out)
- Files not yet on disk skipped (implicit refs that never existed): articles/ dir missing + several memory/state/ files (fleet-control-state.json, skill-repair-history.json)

**Note on mtime methodology:** All file ages computed via `git log -1 --format=%ct` (git commit time), not `stat --format=%Y`. In GitHub Actions all checked-out files share the same stat mtime (checkout time), making `stat`-based ages meaningless. Git commit time is the authoritative freshness signal.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from git commit times — this skill measures nothing it does not also report.*
