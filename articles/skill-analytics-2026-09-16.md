# Skill Analytics — 2026-09-16

**Verdict:** 13 scheduled skill(s) didn't run this window — memory-flush

*Window: last 7d · 86 runs across 30 skills · 100% success · 13 anomalies*

## Anomalies

| Flag | Skill | Detail | Action |
|------|-------|--------|--------|
| 🔴 SILENT | memory-flush | scheduled `0 6 2/2 * *` but zero runs in window | ISS-006 06:00Z dead pocket — migrate away from dead cron slot |
| 🔴 SILENT | memory-structural-dedupe | scheduled `10 6 2/2 * *` but zero runs in window | same dead pocket as memory-flush |
| 🔴 SILENT | run-frequency-guard | scheduled `0 23 * * *` but zero runs in window | check workflow / scheduler |
| 🔴 SILENT | janitor | scheduled `30 5 * * 0` but zero runs in window (Sun 09-13) | check workflow / scheduler |
| 🔴 SILENT | skillpacks | scheduled `0 6 * * 0` but zero runs in window (Sun 09-13) | 06:00Z dead pocket on Sunday |
| 🔴 SILENT | compute-macro-correlate | scheduled `30 6 * * 0` but zero runs in window (Sun 09-13) | 06:30Z pocket on Sunday |
| 🔴 SILENT | config-validator | scheduled `0 7 * * 0` but zero runs in window (Sun 09-13) | check workflow / scheduler |
| 🔴 SILENT | swarm-safety-eval | scheduled `30 7 * * 0` but zero runs in window (Sun 09-13) | check workflow / scheduler |
| 🔴 SILENT | repo-revive | scheduled `0 10 * * 6` but zero runs in window (Sat 09-12) | check workflow / scheduler |
| 🔴 SILENT | cost-report | scheduled `0 7 * * 1` but zero runs in window (Mon 09-14) | check workflow / scheduler |
| 🔴 SILENT | ai-framework-watch | scheduled `30 8 * * 1` but zero runs in window (Mon 09-14) | check workflow / scheduler |
| 🔴 SILENT | milestone-tracker | scheduled `0 12 * * 1` but zero runs in window (Mon 09-14) | check workflow / scheduler |
| 🔴 SILENT | agi-tracker | scheduled `0 13 * * 1` but zero runs in window (Mon 09-14) | skills/agi-tracker/ directory absent; known ISS |

## Top runners (by run count)

| # | Skill | Runs | Success | Last status | Dominant exit |
|---|-------|------|---------|-------------|---------------|
| 1 | pr-review | 8 | 87.5%* | pending | ok |
| 2 | code-health | 6 | 100% | success | ok |
| 3 | notegraph | 6 | 100% | success | ok |
| 4 | fleet-control | 5 | 100% | success | uncategorized |
| 5 | github-monitor | 5 | 100% | success | uncategorized |
| 6 | issue-triage | 5 | 100% | success | ok |
| 7 | stale-content-pr-sweeper | 5 | 100% | success | ok |
| 8 | surplus-pulse | 4 | 100% | success | ok |
| 9 | pr-triage | 4 | 100% | success | ok |
| 10 | batch-health | 3 | 100% | success | ok |
| 11 | gitlawb-fleet-metrics | 3 | 100% | success | uncategorized |
| 12 | goal-tracker | 3 | 67%* | pending | uncategorized |
| 13 | heartbeat | 3 | 100% | success | ok |
| 14 | pr-tracker | 3 | 100% | success | ok |
| 15 | reflect | 3 | 67%* | pending | ok |

*In-progress run counted in total but not yet succeeded; completed-run success rate is 100%.

## Failure rate (sorted, ≥1 failure)

Zero failures across 30 skills this window.

## Exit taxonomy distribution

| Bucket | Count | % | Top skills |
|--------|-------|---|------------|
| ok | ~48 | ~76% | pr-review, issue-triage, stale-content-pr-sweeper, fleet-control, heartbeat |
| uncategorized | ~13 | ~21% | fleet-control, github-monitor, gitlawb-fleet-metrics, goal-tracker, changelog |
| skip_other | ~1 | ~2% | code-health |
| skip_unchanged | 0 | 0% | — |
| new_info | 0 | 0% | — |
| quiet | 0 | 0% | — |
| error | 0 | 0% | — |
| partial | 0 | 0% | — |

*(Sourced from `memory/logs/*.md` — best-effort regex grep, see Step 5. ~10–20% miss rate expected; total of 86 runs from GitHub Actions is ground truth.)*

## Silent scheduled skills (enabled, zero runs)

| Skill | Schedule | Day(s) missed |
|-------|----------|---------------|
| memory-flush | `0 6 2/2 * *` | 09-10, 09-12, 09-14, 09-16 |
| memory-structural-dedupe | `10 6 2/2 * *` | 09-10, 09-12, 09-14, 09-16 |
| run-frequency-guard | `0 23 * * *` | 09-09→09-15 (7 slots) |
| janitor | `30 5 * * 0` | 09-13 (Sun) |
| skillpacks | `0 6 * * 0` | 09-13 (Sun) |
| compute-macro-correlate | `30 6 * * 0` | 09-13 (Sun) |
| config-validator | `0 7 * * 0` | 09-13 (Sun) |
| swarm-safety-eval | `30 7 * * 0` | 09-13 (Sun) |
| repo-revive | `0 10 * * 6` | 09-12 (Sat) |
| cost-report | `0 7 * * 1` | 09-14 (Mon) |
| ai-framework-watch | `30 8 * * 1` | 09-14 (Mon) |
| milestone-tracker | `0 12 * * 1` | 09-14 (Mon) |
| agi-tracker | `0 13 * * 1` | 09-14 (Mon) |

## Source status

- skill-runs JSON: ok
- Window: 168h (2026-09-09T19:02:14Z → 2026-09-16T19:02:14Z)
- aeon.yml: ok
- cron-state.json: ok
- Daily logs scanned: 7/7 for exit taxonomy (2026-09-10 → 2026-09-16)

---
*Companion to `skill-health` (per-skill issue filing) and `heartbeat` (per-run pulse). Fleet-wide observability is the gap this skill closes. Methodology: GitHub Actions run history is ground truth for pass/fail; daily-log markers are best-effort secondary signal for exit taxonomy.*
