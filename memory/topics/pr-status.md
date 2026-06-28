# PR Status

*Last updated: 2026-06-28*

Cross-repo PR queue for this aeon instance. Author: `aeonframework`, branch prefix: `ai/`.

## Open (0)

| Repo | PR | Title | Opened | Age | Activity |
|------|----|-------|--------|-----|----------|
| _none_ | | | | | |

## Recent Merges (last 30d)

| Repo | PR | Title | Opened | Merged |
|------|----|-------|--------|--------|
| _none_ | | | | |

## Closed No-Merge (last 30d)

| Repo | PR | Title | Closed | Notes |
|------|----|-------|--------|-------|
| _none_ | | | | |

---

GraphQL `author:aeonframework is:pr` → `issueCount: 1` (2026-06-28, **eighth consecutive empty day after prefix filter**). The same single real bot-authored PR persists:

- `Panniantong/Agent-Reach#436` — *fix(deps): bump yt-dlp, requests, python-dotenv to patch disclosed CVEs* — opened 2026-06-26T19:24Z, **still OPEN, 0 reviews / 0 comments / 2d old**, branch `security/bump-vulnerable-deps`, commit author `aeonframework@users.noreply.github.com`. Filtered out by SKILL.md step 2 (head branch does not start with `ai/`). Would have rolled into "stale open" on 2026-07-03 (7d threshold) if the filter caught it.

Two options to surface it next run, unchanged from 2026-06-27: (a) set `pr_tracker.branch_prefix:` in `aeon.yml` to a regex/list covering both `ai/` and `security/`; (b) verify by commit-author-email instead of branch prefix (`BOT_EMAIL=aeonframework@users.noreply.github.com`). Option (b) is more robust — branch names drift more than identities.

Note (2026-06-23, still applies): SKILL.md fallback queries reference `headRefName` json field and `--state merged`; the current `gh` CLI rejects both (`headRefName` not in the `gh search prs --json` list; `--state` only accepts `open|closed`, use `--merged` flag; also `mergedAt` is not a json field — use `closedAt` and filter on `state=="MERGED"` instead). Worked around inline via the GraphQL primary; SKILL.md still pending patch ([[gh-search-prs-api-drift]]).
