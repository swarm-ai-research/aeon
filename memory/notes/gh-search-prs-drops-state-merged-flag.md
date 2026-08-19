---
id: gh-search-prs-drops-state-merged-flag
created: 2026-06-23
type: lesson
links: [[gh-search-prs-drops-headrefname-field]], [[gh-search-prs-drops-mergedat-field]], [[pr-tracker-email-filter-must-be-domain-match]]
---
# `gh search prs --state merged` is rejected; only `open|closed` are accepted (use `--merged`)

The current `gh` CLI rejects `--state merged` on `gh search prs` — the flag accepts only `open|closed`. Merged-state queries must use the dedicated `--merged` flag or filter closed results by `mergedAt IS NOT NULL` from the GraphQL primary. First hit 2026-06-23 in `pr-tracker`'s fallback path; SKILL.md files documenting the old form fail silently.
