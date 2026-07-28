---
id: maintainer-close-without-merge-triage-pattern
created: 2026-07-28
type: lesson
links: [[pr-tracker-notify-repeats-with-no-state-change]], [[pr-tracker-step-5-misses-fresh-bot-prs]], [[pr-status]]
---
# For stale dep-bump security PRs, some maintainers close-without-merge as a triage strategy rather than leaving them open indefinitely

2026-07-28 pr-tracker: three PRs flagged stale on 07-25 (Panniantong/Agent-Reach#436 at 31d, openinterpreter/openinterpreter#1810 at 10d, InsForge/InsForge#1742 at 9d) all closed no-merge within 48h of the stale flag (07-26 19:14 → 07-27 13:16). Common shape: dep-bump security PR opened by aeon's bot identity, sat past the 7d stale threshold without maintainer engagement, then closed cold. This means the pr-tracker `stale → closed_no_merge` transition is a real bucket move, not just a wall-clock rolloff — the notify hash-dedup guard from [[pr-tracker-notify-repeats-with-no-state-change]] correctly let this state change through (SEND on 07-28 after four SKIP days on unchanged queue).
