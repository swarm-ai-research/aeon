# Skill Analytics — 2026-06-24

**Verdict:** 5 scheduled skill(s) didn't run this window — agi-tracker

*Window: last 7d · 862 runs across 39 skills · 13.0% success · 43 anomalies*

## Anomalies

| Flag | Skill | Detail | Action |
|------|-------|--------|--------|
| 🔴 SILENT | agi-tracker | scheduled `0 13 * * 1` (Mon 13:00 UTC) — zero runs in 7d window (missed 2026-06-22 for 2nd consecutive Mon) | check messages.yml tick for Mon 13:00 slot |
| 🔴 SILENT | config-validator | scheduled `0 7 * * 0` (Sun 07:00 UTC) — zero runs in 7d window | check messages.yml; ISS-006 06:00–06:30 window may widen to 07:00 |
| 🔴 SILENT | swarm-safety-eval | scheduled `30 7 * * 0` (Sun 07:30 UTC) — zero runs in 7d window | same 07:00–07:30 window concern as config-validator |
| 🔴 SILENT | ai-framework-watch | scheduled `30 8 * * 1` (Mon 08:30 UTC) — zero runs in 7d window | Mon 08:30 slot unconfirmed; verify messages.yml |
| 🔴 SILENT | run-frequency-guard | scheduled `0 23 * * *` (daily 23:00 UTC) — zero runs in 7d window | never run since enable; check skill file + messages.yml |
| 🟠 LOW_SUCCESS | (all 38 active skills) | fleet-wide 13.0% success rate — ISS-001 OAuth outage (2026-06-06→20) accounts for ~95% of failures in this 7d window; all skills show `consecutive_failures: 0` and `last_status: success` | no action beyond ISS-001 monitoring; rates will recover over ~3–4 weeks as the denominator catches up |

> **Note on LOW_SUCCESS flags:** All 38 skills with ≥3 runs in the window fall below the 80% success threshold. This is expected residual from ISS-001 — the 7-day window captures ~14 days of pre-recovery failures. The fleet is operationally healthy (every skill shows `last_status: success`). LOW_SUCCESS here is a trailing metric, not a current alert. Tracking status: skill-health tracks ISS-001 separately.

## Top runners (by run count)

| # | Skill | Runs | Success | Last status | Dominant exit |
|---|-------|------|---------|-------------|---------------|
| 1 | pr-review | 28 | 28.6% | pending | ok |
| 2 | goal-tracker | 26 | 19.2% | pending | ok |
| 3 | reflect | 26 | 19.2% | pending | ok |
| 4 | skill-health | 26 | 19.2% | pending | uncategorized |
| 5 | gitlawb-fleet-metrics | 25 | 20.0% | success | uncategorized |
| 6 | heartbeat | 25 | 20.0% | success | ok |
| 7 | pr-tracker | 25 | 24.0% | success | ok |
| 8 | skill-freshness | 25 | 20.0% | success | ok |
| 9 | batch-health | 24 | 20.8% | success | ok |
| 10 | code-health | 24 | 20.8% | success | uncategorized |
| 11 | fleet-control | 24 | 16.7% | success | uncategorized |
| 12 | stale-content-pr-sweeper | 24 | 20.8% | success | ok |
| 13 | github-monitor | 23 | 17.4% | success | uncategorized |
| 14 | issue-triage | 23 | 17.4% | success | ok |
| 15 | notegraph | 23 | 13.0% | success | uncategorized |

## Failure rate (sorted by failure rate desc, ≥1 failure)

| Skill | Runs | Failures | Failure rate | Success rate | Last conclusion |
|-------|------|----------|-------------|--------------|-----------------|
| changelog | 21 | 20 | 95.2% | 4.8% | success |
| compute-futures-eda | 21 | 20 | 95.2% | 4.8% | success |
| compute-macro-correlate | 21 | 20 | 95.2% | 4.8% | success |
| cost-report | 21 | 20 | 95.2% | 4.8% | success |
| milestone-tracker | 21 | 20 | 95.2% | 4.8% | success |
| self-review | 21 | 20 | 95.2% | 4.8% | success |
| skill-repair | 21 | 20 | 95.2% | 4.8% | success |
| skillpacks | 21 | 20 | 95.2% | 4.8% | success |
| janitor | 20 | 19 | 95.0% | 5.0% | success |
| memory-flush | 20 | 19 | 95.0% | 5.0% | success |
| memory-structural-dedupe | 20 | 19 | 95.0% | 5.0% | success |
| planner | 20 | 19 | 95.0% | 5.0% | success |
| skill-analytics | 22 | 20 | 90.9% | 9.1% | pending |
| skill-evals | 22 | 20 | 90.9% | 9.1% | success |
| skill-graph | 22 | 20 | 90.9% | 9.1% | success |
| skill-update-check | 22 | 20 | 90.9% | 9.1% | success |
| suggest-edges | 22 | 20 | 90.9% | 9.1% | success |
| vuln-scanner | 22 | 20 | 90.9% | 9.1% | success |
| workflow-security-audit | 22 | 20 | 90.9% | 9.1% | success |
| compute-pulse | 22 | 20 | 90.9% | 9.1% | success |
| repo-revive | 21 | 19 | 90.5% | 9.5% | success |
| pr-triage | 22 | 19 | 86.4% | 13.6% | success |
| notegraph | 23 | 20 | 87.0% | 13.0% | success |
| fleet-control | 24 | 20 | 83.3% | 16.7% | success |
| surplus-pulse | 23 | 19 | 82.6% | 17.4% | success |
| github-monitor | 23 | 19 | 82.6% | 17.4% | success |
| issue-triage | 23 | 19 | 82.6% | 17.4% | success |
| gitlawb-fleet-metrics | 25 | 20 | 80.0% | 20.0% | success |
| heartbeat | 25 | 20 | 80.0% | 20.0% | success |
| skill-freshness | 25 | 20 | 80.0% | 20.0% | success |
| batch-health | 24 | 19 | 79.2% | 20.8% | success |
| code-health | 24 | 19 | 79.2% | 20.8% | success |
| stale-content-pr-sweeper | 24 | 19 | 79.2% | 20.8% | success |
| goal-tracker | 26 | 20 | 76.9% | 19.2% | pending |
| reflect | 26 | 20 | 76.9% | 19.2% | pending |
| skill-health | 26 | 20 | 76.9% | 19.2% | pending |
| pr-tracker | 25 | 19 | 76.0% | 24.0% | success |
| pr-review | 28 | 19 | 67.9% | 28.6% | pending |

> **Context:** All failures cluster before 2026-06-20T06:05Z (ISS-001 OAuth outage). Every skill listed above has `last_conclusion: success` or `pending` (in-progress), confirming post-recovery health. The "failure rate" column reflects historical denominator drag, not current reliability.

> `weekly-shiplog`: 1 run, 1 success (100%) — first run 2026-06-22T10:15Z. No failures; excluded from table.

## Exit taxonomy distribution

*Sourced from `memory/logs/2026-06-20.md` through `2026-06-24.md` — best-effort regex grep of exit-code markers. 10–20% miss rate expected.*

| Bucket | Count | % | Top skills |
|--------|-------|---|------------|
| ok | ~58 | ~57% | reflect, pr-tracker, stale-content-pr-sweeper, skill-freshness, pr-review, batch-health, heartbeat |
| uncategorized | ~43 | ~42% | fleet-control, gitlawb-fleet-metrics, skill-health, github-monitor, code-health, surplus-pulse |
| skip-other | ~1 | ~1% | code-health (CODE_HEALTH_SKIPPED 2026-06-24) |
| skip_unchanged | 0 | 0% | — |
| new_info | 0 | 0% | — |
| quiet | 0 | 0% | — |
| error | 0 | 0% | — |
| partial | 0 | 0% | — |

> Dominant fleet-wide exit: **ok** — the majority of logged exits carry a `_OK` suffix. "Uncategorized" is driven by skills using non-standard exit codes (`FLEET_EMPTY`, `GLMETRICS_EMPTY`, `GITHUB_MONITOR_EMPTY_CONFIG`, etc.) rather than the `_OK/_SKIP/_ERROR` taxonomy. These are healthy-quiet exits, not failures.

## Silent scheduled skills (enabled, zero runs)

| Skill | Schedule | First missed occurrence | Note |
|-------|----------|------------------------|------|
| agi-tracker | `0 13 * * 1` | 2026-06-15 (pre-window, ISS-001) | Missed 2026-06-22 — 2nd consecutive Mon; ISS-006 root cause may extend to 13:00 UTC slot |
| config-validator | `0 7 * * 0` | 2026-06-21 | In window; ISS-006 06:00–07:30 silent zone |
| swarm-safety-eval | `30 7 * * 0` | 2026-06-21 | In window; same 07:30 slot concern |
| ai-framework-watch | `30 8 * * 1` | 2026-06-22 | In window; Mon 08:30 slot — separate from ISS-006 06:00 hypothesis |
| run-frequency-guard | `0 23 * * *` | (daily, never run) | Never dispatched since enable; check skill file exists + messages.yml 23:00 tick |

## Source status

- skill-runs JSON: ok (862 runs, 39 distinct skills, `gh api` auth via GITHUB_TOKEN)
- Window: 168h (2026-06-17T19:21:58Z → 2026-06-24T19:21:58Z)
- aeon.yml: ok
- cron-state.json: ok (39 tracked skills, all `consecutive_failures: 0`)
- Daily logs scanned: 5/8 (2026-06-20 through 2026-06-24; 2026-06-17/18/19 absent — fleet was in ISS-001 outage, no log entries written)

---
*Companion to `skill-health` (per-skill issue filing) and `heartbeat` (per-run pulse). Fleet-wide observability is the gap this skill closes. Methodology: GitHub Actions run history is ground truth for pass/fail; daily-log markers are best-effort secondary signal for exit taxonomy.*
