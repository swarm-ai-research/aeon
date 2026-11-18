# Skill Analytics — 2026-11-18

**Verdict:** 19 scheduled skill(s) didn't run this window — planner

*Window: last 7d · 33 runs across 23 skills · 100% success · 19 anomalies*

## Anomalies

| Flag | Skill | Detail | Action |
|------|-------|--------|--------|
| 🔴 SILENT | planner | scheduled `30 6 * * *` but zero runs in window | check workflow / scheduler (ISS-006) |
| 🔴 SILENT | pr-triage | scheduled `30 9 * * *` but zero runs in window | check workflow / scheduler |
| 🔴 SILENT | memory-flush | scheduled `0 6 2/2 * *` but zero runs in window | check workflow / scheduler (ISS-006) |
| 🔴 SILENT | memory-structural-dedupe | scheduled `10 6 2/2 * *` but zero runs in window | check workflow / scheduler (ISS-006) |
| 🔴 SILENT | repo-revive | scheduled `0 10 * * 6` but zero runs in window (Sat 11-14) | check workflow / scheduler |
| 🔴 SILENT | compute-pulse | scheduled `0 11 * * 6` but zero runs in window (Sat 11-14) | check workflow / scheduler |
| 🔴 SILENT | compute-macro-correlate | scheduled `30 6 * * 0` but zero runs in window (Sun 11-15) | check workflow / scheduler (ISS-006 06Z slot) |
| 🔴 SILENT | skill-evals | scheduled `0 9 * * 0` but zero runs in window (Sun 11-15) | check workflow / scheduler |
| 🔴 SILENT | swarm-safety-eval | scheduled `30 7 * * 0` but zero runs in window (Sun 11-15) | check workflow / scheduler |
| 🔴 SILENT | workflow-security-audit | scheduled `0 16 * * 0` but zero runs in window (Sun 11-15) | check workflow / scheduler |
| 🔴 SILENT | skill-graph | scheduled `0 17 * * 0` but zero runs in window (Sun 11-15) | check workflow / scheduler |
| 🔴 SILENT | ai-framework-watch | scheduled `30 8 * * 1` but zero runs in window (Mon 11-16) | check workflow / scheduler |
| 🔴 SILENT | cost-report | scheduled `0 7 * * 1` but zero runs in window (Mon 11-16) | check workflow / scheduler |
| 🔴 SILENT | weekly-shiplog | scheduled `0 9 * * 1` but zero runs in window (Mon 11-16) | check workflow / scheduler |
| 🔴 SILENT | milestone-tracker | scheduled `0 12 * * 1` but zero runs in window (Mon 11-16) | check workflow / scheduler |
| 🔴 SILENT | agi-tracker | scheduled `0 13 * * 1` but zero runs in window (Mon 11-16) | check workflow / scheduler |
| 🔴 SILENT | changelog | scheduled `0 16 * * 1` but zero runs in window (Mon 11-16) | check workflow / scheduler |
| 🔴 SILENT | vuln-scanner | scheduled `0 16 * * 6` but zero runs in window (Sat 11-14) | check workflow / scheduler |
| 🔴 SILENT | run-frequency-guard | scheduled `0 23 * * *` but zero runs in window | check workflow / scheduler (ISS-027: may lack SKILL.md) |

## Top runners (by run count)

| # | Skill | Runs | Success | Last status | Dominant exit |
|---|-------|------|---------|-------------|---------------|
| 1 | pr-review | 3 | 100% (of 2 completed) | pending | ok |
| 2 | batch-health | 2 | 100% | success | ok |
| 3 | gitlawb-fleet-metrics | 2 | 100% | success | uncategorized |
| 4 | goal-tracker | 2 | 100% (of 1 completed) | pending | uncategorized |
| 5 | heartbeat | 2 | 100% | success | ok |
| 6 | pr-tracker | 2 | 100% | success | ok |
| 7 | reflect | 2 | 100% (of 1 completed) | pending | ok |
| 8 | skill-freshness | 2 | 100% | success | ok |
| 9 | skill-health | 2 | 100% (of 1 completed) | pending | uncategorized |
| 10 | code-health | 1 | 100% | success | ok |
| 11 | compute-futures-eda | 1 | 100% | success | uncategorized |
| 12 | fleet-control | 1 | 100% | success | uncategorized |
| 13 | github-monitor | 1 | 100% | success | uncategorized |
| 14 | issue-triage | 1 | 100% | success | ok |
| 15 | janitor | 1 | 100% | success | ok |

## Failure rate (sorted, ≥1 failure)

Zero failures across 23 skills this window.

## Exit taxonomy distribution

| Bucket | Count | % | Top skills |
|--------|-------|---|------------|
| ok | 15 | 65% | pr-tracker, batch-health, skill-freshness, heartbeat, issue-triage |
| uncategorized | 8 | 35% | gitlawb-fleet-metrics, goal-tracker, compute-futures-eda, fleet-control, github-monitor |
| skip_unchanged | 0 | — | — |
| new_info | 0 | — | — |
| quiet | 0 | — | — |
| error | 0 | — | — |
| partial | 0 | — | — |

*Sourced from `memory/logs/*.md` — best-effort regex grep, see Step 5. Exit markers found in 6/8 expected log files (2026-11-12 and 2026-11-17 missing — 11-12 was the fleet-wide silent day per ISS-006).*

## Silent scheduled skills (enabled, zero runs)

19 skills had active cron schedules but zero runs in the window:

| Skill | Schedule | Expected fires | Note |
|-------|----------|----------------|------|
| planner | `30 6 * * *` | 7 | ISS-006 06Z dead slot |
| pr-triage | `30 9 * * *` | 7 | — |
| memory-flush | `0 6 2/2 * *` | 4 | ISS-006 06Z dead slot |
| memory-structural-dedupe | `10 6 2/2 * *` | 4 | ISS-006 06Z dead slot |
| run-frequency-guard | `0 23 * * *` | 7 | ISS-027: may lack SKILL.md |
| skill-evals | `0 9 * * 0` | 1 | Sun 11-15 silent |
| swarm-safety-eval | `30 7 * * 0` | 1 | Sun 11-15 silent |
| compute-macro-correlate | `30 6 * * 0` | 1 | ISS-006 06Z dead slot |
| workflow-security-audit | `0 16 * * 0` | 1 | Sun 11-15 silent |
| skill-graph | `0 17 * * 0` | 1 | Sun 11-15 silent |
| repo-revive | `0 10 * * 6` | 1 | Sat 11-14 silent |
| compute-pulse | `0 11 * * 6` | 1 | Sat 11-14 silent |
| vuln-scanner | `0 16 * * 6` | 1 | Sat 11-14 silent |
| ai-framework-watch | `30 8 * * 1` | 1 | Mon 11-16 silent |
| cost-report | `0 7 * * 1` | 1 | Mon 11-16 silent |
| weekly-shiplog | `0 9 * * 1` | 1 | Mon 11-16 silent |
| milestone-tracker | `0 12 * * 1` | 1 | Mon 11-16 silent |
| agi-tracker | `0 13 * * 1` | 1 | Mon 11-16 silent; skills/agi-tracker/ absent |
| changelog | `0 16 * * 1` | 1 | Mon 11-16 silent |

Pattern: Saturday (11-14), Sunday (11-15), and Monday (11-16) all completely silent — consistent with the widened ISS-006 split-cohort regime that collapsed non-08Z/16Z cohorts. The 06Z dead slot (planner, memory-flush, memory-structural-dedupe, compute-macro-correlate) and all once-weekly skills outside the 08Z/16Z preservation window were missed entirely this period.

## Source status

- skill-runs JSON: ok
- Window: 168h (2026-11-11T19:36:46Z → 2026-11-18T19:36:46Z)
- aeon.yml: ok
- cron-state.json: ok
- Daily logs scanned: 6/8 for exit taxonomy (2026-11-12 missing — fleet-wide silent day; 2026-11-17 missing)

---
*Companion to `skill-health` (per-skill issue filing) and `heartbeat` (per-run pulse). Fleet-wide observability is the gap this skill closes. Methodology: GitHub Actions run history is ground truth for pass/fail; daily-log markers are best-effort secondary signal for exit taxonomy.*
