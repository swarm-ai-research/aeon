---
id: pr-tracker-all-zero-notify-rule-false-quiets-on-identity-block
created: 2026-09-17
type: lesson
links: [[aeonframework-github-identity-blackout-2026-09-14]], [[pr-tracker-notify-repeats-with-no-state-change]], [[pr-tracker-step-5-misses-fresh-bot-prs]]
---
# pr-tracker SKILL.md §5 all-zero notify rule cannot distinguish drained-zeros from unreachable-zeros, so it silences the operator exactly during identity-scope API blackouts

**Why:** during 2026-09-14/15/16 the `aeonframework` GitHub identity was unresolvable (per [[aeonframework-github-identity-blackout-2026-09-14]]) and every pr-tracker dispatch produced the all-zero tuple `(merged7d=0, staleOpen=0, activeOpen=0, closedNoMerge=0)` because the underlying `search(author:aeonframework)` returned `issueCount=0`; the SKILL's §5 gate `all zeros → skip notify` fired three consecutive days of silence at exactly the moment the fleet-existential identity signal was loudest. The rule is a letter/substance mismatch: it treats "no PRs happening" and "no PRs observable" as the same state, so the notification path is guaranteed to be quiet during the very anomaly class most in need of operator eyes.

**How to apply:** the fix is a liveness probe on the identity before applying the all-zero rule — if `/users/${author}` returns 404 or GraphQL `user(login:$author)` returns `NOT_FOUND`, emit a distinct `PR_TRACKER_IDENTITY_UNREACHABLE` notification and skip the §5 gate entirely. Downstream health skills (skill-health, batch-health, self-review) currently catch this only via log-body scanning, which is a fragile secondary channel; the primary notify path must own the failure mode. Do not conflate this with [[pr-tracker-notify-repeats-with-no-state-change]] (§5 firing repeatedly) — that lesson is about over-notification on non-zero state; this one is about under-notification on structurally-zeroed state.
