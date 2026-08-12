# Skill Analytics — 2026-08-12

**Verdict:** 2 scheduled skill(s) didn't run this window — ai-framework-watch, run-frequency-guard

*Window: last 7d · 166 runs across 41 skills · 100.0% success · 2 anomalies*

## Anomalies

| Flag | Skill | Detail | Action |
|------|-------|--------|--------|
| 🔴 SILENT | ai-framework-watch | scheduled `30 8 * * 1` (Mon 08:30 UTC) but zero runs in 7d window — 35th consecutive silent day | investigate messages.yml dispatcher wiring; see [[enabled-skills-can-never-dispatch]] |
| 🔴 SILENT | run-frequency-guard | scheduled `0 23 * * *` (daily 23:00 UTC) but zero runs in 7d window — 35th consecutive silent day | same root cause as ai-framework-watch; cron-state has no entry for either skill |

Both SILENT skills are confirmed as a known fleet gap per [[enabled-skills-can-never-dispatch]] (ISS-021 candidate, 34d carryover). Root cause: messages.yml dispatch matcher not wiring these skills to the runner despite `enabled: true` in aeon.yml.

## Top runners (by run count)

| # | Skill | Runs | Success | Last status | Dominant exit |
|---|-------|------|---------|-------------|---------------|
| 1 | pr-review (swarm-ai-research/swarm) | 14 | 93% | pending | uncategorized |
| 2 | planner | 7 | 100% | success | ok |
| 3 | fleet-control | 7 | 100% | success | uncategorized |
| 4 | github-monitor | 7 | 100% | success | uncategorized |
| 5 | goal-tracker | 7 | 86% | pending | uncategorized |
| 6 | issue-triage | 7 | 100% | success | ok |
| 7 | pr-tracker | 7 | 100% | success | ok |
| 8 | pr-triage (swarm-ai-research/swarm) | 7 | 100% | success | ok |
| 9 | reflect | 7 | 86% | pending | ok |
| 10 | skill-health | 7 | 86% | pending | ok |
| 11 | compute-futures-eda | 7 | 100% | success | ok |
| 12 | batch-health | 6 | 100% | success | ok |
| 13 | code-health | 6 | 100% | success | uncategorized |
| 14 | gitlawb-fleet-metrics | 6 | 100% | success | uncategorized |
| 15 | heartbeat | 6 | 100% | success | ok |

Note: skills showing 86% success (goal-tracker, reflect, skill-health) have 1 in-progress run at snapshot time; pr-review has 1 in-progress. None breach the LOW_SUCCESS threshold (all >80%).

## Failure rate (sorted, ≥1 failure)

Zero failures across 41 skills this window. The entire fleet reported 0 failed runs against 161 succeeded (5 in_progress at snapshot time). The chronic ISS-001 "DEGRADED" classification (38 skills with lifetime success_rate < 0.5 in cron-state) is a historical artefact — in-window the fleet is fully green.

## Exit taxonomy distribution

*Sourced from `memory/logs/*.md` — best-effort regex grep, see Step 5. Miss-rate ~15% expected; uncategorized captures FLEET_EMPTY, GLMETRICS_EMPTY, EMPTY_CONFIG, and un-patterned exits.*

| Bucket | Count | % | Top skills |
|--------|-------|---|------------|
| ok | ~105 | 63% | planner, notegraph, heartbeat, pr-tracker, pr-triage, reflect, skill-health, surplus-pulse, compute-futures-eda, batch-health, stale-content-pr-sweeper, memory-flush, memory-structural-dedupe |
| uncategorized | ~45 | 27% | fleet-control (FLEET_EMPTY), github-monitor (EMPTY_CONFIG), gitlawb-fleet-metrics (GLMETRICS_EMPTY), code-health (EMPTY_CONFIG), goal-tracker |
| skip_other | ~8 | 5% | suggest-edges (NOISE_ABORT × 4, NO_PROPOSALS × 2), pr-review (all-skip) |
| quiet | ~4 | 2% | skill-freshness (FRESHNESS_NO_CHANGE × 3, FRESHNESS_OK × 3) |
| error | 0 | 0% | — |
| skip_unchanged | 0 | 0% | — |
| new_info | 0 | 0% | — |
| partial | 0 | 0% | — |

**Fleet exit dominant:** ok (63%)

**Notable patterns:**
- `fleet-control`, `github-monitor`, `code-health`, `gitlawb-fleet-metrics` are running and succeeding (GHA confirms 100%) but short-circuit before doing meaningful work every single run — FLEET_EMPTY / EMPTY_CONFIG / GLMETRICS_EMPTY exits. These land as uncategorized here but are effectively silent no-ops driven by the `memory/watched-repos.md` gap (planner holding item, streak-7).
- `suggest-edges` has fired 6 times but produced 0 useful edge proposals — all runs either hit the templated-corpus NOISE_ABORT class (streak-4 of sim≥0.985 gitlawb templated pairs) or the NO_PROPOSALS_EQUIVALENT path. The GHA reports `success` because the skill exits cleanly; the *functional* success rate is 0/6 for user-facing value.

## Silent scheduled skills (enabled, zero runs)

| Skill | Schedule | Silent days |
|-------|----------|-------------|
| ai-framework-watch | `30 8 * * 1` (Mon 08:30 UTC) | 35 |
| run-frequency-guard | `0 23 * * *` (daily 23:00 UTC) | 35 |

Root cause per [[enabled-skills-can-never-dispatch]]: neither skill has a `memory/cron-state.json` entry, confirming zero lifetime dispatches. The messages.yml matcher is not wiring these despite `enabled: true` in aeon.yml. ISS-021 draft pending (23rd-day carryover as of 08-11; see MEMORY.md line 48).

## Source status

- skill-runs JSON: ok (161 succeeded / 0 failed / 5 in_progress / 0 cancelled)
- Window: 168h (2026-08-05T18:37:30Z → 2026-08-12T18:37:30Z)
- aeon.yml: ok
- cron-state.json: ok (42 skills; 0 with consecutive_failures ≥ 2)
- Daily logs scanned: 7/7 for exit taxonomy (2026-08-06 through 2026-08-12)

---
*Companion to `skill-health` (per-skill issue filing) and `heartbeat` (per-run pulse). Fleet-wide observability is the gap this skill closes. Methodology: GitHub Actions run history is ground truth for pass/fail; daily-log markers are best-effort secondary signal for exit taxonomy.*
