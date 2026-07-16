---
id: pr-tracker-notify-repeats-with-no-state-change
created: 2026-07-05
updated: 2026-07-16
type: lesson
links: [[pr-tracker-step-5-misses-fresh-bot-prs]], [[pr-tracker-branch-prefix-misses-bot-identity]]
---
# `pr-tracker` step-5 fires an identical notify each day while the PR queue is unchanged

On 2026-07-04 and 2026-07-05 the queue held the same three PRs at identical head SHAs and `updatedAt` timestamps (Agent-Reach#436 stale, Vibe-Trading#390 fresh, kage#66 closed-no-merge), and step-5's `stale ≥ 1 AND closed-no-merge ≥ 1` gate fired an identical notify both days. SKILL.md step-5 has no dedup guard against "same trigger set as last run" — so a persistent stale/closed-no-merge state keeps notifying daily until the wall clock rolls a PR off the 7d window. Durable fix shape: hash the (repo, PR, state, updatedAt) tuples of the notify-triggering set and skip if unchanged since the prior run — validated in-skill 4× (2026-07-09/10/14/15/16) and validated NOT to over-suppress by the 2026-07-11 kage#66 rolloff transition (guard let the legit state change through).
