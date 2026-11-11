# Skill Freshness — 2026-11-11

**Verdict:** ✅ FRESHNESS_OK — all 9 tracked dependencies are within their freshness thresholds across 44 enabled consumers

*Audited 44 enabled skills · 9 dependencies checked · 0 flagged*

## Flagged dependencies

*(No flagged dependencies — all tracked files are fresh.)*

## Healthy consumers

- planner — 1 dep (`memory/state/planner-state.json`), all fresh.
- suggest-edges — 1 dep (`memory/state/suggest-edges.json`), all fresh.
- notegraph — 1 dep (`memory/state/notegraph.json`), all fresh.
- skillpacks — 1 dep (`memory/state/skillpacks.json`), all fresh.
- pr-tracker — 1 dep (`memory/state/pr-tracker.json`), all fresh.
- compute-pulse — 1 dep (`memory/topics/compute-pulse.md`), all fresh.
- surplus-pulse — 1 dep (`memory/topics/surplus-pulse.md`), all fresh.
- compute-macro-correlate — 1 dep (`memory/topics/compute-futures-macro-correlations.md`), all fresh.
+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: ~156 entries, 44 enabled
- Implicit references discovered: 9
- Explicit `chains: consume:` edges: 0 (the only chain, `daily-routine`, is commented out)
- Files not yet on disk (skipped — implicit): ~12 (e.g. `memory/topics/compute-tokens.md`, `memory/topics/watched-repos.md`, `memory/state/skill-repair-history.json`)

## Methodology note

**GHA mtime caveat (`skill-freshness-mtime-blind-in-gha`):** In this environment all files carry the same checkout mtime from the git clone operation. File ages were cross-checked against `git log -1 --format=%ct` per-file timestamps, which revealed all tracked files share the same most-recent commit (`545a99f`, ~16h ago). The pending action-queue fix (use `git log -1 --format=%ct` instead of `stat --format=%Y`) is confirmed still needed to get per-file git commit timestamps in future runs.

**Stale articles observed (not flagged):** `articles/skill-evals-2026-09-13.md` (59 days), `articles/skill-analytics-2026-10-21.md` (21 days), and `articles/self-review-2026-11-01.md` (10 days) are past their weekly thresholds. However, none are consumed by currently-enabled skills via pattern-matched implicit references — only disabled skills (`operator-scorecard`, `signal-verdict`) and self-reads (excluded per spec) reference them. These reflect ISS-006 slot outages, not a consumer-staleness gap.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
