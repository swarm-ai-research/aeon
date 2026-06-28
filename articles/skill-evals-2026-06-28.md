# Skill Evals — 2026-06-28

**Verdict:** SKILL_EVALS_RECOVERED
**Coverage:** 14/50 (28%) ↔ flat vs prior (2026-06-21)
**Diff:** 0 new fail · 1 fixed · 2 still failing · 12 stable

> heartbeat recovered — today's log (`memory/logs/2026-06-28.md`) contains both `## Heartbeat` and `HEARTBEAT_DEGRADED`, satisfying the required-pattern check that failed in the 2026-06-21 eval. swarm-safety-eval now runs successfully (cron-state: `last_success 2026-06-28T08:15:47Z`) but its SSE_EMPTY path writes to the daily log rather than an article, so the `articles/swarm-safety-eval-*.md` eval pattern still shows NO_OUTPUT — the issue classification has shifted from "skill not running" to "skill runs but produces no article when ledger is absent."

## Action Queue
1. Investigate changelog — no_file_match (ISS-002) — 121 runs, 1 success; enabled Mon 16:00 UTC; may require `memory/watched-repos.md` to produce output
2. Patch evals.json:swarm-safety-eval — `articles/swarm-safety-eval-*.md` misses SSE_EMPTY runs which write to `memory/logs/`; consider adding a log-based assertion or documenting that NO_OUTPUT is expected when ledger is absent (update ISS-005 category from `missing-secret-or-cron` to `permanent-limitation`)
3. Add evals.json entry for code-health — pattern: `articles/code-health-*.md`
4. Add evals.json entry for self-review — pattern: `articles/self-review-*.md`
5. Add evals.json entry for skill-analytics — pattern: `articles/skill-analytics-*.md`
6. Add evals.json entry for skill-freshness — pattern: `articles/skill-freshness-*.md`
7. Add evals.json entry for weekly-shiplog — pattern: `articles/weekly-shiplog-*.md`

## Recovered (FIXED)
| Skill | Was | Now |
|-------|-----|-----|
| heartbeat | STILL_FAIL (missing_pattern:heartbeat\|Heartbeat\|HEARTBEAT) | PASS |

## Still Failing
| Skill | Status | Root cause | Issue | Failing since |
|-------|--------|------------|-------|---------------|
| changelog | NO_OUTPUT | no_file_match | ISS-002 | 2026-06-20 |
| swarm-safety-eval | NO_OUTPUT | no_file_match (SSE_EMPTY — skill runs, no article produced) | ISS-005 | 2026-06-20 |

## Full Results
| Skill | Status | Diff | Root cause | Quality | Words | Last output | Enabled |
|-------|--------|------|------------|---------|-------|-------------|---------|
| heartbeat | PASS | FIXED | — | unknown | ~700 | memory/logs/2026-06-28.md | yes |
| repo-pulse | NO_OUTPUT | STABLE | no_file_match | unknown | — | none | no |
| changelog | NO_OUTPUT | STILL_FAIL | no_file_match | unknown | — | none | yes |
| push-recap | NO_OUTPUT | STABLE | no_file_match | unknown | — | none | no |
| fork-fleet | NO_OUTPUT | STABLE | no_file_match | unknown | — | none | no |
| cost-report | PASS | STABLE | — | unknown | ~150 | articles/cost-report-2026-06-20.md | yes |
| repo-article | NO_OUTPUT | STABLE | no_file_match | unknown | — | none | no |
| repo-actions | NO_OUTPUT | STABLE | no_file_match | unknown | — | none | no |
| deep-research | NO_OUTPUT | STABLE | no_file_match | unknown | — | none | dispatch |
| hn-digest | NO_OUTPUT | STABLE | no_file_match | unknown | — | none | no* |
| rss-digest | NO_OUTPUT | STABLE | no_file_match | unknown | — | none | no |
| polymarket | NO_OUTPUT | STABLE | no_file_match | unknown | — | none | no* |
| token-alert | NO_OUTPUT | STABLE | no_file_match | unknown | — | none | no |
| skill-health | PASS | STABLE | — | unknown | ~400 | memory/skill-health/last-report.json | yes |
| swarm-safety-eval | NO_OUTPUT | STILL_FAIL | no_file_match | unknown | — | none | yes |

\* evals.json key does not match skill name in aeon.yml (`hn-digest` → `hacker-news-digest`; `polymarket` → `monitor-polymarket`)

## Coverage Gaps (enabled in aeon.yml, missing from evals.json)
Top 5 by inferrability:
- code-health — inferred pattern: `articles/code-health-*.md`
- self-review — inferred pattern: `articles/self-review-*.md`
- skill-analytics — inferred pattern: `articles/skill-analytics-*.md`
- skill-freshness — inferred pattern: `articles/skill-freshness-*.md`
- weekly-shiplog — inferred pattern: `articles/weekly-shiplog-*.md`

+31 more — run `./scripts/eval-audit --json` for the full uncovered_enabled list.

## Sources
- evals.json=ok · cron-state=ok · skill-health=ok · eval-audit=ok · prior-article=ok (2026-06-21)
