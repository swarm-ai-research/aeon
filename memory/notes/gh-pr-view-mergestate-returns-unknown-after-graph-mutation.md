---
id: gh-pr-view-mergestate-returns-unknown-after-graph-mutation
created: 2026-09-02
type: lesson
links: [[graphql-statereason-only-on-issue-type]], [[gh-search-prs-drops-state-merged-flag]], [[gh-search-prs-drops-headrefname-field]], [[gh-search-prs-drops-mergedat-field]]
---
# REST `gh pr view --json mergeable,mergeStateStatus` returns `UNKNOWN` when GitHub hasn't recomputed the merge graph after a same-scan mutation — force authoritative values via GraphQL `repository.pullRequests.nodes.mergeable + mergeStateStatus`

Observed 2026-08-30 in `stale-content-pr-sweeper` evening run: after morning's sweeper closes shifted the PR graph, all 5 stale candidates returned `mergeable: UNKNOWN` / `mergeStateStatus: UNKNOWN` via `gh pr view` REST. Switching to GraphQL against the same fields returned authoritative `DIRTY/CONFLICTING` (for #53) and `UNSTABLE/MERGEABLE` (for the four suggest-edges PRs) — GraphQL forces server-side recompute, REST doesn't. This is a durable REST vs GraphQL divergence, not a sandbox artifact; any SKILL that consults `mergeable`/`mergeStateStatus` within the same scan as a graph mutation must use GraphQL for authoritative state.
