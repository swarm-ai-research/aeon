# Skill Evals — 2026-07-12

**Verdict:** SKILL_EVALS_REGRESSED
**Coverage:** 14/49 (28%) (first run — BOOTSTRAP)
**Diff:** 13 new fail · 0 fixed · 0 still failing · 0 stable · 2 new pass

## Action Queue
1. Dispatch repo-pulse — no output, never dispatched (ISS-009)
2. Dispatch push-recap — no output, never dispatched (ISS-010)
3. Dispatch fork-fleet — no output, never dispatched (ISS-011)
4. Dispatch deep-research — no output, never dispatched (ISS-014)
5. Dispatch polymarket — no output, never dispatched (ISS-017)
6. Dispatch token-alert — no output, never dispatched (ISS-018)
7. Dispatch repo-article / repo-actions / hn-digest / rss-digest — no output, never dispatched (+4 more: ISS-012, ISS-013, ISS-015, ISS-016)
8. Add evals.json entry for self-review — pattern: `articles/self-review-*.md`

## Regressions (NEW_FAIL)
| Skill | Status | Root cause | Issue |
|-------|--------|------------|-------|
| repo-pulse | NO_OUTPUT | no_file_match | ISS-009 (new) |
| push-recap | NO_OUTPUT | no_file_match | ISS-010 (new) |
| fork-fleet | NO_OUTPUT | no_file_match | ISS-011 (new) |
| repo-article | NO_OUTPUT | no_file_match | ISS-012 (new) |
| repo-actions | NO_OUTPUT | no_file_match | ISS-013 (new) |
| deep-research | NO_OUTPUT | no_file_match | ISS-014 (new) |
| hn-digest | NO_OUTPUT | no_file_match | ISS-015 (new — possibly disabled in aeon.yml) |
| rss-digest | NO_OUTPUT | no_file_match | ISS-016 (new) |
| polymarket | NO_OUTPUT | no_file_match | ISS-017 (new) |
| token-alert | NO_OUTPUT | no_file_match | ISS-018 (new) |
| changelog | NO_OUTPUT | no_file_match | ISS-002 (existing) |
| cost-report | NO_OUTPUT | no_file_match | ISS-008 (existing) |
| swarm-safety-eval | NO_OUTPUT | no_file_match (SSE_EMPTY → log only) | ISS-005 (existing) |

**Note — BOOTSTRAP run:** No prior eval article exists. Every result is classified as NEW_* with no prior state to diff against. The 10 newly filed issues (ISS-009–018) are likely tributaries of ISS-006 (messages.yml cron underdelivery) or ISS-001 (OAuth denominator burn); investigate dispatch wiring before treating as independent failures. ISS-007 (heartbeat: missing_pattern) is not closed this run — BOOTSTRAP mode produces no FIXED results; it will close in a subsequent run if heartbeat continues to pass.

## Full Results
| Skill | Status | Diff | Root cause | Quality | Words | Last output |
|-------|--------|------|------------|---------|-------|-------------|
| heartbeat | PASS | NEW_PASS | — | unknown | 4,123 | 2026-07-12 (today) |
| skill-health | PASS | NEW_PASS | — | unknown | 392 | 2026-07-11 |
| changelog | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | never (ISS-002 open since 2026-06-20) |
| cost-report | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | last run 2026-06-20 (22d, no article) |
| swarm-safety-eval | NO_OUTPUT | NEW_FAIL | no_file_match (SSE_EMPTY → log) | — | — | ran today, SSE_EMPTY (ISS-005 open) |
| repo-pulse | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | never dispatched |
| push-recap | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | never dispatched |
| fork-fleet | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | never dispatched |
| repo-article | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | never dispatched |
| repo-actions | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | never dispatched |
| deep-research | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | never dispatched |
| hn-digest | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | never dispatched (possibly disabled) |
| rss-digest | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | never dispatched |
| polymarket | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | never dispatched |
| token-alert | NO_OUTPUT | NEW_FAIL | no_file_match | — | — | never dispatched |

## Coverage Gaps (enabled in aeon.yml, missing from evals.json)
Top 10 of 35 uncovered enabled skills:

- batch-health — inferred pattern: `memory/logs/*.md`
- self-review — inferred pattern: `articles/self-review-*.md`
- skill-analytics — inferred pattern: `articles/skill-analytics-*.md`
- skill-freshness — inferred pattern: `articles/skill-freshness-*.md`
- vuln-scanner — inferred pattern: `articles/vuln-scan--*.md`
- workflow-security-audit — inferred pattern: `articles/workflow-security-audit-*.md`
- skill-update-check — inferred pattern: `articles/skill-update-check-*.md`
- weekly-shiplog — inferred pattern: `articles/weekly-shiplog-*.md`
- planner — inferred pattern: `memory/logs/*.md`
- memory-flush — inferred pattern: `memory/topics/skills-history.md`

+25 more — see eval-audit output for full list.

## Sources
- evals.json=ok · cron-state=ok · skill-health=ok · eval-audit=ok · prior-article=none (BOOTSTRAP)
