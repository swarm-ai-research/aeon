# Skill Evals — 2026-08-09

**Verdict:** SKILL_EVALS_REGRESSED
**Coverage:** 14/49 (28%) (first run)
**Diff:** 13 new fail · 0 fixed · 0 still failing · 0 stable
> _BOOTSTRAP run — no prior eval article found. All statuses are NEW_*. Skills with open issues had those issues suppressed from re-filing (deduplication)._

## Action Queue
1. Investigate changelog — no_file_match (ISS-002); ran 2026-08-03 but article absent at `articles/changelog-*.md`
2. Investigate swarm-safety-eval — no_file_match (ISS-005); ran today (SSE_EMPTY — `memory/agent-first/` absent)
3. Investigate cost-report — no_file_match (ISS-008); ran 2026-07-27 but no article at `articles/cost-report-*.md`
4. Dispatch repo-pulse — no output; skill is disabled in aeon.yml (`enabled: false`) — re-enable or remove from evals.json
5. Dispatch push-recap — no output; skill is disabled in aeon.yml — re-enable or remove from evals.json
6. Dispatch fork-fleet — no output; skill is disabled in aeon.yml — re-enable or remove from evals.json
7. Add evals.json entry for batch-health — inferred pattern: `memory/logs/*.md`
8. Add evals.json entry for skill-freshness — inferred pattern: `articles/skill-freshness-*.md`

## Regressions (NEW_FAIL — BOOTSTRAP first observation)

| Skill | Status | Root cause | Issue | Notes |
|-------|--------|------------|-------|-------|
| changelog | NO_OUTPUT | no_file_match | [ISS-002](../memory/issues/ISS-002.md) | Ran 2026-08-03; output at wrong path or suppressed |
| swarm-safety-eval | NO_OUTPUT | no_file_match | [ISS-005](../memory/issues/ISS-005.md) | Ran today — SSE_EMPTY; `memory/agent-first/` absent |
| cost-report | NO_OUTPUT | no_file_match | [ISS-008](../memory/issues/ISS-008.md) | Ran 2026-07-27; article absent at expected path |
| repo-pulse | NO_OUTPUT | no_file_match | [ISS-009](../memory/issues/ISS-009.md) | Not in cron-state; skill disabled in aeon.yml |
| push-recap | NO_OUTPUT | no_file_match | [ISS-010](../memory/issues/ISS-010.md) | Not in cron-state; skill disabled in aeon.yml |
| fork-fleet | NO_OUTPUT | no_file_match | [ISS-011](../memory/issues/ISS-011.md) | Not in cron-state; skill disabled in aeon.yml |
| repo-article | NO_OUTPUT | no_file_match | [ISS-012](../memory/issues/ISS-012.md) | Not in cron-state; skill disabled in aeon.yml |
| repo-actions | NO_OUTPUT | no_file_match | [ISS-013](../memory/issues/ISS-013.md) | Not in cron-state; skill disabled in aeon.yml |
| deep-research | NO_OUTPUT | no_file_match | [ISS-014](../memory/issues/ISS-014.md) | Not in cron-state; workflow_dispatch only |
| hn-digest | NO_OUTPUT | no_file_match | [ISS-015](../memory/issues/ISS-015.md) | Not in cron-state; `hacker-news-digest` in aeon.yml, name mismatch |
| rss-digest | NO_OUTPUT | no_file_match | [ISS-016](../memory/issues/ISS-016.md) | Not in cron-state; skill disabled in aeon.yml |
| polymarket | NO_OUTPUT | no_file_match | [ISS-017](../memory/issues/ISS-017.md) | Not in cron-state; no `polymarket` skill in aeon.yml (see monitor-polymarket) |
| token-alert | NO_OUTPUT | no_file_match | [ISS-018](../memory/issues/ISS-018.md) | Not in cron-state; skill disabled in aeon.yml |

_No new issues filed: all 13 NO_OUTPUT skills already have open issues in INDEX.md — deduplication suppressed re-filing._

## Full Results

| Skill | Status | Diff | Root cause | Quality | Words | Last output |
|-------|--------|------|------------|---------|-------|-------------|
| heartbeat | PASS | NEW_PASS | — | unknown | ≫20 | memory/logs/2026-08-09.md |
| skill-health | PASS | NEW_PASS | — | unknown | 394 | memory/skill-health/last-report.json (2026-08-08) |
| changelog | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | N/A | N/A |
| swarm-safety-eval | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | N/A | N/A |
| cost-report | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | N/A | N/A |
| repo-pulse | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | N/A | N/A |
| push-recap | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | N/A | N/A |
| fork-fleet | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | N/A | N/A |
| repo-article | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | N/A | N/A |
| repo-actions | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | N/A | N/A |
| deep-research | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | N/A | N/A |
| hn-digest | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | N/A | N/A |
| rss-digest | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | N/A | N/A |
| polymarket | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | N/A | N/A |
| token-alert | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | N/A | N/A |

**Note on ISS-007:** heartbeat passes today (pattern `## Heartbeat` found in `memory/logs/2026-08-09.md`). ISS-007 was filed on 2026-07-05 when heartbeat missed its 08:00 pocket, consistent with the ISS-006 cron underdelivery pattern rather than a skill logic defect. Per MEMORY.md, consider closing ISS-007 as a false positive. BOOTSTRAP status prevents formal FIXED handling in this run.

## Coverage Gaps (enabled in aeon.yml, missing from evals.json)

Top 10 of 35 uncovered enabled skills:

- batch-health — inferred pattern: `memory/logs/*.md`
- skill-freshness — inferred pattern: `articles/skill-freshness-*.md`
- skill-analytics — inferred pattern: `articles/skill-analytics-*.md`
- self-review — inferred pattern: `articles/self-review-*.md`
- planner — inferred pattern: `memory/logs/*.md`
- reflect — inferred pattern: `memory/topics/*.md`
- goal-tracker — inferred pattern: `memory/logs/*.md`
- pr-tracker — inferred pattern: `memory/logs/*.md`
- code-health — inferred pattern: `articles/code-health-*.md`
- surplus-pulse — inferred pattern: `memory/topics/projects.md`

+25 more — see `./scripts/eval-audit --json` uncovered_enabled array.

## Sources

- evals.json=ok · cron-state=ok · skill-health=ok · eval-audit=ok · prior-article=none (BOOTSTRAP)
