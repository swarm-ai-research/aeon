# Skill Analytics — 2026-10-14

**Verdict:** 10 scheduled skill(s) didn't run this window — planner

*Window: last 7d · 67 runs across 27 skills · 100.0% success · 13 anomalies*

## Anomalies

| Flag | Skill | Detail | Action |
|------|-------|--------|--------|
| 🔴 SILENT | planner | scheduled `30 6 * * *` but zero runs in window | check workflow / scheduler (ISS-006 06Z dead regime) |
| 🔴 SILENT | compute-futures-eda | scheduled `0 6 * * *` but zero runs in window | check workflow / scheduler (ISS-006 06Z dead regime) |
| 🔴 SILENT | memory-flush | scheduled `0 6 2/2 * *` but zero runs in window | check workflow / scheduler (ISS-006 06Z dead regime) |
| 🔴 SILENT | memory-structural-dedupe | scheduled `10 6 2/2 * *` but zero runs in window | check workflow / scheduler (ISS-006 06Z dead regime) |
| 🔴 SILENT | compute-macro-correlate | scheduled `30 6 * * 0` (Sunday 06:30) but zero runs in window | ISS-006 06Z dead regime absorbs Sunday slot per [[iss-006-06z-dead-regime-extends-to-sunday-slot]] |
| 🔴 SILENT | janitor | scheduled `30 5 * * 0` (Sunday 05:30) but zero runs in window | 05Z pocket part of ISS-006 casualty set |
| 🔴 SILENT | skill-evals | scheduled `0 9 * * 0` (Sunday 09:00) but zero runs in window | 09Z cluster part of ISS-006 casualty set |
| 🔴 SILENT | changelog | scheduled `0 16 * * 1` (Monday 16:00) but zero runs in window | check workflow / scheduler |
| 🔴 SILENT | agi-tracker | scheduled `0 13 * * 1` (Monday 13:00) but zero runs in window | `skills/agi-tracker/SKILL.md` missing — no-op dispatch per [[agi-tracker-missing-skill-md-dispatches-no-op]] |
| 🔴 SILENT | milestone-tracker | scheduled `0 12 * * 1` (Monday 12:00) but zero runs in window | check workflow / scheduler |
| 🟠 LOW_SUCCESS | goal-tracker | 66.7% (2/3 runs) — 1 run in_progress at snapshot time | likely resolves; recheck after in_progress completes |
| 🟠 LOW_SUCCESS | reflect | 66.7% (2/3 runs) — 1 run in_progress at snapshot time | likely resolves; recheck after in_progress completes |
| 🟠 LOW_SUCCESS | skill-health | 66.7% (2/3 runs) — 1 run in_progress at snapshot time | likely resolves; recheck after in_progress completes |

> **Note on LOW_SUCCESS flags**: goal-tracker, reflect, and skill-health each show 2 successes + 1 in_progress. The in_progress runs are live concurrent jobs at snapshot time (this skill-analytics run fired mid-batch). These are likely false positives — the formula `success / total` counts in_progress as not-yet-succeeded. Monitor on next pass.

## Top runners (by run count)

| # | Skill | Runs | Success | Last status | Dominant exit |
|---|-------|------|---------|-------------|---------------|
| 1 | pr-review | 6 | 83.3% | pending (1 in_progress) | uncategorized |
| 2 | batch-health | 5 | 100.0% | success | ok |
| 3 | gitlawb-fleet-metrics | 5 | 100.0% | success | uncategorized |
| 4 | heartbeat | 5 | 100.0% | success | uncategorized |
| 5 | skill-freshness | 5 | 100.0% | success | ok |
| 6 | code-health | 3 | 100.0% | success | skip_other |
| 7 | fleet-control | 3 | 100.0% | success | uncategorized |
| 8 | github-monitor | 3 | 100.0% | success | uncategorized |
| 9 | goal-tracker | 3 | 66.7% | pending (1 in_progress) | uncategorized |
| 10 | issue-triage | 3 | 100.0% | success | ok |
| 11 | reflect | 3 | 66.7% | pending (1 in_progress) | ok |
| 12 | skill-health | 3 | 66.7% | pending (1 in_progress) | uncategorized |
| 13 | notegraph | 2 | 100.0% | success | ok |
| 14 | pr-tracker | 2 | 100.0% | success | ok |
| 15 | pr-triage | 2 | 100.0% | success | ok |

## Failure rate (sorted, ≥1 failure)

Zero failures across 27 active skills this window.

## Exit taxonomy distribution

| Bucket | Count | % | Top skills |
|--------|-------|---|------------|
| ok | 13 | 48% | batch-health, skill-freshness, issue-triage, reflect, notegraph, pr-tracker, pr-triage, surplus-pulse, stale-content-pr-sweeper, compute-pulse, vuln-scanner, self-review, weekly-shiplog |
| uncategorized | 13 | 48% | pr-review, gitlawb-fleet-metrics, heartbeat, fleet-control, github-monitor, goal-tracker, skill-health, repo-revive, config-validator, swarm-safety-eval, skill-update-check, suggest-edges, skill-analytics |
| skip_other | 1 | 4% | code-health (CODE_HEALTH_SKIPPED) |
| skip_unchanged | 0 | 0% | — |
| new_info | 0 | 0% | — |
| quiet | 0 | 0% | — |
| error | 0 | 0% | — |
| partial | 0 | 0% | — |

*Sourced from `memory/logs/*.md` — best-effort regex grep, see Step 5. Exit taxonomy represents log markers seen in window; uncategorized means no explicit exit marker was matched in logs, not that the run failed. GitHub Actions success/failure counts are ground truth.*

## Silent scheduled skills (enabled, zero runs)

| Skill | Schedule | Notes |
|-------|----------|-------|
| planner | `30 6 * * *` | ISS-006 06Z dead regime — daily 06:30 |
| compute-futures-eda | `0 6 * * *` | ISS-006 06Z dead regime — daily 06:00 |
| memory-flush | `0 6 2/2 * *` | ISS-006 06Z dead regime — every-other-day 06:00 |
| memory-structural-dedupe | `10 6 2/2 * *` | ISS-006 06Z dead regime — every-other-day 06:10 |
| compute-macro-correlate | `30 6 * * 0` | ISS-006 06Z absorbed Sunday 06:30 slot |
| janitor | `30 5 * * 0` | 05Z casualty — Sunday 05:30 |
| skill-evals | `0 9 * * 0` | 09Z casualty — Sunday 09:00 |
| changelog | `0 16 * * 1` | Monday 16:00 — investigate; no ISS-006 link expected at 16Z Mon |
| agi-tracker | `0 13 * * 1` | `skills/agi-tracker/SKILL.md` absent — silent no-op |
| milestone-tracker | `0 12 * * 1` | Monday 12:00 — investigate |

## Source status

- skill-runs JSON: ok
- Window: 168h (2026-10-07T19:34:31Z → 2026-10-14T19:34:31Z)
- aeon.yml: ok
- cron-state.json: ok
- Daily logs scanned: 8/8 for exit taxonomy (2026-10-07 through 2026-10-14)

---
*Companion to `skill-health` (per-skill issue filing) and `heartbeat` (per-run pulse). Fleet-wide observability is the gap this skill closes. Methodology: GitHub Actions run history is ground truth for pass/fail; daily-log markers are best-effort secondary signal for exit taxonomy.*
