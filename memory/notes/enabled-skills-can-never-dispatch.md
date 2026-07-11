---
id: enabled-skills-can-never-dispatch
created: 2026-07-11
type: lesson
links: [[gha-messages-yml-cron-underdelivery]], [[aeon-skills-dispatch-via-messages-yml]], [[issues/ISS-006]]
---
# A skill can be `enabled: true` with a present SKILL.md and defined schedule yet never dispatch — cron-state.json simply has no entry

Heartbeat's 2026-07-11 P3 novel-missing-entry scan flagged two such skills: `ai-framework-watch` (weekly Mon 08:30, most recent expected 2026-07-06T08:30Z ~120h ago) and `run-frequency-guard` (daily 23:00, most recent expected 2026-07-10T23:00Z ~9.5h ago). Both have SKILL.md files and `enabled: true` in aeon.yml but zero entries in `memory/cron-state.json`; `run-frequency-guard` was present at 100% success in the 2026-06-08 `docs/status.md` snapshot, so its entry was wiped during the OAuth-outage burn and it never re-dispatched. The heartbeat P3 check is the only fleet signal that catches this failure class — skill-health only classifies skills with a cron-state entry, so silent-never-dispatched skills evade every other health signal; investigate root cause per skill (messages.yml matcher, aeon.yml wiring, workflow file references) before assuming ISS-006 tributary.
