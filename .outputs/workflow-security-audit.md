*Workflow audit — 2026-08-09*
WORKFLOW_AUDIT_NEW_HIGH — 1 new high-severity finding.
Auto-fixed 0 · Manual 4.
Top chain: `zizmor/secrets-outside-env` at `.github/workflows/gitlawb-repo-bootstrap.yml:80` — `${{ secrets.GITLAWB_OPERATOR_PEM }}` and `${{ secrets.GITLAWB_OPERATOR_UCAN }}` inlined via single-quoted `echo` in the `Restore operator identity` step, no `env:` intermediary, no `environment:`-gated approval on the dispatch-only bootstrap job. Loss of that Ed25519 key means the fleet identity on gitlawb.com is impersonable across every future `gl` call. Fix (manual): env-indirection + create a `gitlawb-bootstrap` GitHub Environment with required reviewers.
PR: https://github.com/swarm-ai-research/aeon/pull/24

