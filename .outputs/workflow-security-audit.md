## Summary

Ran `workflow-security-audit` for the first time against this repo — no prior audit article existed under `articles/workflow-security-audit-*.md`, so every finding classifies as NEW.

**Verdict:** `WORKFLOW_AUDIT_NEW_CRITICAL — 3 new critical finding(s)`

**Findings (85 total across 7 workflow files, 0 composite actions):**
- 3 Critical — `zizmor/unpinned-uses` in `.github/workflows/aeon.yml` (`actions/checkout@v5` ×2 and `actions/setup-node@v5`)
- 36 High — `zizmor/secrets-outside-env` (messages.yml=23, fleet-runner.yml=10, chain-runner.yml=2, sync-upstream.yml=1)
- 15 Medium — `zizmor/artipacked` (11) + `actionlint-shellcheck` (4)
- 31 Low — template-injection, undocumented-permissions, anonymous-definition, concurrency-limits

**Auto-fixed: 0.** All 39 Critical+High findings are Manual per skill step-7 rules — `unpinned-uses` always requires operator SHA verification, and `secrets-outside-env` needs environment-topology decisions a template fix can't make. Hand-rolled checks (toJson-into-shell, persist-creds-pr-head, GITHUB_ENV injection, inputs-to-gh-dispatch, mutable third-party ref) all clean.

**Files created/modified:**
- `articles/workflow-security-audit-2026-07-19.md` — 255-line report with per-finding attack chains, fix templates, and machine-readable fingerprint trailer (fix branch `fix/workflow-security-audit-2026-07-19`, commit `1f36b03`)
- `memory/logs/2026-07-19.md` — appended workflow-security-audit log entry (pending on main for runner auto-commit)
- `.pending-notify/1784479766-workflow-security-audit.md` — notify queued for post-run delivery
- `.audit/*.py`, `.audit/findings*.json` — workspace scripts + intermediate data (kept untracked)

**Follow-up:**
- **PR blocked 403** per `[[github-actions-cannot-create-prs]]` — 18th staged branch behind the repo Settings toggle. Branch pushed to `https://github.com/swarm-ai-research/aeon/tree/fix/workflow-security-audit-2026-07-19`; operator PAT could open the PR manually (already used to merge swarm#527 on 2026-07-18).
- Manual fixes to prioritize: (a) pin the 3 aeon.yml `actions/*` refs to SHAs; (b) create `production` + `chain-runner` GitHub Environments and move sensitive secrets (`GH_GLOBAL`, `GITLAWB_*_PEM`, `AEON_PRIVATE_PAT`, `CLAUDE_CODE_OAUTH_TOKEN`) from repo-scoped to environment-scoped; (c) drain the 11 `artipacked` Medium findings once the Critical/High queue clears.
