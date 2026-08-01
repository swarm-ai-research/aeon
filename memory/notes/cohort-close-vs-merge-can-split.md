---
id: cohort-close-vs-merge-can-split
created: 2026-08-01
type: lesson
links: [[cold-approve-can-merge-not-just-rot]], [[maintainer-close-without-merge-triage-pattern]], [[pr-tracker-tuple-predictor-calendar-day-boundary-bug]]
---
# Same-repo cohort PRs at similar age can take opposite trajectories — the "cohort repeats" prior is not evidenced

worldmonitor#5477 (day-7 cold-approve MERGE 07-30) and worldmonitor#5518 (day-8.6 CLOSE-no-merge 08-01) are same-repo peer PRs from the 07-23 tauri cohort, and they took opposite trajectories at nearly the same age. The n=2 same-repo cohort-repeat test — implicit in the "cold-approve can merge" narrative from [[cold-approve-can-merge-not-just-rot]] — **inverted**: the second PR did not repeat the merge. Fix shape for pr-tracker predictor: when a cohort peer transitions, do not assume the next peer follows the same trajectory; keep close-no-merge and merge as independent probability arms until n≥3 same-repo observations.
