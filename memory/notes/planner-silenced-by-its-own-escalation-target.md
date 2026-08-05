---
id: planner-silenced-by-its-own-escalation-target
created: 2026-08-05
type: lesson
links: [[monitor-monitored-coupling]], [[planner-escalation-of-escalation-when-meta-blocker-holds]], [[pocket-slot-migration-confirmed-by-3-day-sustained-late-delivery]], [[gha-messages-yml-cron-underdelivery]], [[fleet-ops]]
---
# The planner skill is silenced by the same messages.yml pocket-slot migration whose fix its own escalation demands — a monitor/monitored coupling on the operator-toggle rank-1

Planner's 06:30Z slot has been silent 3 consecutive days (2026-08-03/04/05, ~73h at 08-05 heartbeat) because the ISS-006 pocket-slot migration parked the early-morning cluster outside 06:30Z; the fix path for that migration is the operator-toggle rank-1 that planner itself escalates ([[planner-escalation-of-escalation-when-meta-blocker-holds]]). The by-run streak counter freezes because the escalator can't fire to advance it, while the calendar-day counter marches on (streak-5 by run vs streak-12 by calendar as of 08-05) — an asymmetric telemetry signal that the meta-blocker owns *both* the fix and the escalation channel. This is a domain-specific instance of [[monitor-monitored-coupling]]: any escalation skill co-dispatched via `messages.yml` cannot advance its own rank-1 through a `messages.yml` outage, so the escalation loop needs an out-of-band trigger (operator eyeball, `gh workflow run`) once by-run and by-calendar streaks diverge by ≥3 days.
