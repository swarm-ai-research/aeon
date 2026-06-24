---
id: narrow-cron-pocket-vs-window-drop
created: 2026-06-24
type: lesson
links: [[aeon-skills-dispatch-via-messages-yml]], [[issues/ISS-006]]
---
# A recurring narrow-pocket silence (~30 min) points to a schedule-matcher bug, not a cron-tick drop

If skills scheduled inside a tight window (e.g. only `0 6` and `30 6` UTC) miss for multiple days while adjacent times (`0 5`, `30 5`, `0 8`+) run cleanly, the `messages.yml` `*/5` cron is delivering — the schedule-matcher is dropping that hour-field. Distinguish from [[aeon-skills-dispatch-via-messages-yml]] (window-wide silence = either matcher OR cron drop). Diagnostic: `gh run list --workflow=messages.yml --created=YYYY-MM-DD` and confirm `*/5` ticks landed at the missed times; if yes, inspect hour-field parsing for the dead pocket.
