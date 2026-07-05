# Skill Evals — 2026-07-05

**Verdict:** SKILL_EVALS_REGRESSED
**Coverage:** 14/49 (28%) (first run)
**Diff:** 14 new fail · 0 fixed · 0 still failing · 0 stable

> Bootstrap run — no prior eval article exists, so all results are NEW_*.
> 10 of 14 new fails are disabled skills with no output (expected). 4 new fails are enabled skills.

## Action Queue
1. Investigate heartbeat — missing_pattern:heartbeat|Heartbeat|HEARTBEAT (ISS-007)
2. Dispatch cost-report — no output in 15 days, last success 2026-06-20 (ISS-008)
3. Add evals.json entry for batch-health — pattern: `memory/logs/*.md`
4. Add evals.json entry for code-health — pattern: `articles/code-health-*.md`
5. Add evals.json entry for planner — pattern: `memory/logs/*.md`
6. Add evals.json entry for fleet-control — pattern: `articles/fleet-status--*.md`
7. Add evals.json entry for skill-freshness — pattern: `articles/skill-freshness-*.md`
8. +30 more — see Coverage Gaps

## Regressions (NEW_FAIL)

### Enabled skills (action required)

| Skill | Status | Root cause | Issue |
|-------|--------|------------|-------|
| heartbeat | NEW_FAIL | missing_pattern:heartbeat\|Heartbeat\|HEARTBEAT | ISS-007 |
| changelog | NEW_FAIL | no_file_match | ISS-002 (existing) |
| cost-report | NEW_FAIL | no_file_match | ISS-008 |
| swarm-safety-eval | NEW_FAIL | no_file_match | ISS-005 (existing) |

### Disabled skills (expected — no output by design)

| Skill | Status | Root cause |
|-------|--------|------------|
| repo-pulse | NO_OUTPUT | disabled, no_file_match |
| push-recap | NO_OUTPUT | disabled, no_file_match |
| fork-fleet | NO_OUTPUT | disabled, no_file_match |
| repo-article | NO_OUTPUT | disabled, no_file_match |
| repo-actions | NO_OUTPUT | disabled, no_file_match |
| deep-research | NO_OUTPUT | disabled (workflow_dispatch), no_file_match |
| hn-digest | NO_OUTPUT | disabled, no_file_match |
| rss-digest | NO_OUTPUT | disabled, no_file_match |
| polymarket | NO_OUTPUT | disabled, no_file_match |
| token-alert | NO_OUTPUT | disabled, no_file_match |

## Full Results

| Skill | Status | Diff | Root cause | Quality | Words | Last output |
|-------|--------|------|------------|---------|-------|-------------|
| heartbeat | FAIL | NEW_FAIL | missing_pattern:heartbeat\|Heartbeat\|HEARTBEAT | unknown | 839 | memory/logs/2026-07-05.md |
| repo-pulse | NO_OUTPUT | NEW_FAIL | no_file_match (disabled) | unknown | — | never |
| changelog | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | 2026-06-29 (cron-state) |
| push-recap | NO_OUTPUT | NEW_FAIL | no_file_match (disabled) | unknown | — | never |
| fork-fleet | NO_OUTPUT | NEW_FAIL | no_file_match (disabled) | unknown | — | never |
| cost-report | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | 2026-06-20 (cron-state) |
| repo-article | NO_OUTPUT | NEW_FAIL | no_file_match (disabled) | unknown | — | never |
| repo-actions | NO_OUTPUT | NEW_FAIL | no_file_match (disabled) | unknown | — | never |
| deep-research | NO_OUTPUT | NEW_FAIL | no_file_match (disabled) | unknown | — | never |
| hn-digest | NO_OUTPUT | NEW_FAIL | no_file_match (disabled) | unknown | — | never |
| rss-digest | NO_OUTPUT | NEW_FAIL | no_file_match (disabled) | unknown | — | never |
| polymarket | NO_OUTPUT | NEW_FAIL | no_file_match (disabled) | unknown | — | never |
| token-alert | NO_OUTPUT | NEW_FAIL | no_file_match (disabled) | unknown | — | never |
| skill-health | PASS | NEW_PASS | — | unknown | 338 | memory/skill-health/last-report.json |
| swarm-safety-eval | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | SSE_EMPTY in log (ISS-005) |

### Notes on enabled skill failures

**heartbeat** — Today's `memory/logs/2026-07-05.md` exists (839 words) but contains no heartbeat entry: only planner, stale-content-pr-sweeper, swarm-safety-eval, config-validator, skillpacks, and compute-futures-eda. The 08:00 UTC heartbeat slot is a known cold pocket on odd-DOM days (ISS-006). Prior run confirmed at 2026-07-04T08:54:49Z (`HEARTBEAT_OK` in 2026-07-04 log). Root is ISS-006 cron underdelivery, not a skill logic defect — but the eval must flag it.

**changelog** — No article file produced. Last success in cron-state: 2026-06-29T17:32:55Z. Enabled at Mon 16:00 UTC. Next slot: 2026-07-07. ISS-002 already open.

**cost-report** — No article file produced. Last success: 2026-06-20T06:10:00Z (~15 days ago). Enabled at Mon 07:00 UTC. Two subsequent Monday slots missed. Filed ISS-008. Next scheduled: 2026-07-07 07:00 UTC.

**swarm-safety-eval** — No article file. Today's log shows `SSE_EMPTY` (no agent-first ledger). Per MEMORY.md and ISS-005, this is a permanent-limitation (no output until `memory/agent-first/` ledgers exist). ISS-005 already open.

## Coverage Gaps (enabled in aeon.yml, missing from evals.json)

Top 10 of 35 uncovered enabled skills:

- batch-health — inferred pattern: `memory/logs/*.md`
- code-health — inferred pattern: `articles/code-health-*.md`
- compute-futures-eda — inferred pattern: `memory/logs/*.md`
- compute-macro-correlate — inferred pattern: `memory/topics/compute-futures-macro-correlations.md`
- compute-pulse — inferred pattern: `memory/logs/*.md`
- config-validator — inferred pattern: `memory/logs/*.md`
- fleet-control — inferred pattern: `articles/fleet-status--*.md`
- planner — inferred pattern: `memory/logs/*.md`
- pr-tracker — inferred pattern: `memory/logs/*.md`
- reflect — inferred pattern: `memory/topics/*.md`

+25 more — see `scripts/eval-audit --json` for full list.

## Sources
- evals.json=ok · cron-state=ok · skill-health=ok · eval-audit=ok · prior-article=none (bootstrap)
