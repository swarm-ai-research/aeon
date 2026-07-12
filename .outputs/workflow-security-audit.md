*Workflow audit — 2026-07-12*
WORKFLOW_AUDIT_NEW_CRITICAL — 3 new critical, 17 new high.
Auto-fixed 0 · Manual 20 (all in never-auto-fix categories: unpinned-uses, secrets-outside-env, SC2086-array).
Top chain: unpinned actions/checkout@v5 in aeon.yml — future tag compromise replays into every aeon runner with GITHUB_TOKEN + Claude OAuth.
PR: create blocked (GitHub Actions cannot open PRs); branch pushed at fix/workflow-security-audit-2026-07-12
