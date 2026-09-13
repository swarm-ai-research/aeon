# Skill Evals — 2026-09-13

**Verdict:** SKILL_EVALS_REGRESSED
**Coverage:** 14/49 (28%) (first run — BOOTSTRAP)
**Diff:** 13 new fail · 0 fixed · 0 still failing · 0 stable

> Bootstrap: no prior skill-evals article found. All results are `NEW_*`. Of the 13 NEW_FAIL, 12 are pre-existing `no_file_match` failures already tracked by open issues (ISS-002/005/009–018) — all are disabled skills or skills blocked by ISS-001/ISS-006. One is a genuine new regression: heartbeat missing its keyword in today's log, likely due to ISS-006's 08:00Z dead pocket. ISS-008 (cost-report: no_file_match) closes — cost-report now passes.

## Action Queue

1. Investigate heartbeat — missing_pattern:heartbeat|Heartbeat|HEARTBEAT; 08:00Z slot likely dead again (ISS-027)
2. Add evals.json entry for skill-freshness — pattern: `articles/skill-freshness-*.md`
3. Add evals.json entry for vuln-scanner — pattern: `articles/vuln-scan-*.md`
4. Add evals.json entry for surplus-pulse — pattern: `articles/surplus-pulse-*.md`
5. Add evals.json entry for reflect — pattern: `memory/topics/*.md`
6. Add evals.json entry for code-health — pattern: `articles/code-health-*.md`
7. +29 more uncovered enabled — see Coverage Gaps

## Regressions (NEW_FAIL)

| Skill | Status | Root cause | Issue |
|-------|--------|------------|-------|
| heartbeat | NEW_FAIL | missing_pattern:heartbeat\|Heartbeat\|HEARTBEAT | ISS-027 (filed) |
| changelog | NEW_FAIL | no_file_match | ISS-002 (pre-existing) |
| swarm-safety-eval | NEW_FAIL | no_file_match | ISS-005 (pre-existing) |
| repo-pulse | NEW_FAIL | no_file_match | ISS-009 (pre-existing) |
| push-recap | NEW_FAIL | no_file_match | ISS-010 (pre-existing) |
| fork-fleet | NEW_FAIL | no_file_match | ISS-011 (pre-existing) |
| repo-article | NEW_FAIL | no_file_match | ISS-012 (pre-existing) |
| repo-actions | NEW_FAIL | no_file_match | ISS-013 (pre-existing) |
| deep-research | NEW_FAIL | no_file_match | ISS-014 (pre-existing) |
| hn-digest | NEW_FAIL | no_file_match | ISS-015 (pre-existing) |
| rss-digest | NEW_FAIL | no_file_match | ISS-016 (pre-existing) |
| polymarket | NEW_FAIL | no_file_match | ISS-017 (pre-existing) |
| token-alert | NEW_FAIL | no_file_match | ISS-018 (pre-existing) |

*12 of 13 are disabled skills with pre-existing tracked issues. Only ISS-027 is newly filed.*

## Recovered (FIXED)

| Skill | Was | Now |
|-------|-----|-----|
| cost-report | ISS-008 open (no_file_match) | PASS — articles/cost-report-2026-09-07.md, 466 words, $104.95 passes numeric check |

*ISS-008 closed (detected_by: skill-evals; file confirmed, all assertions pass).*

## Full Results

| Skill | Status | Diff | Root cause | Quality | Words | Last output |
|-------|--------|------|------------|---------|-------|-------------|
| heartbeat | FAIL | NEW_FAIL | missing_pattern:heartbeat\|Heartbeat\|HEARTBEAT | unknown | 158 | memory/logs/2026-09-13.md |
| repo-pulse | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | — |
| changelog | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | — |
| push-recap | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | — |
| fork-fleet | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | — |
| cost-report | PASS | NEW_PASS | — | unknown | 466 | articles/cost-report-2026-09-07.md |
| repo-article | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | — |
| repo-actions | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | — |
| deep-research | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | — |
| hn-digest | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | — |
| rss-digest | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | — |
| polymarket | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | — |
| token-alert | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | — |
| skill-health | PASS | NEW_PASS | — | unknown | ~800 | memory/skill-health/last-report.json |
| swarm-safety-eval | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | — |

## Coverage Gaps (enabled in aeon.yml, missing from evals.json)

First 10 of 35 uncovered enabled skills:

- batch-health — inferred pattern: `memory/logs/*.md`
- code-health — inferred pattern: `articles/code-health-*.md`
- compute-futures-eda — inferred pattern: `memory/logs/*.md`
- compute-macro-correlate — inferred pattern: `memory/topics/compute-futures-macro-correlations.md`
- compute-pulse — inferred pattern: `memory/logs/*.md`
- config-validator — inferred pattern: `memory/logs/*.md`
- fleet-control — inferred pattern: `articles/fleet-status--*.md`
- github-monitor — inferred pattern: `memory/logs/*.md`
- gitlawb-fleet-metrics — inferred pattern: `memory/logs/*.md`
- goal-tracker — inferred pattern: `memory/logs/*.md`

+25 more (reflect, skill-freshness, vuln-scanner, surplus-pulse, self-review, skill-analytics, skill-update-check, workflow-security-audit, weekly-shiplog, notegraph, planner, pr-tracker, pr-triage, repo-revive, issue-triage, janitor, memory-flush, memory-structural-dedupe, milestone-tracker, skill-graph, skill-repair, skillpacks, stale-content-pr-sweeper, suggest-edges, agi-tracker).

## Sources

- evals.json=ok · cron-state=ok · skill-health=ok · eval-audit=ok · prior-article=none (BOOTSTRAP)
