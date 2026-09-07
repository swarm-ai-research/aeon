---
id: stale-content-pr-sweeper-default-author-filter-closes-zero-prs
created: 2026-09-07
type: lesson
links: [[stale-content-pr-sweeper-tracked-prefix-drift]], [[github-actions-cannot-create-prs]]
---
# `stale-content-pr-sweeper` SKILL.md's hardcoded `ALLOWED_AUTHORS = {"aeonframework"}` closes zero PRs on the current tracked-branch corpus

**Why:** Every notegraph / suggest-edges / compute-macro / skill-graph PR in the aeon-repo queue is authored by `app/github-actions`, not `aeonframework` directly (the aeon bot commits via the Actions token). Four consecutive operator-invocation runs (2026-08-21, 2026-08-24, 2026-08-30, 2026-09-06) confirmed the literal SKILL author filter closes 0 PRs; each run had to be re-executed with a widened `{aeonframework, app/github-actions}` allowlist to close superseded content branches.

**How to apply:** Patch SKILL.md's `ALLOWED_AUTHORS` set to include `app/github-actions` before the next scheduled sweep — pairs with the branch-prefix patch in [[stale-content-pr-sweeper-tracked-prefix-drift]] as the two-part fix needed for the SKILL to close anything without operator override. Without both patches, sweeper is silently a no-op on the class of branches it exists to prune.
