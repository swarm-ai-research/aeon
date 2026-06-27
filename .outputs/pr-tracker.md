## Summary

Executed `pr-tracker` per `skills/pr-tracker/SKILL.md`.

**Config resolved:** `AUTHOR=aeonframework` (from memory; aeon.yml unset, env unset, `gh api user` 403'd — GitHub App token has no user scope), `BRANCH_PREFIX=ai/` (default), `BOT_EMAIL=""` (no filter).

**GraphQL result:** 1 PR by `aeonframework` — `Panniantong/Agent-Reach#436` (open, branch `security/bump-vulnerable-deps`, commit author `aeonframework@users.noreply.github.com`). Filtered out by the `ai/` prefix rule.

**Categories:** merged 0 / stale-open 0 / active-open 0 / closed-no-merge 0 → notification **skipped** per SKILL.md step 5.

**New finding worth flagging:** first non-zero raw author count in 7 days, on a `security/` branch — a non-`external-feature` bot path is opening PRs that the prefix filter silently drops. Recorded in `memory/topics/pr-status.md` with a recommendation to switch the filter from branch-prefix to commit-author-email (`BOT_EMAIL=aeonframework@users.noreply.github.com`) on the next SKILL.md patch, alongside the already-pending [[gh-search-prs-api-drift]] fix.

**Files modified:**
- `memory/topics/pr-status.md` — refreshed with today's date and the new `#436` finding
- `memory/logs/2026-06-27.md` — appended `## PR Tracker` block

**Follow-up:** patch `pr-tracker/SKILL.md` to (a) prefer commit-author-email over branch-prefix, and (b) fix the fallback `gh search prs` flags per [[gh-search-prs-api-drift]].
