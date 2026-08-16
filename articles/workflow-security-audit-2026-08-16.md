# Workflow Security Audit — 2026-08-16

**Verdict:** WORKFLOW_AUDIT_UNCHANGED — 78 carried over from 2026-08-09
**Repo:** [swarm-ai-research/aeon](https://github.com/swarm-ai-research/aeon)
**Files audited:** 8 (8 workflows, 0 composite actions)
**Findings this run:** 78 (3 critical, 22 high, 9 medium, 44 low)
**Delta vs 2026-08-09:** 0 new, 0 reintroduced, 78 unchanged, 0 resolved
**Auto-fixed:** 0

## Regressions (previously-fixed findings now present again)

_None. No prior fingerprint was marked `auto-fixed` or `resolved`, so there is nothing to regress against._

## New findings

_None. Every finding present on this run was also present on `2026-08-09` (same rule / file / step across all 78 items) — no NEW deltas, no auto-fix work, no notify._

Per the SKILL step-5 gating rule, `UNCHANGED` mode does not open a PR and does not notify; silence is correct on no-delta runs so the notify channel stays high-signal. The full carried-over set is captured below for completeness and for the next run's delta baseline.

## Carried over (unchanged from 2026-08-09)

Every finding below has a stable fingerprint in the trailer at the bottom of this file. The next run keys against those to detect regressions.

| Severity | Rule | Count | Files |
|---|---|---|---|
| Critical | `zizmor/unpinned-uses` | 3 | aeon.yml(3) |
| High | `zizmor/ref-version-mismatch` | 6 | chain-runner.yml(1), fleet-runner.yml(1), lint.yml(1), messages.yml(1), sync-aeon-public-results.yml(1), sync-upstream.yml(1) |
| High | `zizmor/secrets-outside-env` | 16 | chain-runner.yml(4), fleet-runner.yml(4), gitlawb-repo-bootstrap.yml(1), messages.yml(5), sync-upstream.yml(2) |
| Medium | `actionlint/SC2086` | 1 | fleet-runner.yml(1) |
| Medium | `zizmor/artipacked` | 8 | aeon.yml(2), chain-runner.yml(1), fleet-runner.yml(1), lint.yml(1), messages.yml(1), sync-aeon-public-results.yml(1), sync-upstream.yml(1) |
| Low | `actionlint/SC2034` | 2 | chain-runner.yml(1), messages.yml(1) |
| Low | `actionlint/SC2129` | 6 | aeon.yml(2), chain-runner.yml(1), messages.yml(3) |
| Low | `actionlint/SC2155` | 2 | chain-runner.yml(1), fleet-runner.yml(1) |
| Low | `zizmor/anonymous-definition` | 8 | aeon.yml(1), chain-runner.yml(1), fleet-runner.yml(1), gitlawb-repo-bootstrap.yml(1), messages.yml(2), sync-aeon-public-results.yml(1), sync-upstream.yml(1) |
| Low | `zizmor/concurrency-limits` | 2 | fleet-runner.yml(1), gitlawb-repo-bootstrap.yml(1) |
| Low | `zizmor/template-injection` | 19 | aeon.yml(12), fleet-runner.yml(3), gitlawb-repo-bootstrap.yml(1), messages.yml(1), sync-upstream.yml(2) |
| Low | `zizmor/undocumented-permissions` | 5 | aeon.yml(1), chain-runner.yml(1), fleet-runner.yml(1), messages.yml(1), sync-upstream.yml(1) |

### Critical + High detail (all carried over, all still `Manual required`)

| Severity | Rule | File | Step | First seen |
|---|---|---|---|---|
| Critical | `zizmor/unpinned-uses` | `aeon.yml` | `Checkout repo` | ≤ 2026-08-09 |
| Critical | `zizmor/unpinned-uses` | `aeon.yml` | `Early checkout` | ≤ 2026-08-09 |
| Critical | `zizmor/unpinned-uses` | `aeon.yml` | `Setup Node.js` | ≤ 2026-08-09 |
| High | `zizmor/ref-version-mismatch` | `chain-runner.yml` | `Checkout repo` | ≤ 2026-08-09 |
| High | `zizmor/ref-version-mismatch` | `fleet-runner.yml` | `Checkout` | ≤ 2026-08-09 |
| High | `zizmor/ref-version-mismatch` | `lint.yml` | `Checkout` | ≤ 2026-08-09 |
| High | `zizmor/ref-version-mismatch` | `messages.yml` | `Checkout repo` | ≤ 2026-08-09 |
| High | `zizmor/ref-version-mismatch` | `sync-aeon-public-results.yml` | `Checkout aeon` | ≤ 2026-08-09 |
| High | `zizmor/ref-version-mismatch` | `sync-upstream.yml` | `Checkout fork` | ≤ 2026-08-09 |
| High | `zizmor/secrets-outside-env` | `chain-runner.yml` | `Checkout repo` | ≤ 2026-08-09 |
| High | `zizmor/secrets-outside-env` | `chain-runner.yml` | `Run chain` | ≤ 2026-08-09 |
| High | `zizmor/secrets-outside-env` | `chain-runner.yml` | `Sync state to aeon-private (Phase 1 dual-write)` | ≤ 2026-08-09 |
| High | `zizmor/secrets-outside-env` | `chain-runner.yml` | `Update cron state` | ≤ 2026-08-09 |
| High | `zizmor/secrets-outside-env` | `fleet-runner.yml` | `Prefetch live Surplus prices (best-effort, outside sandbox)` | ≤ 2026-08-09 |
| High | `zizmor/secrets-outside-env` | `fleet-runner.yml` | `Restore fleet identities` | ≤ 2026-08-09 |
| High | `zizmor/secrets-outside-env` | `fleet-runner.yml` | `Run fleet task runner` | ≤ 2026-08-09 |
| High | `zizmor/secrets-outside-env` | `fleet-runner.yml` | `Sync state to aeon-private (Phase 1 dual-write)` | ≤ 2026-08-09 |
| High | `zizmor/secrets-outside-env` | `gitlawb-repo-bootstrap.yml` | `Restore operator identity` | ≤ 2026-08-09 |
| High | `zizmor/secrets-outside-env` | `messages.yml` | `Checkout repo` | ≤ 2026-08-09 |
| High | `zizmor/secrets-outside-env` | `messages.yml` | `Collect and dispatch messages` | ≤ 2026-08-09 |
| High | `zizmor/secrets-outside-env` | `messages.yml` | `Determine and dispatch scheduled skills` | ≤ 2026-08-09 |
| High | `zizmor/secrets-outside-env` | `messages.yml` | `Run` | ≤ 2026-08-09 |
| High | `zizmor/secrets-outside-env` | `messages.yml` | `Sync state to aeon-private (Phase 1 dual-write)` | ≤ 2026-08-09 |
| High | `zizmor/secrets-outside-env` | `sync-upstream.yml` | `Checkout fork` | ≤ 2026-08-09 |
| High | `zizmor/secrets-outside-env` | `sync-upstream.yml` | `Open or update PR` | ≤ 2026-08-09 |

## Resolved since 2026-08-09

_None. Every fingerprint from the prior audit still fires on this run — the operator toggle that keeps the fix branch from merging (`enabled: false` decisions, environment gating, SHA-pin operator approval) is still the primary blocker._

## Source status

- zizmor 1.25.2: `ok`
- actionlint 1.7.12: `ok`
- hand-rolled backstops: `ok` (toJson-into-shell, pull_request_target + persist-credentials, GITHUB_ENV injection — 0 hits, April 11 `messages.yml:577` regression pattern remains fixed)

## Method note

Prior report on `main` is absent (the historical `fix/workflow-security-audit-*` branches remain unmerged per `[[github-actions-cannot-create-prs]]`). Fell back to `git fetch origin fix/workflow-security-audit-2026-08-09` for the trailer. Semkey matching is `(rule_id, basename(file), step_name)` — line-fallback via SARIF snippet plus a `- name:` walker back from the reported line — which absorbs unrelated edits that shift line numbers without changing the finding.

<!--
workflow-security-audit-fingerprints
7491c14fbe74 severity=Critical status=manual rule=zizmor/unpinned-uses file=.github/workflows/aeon.yml step=Checkout_repo
9fb519eb4fdb severity=Critical status=manual rule=zizmor/unpinned-uses file=.github/workflows/aeon.yml step=Early_checkout
920a2c40af77 severity=Critical status=manual rule=zizmor/unpinned-uses file=.github/workflows/aeon.yml step=Setup_Node.js
92de995e00e5 severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/chain-runner.yml step=Checkout_repo
d5fac004ec2a severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/fleet-runner.yml step=Checkout
e04aa697aeac severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/lint.yml step=Checkout
43037ab85149 severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/messages.yml step=Checkout_repo
f77041a532da severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/sync-aeon-public-results.yml step=Checkout_aeon
63faf96ee9e4 severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/sync-upstream.yml step=Checkout_fork
cfad683f1a80 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/chain-runner.yml step=Checkout_repo
92be19585492 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/chain-runner.yml step=Run_chain
07c66694806a severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/chain-runner.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
bde515abcfd3 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/chain-runner.yml step=Update_cron_state
492f5627d723 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=Prefetch_live_Surplus_prices_(best-effort,_outside_sandbox)
8970a9ecf814 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=Restore_fleet_identities
9e568b8ce48d severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=Run_fleet_task_runner
6a78074b9b49 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
a001d09f6dce severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/gitlawb-repo-bootstrap.yml step=Restore_operator_identity
e619ae84091a severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=Checkout_repo
d07b94573673 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=Collect_and_dispatch_messages
eb3f904202e5 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=Determine_and_dispatch_scheduled_skills
b38245804892 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=Run
9cff378b979c severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
7b4cecdf97db severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/sync-upstream.yml step=Checkout_fork
8ea38df05599 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/sync-upstream.yml step=Open_or_update_PR
ae6e84d38c01 severity=Medium status=manual rule=actionlint/SC2086 file=.github/workflows/fleet-runner.yml step=Run_fleet_task_runner
0c66d5f673cf severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/aeon.yml step=Checkout_repo
d42af71c10f4 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/aeon.yml step=Early_checkout
d2fc7a994dfa severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/chain-runner.yml step=Checkout_repo
66f9cf0a3bde severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/fleet-runner.yml step=Checkout
20e02889fa19 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/lint.yml step=Checkout
026cbff74a33 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/messages.yml step=Checkout_repo
e227de85a27c severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/sync-aeon-public-results.yml step=Checkout_aeon
7c001f1bd15a severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/sync-upstream.yml step=Checkout_fork
08b995f41897 severity=Low status=manual rule=actionlint/SC2034 file=.github/workflows/chain-runner.yml step=Run_chain
06fe941af2e4 severity=Low status=manual rule=actionlint/SC2034 file=.github/workflows/messages.yml step=Determine_and_dispatch_scheduled_skills
91b96544b7f7 severity=Low status=manual rule=actionlint/SC2129 file=.github/workflows/aeon.yml step=Log_token_usage
83699d9e5699 severity=Low status=manual rule=actionlint/SC2129 file=.github/workflows/aeon.yml step=Run
08ca247f92f5 severity=Low status=manual rule=actionlint/SC2129 file=.github/workflows/chain-runner.yml step=Run_chain
d9f23e63cdb8 severity=Low status=manual rule=actionlint/SC2129 file=.github/workflows/messages.yml step=Extract_message
de91c5dc7925 severity=Low status=manual rule=actionlint/SC2129 file=.github/workflows/messages.yml step=Log_token_usage
dbea56861609 severity=Low status=manual rule=actionlint/SC2129 file=.github/workflows/messages.yml step=Run
a660bb47c98f severity=Low status=manual rule=actionlint/SC2155 file=.github/workflows/chain-runner.yml step=Run_chain
67d1bc1fcdc9 severity=Low status=manual rule=actionlint/SC2155 file=.github/workflows/fleet-runner.yml step=Bootstrap_fleet_registry
e96ff3f42d77 severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/aeon.yml step=(unknown)
549a46f9e41b severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/chain-runner.yml step=(unknown)
b272fb7c7d18 severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/fleet-runner.yml step=(unknown)
3f73d5880a40 severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/gitlawb-repo-bootstrap.yml step=(unknown)
a9762072a520 severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/messages.yml step=(unknown)
ab0972e6be9a severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/messages.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
49c90512632e severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/sync-aeon-public-results.yml step=(unknown)
a325358363ef severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/sync-upstream.yml step=(unknown)
6de4062a004e severity=Low status=manual rule=zizmor/concurrency-limits file=.github/workflows/fleet-runner.yml step=(unknown)
9d01e01f8dab severity=Low status=manual rule=zizmor/concurrency-limits file=.github/workflows/gitlawb-repo-bootstrap.yml step=(unknown)
3332f8b86f42 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Analyze_skill_output
7aafea20960b severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Capture_skill_output
5535ba0c284b severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Check_if_there's_work
cf45a18cee4a severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Commit_results
5ba103396fae severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Convert_feed_outputs
f102d53867b2 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Determine_skill
1b9eeff4363e severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Log_token_usage
907c10fb7244 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Run
b63d3b0e1177 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Run_pre-fetch_scripts
051949b55347 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Track_token_costs
f2d8296c0167 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Update_cron_state
51de415c8adb severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Validate_skill_secrets
93c5d3921f5c severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=Commit_results
5b3558adc1dc severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=Notify
58b55d8838c8 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=Restore_fleet_identities
5990eb101b1e severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/gitlawb-repo-bootstrap.yml step=Restore_operator_identity
c8163d0d9e92 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/messages.yml step=Extract_message
0b8717f70ea1 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/sync-upstream.yml step=Open_or_update_PR
f90eb9ea17da severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/sync-upstream.yml step=Push_sync_branch
ca298be1d2d1 severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/aeon.yml step=(unknown)
e0ecebefad2d severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/chain-runner.yml step=(unknown)
c5e6e31ecabb severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/fleet-runner.yml step=(unknown)
17e914f3a957 severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/messages.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
980627b69ffe severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/sync-upstream.yml step=(unknown)
-->
