---
id: stale-content-pr-sweeper-defect-impact-bounded-by-upstream-backlog
created: 2026-10-29
type: lesson
links: [[stale-content-pr-sweeper-default-author-filter-closes-zero-prs]], [[stale-content-pr-sweeper-tracked-prefix-drift]], [[operator-bulk-close-post-identity-recovery]]
---
# stale-content-pr-sweeper author-allowlist defect is non-impactful when upstream clears the backlog — defect blast radius bounded by candidate pile-up size

**Why:** 10-21 → 10-29 the open-PR queue collapsed 59 → 12 (notegraph/* 16→1, suggest-edges/* 14→0, fix/* 3→1); today's run surfaced 1 TRACKED-prefix candidate (notegraph #107) rejected by `ALLOWED_AUTHORS` filter missing `app/github-actions`, and the counterfactual close-count under the patched config is also 0 because the single-entry group has nothing to supersede. First observed case where the defect's actual output matches its patched-config output — defect was non-impactful today.

**How to apply:** the author-allowlist defect per [[stale-content-pr-sweeper-default-author-filter-closes-zero-prs]] has a bounded harm model: it blocks closes only while candidates exceed per-group `keep_latest`. When upstream sweeps (operator bulk-close per [[operator-bulk-close-post-identity-recovery]] or routine merges) drain the backlog below that threshold, the defect produces identical output to the patched config. Patch urgency is still real — next notegraph/suggest-edges cadence refills the groups and the defect re-engages — but during post-sweep troughs the skill's zero-close line is correct-by-coincidence, not evidence of continued damage.
