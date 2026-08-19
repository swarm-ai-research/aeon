---
id: notegraph-silent-revert-on-fabricated-merge-claim
created: 2026-08-19
type: lesson
links: [[notegraph-head-vs-state-delta-misread-as-pr-merge]], [[notegraph-workspace-head-diverges-from-origin]], [[notegraph-extractor-generatedat-nondeterministic]]
---
# On a fabricated "PR merged" inference, notegraph's silent-exit path can revert the extractor's fresh graph back to a months-stale HEAD

Distinct from [[notegraph-head-vs-state-delta-misread-as-pr-merge]] (which is about misreading the delta): on 2026-08-16 the notegraph run inferred "PR #32 merged", flipped into the [[notegraph-extractor-generatedat-nondeterministic]] silent-exit path, and reverted the extractor's freshly-produced 280n graph back to HEAD's 121n — destroying ~159 new nodes without a notify. The silent-exit branch treats "graph didn't change vs HEAD" as safe-to-restore, but when HEAD is drifted (`origin/main` still at 121n from 06-25) and the merge inference is fabricated, restoration is silent data destruction; the guard must confirm merge via `gh pr view --json state,mergedAt` returning MERGED before letting silent-exit run.
