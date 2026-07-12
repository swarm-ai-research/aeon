## Verdict
WORKFLOW_AUDIT_NEW_CRITICAL — 3 new critical finding(s)

## Summary
- **NEW:** 77 (3 crit / 17 high / 26 med / 31 low)
- **REINTRODUCED:** 0
- **UNCHANGED:** 0
- **RESOLVED:** 0
- **Auto-fixed:** 0
- **Manual review:** 20

All 3 NEW Critical + 17 NEW High land in never-auto-fix categories per SKILL constraints:
- 3× `unpinned-uses` — pinning `actions/checkout@v5` and `actions/setup-node@v5` in `.github/workflows/aeon.yml` needs an operator to verify the intended commit SHA.
- 15× `secrets-outside-env` — moving `secrets.GH_GLOBAL`, `AEON_PRIVATE_PAT`, `ANTHROPIC_API_KEY`, `CLAUDE_CODE_OAUTH_TOKEN`, etc. behind a GitHub deployment environment with required reviewers is a workflow structural change.
- 2× `actionlint/shellcheck` SC2086 on `$ARGS` at `.github/workflows/fleet-runner.yml:294` (step "Run fleet task runner") — the fix is a bash-array refactor (`ARGS=()`, `ARGS+=(--agent "$AGENT")`, `"${ARGS[@]}"`), not the SKILL's env-intermediary template.

## Attack chains worth reading first
1. `unpinned-uses` on `actions/checkout@v5` (aeon.yml:85, "Early checkout") — a future tag/namespace compromise replays into every aeon runner with full-repo GITHUB_TOKEN + passthrough Claude OAuth. Critical.
2. `secrets-outside-env` on `AEON_PRIVATE_PAT` (fleet-runner.yml:354, "Sync state to aeon-private (Phase 1 dual-write)") — the PAT is exposed at job scope with no environment gate; any compromised prior step reads it. High.
3. `shellcheck SC2086` on `$ARGS` (fleet-runner.yml:294, "Run fleet task runner") — `inputs.agent` word-splits into the `node …` invocation. Confined to write-authenticated dispatchers, but a clean audit-trail win. High.

## Notable
- The historic `messages.yml:577` `toJson(github.event.client_payload.message)` pattern is now correctly gated via `_CLIENT_PAYLOAD_MESSAGE` env at `messages.yml:667` — hand-rolled scanner confirms no residual echo-toJson-into-shell instances.
- Prior audit reports on `fix/workflow-security-audit-*` branches were never merged (blocked by the PAT provisioning issue tracked in memory), so this is treated as a fresh baseline (`Delta vs (no prior audit): 77 new`).

## Full report
articles/workflow-security-audit-2026-07-12.md

## Source status
zizmor: ok (v1.25.2, 116 raw results) · actionlint: ok (v1.7.12, 20 raw results) · hand-rolled: ok (0 additional)
