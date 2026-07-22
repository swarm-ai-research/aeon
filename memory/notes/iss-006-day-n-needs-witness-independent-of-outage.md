---
id: iss-006-day-n-needs-witness-independent-of-outage
created: 2026-07-22
type: lesson
links: [[iss-006-pocket-recovery-is-noise]], [[monitor-monitored-coupling]], [[gha-messages-yml-cron-underdelivery]]
---
# ISS-006 Day-N counting requires witnesses that are themselves dispatch-independent — a skill that missed the day cannot testify the day was clean

Observed 2026-07-20 → 07-21 correction: the 07-20 evening reflect confirmed ISS-006 close-clock Day-2 based on the on-disk cron-state showing planner + compute-futures-eda + memory-flush + memory-structural-dedupe timestamps, but compute-futures-eda's own next-day log (07-21) flagged "1-day gap: 07-19 CSV was present but not analyzed on 07-20" — evidence cfe missed 07-20, and cron-state confirmed batch-health + heartbeat last_success 2026-07-19T09:22Z / 09:25Z (both silent 07-20 + 07-21). The 07-20 reflect had used the *outage-class skills themselves* as their own Day-N witnesses, so the confirmation was circular; the real timeline was 07-19 Day-1 → 07-20 GAP → 07-21 Day-1 restart. Fix shape: Day-N advancement must be gated on a witness outside the outage class (operator eyeball, external status pinger, or a skill whose cron-state entry was untouched by the outage) — never on the outage-class skills' own recent-timestamp claims.
