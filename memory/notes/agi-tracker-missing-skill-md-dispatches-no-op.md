---
id: agi-tracker-missing-skill-md-dispatches-no-op
created: 2026-07-20
type: lesson
links: [[enabled-skills-can-never-dispatch]], [[agi-tracker-weekly-skill]], [[iss-006-pocket-recovery-is-noise]]
---
# `agi-tracker` is enabled + dispatches + reports HEALTHY, yet silently produces no output because `skills/agi-tracker/SKILL.md` is missing

Distinct from [[enabled-skills-can-never-dispatch]]: `agi-tracker` (aeon.yml:188, `schedule: "0 13 * * 1"`) has a cron-state entry and skill-health classifies it HEALTHY, but 2026-07-19 config-validator flagged `skills/agi-tracker/SKILL.md` absent — a runner that dispatches but has no instructions to execute silently produces no article. Explains the 2026-07-06 + 2026-07-13 silent Mon 13:00 UTC slots (2-run streak; today 2026-07-20 is the 3rd weekly attempt). Fix: either restore the SKILL.md (last article was 2026-06-29 per [[agi-tracker-weekly-skill]] — likely deleted or never re-added after that run) OR set `enabled: false` in aeon.yml until it exists. HEALTHY-but-empty-output is a new class of failure the health rubric doesn't catch.
