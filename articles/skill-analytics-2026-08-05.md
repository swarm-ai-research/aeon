# Skill Analytics — 2026-08-05

**Verdict:** 4 scheduled skill(s) didn't run this window — run-frequency-guard, ai-framework-watch, agi-tracker, cost-report

*Window: last 7d · 160 runs across 39 skills · 100.0% success · 8 anomalies*

## Anomalies

| Flag | Skill | Detail | Action |
|------|-------|--------|--------|
| 🔴 SILENT | run-frequency-guard | scheduled `0 23 * * *` but zero runs in window | [[enabled-skills-can-never-dispatch]] — no cron-state entry; 27+ silent days; ISS-021 candidate |
| 🔴 SILENT | ai-framework-watch | scheduled `30 8 * * 1` but zero runs in window | [[enabled-skills-can-never-dispatch]] — no cron-state entry; 27+ silent days; ISS-021 candidate |
| 🔴 SILENT | agi-tracker | scheduled `0 13 * * 1` but zero runs in window | [[agi-tracker-missing-skill-md-dispatches-no-op]] — SKILL.md missing, dispatches no-op; set `enabled: false` on aeon.yml:188 or author SKILL.md |
| 🔴 SILENT | cost-report | scheduled `0 7 * * 1` but zero runs in window | missed Mon 08-03 slot inside ISS-020 batch outage; next slot Mon 2026-08-10 |
| 🟡 ALL_SKIP | fleet-control | 7 runs, all FLEET_EMPTY | `memory/instances.json` empty — populate to get useful output |
| 🟡 ALL_SKIP | github-monitor | 7 runs, all EMPTY_CONFIG | `memory/watched-repos.md` missing — populate or disable |
| 🟡 ALL_SKIP | gitlawb-fleet-metrics | 7 runs, all GLMETRICS_EMPTY | no GitLawb fleet registered in `memory/gitlawb-fleet.json` |
| 🟡 ALL_SKIP | goal-tracker | 7 runs, all NO_GOALS | no `## Goals` section in MEMORY.md — add one or accept steady-state silence |

## Top runners (by run count)

| # | Skill | Runs | Success | Last status | Dominant exit |
|---|-------|------|---------|-------------|---------------|
| 1 | pr-review | 14 | 93% | pending | ok |
| 2 | batch-health | 7 | 100% | success | ok |
| 3 | code-health | 7 | 100% | success | ok |
| 4 | fleet-control | 7 | 100% | success | skip_other |
| 5 | github-monitor | 7 | 100% | success | skip_other |
| 6 | gitlawb-fleet-metrics | 7 | 100% | success | skip_other |
| 7 | goal-tracker | 7 | 86% | pending | skip_other |
| 8 | heartbeat | 7 | 100% | success | ok |
| 9 | issue-triage | 7 | 100% | success | ok |
| 10 | notegraph | 7 | 100% | success | ok |
| 11 | reflect | 7 | 86% | pending | ok |
| 12 | skill-freshness | 7 | 100% | success | ok |
| 13 | skill-health | 7 | 86% | pending | ok |
| 14 | stale-content-pr-sweeper | 7 | 100% | success | ok |
| 15 | suggest-edges | 7 | 100% | success | ok |

*(surplus-pulse also at 7 runs/100%, just outside top 15 display; compute-futures-eda at 6 runs/100%)*

## Failure rate (sorted, ≥1 failure)

Zero failures across 39 skills this window. All 160 runs concluded success or are in_progress.

## Exit taxonomy distribution

| Bucket | Skills with dominant | Notes |
|--------|---------------------|-------|
| ok | ~21 | heartbeat, batch-health, notegraph, reflect, pr-review, pr-tracker, surplus-pulse, skill-health, stale-content-pr-sweeper, suggest-edges, issue-triage, skill-freshness, planner, memory-flush, memory-structural-dedupe, milestone-tracker, janitor, pr-triage, code-health, compute-futures-eda, compute-pulse |
| skip_other | ~7 | fleet-control (FLEET_EMPTY), github-monitor (EMPTY_CONFIG), gitlawb-fleet-metrics (GLMETRICS_EMPTY), goal-tracker (NO_GOALS), swarm-safety-eval (SSE_EMPTY), weekly-shiplog (SHIPLOG_NO_REPOS), changelog (ABORT_NO_CONFIG) |
| uncategorized | ~10 | config-validator, repo-revive, self-review, skill-analytics, skill-evals, skill-graph, skill-update-check, suggest-edges (partial), vuln-scanner, workflow-security-audit — log markers absent or non-standard exit strings |
| skip_unchanged | ~1 | skillpacks (SKILLPACKS_NO_CHANGE) |
| error | 0 | — |
| partial | 0 | — |

*(Sourced from `memory/logs/*.md` — best-effort regex grep. Cell-aligns to ground-truth pass/fail counts in the Top runners table.)*

## Silent scheduled skills (enabled, zero runs)

| Skill | Schedule | Context |
|-------|----------|---------|
| run-frequency-guard | `0 23 * * *` (daily) | 27+ silent days; never dispatched — no cron-state entry; [[enabled-skills-can-never-dispatch]]; ISS-021 candidate (draft 17th-day carryover) |
| ai-framework-watch | `30 8 * * 1` (Mon) | 27+ silent days; never dispatched — same class; ISS-021 candidate |
| agi-tracker | `0 13 * * 1` (Mon) | Last ran 2026-07-20; SKILL.md missing → dispatches no-op; 6th silent-risk slot would be Mon 2026-08-10; [[agi-tracker-missing-skill-md-dispatches-no-op]] |
| cost-report | `0 7 * * 1` (Mon) | Last ran 2026-07-27; missed Mon 08-03 slot inside ISS-020 batch outage (planner+compute-futures-eda+cost-report all silent); next slot Mon 2026-08-10 |

**Note on planner:** Not SILENT (2 runs in window), but running far below daily cadence (2/7 expected). All 3 consecutive post-08-02 06:30Z slots were silent (08-03 inside ISS-020 outage, 08-04 and 08-05 continuing drift per [[pocket-slot-migration-confirmed-by-3-day-sustained-late-delivery]]). Below the SILENT threshold but worth watching.

## Source status

- skill-runs JSON: ok (exit 0, 160 runs, 39 skills, 0 failures)
- Window: 168h (2026-07-29T18:52Z → 2026-08-05T18:52Z)
- aeon.yml: ok
- cron-state.json: ok (42 tracked skills + 2 never-dispatched = 44 total)
- Daily logs scanned: 8/8 for exit taxonomy (2026-07-29 through 2026-08-05)

---
*Companion to `skill-health` (per-skill issue filing) and `heartbeat` (per-run pulse). Fleet-wide observability is the gap this skill closes. Methodology: GitHub Actions run history is ground truth for pass/fail; daily-log markers are best-effort secondary signal for exit taxonomy.*
