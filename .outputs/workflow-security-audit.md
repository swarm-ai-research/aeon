*Workflow audit — 2026-09-27*
WORKFLOW_AUDIT_NEW_CRITICAL — 3 new critical, 55 new high, 31 med, 64 low. First on-disk delta baseline.
Auto-fixed 0 · Manual 58
Top chain: `actions/checkout@v4.4.0` unpinned at `.github/workflows/aeon.yml:85` (Early checkout) — aeon.yml is externally reachable via `issues` + `workflow_dispatch`, so a repointed tag ⇒ RCE with fleet-wide secret scope (GITHUB_TOKEN + ANTHROPIC_API_KEY + GH_GLOBAL + notify creds).
PR: https://github.com/swarm-ai-research/aeon/pull/85
Report: articles/workflow-security-audit-2026-09-27.md
