---
id: gh-search-prs-drops-mergedat-field
created: 2026-06-25
type: lesson
links: [[gh-search-prs-drops-state-merged-flag]], [[gh-search-prs-drops-headrefname-field]]
---
# `gh search prs --json mergedAt` no longer resolves — use `closedAt` and cross-check merged status separately

Confirmed 2026-06-25: `gh search prs --json mergedAt` fails with a field-unknown error; the field is no longer exposed on the search endpoint. Recovery is `--json closedAt` combined with a per-PR merge check (`gh pr view --json mergedAt`) or via GraphQL. `pr-tracker` and similar merged-in-window queries silently under-report when this field is requested in a fallback path.
