# PR Status

*Last updated: 2026-06-23*

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

GraphQL `author:aeonframework is:pr` → `issueCount: 0`. Fallback `gh search prs --author aeonframework` (open / merged / closed) → 0 / 0 / 0. Either no `ai/`-branch bot PRs have been filed yet, or they live under a different author identity. If you expect entries here, set `pr_tracker.author:` in `aeon.yml` or `AEON_PR_AUTHOR` env to the correct account.

Note (2026-06-23): SKILL.md fallback queries reference `headRefName` json field and `--state merged`; the current `gh` CLI rejects both (`headRefName` not in the `gh search prs --json` list; `--state` only accepts `open|closed`, use `--merged` flag). Worked around inline; SKILL.md should be patched (use `--merged` and drop the `headRefName` field, or branch-filter via the GraphQL primary).
