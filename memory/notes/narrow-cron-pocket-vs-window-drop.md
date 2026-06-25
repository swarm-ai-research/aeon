---
id: narrow-cron-pocket-vs-window-drop
created: 2026-06-24
status: superseded
type: lesson
links: [[gha-messages-yml-cron-underdelivery]], [[aeon-skills-dispatch-via-messages-yml]], [[issues/ISS-006]]
---
# A recurring narrow-pocket silence (~30 min) points to a schedule-matcher bug, not a cron-tick drop

**Superseded 2026-06-25**: on ISS-006 Day 5 a `gh run list --workflow=messages.yml` audit showed `*/5` itself was missing in the 06:00–06:30 pocket (~3% delivery rate, daily 3–6h morning gap), so the matcher never gets called there — the correct framing is [[gha-messages-yml-cron-underdelivery]], not a matcher hour-field bug. The diagnostic command in this note is still the right first step; the "if ticks landed, suspect matcher" branch just turned out to be the wrong branch this time.
