# Skill Evals — 2026-07-26

**Verdict:** SKILL_EVALS_REGRESSED
**Coverage:** 14/49 (28%) (first run — BOOTSTRAP)
**Diff:** 13 new fail · 0 fixed · 0 still failing · 0 stable · 2 new pass *(BOOTSTRAP: no prior eval article exists)*

## Action Queue
1. Investigate 13 NO_OUTPUT skills (ISS-002, ISS-005, ISS-008–ISS-018) — root cause: ISS-001 OAuth burn still draining article-output skills; close ISS-001 to unlock batch
2. Add evals.json entry for `skill-freshness` — pattern: `articles/skill-freshness-*.md` [ran today; highest-value gap]
3. Add evals.json entry for `self-review` — pattern: `articles/self-review-*.md`
4. Add evals.json entry for `workflow-security-audit` — pattern: `articles/workflow-security-audit-*.md`
5. Add evals.json entry for `vuln-scanner` — pattern: `articles/vuln-scan--*.md`
6. Add evals.json entry for `skill-analytics` — pattern: `articles/skill-analytics-*.md`
7. Note: ISS-007 (heartbeat: missing_pattern) is candidate for close — heartbeat is NEW_PASS today; next non-BOOTSTRAP run will formally FIXED + close it
8. +30 more coverage gaps — see Coverage Gaps section

## Regressions (NEW_FAIL)

| Skill | Status | Root cause | Issue |
|-------|--------|------------|-------|
| changelog | NO_OUTPUT | no_file_match | ISS-002 (open) |
| swarm-safety-eval | NO_OUTPUT | no_file_match | ISS-005 (open) |
| cost-report | NO_OUTPUT | no_file_match | ISS-008 (open) |
| repo-pulse | NO_OUTPUT | no_file_match | ISS-009 (open) |
| push-recap | NO_OUTPUT | no_file_match | ISS-010 (open) |
| fork-fleet | NO_OUTPUT | no_file_match | ISS-011 (open) |
| repo-article | NO_OUTPUT | no_file_match | ISS-012 (open) |
| repo-actions | NO_OUTPUT | no_file_match | ISS-013 (open) |
| deep-research | NO_OUTPUT | no_file_match | ISS-014 (open) |
| hn-digest | NO_OUTPUT | no_file_match | ISS-015 (open) |
| rss-digest | NO_OUTPUT | no_file_match | ISS-016 (open) |
| polymarket | NO_OUTPUT | no_file_match | ISS-017 (open) |
| token-alert | NO_OUTPUT | no_file_match | ISS-018 (open) |

*All 13 regressions already have open issues — no new ISS filed. All are article-output skills with no file under their output_pattern. Root cause traces to ISS-001 OAuth-burn denominator: zero-token runs prevented article writes from ~2026-06-06 through recovery. swarm-safety-eval is a special case: it ran today (SSE_EMPTY — no ledger in memory/agent-first/) but writes no article file.*

## Full Results

| Skill | Status | Diff | Root cause | Quality | Words | Last output |
|-------|--------|------|------------|---------|-------|-------------|
| heartbeat | PASS | NEW_PASS | — | unknown | 1000+ | memory/logs/2026-07-26.md (today) |
| skill-health | PASS | NEW_PASS | — | unknown | 100+ | memory/skill-health/last-report.json (07-25T18:44Z) |
| changelog | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none found |
| swarm-safety-eval | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none (ran today: SSE_EMPTY) |
| cost-report | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none found |
| repo-pulse | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none found |
| push-recap | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none found |
| fork-fleet | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none found |
| repo-article | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none found |
| repo-actions | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none found |
| deep-research | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none found |
| hn-digest | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none found |
| rss-digest | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none found |
| polymarket | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none found |
| token-alert | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none found |

**Notes:**
- `articles/` directory has exactly 1 file: `skill-freshness-2026-07-26.md` — confirming the near-total article-output collapse
- heartbeat assertions: `min_words=20` ✓ (~1000+), `heartbeat|Heartbeat|HEARTBEAT` ✓ ("## Heartbeat" + "HEARTBEAT_DEGRADED" in log), forbidden patterns absent ✓
- skill-health assertions: `min_words=20` ✓, `classification|healthy_count|critical|degraded` ✓ (all present in JSON), forbidden patterns absent ✓; stale check: ~14h old, schedule daily at 18:00 UTC, 2× = 48h → not stale ✓
- ISS-007 (heartbeat: missing_pattern, detected_by: skill-evals): heartbeat passes today — ISS-007 is candidate for close; BOOTSTRAP mode prevents formal FIXED classification; next run will resolve it

## Coverage Gaps (enabled in aeon.yml, missing from evals.json)

- skill-freshness — inferred pattern: `articles/skill-freshness-*.md` [**just ran today** — highest priority to spec]
- self-review — inferred pattern: `articles/self-review-*.md`
- workflow-security-audit — inferred pattern: `articles/workflow-security-audit-*.md`
- vuln-scanner — inferred pattern: `articles/vuln-scan--*.md`
- skill-analytics — inferred pattern: `articles/skill-analytics-*.md`
- weekly-shiplog — inferred pattern: `articles/weekly-shiplog-*.md`
- fleet-control — inferred pattern: `articles/fleet-status--*.md`
- skill-evals (self) — inferred pattern: `articles/skill-evals-*.md` [this run produces the first entry]
- skill-graph — inferred pattern: `memory/topics/*.md`
- planner — inferred pattern: `memory/logs/*.md`

+25 more uncovered enabled skills — see `./scripts/eval-audit --json` (`uncovered_enabled` array)

## Sources
- evals.json=ok · cron-state=ok · skill-health=ok · eval-audit=ok · prior-article=none (BOOTSTRAP)
