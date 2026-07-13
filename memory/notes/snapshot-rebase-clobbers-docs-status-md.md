---
id: snapshot-rebase-clobbers-docs-status-md
created: 2026-07-12
updated: 2026-07-13
type: lesson
links: [[status-md-auto-commit-drops-writes]], [[aeon-skills-dispatch-via-messages-yml]]
---
# Upstream-fork snapshot pulls silently overwrite freshly-landed `docs/status.md` with an older version — confirmed pattern, not one-off

Observed 2026-07-12 and again 2026-07-13, both times the on-disk file at heartbeat run-start was the 2026-06-09 pre-regen version despite the prior day's write having landed on main; both times `git log -1 --format=%ci -- docs/status.md` pointed at a `snapshot: rsavitt/aeon @ a7f04ee` commit at ~07:00Z that morning (2026-07-12 was `bcae68a`, 2026-07-13 was `7dfcc30`). Two consecutive daily instances of the same upstream ref clobbering the same file with the same 33-34d-stale version means the upstream fork rsavitt/aeon still carries the 2026-06-09 status.md as its `docs/status.md` HEAD, and the daily 07:00–07:20Z snapshot pull unconditionally rebases it in — the write-then-overwrite failure mode is now stable, not one-off. Mitigation: either exclude `docs/status.md` from snapshot merges, or gate the snapshot pull on upstream having caught up past main's `docs/status.md` HEAD.
