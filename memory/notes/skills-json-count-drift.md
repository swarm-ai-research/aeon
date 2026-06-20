---
id: skills-json-count-drift
created: 2026-06-10
type: lesson
links: [[generate-skills-json-newline-bug]]
---
# Committed `skills.json` lags the skill count on disk

As of 2026-06-10 the committed file listed 161 skills versus 173 directories under `skills/`. Re-run `./generate-skills-json` after fixing [[generate-skills-json-newline-bug]] to close the drift.
