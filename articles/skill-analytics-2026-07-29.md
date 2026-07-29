# Skill Analytics — 2026-07-29

**Verdict:** 5 scheduled skills didn't run this window — ai-framework-watch, run-frequency-guard, agi-tracker, weekly-shiplog, compute-macro-correlate

*Window: last 7d · 146 runs across 26 skills · 99.3% success · 5 anomalies*

## Anomalies

| Flag | Skill | Detail | Action |
|------|-------|--------|--------|
| 🔴 SILENT | ai-framework-watch | scheduled `30 8 * * 1` (Mon 08:30) — 21st consecutive never-dispatched day | check `messages.yml` matcher; no cron-state entry |
| 🔴 SILENT | run-frequency-guard | scheduled `0 23 * * *` (daily 23:00) — 21st consecutive never-dispatched day | check `messages.yml` matcher; no cron-state entry |
| 🔴 SILENT | agi-tracker | scheduled `0 13 * * 1` (Mon 13:00) — zero runs in window; last dispatch 07-20, 4th consecutive weekly miss | restore SKILL.md or set `enabled: false` in aeon.yml:188 |
| 🔴 SILENT | weekly-shiplog | scheduled `0 9 * * 1` (Mon 09:00) — zero runs in window; last dispatch 07-20, 07-27 Monday slot missed | check workflow trigger / scheduler pocket |
| 🔴 SILENT | compute-macro-correlate | scheduled `30 6 * * 0` (Sun 06:30) — zero runs in window; last dispatch 07-19, 07-26 Sunday slot missed | check workflow trigger / scheduler pocket |

## Top runners (by run count)

| # | Skill | Runs | Success | Last status | Dominant exit |
|---|-------|------|---------|-------------|---------------|
| 1 | goal-tracker | 8 | 87.5%* | pending | ok |
| 2 | reflect | 8 | 87.5%* | pending | ok |
| 3 | skill-health | 8 | 87.5%* | pending | ok |
| 4 | code-health | 7 | 100% | success | ok |
| 5 | surplus-pulse | 7 | 100% | success | ok |
| 6 | compute-futures-eda | 6 | 100% | success | uncategorized |
| 7 | fleet-control | 6 | 100% | success | uncategorized |
| 8 | github-monitor | 6 | 100% | success | uncategorized |
| 9 | issue-triage | 6 | 100% | success | ok |
| 10 | pr-tracker | 6 | 100% | success | ok |
| 11 | pr-triage | 6 | 100% | success | ok |
| 12 | batch-health | 5 | 100% | success | ok |
| 13 | gitlawb-fleet-metrics | 5 | 100% | success | uncategorized |
| 14 | heartbeat | 5 | 100% | success | ok |
| 15 | planner | 5 | 100% | success | ok |

*Success % based on completed runs; 1 run currently in progress each.

## Failure rate (sorted, ≥1 failure)

| Skill | Runs | Failures | Success rate | Last conclusion |
|-------|------|----------|--------------|-----------------|
| skill-freshness | 5 | 1 | 80% | success |

Only 1 skill logged a failure this window. Zero ALL_FAIL or CONSECUTIVE_FAILURES conditions.

## Exit taxonomy distribution

| Bucket | Count | % | Top skills |
|--------|-------|---|------------|
| ok | ~108 | ~68% | goal-tracker, reflect, surplus-pulse, issue-triage, planner |
| uncategorized | ~30 | ~19% | fleet-control (FLEET_EMPTY), github-monitor (EMPTY_CONFIG), gitlawb-fleet-metrics (GLMETRICS_EMPTY), compute-futures-eda |
| quiet | ~12 | ~8% | notegraph (silent-exit on timestamp-only diff) |
| skip_unchanged | 0 | 0% | — |
| new_info | 0 | 0% | — |
| skip_other | 0 | 0% | — |
| error | ~5 | ~3% | skill-freshness (1 confirmed failure run) |
| partial | 0 | 0% | — |

Sourced from `memory/logs/*.md` — best-effort regex grep (see methodology). "Uncategorized" captures early-exit statuses (FLEET_EMPTY, EMPTY_CONFIG, GLMETRICS_EMPTY) that don't match the `_OK`/`_SKIP*`/`_ERROR` taxonomy — these represent correctly-behaving short-circuits, not silent failures.

## Silent scheduled skills (enabled, zero runs in window)

| Skill | Schedule | Last dispatch | Notes |
|-------|----------|---------------|-------|
| ai-framework-watch | `30 8 * * 1` (Mon 08:30) | never | 21 consecutive silent days; no cron-state entry per [[enabled-skills-can-never-dispatch]] |
| run-frequency-guard | `0 23 * * *` (daily 23:00) | never | 21 consecutive silent days; no cron-state entry per [[enabled-skills-can-never-dispatch]] |
| agi-tracker | `0 13 * * 1` (Mon 13:00) | 2026-07-20 | 4th consecutive weekly miss; HEALTHY-but-empty class per [[agi-tracker-missing-skill-md-dispatches-no-op]] |
| weekly-shiplog | `0 9 * * 1` (Mon 09:00) | 2026-07-20 | 07-27 Monday slot not fired; pocket interference likely |
| compute-macro-correlate | `30 6 * * 0` (Sun 06:30) | 2026-07-19 | 07-26 Sunday slot not fired; pocket interference or dispatch gap |

## Source status

- skill-runs JSON: ok (146 total runs, 1 failure, 5 in_progress)
- Window: 168h (2026-07-22T18:41:58Z → 2026-07-29T18:41:58Z)
- aeon.yml: ok (42 cron-scheduled enabled skills + 1 reactive)
- cron-state.json: ok (42 tracked + 2 never-dispatched = 44 total)
- Daily logs scanned: 7/7 (2026-07-23 through 2026-07-29) for exit taxonomy

**Data gap note:** ~12 skills ran within the window per cron-state but do not appear in the `skill-runs` snapshot — including pr-review (daily 09:00+18:00), suggest-edges (daily 05:30), skill-evals, workflow-security-audit, skill-graph, self-review, skill-update-check, swarm-safety-eval, skillpacks, repo-revive, vuln-scanner, and the prior skill-analytics run (07-22). These are captured in daily logs and cron-state but not in GitHub Actions run history as returned by `./scripts/skill-runs`. Pass/fail ground truth reflects only the 26 skills the script captured; the ~12 data-gap skills are excluded from anomaly classification.

---
*Companion to `skill-health` (per-skill issue filing) and `heartbeat` (per-run pulse). Fleet-wide observability is the gap this skill closes. Methodology: GitHub Actions run history is ground truth for pass/fail; daily-log markers are best-effort secondary signal for exit taxonomy.*
