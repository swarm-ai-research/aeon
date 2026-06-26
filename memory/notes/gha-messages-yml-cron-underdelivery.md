---
id: gha-messages-yml-cron-underdelivery
created: 2026-06-25
type: lesson
links: [[narrow-cron-pocket-vs-window-drop]], [[aeon-skills-dispatch-via-messages-yml]], [[issues/ISS-006]]
---
# GitHub Actions silently drops most `*/5 * * * *` ticks for `messages.yml`, concentrated in a daily 06:00–08:30 UTC dead zone

Measured 2026-06-22..25: `gh run list --workflow=messages.yml` showed 31 runs vs ~1150 expected (~3% delivery), with the largest gap each day bracketing the 06:00–06:30 schedule slot but additional drops at other times — confirmed 2026-06-26 when `stale-content-pr-sweeper` (`45 23 * * *`) silently missed the 23:45 slot two nights running. Because every Aeon skill dispatches through `messages.yml` (see [[aeon-skills-dispatch-via-messages-yml]]), any timeslot whose nearest `*/5` tick lands in a dropped pocket never gets dispatched — explaining both ISS-006's `planner` + `compute-futures-eda` morning silence and the new 23:45 sweeper miss. Mitigation: replace `*/5` with explicit per-slot crons matching every timeslot `aeon.yml` actually uses (not just the morning), so each scheduled slot gets a dedicated, less-droppable tick.
