# Workflow Security Audit — 2026-08-09

**Verdict:** WORKFLOW_AUDIT_NEW_HIGH — 1 new high-severity finding(s)
**Repo:** [swarm-ai-research/aeon](https://github.com/swarm-ai-research/aeon)
**Files audited:** 8 (8 workflows, 0 composite actions)
**Findings this run:** 78 (3 critical, 22 high, 9 medium, 44 low)
**Delta vs 2026-07-26:** 4 new, 0 reintroduced, 74 unchanged (of which 23 matched via fuzzy anchor), 1 resolved
**Auto-fixed:** 0

## Regressions (previously-fixed findings now present again)

_None — no fingerprint from the prior audit was marked `auto-fixed` or `resolved`, so no regressions to report._

## New findings

4 new finding(s) surfaced this run, all in the newly-added workflow `gitlawb-repo-bootstrap.yml` (introduced since the 2026-07-26 audit). The workflow is dispatch-only (`workflow_dispatch` with `permissions: {}` at the top level), which bounds the blast radius — but the one **High** finding (private-key secret in inline shell) deserves a proper environment gate before it accumulates operator use.

### [HIGH] zizmor/secrets-outside-env — secret written to disk via inline template interpolation
**File:** `.github/workflows/gitlawb-repo-bootstrap.yml` · **Step:** `Restore operator identity` · **Line:** 80
**Pattern:**
```yaml
- name: Restore operator identity
  run: |
    set -euo pipefail
    if [ -z '${{ secrets.GITLAWB_OPERATOR_PEM }}' ]; then
      echo "::error::GITLAWB_OPERATOR_PEM is not set — nothing to create the repo as"
      exit 1
    fi
    mkdir -p ~/.gitlawb
    echo '${{ secrets.GITLAWB_OPERATOR_PEM }}' > ~/.gitlawb/identity.pem
    echo '${{ secrets.GITLAWB_OPERATOR_UCAN }}' > ~/.gitlawb/ucan.json
    chmod 600 ~/.gitlawb/identity.pem
```

**Attack chain:**
1. **Entry:** `workflow_dispatch` — reachable by any user with `actions: write` on this repo (currently: the operator and the aeon GitHub App).
2. **Vector:** `${{ secrets.GITLAWB_OPERATOR_PEM }}` is expanded by the runner **before** shell execution and pasted into the script body. A single-quoted heredoc protects against shell metachar interpretation for well-formed PEM content, but the secret ends up as a literal in the rendered step body — visible in job debug logs (`ACTIONS_STEP_DEBUG=true`), and captured by any earlier step that reads `/proc/self/status` or intercepts the runner’s temp files.
3. **Sink:** Written to `~/.gitlawb/identity.pem` and `~/.gitlawb/ucan.json` inside a `run:` block whose environment includes no `env:` intermediary — the more-common runner-log leak path (typical of `secrets-outside-env` rule).
4. **Reachable secrets:** `GITLAWB_OPERATOR_PEM` (Ed25519 private key that owns the aeon repo on the GitLawb node), `GITLAWB_OPERATOR_UCAN` (delegated-auth capability envelope).
5. **Blast radius:** An attacker with the operator key can create/rename/delete the aeon repo on gitlawb.com under the current DID, forge UCAN delegations, and impersonate the fleet identity across every future `gl` call — including issue creation for `aeon-reviewer` and `aeon-sentinel` reports (which are the fleet's primary integrity signal). Fully re-provisioning the operator identity requires generating a new DID and re-associating every downstream repo.

**Fix:**
```yaml
# BEFORE
- name: Restore operator identity
  run: |
    set -euo pipefail
    if [ -z '${{ secrets.GITLAWB_OPERATOR_PEM }}' ]; then
      echo "::error::GITLAWB_OPERATOR_PEM is not set — nothing to create the repo as"
      exit 1
    fi
    mkdir -p ~/.gitlawb
    echo '${{ secrets.GITLAWB_OPERATOR_PEM }}' > ~/.gitlawb/identity.pem
    echo '${{ secrets.GITLAWB_OPERATOR_UCAN }}' > ~/.gitlawb/ucan.json
    chmod 600 ~/.gitlawb/identity.pem

# AFTER — env-indirection + `environment:` gate for approval-required use
jobs:
  bootstrap:
    environment: gitlawb-bootstrap  # create in Repo Settings → Environments; require operator approval
    ...
    steps:
      - name: Restore operator identity
        env:
          _PEM: ${{ secrets.GITLAWB_OPERATOR_PEM }}
          _UCAN: ${{ secrets.GITLAWB_OPERATOR_UCAN }}
        run: |
          set -euo pipefail
          if [ -z "$_PEM" ]; then
            echo "::error::GITLAWB_OPERATOR_PEM is not set — nothing to create the repo as"
            exit 1
          fi
          mkdir -p ~/.gitlawb
          printf '%s' "$_PEM" > ~/.gitlawb/identity.pem
          printf '%s' "$_UCAN" > ~/.gitlawb/ucan.json
          chmod 600 ~/.gitlawb/identity.pem
```

**Status:** Manual required — the fix combines an `env:`-indirection edit (mechanical) with creating a GitHub Environment named `gitlawb-bootstrap` and adding an operator-approval requirement (Repo Settings → Environments → New environment → Required reviewers). Per SKILL constraint, environment-scoping decisions are operator-only, so this audit does not auto-apply the edit.

---

### Low / Medium new findings (compact)

| Severity | Rule | File | Line | Step | Status |
|---|---|---|---|---|---|
| Low | `zizmor/template-injection` | `gitlawb-repo-bootstrap.yml` | 80 | Restore operator identity | Manual (Low; not in auto-fix scope) |
| Low | `zizmor/anonymous-definition` | `gitlawb-repo-bootstrap.yml` | 39 | (job/workflow level) | Manual (Low; not in auto-fix scope) |
| Low | `zizmor/concurrency-limits` | `gitlawb-repo-bootstrap.yml` | 20 | (job/workflow level) | Manual (Low; not in auto-fix scope) |

## Carried over (unchanged)

74 finding(s) carried over from 2026-07-26 unchanged. Of these, 23 matched via fuzzy anchor (rule+file pair, same class, different step-name after upstream refactor). Aggregated by rule:

| Severity | Rule | Count | Files |
|---|---|---|---|
| Critical | `zizmor/unpinned-uses` | 3 | aeon.yml |
| High | `zizmor/ref-version-mismatch` | 6 | chain-runner.yml, fleet-runner.yml, lint.yml, messages.yml, sync-aeon-public-results.yml, sync-upstream.yml |
| High | `zizmor/secrets-outside-env` | 15 | chain-runner.yml, fleet-runner.yml, messages.yml, sync-upstream.yml |
| Medium | `actionlint/SC2086` | 1 | fleet-runner.yml |
| Medium | `zizmor/artipacked` | 8 | aeon.yml, chain-runner.yml, fleet-runner.yml, lint.yml, messages.yml, sync-aeon-public-results.yml, sync-upstream.yml |
| Low | `actionlint/SC2034` | 2 | chain-runner.yml, messages.yml |
| Low | `actionlint/SC2129` | 6 | aeon.yml, chain-runner.yml, messages.yml |
| Low | `actionlint/SC2155` | 2 | chain-runner.yml, fleet-runner.yml |
| Low | `zizmor/anonymous-definition` | 7 | aeon.yml, chain-runner.yml, fleet-runner.yml, messages.yml, sync-aeon-public-results.yml, sync-upstream.yml |
| Low | `zizmor/concurrency-limits` | 1 | fleet-runner.yml |
| Low | `zizmor/template-injection` | 18 | aeon.yml, fleet-runner.yml, messages.yml, sync-upstream.yml |
| Low | `zizmor/undocumented-permissions` | 5 | aeon.yml, chain-runner.yml, fleet-runner.yml, messages.yml, sync-upstream.yml |

## Resolved since 2026-07-26

- [Low] `zizmor/template-injection` in `.github/workflows/aeon.yml` (prior step: `line480`) — no longer present.

The single resolved finding is a template-injection anchor at `aeon.yml` step `line480`. Given that no NEW template-injection appeared in `aeon.yml`, this appears to be a genuine resolution (the interpolation site was cleaned up during an unrelated refactor).

## Source status

- zizmor: **ok** — pinned `1.25.2` binary from `.audit-bin/`; scanned 8 workflows under `.github/workflows/` with `--persona auditor --format sarif`; 133 raw results before rule×file×step dedup.
- actionlint: **ok** — bundled binary from `.audit-bin/`; 20 shellcheck findings (1 escalated to Medium via `SC2086`, rest Low style-class).
- hand-rolled: **ok** — toJson-into-shell (fix pattern present at `messages.yml:667`), `persist-credentials: true` (0 explicit), `GITHUB_ENV`/`GITHUB_OUTPUT` writes with `${{ github.event.* }}` (0), fleet-specific `${{ inputs.* }}` in raw shell (0 — all env-guarded), mutable third-party ref (0 — every `uses:` is `actions/*` first-party). No new hand-rolled backstops fired.

<!--
workflow-security-audit-fingerprints
a001d09f6dce severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/gitlawb-repo-bootstrap.yml step=Restore_operator_identity
5990eb101b1e severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/gitlawb-repo-bootstrap.yml step=Restore_operator_identity
3f73d5880a40 severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/gitlawb-repo-bootstrap.yml step=(unknown)
9d01e01f8dab severity=Low status=manual rule=zizmor/concurrency-limits file=.github/workflows/gitlawb-repo-bootstrap.yml step=(unknown)
9fb519eb4fdb severity=Critical status=manual rule=zizmor/unpinned-uses file=.github/workflows/aeon.yml step=Early_checkout
7491c14fbe74 severity=Critical status=manual rule=zizmor/unpinned-uses file=.github/workflows/aeon.yml step=Checkout_repo
920a2c40af77 severity=Critical status=manual rule=zizmor/unpinned-uses file=.github/workflows/aeon.yml step=Setup_Node.js
92de995e00e5 severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/chain-runner.yml step=Checkout_repo
cfad683f1a80 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/chain-runner.yml step=Checkout_repo
92be19585492 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/chain-runner.yml step=Run_chain
bde515abcfd3 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/chain-runner.yml step=Update_cron_state
07c66694806a severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/chain-runner.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
d5fac004ec2a severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/fleet-runner.yml step=Checkout
8970a9ecf814 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=Restore_fleet_identities
492f5627d723 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=Prefetch_live_Surplus_prices_(best-effort,_outside_sandbox)
9e568b8ce48d severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=Run_fleet_task_runner
6a78074b9b49 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
e04aa697aeac severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/lint.yml step=Checkout
43037ab85149 severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/messages.yml step=Checkout_repo
e619ae84091a severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=Checkout_repo
eb3f904202e5 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=Determine_and_dispatch_scheduled_skills
d07b94573673 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=Collect_and_dispatch_messages
9cff378b979c severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
b38245804892 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=Run
f77041a532da severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/sync-aeon-public-results.yml step=Checkout_aeon
63faf96ee9e4 severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/sync-upstream.yml step=Checkout_fork
7b4cecdf97db severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/sync-upstream.yml step=Checkout_fork
8ea38df05599 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/sync-upstream.yml step=Open_or_update_PR
d42af71c10f4 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/aeon.yml step=Early_checkout
0c66d5f673cf severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/aeon.yml step=Checkout_repo
d2fc7a994dfa severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/chain-runner.yml step=Checkout_repo
66f9cf0a3bde severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/fleet-runner.yml step=Checkout
20e02889fa19 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/lint.yml step=Checkout
026cbff74a33 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/messages.yml step=Checkout_repo
e227de85a27c severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/sync-aeon-public-results.yml step=Checkout_aeon
7c001f1bd15a severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/sync-upstream.yml step=Checkout_fork
ae6e84d38c01 severity=Medium status=manual rule=actionlint/SC2086 file=.github/workflows/fleet-runner.yml step=Run_fleet_task_runner
f102d53867b2 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Determine_skill
5535ba0c284b severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Check_if_there's_work
51de415c8adb severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Validate_skill_secrets
b63d3b0e1177 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Run_pre-fetch_scripts
1b9eeff4363e severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Log_token_usage
051949b55347 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Track_token_costs
7aafea20960b severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Capture_skill_output
3332f8b86f42 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Analyze_skill_output
5ba103396fae severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Convert_feed_outputs
cf45a18cee4a severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Commit_results
f2d8296c0167 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Update_cron_state
58b55d8838c8 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=Restore_fleet_identities
93c5d3921f5c severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=Commit_results
5b3558adc1dc severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=Notify
c8163d0d9e92 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/messages.yml step=Extract_message
17e914f3a957 severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/messages.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
ab0972e6be9a severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/messages.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
f90eb9ea17da severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/sync-upstream.yml step=Push_sync_branch
0b8717f70ea1 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/sync-upstream.yml step=Open_or_update_PR
907c10fb7244 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Run
ca298be1d2d1 severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/aeon.yml step=(unknown)
e96ff3f42d77 severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/aeon.yml step=(unknown)
e0ecebefad2d severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/chain-runner.yml step=(unknown)
549a46f9e41b severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/chain-runner.yml step=(unknown)
c5e6e31ecabb severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/fleet-runner.yml step=(unknown)
b272fb7c7d18 severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/fleet-runner.yml step=(unknown)
6de4062a004e severity=Low status=manual rule=zizmor/concurrency-limits file=.github/workflows/fleet-runner.yml step=(unknown)
a9762072a520 severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/messages.yml step=(unknown)
49c90512632e severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/sync-aeon-public-results.yml step=(unknown)
980627b69ffe severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/sync-upstream.yml step=(unknown)
a325358363ef severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/sync-upstream.yml step=(unknown)
83699d9e5699 severity=Low status=manual rule=actionlint/SC2129 file=.github/workflows/aeon.yml step=Run
91b96544b7f7 severity=Low status=manual rule=actionlint/SC2129 file=.github/workflows/aeon.yml step=Log_token_usage
08b995f41897 severity=Low status=manual rule=actionlint/SC2034 file=.github/workflows/chain-runner.yml step=Run_chain
08ca247f92f5 severity=Low status=manual rule=actionlint/SC2129 file=.github/workflows/chain-runner.yml step=Run_chain
a660bb47c98f severity=Low status=manual rule=actionlint/SC2155 file=.github/workflows/chain-runner.yml step=Run_chain
67d1bc1fcdc9 severity=Low status=manual rule=actionlint/SC2155 file=.github/workflows/fleet-runner.yml step=Bootstrap_fleet_registry
06fe941af2e4 severity=Low status=manual rule=actionlint/SC2034 file=.github/workflows/messages.yml step=Determine_and_dispatch_scheduled_skills
d9f23e63cdb8 severity=Low status=manual rule=actionlint/SC2129 file=.github/workflows/messages.yml step=Extract_message
dbea56861609 severity=Low status=manual rule=actionlint/SC2129 file=.github/workflows/messages.yml step=Run
de91c5dc7925 severity=Low status=manual rule=actionlint/SC2129 file=.github/workflows/messages.yml step=Log_token_usage
-->
