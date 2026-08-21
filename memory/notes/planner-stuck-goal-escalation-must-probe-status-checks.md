---
id: planner-stuck-goal-escalation-must-probe-status-checks
created: 2026-08-21
type: lesson
links: [[planner-escalation-of-escalation-when-meta-blocker-holds]], [[pr-creation-toggle-is-distinct-from-merge-capability]], [[github-actions-cannot-create-prs]]
---
# When planner's stuck-goal escalation rule fires, the first probe must be `gh pr view --json statusCheckRollup` on the concrete target, not a rephrase of the goal

Observed 2026-08-21: planner's rank-1 aeon-repo-queue-merge had restated for 4 consecutive days at streak 12 → the SKILL step-1 stuck-goal escalation rule fired, and this run probed `gh pr view 26 --json statusCheckRollup` for the first time, surfacing that PR #26 (dependabot actions/checkout, textbook auto-merge candidate) had **4/5 checks passing plus a single ShellCheck FAILURE** on workflow `Lint` (job `95256043957`, completed 2026-08-17T01:09:55Z, 4d stale). The chronic streak masked a specific tractable unblock the whole time — the failing check has been there since day 10 of the streak but the planner rephrased the generic goal daily without ever probing check status. Rule change: at the first restatement (day 2), planner should already run `gh pr view --json statusCheckRollup,mergeable,mergeStateStatus` on any named PR target and lift a single-check failure into the plan body rather than waiting for day-4 escalation to surface it.
