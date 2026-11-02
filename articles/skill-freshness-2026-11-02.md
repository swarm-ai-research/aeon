# Skill Freshness — 2026-11-02

**Verdict:** ✅ FRESHNESS_OK — no enabled consumer has a flagged dependency

*Audited 44 enabled skills · 9 dependencies checked · 0 flagged*

## Flagged dependencies

No flagged dependencies this run. All assessed dependencies are within their expected freshness windows (or indeterminate due to sandbox timestamp limitations — see Source Status below).

## What this means per consumer

No consumer requires operator action. All enabled skills with assessable upstream file dependencies are reading data within their expected freshness windows.

## Healthy consumers

- planner — 1 dep (memory/state/planner-state.json), fresh.
- notegraph — 1 dep (memory/state/notegraph.json), fresh.
- suggest-edges — 1 dep (memory/state/suggest-edges.json), fresh.
- skillpacks — 1 dep (memory/state/skillpacks.json), fresh.
- surplus-pulse — 1 dep (memory/topics/surplus-pulse.md), fresh.
- compute-pulse — 1 dep (memory/topics/compute-pulse.md), fresh.
- compute-macro-correlate — 1 dep (memory/topics/compute-futures-macro-correlations.md), fresh.
- skill-freshness — 1 dep (memory/topics/skill-freshness-state.json), fresh.

+ 36 more all-fresh consumers (no assessable upstream file deps or only self-state reads).

## Source status

- `aeon.yml`: ~170 entries, 44 enabled
- Implicit references discovered: 22 (across all enabled SKILL.md files)
- Explicit `chains: consume:` edges: 0 (chains block is fully commented out)
- Files not yet on disk (skipped — implicit references that never existed): 6
  - `memory/topics/projects.md` (referenced by surplus-pulse; optional integration context)
  - `memory/topics/compute-tokens.md` (referenced by compute-pulse; optional watchlist)
  - `memory/topics/framework-watch-state.json` (referenced by ai-framework-watch; auto-created on first run)
  - `memory/topics/skill-graph-state.json` (referenced by skill-graph; auto-created on first run)
  - `memory/state/fleet-control-state.json` (referenced by fleet-control; auto-created on first run)
  - `memory/state/skill-repair-history.json` (referenced by skill-repair; auto-created on first run)
- Consumer scan skipped: `agi-tracker` is `enabled: true` in aeon.yml but `skills/agi-tracker/` directory is absent — no SKILL.md to audit; 11+ silent dispatches already logged in MEMORY.md.

### Sandbox note — mtime blindness

This run executes in a GHA shallow clone (single commit: `07a6718`, 2026-11-01T20:03Z). All on-disk file mtimes equal the checkout timestamp, and `git log -1 --format=%ct` returns the same single-commit timestamp for every file — both are useless for per-file aging. This run therefore:

- **Articles (`articles/*.md`):** derives age from the ISO date embedded in the filename — reliable.
- **Memory/topics and memory/state files:** cannot determine age from timestamps; marked as indeterminate and treated as OK (no false positives).

The unpatched [[skill-freshness-mtime-blind-in-gha]] bug means non-article dependencies may be silently stale without detection. The action-queue fix (multi-commit clone + `git log -1 --format=%ct`) is required before this skill can assess memory file freshness with confidence.

### Cross-skill article dependency audit (filename-derived ages)

No enabled skill has an explicit cross-skill article dependency (`articles/{other-skill}-${today}.md` reference) in its SKILL.md. Broad directory reads like "last 7 days of articles/" (reflect, self-review) do not produce assessable file-level edges.

Notable movement since yesterday's run (2026-11-01): **self-review recovered from 21d STALE to 1d OK** — `self-review-2026-11-01.md` was produced in the `07a6718` reflect-success commit. **vuln-scan is now ~378h old and will breach the 384h STALE boundary within ~6h** (by ~16:00 UTC today if vuln-scanner doesn't run — it won't; next scheduled run is Saturday 2026-11-07 at 16:00 UTC, by which point it will be ~22d / ~528h). No cross-skill consumer means no fleet flag fires, but the gap is widening.

| Producer | Most recent article | Age | Producer cadence | Threshold | Verdict |
|----------|--------------------|----|-----------------|-----------|---------|
| skill-freshness | 2026-11-01 | 1d (24h) | daily (28h) | 28h | OK |
| self-review | 2026-11-01 | 1d (24h) | weekly (192h) | 192h | OK (recovered from 21d STALE) |
| skill-analytics | 2026-10-21 | 12d (288h) | weekly (192h) | 192h | WARN — self-only consumer, no flag |
| vuln-scan | 2026-10-17 | ~16d (~378h) | weekly (192h) | 192h | WARN → STALE within ~6h — self-only consumer, no flag |
| cost-report | 2026-09-28 | 35d (840h) | weekly (192h) | 192h | STALE — self-only consumer, no flag |
| skill-evals | 2026-09-13 | 50d (1200h) | weekly (192h) | 192h | STALE — self-only consumer, no flag |

These gaps are fleet health signals (covered by skill-health and skill-analytics) but do not trigger skill-freshness flags because no enabled consumer has an explicit dependency on them.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from filename-derived dates (articles) or treated as indeterminate (state/topic files in GHA shallow clone) — this skill measures nothing it does not also report.*
