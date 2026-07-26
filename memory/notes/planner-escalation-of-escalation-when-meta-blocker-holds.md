---
id: planner-escalation-of-escalation-when-meta-blocker-holds
created: 2026-07-26
type: lesson
links: [[github-actions-cannot-create-prs]], [[iss-006-pocket-recovery-is-noise]], [[fleet-ops]]
---
# When a streak-3 concrete Aeon-local escalation still can't close because it dies at the same meta-blocker, planner should elevate the meta-blocker itself as new rank-1 rather than thrash on the concrete action

Observed 2026-07-25: streak-3 escalation `enabled: false on aeon.yml:188 for agi-tracker` did not close — the one-line patch is Aeon-local but its branch merge dies at [[github-actions-cannot-create-prs]]. Planner's response was not "escalate to streak-4 with the same rank-1"; it elevated the meta-block (operator Repo Settings toggle / PAT provisioning) from the streak-4 holding slot `verify-repo-settings-toggle-vs-pat` into active rank-1 `elevate-repo-settings-toggle-active`, and folded the agi-tracker one-liner under it. The general pattern: once N concrete escalations all fail at the same choke point, the choke point becomes the real work — thrashing on the concrete action just burns planner slots without advancing state.
