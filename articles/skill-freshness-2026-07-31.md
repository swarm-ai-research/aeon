# Skill Freshness — 2026-07-31

**Verdict:** ✅ FRESHNESS_OK — all dependency-bearing consumers are reading files within their freshness windows

*Audited 44 enabled skills · 4 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — all scored dependencies are within threshold.)*

## What this means per consumer

All consumers with real, non-self, non-optional dependencies scored OK. No action required.

## Healthy consumers

- surplus-pulse — 1 dep (memory/topics/surplus-pulse.md), all fresh.
- compute-pulse — 1 dep (memory/topics/compute-pulse.md), all fresh.
- planner — 1 dep (memory/state/planner-state.json), all fresh.
- pr-tracker — 1 dep (memory/topics/pr-status.md), all fresh.

+ 40 more all-fresh consumers (no real cross-consumer file reads detected).

## Source status

- `aeon.yml`: 166 entries, 44 enabled
- Implicit references discovered: 28 (across all enabled SKILL.md files)
- Explicit `chains: consume:` edges: 0 (chains block is commented out)
- Files not yet on disk (skipped — implicit references that never existed or handled gracefully): 10

### Scored dependencies

| Consumer | Dependency | Class | Age | Threshold | Severity |
|----------|-----------|-------|-----|-----------|----------|
| surplus-pulse | `memory/topics/surplus-pulse.md` | memory/topics | 2.5h | 168h | ✅ OK |
| compute-pulse | `memory/topics/compute-pulse.md` | memory/topics | 2.5h | 168h | ✅ OK |
| planner | `memory/state/planner-state.json` | memory/state | 2.5h | 720h | ✅ OK |
| pr-tracker | `memory/topics/pr-status.md` | memory/topics | 2.5h | 168h | ✅ OK |

All files were committed in snapshot `7f0fdb5` at 2026-07-31 07:09:28 UTC. Age computed against audit time 09:33 UTC ≈ 2.5h. All well within class thresholds.

### Implicit missing files (not flagged — implicit references only)

These files were referenced in SKILL.md files but do not exist on disk. Per policy, MISSING only fires for explicit `chains: consume:` edges. All are either first-run-create patterns or optional inputs:

| Consumer | Missing path | Notes |
|----------|-------------|-------|
| ai-framework-watch | `memory/topics/framework-watch-state.json` | Creates on first run |
| fleet-control | `memory/state/fleet-control-state.json` | Creates on first run |
| skill-repair | `memory/state/skill-repair-history.json` | Creates on first run |
| repo-revive | `memory/topics/watched-repos.md` | Exits cleanly if absent (REPO_REVIVE_NO_CONFIG) |
| repo-revive | `memory/topics/stale-models.md` | Optional feature gate |
| surplus-pulse | `memory/topics/projects.md` | Optional context file |
| pr-review | `memory/topics/pr-review-rules.md` | Optional rules file |
| compute-futures-eda | `memory/gitlawb-compute-futures-proofs/*.csv` | No CSV files yet; skill exits cleanly |
| gitlawb-fleet-metrics | `memory/gitlawb-fleet.json` | Empty fleet → GLMETRICS_EMPTY, no error |
| compute-macro-correlate | `memory/topics/compute-futures-macro-correlations.md` | Creates on first run |

### Filtered references

The following references were excluded from scoring:
- **Own-output** (self-state-keeping): notegraph→state/notegraph.json, skillpacks→state/skillpacks.json, skill-freshness→topics/skill-freshness-state.json, skill-graph→topics/skill-graph-state.json, compute-futures-eda→topics/compute-futures-eda/ (prior runs)
- **Disabled producer**: heartbeat→articles/token-report-*.md (token-report disabled), weekly-shiplog→articles/push-recap-*.md (push-recap disabled)
- **Own prior article** (idempotency check): weekly-shiplog, skill-evals, swarm-safety-eval, fleet-control, workflow-security-audit reading their own previous articles
- **General directory pattern** (no specific filename): reflect→memory/topics/*.md (glob, not a named-file dep)

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from git-log timestamps (per [[skill-freshness-mtime-blind-in-gha]]) — this skill measures nothing it does not also report.*
