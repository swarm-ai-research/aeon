---
id: aeon-skills-dispatch-via-messages-yml
created: 2026-06-23
type: lesson
links: [[monitor-monitored-coupling]], [[issues/ISS-006]]
---
# Every Aeon skill dispatches through `messages.yml` → `aeon.yml`; no per-skill workflow files exist

A morning-batch silence affecting many skills at once therefore cannot be explained by per-skill `gh workflow disable` or per-file schedule drift — there is no per-skill workflow file to drift. The diagnostic implication: when an entire cron window goes silent, look for a `*/5` cron-tick drop or edit on `messages.yml`/`aeon.yml`, not for per-skill auto-disable.
