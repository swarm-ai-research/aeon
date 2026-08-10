---
id: skill-state-on-blocked-pr-branch-is-lost
created: 2026-07-10
type: lesson
links: [[github-actions-cannot-create-prs]], [[pr-tracker-notify-repeats-with-no-state-change]]
---
# Skills that persist dedup state on their daily branch lose it when the PR is blocked

`suggest-edges` writes `memory/state/suggest-edges.json` (the `applied` set that suppresses previously-proposed edges) alongside the source-note diff on branch `suggest-edges/${date}`. Because [[github-actions-cannot-create-prs]] blocks PR creation, the branch never merges to main and every subsequent run from main starts state-less — validated 2026-07-10 when suggest-edges re-proposed the exact same 3 similarity-1.00 edges from `gitlawb-compute-futures-proofs/2026-06-20.md` that had already been "applied" on 2026-07-07's branch. Re-confirmed 2026-08-08 (#21), 2026-08-09 (#22), 2026-08-10 (aborted mid-skill; would have been #24) — three consecutive daily runs post-unblock all regenerated identical proposals from `2026-06-24.md`, forming a supersession chain that stale-content-pr-sweeper could not compress because of its own author-filter gap per MEMORY.md line 45. Any skill using this branch-write-and-hope-PR-merges pattern for dedup state (suggest-edges, and any future skill that copies the shape) needs either a direct-to-main commit for the state file or an `applied` list stored somewhere the operator's PAT-queue delay can't strand it; secondary defense is a script-level `gh pr list` guard that skips proposals when an open PR on the same source note already exists.
