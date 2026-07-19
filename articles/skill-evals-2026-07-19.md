# Skill Evals — 2026-07-19

**Verdict:** SKILL_EVALS_REGRESSED
**Coverage:** 14/49 (28%) (first run — BOOTSTRAP)
**Diff:** 13 new fail · 0 fixed · 0 still failing · 0 stable · 2 new pass

> **BOOTSTRAP run**: no prior `articles/skill-evals-*.md` found. All statuses are `NEW_*`. The 13 `NEW_FAIL` skills each have an existing open issue — no new issues were filed. The 10 disabled skills fail only because they aren't running; the 3 enabled failures (changelog, cost-report, swarm-safety-eval) are the actionable regressions.

## Action Queue
1. Dispatch changelog — enabled, no output; Mon 16:00 UTC (ISS-002)
2. Dispatch cost-report — enabled, no output; Mon 07:00 UTC (ISS-008)
3. Dispatch swarm-safety-eval — enabled, no output; Sun 07:30 UTC (ISS-005)
4. Investigate heartbeat ISS-007 — pattern `heartbeat` now found in `memory/logs/2026-07-19.md`; close as false positive or add same-day grace per MEMORY.md note
5. Add evals.json entry for batch-health — pattern: `memory/logs/*.md`
6. Add evals.json entry for code-health — pattern: `articles/code-health-*.md`
7. Add evals.json entry for skill-freshness — pattern: `articles/skill-freshness-*.md`
8. Add evals.json entry for self-review — pattern: `articles/self-review-*.md` (+31 more — see Coverage Gaps)

## Regressions (NEW_FAIL)

All 13 failing skills have existing open issues — no new issues filed this run.
10 of 13 are disabled skills with no output. 3 are enabled and need dispatch.

| Skill | Enabled | Status | Root cause | Issue |
|-------|---------|--------|------------|-------|
| changelog | yes | NEW_FAIL | no_file_match | ISS-002 |
| cost-report | yes | NEW_FAIL | no_file_match | ISS-008 |
| swarm-safety-eval | yes | NEW_FAIL | no_file_match | ISS-005 |
| deep-research | no (workflow_dispatch) | NEW_FAIL | no_file_match | ISS-014 |
| fork-fleet | no | NEW_FAIL | no_file_match | ISS-011 |
| hn-digest | no (as hacker-news-digest) | NEW_FAIL | no_file_match | ISS-015 |
| polymarket | no (as monitor-polymarket) | NEW_FAIL | no_file_match | ISS-017 |
| push-recap | no | NEW_FAIL | no_file_match | ISS-010 |
| repo-actions | no | NEW_FAIL | no_file_match | ISS-013 |
| repo-article | no | NEW_FAIL | no_file_match | ISS-012 |
| repo-pulse | no | NEW_FAIL | no_file_match | ISS-009 |
| rss-digest | no | NEW_FAIL | no_file_match | ISS-016 |
| token-alert | no | NEW_FAIL | no_file_match | ISS-018 |

## Full Results

| Skill | Status | Diff | Root cause | Quality | Words | Last output |
|-------|--------|------|------------|---------|-------|-------------|
| changelog | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | never |
| cost-report | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | never |
| deep-research | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | never |
| fork-fleet | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | never |
| heartbeat | PASS | NEW_PASS | — | unknown | >20 | 2026-07-19 (via log) |
| hn-digest | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | never |
| polymarket | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | never |
| push-recap | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | never |
| repo-actions | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | never |
| repo-article | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | never |
| repo-pulse | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | never |
| rss-digest | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | never |
| skill-health | PASS | NEW_PASS | — | unknown | >20 | 2026-07-18 |
| swarm-safety-eval | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | never |
| token-alert | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | never |

### Notes on passing skills

**heartbeat**: `memory/logs/2026-07-19.md` is the most recent log (today's runs write to it before heartbeat's 08:00 UTC slot). The keyword `heartbeat` appears on line 49 within the planner's ranked-priorities section — pattern check passes by the letter of the spec, but ISS-007 was filed because earlier runs found the log file populated by *other* skills before the heartbeat section was written. This is the false-positive race condition described in MEMORY.md. ISS-007 warrants review.

**skill-health**: `memory/skill-health/last-report.json` exists and passed all checks. Last run 2026-07-18T18:40:00Z (within 2× daily cadence). Contains all required patterns (classification, healthy_count, critical, degraded). No forbidden tokens.

### Note on hn-digest

`hn-digest` in `evals.json` does not match any skill in `aeon.yml` (the registered skill is `hacker-news-digest`). The eval-audit script excludes it from the coverage count (it appears in neither covered nor uncovered lists). The entry is still evaluated here against its output pattern; eval-audit coverage shows 14/49, not 15/49.

## Coverage Gaps (enabled in aeon.yml, missing from evals.json)

35 enabled skills have no eval spec. Top 5 by coverage value:

- batch-health — inferred pattern: `memory/logs/*.md`
- code-health — inferred pattern: `articles/code-health-*.md`
- compute-futures-eda — inferred pattern: `memory/logs/*.md`
- compute-macro-correlate — inferred pattern: `memory/topics/compute-futures-macro-correlations.md`
- compute-pulse — inferred pattern: `memory/logs/*.md`

+30 more — run `./scripts/eval-audit --json` for full list with inferred patterns.

## Sources
- evals.json=ok · cron-state=ok · skill-health=ok · eval-audit=ok · prior-article=none (BOOTSTRAP)
