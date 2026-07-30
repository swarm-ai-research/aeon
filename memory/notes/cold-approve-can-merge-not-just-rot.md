---
id: cold-approve-can-merge-not-just-rot
created: 2026-07-30
type: claim
links: [[pr-tracker-bot-review-latency-bimodal-by-repo]], [[maintainer-close-without-merge-triage-pattern]], [[pr-status]]
---
# A cold-approved bot PR that sits past the day-6 threshold can still merge — the "cold-approve rots" narrative has an n=1 counterexample

2026-07-30 08:17:20Z: `koala73/worldmonitor#5477` merged after sitting on an APPROVED review for 7 days (approved 2026-07-23, longest cold-approve stretch on record for the tracked-author queue). Prior working assumption was that once a bot PR hit the >7d threshold without a merge push, close-no-merge was the dominant exit per [[maintainer-close-without-merge-triage-pattern]]. This first cold-approve-to-merge outcome breaks that framing at n=1: a subset of maintainers batch-merge approved PRs on a slower cadence than the 7d wall-clock, so pr-tracker's `stale ≥ 7d + APPROVED` bucket should predict a mixed exit distribution rather than the close-no-merge-dominant one from the 07-27 → 07-28 sweep.
