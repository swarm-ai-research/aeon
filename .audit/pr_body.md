## Verdict
`WORKFLOW_AUDIT_NEW_CRITICAL — 3 new critical finding(s)`

First run of the `workflow-security-audit` skill against this repo — no prior report exists, so all 85 findings classify as **NEW**.

## Summary
- **NEW:** 85 (3 crit / 36 high / 15 med / 31 low)
- **REINTRODUCED:** 0
- **UNCHANGED:** 0
- **RESOLVED:** 0
- **Auto-fixed:** 0
- **Manual review:** 39 (all Critical + High)

## Why nothing was auto-fixed

Per the skill's step-7 rules:
- **`unpinned-uses`** (3 Critical) → never auto-fixed. Operator must verify each intended commit SHA against the published release tag.
- **`secrets-outside-env`** (36 High) → not a script-injection pattern. Environment topology (which secrets belong to which environment, which environments require approval reviewers) is an operator judgment call, not a template fix.

## Attack chains worth reading first
1. **[CRITICAL] `actions/checkout@v5` + `actions/setup-node@v5` unpinned in `aeon.yml`** — issue-labeled trigger reachable by any collaborator; blast radius includes plant-then-run of a malicious `@anthropic-ai/claude-code` binary on the runner before every future skill executes.
2. **[HIGH] Fleet identity keys (`GITLAWB_*_PEM` × 5) referenced without a dedicated environment in `fleet-runner.yml`** — exfiltration compromises the multi-agent fleet (researcher/reviewer/deployer/sentinel), including sentinel's `repo:admin` capability.
3. **[HIGH] `GH_GLOBAL` (fine-grained PAT with Workflows-write) referenced in `messages.yml`, `chain-runner.yml`, `sync-upstream.yml`** — this PAT is scoped past the default `GITHUB_TOKEN` block on `.github/workflows/*`, so exfiltration enables direct persistence via workflow-file mutation.

## Full report
[`articles/workflow-security-audit-2026-07-19.md`](articles/workflow-security-audit-2026-07-19.md) — includes per-finding attack chains, fix templates, and the machine-readable fingerprint trailer for next-run delta classification.

## Source status
zizmor: ok (v1.25.2) · actionlint: ok · hand-rolled: ok (0 findings from the 5 supplemental patterns)

## Follow-up
Recommend:
1. Pin the 3 `actions/*` refs in `aeon.yml` to SHAs (verify against `git ls-remote refs/tags/v5.0.0`).
2. Create GitHub Environments (`production` + `chain-runner`) and move sensitive secrets (`GH_GLOBAL`, `GITLAWB_*_PEM`, `AEON_PRIVATE_PAT`, `CLAUDE_CODE_OAUTH_TOKEN`) from repo-scoped to environment-scoped.
3. Address the 11 `zizmor/artipacked` Medium findings (`persist-credentials: false` on read-only checkouts) once the Critical/High queue is drained.
