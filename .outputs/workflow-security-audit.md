*Workflow audit — 2026-09-06*
WORKFLOW_AUDIT_NEW_CRITICAL — 3 crit / 55 high / 31 med / 64 low (first on-disk delta baseline for swarm-ai-research/aeon)
Auto-fixed 0 · Manual 58 (all top-severity items are unpinned-uses / secrets-outside-env / ref-version-mismatch — operator judgment required)
Top chain: aeon.yml:85,121,133 — actions/checkout@v4.4.0 (×2) + actions/setup-node@v5 unpinned on a workflow triggered by any collaborator via workflow_dispatch and any authenticated user via issues.opened
PR: https://github.com/swarm-ai-research/aeon/pull/63
