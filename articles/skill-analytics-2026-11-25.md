# Skill Analytics — 2026-11-25

**Verdict:** 24 scheduled skill(s) didn't run this window — planner, suggest-edges, compute-futures-eda, pr-triage, pr-tracker (and 19 more)

*Window: last 7d · 56 runs across 19 skills · 100% success · 27 anomalies*

## Anomalies

| Flag | Skill | Detail | Action |
|------|-------|--------|--------|
| 🔴 SILENT | planner | scheduled `30 6 * * *` but zero runs in window | check workflow / scheduler (ISS-006 06Z dead slot) |
| 🔴 SILENT | suggest-edges | scheduled `30 5 * * *` but zero runs in window | check workflow / scheduler (ISS-006 05Z dead slot) |
| 🔴 SILENT | compute-futures-eda | scheduled `0 6 * * *` but zero runs in window | check workflow / scheduler (ISS-006 06Z dead slot) |
| 🔴 SILENT | memory-flush | scheduled `0 6 2/2 * *` but zero runs in window | check workflow / scheduler (ISS-006 06Z dead slot) |
| 🔴 SILENT | memory-structural-dedupe | scheduled `10 6 2/2 * *` but zero runs in window | check workflow / scheduler (ISS-006 06Z dead slot) |
| 🔴 SILENT | pr-triage | scheduled `30 9 * * *` but zero runs in window | check workflow / scheduler |
| 🔴 SILENT | pr-tracker | scheduled `0 10 * * *` but zero runs in window | check workflow / scheduler |
| 🔴 SILENT | run-frequency-guard | scheduled `0 23 * * *` but zero runs in window | check workflow / scheduler (ISS-027: may lack SKILL.md) |
| 🔴 SILENT | janitor | scheduled `30 5 * * 0` but zero runs in window (Sun 11-22) | check workflow / scheduler (Sunday cohort silent) |
| 🔴 SILENT | config-validator | scheduled `0 7 * * 0` but zero runs in window (Sun 11-22) | check workflow / scheduler (Sunday cohort silent) |
| 🔴 SILENT | swarm-safety-eval | scheduled `30 7 * * 0` but zero runs in window (Sun 11-22) | check workflow / scheduler (Sunday cohort silent) |
| 🔴 SILENT | skill-evals | scheduled `0 9 * * 0` but zero runs in window (Sun 11-22) | check workflow / scheduler (Sunday cohort silent) |
| 🔴 SILENT | workflow-security-audit | scheduled `0 16 * * 0` but zero runs in window (Sun 11-22) | check workflow / scheduler (Sunday cohort silent) |
| 🔴 SILENT | skill-graph | scheduled `0 17 * * 0` but zero runs in window (Sun 11-22) | check workflow / scheduler (Sunday cohort silent) |
| 🔴 SILENT | skillpacks | scheduled `0 6 * * 0` but zero runs in window (Sun 11-22) | check workflow / scheduler (Sunday cohort silent) |
| 🔴 SILENT | compute-macro-correlate | scheduled `30 6 * * 0` but zero runs in window (Sun 11-22) | check workflow / scheduler (Sunday 06Z dead slot) |
| 🔴 SILENT | self-review | scheduled `30 18 * * 0` but zero runs in window (Sun 11-22) | check workflow / scheduler (Sunday cohort silent) |
| 🔴 SILENT | repo-revive | scheduled `0 10 * * 6` but zero runs in window (Sat 11-21) | check workflow / scheduler |
| 🔴 SILENT | vuln-scanner | scheduled `0 16 * * 6` but zero runs in window (Sat 11-21) | check workflow / scheduler |
| 🔴 SILENT | ai-framework-watch | scheduled `30 8 * * 1` but zero runs in window (Mon 11-23) | check workflow / scheduler (ISS-027: may lack SKILL.md) |
| 🔴 SILENT | cost-report | scheduled `0 7 * * 1` but zero runs in window (Mon 11-23) | check workflow / scheduler |
| 🔴 SILENT | milestone-tracker | scheduled `0 12 * * 1` but zero runs in window (Mon 11-23) | check workflow / scheduler |
| 🔴 SILENT | agi-tracker | scheduled `0 13 * * 1` but zero runs in window (Mon 11-23) | check workflow / scheduler (no SKILL.md) |
| 🔴 SILENT | changelog | scheduled `0 16 * * 1` but zero runs in window (Mon 11-23) | check workflow / scheduler |
| 🟠 LOW_SUCCESS | goal-tracker | 75% (3/4) — 1 run still in_progress, not a failure | monitor; likely clears on completion |
| 🟠 LOW_SUCCESS | reflect | 75% (3/4) — 1 run still in_progress, not a failure | monitor; likely clears on completion |
| 🟠 LOW_SUCCESS | skill-health | 75% (3/4) — 1 run still in_progress, not a failure | monitor; likely clears on completion |

**Note:** The 24 SILENT skills split into three cohorts: (1) 05Z/06Z daily dead slots (5 skills — ongoing ISS-006); (2) Sunday Nov 22 total silence (9 skills — entire Sunday cohort dropped); (3) Saturday/Monday one-shot misses (7 skills — Sat 11-21 Sat-cohort + Mon 11-23 ISS-047). The 3 LOW_SUCCESS flags are all in_progress artifacts from the current batch fire, not genuine failure streaks.

## Top runners (by run count)

| # | Skill | Runs | Success | Last status | Dominant exit |
|---|-------|------|---------|-------------|---------------|
| 1 | pr-review | 7 | 86% | pending | skip-other (1 FULL_SKIP) |
| 2 | batch-health | 4 | 100% | success | ok |
| 3 | gitlawb-fleet-metrics | 4 | 100% | success | uncategorized |
| 4 | goal-tracker | 4 | 75%* | pending | ok |
| 5 | heartbeat | 4 | 100% | success | ok |
| 6 | reflect | 4 | 75%* | pending | ok |
| 7 | skill-freshness | 4 | 100% | success | ok |
| 8 | skill-health | 4 | 75%* | pending | ok |
| 9 | fleet-control | 3 | 100% | success | uncategorized |
| 10 | github-monitor | 3 | 100% | success | quiet |
| 11 | issue-triage | 3 | 100% | success | ok |
| 12 | stale-content-pr-sweeper | 3 | 100% | success | ok |
| 13 | code-health | 2 | 100% | success | uncategorized |
| 14 | skill-analytics | 2 | 50%* | pending | ok |
| 15 | compute-pulse | 1 | 100% | success | ok |

*in_progress run counted in denominator; failure=0 for all.

## Failure rate (sorted, ≥1 failure)

Zero failures across 19 active skills this window. All 56 completed runs succeeded (5 currently in_progress).

## Exit taxonomy distribution

*Sourced from `memory/logs/*.md` — best-effort regex grep (Step 5). ~50% coverage; uncategorized does not imply unhealthy.*

| Bucket | Count | % | Top skills |
|--------|-------|---|------------|
| ok | ~25 | ~45% | batch-health, heartbeat, reflect, stale-content-pr-sweeper, issue-triage, skill-freshness |
| uncategorized | ~25 | ~45% | fleet-control, gitlawb-fleet-metrics, goal-tracker, pr-review (most runs) |
| quiet | 2 | ~4% | github-monitor (EMPTY_CONFIG), weekly-shiplog (SHIPLOG_NO_REPOS) |
| skip-other | 1 | ~2% | pr-review (1× PR_REVIEW_FULL_SKIP) |
| error | 0 | 0% | — |
| partial | 0 | 0% | — |
| skip_unchanged | 0 | 0% | — |
| new_info | 0 | 0% | — |

## Silent scheduled skills (enabled, zero runs)

24 skills had zero runs despite active cron schedules:

| Skill | Schedule | Cohort |
|-------|----------|--------|
| planner | `30 6 * * *` | 06Z daily dead (ISS-006) |
| suggest-edges | `30 5 * * *` | 05Z daily dead (ISS-006) |
| compute-futures-eda | `0 6 * * *` | 06Z daily dead (ISS-006) |
| memory-flush | `0 6 2/2 * *` | 06Z daily dead (ISS-006) |
| memory-structural-dedupe | `10 6 2/2 * *` | 06Z daily dead (ISS-006) |
| pr-triage | `30 9 * * *` | 09Z daily |
| pr-tracker | `0 10 * * *` | 10Z daily |
| run-frequency-guard | `0 23 * * *` | 23Z daily (ISS-027) |
| janitor | `30 5 * * 0` | Sunday 11-22 silent |
| config-validator | `0 7 * * 0` | Sunday 11-22 silent |
| swarm-safety-eval | `30 7 * * 0` | Sunday 11-22 silent |
| skill-evals | `0 9 * * 0` | Sunday 11-22 silent |
| workflow-security-audit | `0 16 * * 0` | Sunday 11-22 silent |
| skill-graph | `0 17 * * 0` | Sunday 11-22 silent |
| skillpacks | `0 6 * * 0` | Sunday 11-22 silent (06Z) |
| compute-macro-correlate | `30 6 * * 0` | Sunday 11-22 silent (06Z) |
| self-review | `30 18 * * 0` | Sunday 11-22 silent |
| repo-revive | `0 10 * * 6` | Sat 11-21 silent |
| vuln-scanner | `0 16 * * 6` | Sat 11-21 silent |
| ai-framework-watch | `30 8 * * 1` | Mon 11-23 (ISS-027) |
| cost-report | `0 7 * * 1` | Mon 11-23 |
| milestone-tracker | `0 12 * * 1` | Mon 11-23 |
| agi-tracker | `0 13 * * 1` | Mon 11-23 (no SKILL.md) |
| changelog | `0 16 * * 1` | Mon 11-23 |

**Context:** Sunday 11-22 was a complete silent day for the Sunday cohort (9 skills). The 06Z/05Z daily slots remain persistently dead under ISS-006 (now Day-21 for 06Z continuous silence). Monday 11-23 partial silence per ISS-047 (3-tuple confirmed: cost-report, compute-futures-eda, planner; broader Monday slots also dropped). Saturday 11-21 Sat-EVEN cohort silent.

## Source status

- skill-runs JSON: ok
- Window: 168h (2026-11-18T19:17:09Z → 2026-11-25T19:17:09Z)
- aeon.yml: ok
- cron-state.json: ok (all 40 tracked skills show consecutive_failures=0)
- Daily logs scanned: 8/8 for exit taxonomy (2026-11-18 through 2026-11-25)

---
*Companion to `skill-health` (per-skill issue filing) and `heartbeat` (per-run pulse). Fleet-wide observability is the gap this skill closes. Methodology: GitHub Actions run history is ground truth for pass/fail; daily-log markers are best-effort secondary signal for exit taxonomy.*
