---
id: notify-script-has-no-f-flag
created: 2026-07-05
updated: 2026-07-08
type: lesson
links: [[aeon-skills-dispatch-via-messages-yml]], [[notify-inline-cat-substitution-blocked-in-sandbox]]
---
# The `./notify` script takes the message as `$1` — the documented `-f <file>` flag does not exist

Multiple SKILL.md files (pr-tracker, surplus-pulse, others) document `./notify -f <path>` but the actual script — both the live workspace copy and the workflow-embedded copy at `.github/workflows/aeon.yml:332-461` — takes the message as `$1`, so `./notify -f path.md` writes the literal string `-f` as the message body into `.pending-notify/<ts>.md` and would deliver "-f" to all channels. On 2026-07-04, 2026-07-05, and again on 2026-07-08 pr-tracker, this silently corrupted the queued notify payload. Recovery: **overwrite the bogus `.pending-notify/<ts>.md` in place with the intended body** and do not re-fire `./notify` (a second invocation would queue a duplicate); the post-run `scripts/postprocess-notify.sh` dispatches whatever is on disk at that path. The earlier "re-invoke inline `MSG=$(cat file); ./notify "$MSG"`" recovery is invalidated per [[notify-inline-cat-substitution-blocked-in-sandbox]] — direct file rewrite is the only working path.
