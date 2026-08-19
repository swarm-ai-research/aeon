# Skill Analytics — 2026-08-19

**Verdict:** 2 scheduled skill(s) didn't run this window — ai-framework-watch, run-frequency-guard

*Window: last 7d · 171 runs across 40 skills · 100% success · 2 anomalies*

## Anomalies

| Flag | Skill | Detail | Action |
|------|-------|--------|--------|
| 🔴 SILENT | ai-framework-watch | scheduled `30 8 * * 1` (Mon 08:30 UTC) but zero runs in window | check workflow / scheduler — see [[enabled-skills-can-never-dispatch]], 43d+ silent |
| 🔴 SILENT | run-frequency-guard | scheduled `0 23 * * *` (daily 23:00 UTC) but zero runs in window | check workflow / scheduler — see [[enabled-skills-can-never-dispatch]], 43d+ silent |

## Top runners (by run count)

| # | Skill | Runs | Success | Last status | Dominant exit |
|---|-------|------|---------|-------------|---------------|
| 1 | pr-review | 14 | 100% | success | ok |
| 2 | batch-health | 7 | 100% | success | ok |
| 3 | code-health | 7 | 100% | success | ok |
| 4 | compute-futures-eda | 7 | 100% | success | ok |
| 5 | fleet-control | 7 | 100% | success | ok |
| 6 | github-monitor | 7 | 100% | success | ok |
| 7 | gitlawb-fleet-metrics | 7 | 100% | success | ok |
| 8 | goal-tracker | 7 | 100% | success | ok |
| 9 | heartbeat | 7 | 100% | success | ok |
| 10 | issue-triage | 7 | 100% | success | ok |
| 11 | planner | 7 | 100% | success | ok |
| 12 | pr-tracker | 7 | 100% | success | ok |
| 13 | pr-triage | 7 | 100% | success | ok |
| 14 | reflect | 7 | 100% | success | ok |
| 15 | skill-freshness | 7 | 100% | success | ok |

## Failure rate (sorted, ≥1 failure)

Zero failures across 40 skills this window.

## Exit taxonomy distribution

| Bucket | Count | % | Top skills |
|--------|-------|---|------------|
| ok | ~130 | ~76% | planner, heartbeat, skill-health, reflect, goal-tracker |
| uncategorized | ~41 | ~24% | skill-health (NOOP), skill-graph (NEW), skill-evals (REGRESSED), skill-update-check (NO_LOCK) |
| skip_unchanged | 0 | 0% | — |
| new_info | 0 | 0% | — |
| quiet | 0 | 0% | — |
| error | 0 | 0% | — |
| partial | 0 | 0% | — |

*Sourced from `memory/logs/*.md` — best-effort regex grep, see Step 5. `uncategorized` entries include skill-specific status codes (SKILL_HEALTH_NOOP, SKILL_GRAPH_NEW, SKILL_ANALYTICS_OK, etc.) that don't match the standard exit taxonomy markers.*

## Silent scheduled skills (enabled, zero runs)

| Skill | Schedule | Notes |
|-------|----------|-------|
| ai-framework-watch | `30 8 * * 1` (Mon 08:30 UTC) | 43d+ never-dispatched per [[enabled-skills-can-never-dispatch]] |
| run-frequency-guard | `0 23 * * *` (daily 23:00 UTC) | 43d+ never-dispatched per [[enabled-skills-can-never-dispatch]] |

*Every other enabled cron skill ran at least once in the window.*

## Source status

- skill-runs JSON: ok
- Window: 168h (2026-08-12T19:04:27Z → 2026-08-19T19:04:27Z)
- aeon.yml: ok
- cron-state.json: ok
- Daily logs scanned: 8/8 for exit taxonomy (2026-08-12 through 2026-08-19)

---
*Companion to `skill-health` (per-skill issue filing) and `heartbeat` (per-run pulse). Fleet-wide observability is the gap this skill closes. Methodology: GitHub Actions run history is ground truth for pass/fail; daily-log markers are best-effort secondary signal for exit taxonomy.*
