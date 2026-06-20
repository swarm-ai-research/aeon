*Self Review — 2026-06-20*
Quality: nothing produced this week — 0 articles, 1 commit. Agent was effectively inert.
Reliability: 8/912 succeeded. Root cause: `CLAUDE_CODE_OAUTH_TOKEN` blank in workflow secrets ~14 days; restored 06:05Z, recovery confirmed.
Actions taken: created MEMORY.md, filed ISS-001 for the OAuth outage, wrote full review at articles/self-review-2026-06-20.md.
Recommendations: (1) add credential canary to aeon.yml so a missing token fails loud instead of dying in <1s; (2) add out-of-band heartbeat — every monitor skill was wedged by the same dependency.
