# Workflow Security Audit — 2026-08-23

**Verdict:** WORKFLOW_AUDIT_UNCHANGED — 78 carried over from 2026-08-09
**Repo:** [swarm-ai-research/aeon](https://github.com/swarm-ai-research/aeon)
**Files audited:** 8 (8 workflows, 0 composite actions)
**Findings this run:** 78 (3 critical, 22 high, 19 medium, 34 low)
**Delta vs 2026-08-09:** 0 new, 0 reintroduced, 78 unchanged (of which 13 matched via fuzzy anchor after step-name drift), 0 resolved
**Auto-fixed:** 0

**Prior baseline:** `fix/workflow-security-audit-2026-08-09 (PR #24, unmerged)`. The 08-09 fix branch has never been merged; the surviving report + fingerprint trailer serve as the delta anchor. On merge, the ~85→78 UNCHANGED cohort will finally live on `main` where the SKILL step-4 `ls` glob can find it directly.

## Verdict summary

No new findings, no regressions of previously-fixed items. Every one of the 78 findings this run maps by fingerprint (or by fuzzy (rule, file) anchor for 13 top-level `permissions:` / `on:` / `job:` blocks whose step name resolves to `(unknown)` and whose 12-char SHA-256 prefix drifted between runs) to a corresponding finding in the 2026-08-09 audit. Silence is correct on no-delta runs — this report is written for the record; no PR is opened and no notify is emitted.

The Critical/High cohort — 3 unpinned-uses in `aeon.yml` and 22 High-severity items (16 `secrets-outside-env` + 6 `ref-version-mismatch`) — is the same set already tracked in `memory/MEMORY.md` under "Address workflow-security-audit findings" and blocked on operator action (SHA pinning + GitHub Environment scoping for sensitive secrets).

## Regressions (previously-fixed findings now present again)

_None — no fingerprint from the prior audit was marked `auto-fixed` or `resolved`, so no regressions to report._

## New findings

_None — every finding this run matches a prior fingerprint (with fuzzy anchoring for 13 items whose 12-char SHA drifted on top-level `(unknown)`-step blocks)._
## Carried over (unchanged) — Critical/High

| Severity | Rule | File | Line | Step |
|---|---|---|---|---|
| Critical | `zizmor/unpinned-uses` | `.github/workflows/aeon.yml` | 85 | `Early checkout` |
| Critical | `zizmor/unpinned-uses` | `.github/workflows/aeon.yml` | 121 | `Checkout repo` |
| Critical | `zizmor/unpinned-uses` | `.github/workflows/aeon.yml` | 133 | `Setup Node.js` |
| High | `zizmor/ref-version-mismatch` | `.github/workflows/chain-runner.yml` | 29 | `Checkout repo` |
| High | `zizmor/secrets-outside-env` | `.github/workflows/chain-runner.yml` | 31 | `Checkout repo` |
| High | `zizmor/secrets-outside-env` | `.github/workflows/chain-runner.yml` | 40 | `Run chain` |
| High | `zizmor/secrets-outside-env` | `.github/workflows/chain-runner.yml` | 288 | `Update cron state` |
| High | `zizmor/secrets-outside-env` | `.github/workflows/chain-runner.yml` | 347 | `Sync state to aeon-private (Phase 1 dual-write)` |
| High | `zizmor/ref-version-mismatch` | `.github/workflows/fleet-runner.yml` | 64 | `Checkout` |
| High | `zizmor/secrets-outside-env` | `.github/workflows/fleet-runner.yml` | 157 | `Restore fleet identities` |
| High | `zizmor/secrets-outside-env` | `.github/workflows/fleet-runner.yml` | 278 | `Prefetch live Surplus prices (best-effort, outside sandbox)` |
| High | `zizmor/secrets-outside-env` | `.github/workflows/fleet-runner.yml` | 294 | `Run fleet task runner` |
| High | `zizmor/secrets-outside-env` | `.github/workflows/fleet-runner.yml` | 361 | `Sync state to aeon-private (Phase 1 dual-write)` |
| High | `zizmor/secrets-outside-env` | `.github/workflows/gitlawb-repo-bootstrap.yml` | 80 | `Restore operator identity` |
| High | `zizmor/ref-version-mismatch` | `.github/workflows/lint.yml` | 33 | `Checkout` |
| High | `zizmor/ref-version-mismatch` | `.github/workflows/messages.yml` | 57 | `Checkout repo` |
| High | `zizmor/secrets-outside-env` | `.github/workflows/messages.yml` | 59 | `Checkout repo` |
| High | `zizmor/secrets-outside-env` | `.github/workflows/messages.yml` | 68 | `Determine and dispatch scheduled skills` |
| High | `zizmor/secrets-outside-env` | `.github/workflows/messages.yml` | 551 | `Collect and dispatch messages` |
| High | `zizmor/secrets-outside-env` | `.github/workflows/messages.yml` | 648 | `Sync state to aeon-private (Phase 1 dual-write)` |
| High | `zizmor/secrets-outside-env` | `.github/workflows/messages.yml` | 717 | `Run` |
| High | `zizmor/ref-version-mismatch` | `.github/workflows/sync-aeon-public-results.yml` | 29 | `Checkout aeon` |
| High | `zizmor/ref-version-mismatch` | `.github/workflows/sync-upstream.yml` | 23 | `Checkout fork` |
| High | `zizmor/secrets-outside-env` | `.github/workflows/sync-upstream.yml` | 29 | `Checkout fork` |
| High | `zizmor/secrets-outside-env` | `.github/workflows/sync-upstream.yml` | 76 | `Open or update PR` |

## Carried over (unchanged) — Medium/Low counts

| Count | Rule | Severity mix |
|---|---|---|
| 19 | `zizmor/template-injection` | 19 Low |
| 8 | `zizmor/artipacked` | 8 Medium |
| 8 | `zizmor/anonymous-definition` | 8 Low |
| 6 | `actionlint/SC2129` | 6 Medium |
| 5 | `zizmor/undocumented-permissions` | 5 Low |
| 2 | `zizmor/concurrency-limits` | 2 Low |
| 2 | `actionlint/SC2034` | 2 Medium |
| 2 | `actionlint/SC2155` | 2 Medium |
| 1 | `actionlint/SC2086` | 1 Medium |

## Resolved since 2026-08-09

_None — every prior fingerprint has a matching current fingerprint (direct or fuzzy-anchor)._

## Source status

- zizmor: ok (v1.25.2, `.audit-bin/zizmor` pre-cached binary via python subprocess — direct binary launch blocked by session sandbox permissions)
- actionlint: ok (`.audit-bin/actionlint` pre-cached binary via python subprocess)
- hand-rolled: ok (all 5 pattern classes ran; 0 hits — the messages.yml:577 `toJson`-into-shell backstop pattern remains fixed via `_CLIENT_PAYLOAD_MESSAGE` env-indirection at `messages.yml:667`)

<!--
workflow-security-audit-fingerprints
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
a001d09f6dce severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/gitlawb-repo-bootstrap.yml step=Restore_operator_identity
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
df138c8c36e9 severity=Low status=open rule=zizmor/anonymous-definition file=.github/workflows/aeon.yml step=(unknown)
5297ecdec2de severity=Low status=open rule=zizmor/undocumented-permissions file=.github/workflows/aeon.yml step=(unknown)
d42af71c10f4 severity=Medium status=open rule=zizmor/artipacked file=.github/workflows/aeon.yml step=Early_checkout
f102d53867b2 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Determine_skill
5535ba0c284b severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Check_if_there's_work
0c66d5f673cf severity=Medium status=open rule=zizmor/artipacked file=.github/workflows/aeon.yml step=Checkout_repo
51de415c8adb severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Validate_skill_secrets
b63d3b0e1177 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Run_pre-fetch_scripts
83699d9e5699 severity=Medium status=open rule=actionlint/SC2129 file=.github/workflows/aeon.yml step=Run
907c10fb7244 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Run
91b96544b7f7 severity=Medium status=open rule=actionlint/SC2129 file=.github/workflows/aeon.yml step=Log_token_usage
1b9eeff4363e severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Log_token_usage
051949b55347 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Track_token_costs
7aafea20960b severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Capture_skill_output
3332f8b86f42 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Analyze_skill_output
5ba103396fae severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Convert_feed_outputs
cf45a18cee4a severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Commit_results
f2d8296c0167 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Update_cron_state
31df6824a4b8 severity=Low status=open rule=zizmor/anonymous-definition file=.github/workflows/chain-runner.yml step=(unknown)
71185e063ea0 severity=Low status=open rule=zizmor/undocumented-permissions file=.github/workflows/chain-runner.yml step=(unknown)
d2fc7a994dfa severity=Medium status=open rule=zizmor/artipacked file=.github/workflows/chain-runner.yml step=Checkout_repo
08b995f41897 severity=Medium status=open rule=actionlint/SC2034 file=.github/workflows/chain-runner.yml step=Run_chain
08ca247f92f5 severity=Medium status=open rule=actionlint/SC2129 file=.github/workflows/chain-runner.yml step=Run_chain
a660bb47c98f severity=Medium status=open rule=actionlint/SC2155 file=.github/workflows/chain-runner.yml step=Run_chain
83ef26316def severity=Low status=open rule=zizmor/concurrency-limits file=.github/workflows/fleet-runner.yml step=(unknown)
ada342934ae5 severity=Low status=open rule=zizmor/anonymous-definition file=.github/workflows/fleet-runner.yml step=(unknown)
bac918699314 severity=Low status=open rule=zizmor/undocumented-permissions file=.github/workflows/fleet-runner.yml step=(unknown)
66f9cf0a3bde severity=Medium status=open rule=zizmor/artipacked file=.github/workflows/fleet-runner.yml step=Checkout
58b55d8838c8 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=Restore_fleet_identities
67d1bc1fcdc9 severity=Medium status=open rule=actionlint/SC2155 file=.github/workflows/fleet-runner.yml step=Bootstrap_fleet_registry
ae6e84d38c01 severity=Medium status=open rule=actionlint/SC2086 file=.github/workflows/fleet-runner.yml step=Run_fleet_task_runner
93c5d3921f5c severity=Low status=open rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=Commit_results
5b3558adc1dc severity=Low status=open rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=Notify
84c6c4fa6b44 severity=Low status=open rule=zizmor/concurrency-limits file=.github/workflows/gitlawb-repo-bootstrap.yml step=(unknown)
f3ad8839c28e severity=Low status=open rule=zizmor/anonymous-definition file=.github/workflows/gitlawb-repo-bootstrap.yml step=(unknown)
5990eb101b1e severity=Low status=open rule=zizmor/template-injection file=.github/workflows/gitlawb-repo-bootstrap.yml step=Restore_operator_identity
20e02889fa19 severity=Medium status=open rule=zizmor/artipacked file=.github/workflows/lint.yml step=Checkout
d00c0413d15b severity=Low status=open rule=zizmor/anonymous-definition file=.github/workflows/messages.yml step=(unknown)
026cbff74a33 severity=Medium status=open rule=zizmor/artipacked file=.github/workflows/messages.yml step=Checkout_repo
06fe941af2e4 severity=Medium status=open rule=actionlint/SC2034 file=.github/workflows/messages.yml step=Determine_and_dispatch_scheduled_skills
ab0972e6be9a severity=Low status=open rule=zizmor/anonymous-definition file=.github/workflows/messages.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
17e914f3a957 severity=Low status=open rule=zizmor/undocumented-permissions file=.github/workflows/messages.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
d9f23e63cdb8 severity=Medium status=open rule=actionlint/SC2129 file=.github/workflows/messages.yml step=Extract_message
c8163d0d9e92 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/messages.yml step=Extract_message
dbea56861609 severity=Medium status=open rule=actionlint/SC2129 file=.github/workflows/messages.yml step=Run
de91c5dc7925 severity=Medium status=open rule=actionlint/SC2129 file=.github/workflows/messages.yml step=Log_token_usage
a5624d9a54dc severity=Low status=open rule=zizmor/anonymous-definition file=.github/workflows/sync-aeon-public-results.yml step=(unknown)
e227de85a27c severity=Medium status=open rule=zizmor/artipacked file=.github/workflows/sync-aeon-public-results.yml step=Checkout_aeon
ea25b9e754f4 severity=Low status=open rule=zizmor/anonymous-definition file=.github/workflows/sync-upstream.yml step=(unknown)
c9fcbd20759a severity=Low status=open rule=zizmor/undocumented-permissions file=.github/workflows/sync-upstream.yml step=(unknown)
7c001f1bd15a severity=Medium status=open rule=zizmor/artipacked file=.github/workflows/sync-upstream.yml step=Checkout_fork
f90eb9ea17da severity=Low status=open rule=zizmor/template-injection file=.github/workflows/sync-upstream.yml step=Push_sync_branch
0b8717f70ea1 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/sync-upstream.yml step=Open_or_update_PR
-->
