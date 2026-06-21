# Skill Evals — 2026-06-21

**Verdict:** SKILL_EVALS_RECOVERED
**Coverage:** 14/50 (28%) → flat vs prior
**Diff:** 0 new fail · 2 fixed · 3 still failing · 10 stable

> cost-report and skill-health recovered — both produced valid output after the post-OAuth-outage recovery batch on 2026-06-20. No new regressions this run. Three enabled skills remain unresolved.

## Action Queue
1. Investigate heartbeat — missing_pattern:heartbeat|Heartbeat|HEARTBEAT (ISS-001) [today's log has stale-content-pr-sweeper + notegraph entries but no heartbeat section; heartbeat cron is 08:00 UTC, skill-evals runs 09:00 UTC — heartbeat either failed silently or the log write was dropped]
2. Dispatch changelog — no output in 7+ days (ISS-002) [enabled Mon 16:00 UTC; 120 runs, 0 successes; root cause: `memory/watched-repos.md` absent — create this file to unblock]
3. Dispatch swarm-safety-eval — no output in 7+ days (ISS-005) [enabled Sun 07:30 UTC; today is Sunday and it should have run; 0 lifetime successes — no watched agent fleet to evaluate]
4. Add evals.json entry for code-health — pattern: `articles/code-health-*.md`
5. Add evals.json entry for self-review — pattern: `articles/self-review-*.md`
6. Add evals.json entry for skill-analytics — pattern: `articles/skill-analytics-*.md`
7. Add evals.json entry for skill-freshness — pattern: `articles/skill-freshness-*.md`
8. Add evals.json entry for weekly-shiplog — pattern: `articles/weekly-shiplog-*.md`

## Recovered (FIXED)
| Skill | Was | Now |
|-------|-----|-----|
| cost-report | NO_OUTPUT | PASS |
| skill-health | NO_OUTPUT | PASS |

## Still Failing
| Skill | Status | Root cause | Issue | Failing since |
|-------|--------|------------|-------|---------------|
| heartbeat | FAIL | missing_pattern:heartbeat\|Heartbeat\|HEARTBEAT | ISS-001 | 2026-06-20 |
| changelog | NO_OUTPUT | no_file_match | ISS-002 | 2026-06-20 |
| swarm-safety-eval | NO_OUTPUT | no_file_match | ISS-005 | 2026-06-20 |

## Full Results
| Skill | Status | Diff | Root cause | Quality | Words | Last output | Enabled |
|-------|--------|------|------------|---------|-------|-------------|---------|
| heartbeat | FAIL | STILL_FAIL | missing_pattern:heartbeat\|... | unknown | ~130 | 2026-06-21.md | yes |
| repo-pulse | NO_OUTPUT | STABLE | no_file_match | unknown | — | none | no |
| changelog | NO_OUTPUT | STILL_FAIL | no_file_match | unknown | — | none | yes |
| push-recap | NO_OUTPUT | STABLE | no_file_match | unknown | — | none | no |
| fork-fleet | NO_OUTPUT | STABLE | no_file_match | unknown | — | none | no |
| cost-report | PASS | FIXED | — | unknown | ~150 | 2026-06-20.md | yes |
| repo-article | NO_OUTPUT | STABLE | no_file_match | unknown | — | none | no |
| repo-actions | NO_OUTPUT | STABLE | no_file_match | unknown | — | none | no |
| deep-research | NO_OUTPUT | STABLE | no_file_match | unknown | — | none | no |
| hn-digest | NO_OUTPUT | STABLE | no_file_match | unknown | — | none | no* |
| rss-digest | NO_OUTPUT | STABLE | no_file_match | unknown | — | none | no |
| polymarket | NO_OUTPUT | STABLE | no_file_match | unknown | — | none | no* |
| token-alert | NO_OUTPUT | STABLE | no_file_match | unknown | — | none | no |
| skill-health | PASS | FIXED | — | unknown | ~100 | last-report.json | yes |
| swarm-safety-eval | NO_OUTPUT | STILL_FAIL | no_file_match | unknown | — | none | yes |

\* evals.json key does not match skill name in aeon.yml

## Coverage Gaps (enabled in aeon.yml, missing from evals.json)
Top 5 by inferrability:
- code-health — inferred pattern: `articles/code-health-*.md`
- self-review — inferred pattern: `articles/self-review-*.md`
- skill-analytics — inferred pattern: `articles/skill-analytics-*.md`
- skill-freshness — inferred pattern: `articles/skill-freshness-*.md`
- weekly-shiplog — inferred pattern: `articles/weekly-shiplog-*.md`

+31 more — run `./scripts/eval-audit --json` for full uncovered_enabled list.

## Sources
- evals.json=ok · cron-state=ok · skill-health=ok · eval-audit=ok · prior-article=ok (2026-06-20)
