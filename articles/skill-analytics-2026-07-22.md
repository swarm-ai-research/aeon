# Skill Analytics — 2026-07-22

**Verdict:** 3 scheduled skill(s) didn't run this window — janitor, ai-framework-watch, run-frequency-guard

*Window: last 7d · 149 runs across 39 skills · 100.0% success · 3 anomalies*

## Anomalies

| Flag | Skill | Detail | Action |
|------|-------|--------|--------|
| 🔴 SILENT | janitor | scheduled `30 5 * * 0` (Sunday 05:30 UTC) but zero runs in window (window covered Sunday 2026-07-19) | check workflow / scheduler — messages.yml 06:00–08:30 dead zone may extend to 05:30 |
| 🔴 SILENT | ai-framework-watch | scheduled `30 8 * * 1` (Monday 08:30 UTC) but zero runs in window (12-day consecutive silent streak per memory) | enabled with valid cron; never dispatching — likely messages.yml matcher or GHA wiring gap; see [[enabled-skills-can-never-dispatch]] |
| 🔴 SILENT | run-frequency-guard | scheduled `0 23 * * *` (daily 23:00 UTC) but zero runs in window (12-day consecutive silent streak per memory) | enabled with valid cron; never dispatching — same root cause as ai-framework-watch; see [[enabled-skills-can-never-dispatch]] |

## Top runners (by run count)

| # | Skill | Runs | Success | Last status | Dominant exit |
|---|-------|------|---------|-------------|---------------|
| 1 | pr-review (swarm) | 14 | 93% | pending | ok |
| 2 | code-health | 7 | 100% | success | ok |
| 3 | compute-futures-eda | 7 | 100% | success | uncategorized |
| 4 | fleet-control | 7 | 100% | success | uncategorized |
| 5 | github-monitor | 7 | 100% | success | uncategorized |
| 6 | goal-tracker | 7 | 86% | pending | ok |
| 7 | issue-triage | 7 | 100% | success | ok |
| 8 | pr-tracker | 7 | 100% | success | ok |
| 9 | reflect | 7 | 86% | pending | ok |
| 10 | skill-health | 7 | 86% | pending | uncategorized |
| 11 | surplus-pulse | 7 | 100% | success | ok |
| 12 | batch-health | 5 | 100% | success | ok |
| 13 | gitlawb-fleet-metrics | 5 | 100% | success | uncategorized |
| 14 | heartbeat | 5 | 100% | success | ok |
| 15 | planner | 5 | 100% | success | ok |

## Failure rate (sorted, ≥1 failure)

Zero failures across 39 skills this window. (5 runs currently in_progress for goal-tracker, reflect, skill-health, skill-analytics, pr-review — not counted as failures.)

## Exit taxonomy distribution

*Sourced from `memory/logs/*.md` — best-effort regex grep, see Step 5. 129 markers matched across 7 log files (2026-07-16 → 2026-07-22). Skills with no log markers fall into uncategorized; ~15 skills produced no markers this window.*

| Bucket | Count | % | Top skills |
|--------|-------|---|------------|
| ok | 117 | 90.7% | issue-triage (17), pr-review (12), skill-freshness (11), pr-triage (8), code-health (8) |
| partial | 4 | 3.1% | skill-health |
| uncategorized | 7 | 5.4% | skill-health (5× NOOP), skill-evals (1× REGRESSED) |
| error | 1 | 0.8% | (unattributed `_ERROR` marker) |
| quiet | 0 | 0.0% | |
| skip_unchanged | 0 | 0.0% | |
| new_info | 0 | 0.0% | |
| skip_other | 0 | 0.0% | |

Note: `skill-health` shows a mixed profile — 5× NOOP (no issues to file), 4× PARTIAL, 3× OK — dominant bucket is uncategorized due to NOOP not matching `_OK_SILENT`/`_QUIET` patterns. Semantically healthy; the NOOP exits indicate quiet fleet operation.

## Silent scheduled skills (enabled, zero runs)

| Skill | Schedule | Notes |
|-------|----------|-------|
| janitor | `30 5 * * 0` | Sunday 05:30 UTC; window covered 2026-07-19 (Sun); last success unknown — likely dispatch drop in pre-06:00 slot |
| ai-framework-watch | `30 8 * * 1` | Monday 08:30 UTC; 12-day never-dispatch streak per [[enabled-skills-can-never-dispatch]]; ISS-020 candidate |
| run-frequency-guard | `0 23 * * *` | Daily 23:00 UTC; 12-day never-dispatch streak per [[enabled-skills-can-never-dispatch]]; ISS-020 candidate |

Shared probable root cause: messages.yml cron matcher has a known dead zone covering the 06:00–08:30 window; janitor fires at 05:30 (just before the zone) and may be similarly affected. ISS-006 fix (replacing `*/5 * * * *` with explicit per-slot crons) is the underlying repair — currently blocked on repo Settings toggle for branch merge.

## Source status

- skill-runs JSON: ok
- Window: 168h (2026-07-15T19:15:33Z → 2026-07-22T19:15:33Z)
- aeon.yml: ok
- cron-state.json: ok
- Daily logs scanned: 7/7 for exit taxonomy (2026-07-16 → 2026-07-22)

---
*Companion to `skill-health` (per-skill issue filing) and `heartbeat` (per-run pulse). Fleet-wide observability is the gap this skill closes. Methodology: GitHub Actions run history is ground truth for pass/fail; daily-log markers are best-effort secondary signal for exit taxonomy.*
