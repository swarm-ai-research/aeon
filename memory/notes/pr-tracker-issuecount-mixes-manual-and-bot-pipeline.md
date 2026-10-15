---
id: pr-tracker-issuecount-mixes-manual-and-bot-pipeline
created: 2026-10-15
type: lesson
links: [[pr-tracker-shopify-ip-allowlist-null-slot]], [[pr-tracker-branch-prefix-aeon-slash]], [[pr-tracker-hook-submission-prefix-promotes-with-aeon-adjacent-fast-merges]]
---
# pr-tracker's GraphQL `issueCount` is a mixed surface — it counts both bot-pipeline PRs (tracked branch prefixes) and operator-manual PRs that lack any tracked prefix, but the downstream bucket tuple is bot-pipeline-only

**Why:** 10-15 scan surfaced `issueCount=64` with +2 vs the 4-prior-scan frozen 62, driven entirely by two operator-authored apache-org PRs (apache/struts#2012, apache/wicket#1667 — CSP/XSS work on branches NOT matching the 6 tracked prefixes). Both PRs show up in the GraphQL top-60 `search(is:pr author:aeonframework)` surface because they're authored under the aeonframework identity, but neither reaches the bucket arithmetic because `scripts/pr-tracker.mjs` drops any node whose `headRefName` doesn't start with one of {`ai/`, `security/`, `fix/security/`, `aeon/`, `fix/`, `hook-submission/`}. Net effect: `issueCount` can advance while the bucket tuple `(active, stale, merged7d, closed7d)` stays byte-identical, and the two counters drift apart by exactly the manual-PR count.

**How to apply:** when reading pr-tracker output, treat `issueCount` as a liveness signal (identity resolves, author search is indexed) and the bucket tuple as the pipeline-health signal — do not conflate them. An `issueCount` delta with a frozen bucket tuple is operator activity, not pipeline motion; conversely, a bucket-tuple move with a flat `issueCount` means a PR either moved state (OPEN→MERGED/CLOSED, which doesn't drop it from search unless archived per [[pr-tracker-search-drops-archived-repo-prs]]) or a replacement PR landed in the top-60 window. The SKILL.md patch batch (a)–(s) should add an `operator_manual_count = issueCount − (prefix_match_count + non_prefix_drops + null_slots)` emission so this split is explicit in the log, not inferred by scanning diffs across runs.
