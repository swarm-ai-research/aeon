# Workflow Security Audit — 2026-08-02

**Verdict:** WORKFLOW_AUDIT_UNCHANGED — 75 carried over from 2026-07-26
**Repo:** [swarm-ai-research/aeon](https://github.com/swarm-ai-research/aeon)
**Files audited:** 7 (7 workflows, 0 composite actions)
**Findings this run:** 75 (3 critical, 21 high, 19 medium, 32 low)
**Delta vs 2026-07-26:** 0 new, 0 reintroduced, 75 unchanged, 0 resolved
**Auto-fixed:** 0

## Verdict interpretation

`UNCHANGED` — every finding here was already surfaced in the [2026-07-26 audit](../../../tree/fix/workflow-security-audit-2026-07-26/articles/workflow-security-audit-2026-07-26.md) and none have been fixed since. Per the skill's gating rule, no PR is opened and no notify fires — silence on no-delta runs is intentional so the notify channel does not learn to be ignored.

The 3 Critical + 21 High items sit on the same MEMORY.md follow-up (per `## Pointers`): (a) pin the `actions/checkout@v5` and `actions/setup-node@v5` refs in `aeon.yml` to SHAs, (b) create `production` and `chain-runner` GitHub Environments and move sensitive secrets (`GH_GLOBAL`, `GITLAWB_*_PEM`, `AEON_PRIVATE_PAT`, `CLAUDE_CODE_OAUTH_TOKEN`) from repo-scoped to environment-scoped, (c) address 11 `zizmor/artipacked` Mediums (`persist-credentials: false` on read-only checkouts). These require operator judgment — auto-fix is deliberately out of scope for pinning, permissions, and persist-credentials per skill constraints.

## Regressions (previously-fixed findings now present again)

_None — no fingerprints marked `auto-fixed` or `resolved` in the prior report have re-appeared._

## New findings

_None — no fingerprints appeared this run that were absent from the prior audit._

## Carried over (unchanged)

| Severity | Rule | File | Step | Line |
|---|---|---|---|---|
| Critical | `zizmor/unpinned-uses` | `aeon.yml` | `Early_checkout` | 85 |
| Critical | `zizmor/unpinned-uses` | `aeon.yml` | `Checkout_repo` | 121 |
| Critical | `zizmor/unpinned-uses` | `aeon.yml` | `Setup_Node.js` | 133 |
| High | `zizmor/ref-version-mismatch` | `chain-runner.yml` | `Checkout_repo` | 29 |
| High | `zizmor/secrets-outside-env` | `chain-runner.yml` | `Checkout_repo` | 31 |
| High | `zizmor/secrets-outside-env` | `chain-runner.yml` | `Run_chain` | 40 |
| High | `zizmor/secrets-outside-env` | `chain-runner.yml` | `Update_cron_state` | 288 |
| High | `zizmor/secrets-outside-env` | `chain-runner.yml` | `Sync_state_to_aeon-private_(Phase_1_dual` | 347 |
| High | `zizmor/ref-version-mismatch` | `fleet-runner.yml` | `Checkout` | 57 |
| High | `zizmor/secrets-outside-env` | `fleet-runner.yml` | `Restore_fleet_identities` | 150 |
| High | `zizmor/secrets-outside-env` | `fleet-runner.yml` | `Prefetch_live_Surplus_prices_(best-effor` | 271 |
| High | `zizmor/secrets-outside-env` | `fleet-runner.yml` | `Run_fleet_task_runner` | 287 |
| High | `zizmor/secrets-outside-env` | `fleet-runner.yml` | `Sync_state_to_aeon-private_(Phase_1_dual` | 354 |
| High | `zizmor/ref-version-mismatch` | `lint.yml` | `Checkout` | 33 |
| High | `zizmor/ref-version-mismatch` | `messages.yml` | `Checkout_repo` | 57 |
| High | `zizmor/secrets-outside-env` | `messages.yml` | `Checkout_repo` | 59 |
| High | `zizmor/secrets-outside-env` | `messages.yml` | `Determine_and_dispatch_scheduled_skills` | 68 |
| High | `zizmor/secrets-outside-env` | `messages.yml` | `Collect_and_dispatch_messages` | 551 |
| High | `zizmor/secrets-outside-env` | `messages.yml` | `Sync_state_to_aeon-private_(Phase_1_dual` | 648 |
| High | `zizmor/secrets-outside-env` | `messages.yml` | `Run` | 717 |
| High | `zizmor/ref-version-mismatch` | `sync-aeon-public-results.yml` | `Checkout_aeon` | 29 |
| High | `zizmor/ref-version-mismatch` | `sync-upstream.yml` | `Checkout_fork` | 23 |
| High | `zizmor/secrets-outside-env` | `sync-upstream.yml` | `Checkout_fork` | 29 |
| High | `zizmor/secrets-outside-env` | `sync-upstream.yml` | `Open_or_update_PR` | 76 |
| Medium | `zizmor/artipacked` | `aeon.yml` | `Early_checkout` | 83 |
| Medium | `zizmor/artipacked` | `aeon.yml` | `Checkout_repo` | 119 |
| Medium | `actionlint/SC2129` | `aeon.yml` | `Run` | 286 |
| Medium | `actionlint/SC2129` | `aeon.yml` | `Log_token_usage` | 601 |
| Medium | `zizmor/artipacked` | `chain-runner.yml` | `Checkout_repo` | 28 |
| Medium | `actionlint/SC2034` | `chain-runner.yml` | `Run_chain` | 42 |
| Medium | `actionlint/SC2129` | `chain-runner.yml` | `Run_chain` | 42 |
| Medium | `actionlint/SC2155` | `chain-runner.yml` | `Run_chain` | 42 |
| Medium | `zizmor/artipacked` | `fleet-runner.yml` | `Checkout` | 56 |
| Medium | `actionlint/SC2155` | `fleet-runner.yml` | `Bootstrap_fleet_registry` | 179 |
| Medium | `actionlint/SC2086` | `fleet-runner.yml` | `Run_fleet_task_runner` | 294 |
| Medium | `zizmor/artipacked` | `lint.yml` | `Checkout` | 32 |
| Medium | `zizmor/artipacked` | `messages.yml` | `Checkout_repo` | 56 |
| Medium | `actionlint/SC2034` | `messages.yml` | `Determine_and_dispatch_scheduled_skills` | 69 |
| Medium | `actionlint/SC2129` | `messages.yml` | `Extract_message` | 669 |
| Medium | `actionlint/SC2129` | `messages.yml` | `Run` | 734 |
| Medium | `actionlint/SC2129` | `messages.yml` | `Log_token_usage` | 815 |
| Medium | `zizmor/artipacked` | `sync-aeon-public-results.yml` | `Checkout_aeon` | 28 |
| Medium | `zizmor/artipacked` | `sync-upstream.yml` | `Checkout_fork` | 22 |
| Low | `zizmor/anonymous-definition` | `aeon.yml` | `line72` | 72 |
| Low | `zizmor/undocumented-permissions` | `aeon.yml` | `line77` | 77 |
| Low | `zizmor/template-injection` | `aeon.yml` | `Determine_skill` | 98 |
| Low | `zizmor/template-injection` | `aeon.yml` | `Check_if_there's_work` | 112 |
| Low | `zizmor/template-injection` | `aeon.yml` | `Validate_skill_secrets` | 150 |
| Low | `zizmor/template-injection` | `aeon.yml` | `Run_pre-fetch_scripts` | 194 |
| Low | `zizmor/template-injection` | `aeon.yml` | `Run` | 288 |
| Low | `zizmor/template-injection` | `aeon.yml` | `line480` | 480 |
| Low | `zizmor/template-injection` | `aeon.yml` | `Log_token_usage` | 602 |
| Low | `zizmor/template-injection` | `aeon.yml` | `Track_token_costs` | 625 |
| Low | `zizmor/template-injection` | `aeon.yml` | `Capture_skill_output` | 630 |
| Low | `zizmor/template-injection` | `aeon.yml` | `Analyze_skill_output` | 651 |
| Low | `zizmor/template-injection` | `aeon.yml` | `Convert_feed_outputs` | 752 |
| Low | `zizmor/template-injection` | `aeon.yml` | `Commit_results` | 863 |
| Low | `zizmor/template-injection` | `aeon.yml` | `Update_cron_state` | 927 |
| Low | `zizmor/anonymous-definition` | `chain-runner.yml` | `line20` | 20 |
| Low | `zizmor/undocumented-permissions` | `chain-runner.yml` | `line24` | 24 |
| Low | `zizmor/concurrency-limits` | `fleet-runner.yml` | `line4` | 4 |
| Low | `zizmor/anonymous-definition` | `fleet-runner.yml` | `line44` | 44 |
| Low | `zizmor/undocumented-permissions` | `fleet-runner.yml` | `line48` | 48 |
| Low | `zizmor/template-injection` | `fleet-runner.yml` | `Restore_fleet_identities` | 150 |
| Low | `zizmor/template-injection` | `fleet-runner.yml` | `Commit_results` | 315 |
| Low | `zizmor/template-injection` | `fleet-runner.yml` | `Notify` | 347 |
| Low | `zizmor/anonymous-definition` | `messages.yml` | `line47` | 47 |
| Low | `zizmor/anonymous-definition` | `messages.yml` | `Sync_state_to_aeon-private_(Phase_1_dual` | 651 |
| Low | `zizmor/undocumented-permissions` | `messages.yml` | `Sync_state_to_aeon-private_(Phase_1_dual` | 658 |
| Low | `zizmor/template-injection` | `messages.yml` | `Extract_message` | 670 |
| Low | `zizmor/anonymous-definition` | `sync-aeon-public-results.yml` | `line23` | 23 |
| Low | `zizmor/anonymous-definition` | `sync-upstream.yml` | `line16` | 16 |
| Low | `zizmor/undocumented-permissions` | `sync-upstream.yml` | `line19` | 19 |
| Low | `zizmor/template-injection` | `sync-upstream.yml` | `Push_sync_branch` | 71 |
| Low | `zizmor/template-injection` | `sync-upstream.yml` | `Open_or_update_PR` | 78 |

## Resolved since 2026-07-26

_None — no fingerprints from the prior audit are absent from this run._

## Source status

- zizmor 1.25.2 (via `.audit-bin/zizmor`): **ok** — 125 raw results, dedup → 43 unique
- actionlint 1.7.12 (via `.audit-bin/actionlint`): **ok** — 20 shellcheck results, 2 upgraded to High for SC2086 near `${{ github.* }}`
- hand-rolled backstops (`toJson-into-shell`, `persist-credentials + head.sha`, `GITHUB_ENV` write injection, fleet inputs passthrough, mutable third-party ref): **ok** — 0 hits (April 11 `messages.yml:577` pattern remains fixed)

<!--
workflow-security-audit-fingerprints
3dbcbd5d67e12bd2 severity=Critical status=manual rule=zizmor/unpinned-uses file=.github/workflows/aeon.yml step=Early_checkout line=85 delta=UNCHANGED
d85d65ea95719cc0 severity=Critical status=manual rule=zizmor/unpinned-uses file=.github/workflows/aeon.yml step=Checkout_repo line=121 delta=UNCHANGED
1c76afe5a59326fc severity=Critical status=manual rule=zizmor/unpinned-uses file=.github/workflows/aeon.yml step=Setup_Node.js line=133 delta=UNCHANGED
736a26f1a6847b8b severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/chain-runner.yml step=Checkout_repo line=29 delta=UNCHANGED
cfc4704b6b9da385 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/chain-runner.yml step=Checkout_repo line=31 delta=UNCHANGED
9ca6a32f200ea550 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/chain-runner.yml step=Run_chain line=40 delta=UNCHANGED
8942a4f9874fe2cd severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/chain-runner.yml step=Update_cron_state line=288 delta=UNCHANGED
3fdb68ecdfae6469 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/chain-runner.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write) line=347 delta=UNCHANGED
b6a515b9fdce8a71 severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/fleet-runner.yml step=Checkout line=57 delta=UNCHANGED
af76df5322872127 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=Restore_fleet_identities line=150 delta=UNCHANGED
6caedf1baaf127d5 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=Prefetch_live_Surplus_prices_(best-effort,_outside_sandbox) line=271 delta=UNCHANGED
3859586b82478e6b severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=Run_fleet_task_runner line=287 delta=UNCHANGED
a145c985a63c1a87 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write) line=354 delta=UNCHANGED
53a6dcdb26fa3b84 severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/lint.yml step=Checkout line=33 delta=UNCHANGED
b6a7f6aa899fac1b severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/messages.yml step=Checkout_repo line=57 delta=UNCHANGED
8e3d7d77c9df7452 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=Checkout_repo line=59 delta=UNCHANGED
530b05dab29c2bcc severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=Determine_and_dispatch_scheduled_skills line=68 delta=UNCHANGED
b1588a9c404eecab severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=Collect_and_dispatch_messages line=551 delta=UNCHANGED
a2338cb3ec2b60e6 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write) line=648 delta=UNCHANGED
50e4cd47a6d968a4 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=Run line=717 delta=UNCHANGED
d80e3c31b6d40d62 severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/sync-aeon-public-results.yml step=Checkout_aeon line=29 delta=UNCHANGED
19c6a1ccad3b38d5 severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/sync-upstream.yml step=Checkout_fork line=23 delta=UNCHANGED
dbc0b29aa33d4d3d severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/sync-upstream.yml step=Checkout_fork line=29 delta=UNCHANGED
c2cd7cccd95fe122 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/sync-upstream.yml step=Open_or_update_PR line=76 delta=UNCHANGED
248b89651714d258 severity=Medium status=open rule=zizmor/artipacked file=.github/workflows/aeon.yml step=Early_checkout line=83 delta=UNCHANGED
54234a2fc6c7430a severity=Medium status=open rule=zizmor/artipacked file=.github/workflows/aeon.yml step=Checkout_repo line=119 delta=UNCHANGED
61cc81d9053e771f severity=Medium status=open rule=actionlint/SC2129 file=.github/workflows/aeon.yml step=Run line=286 delta=UNCHANGED
3dc7ee6c4e138473 severity=Medium status=open rule=actionlint/SC2129 file=.github/workflows/aeon.yml step=Log_token_usage line=601 delta=UNCHANGED
efac310187bac2d3 severity=Medium status=open rule=zizmor/artipacked file=.github/workflows/chain-runner.yml step=Checkout_repo line=28 delta=UNCHANGED
87fad36648fe1005 severity=Medium status=open rule=actionlint/SC2034 file=.github/workflows/chain-runner.yml step=Run_chain line=42 delta=UNCHANGED
8b226d600508f001 severity=Medium status=open rule=actionlint/SC2129 file=.github/workflows/chain-runner.yml step=Run_chain line=42 delta=UNCHANGED
7240c42c2d4256ce severity=Medium status=open rule=actionlint/SC2155 file=.github/workflows/chain-runner.yml step=Run_chain line=42 delta=UNCHANGED
eb90a799b0dae9a0 severity=Medium status=open rule=zizmor/artipacked file=.github/workflows/fleet-runner.yml step=Checkout line=56 delta=UNCHANGED
6d0f9b1271dd4488 severity=Medium status=open rule=actionlint/SC2155 file=.github/workflows/fleet-runner.yml step=Bootstrap_fleet_registry line=179 delta=UNCHANGED
25c7d5bee4bfdc5d severity=Medium status=open rule=actionlint/SC2086 file=.github/workflows/fleet-runner.yml step=Run_fleet_task_runner line=294 delta=UNCHANGED
128a919e78a0c890 severity=Medium status=open rule=zizmor/artipacked file=.github/workflows/lint.yml step=Checkout line=32 delta=UNCHANGED
9d7b8dae6e7516b0 severity=Medium status=open rule=zizmor/artipacked file=.github/workflows/messages.yml step=Checkout_repo line=56 delta=UNCHANGED
58cc066eb2271b73 severity=Medium status=open rule=actionlint/SC2034 file=.github/workflows/messages.yml step=Determine_and_dispatch_scheduled_skills line=69 delta=UNCHANGED
b64c2146a24785af severity=Medium status=open rule=actionlint/SC2129 file=.github/workflows/messages.yml step=Extract_message line=669 delta=UNCHANGED
0e93c659db798a03 severity=Medium status=open rule=actionlint/SC2129 file=.github/workflows/messages.yml step=Run line=734 delta=UNCHANGED
55172540ced11603 severity=Medium status=open rule=actionlint/SC2129 file=.github/workflows/messages.yml step=Log_token_usage line=815 delta=UNCHANGED
a1d529ca6c21ba65 severity=Medium status=open rule=zizmor/artipacked file=.github/workflows/sync-aeon-public-results.yml step=Checkout_aeon line=28 delta=UNCHANGED
31869ec82722d8bf severity=Medium status=open rule=zizmor/artipacked file=.github/workflows/sync-upstream.yml step=Checkout_fork line=22 delta=UNCHANGED
ffc6676cb17342bf severity=Low status=open rule=zizmor/anonymous-definition file=.github/workflows/aeon.yml step=line72 line=72 delta=UNCHANGED
0559211984bfbe84 severity=Low status=open rule=zizmor/undocumented-permissions file=.github/workflows/aeon.yml step=line77 line=77 delta=UNCHANGED
962d8841839cbb2e severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Determine_skill line=98 delta=UNCHANGED
800850b22511f21c severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Check_if_there's_work line=112 delta=UNCHANGED
946702e561b6a3f1 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Validate_skill_secrets line=150 delta=UNCHANGED
d833d6df0f51c93d severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Run_pre-fetch_scripts line=194 delta=UNCHANGED
a2958a26d449e976 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Run line=288 delta=UNCHANGED
88861fd68b7f6c11 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=line480 line=480 delta=UNCHANGED
b27a3fdbeb938fd8 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Log_token_usage line=602 delta=UNCHANGED
442cf8d8d297ad37 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Track_token_costs line=625 delta=UNCHANGED
1aa058af791a5038 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Capture_skill_output line=630 delta=UNCHANGED
05b3c620ed2161e1 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Analyze_skill_output line=651 delta=UNCHANGED
54f472fde9d1f031 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Convert_feed_outputs line=752 delta=UNCHANGED
e23dc1e7a4c22959 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Commit_results line=863 delta=UNCHANGED
f8e7c27de8547e00 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Update_cron_state line=927 delta=UNCHANGED
b799630b87d1dfea severity=Low status=open rule=zizmor/anonymous-definition file=.github/workflows/chain-runner.yml step=line20 line=20 delta=UNCHANGED
bb98a38fad066e4e severity=Low status=open rule=zizmor/undocumented-permissions file=.github/workflows/chain-runner.yml step=line24 line=24 delta=UNCHANGED
080777dc05147525 severity=Low status=open rule=zizmor/concurrency-limits file=.github/workflows/fleet-runner.yml step=line4 line=4 delta=UNCHANGED
d0015b8535ebab44 severity=Low status=open rule=zizmor/anonymous-definition file=.github/workflows/fleet-runner.yml step=line44 line=44 delta=UNCHANGED
f44bdbddc0cd90a9 severity=Low status=open rule=zizmor/undocumented-permissions file=.github/workflows/fleet-runner.yml step=line48 line=48 delta=UNCHANGED
a1548a4e0e35fc1c severity=Low status=open rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=Restore_fleet_identities line=150 delta=UNCHANGED
8b5b5f84acb29e26 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=Commit_results line=315 delta=UNCHANGED
72d9c0f7f90ca88b severity=Low status=open rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=Notify line=347 delta=UNCHANGED
69ae744493f88671 severity=Low status=open rule=zizmor/anonymous-definition file=.github/workflows/messages.yml step=line47 line=47 delta=UNCHANGED
fd2cdc15893eb687 severity=Low status=open rule=zizmor/anonymous-definition file=.github/workflows/messages.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write) line=651 delta=UNCHANGED
e33522eec5a158e2 severity=Low status=open rule=zizmor/undocumented-permissions file=.github/workflows/messages.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write) line=658 delta=UNCHANGED
f2fe7efaca566e83 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/messages.yml step=Extract_message line=670 delta=UNCHANGED
729bfd27b0c29764 severity=Low status=open rule=zizmor/anonymous-definition file=.github/workflows/sync-aeon-public-results.yml step=line23 line=23 delta=UNCHANGED
948f5f1e71c64dc6 severity=Low status=open rule=zizmor/anonymous-definition file=.github/workflows/sync-upstream.yml step=line16 line=16 delta=UNCHANGED
190cbb0411df9999 severity=Low status=open rule=zizmor/undocumented-permissions file=.github/workflows/sync-upstream.yml step=line19 line=19 delta=UNCHANGED
19b5a87fc0571e02 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/sync-upstream.yml step=Push_sync_branch line=71 delta=UNCHANGED
6294f91574ffea14 severity=Low status=open rule=zizmor/template-injection file=.github/workflows/sync-upstream.yml step=Open_or_update_PR line=78 delta=UNCHANGED
-->
