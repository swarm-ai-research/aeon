# Skill Analytics — 2026-08-26

**Verdict:** 2 scheduled skill(s) didn't run this window — ai-framework-watch (50th silent day) + run-frequency-guard (50th silent day)

*Window: last 7d · 176 runs across 41 skills · 99.4% success · 3 anomalies*

## Anomalies

| Flag | Skill | Detail | Action |
|------|-------|--------|--------|
| 🔴 SILENT | ai-framework-watch | scheduled `30 8 * * 1` (Mon 08:30 UTC) — 0 runs in window; 50th consecutive silent day | investigate cron-state absence; restore SKILL.md or set `enabled: false` |
| 🔴 SILENT | run-frequency-guard | scheduled `0 23 * * *` (daily 23:00 UTC) — 0 runs in window; 50th consecutive silent day | investigate messages.yml matcher / workflow wiring per ISS-021 draft |
| 🟡 ALL_SKIP | code-health | 7/7 runs emitting skip-class exits (`CODE_HEALTH_SKIP_NO_CONFIG` / `CODE_HEALTH_EMPTY_CONFIG`); all blocked by missing `memory/watched-repos.md` — streak-22 | populate `memory/watched-repos.md` OR set `enabled: false` on all 6 watched-repos-dependent skills |

## Top runners (by run count)

| # | Skill | Runs | Success | Last status | Dominant exit |
|---|-------|------|---------|-------------|---------------|
| 1 | pr-review (swarm-ai-research/swarm) | 14 | 100% | success | ok |
| 2 | batch-health | 7 | 100% | success | ok |
| 3 | code-health | 7 | 100% (GHA) | success | skip_other |
| 4 | compute-futures-eda | 7 | 100% | success | ok |
| 5 | fleet-control | 7 | 100% | success | uncategorized |
| 6 | github-monitor | 7 | 100% | success | uncategorized |
| 7 | gitlawb-fleet-metrics | 7 | 100% | success | uncategorized |
| 8 | goal-tracker | 7 | 100% | pending | ok |
| 9 | heartbeat | 7 | 100% | success | ok |
| 10 | issue-triage | 7 | 100% | success | ok |
| 11 | notegraph | 7 | 100% | success | ok |
| 12 | planner | 7 | 100% | success | ok |
| 13 | pr-tracker | 7 | 100% | success | ok |
| 14 | pr-triage (swarm-ai-research/swarm) | 7 | 100% | success | ok |
| 15 | reflect | 7 | 100% | pending | ok |

Additional active skills (≥1 run): memory-flush (4), memory-structural-dedupe (4), agi-tracker (1), changelog (1), compute-macro-correlate (1), compute-pulse (1), config-validator (1), cost-report (2), janitor (1), milestone-tracker (1), repo-revive (1), self-review (1), skill-analytics (2), skill-evals (1), skill-freshness (7), skill-graph (1), skill-health (7), skill-update-check (1), skillpacks (1), stale-content-pr-sweeper (7), suggest-edges (7), surplus-pulse (7), swarm-safety-eval (1), vuln-scanner (1), weekly-shiplog (1), workflow-security-audit (1).

## Failure rate (sorted, ≥1 failure)

| Skill | Runs | Failures | Success rate | Last conclusion |
|-------|------|----------|--------------|-----------------|
| cost-report | 2 | 1 | 50% | success (recovered same cycle 08-24T08:30:52Z) |

Note: 1 failure across 176 total runs. The sole failure (cost-report 08-24T07:39Z) recovered within the same cycle at 08:30Z and is not indicative of a persistent issue. No `consecutive_failures > 0` entries across any skill in cron-state.json.

## Exit taxonomy distribution

| Bucket | Count (est.) | % | Top skills |
|--------|-------------|---|------------|
| ok | ~130 | ~74% | planner, heartbeat, pr-tracker, suggest-edges, notegraph, surplus-pulse, reflect, skill-health, issue-triage, pr-triage, batch-health, stale-content-pr-sweeper, skill-freshness, compute-futures-eda, memory-flush, … |
| uncategorized | ~35 | ~20% | gitlawb-fleet-metrics (GLMETRICS_EMPTY ×7), fleet-control (FLEET_EMPTY ×7), github-monitor (GITHUB_MONITOR_EMPTY_CONFIG ×7), goal-tracker (NO_GOALS on one fire), others |
| skip_other | ~8 | ~5% | code-health (CODE_HEALTH_SKIP_NO_CONFIG / EMPTY_CONFIG ×7) |
| error | ~1 | <1% | cost-report (08-24 07:39Z transient, recovered) |
| quiet | ~2 | ~1% | skill-freshness (FRESHNESS_NO_CHANGE on no-change days), skill-health (hash-stable daily-reminder fires) |
| skip_unchanged | 0 | 0% | — |
| new_info | 0 | 0% | — |
| partial | 0 | 0% | — |

Sourced from `memory/logs/*.md` (08-19 → 08-26) — best-effort regex grep, see Step 5. ~10–20% miss-rate expected; GitHub Actions success/failure counts are ground truth for pass/fail.

Top 3 fleet-dominant exit buckets: **ok (~130), uncategorized (~35), skip_other (~8)**

## Silent scheduled skills (enabled, zero runs)

| Skill | Schedule | Expected runs (7d) | Silent days |
|-------|----------|--------------------|-------------|
| ai-framework-watch | `30 8 * * 1` (Mon 08:30 UTC) | 1 | **50** |
| run-frequency-guard | `0 23 * * *` (daily 23:00 UTC) | 7 | **50** |

Both skills have `enabled: true` in `aeon.yml` but zero entries in `memory/cron-state.json` — they have never dispatched. Root cause tracked in [[enabled-skills-can-never-dispatch]]; ISS-021 draft outstanding 38 days. Fix path: investigate messages.yml matcher + workflow wiring, or land `enabled: false`.

## Source status

- skill-runs JSON: ok (176 runs, 41 skills)
- Window: 168h (2026-08-19T18:57:00Z → 2026-08-26T18:57:00Z)
- aeon.yml: ok
- cron-state.json: ok (44 tracked skills)
- Daily logs scanned: 8/8 for exit taxonomy (08-19 → 08-26)

---
*Companion to `skill-health` (per-skill issue filing) and `heartbeat` (per-run pulse). Fleet-wide observability is the gap this skill closes. Methodology: GitHub Actions run history is ground truth for pass/fail; daily-log markers are best-effort secondary signal for exit taxonomy.*
