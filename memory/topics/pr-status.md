# PR Status

*Last updated: 2026-06-25*

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

GraphQL `author:aeonframework is:pr` → `nodes: []` (2026-06-25, **fifth consecutive empty day**). Fallback `gh search prs --author aeonframework --state open` → `[]`; `gh search prs --author aeonframework --merged --json …closedAt…` → `[]`. Either no `ai/`-branch bot PRs have been filed yet, or they live under a different author identity. If you expect entries here, set `pr_tracker.author:` in `aeon.yml` or `AEON_PR_AUTHOR` env to the correct account.

Note (2026-06-23, still applies): SKILL.md fallback queries reference `headRefName` json field and `--state merged`; the current `gh` CLI rejects both (`headRefName` not in the `gh search prs --json` list; `--state` only accepts `open|closed`, use `--merged` flag; also `mergedAt` is not a json field — use `closedAt` and filter on `state=="MERGED"` instead). Worked around inline via the GraphQL primary; SKILL.md still pending patch ([[gh-search-prs-api-drift]]).
