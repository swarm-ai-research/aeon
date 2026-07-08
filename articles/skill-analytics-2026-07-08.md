# Skill Analytics — 2026-07-08

**Verdict:** 4 scheduled skill(s) didn't run this window — janitor

*Window: last 7d · 136 runs across 39 skills · 100.0% success · 4 anomalies*

## Anomalies

| Flag | Skill | Detail | Action |
|------|-------|--------|--------|
| 🔴 SILENT | janitor | scheduled `30 5 * * 0` (Sun 05:30 UTC) but zero runs in window | ISS-006 tributary; last success 2026-06-20 (~18d ago) |
| 🔴 SILENT | run-frequency-guard | scheduled `0 23 * * *` (daily 23:00 UTC) but zero runs in window | no cron-state entry — never dispatched; systemic non-arm |
| 🔴 SILENT | ai-framework-watch | scheduled `30 8 * * 1` (Mon 08:30 UTC) but zero runs in window | no cron-state entry; 3rd consecutive Monday non-arm |
| 🔴 SILENT | cost-report | scheduled `0 7 * * 1` (Mon 07:00 UTC) but zero runs in window | ISS-008; 3rd consecutive Monday miss; last success 2026-06-20 |

## Top runners (by run count)

| # | Skill | Runs | Success | Last status | Dominant exit |
|---|-------|------|---------|-------------|---------------|
| 1 | pr-review | 12 | 92% | pending | ok |
| 2 | code-health | 7 | 100% | success | uncategorized |
| 3 | goal-tracker | 7 | 86% | pending | ok |
| 4 | reflect | 7 | 86% | pending | ok |
| 5 | skill-health | 7 | 86% | pending | ok |
| 6 | surplus-pulse | 7 | 100% | success | ok |
| 7 | batch-health | 6 | 100% | success | ok |
| 8 | gitlawb-fleet-metrics | 6 | 100% | success | uncategorized |
| 9 | heartbeat | 6 | 100% | success | ok |
| 10 | pr-tracker | 6 | 100% | success | ok |
| 11 | skill-freshness | 6 | 100% | success | ok |
| 12 | fleet-control | 5 | 100% | success | uncategorized |
| 13 | github-monitor | 5 | 100% | success | uncategorized |
| 14 | issue-triage | 5 | 100% | success | ok |
| 15 | notegraph | 5 | 100% | success | uncategorized |

*Note: skills with pending in_progress runs (pr-review, goal-tracker, reflect, skill-health) show success/total; in_progress runs excluded from success-pct denominator by spec but counted in total.*

## Failure rate (sorted, ≥1 failure)

Zero failures across 39 active skills this window.

(All 136 runs either succeeded or are in-progress; 0 failed, 0 cancelled.)

## Exit taxonomy distribution

(Sourced from `memory/logs/*.md` — best-effort regex grep, see Step 5. Scanned 4 of 8 log files in the window — 2026-07-05 through 2026-07-08.)

| Bucket | Count | % | Top skills |
|--------|-------|---|------------|
| ok | ~50 | ~68% | heartbeat, surplus-pulse, reflect, skill-health, pr-tracker |
| uncategorized | ~20 | ~27% | gitlawb-fleet-metrics, fleet-control, github-monitor, notegraph, code-health |
| error | ~2 | ~3% | pr-triage (PR_TRIAGE_ERROR — dispatch 403 on cross-org repo) |
| new_info | 1 | ~1% | workflow-security-audit |
| skip_other | ~1 | ~1% | code-health (CODE_HEALTH_SKIP) |
| skip_unchanged | 0 | 0% | — |
| quiet | 0 | 0% | — |
| partial | 0 | 0% | — |

**Fleet exit dominant:** ok (dominant in ~27 skills), uncategorized (~7 skills), new_info (1 skill)

Note on "uncategorized" cluster: gitlawb-fleet-metrics (GLMETRICS_EMPTY), fleet-control (FLEET_EMPTY), github-monitor (GITHUB_MONITOR_EMPTY_CONFIG), and most notegraph runs (NOTEGRAPH_NO_CHANGE) all emit non-standard exit codes that don't match any canonical marker. These are structural-quiet runs, not failures — the underlying GH Actions workflows all succeeded. This is a taxonomy gap, not a health concern.

Note on pr-triage "error": PR_TRIAGE_ERROR reflects a cross-org write permission denial (403 on comment/label dispatch to swarm-ai-research/swarm). All 4 runs show `success` in GH Actions — the error is a dispatch-side limitation, not a skill-level crash.

## Silent scheduled skills (enabled, zero runs)

| Skill | Schedule | Last success | Note |
|-------|----------|-------------|------|
| janitor | `30 5 * * 0` (Sun 05:30 UTC) | 2026-06-20 (~18d) | ISS-006 tributary; Sunday 05:30 pocket chronically dead |
| run-frequency-guard | `0 23 * * *` (daily 23:00 UTC) | never | no cron-state entry; never dispatched across entire ISS-006 window |
| ai-framework-watch | `30 8 * * 1` (Mon 08:30 UTC) | never | no cron-state entry; 3 consecutive Monday non-arms |
| cost-report | `0 7 * * 1` (Mon 07:00 UTC) | 2026-06-20 (~18d) | ISS-008 (filed 2026-07-05); 3rd consecutive Monday miss |

All 4 trace to the same root cause: ISS-006 `messages.yml` `*/5 * * * *` cron underdelivery. The 06:00–07:30 and 23:00 pockets are systemically unreliable. Fix: replace `messages.yml`'s blanket `*/5` with explicit per-slot crons covering every `aeon.yml` timeslot.

## Source status

- skill-runs JSON: ok (gh api succeeded, no fallback needed)
- Window: 168h (2026-07-01T18:44:35Z → 2026-07-08T18:44:35Z)
- aeon.yml: ok
- cron-state.json: ok (42 entries; all consecutive_failures = 0)
- Daily logs scanned: 4/8 for exit taxonomy (2026-07-05 – 2026-07-08; 2026-07-01 – 2026-07-04 not read — best-effort secondary signal, does not affect ground-truth pass/fail counts)

---
*Companion to `skill-health` (per-skill issue filing) and `heartbeat` (per-run pulse). Fleet-wide observability is the gap this skill closes. Methodology: GitHub Actions run history is ground truth for pass/fail; daily-log markers are best-effort secondary signal for exit taxonomy.*
