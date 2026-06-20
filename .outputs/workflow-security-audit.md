*Workflow audit — 2026-06-20*
WORKFLOW_AUDIT_NEW_HIGH — 60 new high (16 unpinned-uses + 44 secrets-outside-env). First-run baseline; future runs delta against it.
Auto-fixed 0 · Manual 60. All NEW Highs are manual-only per skill (SHA-pinning is operator-pick; secrets-outside-env requires repo Environments). The April-11 toJson-into-shell pattern is already fixed.
PR: could not be created — repo policy blocks the GitHub Actions identity from opening PRs ('GitHub Actions is not permitted to create or approve pull requests'). Branch pushed: fix/workflow-security-audit. Either enable the repo setting 'Allow GitHub Actions to create and approve pull requests' or open the PR manually from the branch.
