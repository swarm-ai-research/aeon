## Verdict
WORKFLOW_AUDIT_NEW_CRITICAL — 16 new critical finding(s)

## Summary
- **NEW:** 100 (16 crit / 36 high / 17 med / 31 low)
- **REINTRODUCED:** 0
- **UNCHANGED:** 0
- **RESOLVED:** 0
- **Auto-fixed:** 0
- **Manual review:** 52

This is the **first** workflow-security-audit run for this repo, so every finding is classified as NEW. Per the skill's constraints, the two large classes (`unpinned-uses` and `secrets-outside-env`) are never auto-fixed — both require operator judgment.

## Attack chains worth reading first
1. **`unpinned-uses` ×16** — every `actions/checkout@v4|v5` and `actions/setup-node@v4|v5` resolves at runtime to whatever commit the tag currently points to. With `permissions: contents: write + pull-requests: write` on `aeon.yml`'s primary job, a compromised tag would inherit the full GITHUB_TOKEN plus 30+ `env:`-scoped third-party API secrets (XAI, ANTHROPIC, REPLICATE, FLEET_TOKEN, GH_GLOBAL, etc.). Mitigated today by GitHub's verified-org tier on `actions/*`; pinning would remove that trust assumption.
2. **`secrets-outside-env` ×36** — `messages.yml`'s `run` job loads ~15 secrets (Anthropic, Telegram, Discord, Slack, XAI, CoinGecko, Alchemy) into job-level `env:` rather than gating them behind a deployment environment. Any later-added step in that job, or any compromise of the existing template-injection-prone steps, can read all of them. Worst single-job blast radius in the repo.
3. **`messages.yml` `repository_dispatch` trigger + tojson env routing (fixed)** — the previously-flagged `toJson(github.event.client_payload.message)` → shell pattern is now correctly routed via `_CLIENT_PAYLOAD_MESSAGE` env then `printf '%s' "$_CLIENT_PAYLOAD_MESSAGE" | jq -r '.'`. Hand-rolled check confirms no regression at `messages.yml:659`. Flagging as confirmed-resolved rather than a finding.

## Full report
`articles/workflow-security-audit-2026-06-28.md` — includes per-occurrence tables, attack chains, fix templates, and a machine-readable fingerprint trailer the next run will use for delta classification.

## Source status
zizmor: ok (1.25.2, persona=auditor) · actionlint: ok (1.7.12) · hand-rolled: ok

## Why this PR contains no code changes
The skill explicitly forbids auto-fixing `unpinned-uses`, `persist-credentials`, and `permissions` findings. No script-injection patterns surfaced this run, so there's nothing in the "safe to auto-apply" bucket. The PR ships the report only; remediation requires operator decisions on (a) tag-vs-SHA pinning policy and (b) whether to introduce a GitHub Environment for prod secrets.
