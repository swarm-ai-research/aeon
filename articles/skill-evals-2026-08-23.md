# Skill Evals — 2026-08-23

**Verdict:** SKILL_EVALS_REGRESSED
**Coverage:** 14/49 (28%) (first run)
**Diff:** 13 new fail · 1 fixed · 0 still failing · 0 stable

> **Note — BOOTSTRAP run.** No prior eval article exists; all results are labeled NEW_* vs. the existing open issues in `memory/issues/INDEX.md`. The 13 NEW_FAILs are all `no_file_match` on article-based skills; every one is already tracked by an open ISS. No new issues filed. ISS-007 closed: heartbeat now passes its required-pattern check.

## Action Queue
1. Investigate article commits — 12 of 13 failing skills write to `articles/`; only `skill-freshness-2026-08-23.md` is present in `articles/` today, suggesting article-writing skills either don't commit their output or snapshot-rebases clobber it. Auditing which skills commit vs. write-ephemerally would unblock ISS-002/005/008–018 in one fix.
2. Dispatch swarm-safety-eval — SSE_EMPTY: `memory/agent-first/` ledger absent; skill runs but produces no article (ISS-005)
3. Dispatch cost-report — `last_success: 2026-08-17T07:55:11Z` (6d ago) but no article found in git; if skill commits to a branch, ensure merge path (ISS-008)
4. Add spec entry for `batch-health` — inferred pattern: `memory/logs/*.md`
5. Add spec entry for `planner` — inferred pattern: `memory/logs/*.md`
6. Add spec entry for `pr-tracker` — inferred pattern: `memory/logs/*.md`
7. Add spec entry for `skill-freshness` — inferred pattern: `articles/skill-freshness-*.md`
8. +28 more enabled skills without coverage — see Coverage Gaps

## Recovered (FIXED)
| Skill | Was | Now |
|-------|-----|-----|
| heartbeat | ISS-007 open (missing_pattern:heartbeat\|Heartbeat\|HEARTBEAT, filed 2026-07-05 due to ISS-006 cron silence — heartbeat didn't run that day) | PASS — `memory/logs/2026-08-23.md` contains `HEARTBEAT_OK` and multiple `heartbeat` references; pattern unambiguously found |

## Regressions (NEW_FAIL)
| Skill | Status | Root cause | Issue |
|-------|--------|------------|-------|
| changelog | NO_OUTPUT | no_file_match | ISS-002 |
| cost-report | NO_OUTPUT | no_file_match | ISS-008 |
| deep-research | NO_OUTPUT | no_file_match | ISS-014 |
| fork-fleet | NO_OUTPUT | no_file_match | ISS-011 |
| hn-digest | NO_OUTPUT | no_file_match | ISS-015 |
| polymarket | NO_OUTPUT | no_file_match | ISS-017 |
| push-recap | NO_OUTPUT | no_file_match | ISS-010 |
| repo-actions | NO_OUTPUT | no_file_match | ISS-013 |
| repo-article | NO_OUTPUT | no_file_match | ISS-012 |
| repo-pulse | NO_OUTPUT | no_file_match | ISS-009 |
| rss-digest | NO_OUTPUT | no_file_match | ISS-016 |
| swarm-safety-eval | NO_OUTPUT | no_file_match | ISS-005 |
| token-alert | NO_OUTPUT | no_file_match | ISS-018 |

All 13 are `no_file_match` against `articles/`-based output patterns. Root cause: skills appear to write articles ephemerally (not committed to git) or commits are clobbered by snapshot-rebases. `articles/` directory exists with one file (`skill-freshness-2026-08-23.md`, committed today); all other article outputs are absent. No new issues filed — each skill has an existing open ISS.

## Full Results
| Skill | Status | Diff | Root cause | Quality | Words | Last output |
|-------|--------|------|------------|---------|-------|-------------|
| heartbeat | PASS | FIXED | — | unknown | 2000+ | 2026-08-23 (memory/logs/2026-08-23.md) |
| skill-health | PASS | NEW_PASS | — | unknown | 200+ | 2026-08-22 (memory/skill-health/last-report.json) |
| changelog | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| cost-report | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| deep-research | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| fork-fleet | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| hn-digest | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| polymarket | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| push-recap | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| repo-actions | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| repo-article | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| repo-pulse | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| rss-digest | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| swarm-safety-eval | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| token-alert | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |

## Coverage Gaps (enabled in aeon.yml, missing from evals.json)
- batch-health — inferred pattern: `memory/logs/*.md`
- code-health — inferred pattern: `articles/code-health-*.md`
- compute-futures-eda — inferred pattern: `memory/logs/*.md`
- compute-macro-correlate — inferred pattern: `memory/topics/compute-futures-macro-correlations.md`
- compute-pulse — inferred pattern: `memory/logs/*.md`
+30 more — run `./scripts/eval-audit --json` for the full `uncovered_enabled` list (35 total)

## Sources
- evals.json=ok · cron-state=ok · skill-health=ok · eval-audit=ok · prior-article=none (BOOTSTRAP)
