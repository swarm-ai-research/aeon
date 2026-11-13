# Skill Freshness — 2026-11-13

**Verdict:** ✅ FRESHNESS_OK — 0 of 8 discovered dependencies flagged across 0 of 44 enabled consumers

*Audited 44 enabled skills · 8 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — all consumer dependencies are within their freshness window.)*

## What this means per consumer

*(No consumers with a verdict other than OK.)*

## Healthy consumers

- planner — 1 dep (`memory/state/planner-state.json`), all fresh.
- notegraph — 1 dep (`memory/state/notegraph.json`), all fresh.
- suggest-edges — 1 dep (`memory/state/suggest-edges.json`), all fresh.
- skillpacks — 1 dep (`memory/state/skillpacks.json`), all fresh.
- compute-macro-correlate — 1 dep (`memory/topics/compute-futures-macro-correlations.md`), all fresh.
- compute-futures-eda — 1 dep (`memory/topics/compute-futures-eda/`), all fresh.
- compute-pulse — 1 dep (`memory/topics/compute-pulse.md`), all fresh.
- skill-evals — 1 dep (`articles/skill-evals-*.md`, self-read, filtered from MISSING), all fresh.

+ 36 more all-fresh consumers.

## Observations (producer gaps, no active consumer impact)

The following producer outputs are stale by their path-class threshold but have **no active enabled consumer** reading them — they are not flagged per spec:

| Producer | Most recent output | Age | Threshold | Status | Active consumer? |
|----------|--------------------|-----|-----------|--------|-----------------|
| `.outputs/` (all 32 chain files) | 2026-11-11 (batch commit) | ~39h | 4h (chain) | STALE | No — chains commented out |
| `skill-analytics` | `articles/skill-analytics-2026-10-21.md` | 23d (552h) | 192h weekly → 384h 2× | STALE | `operator-scorecard` (disabled) |
| `skill-evals` | `articles/skill-evals-2026-09-13.md` | 61d (1464h) | 192h weekly → 384h 2× | STALE | `operator-scorecard` (disabled) |
| `self-review` | `articles/self-review-2026-11-01.md` | 12d (288h) | 192h weekly | WARN | None |

**Signal**: `skill-analytics` has not produced an article in 23 days; `skill-evals` in 61 days. Both are weekly skills that should fire on their cron. Likely ISS-006 slot casualties (both sit in dead 06Z/18Z slots). No consumer-side action today, but worth checking with `./scripts/skill-runs --skill skill-analytics --hours 720`.

## Source status

- `aeon.yml`: 155 entries, 44 enabled
- Explicit `chains: consume:` edges: 0 (all chain definitions are commented out)
- Implicit references discovered: 10 total; 8 surviving (2 skipped — implicit refs to files that never existed: `memory/topics/framework-watch-state.json`, `memory/topics/compute-tokens.md`)
- Cross-skill consumer dependencies (non-self-reference): 0
- Files not yet on disk (skipped — implicit refs, never existed): 2
- Note: file ages derived from `git log -1 --format=%ct` (mtime unreliable in GHA per [[skill-freshness-mtime-blind-in-gha]]); all files share commit timestamp 2026-11-11T17:22:59Z (single batch commit), age ~39.4h at audit time

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from git-tracked file timestamps — this skill measures nothing it does not also report.*
