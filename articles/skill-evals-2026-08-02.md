# Skill Evals — 2026-08-02

**Verdict:** SKILL_EVALS_REGRESSED
**Coverage:** 14/49 (28%) (first run)
**Diff:** 14 new fail · 0 fixed · 0 still failing · 0 stable · 1 new pass *(BOOTSTRAP — no prior article)*

> BOOTSTRAP note: No prior `articles/skill-evals-*.md` exists. All results are treated as NEW_*. All 14 failures have pre-existing open issues — no new issues filed this run.

## Action Queue
1. Investigate `heartbeat` — missing_pattern:heartbeat|Heartbeat|HEARTBEAT (ISS-007) — MEMORY flags as same-day false positive; close ISS-007 or add 12:00 UTC grace window to eval
2. Dispatch `changelog` — no output (ISS-002) — enabled (Mon 16:00 UTC), last success 2026-07-27
3. Dispatch `cost-report` — no output (ISS-008) — enabled (Mon 07:00 UTC), last success 2026-07-27
4. Investigate `swarm-safety-eval` — no_file_match despite 5 successful runs (ISS-005) — skill writes to log, not `articles/`; evals.json pattern mismatch
5. Patch evals.json — annotate or remove 10 disabled skills (repo-pulse, push-recap, fork-fleet, repo-article, repo-actions, deep-research, hn-digest, rss-digest, polymarket, token-alert) — NO_OUTPUT is expected while disabled; these entries produce permanent false failures
6. Add evals.json entry for `self-review` — pattern: `articles/self-review-*.md`
7. Add evals.json entry for `vuln-scanner` — pattern: `articles/vuln-scan--*.md`
8. Add evals.json entry for `skill-analytics` — pattern: `articles/skill-analytics-*.md` (+27 more — see Coverage Gaps)

## Regressions (NEW_FAIL)

| Skill | Status | Root cause | Issue |
|-------|--------|------------|-------|
| heartbeat | NEW_FAIL | missing_pattern:heartbeat\|Heartbeat\|HEARTBEAT | ISS-007 |
| changelog | NEW_FAIL | no_file_match | ISS-002 |
| cost-report | NEW_FAIL | no_file_match | ISS-008 |
| swarm-safety-eval | NEW_FAIL | no_file_match | ISS-005 |
| repo-pulse | NEW_FAIL | no_file_match | ISS-009 |
| push-recap | NEW_FAIL | no_file_match | ISS-010 |
| fork-fleet | NEW_FAIL | no_file_match | ISS-011 |
| repo-article | NEW_FAIL | no_file_match | ISS-012 |
| repo-actions | NEW_FAIL | no_file_match | ISS-013 |
| deep-research | NEW_FAIL | no_file_match | ISS-014 |
| hn-digest | NEW_FAIL | no_file_match | ISS-015 |
| rss-digest | NEW_FAIL | no_file_match | ISS-016 |
| polymarket | NEW_FAIL | no_file_match | ISS-017 |
| token-alert | NEW_FAIL | no_file_match | ISS-018 |

*Issues filed this run: none (all pre-existing open issues cover each failure).*

## Full Results

| Skill | Status | Diff | Root cause | Quality | Words | Last output |
|-------|--------|------|------------|---------|-------|-------------|
| heartbeat | FAIL | NEW_FAIL | missing_pattern:heartbeat\|Heartbeat\|HEARTBEAT | unknown | 2354 | 2026-08-02 |
| skill-health | PASS | NEW_PASS | — | unknown | 495 | 2026-08-01 |
| changelog | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| cost-report | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| swarm-safety-eval | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| repo-pulse | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| push-recap | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| fork-fleet | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| repo-article | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| repo-actions | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| deep-research | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| hn-digest | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| rss-digest | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| polymarket | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |
| token-alert | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | — |

**Heartbeat note:** latest log is `memory/logs/2026-08-02.md` (2354 words, no forbidden patterns). Heartbeat's `last_success` was 2026-08-01T08:45:43Z — it did not run on 08-02 before this eval. The pattern miss is a timing artifact, not a quality regression. MEMORY.md calls for closing ISS-007 as a false positive or adding same-day grace.

**Disabled-skill note:** 10 of 14 failing skills are `enabled: false` in `aeon.yml` (repo-pulse, push-recap, fork-fleet, repo-article, repo-actions, deep-research, hn-digest, rss-digest, polymarket, token-alert). Their NO_OUTPUT status is structural, not a runtime failure. These entries should be annotated or removed from `evals.json` to eliminate chronic false-positive signal.

## Coverage Gaps (enabled in aeon.yml, missing from evals.json)

- batch-health — inferred pattern: `memory/logs/*.md`
- self-review — inferred pattern: `articles/self-review-*.md`
- skill-analytics — inferred pattern: `articles/skill-analytics-*.md`
- vuln-scanner — inferred pattern: `articles/vuln-scan--*.md`
- skill-freshness — inferred pattern: `articles/skill-freshness-*.md`
- compute-futures-eda — inferred pattern: `memory/logs/*.md`
- compute-macro-correlate — inferred pattern: `memory/topics/compute-futures-macro-correlations.md`
- planner — inferred pattern: `memory/logs/*.md`
- skill-repair — inferred pattern: `memory/logs/*.md`
- skill-update-check — inferred pattern: `articles/skill-update-check-*.md`

+25 more — see `./scripts/eval-audit --json` for full list (35 uncovered enabled skills total)

## Sources
- evals.json=ok · cron-state=ok · skill-health=ok · eval-audit=ok · prior-article=none (BOOTSTRAP)
