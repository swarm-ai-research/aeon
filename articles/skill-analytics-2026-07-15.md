# Skill Analytics — 2026-07-15

**Verdict:** 3 scheduled skill(s) didn't run this window — run-frequency-guard, weekly-shiplog, ai-framework-watch

*Window: last 7d · 143 runs across 40 skills · 100% success · 3 anomalies*

## Anomalies

| Flag | Skill | Detail | Action |
|------|-------|--------|--------|
| 🔴 SILENT | run-frequency-guard | scheduled `0 23 * * *` (daily 23:00 UTC) but zero runs in window | check workflow / scheduler |
| 🔴 SILENT | weekly-shiplog | scheduled `0 9 * * 1` (Mon 09:00 UTC) — expected 2026-07-13, zero runs in window | check workflow / scheduler |
| 🔴 SILENT | ai-framework-watch | scheduled `30 8 * * 1` (Mon 08:30 UTC) — expected 2026-07-13, zero runs in window | check workflow / scheduler |

## Top runners (by run count)

| # | Skill | Runs | Success | Last status | Dominant exit |
|---|-------|------|---------|-------------|---------------|
| 1 | pr-review | 13 | 100% | success | ok |
| 2 | code-health | 7 | 100% | success | ok |
| 3 | goal-tracker | 7 | 100% | success | ok |
| 4 | pr-tracker | 7 | 100% | success | ok |
| 5 | reflect | 7 | 100% | success | ok |
| 6 | skill-health | 7 | 100% | success | ok |
| 7 | fleet-control | 6 | 100% | success | uncategorized |
| 8 | github-monitor | 6 | 100% | success | uncategorized |
| 9 | issue-triage | 6 | 100% | success | ok |
| 10 | notegraph | 6 | 100% | success | ok |
| 11 | pr-triage | 6 | 100% | success | ok |
| 12 | suggest-edges | 6 | 100% | success | ok |
| 13 | surplus-pulse | 6 | 100% | success | ok |
| 14 | batch-health | 5 | 100% | success | ok |
| 15 | gitlawb-fleet-metrics | 5 | 100% | success | uncategorized |

## Failure rate (sorted, ≥1 failure)

Zero failures across 40 skills this window.

## Exit taxonomy distribution

*Sourced from `memory/logs/*.md` — best-effort regex grep. ~10–20% miss rate expected; GHA run counts above are ground truth.*

| Bucket | Count | % | Top skills |
|--------|-------|---|------------|
| ok | ~91 | 64% | pr-review (13), reflect (7), goal-tracker (7), pr-tracker (7), pr-triage (5) |
| uncategorized | ~51 | 36% | fleet-control (6), github-monitor (6), gitlawb-fleet-metrics (5), compute-futures-eda (4) |
| error | 1 | <1% | suggest-edges (2026-07-14 SUGGEST_EDGES_ERROR — known PAT block, not a script crash) |
| skip_unchanged | 0 | 0% | — |
| new_info | 0 | 0% | — |
| quiet | 0 | 0% | — |
| partial | 0 | 0% | — |

## Silent scheduled skills (enabled, zero runs)

| Skill | Schedule | Expected run in window |
|-------|----------|----------------------|
| run-frequency-guard | `0 23 * * *` (daily 23:00 UTC) | Every day — 7 expected, 0 fired |
| weekly-shiplog | `0 9 * * 1` (Mon 09:00 UTC) | 2026-07-13 09:00 UTC |
| ai-framework-watch | `30 8 * * 1` (Mon 08:30 UTC) | 2026-07-13 08:30 UTC |

Note: `ai-framework-watch` has no entry in `cron-state.json` and has never appeared in the skill-runs snapshot — consistent with [[enabled-skills-can-never-dispatch]] (enabled + SKILL.md present, but cron never triggered). `run-frequency-guard` is in the same category. `weekly-shiplog` last ran 2026-07-06 (confirmed in cron-state) but missed its 2026-07-13 slot.

## Source status

- skill-runs JSON: ok
- Window: 168h (2026-07-08T19:36:04Z → 2026-07-15T19:36:04Z)
- aeon.yml: ok
- cron-state.json: ok
- Daily logs scanned: 8/8 (2026-07-08 through 2026-07-15)

---
*Companion to `skill-health` (per-skill issue filing) and `heartbeat` (per-run pulse). Fleet-wide observability is the gap this skill closes. Methodology: GitHub Actions run history is ground truth for pass/fail; daily-log markers are best-effort secondary signal for exit taxonomy.*
