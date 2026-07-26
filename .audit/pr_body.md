## Verdict
WORKFLOW_AUDIT_NEW_CRITICAL — 3 new critical finding(s) (bootstrap run; no prior audit on main)

## Summary
- **NEW:** 75 (3 crit / 22 high / 18 med / 32 low), 145 total occurrences before dedup by rule×file×step
- **REINTRODUCED:** 0
- **UNCHANGED:** 0
- **RESOLVED:** 0
- **Auto-fixed:** 0 — every Critical/High falls into the Manual-only bucket per the skill's constraint (pinning, permissions, persist-credentials, secrets-outside-env)
- **Manual review:** 25 (3 Critical + 22 High)

## Why zero auto-fixes on NEW_CRITICAL
- The 3 Criticals are `zizmor/unpinned-uses` on `aeon.yml` `actions/checkout@v5` × 2 and `actions/setup-node@v5` × 1 — picking the SHA is a review call, not a mechanical rewrite. `checkout@93cb6efe1820843…` and `setup-node@2028fbc5c25fe9c…` are the current v5 heads at time of writing; please verify before pinning.
- 43 of the 22 unique Highs are `zizmor/secrets-outside-env` — moving `GH_GLOBAL`, `AEON_PRIVATE_PAT`, `CLAUDE_CODE_OAUTH_TOKEN`, `GITLAWB_*_PEM`, and the notification/API token set from repo scope to environment scope requires **creating the `production` and `chain-runner` GitHub Environments in Settings first**. Editing the workflow to add `environment: production` before the env exists silently breaks every skill.
- 9 Highs are `zizmor/ref-version-mismatch` — the SHA is pinned but the tag comment reads `v5`/`v4` without a patch version. Reviewer can approve a hijacked SHA thinking they're approving the vetted release. Fix is a comment-level bump; still needs verification.
- 2 Highs are `actionlint/SC2086` on `fleet-runner.yml:294` inside `Run fleet task runner` — unquoted `$AGENT` (from `inputs.agent`) inside `ARGS="$ARGS --agent $AGENT"`. Argument injection reachable via `workflow_dispatch`; fix is a bash array (`EXTRA_ARGS=()`) plus quoting.

## Attack chains worth reading first
1. `zizmor/unpinned-uses` on `aeon.yml:85/121/133` — every skill run pulls unpinned `actions/checkout@v5` + `actions/setup-node@v5`. A moved tag or maintainer compromise gives an attacker `contents:write` + `pull-requests:write` on this repo, i.e. the ability to self-modify the aeon agent between two runs.
2. `zizmor/secrets-outside-env` × 43 across `messages.yml`, `fleet-runner.yml`, `chain-runner.yml`, `sync-upstream.yml` — every sensitive secret is repo-scoped, no environment gate, no reviewer approval. One compromised action or one malicious `workflow_dispatch` input landing in a bash sink → exfiltration.
3. `actionlint/SC2086` on `fleet-runner.yml:294` — unquoted `$AGENT` from `inputs.agent` reaches `--agent $AGENT` in the fleet task-runner invocation; crafted input `x --secret-leak $(...)` word-splits into extra CLI args.

## Full report
`articles/workflow-security-audit-2026-07-26.md` (997 lines) — attack chains, fix templates, and machine-readable fingerprint trailer for delta classification against future runs.

## Branch note
This is a version-suffixed branch (`fix/workflow-security-audit-2026-07-26`) because the base `fix/workflow-security-audit` still exists on origin from the 2026-06-20 run whose PR never landed (the ≥18-branch queue behind the operator Repo Settings toggle, per `memory/MEMORY.md` line 46). No force-push, no destructive git operations. The 06-20 branch retains its history.

## Source status
zizmor 1.25.2: **ok** · actionlint 1.7.12: **ok** · hand-rolled backstops: **ok** (0 hits — April 11 `messages.yml:577` toJson-into-shell pattern remains fixed)
