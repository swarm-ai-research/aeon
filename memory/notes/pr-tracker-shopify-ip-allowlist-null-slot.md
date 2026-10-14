---
id: pr-tracker-shopify-ip-allowlist-null-slot
created: 2026-10-14
type: lesson
links: [[pr-tracker-search-drops-archived-repo-prs]], [[pr-tracker-repo-deletion-loses-pr-permanently]], [[gh-search-prs-api-drift]]
---
# pr-tracker GraphQL `search(is:pr author:aeonframework)` returns a null node for a Shopify-authored PR that sits behind an IP allow-list — n=3 scans (10-07, 10-10, 10-14) confirm the slot is persistent, not transient

**Why:** On three consecutive pr-tracker scans the GraphQL `issueCount` returned 62 but the node list contained 60 concrete entries plus 1 null slot plus 1 non-prefix drop; the null slot is byte-identical across all three scans and traces to a Shopify-hosted PR whose metadata is gated by an org IP allow-list that excludes the aeon GitHub App's runner. Unlike [[pr-tracker-search-drops-archived-repo-prs]] (which drops PRs entirely from the result list) and [[pr-tracker-repo-deletion-loses-pr-permanently]] (which 404s the host), the IP-allow-list case keeps the PR *present* in the issueCount but *unresolvable* as a node — so bucket arithmetic (CLOSED/MERGED/OPEN) silently loses one row every scan. At n=3 the pattern is stable enough to promote from a per-scan quirk to a durable gh-search behavior class.

**How to apply:** patch pr-tracker SKILL.md step-N to detect `null` entries in the GraphQL node list, log them as `pr-tracker-null-slot: <issueCount - resolved_count>`, and emit a distinct bucket-count tag so the (CLOSED, OPEN, MERGED, CLOSED_NO_MERGE) tuple downstream of pr-tracker remains invariant even when a null slot is present. Treat the null slot as *not-countable* rather than *missing* — do not re-attempt to resolve it per-scan (the IP allow-list is static policy, not stochastic), but do flag an operator action item when a new null slot appears (indicates either a fresh IP-gated PR or a repo migrating behind one). Pair this with the (a)–(r) pr-tracker batch; this is item (r) and now ready for landing at n=3.
