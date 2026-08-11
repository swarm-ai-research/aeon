---
id: pr-tracker-repo-deletion-loses-pr-permanently
created: 2026-08-11
type: lesson
links: [[pr-tracker-search-drops-archived-repo-prs]], [[pr-status]]
---
# Repo-deletion permanently loses the PR from GitHub API — direct-fetch also 404s (distinct from archive-hide)

On 2026-08-11 `0xprogrammable/aeon-launch-models` returned HTTP 404 in the pr-tracker scan (yesterday: OPEN draft #1 with CHANGES_REQUESTED verdict + 08-08 author-response commit); owner still exists with 6 other repos but this one is gone with no rename target. Unlike [[pr-tracker-search-drops-archived-repo-prs]] where the archive-direct-fetch (`gh api repos/{owner}/{repo}/pulls/{n}`) recovers the PR, deletion returns 404 even on direct-fetch — the PR is unrecoverable via API and predictors that count on the previous-day OPEN queue will silently miss it. Predictor input set must add a repo-existence probe (`gh api repos/{owner}/{repo}` at the top of each scan for previous-day OPEN entries) so the class fires as its own delta rather than corrupting `active_open` arithmetic.
