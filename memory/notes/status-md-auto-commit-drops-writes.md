---
id: status-md-auto-commit-drops-writes
created: 2026-07-05
type: lesson
links: [[aeon-skills-dispatch-via-messages-yml]]
---
# heartbeat rewrites of `docs/status.md` are silently lost by the workflow auto-commit step

On 2026-07-05 heartbeat regenerated `docs/status.md` and observed the on-disk file was still the 2026-06-09 pre-regen version — despite the 2026-07-04 heartbeat log claiming the rewrite happened. The write itself succeeds inside the runner, but the workflow-level auto-commit step is not staging `docs/status.md`, so every heartbeat regen is a no-op at repo level and the status page ages indefinitely. Fix shape: audit the auto-commit `git add` glob in `messages.yml` to confirm `docs/` is included, or make heartbeat commit `docs/status.md` explicitly before returning.
