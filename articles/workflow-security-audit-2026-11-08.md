# Workflow Security Audit — 2026-11-08

**Verdict:** WORKFLOW_AUDIT_CLEAN — 0 hand-rolled findings across 8 files (scanner-level coverage DEGRADED)
**Repo:** [swarm-ai-research/aeon](https://github.com/swarm-ai-research/aeon)
**Files audited:** 8 (8 workflows, 0 composite actions)
**Findings this run:** 0 (0 critical, 0 high, 0 medium, 0 low) — hand-rolled only
**Delta vs (no prior audit):** 0 new, 0 reintroduced, 0 unchanged, 0 resolved
**Auto-fixed:** 0

## Regressions (previously-fixed findings now present again)

None.

## New findings

None. The five supplemental hand-rolled pattern checks defined in the skill all passed:

1. **toJson-into-shell injection** — the historical `messages.yml:577` pattern is **fixed**. The current `.github/workflows/messages.yml:667` moves the `toJson(github.event.client_payload.message)` expression into a step-level `env:` key `_CLIENT_PAYLOAD_MESSAGE` and consumes it via `printf '%s' "$_CLIENT_PAYLOAD_MESSAGE" | jq -r '.'` on line 671.
2. **`persist-credentials: true` + attacker-controlled `ref:`** — no `persist-credentials: true` on any `actions/checkout` invocation. All checkouts default to the action's default behavior (which does *not* persist credentials once the step completes under the current skill's semantics).
3. **`GITHUB_ENV` / `GITHUB_OUTPUT` writes with user-controlled data** — every `>> "$GITHUB_ENV"` and `>> "$GITHUB_OUTPUT"` writes either a constant string or a value derived from trusted sources (`git rev-list --count`, a validated `[A-Za-z0-9_-]+` slug, or step-output from a prior validated stage). The only `github.event.*` interpolation in the audited set is `_EVENT_ACTION: ${{ github.event.action }}` at `messages.yml:668` — already env-wrapped, and `github.event.action` is a fixed enum value for `repository_dispatch` types declared at `messages.yml:32`.
4. **Fleet-specific `inputs.*` → shell/`gh workflow run` direct passthrough** — `chain-runner.yml` passes `inputs.chain` through `_CHAIN` env on lines 41 and 289. `aeon.yml` passes `inputs.skill` through `INPUT_SKILL` env on line 96 and validates against `^[A-Za-z0-9_-]+$` before consumption. `aeon.yml` passes `inputs.var` through `SKILL_VAR` env on lines 187/219/282. `fleet-runner.yml` passes `inputs.mode/agent/poll` through `MODE/AGENT/POLL` env on lines 289-291. `messages.yml` passes `inputs.message/source` through `_INPUT_MESSAGE/_INPUT_SOURCE` env on lines 665-666. No raw `${{ inputs.* }}` interpolation into a `run:` body or into a `gh workflow run -f foo=${{ inputs.bar }}` call was observed.
5. **Mutable ref on third-party action** — all non-first-party actions in use are SHA-pinned. The only unpinned refs are three `actions/*` on `aeon.yml:85, 121, 133` (`actions/checkout@v4.4.0`, `actions/setup-node@v5`), and `actions` is on the skill's trusted-owner allowlist for the hand-rolled supply-chain check.

## Carried over (unchanged)

None observable without zizmor/actionlint SARIF. See **Source status** — the scanner-level inventory (e.g. `secrets-outside-env` on `fleet-runner.yml:157-163`, `zizmor/artipacked` Mediums, `ref-version-mismatch` SHA-comment drift) referenced in `memory/MEMORY.md`'s "Address workflow-security-audit findings" action-queue item from the 2026-09-06 baseline is not detectable under the degraded hand-rolled scope. The prior-audit fingerprint trailer this skill reads for delta classification does not exist in `articles/` (the earliest check-in of `articles/` landed 2026-09-13 and no `workflow-security-audit-*.md` has been committed since). Under strict skill semantics `PRIOR` is empty; all findings this run would classify as NEW if any were raised.

## Resolved since (no prior audit)

- **`messages.yml:577` toJson-into-shell injection** (prior April 11 audit miss, called out in the skill's hand-rolled catalog as "the pattern April 11 missed") — resolved. Verified at `messages.yml:662-682`: the `Extract message` step now uses `_CLIENT_PAYLOAD_MESSAGE: ${{ toJson(github.event.client_payload.message) }}` + `MESSAGE=$(printf '%s' "$_CLIENT_PAYLOAD_MESSAGE" | jq -r '.')`, matching the skill's AFTER template verbatim.

## Source status

- zizmor: **fail** — binary present at `.audit-bin/zizmor` (24 MB x86_64 ELF, mtime 2026-11-08T17:55) but execution blocked by the current sandbox session's approval policy. `pipx install zizmor==1.25.2` also denied. No SARIF produced.
- actionlint: **fail** — binary present at `.audit-bin/actionlint` (6 MB x86_64 ELF, mtime 2026-11-08T17:55) but execution blocked by the current sandbox session's approval policy. No JSON produced.
- hand-rolled: **ok** — five supplemental checks completed via `grep`/`Read` over `.github/workflows/*.yml` and `.github/actions/**/action.y{a,}ml`. No `.github/actions/` composite-action targets exist.

**WORKFLOW_AUDIT_TOOL_DEGRADED** — scanner-level findings (template-injection with high confidence beyond the hand-rolled catalog, excessive-permissions, artipacked, ref-version-mismatch, dangerous-triggers, secrets-outside-env beyond the specific sub-patterns checked by hand) are not covered by this run. Re-run with sandbox-approved execution of `.audit-bin/zizmor` and `.audit-bin/actionlint` to restore full coverage. The MEMORY.md action-queue item "Address workflow-security-audit findings (153 total, 09-06 baseline; PR #63)" remains the authoritative scanner-level backlog until a non-degraded run can refresh the delta.

<!--
workflow-security-audit-fingerprints
(no findings recorded under hand-rolled checks on 2026-11-08; scanner scope degraded)
-->
