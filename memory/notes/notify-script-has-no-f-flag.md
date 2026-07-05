---
id: notify-script-has-no-f-flag
created: 2026-07-05
type: lesson
links: [[aeon-skills-dispatch-via-messages-yml]]
---
# The `./notify` script takes the message as `$1` — the documented `-f <file>` flag does not exist

Multiple SKILL.md files (pr-tracker, surplus-pulse, others) document `./notify -f <path>` but the actual script — both the live workspace copy and the workflow-embedded copy at `.github/workflows/aeon.yml:332-461` — takes the message as `$1`, so `./notify -f path.md` writes the literal string `-f` as the message body into `.pending-notify/<ts>.md` and would deliver "-f" to all channels. On 2026-07-04 and 2026-07-05 at least two skills (pr-tracker, surplus-pulse) silently corrupted notifications this way; recovery is to overwrite the bogus pending file with a `test-*` name pattern (which the post-run step suppresses) and re-invoke inline: `MSG=$(cat file); ./notify "$MSG"`.
