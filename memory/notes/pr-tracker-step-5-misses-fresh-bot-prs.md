---
id: pr-tracker-step-5-misses-fresh-bot-prs
created: 2026-07-03
type: lesson
links: [[pr-tracker-branch-prefix-misses-bot-identity]], [[aeon-bot-uses-multiple-signing-identities]]
---
# `pr-tracker` step-5 only notifies on merges / stale / closed-no-merge — brand-new bot PRs are invisible to the operator

On 2026-07-03 two brand-new bot PRs (`HKUDS/Vibe-Trading#390` at 2h old, `tamnd/kage#66` at 11h old) landed the same day and neither triggered a notification: SKILL.md step-5 fires notify only for recent merges (7d), stale-open (>7d no activity), or closed-no-merge (7d) — a fresh PR is none of those. The operator's primary signal for "the bot did work today" therefore never fires until the PR ages into staleness or resolves, which for a 2h-old PR means at least 7 days of silence. Durable fix shape: add a fourth trigger ("N ≥ 1 new bot PRs opened in the last 24h") or a daily recap when the open count differs from yesterday's snapshot.
