# Skill Evals — 2026-06-20

**Verdict:** SKILL_EVALS_REGRESSED
**Coverage:** 14/50 (28%) (first run — BOOTSTRAP)
**Diff:** 15 new fail · 0 fixed · 0 still failing · 0 stable

> **BOOTSTRAP:** No prior eval article found. All results are NEW_*. This run establishes the baseline; regressions reflect current state, not a change from a previous passing state.

## Action Queue
1. Investigate heartbeat — missing_pattern:heartbeat|Heartbeat|HEARTBEAT (ISS-001) [log exists today but lacks keyword; skill may not have run or omitted its log line]
2. Dispatch changelog — no output in 7+ days (ISS-002) [enabled Mon; 120 runs, 0 successes]
3. Dispatch cost-report — no output in 7+ days (ISS-003) [enabled Mon; 50 runs, 0 successes]
4. Dispatch skill-health — no output in 7+ days (ISS-004) [enabled daily; 195 runs, 0 successes — blocks quality cross-checks]
5. Dispatch swarm-safety-eval — no output (ISS-005) [enabled Sun; 0 successes]
6. Patch evals.json:hn-digest — rename key to `hacker-news-digest` (skill name mismatch; also update output_pattern if needed)
7. Add evals.json entry for code-health — pattern: `articles/code-health-*.md`
8. Add evals.json entry for reflect — pattern: `memory/topics/*.md` (+34 more uncovered enabled — see Coverage Gaps)

## Regressions (NEW_FAIL)

### Enabled skills (actionable)
| Skill | Status | Root cause | Issue |
|-------|--------|------------|-------|
| heartbeat | FAIL | missing_pattern:heartbeat\|Heartbeat\|HEARTBEAT | ISS-001 |
| changelog | NO_OUTPUT | no_file_match | ISS-002 |
| cost-report | NO_OUTPUT | no_file_match | ISS-003 |
| skill-health | NO_OUTPUT | no_file_match | ISS-004 |
| swarm-safety-eval | NO_OUTPUT | no_file_match | ISS-005 |

### Disabled skills (no output expected — no issues filed)
| Skill | Status | Root cause | Note |
|-------|--------|------------|------|
| repo-pulse | NO_OUTPUT | no_file_match | disabled in aeon.yml |
| push-recap | NO_OUTPUT | no_file_match | disabled in aeon.yml |
| fork-fleet | NO_OUTPUT | no_file_match | disabled in aeon.yml |
| repo-article | NO_OUTPUT | no_file_match | disabled in aeon.yml |
| repo-actions | NO_OUTPUT | no_file_match | disabled in aeon.yml |
| deep-research | NO_OUTPUT | no_file_match | disabled (workflow_dispatch only) |
| hn-digest | NO_OUTPUT | no_file_match | key mismatch — aeon.yml uses `hacker-news-digest` |
| rss-digest | NO_OUTPUT | no_file_match | disabled in aeon.yml |
| polymarket | NO_OUTPUT | no_file_match | key mismatch — aeon.yml uses `monitor-polymarket` |
| token-alert | NO_OUTPUT | no_file_match | disabled in aeon.yml |

## Full Results
| Skill | Status | Diff | Root cause | Quality | Words | Last output | Enabled |
|-------|--------|------|------------|---------|-------|-------------|---------|
| heartbeat | FAIL | NEW_FAIL | missing_pattern:heartbeat\|... | unknown | ~65 | 2026-06-20.md | yes |
| repo-pulse | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none | no |
| changelog | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none | yes |
| push-recap | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none | no |
| fork-fleet | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none | no |
| cost-report | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none | yes |
| repo-article | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none | no |
| repo-actions | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none | no |
| deep-research | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none | no |
| hn-digest | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none | no* |
| rss-digest | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none | no |
| polymarket | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none | no* |
| token-alert | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none | no |
| skill-health | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none | yes |
| swarm-safety-eval | NO_OUTPUT | NEW_FAIL | no_file_match | unknown | — | none | yes |

\* evals.json key does not match the skill name in aeon.yml

## Systemic Note

`memory/cron-state.json` shows **every skill at 0% success rate** (except janitor and memory-structural-dedupe which each have 1–2 lifetime successes). All error entries record 0 input tokens and 0 output tokens, indicating the Claude Code execution step is not running — the workflow is failing before Claude is invoked. The 5 enabled-skill NEW_FAILs above are symptoms of this upstream breakage; fixing the root workflow issue will likely resolve them all.

## Coverage Gaps (enabled in aeon.yml, missing from evals.json)
Top 5 by inferrability:
- code-health — inferred pattern: `articles/code-health-*.md`
- self-review — inferred pattern: `articles/self-review-*.md`
- skill-analytics — inferred pattern: `articles/skill-analytics-*.md`
- skill-freshness — inferred pattern: `articles/skill-freshness-*.md`
- reflect — inferred pattern: `memory/topics/*.md`

+31 more — run `./scripts/eval-audit --json` for full uncovered_enabled list.

## Sources
- evals.json=ok · cron-state=ok · skill-health=empty (no last-report.json) · eval-audit=ok · prior-article=none (BOOTSTRAP)
