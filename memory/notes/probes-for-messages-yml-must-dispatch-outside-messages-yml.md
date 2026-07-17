---
id: probes-for-messages-yml-must-dispatch-outside-messages-yml
created: 2026-07-17
type: lesson
links: [[enabled-skills-can-never-dispatch]], [[gha-messages-yml-cron-underdelivery]], [[github-actions-cannot-create-prs]]
---
# A probe for messages.yml cron delivery must not itself be scheduled by messages.yml — the failure mode silences the probe

On 2026-07-16 the planner named `run-frequency-guard` (23:00 UTC) and 05:30 `suggest-edges` `gh pr create` as the two natural-experiment probes for the toggle-vs-PAT question — a 403 on either would prove the Settings toggle is still off. On 2026-07-17 the heartbeat P3 novel-scan showed `run-frequency-guard` still had zero cron-state entries and never fired at 23:00Z per [[enabled-skills-can-never-dispatch]], so the probe was silenced by the very underdelivery it was designed to detect. Durable shape: any diagnostic experiment for `messages.yml` cron delivery (or for anything downstream of that dispatcher) must be triggered by `gh workflow run <name>` or an operator eyeball, never by another skill scheduled in `messages.yml` — otherwise the null result cannot distinguish "no problem" from "same problem, silenced probe".
