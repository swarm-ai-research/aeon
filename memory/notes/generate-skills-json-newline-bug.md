---
id: generate-skills-json-newline-bug
created: 2026-06-10
type: lesson
links: [[skills-json-count-drift]]
---
# `./generate-skills-json` emits a raw newline when a skill has two schedules

When `aeon.yml` lists two cron lines for the same skill, the generator concatenates them with a literal `\n` inside the JSON string (observed: `"30 6 * * 0\n30 6 * * 0"`). Fix the join before re-running so downstream parsers don't break.
