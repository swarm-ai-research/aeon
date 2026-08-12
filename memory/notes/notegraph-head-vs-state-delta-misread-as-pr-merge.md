---
id: notegraph-head-vs-state-delta-misread-as-pr-merge
created: 2026-08-12
type: lesson
links: [[notegraph-extractor-generatedat-nondeterministic]], [[github-actions-cannot-create-prs]], [[pr-creation-toggle-is-distinct-from-merge-capability]]
---
# Notegraph's HEAD-vs-last-state delta heuristic misattributes reflect's direct commits as PR merges

On 2026-08-12 the notegraph run observed HEAD's stored graph at 260n against last-state 256n and its log entry inferred "#28 merged between the 08-11 and 08-12 runs — first merged-in-window notegraph PR since the [[github-actions-cannot-create-prs]] unblock", but `gh pr view 28` returned `state=OPEN mergedAt=null` — the 4-node HEAD advance was actually the 08-11 reflect skill directly committing regenerated `notegraph.json` (+2 new atomic notes and +2 promoted helper scripts) to main. The skill's heuristic (HEAD graph > last-state graph → attribute to the most recent notegraph PR's merge) is unsound whenever any sibling skill can commit regenerated outputs directly to main, which reflect does on every consolidation pass. Fix: before emitting a merge-status claim to the log, run `gh pr view $PR --json state,mergedAt` and only claim merge on `state=MERGED` — otherwise attribute the HEAD advance to a direct commit and log which commit(s) touched `notegraph.json` in the interval.
