*Workflow audit — 2026-06-28*
WORKFLOW_AUDIT_NEW_CRITICAL — 16 new critical findings (unpinned-uses across 7 workflows)
Auto-fixed 0 · Manual 52 (16 crit + 36 high)
Top chain: every actions/checkout@v4|v5 + setup-node@v4|v5 reachable to compromised tag owner; aeon.yml job has contents:write + pull-requests:write + 30+ env-scoped API secrets
Branch: https://github.com/swarm-ai-research/aeon/tree/fix/workflow-security-audit-2026-06-28 (default Actions token can't open PR — open via UI or rerun under GH_GLOBAL)
