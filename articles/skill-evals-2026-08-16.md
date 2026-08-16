# Skill Evals — 2026-08-16

**Verdict:** SKILL_EVALS_REGRESSED
**Coverage:** 14/49 (28%) (first run)
**Diff:** 14 new fail · 0 fixed · 0 still failing · 0 stable · 1 new pass *(BOOTSTRAP — no prior eval article)*

## Action Queue
1. Patch evals.json:heartbeat — `forbidden_pattern:\${var}` triggers on literal `${var}` in skill-log preambles (run summaries write "with `${var}` empty"), not on template substitution failures; restrict assertion scope or remove
2. Investigate swarm-safety-eval — ran successfully today at 07:35Z (last_status: success, 7 runs, 100% rate) but no `articles/swarm-safety-eval-*.md` exists (ISS-005)
3. Dispatch repo-pulse — no article output, likely cron-delivery gap (ISS-009)
4. Add evals.json entry for self-review — pattern: `articles/self-review-*.md`
5. Add evals.json entry for skill-analytics — pattern: `articles/skill-analytics-*.md`
6. Add evals.json entry for fleet-control — pattern: `articles/fleet-status--*.md`
7. Add evals.json entry for skill-freshness — pattern: `articles/skill-freshness-*.md`
8. +31 more uncovered enabled skills — see Coverage Gaps

## Regressions (NEW_FAIL)
*Note: BOOTSTRAP run — all NEW_FAIL labels are first-baseline classifications, not regressions from a known-good state. 13 of 14 are pre-existing chronic issues with open ISS entries; no new issues filed.*

| Skill | Status | Root cause | Issue |
|-------|--------|------------|-------|
| heartbeat | NEW_FAIL | forbidden_pattern:\${var} (false positive — literal `${var}` in log preambles) | ISS-007 (open, diff root_cause) |
| repo-pulse | NEW_FAIL | no_file_match | ISS-009 |
| changelog | NEW_FAIL | no_file_match | ISS-002 |
| push-recap | NEW_FAIL | no_file_match | ISS-010 |
| fork-fleet | NEW_FAIL | no_file_match | ISS-011 |
| cost-report | NEW_FAIL | no_file_match | ISS-008 |
| repo-article | NEW_FAIL | no_file_match | ISS-012 |
| repo-actions | NEW_FAIL | no_file_match | ISS-013 |
| deep-research | NEW_FAIL | no_file_match | ISS-014 |
| hn-digest | NEW_FAIL | no_file_match | ISS-015 |
| rss-digest | NEW_FAIL | no_file_match | ISS-016 |
| polymarket | NEW_FAIL | no_file_match | ISS-017 |
| token-alert | NEW_FAIL | no_file_match | ISS-018 |
| swarm-safety-eval | NEW_FAIL | no_file_match | ISS-005 |

## Full Results
| Skill | Status | Diff | Root cause | Quality | Words | Last output |
|-------|--------|------|------------|---------|-------|-------------|
| heartbeat | FAIL | NEW_FAIL | forbidden_pattern:\${var} | unknown | 4003 | memory/logs/2026-08-16.md |
| repo-pulse | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| changelog | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| push-recap | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| fork-fleet | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| cost-report | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| repo-article | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| repo-actions | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| deep-research | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| hn-digest | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| rss-digest | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| polymarket | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| token-alert | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| skill-health | PASS | NEW_PASS | — | unknown | 527 | memory/skill-health/last-report.json |
| swarm-safety-eval | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |

## Coverage Gaps (enabled in aeon.yml, missing from evals.json)
- self-review — inferred pattern: `articles/self-review-*.md`
- skill-analytics — inferred pattern: `articles/skill-analytics-*.md`
- fleet-control — inferred pattern: `articles/fleet-status--*.md`
- skill-freshness — inferred pattern: `articles/skill-freshness-*.md`
- skill-update-check — inferred pattern: `articles/skill-update-check-*.md`
- pr-tracker — inferred pattern: `memory/logs/*.md`
- planner — inferred pattern: `memory/logs/*.md`
- vuln-scanner — inferred pattern: `articles/vuln-scan--*.md`
- workflow-security-audit — inferred pattern: `articles/workflow-security-audit-*.md`
- weekly-shiplog — inferred pattern: `articles/weekly-shiplog-*.md`
- +25 more — see `./scripts/eval-audit --json` uncovered_enabled list

## Sources
- evals.json=ok · cron-state=ok · skill-health=ok (7 files) · eval-audit=ok · prior-article=none (BOOTSTRAP)
