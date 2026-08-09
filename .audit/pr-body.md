## Verdict
WORKFLOW_AUDIT_NEW_HIGH — 1 new high-severity finding

## Summary
- **NEW:** 4 (0 crit / 1 high / 0 med / 3 low)
- **REINTRODUCED:** 0
- **UNCHANGED:** 74 (of which 23 matched via fuzzy anchor after step-name drift)
- **RESOLVED:** 1 (`zizmor/template-injection` at `aeon.yml` prior step `line480` — dropped out this scan)
- **Auto-fixed:** 0
- **Manual review:** 4 — all 4 new findings live in the newly-added `.github/workflows/gitlawb-repo-bootstrap.yml` (dispatch-only, `permissions: {}` at top level)

## Attack chains worth reading first
1. **[HIGH] `zizmor/secrets-outside-env` at `gitlawb-repo-bootstrap.yml:80` (`Restore operator identity`)** — `${{ secrets.GITLAWB_OPERATOR_PEM }}` and `${{ secrets.GITLAWB_OPERATOR_UCAN }}` are expanded into the shell body via inline single-quoted `echo`, with no `env:` intermediary and no `environment:`-gated approval on the job. A compromised earlier step (there's currently one: the `gh release download` of the `gl` CLI from `gitlawb/releases`) could exfiltrate the fleet's Ed25519 operator key and UCAN capability envelope. Losing that identity means an attacker can impersonate the fleet against `gitlawb.com` — forge UCAN delegations, create/rename/delete `aeon` on the node, and poison every downstream `aeon-reviewer` / `aeon-sentinel` issue. Full recovery requires re-provisioning the DID.

## Full report
`articles/workflow-security-audit-2026-08-09.md`

## Why 0 auto-fixed
The one High finding is `secrets-outside-env`, whose fix is two-part: (a) mechanical env-indirection edit and (b) creating a GitHub Environment named `gitlawb-bootstrap` with required-reviewer approval. Part (b) requires operator judgment (which reviewers, which timeouts) so per SKILL constraint the audit does not auto-apply. The 3 new Lows (`template-injection` co-located at line 80, plus `anonymous-definition` and `concurrency-limits` at workflow-level) are below the Critical/High auto-fix threshold.

## Source status
zizmor: **ok** (v1.25.2, `.audit-bin/` pin) · actionlint: **ok** (bundled binary) · hand-rolled: **ok** (toJson-into-shell fix pattern still present at `messages.yml:667`; no new inputs.\* in raw shell; no persist-credentials: true; no mutable third-party refs)

## Follow-up context
This is the third consecutive audit surfacing the same 74-finding UNCHANGED wallpaper (3C unpinned-uses on `aeon.yml`, 21H mix of `ref-version-mismatch` and `secrets-outside-env` across the fleet workflows, 8M `artipacked`). Per MEMORY.md pointer #48 those need: (a) SHA-pin the 3 `actions/*` refs on `aeon.yml`, (b) create `production` + `chain-runner` Environments and move sensitive secrets, (c) add `persist-credentials: false` on read-only checkouts. Blocked on `[[github-actions-cannot-create-prs]]` merge path unproven.
