---
id: notegraph-workspace-head-diverges-from-origin
created: 2026-08-18
type: lesson
links: [[notegraph-head-baseline-drift-inflates-new-orphans]], [[notegraph-head-vs-state-delta-misread-as-pr-merge]], [[github-actions-cannot-create-prs]], [[pr-creation-toggle-is-distinct-from-merge-capability]]
---
# `git show HEAD:notegraph.json` in a CI snapshot workspace can return staged/committed state, not `origin/main`, producing a false-positive "chain merged" inference

On 2026-08-18 the notegraph run's `git show HEAD:notegraph.json` returned 286n / 2925e — consistent with the local state file — and the log interpreted this as "the ~54-day 121n lockup dissolved, chain evidently merged." But `gh pr view 35` and `gh pr view 36` both returned `state: OPEN, mergedAt: null`, and a follow-up `git show HEAD:notegraph.json` on the persisted snapshot still returned 121n / 856e — i.e., `origin/main` had not changed. The workspace HEAD had transiently included the run's own uncommitted or snapshot-committed `notegraph.json`, making it look identical to state. Fix: the SKILL's HEAD-diff branch must resolve baseline against `origin/main` (or the PR base ref) rather than the ambiguous local `HEAD`, and cross-verify a suspected "chain merged" inference against `gh pr view` before writing the interpretive verdict.
