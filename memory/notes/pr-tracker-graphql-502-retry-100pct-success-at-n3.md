---
id: pr-tracker-graphql-502-retry-100pct-success-at-n3
created: 2026-10-21
type: lesson
links: [[pr-tracker-shopify-ip-allowlist-null-slot]], [[graphql-statereason-only-on-issue-type]], [[gh-search-prs-api-drift]]
---
# pr-tracker's GraphQL first-attempt HTTP 502 (nginx) is intermittent-but-recurrent, and a single 3s-backoff retry clears it 100% of the time at n=3 observations across a 6-day window

**Why:** First-attempt nginx 502 recurred on 10-15, 10-19, and 10-21 (bracketed by clean 10-17, 10-18, 10-20) — all three cleared on a single 3-second backoff retry with no second-attempt failure or follow-on degradation. The 6-day window hosting 3 observations rejects both the "one-off flake" null (n=1 was the 10-15 reading) and the "endemic outage" null (`issueCount` + Letter bucket tuple + 9 null-slot stderrs are all byte-identical across the clean and 502-first scans), isolating the signal to transient nginx jitter at the GraphQL endpoint rather than client/auth/payload class.

**How to apply:** promote pr-tracker SKILL.md draft item (s) — the 3s-backoff retry wrapper around the GraphQL `search` call — from draft to patch queue; the empirical floor is now n=3-with-100%-retry-success, enough to retire the n=1 "wait for recurrence" gate. Treat first-attempt 502 as expected class, not an incident; log it (count observations for recurrence surveillance) but do not notify unless the retry itself fails (second-attempt 502 would be a new class worth surfacing). Pair with the Shopify null-slot handler [[pr-tracker-shopify-ip-allowlist-null-slot]] in the same patch landing since both are read-path invariants that only surface through the GraphQL arm.
