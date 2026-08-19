---
id: notify-has-hash-dedup-queue-layer
created: 2026-08-19
type: lesson
links: [[notify-inline-cat-substitution-blocked-in-sandbox]], [[notify-script-has-no-f-flag]], [[pr-tracker-notify-repeats-with-no-state-change]]
---
# `./notify` has a queue-level hash-dedup layer distinct from any SKILL-level dedup

On 2026-08-18 a pr-tracker retry attempt logged `duplicate message (hash 0e6503c1), skipping` when re-writing the same body to `.pending-notify/` — the notify pipeline hashes each queued payload and drops duplicates at dispatch time, separate from any SKILL-level `sent` tuple gate. This layer partially masks the [[pr-tracker-notify-repeats-with-no-state-change]] bug on the operator side (identical bodies never fan out twice per window) but does NOT stop the underlying identical `.pending-notify/` writes or the daily-log churn; the SKILL-level dedup guard still needs to land.
