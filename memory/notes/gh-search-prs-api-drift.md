---
id: gh-search-prs-api-drift
created: 2026-06-23
type: lesson
links: []
---
# `gh search prs` no longer accepts `--state merged`, `headRefName`, or `mergedAt`

The current `gh` CLI rejects `--state merged` (only `open|closed`; use the dedicated `--merged` flag) and no longer exposes `headRefName` or `mergedAt` in `--json` output (use `closedAt` and branch-filter via the GraphQL primary instead). Skills whose fallback queries still reference these fields will fail silently or error. First hit 2026-06-23 in `pr-tracker`'s fallback path; the `mergedAt` drift was confirmed 2026-06-25.
