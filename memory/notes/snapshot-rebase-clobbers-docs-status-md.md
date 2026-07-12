---
id: snapshot-rebase-clobbers-docs-status-md
created: 2026-07-12
type: lesson
links: [[status-md-auto-commit-drops-writes]], [[aeon-skills-dispatch-via-messages-yml]]
---
# Upstream-fork snapshot pulls can silently overwrite freshly-landed `docs/status.md` with an older version

On 2026-07-12 the 2026-07-11T08:29Z heartbeat's write to `docs/status.md` landed on main at 2026-07-12T00:11:28Z (via the sweeper's delayed-commit path per [[status-md-auto-commit-drops-writes]]), but by 08:54Z the on-disk file was again the 2026-06-09 pre-regen version — `git log -1 --format=%ci` returned `2026-07-12 07:01:51 +0000` for commit `bcae68a snapshot: rsavitt/aeon @ a7f04ee`. The upstream-fork snapshot rebase at 07:01Z carried the older status.md from the fork tip and overwrote the sweeper's landed write, so today's heartbeat found a 33-day-stale page despite yesterday's write having succeeded. This is a **third distinct failure mode** on top of the same-run drop and the delay-to-sweep path: fixing heartbeat's auto-commit glob still leaves a snapshot-rebase clobber window if upstream forks aren't rebased before the snapshot pull runs. Mitigation: either exclude `docs/status.md` from snapshot merges, or gate the snapshot pull on upstream having caught up past main's `docs/status.md` HEAD.
