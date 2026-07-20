---
id: snapshot-rebase-clobbers-docs-status-md
created: 2026-07-12
updated: 2026-07-20
type: lesson
links: [[status-md-auto-commit-drops-writes]], [[aeon-skills-dispatch-via-messages-yml]]
---
# Upstream-fork snapshot pulls silently overwrite freshly-landed `docs/status.md` — entrenched 9-day pattern robust to upstream ref rotation

Observed 9 consecutive days 2026-07-12 → 07-20: on-disk file at heartbeat run-start was the pre-regen version despite the prior day's write having landed on main, and `git log -1 --format=%ci -- docs/status.md` pointed at a `snapshot: rsavitt/aeon @ <ref>` commit at ~07:00Z each morning (`bcae68a`, `7dfcc30`, `c0b648a`, `e9e7f22`, `c2ca336`, `f6dd14f`, `d4892f9`, and 07-19/20 both `3d18558` on ref `fa89d8c`). The upstream ref was `a7f04ee` for six days then rotated to `fa89d8c` on 07-18 and stayed there for 07-19 + 07-20 — same clobber outcome regardless of upstream advancement OR stasis, confirming the failure mode is the snapshot merge itself unconditionally rebasing `docs/status.md` in, not stale upstream state. 10 days past 2026-07-16 mitigation urgency threshold. Fix: exclude `docs/status.md` from snapshot merges, or gate the snapshot pull on upstream carrying a `docs/status.md` newer than main's HEAD.
