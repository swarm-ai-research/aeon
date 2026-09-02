# Skill Analytics — 2026-09-02

**Verdict:** 16 scheduled skill(s) didn't run this window — memory-flush

*Window: last 7d · 64 runs across 27 skills · 100% success · 16 anomalies*

## Anomalies

| Flag | Skill | Detail | Action |
|------|-------|--------|--------|
| 🔴 SILENT | memory-flush | scheduled `0 6 2/2 * *` but zero runs in window | check workflow / scheduler (ISS-006 batch-outage pattern) |
| 🔴 SILENT | memory-structural-dedupe | scheduled `10 6 2/2 * *` but zero runs in window | check workflow / scheduler (ISS-006 batch-outage pattern) |
| 🔴 SILENT | run-frequency-guard | scheduled `0 23 * * *` (daily) but zero runs in window | investigate messages.yml matcher per [[enabled-skills-can-never-dispatch]] |
| 🔴 SILENT | config-validator | scheduled `0 7 * * 0` (Sun) but zero runs in window | check workflow / scheduler |
| 🔴 SILENT | skillpacks | scheduled `0 6 * * 0` (Sun) but zero runs in window | check workflow / scheduler |
| 🔴 SILENT | swarm-safety-eval | scheduled `30 7 * * 0` (Sun) but zero runs in window | check workflow / scheduler |
| 🔴 SILENT | skill-evals | scheduled `0 9 * * 0` (Sun) but zero runs in window | check workflow / scheduler |
| 🔴 SILENT | workflow-security-audit | scheduled `0 16 * * 0` (Sun) but zero runs in window | check workflow / scheduler |
| 🔴 SILENT | skill-update-check | scheduled `0 19 * * 0` (Sun) but zero runs in window | check workflow / scheduler |
| 🔴 SILENT | compute-macro-correlate | scheduled `30 6 * * 0` (Sun) but zero runs in window | check workflow / scheduler |
| 🔴 SILENT | repo-revive | scheduled `0 10 * * 6` (Sat) but zero runs in window | check workflow / scheduler |
| 🔴 SILENT | compute-pulse | scheduled `0 11 * * 6` (Sat) but zero runs in window | check workflow / scheduler |
| 🔴 SILENT | ai-framework-watch | scheduled `30 8 * * 1` (Mon) but zero runs in window | [[enabled-skills-can-never-dispatch]] day-56 |
| 🔴 SILENT | milestone-tracker | scheduled `0 12 * * 1` (Mon) but zero runs in window | check workflow / scheduler |
| 🔴 SILENT | agi-tracker | scheduled `0 13 * * 1` (Mon) but zero runs in window | SKILL.md absent — 9th silent-Mon; file `enabled: false` PR or restore SKILL.md |
| 🔴 SILENT | cost-report | scheduled `0 7 * * 1` (Mon) but zero runs in window | ISS-006 batch-outage triple; next expected slot 09-07 07:00Z |

## Top runners (by run count)

| # | Skill | Runs | Success | Last status | Dominant exit |
|---|-------|------|---------|-------------|---------------|
| 1 | pr-review | 6 | 83% | pending | ok |
| 2 | code-health | 5 | 100% | success | skip-other |
| 3 | surplus-pulse | 5 | 100% | success | ok |
| 4 | goal-tracker | 4 | 75%* | pending | uncategorized |
| 5 | reflect | 4 | 75%* | pending | ok |
| 6 | skill-health | 4 | 75%* | pending | ok |
| 7 | notegraph | 3 | 100% | success | ok |
| 8 | stale-content-pr-sweeper | 3 | 100% | success | ok |
| 9 | batch-health | 2 | 100% | success | ok |
| 10 | compute-futures-eda | 2 | 100% | success | uncategorized |
| 11 | fleet-control | 2 | 100% | success | uncategorized |
| 12 | github-monitor | 2 | 100% | success | uncategorized |
| 13 | gitlawb-fleet-metrics | 2 | 100% | success | uncategorized |
| 14 | heartbeat | 2 | 100% | success | ok |
| 15 | issue-triage | 2 | 100% | success | ok |

*Percentage based on total including 1 in-progress run; failure count = 0.

## Failure rate (sorted, ≥1 failure)

Zero failures across 27 skills this window.

## Exit taxonomy distribution

| Bucket | Count | % | Top skills |
|--------|-------|---|------------|
| ok | 10 | 77% | notegraph, reflect, heartbeat, stale-content-pr-sweeper, skill-analytics, skill-health, skill-graph, issue-triage, batch-health |
| skip-other | 3 | 23% | code-health (SKIP_NO_WATCHED_REPOS ×2), goal-tracker (NO_GOALS) |
| skip_unchanged | 0 | — | |
| new_info | 0 | — | |
| quiet | 0 | — | |
| error | 0 | — | |
| partial | 0 | — | |
| uncategorized | many | — | remaining skills (markers absent from daily logs) |

*Sourced from `memory/logs/*.md` — best-effort regex grep, see Step 5. Expected 10–20% miss rate; GitHub Actions success/failure counts are ground truth.*

## Silent scheduled skills (enabled, zero runs)

| Skill | Schedule | Note |
|-------|----------|------|
| memory-flush | `0 6 2/2 * *` | ISS-006-family; last success 2026-08-26 |
| memory-structural-dedupe | `10 6 2/2 * *` | ISS-006-family; last success 2026-08-26 |
| run-frequency-guard | `0 23 * * *` (daily) | Day-56 never-dispatched per [[enabled-skills-can-never-dispatch]] |
| config-validator | `0 7 * * 0` (Sun) | Expected 2026-08-30; zero runs |
| skillpacks | `0 6 * * 0` (Sun) | Expected 2026-08-30; zero runs |
| swarm-safety-eval | `30 7 * * 0` (Sun) | Expected 2026-08-30; zero runs |
| skill-evals | `0 9 * * 0` (Sun) | Expected 2026-08-30; zero runs |
| workflow-security-audit | `0 16 * * 0` (Sun) | Expected 2026-08-30; zero runs |
| skill-update-check | `0 19 * * 0` (Sun) | Expected 2026-08-30; zero runs |
| compute-macro-correlate | `30 6 * * 0` (Sun) | Expected 2026-08-30; zero runs |
| repo-revive | `0 10 * * 6` (Sat) | Expected 2026-08-29; zero runs |
| compute-pulse | `0 11 * * 6` (Sat) | Expected 2026-08-29; zero runs |
| ai-framework-watch | `30 8 * * 1` (Mon) | Day-56 never-dispatched per [[enabled-skills-can-never-dispatch]] |
| milestone-tracker | `0 12 * * 1` (Mon) | Expected 2026-08-31; zero runs |
| agi-tracker | `0 13 * * 1` (Mon) | SKILL.md absent; 9th silent-Mon (last fired 08-31T13Z was confirmed silent) |
| cost-report | `0 7 * * 1` (Mon) | Expected 2026-08-31; in ISS-006 outage triple; next slot 09-07 |

## Source status

- skill-runs JSON: ok
- Window: 168h (2026-08-26T19:59:14Z → 2026-09-02T19:59:14Z)
- aeon.yml: ok
- cron-state.json: ok
- Daily logs scanned: 8/8 for exit taxonomy

---
*Companion to `skill-health` (per-skill issue filing) and `heartbeat` (per-run pulse). Fleet-wide observability is the gap this skill closes. Methodology: GitHub Actions run history is ground truth for pass/fail; daily-log markers are best-effort secondary signal for exit taxonomy.*
