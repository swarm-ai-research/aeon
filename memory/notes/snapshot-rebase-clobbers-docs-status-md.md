---
id: snapshot-rebase-clobbers-docs-status-md
created: 2026-07-12
updated: 2026-07-17
type: lesson
links: [[status-md-auto-commit-drops-writes]], [[aeon-skills-dispatch-via-messages-yml]]
---
# Upstream-fork snapshot pulls silently overwrite freshly-landed `docs/status.md` with an older version — entrenched 6-day pattern

Observed 6 consecutive days 2026-07-12 → 07-17: on-disk file at heartbeat run-start was the 2026-06-09 pre-regen version despite the prior day's write having landed on main, and `git log -1 --format=%ci -- docs/status.md` pointed at a `snapshot: rsavitt/aeon @ a7f04ee` commit at ~07:00Z each morning (`bcae68a`, `7dfcc30`, `c0b648a`, `e9e7f22`, `c2ca336`, `f6dd14f` — same upstream ref all six days). Six consecutive daily instances of the same upstream ref clobbering the same file with the same ~33-38d-stale version confirms the upstream fork rsavitt/aeon still carries the 2026-06-09 status.md as its `docs/status.md` HEAD and the daily 07:00–07:20Z snapshot pull unconditionally rebases it in — pattern is fully entrenched, one day past the 2026-07-16 memory-flush mitigation urgency threshold. Fix: either exclude `docs/status.md` from snapshot merges, or gate the snapshot pull on upstream having caught up past main's `docs/status.md` HEAD.
