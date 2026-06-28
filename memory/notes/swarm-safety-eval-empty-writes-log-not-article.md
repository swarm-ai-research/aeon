---
id: swarm-safety-eval-empty-writes-log-not-article
created: 2026-06-28
type: lesson
links: [[issues/ISS-005]]
---
# `swarm-safety-eval` runs successfully on an empty ledger but writes only to the daily log — not an article

skill-evals 2026-06-28 confirms the skill is dispatching (`cron-state.last_success: 2026-06-28T08:15:47Z`), but its SSE_EMPTY path appends to `memory/logs/${today}.md` instead of producing `articles/swarm-safety-eval-*.md`, so the eval's article-pattern check still reports `no_file_match`. ISS-005 root cause therefore is not "skill not running" (its original framing) but "skill runs but produces no article when `memory/agent-first/` ledger is absent" — fix is to reclassify ISS-005 from `missing-secret-or-cron` to `permanent-limitation` and either add a log-based eval assertion or document NO_OUTPUT as expected when the ledger is missing. Same shape as any skill that is correct-but-quiet — chasing the missing file is wrong, the eval contract needs updating.
