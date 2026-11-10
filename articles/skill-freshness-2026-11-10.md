# Skill Freshness — 2026-11-10

**Verdict:** ✅ FRESHNESS_OK — all 9 tracked dependencies are within their freshness windows

*Audited 44 enabled skills · 9 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — all tracked dependencies are fresh.)*

## Healthy consumers

- compute-pulse — 2 deps (compute-pulse.md, compute-tokens.md†), all fresh.
- compute-macro-correlate — 1 dep (compute-futures-macro-correlations.md), all fresh.
- surplus-pulse — 2 deps (surplus-pulse.md, projects.md†), all fresh.
- pr-tracker — 2 deps (pr-status.md, pr-tracker.json), all fresh.
- planner — 1 dep (planner-state.json), all fresh.
- notegraph — 1 dep (notegraph.json), all fresh.
- skillpacks — 1 dep (skillpacks.json), all fresh.
- suggest-edges — 1 dep (suggest-edges.json), all fresh.

*† dependency path not on disk — implicit ref to never-created file; not flagged per spec.*

+ 36 more all-fresh consumers (no tracked file dependencies identified).

## Source status

- `aeon.yml`: 109 entries, 44 enabled
- Implicit references discovered: 9
- Explicit `chains: consume:` edges: 0
- Files not yet on disk (skipped — implicit references that never existed): 4
  - `memory/topics/watched-repos.md` — referenced by github-monitor, code-health, repo-revive, changelog, weekly-shiplog; skills short-circuit gracefully when absent
  - `memory/topics/compute-tokens.md` — optional override for compute-pulse token watchlist
  - `memory/topics/projects.md` — optional baseline for surplus-pulse
  - `memory/state/fleet-control-state.json` — created on first fleet-control run; not yet present

## Notes

All dependency timestamps derive from the most recent git commit (2026-11-09T18:49:32Z, single-commit shallow clone). The [known fix](../memory/MEMORY.md) to use `git log -1 --format=%ct` over `stat --format=%Y` is pending; in this environment both return the same value because the working tree was committed in one shot. Filename dates on articles confirm the articles directory skew: skill-evals last ran 2026-09-13 (58 d), skill-analytics last ran 2026-10-21 (20 d), self-review last ran 2026-11-01 (9 d). These are **producer** gaps — no currently-enabled consumer has an explicit dependency on those files, so they do not raise the fleet verdict. If operator-scorecard or signal-verdict are re-enabled they will immediately surface a STALE reading against skill-analytics and skill-evals.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
