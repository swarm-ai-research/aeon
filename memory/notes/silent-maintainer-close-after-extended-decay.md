---
id: silent-maintainer-close-after-extended-decay
created: 2026-08-30
type: lesson
links: [[pr-tracker-stale-bot-comment-inverts-stale-classification]], [[maintainer-close-without-merge-triage-pattern]], [[stale-bucket-bulk-clear-via-clustered-maintainer-sweep]]
---
# `workweave/router#871` was closed 2026-08-30 01:05Z after 28d open with no stale-bot lineage and no close-comment — new class-first "silent-maintainer-close" distinct from stale-bot terminal step and CLA-block

The PR sat 28d with a single `devin-ai-integration` comment 2026-08-03 as its only activity, then closed silently — no stale-bot marker, no maintainer close comment, no CLA gate. Distinct from [[pr-tracker-stale-bot-comment-inverts-stale-classification]] (which requires a bot terminal-step ~12d cadence) and from CLA-block Sub A (which requires a CLA-assistant bot in the prior comment chain). Predictor consequence: silent-close events are unlabeled in the activity stream and only surface at close-time, so `pr-tracker` cannot predict them from `stateReason`, comment lineage, or bot markers; watch for repeat instances at the 20–30d decay-mark on PRs whose sole prior activity was a triage-bot comment, and consider surfacing "silent >20d decay open" as its own STALE sub-bucket if n>=2.
