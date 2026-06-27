---
id: gha-messages-yml-cron-underdelivery
created: 2026-06-25
type: lesson
links: [[narrow-cron-pocket-vs-window-drop]], [[aeon-skills-dispatch-via-messages-yml]], [[issues/ISS-006]]
---
# GitHub Actions silently drops most `*/5 * * * *` ticks for `messages.yml`, hitting multiple slot-shaped pockets each day

Measured 2026-06-22..25: `gh run list --workflow=messages.yml` showed 31 runs vs ~1150 expected (~3% delivery). The dropped pockets cluster around scheduled slots rather than the cron cycle: morning 06:00–06:30 (planner, compute-futures-eda; 7-day silence broke 2026-06-27 at 07:34Z, 64-min lag), nightly 23:45 (stale-content-pr-sweeper; missed 06-24/25, recovered 06-27T00:19Z), and 09:00 (fleet-control, github-monitor, issue-triage, pr-triage, pr-review's 09:00-only slot — 5 days silent since 06-22T10:14Z, while pr-review's sister 18:00 slot fires fine). Because every Aeon skill dispatches through `messages.yml` (see [[aeon-skills-dispatch-via-messages-yml]]), any timeslot whose nearest `*/5` tick lands in a dropped pocket never gets dispatched; mitigation is to replace `*/5` with explicit per-slot crons covering every `aeon.yml` timeslot — the multi-pocket pattern rules out a single "morning-only" fix.
