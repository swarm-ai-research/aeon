---
id: stale-content-pr-sweeper-tracked-prefix-drift
created: 2026-08-19
type: lesson
links: [[github-actions-cannot-create-prs]], [[pr-creation-toggle-is-distinct-from-merge-capability]]
---
# `stale-content-pr-sweeper` TRACKED-branch prefixes drift from the actual branch names skills produce

The SKILL's TRACKED prefix list is derived from skill NAMES, but several skills (`compute-macro-correlate` → branch `compute-macro/YYYY-MM-DD`, `skill-graph` → branch `skill-graph/...`) push branches with truncated or aliased prefixes that don't match. A sweep run consequently walks past these branches even when the supersession criterion is satisfied; fix is either (a) add all live short-prefix aliases (`compute-macro`, `skill-graph`, `suggest-edges`, `notegraph`, `aeon-hooks`) to TRACKED, or (b) rename each skill's branch-creation step to produce the full skill-name prefix.
