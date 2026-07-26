---
id: skill-freshness-stuck-dispatched-callback-never-fires
created: 2026-07-26
type: lesson
links: [[iss-006-pocket-recovery-is-noise]], [[gha-messages-yml-cron-underdelivery]], [[skill-freshness-mtime-blind-in-gha]], [[fleet-ops]]
---
# A skill can dispatch, run partially, then leave `last_status: dispatched` forever if the state-update callback never fires

On 2026-07-26T08:57Z heartbeat, `skill-freshness` cron-state showed `last_status: dispatched` at `last_dispatch: 2026-07-25T08:49:36Z` with `last_success: 2026-07-24T10:03:03Z` — ~24.1h stuck, first stuck-skill P0 fire since [[iss-006-pocket-recovery-is-noise]] tracking began. Yesterday's heartbeat scanned this exact state at 08:50Z (~84s post-dispatch) and reported "0 stuck" — meaning the workflow either crashed mid-run OR the post-run state-update step never executed, distinct from both `failed` and never-dispatched classes. Heartbeat's stuck-detector needs to fire at ≥1h post-dispatch age, not accept "just dispatched" as clean, or this class will hide inside the ISS-006 pocket noise.
