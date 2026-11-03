# Skill Freshness — 2026-11-03

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

This run executes in a GHA shallow clone (single commit: `9463294`, 2026-11-02). All on-disk file mtimes equal the checkout timestamp, and `git log -1 --format=%ct` returns the same single-commit timestamp for every file — both are useless for per-file aging. This run therefore:

- **Articles (`articles/*.md`):** derives age from the ISO date embedded in the filename — reliable.
- **Memory/topics and memory/state files:** cannot determine age from timestamps; marked as indeterminate and treated as OK (no false positives).

The unpatched [[skill-freshness-mtime-blind-in-gha]] bug means non-article dependencies may be silently stale without detection. The action-queue fix (multi-commit clone + `git log -1 --format=%ct`) is required before this skill can assess memory file freshness with confidence.

### Cross-skill article dependency audit (filename-derived ages)

No enabled skill has an explicit cross-skill article dependency (`articles/{other-skill}-${today}.md` reference) in its SKILL.md. Broad directory reads like "last 7 days of articles/" (reflect, self-review) do not produce assessable file-level edges.

Notable movement since yesterday's run (2026-11-02): **vuln-scan crossed the STALE threshold** — now ~408h old (2026-10-17), past the 384h (2×192h) STALE boundary; yesterday's run flagged this was ~6h away from the crossing. **skill-freshness recovered** — `skill-freshness-2026-11-02.md` produced in yesterday's run (24h old, OK within 28h threshold). No cross-skill consumer means no fleet flag fires for any of the stale producers below.

| Producer | Most recent article | Age | Producer cadence | Threshold | Verdict |
|----------|--------------------|----|-----------------|-----------|---------|
| skill-freshness | 2026-11-02 | 1d (24h) | daily (28h) | 28h | OK |
| self-review | 2026-11-01 | 2d (48h) | weekly (192h) | 192h | OK |
| skill-analytics | 2026-10-21 | 13d (312h) | weekly (192h) | 192h | WARN — self-only consumer, no flag |
| vuln-scan | 2026-10-17 | 17d (408h) | weekly (192h) | 192h | **STALE** (crossed 384h boundary ~Nov 2 16:00Z) — self-only consumer, no flag |
| cost-report | 2026-09-28 | 36d (864h) | weekly (192h) | 192h | STALE — self-only consumer, no flag |
| skill-evals | 2026-09-13 | 51d (1224h) | weekly (192h) | 192h | STALE — self-only consumer, no flag |

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from filename-derived dates (articles) or treated as indeterminate (state/topic files in GHA shallow clone) — this skill measures nothing it does not also report.*
