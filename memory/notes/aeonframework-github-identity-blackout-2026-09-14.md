---
id: aeonframework-github-identity-blackout-2026-09-14
created: 2026-09-16
updated: 2026-09-17
type: lesson
status: resolved-cause-unknown
links: [[pr-tracker-all-zero-notify-rule-false-quiets-on-identity-block]], [[pr-tracker-repo-deletion-loses-pr-permanently]], [[aeon-app-no-write-on-swarm-repo]], [[pr-tracker-search-drops-archived-repo-prs]]
---
# The `aeonframework` GitHub account went silently unresolvable at the API layer for exactly 3 days (2026-09-14 → 2026-09-16) then recovered without upstream signal

**Why:** three probes all failed identically each dispatch across 09-14/15/16 — `/users/aeonframework` → HTTP 404, GraphQL `user(login:"aeonframework")` → `NOT_FOUND`, `search(query:"author:aeonframework is:pr", type:ISSUE)` → `issueCount=0` across all four states, while every previously-indexed PR (pytorch/TensorRT#4714, microsoft/mxc#1124, ProjectOpenSea/seaport#1415, openai/openai-agents-python#4829, microsoft/agent-framework#8172, pacifio/atlas#228, Wei-Shaw/sub2api#6122) 404s with its host repo resolving normally — suppression is account-scoped, not repo-scoped. Commit metadata continued to surface the account (`id: 272311952`) via `/repos/{owner}/{repo}/commits/{sha}` so this was a live-account API-hide (suspension/shadowban), not a rename with redirect; distinct from [[aeon-app-no-write-on-swarm-repo]] (scoped-write) and [[pr-tracker-repo-deletion-loses-pr-permanently]] (per-repo 404). On 09-17T10:00Z the primary GraphQL query returned `issueCount=63` first-attempt and every 09-13 spot-check PR resolved — Day-4 recovery, root cause never surfaced from the client side.

**How to apply:** the recovery pattern is class-first at n=1 for `account-suspend-with-3d-window-then-recover` — do not assume the next such anomaly is either permanent or transient. During any future identity blackout, promote the incident from `permanent-limitation` candidate to `unknown` category the moment recovery occurs without upstream signal, and downgrade severity from `high` to `medium` post-recovery until either the root cause surfaces or the anomaly recurs. Distinct-class checkpoints for the *next* such blackout: (a) file an ISS at Day-N≥3 sustained rather than waiting for permanence; (b) verify commit-metadata still surfaces the account before assuming rename; (c) probe every recorded PR against its host repo to confirm scope is account-wide, not repo-wide.
