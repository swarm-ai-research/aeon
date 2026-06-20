# Skill Analytics — 2026-06-20

**Verdict:** 6 scheduled skill(s) didn't run this window — agi-tracker

*Window: last 7d · 942 runs across 38 skills · 1.1% success · 44 anomalies*

## Anomalies

| Flag | Skill | Detail | Action |
|------|-------|--------|--------|
| 🔴 SILENT | agi-tracker | scheduled `0 13 * * 1` but zero runs in window | check workflow / scheduler |
| 🔴 SILENT | config-validator | scheduled `0 7 * * 0` but zero runs in window | check workflow / scheduler |
| 🔴 SILENT | ai-framework-watch | scheduled `30 8 * * 1` but zero runs in window | check workflow / scheduler |
| 🔴 SILENT | swarm-safety-eval | scheduled `30 7 * * 0` but zero runs in window | check workflow / scheduler |
| 🔴 SILENT | run-frequency-guard | scheduled `0 23 * * *` but zero runs in window | check workflow / scheduler |
| 🔴 SILENT | weekly-shiplog | scheduled `0 9 * * 1` but zero runs in window | check workflow / scheduler |
| 🟠 CONSECUTIVE_FAILURES | compute-futures-eda | 202-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | pr-review | 196-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | gitlawb-fleet-metrics | 196-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | skill-health | 195-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | skill-analytics | 188-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | notegraph | 188-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | suggest-edges | 187-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | goal-tracker | 185-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | reflect | 185-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | code-health | 184-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | pr-tracker | 181-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | surplus-pulse | 180-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | issue-triage | 178-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | github-monitor | 176-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | fleet-control | 173-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | batch-health | 174-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | skill-freshness | 172-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | pr-triage | 172-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | planner | 171-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | heartbeat | 170-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | compute-pulse | 168-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | skill-repair | 161-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | repo-revive | 157-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | janitor | 151-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | skill-evals | 149-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | skill-update-check | 142-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | skill-graph | 141-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | self-review | 140-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | skillpacks | 140-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | memory-flush | 136-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | workflow-security-audit | 134-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | memory-structural-dedupe | 134-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | vuln-scanner | 127-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | changelog | 120-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | stale-content-pr-sweeper | 119-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | compute-macro-correlate | 64-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | cost-report | 50-run streak | see skill-health for filed issue |
| 🟠 CONSECUTIVE_FAILURES | milestone-tracker | 45-run streak | see skill-health for filed issue |

**Context note:** skill-runs flagged nearly all skills as DUPLICATE_RUNS (25 actual runs vs. 7–14 expected for daily/weekly crons over 7d). This suggests a batch-trigger anomaly — all 38 skills fired simultaneously at ~06:05 UTC today rather than on their individual schedules. The CONSECUTIVE_FAILURES flag takes priority per anomaly rules, but the mass-batch pattern is the underlying cause and warrants investigation.

## Top runners (by run count)

| # | Skill | Runs | Success | Last status | Dominant exit |
|---|-------|------|---------|-------------|---------------|
| 1 | changelog | 25 | 4% | success | uncategorized |
| 2 | code-health | 25 | 4% | success | uncategorized |
| 3 | github-monitor | 25 | 4% | success | uncategorized |
| 4 | goal-tracker | 25 | 4% | success | uncategorized |
| 5 | repo-revive | 25 | 4% | success | uncategorized |
| 6 | compute-futures-eda | 25 | 0% | pending | uncategorized |
| 7 | compute-macro-correlate | 25 | 0% | pending | uncategorized |
| 8 | compute-pulse | 25 | 0% | pending | uncategorized |
| 9 | cost-report | 25 | 0% | pending | uncategorized |
| 10 | fleet-control | 25 | 0% | pending | uncategorized |
| 11 | gitlawb-fleet-metrics | 25 | 0% | pending | uncategorized |
| 12 | heartbeat | 25 | 0% | pending | uncategorized |
| 13 | milestone-tracker | 25 | 0% | pending | uncategorized |
| 14 | notegraph | 25 | 0% | pending | uncategorized |
| 15 | pr-review | 25 | 0% | pending | uncategorized |

## Failure rate (sorted, ≥1 failure)

| Skill | Runs | Failures | Success rate | Last conclusion |
|-------|------|----------|--------------|-----------------|
| compute-macro-correlate | 25 | 24 | 0% | pending |
| cost-report | 25 | 24 | 0% | pending |
| fleet-control | 25 | 24 | 0% | pending |
| github-monitor | 25 | 24 | 4% | success |
| gitlawb-fleet-metrics | 25 | 24 | 0% | pending |
| goal-tracker | 25 | 24 | 4% | success |
| heartbeat | 25 | 24 | 0% | pending |
| milestone-tracker | 25 | 24 | 0% | pending |
| notegraph | 25 | 24 | 0% | pending |
| pr-review | 25 | 24 | 0% | pending |
| pr-tracker | 25 | 24 | 0% | pending |
| reflect | 25 | 24 | 0% | pending |
| repo-revive | 25 | 24 | 4% | success |
| self-review | 25 | 24 | 0% | pending |
| skill-analytics | 25 | 24 | 0% | pending |
| skill-evals | 25 | 24 | 0% | pending |
| skill-freshness | 25 | 24 | 0% | pending |
| skill-graph | 25 | 24 | 0% | pending |
| skill-health | 25 | 24 | 0% | pending |
| skill-repair | 25 | 24 | 0% | pending |
| skill-update-check | 25 | 24 | 0% | pending |
| skillpacks | 25 | 24 | 0% | pending |
| suggest-edges | 25 | 24 | 0% | pending |
| surplus-pulse | 25 | 24 | 0% | pending |
| vuln-scanner | 25 | 24 | 0% | pending |
| workflow-security-audit | 25 | 24 | 0% | pending |
| batch-health | 24 | 23 | 0% | pending |
| issue-triage | 24 | 23 | 4% | success |
| janitor | 24 | 23 | 4% | success |
| memory-flush | 24 | 23 | 4% | success |
| memory-structural-dedupe | 24 | 23 | 4% | success |
| planner | 24 | 23 | 0% | pending |
| stale-content-pr-sweeper | 24 | 23 | 4% | success |
| changelog | 25 | 23 | 4% | success |
| code-health | 25 | 23 | 4% | success |
| compute-futures-eda | 25 | 23 | 0% | pending |
| compute-pulse | 25 | 23 | 0% | pending |
| pr-triage | 24 | 22 | 0% | pending |

## Exit taxonomy distribution

| Bucket | Count | % | Top skills |
|--------|-------|---|------------|
| ok | 0 | 0% | — |
| skip_unchanged | 0 | 0% | — |
| new_info | 0 | 0% | — |
| quiet | 0 | 0% | — |
| error | 0 | 0% | — |
| partial | 0 | 0% | — |
| uncategorized | 38 | 100% | all (no log files found in window) |

*Sourced from `memory/logs/*.md` — best-effort regex grep, see Step 5. Zero log files fell within the 2026-06-13 → 2026-06-20 window (only `2026-06-10.md` exists, pre-window). All 38 skills default to uncategorized.*

## Silent scheduled skills (enabled, zero runs)

| Skill | Schedule | Note |
|-------|----------|------|
| agi-tracker | `0 13 * * 1` (Mon 13:00 UTC) | Expected ≥1 run on 2026-06-16 |
| config-validator | `0 7 * * 0` (Sun 07:00 UTC) | Expected ≥1 run on 2026-06-15 |
| ai-framework-watch | `30 8 * * 1` (Mon 08:30 UTC) | Expected ≥1 run on 2026-06-16 |
| swarm-safety-eval | `30 7 * * 0` (Sun 07:30 UTC) | Expected ≥1 run on 2026-06-15 |
| run-frequency-guard | `0 23 * * *` (daily 23:00 UTC) | Expected ≥7 runs in window |
| weekly-shiplog | `0 9 * * 1` (Mon 09:00 UTC) | Expected ≥1 run on 2026-06-16 |

## Source status

- skill-runs JSON: ok
- Window: 168h (2026-06-13T06:07:54Z → 2026-06-20T06:07:54Z)
- aeon.yml: ok
- cron-state.json: ok (38 skills tracked, all showing 100+ consecutive failures — stale state consistent with systemic failure mode)
- Daily logs scanned: 0/7 for exit taxonomy (only `2026-06-10.md` exists; pre-window)

---
*Companion to `skill-health` (per-skill issue filing) and `heartbeat` (per-run pulse). Fleet-wide observability is the gap this skill closes. Methodology: GitHub Actions run history is ground truth for pass/fail; daily-log markers are best-effort secondary signal for exit taxonomy.*
