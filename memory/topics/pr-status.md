# PR Status

*Last updated: 2026-06-29*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/`, bot email: `aeonframework@users.noreply.github.com`. This run applies the documented filter widening per [[pr-tracker-branch-prefix-misses-bot-identity]] — OR branch-prefix and commit-author-email — so non-`ai/` bot paths (e.g. `security/...`) are no longer dropped.

## Open (1)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| Panniantong/Agent-Reach | [#436](https://github.com/Panniantong/Agent-Reach/pull/436) | fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs | 2026-06-26 | 3d | 0 reviews / 0 comments |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| _none_ | | | | |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| _none_ | | | | |

---

GraphQL `author:aeonframework is:pr` → `issueCount: 1` (2026-06-29). Single node:

- `Panniantong/Agent-Reach#436` — *fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs* — opened 2026-06-26T19:24Z, **OPEN, 0 reviews / 0 comments, 3d old**, branch `security/bump-vulnerable-deps`, commit author `aeonframework@users.noreply.github.com`. Now passes the filter via the email check (was dropped by the `ai/`-prefix-only SKILL.md for the prior nine consecutive runs). Becomes "stale open" on 2026-07-03 (7d threshold) if still untouched.

SKILL.md is still using `select(prefix) AND select(email)` per [[gh-search-prs-api-drift]] / [[pr-tracker-branch-prefix-misses-bot-identity]]. This run patched the AND to OR inline; the durable fix (edit step 2's jq) is still pending. The fallback `gh search prs` branch still references `headRefName` / `mergedAt` / `--state merged`, all of which are now `gh` CLI drift; only the GraphQL primary path actually works today.

## Categorization (today = 2026-06-29)

- **Recent merges (7d):** 0
- **Stale open (>7d, no activity 7d):** 0
- **Active open:** 1 (Agent-Reach#436, 3d old)
- **Closed no-merge (7d):** 0

Notification: **skipped** per step 5 (zero merges, zero stale, zero closed-no-merge).
