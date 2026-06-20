# Skill Freshness — 2026-06-20

**Verdict:** ✅ FRESHNESS_OK — all discovered dependencies are fresh or absent by design

*Audited 44 enabled skills · 11 non-self dependencies checked · 0 flagged*

## Flagged dependencies

*(None — all dependencies resolved to OK or were correctly absent.)*

## What this means per consumer

No consumer had a stale, missing, or warn-band dependency. Nothing to action.

## Healthy consumers

- planner — 1 dep (memory/state/planner-state.json, create-if-missing → skip), all fresh.
- batch-health — 0 discovered deps, all fresh.
- memory-flush — 0 discovered deps, all fresh.
- memory-structural-dedupe — 0 discovered deps, all fresh.

+ 40 more all-fresh consumers.

## Source status

- `aeon.yml`: 44 enabled skills parsed (of ~174 total skill entries on disk)
- Explicit `chains: consume:` edges: 0 (all chain blocks are commented out)
- Implicit references discovered: 11 non-self cross-skill deps
- Files not yet on disk (skipped — implicit references that never existed): 11
  - `memory/state/planner-state.json` (planner, create-if-missing)
  - `memory/state/fleet-control-state.json` (fleet-control, create-if-missing)
  - `memory/topics/framework-watch-state.json` (ai-framework-watch, create-if-missing)
  - `memory/topics/compute-pulse.md` (compute-pulse, create-if-missing)
  - `memory/topics/compute-tokens.md` (compute-pulse, optional)
  - `memory/topics/compute-futures-macro-correlations.md` (compute-macro-correlate, create-on-first-run)
  - `memory/topics/surplus-pulse.md` (surplus-pulse, create-if-missing)
  - `memory/topics/projects.md` (surplus-pulse, optional reference)
  - `articles/token-report-*.md` (heartbeat, optional — token-report disabled)
  - `.outputs/github-trending.md` (vuln-scanner, conditional — github-trending disabled)
  - `articles/push-recap-*.md` (weekly-shiplog, conditional — push-recap disabled)

**Producer cadence breakdown (enabled skills only):**
- Daily (23): planner, batch-health, memory-flush, memory-structural-dedupe, stale-content-pr-sweeper, issue-triage, pr-triage, pr-review, pr-tracker, github-monitor, code-health, surplus-pulse, compute-futures-eda, goal-tracker, skill-health, reflect, fleet-control, gitlawb-fleet-metrics, notegraph, suggest-edges, skill-freshness, run-frequency-guard, heartbeat
- Weekly (20): janitor, repo-revive, compute-pulse, compute-macro-correlate, changelog, vuln-scanner, agi-tracker, milestone-tracker, config-validator, skill-analytics, self-review, cost-report, ai-framework-watch, skill-evals, swarm-safety-eval, skill-update-check, weekly-shiplog, workflow-security-audit, skill-graph, skillpacks
- On-demand (1): skill-repair (reactive)

**On-disk file freshness (files that exist and were checked):**
| File | Class | Age | Threshold | Verdict |
|------|-------|-----|-----------|---------|
| `.outputs/code-health.md` | outputs | ~1 min | 4h | ✅ OK |
| `.outputs/github-monitor.md` | outputs | ~1 min | 4h | ✅ OK |
| `.outputs/issue-triage.md` | outputs | ~1 min | 4h | ✅ OK |
| `.outputs/janitor.md` | outputs | ~1 min | 4h | ✅ OK |
| `.outputs/memory-flush.md` | outputs | ~1 min | 4h | ✅ OK |
| `.outputs/memory-structural-dedupe.md` | outputs | ~1 min | 4h | ✅ OK |
| `.outputs/repo-revive.md` | outputs | ~1 min | 4h | ✅ OK |
| `.outputs/stale-content-pr-sweeper.md` | outputs | ~1 min | 4h | ✅ OK |
| `memory/topics/agi-tracker.md` | topics | ~1 min | 168h | ✅ OK |

*Note: `.outputs/` files are not currently consumed by any enabled skill (all `chains:` blocks are commented out). They are produced by daily skills as a chain-ready artifact; freshness is still tracked as a baseline for when chains are re-enabled.*

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
