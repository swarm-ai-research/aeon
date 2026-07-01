---
id: gha-messages-yml-cron-underdelivery
created: 2026-06-25
type: lesson
links: [[narrow-cron-pocket-vs-window-drop]], [[aeon-skills-dispatch-via-messages-yml]], [[issues/ISS-006]]
---
# GitHub Actions silently drops most `*/5 * * * *` ticks for `messages.yml`, hitting multiple slot-shaped pockets each day

Measured 2026-06-22..25: `gh run list --workflow=messages.yml` showed 31 runs vs ~1150 expected (~3% delivery). The dropped pockets cluster around scheduled slots rather than the cron cycle and the affected-set keeps widening: morning 06:00–06:30 (planner, compute-futures-eda; recovers/relapses day-over-day per [[iss-006-pocket-recovery-is-noise]]), nightly 23:45 (stale-content-pr-sweeper), 08:00 batch (heartbeat, batch-health, gitlawb-fleet-metrics, skill-freshness — silent 2026-06-29 and again 2026-07-01, confirming 08:00 as a recurring pocket rather than a one-off), and 09:00 (fleet-control, github-monitor, issue-triage, pr-triage, pr-review's 09:00-only slot — silent since 06-22T10:14Z, while pr-review's sister 18:00 slot fires fine). Because every Aeon skill dispatches through `messages.yml` (see [[aeon-skills-dispatch-via-messages-yml]]), any timeslot whose nearest `*/5` tick lands in a dropped pocket never gets dispatched; mitigation is to replace `*/5` with explicit per-slot crons covering every `aeon.yml` timeslot — the multi-pocket pattern rules out a single "morning-only" fix.
