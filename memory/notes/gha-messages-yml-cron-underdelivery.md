---
id: gha-messages-yml-cron-underdelivery
created: 2026-06-25
type: lesson
links: [[narrow-cron-pocket-vs-window-drop]], [[aeon-skills-dispatch-via-messages-yml]], [[issues/ISS-006]]
---
# GitHub Actions silently drops most `*/5 * * * *` ticks for `messages.yml`, concentrated in a daily 06:00–08:30 UTC dead zone

Measured 2026-06-22..25: `gh run list --workflow=messages.yml` showed 31 runs vs ~1150 expected (~3% delivery), with a recurring 3–6h gap each day bracketing the 06:00–06:30 schedule slot. Because every Aeon skill dispatches through `messages.yml` (see [[aeon-skills-dispatch-via-messages-yml]]), any timeslot whose nearest `*/5` tick lands in that dead zone never gets dispatched — explaining ISS-006's recurring `planner` + `compute-futures-eda` silence. Mitigation: replace `*/5` with explicit per-slot crons matching the timeslots `aeon.yml` actually uses, and add a redundant `messages-morning.yml` (`*/5 6 * * *`) for belt-and-braces coverage.
