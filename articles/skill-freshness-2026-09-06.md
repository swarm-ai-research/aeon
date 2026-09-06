# Skill Freshness — 2026-09-06

**Verdict:** ✅ FRESHNESS_OK — all enabled consumers' tracked dependencies are within their freshness windows

*Audited 43 enabled skills · 7 dependencies checked · 0 flagged*

## Flagged dependencies

*(none)*

## What this means per consumer

*(no consumers with verdict ≠ OK)*

## Healthy consumers

- planner — 1 dep (memory/state/planner-state.json), all fresh.
- surplus-pulse — 1 dep (memory/topics/surplus-pulse.md), all fresh.
- compute-pulse — 1 dep (memory/topics/compute-pulse.md), all fresh.
- skill-freshness — 1 dep (memory/topics/skill-freshness-state.json), all fresh.
- heartbeat — implicit articles/token-report-*.md reference skipped (on_demand producer).
- notegraph — 1 dep (memory/state/notegraph.json), all fresh.
- suggest-edges — 1 dep (memory/state/suggest-edges.json), all fresh.

+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: 88 entries parsed, 43 enabled (1 reactive skill-repair excluded as consumer)
- Implicit references discovered: 12 (post-grep, pre-filter)
- Explicit `chains: consume:` edges: 0 (all chains currently commented out)
- Files not yet on disk (skipped — implicit references that never existed): 3
  - `memory/topics/framework-watch-state.json` (ai-framework-watch own state, implicit MISSING → not flagged)
  - `memory/topics/compute-tokens.md` (compute-pulse optional input, implicit MISSING → not flagged)
  - `memory/topics/projects.md` (surplus-pulse optional input, implicit MISSING → not flagged)

## Notes

**Dedup status: FRESHNESS_NO_CHANGE.** Flagged fingerprint is identical to the 2026-09-04 run (sha1 of empty set = `da39a3ee5e6b4b0d3255bfef95601890afd80709`; 0 flagged entries both runs). Last run was 2 days ago, within the 7-day re-emit window — notification suppressed.

**Known limitation: single-commit repository.** All on-disk files share the same git log timestamp (2026-09-06 00:10 UTC, stale-content-pr-sweeper bulk commit). This means `git log -1 --format=%ct` returns the same 8.8h age for all files, making per-file staleness indistinguishable at the git level. The correct ages must be inferred from file-name dates where available:

- `memory/state/daily-plan-*.md` newest: `2026-09-01.md` — planner last ran 5 days ago (consistent with ISS-006 06:00Z pocket dead, planner runs at 06:30Z)
- `memory/topics/compute-futures-eda/` newest: `2026-09-04.md` — compute-futures-eda last ran 2 days ago (consistent with ISS-006 06:00Z pocket outage on 09-05/06)
- `memory/topics/compute-futures-macro-correlations.md` — MISSING (on unmerged branch `compute-macro/2026-08-16` per MEMORY.md)

These filename-date observations confirm ISS-006 batch outage but fall outside the scope of the freshness thresholds: `memory/state/` threshold is 30 days (5 days well within), `memory/topics/compute-futures-eda/` is a subdirectory not captured by the topic-file grep pattern. No threshold violations result.

**Action item carried forward:** Fix this SKILL.md to use filename-date inference for state files alongside git log, per [[skill-freshness-mtime-blind-in-gha]].

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk git log timestamps — this skill measures nothing it does not also report.*
