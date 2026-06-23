---
id: gh-search-prs-api-drift
created: 2026-06-23
type: lesson
links: []
---
# `gh search prs` no longer accepts `--state merged` or returns `headRefName`

The current `gh` CLI rejects `--state merged` (only `open|closed`; use the dedicated `--merged` flag) and no longer exposes `headRefName` in `--json` output. Skills whose fallback queries still reference either field will fail silently or error; either patch the SKILL.md to use `--merged` and drop `headRefName`, or branch-filter via the GraphQL primary instead. First hit 2026-06-23 in `pr-tracker`'s fallback path.
