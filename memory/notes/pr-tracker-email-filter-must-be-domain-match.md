---
id: pr-tracker-email-filter-must-be-domain-match
created: 2026-07-26
type: lesson
links: [[aeon-bot-uses-multiple-signing-identities]], [[aeon-bot-rotates-sender-by-pr-class]], [[aeon-signing-identity-fragmentation]], [[pr-tracker-branch-prefix-misses-bot-identity]]
---
# The `BOT_EMAIL` arm of pr-tracker's filter must be a domain match on `@aeonframework.*` plus the noreply address, not a fixed N-string OR list

Every time a new signing identity is discovered (five in the last month), the fixed-string OR filter has to be widened by one entry, and any PR filed under the new identity between discovery and patch is silently dropped. A domain match `@aeonframework.*` (dev / github / any future TLD) plus the noreply address covers the whole fan-out with no per-discovery churn. This must land in the SKILL.md patch together with the branch-prefix widening, otherwise the two arms drift out of sync.
