---
id: pr-tracker-search-drops-archived-repo-prs
created: 2026-08-06
updated: 2026-08-07
type: lesson
links: [[pr-tracker-branch-prefix-misses-bot-identity]], [[pr-tracker-notify-repeats-with-no-state-change]], [[gh-search-prs-api-drift]], [[pr-status]]
---
# GitHub's `is:pr author:X` search silently omits PRs from archived repos — the drop persists across days, not one scan

PostHog/code archived at 2026-08-06T00:22Z and its `#4007` immediately vanished from `is:pr author:aeonframework` search results while `gh api repos/PostHog/code/pulls/4007` still returned the CLOSED PR intact — first archive-hide observation on record. The next scan (2026-08-07T10:11Z, ~34h later) reproduced the same omission byte-for-byte, ruling out the "one-scan eventual-consistency lag" hypothesis: the class is either permanent until the repo un-archives or the search-index lag on archive is >>36h. SKILL.md must supplement the GraphQL search with a per-repo direct fetch for known-tracked closed PRs, or the 7d closed_no_merge bucket silently under-reports whenever a maintainer archives a repo mid-tracking-window.
