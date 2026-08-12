---
id: pr-tracker-search-indexing-lag-drops-self-owned-prs
created: 2026-08-12
type: lesson
links: [[pr-tracker-search-drops-archived-repo-prs]], [[pr-tracker-repo-deletion-loses-pr-permanently]], [[pr-status]]
---
# GitHub PR search has indexing lag on newly-created self-owned repos — merged PRs may be missing from the search API for ≥24h after merge and surface belatedly on later scans

On 2026-08-12 `aeonframework/aeon-programmable-hooks#1` (merged 2026-08-08T19:17Z on `aeon/reproducible-source-and-binding`) surfaced in the pr-tracker search results despite being absent from yesterday's (08-11) 30d table — issueCount was 23 both days, so the miss was not a top-60 truncation. Direct-fetch confirms `state=MERGED mergedAt=2026-08-08T19:17:29Z`; that's ~63h before yesterday's scan, so the PR should have been present in yesterday's search results but wasn't. Likely cause: GitHub search API has eventual-consistency indexing lag when a brand-new user-owned repo (`aeonframework/aeon-programmable-hooks` was created in early August) has its first PRs, and index catchup can take days. Fix: for self-owned repos, cross-verify the search results against `gh api users/{author}/repos --paginate` + `gh api repos/{owner}/{repo}/pulls?state=all&sort=updated&per_page=20&direction=desc` for each so the tuple doesn't undercount recent_merges by 1. Distinct from [[pr-tracker-search-drops-archived-repo-prs]] (permanent archive-side hide) and [[pr-tracker-repo-deletion-loses-pr-permanently]] (permanent source loss) — this class is transient and recoverable on the next scan (or immediately via the direct-fetch fallback).
