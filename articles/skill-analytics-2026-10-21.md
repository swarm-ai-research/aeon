# Skill Analytics — 2026-10-21

**Verdict:** 7 scheduled skill(s) didn't run this window — compute-macro-correlate, config-validator, self-review, skill-evals, cost-report, agi-tracker, milestone-tracker

*Window: last 7d · 86 runs across 33 skills · 100% success · 7 anomalies*

## Anomalies

| Flag | Skill | Detail | Action |
|------|-------|--------|--------|
| 🔴 SILENT | compute-macro-correlate | scheduled `30 6 * * 0` (Sun 06:30Z) — zero runs in window | check ISS-006 Sunday 06:30Z pocket |
| 🔴 SILENT | config-validator | scheduled `0 7 * * 0` (Sun 07:00Z) — zero runs in window | check ISS-006 Sunday 07Z cluster |
| 🔴 SILENT | self-review | scheduled `30 18 * * 0` (Sun 18:30Z) — zero runs in window | check Sunday 18:30Z pocket |
| 🔴 SILENT | skill-evals | scheduled `0 9 * * 0` (Sun 09:00Z) — zero runs in window | check Sunday 09Z pocket |
| 🔴 SILENT | cost-report | scheduled `0 7 * * 1` (Mon 07:00Z) — zero runs in window | check Monday 07Z pocket |
| 🔴 SILENT | agi-tracker | scheduled `0 13 * * 1` (Mon 13:00Z) — zero runs in window | known: `skills/agi-tracker/SKILL.md` absent; disable or restore |
| 🔴 SILENT | milestone-tracker | scheduled `0 12 * * 1` (Mon 12:00Z) — zero runs in window | check Monday 12Z pocket |

All Sunday scheduled skills (compute-macro-correlate, config-validator, self-review, skill-evals) were silent on 2026-10-18 — consistent with ISS-006 Sunday pocket damage. Monday (10-19) cost-report and milestone-tracker also silent. agi-tracker is a known no-op (no SKILL.md).

## Top runners (by run count)

| # | Skill | Runs | Success | Last status | Dominant exit |
|---|-------|------|---------|-------------|---------------|
| 1 | pr-review (swarm) | 9 | 89% | pending | ok |
| 2 | pr-tracker | 6 | 100% | success | ok |
| 3 | stale-content-pr-sweeper | 6 | 100% | success | ok |
| 4 | goal-tracker | 5 | 80% | pending | uncategorized |
| 5 | notegraph | 5 | 100% | success | ok |
| 6 | reflect | 5 | 100% | success | ok |
| 7 | skill-health | 5 | 80% | pending | ok |
| 8 | fleet-control | 4 | 100% | success | uncategorized |
| 9 | github-monitor | 4 | 100% | success | uncategorized |
| 10 | issue-triage | 4 | 100% | success | ok |
| 11 | pr-triage (swarm) | 4 | 100% | success | ok |
| 12 | code-health | 3 | 100% | success | ok |
| 13 | suggest-edges | 3 | 100% | success | uncategorized |
| 14 | surplus-pulse | 3 | 100% | success | ok |
| 15 | compute-futures-eda | 2 | 100% | success | uncategorized |

Note: "pending" = 1 run currently in_progress at time of snapshot; success counts only completed runs.

## Failure rate (sorted, ≥1 failure)

Zero failures across 33 skills this window. All 86 runs concluded success or are in-progress (5 pending).

## Exit taxonomy distribution

*Sourced from `memory/logs/*.md` — best-effort regex grep (Step 5). Expected 10–20% miss rate; GitHub Actions counts above are ground truth.*

| Bucket | Count | % | Top skills |
|--------|-------|---|------------|
| ok | ~44 | 51% | stale-content-pr-sweeper (6), pr-tracker (6), notegraph (5), reflect (5), skill-health (5) |
| uncategorized | ~42 | 49% | pr-review (9), goal-tracker (5), fleet-control (4), github-monitor (4), suggest-edges (3) |
| skip_unchanged | 0 | 0% | — |
| new_info | 0 | 0% | — |
| quiet | 0 | 0% | — |
| error | 0 | 0% | — |
| partial | 0 | 0% | — |

High uncategorized share reflects skills that emit custom _OK variants (e.g., `ISSUE_TRIAGE_OK no-watched-repos`, `PR_TRIAGE_OK no-candidates`) captured in the ok bucket above, and skills that log success without a regex-matchable marker. No error-class exits observed.

## Silent scheduled skills (enabled, zero runs)

| Skill | Schedule | Notes |
|-------|----------|-------|
| compute-macro-correlate | `30 6 * * 0` (Sun 06:30Z) | ISS-006 06:30Z Sunday pocket dead; last run pre-window |
| config-validator | `0 7 * * 0` (Sun 07:00Z) | ISS-006 Sunday 07Z cluster; last run pre-window |
| self-review | `30 18 * * 0` (Sun 18:30Z) | Sunday 18:30Z pocket; last run pre-window |
| skill-evals | `0 9 * * 0` (Sun 09:00Z) | Sunday 09Z pocket; last run 2026-09-13 |
| cost-report | `0 7 * * 1` (Mon 07:00Z) | Monday 07Z pocket; last run pre-window |
| agi-tracker | `0 13 * * 1` (Mon 13:00Z) | Known: `skills/agi-tracker/SKILL.md` absent — no-op dispatch; see action queue |
| milestone-tracker | `0 12 * * 1` (Mon 12:00Z) | Monday 12Z pocket; last run pre-window |

Pattern: all 4 Sunday-scheduled skills silent (consistent with ISS-006 Sunday pocket damage). 2 of 3 Monday-scheduled skills silent (cost-report + milestone-tracker); weekly-shiplog `0 9 * * 1` was the sole Monday success (10-19T09:00Z).

## Source status

- skill-runs JSON: ok
- Window: 168h (2026-10-14T19:56:56Z → 2026-10-21T19:56:56Z)
- aeon.yml: ok
- cron-state.json: ok (all `consecutive_failures: 0`)
- Daily logs scanned: 8/8 for exit taxonomy (2026-10-14 → 2026-10-21)

---
*Companion to `skill-health` (per-skill issue filing) and `heartbeat` (per-run pulse). Fleet-wide observability is the gap this skill closes. Methodology: GitHub Actions run history is ground truth for pass/fail; daily-log markers are best-effort secondary signal for exit taxonomy.*
