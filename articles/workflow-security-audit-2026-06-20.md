# Workflow Security Audit — 2026-06-20

**Verdict:** `WORKFLOW_AUDIT_NEW_HIGH — 60 new high-severity finding(s)`
**Repo:** [swarm-ai-research/aeon](https://github.com/swarm-ai-research/aeon)
**Files audited:** 7 (7 workflows, 0 composite actions)
**Findings this run:** 150 (0 critical, 60 high, 31 medium, 59 low)
**Delta vs (no prior audit):** 150 new, 0 reintroduced, 0 unchanged, 0 resolved
**Auto-fixed:** 0
**Manual review required:** 60

> **First-run note.** No prior `articles/workflow-security-audit-*.md` exists in the repo or its git history. Every finding is labeled `NEW` by construction. The next run will deltas against this report.

## Regressions (previously-fixed findings now present again)

_None — no prior audit to regress against._

## New findings — High

The 60 high-severity findings collapse to two patterns. Each is presented as one attack chain rather than 60 near-identical entries.

### [HIGH] unpinned-uses — first-party `actions/*` referenced by mutable major tag
**Count:** 16 across 7 files
**Locations:** `aeon.yml:85` (@v5), `aeon.yml:121` (@v5), `aeon.yml:133` (@v5), `chain-runner.yml:29` (@v5), `fleet-runner.yml:52` (@v5), `fleet-runner.yml:91` (@v5), `lint.yml:33` (@v4), `lint.yml:71` (@v4), `lint.yml:74` (@v4), `lint.yml:92` (@v4), +6 more
**Pattern:**
```yaml
uses: actions/checkout@v5     # mutable — points to whatever v5.* publishes today
uses: actions/setup-node@v5   # same
uses: actions/checkout@v4     # same on v4
```

**Attack chain:**
1. **Entry:** any push, schedule, or dispatch event → all jobs check out via the unpinned tag.
2. **Vector:** GitHub re-points the `v5` tag if `actions/checkout` repo is compromised, or if a maintainer pushes a malicious commit and re-tags. The workflow grabs whatever code the tag points to *at runtime*.
3. **Sink:** the action runs inside the job with the same `permissions:` and `secrets:` as everything else in the job — including `contents: write`, `pull-requests: write`, and any auth tokens (`GH_GLOBAL`, `AEON_PRIVATE_PAT`, `CLAUDE_CODE_OAUTH_TOKEN`).
4. **Reachable secrets:** every secret referenced anywhere in the job (44 secret-references in this audit; see secrets-outside-env section).
5. **Blast radius:** full repo write (push to main, force-push, delete branches), cross-repo dispatch (chain-runner triggers other workflows), private-mirror sync (AEON_PRIVATE_PAT writes to the private aeon repo). A compromised `actions/checkout` would be a worst-case event for this repo.

**Trade-off:** SHA-pinning trades supply-chain protection for dependency drift cost (you must bump pins to get security patches). For first-party `actions/*`, the GitHub-attested supply chain is the strongest in the ecosystem — but pinning is still policy-recommended and is what zizmor's auditor persona enforces.

**Fix:** Replace each `actions/*@vN` with `actions/*@<full-40-char-sha> # vN.N.N` and bump quarterly. Renovate or Dependabot can manage the pin updates.

**Status:** Manual required — operator must select the exact commit SHA per pin; the skill does not auto-pin (matches the `Never auto-fix pinning` constraint).
### [HIGH] secrets-outside-env — secrets referenced outside a GitHub Actions Environment
**Count:** 44 across 5 files
**Files:** `messages.yml`(27), `fleet-runner.yml`(10), `chain-runner.yml`(4), `sync-upstream.yml`(2), `sync-aeon-public-results.yml`(1)
**Secrets referenced:** `AEON_PRIVATE_PAT`, `AEON_PUBLIC_PAT`, `ALCHEMY_API_KEY`, `ANTHROPIC_API_KEY`, `CLAUDE_CODE_OAUTH_TOKEN`, `COINGECKO_API_KEY`, `DISCORD_BOT_TOKEN`, `DISCORD_CHANNEL_ID`, `DISCORD_WEBHOOK_URL`, `GH_GLOBAL`, `GITLAWB_DEPLOYER_PEM`, `GITLAWB_OPERATOR_PEM`, `GITLAWB_OPERATOR_UCAN`, `GITLAWB_RESEARCHER_PEM`, `GITLAWB_REVIEWER_PEM`, `GITLAWB_SENTINEL_PEM`, `SLACK_BOT_TOKEN`, `SLACK_CHANNEL_ID`, `SLACK_WEBHOOK_URL`, `SURPLUS_API_KEY`, `SURPLUS_PRICING_URL`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `XAI_API_KEY`
**Pattern:**
```yaml
jobs:
  run:
    runs-on: ubuntu-latest
    # no `environment: prod-deploy` declaration → secret access is unscoped
    steps:
      - name: Run chain
        env:
          GH_TOKEN: ${{ secrets.GH_GLOBAL }}    # unscoped secret use
```

**Attack chain:**
1. **Entry:** every job has unrestricted access to every secret defined at the repo or org level — there is no GitHub Environment gate (`environment: production`) that would require deployment-protection rules, required reviewers, or branch restrictions before the secret is materialized in the runner.
2. **Vector:** a malicious PR (or compromised collaborator, or compromised dependency surfaced via `actions/checkout` — see unpinned-uses above) running on a non-`main` branch can still reach these secrets, because no environment-scoped protection rules apply.
3. **Sink:** the secret is written into `env:` at job-step level, where it is exfiltrable via any process the workflow spawns. Several secrets here (`AEON_PRIVATE_PAT`, `GH_GLOBAL`) carry **cross-repo** write privileges.
4. **Reachable scope:** `AEON_PRIVATE_PAT` writes to the private mirror (`aeon-private`). `GH_GLOBAL` is a fine-grained PAT covering this repo and its sibling repos. `CLAUDE_CODE_OAUTH_TOKEN` is a paying API token — exfiltration = direct billing impact.
5. **Blast radius:** in the absence of environment protections, a single supply-chain compromise or attacker-influenced workflow path discloses all five sensitive PATs. Adding `environment:` declarations is the canonical mitigation — it gates secret materialization on required reviewers, wait timers, and branch protection.

**Fix:** declare GitHub Environments in repo settings (e.g. `aeon-prod`) with required reviewer + branch restrictions, then add `environment: aeon-prod` to each job that uses these secrets. This is a repo-admin operation, not a workflow edit.

**Status:** Manual required — requires repo-settings change (create Environment, attach secrets, configure protection rules). The skill explicitly skips auto-fixing this class.


## Medium-severity findings (31 findings — compact table)

| Severity | Rule | File | Count | Sample line |
|---|---|---|---|---|
| Medium | `shellcheck` | `chain-runner.yml` | 5 | 42 |
| Medium | `shellcheck` | `fleet-runner.yml` | 4 | 143 |
| Medium | `artipacked` | `lint.yml` | 3 | 32 |
| Medium | `shellcheck-sc2129` | `messages.yml` | 3 | 640 |
| Medium | `artipacked` | `aeon.yml` | 2 | 83 |
| Medium | `shellcheck-sc2129` | `aeon.yml` | 2 | 286 |
| Medium | `shellcheck-sc2129` | `chain-runner.yml` | 2 | 42 |
| Medium | `shellcheck-sc2086` | `fleet-runner.yml` | 2 | 258 |
| Medium | `artipacked` | `messages.yml` | 2 | 48 |
| Medium | `artipacked` | `chain-runner.yml` | 1 | 28 |
| Medium | `shellcheck-sc2034` | `chain-runner.yml` | 1 | 42 |
| Medium | `artipacked` | `fleet-runner.yml` | 1 | 51 |
| Medium | `shellcheck-sc2034` | `messages.yml` | 1 | 61 |
| Medium | `artipacked` | `sync-aeon-public-results.yml` | 1 | 20 |
| Medium | `artipacked` | `sync-upstream.yml` | 1 | 22 |


## Low / Informational findings (59 findings — compact table)

| Severity | Rule | File | Count | Sample line |
|---|---|---|---|---|
| Low | `template-injection` | `aeon.yml` | 29 | 98 |
| Low | `template-injection` | `fleet-runner.yml` | 12 | 114 |
| Low | `template-injection` | `sync-upstream.yml` | 4 | 71 |
| Low | `anonymous-definition` | `messages.yml` | 2 | 39 |
| Low | `anonymous-definition` | `aeon.yml` | 1 | 72 |
| Low | `undocumented-permissions` | `aeon.yml` | 1 | 77 |
| Low | `anonymous-definition` | `chain-runner.yml` | 1 | 20 |
| Low | `undocumented-permissions` | `chain-runner.yml` | 1 | 24 |
| Low | `concurrency-limits` | `fleet-runner.yml` | 1 | 4 |
| Low | `anonymous-definition` | `fleet-runner.yml` | 1 | 39 |
| Low | `undocumented-permissions` | `fleet-runner.yml` | 1 | 43 |
| Low | `undocumented-permissions` | `messages.yml` | 1 | 629 |
| Low | `template-injection` | `messages.yml` | 1 | 641 |
| Low | `anonymous-definition` | `sync-aeon-public-results.yml` | 1 | 15 |
| Low | `anonymous-definition` | `sync-upstream.yml` | 1 | 16 |
| Low | `undocumented-permissions` | `sync-upstream.yml` | 1 | 19 |

## Carried over (unchanged)

_None — first run._

## Resolved since prior audit

_None — first run._

## Hand-rolled supplemental checks

| Check | Result |
|---|---|
| `toJson(github.event.*)` piped to shell (April 11 pattern) | clean — `messages.yml:659` already uses `env: _CLIENT_PAYLOAD_MESSAGE` → `printf '%s' "$_CLIENT_PAYLOAD_MESSAGE"` |
| `persist-credentials: true` on PR-ref checkout | clean — no `persist-credentials: true` present; no `pull_request_target`/`workflow_run` triggers |
| `GITHUB_ENV` write with `${{ github.event.* }}` interpolation | clean — only static literals (`CHAIN_STATUS=failed`) written |
| Fleet `inputs.*` flowing into `gh workflow run` / `gh api` / `run:` shell | clean — `chain-runner.yml` and `fleet-runner.yml` use `env:` indirection for all `inputs.*` references |
| Mutable ref on third-party action | clean — every `uses:` is first-party `actions/*` |

## Source status

- zizmor: `ok` (v1.25.2, persona=auditor) — 130 findings across 7 workflows
- actionlint: `ok` — 20 shellcheck findings (all style; none touch `${{ github.* }}` interpolations)
- hand-rolled: `ok` — 5 checks, 0 findings
- **Filename reconciliation:** the SARIF scan ran against `sync-aeon-public.yml`; that file has since been renamed to `sync-aeon-public-results.yml` (same content, same patterns). Findings retagged to the current filename. The bash sandbox blocked rerunning zizmor with `--output` in this session; the existing scan artifacts from earlier in the same session were used.

<!--
workflow-security-audit-fingerprints
d3907f45f6189608 severity=High status=manual rule=unpinned-uses file=aeon.yml step=Early_checkout
8bc6d7f0ee4b41a4 severity=High status=manual rule=unpinned-uses file=aeon.yml step=Checkout_repo
2ed6a792272eb549 severity=High status=manual rule=unpinned-uses file=aeon.yml step=Setup_Node.js
d27794f885186fe9 severity=High status=manual rule=unpinned-uses file=chain-runner.yml step=Checkout_repo
792242570d8a6618 severity=High status=manual rule=secrets-outside-env file=chain-runner.yml step=Checkout_repo
355b824312f526a9 severity=High status=manual rule=secrets-outside-env file=chain-runner.yml step=Run_chain
8bafa9d71dea2830 severity=High status=manual rule=secrets-outside-env file=chain-runner.yml step=Update_cron_state
019f18f17d22ce5b severity=High status=manual rule=secrets-outside-env file=chain-runner.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
1a087c3833e8896a severity=High status=manual rule=unpinned-uses file=fleet-runner.yml step=Checkout
2401298b436b7408 severity=High status=manual rule=unpinned-uses file=fleet-runner.yml step=Setup_Node.js
d6c34d9c83f82f95 severity=High status=manual rule=secrets-outside-env file=fleet-runner.yml step=Restore_fleet_identities
d6c34d9c83f82f95 severity=High status=manual rule=secrets-outside-env file=fleet-runner.yml step=Restore_fleet_identities
d6c34d9c83f82f95 severity=High status=manual rule=secrets-outside-env file=fleet-runner.yml step=Restore_fleet_identities
d6c34d9c83f82f95 severity=High status=manual rule=secrets-outside-env file=fleet-runner.yml step=Restore_fleet_identities
d6c34d9c83f82f95 severity=High status=manual rule=secrets-outside-env file=fleet-runner.yml step=Restore_fleet_identities
d6c34d9c83f82f95 severity=High status=manual rule=secrets-outside-env file=fleet-runner.yml step=Restore_fleet_identities
b1242a30b0ad41b5 severity=High status=manual rule=secrets-outside-env file=fleet-runner.yml step=Prefetch_live_Surplus_prices_(best-effort,_outside_sandbox)
b1242a30b0ad41b5 severity=High status=manual rule=secrets-outside-env file=fleet-runner.yml step=Prefetch_live_Surplus_prices_(best-effort,_outside_sandbox)
8d327086b39f0fde severity=High status=manual rule=secrets-outside-env file=fleet-runner.yml step=Run_fleet_task_runner
e97c702db28a09cb severity=High status=manual rule=secrets-outside-env file=fleet-runner.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
7406a69667bfcbf0 severity=High status=manual rule=unpinned-uses file=lint.yml step=Checkout
7406a69667bfcbf0 severity=High status=manual rule=unpinned-uses file=lint.yml step=Checkout
e0975afa1b7758b8 severity=High status=manual rule=unpinned-uses file=lint.yml step=Setup_Node
7406a69667bfcbf0 severity=High status=manual rule=unpinned-uses file=lint.yml step=Checkout
e0975afa1b7758b8 severity=High status=manual rule=unpinned-uses file=lint.yml step=Setup_Node
6047346229d43326 severity=High status=manual rule=unpinned-uses file=messages.yml step=Checkout_repo
357fdd8a3af7f776 severity=High status=manual rule=secrets-outside-env file=messages.yml step=Checkout_repo
63354f207301a00b severity=High status=manual rule=secrets-outside-env file=messages.yml step=Determine_and_dispatch_scheduled_skills
cfabd267ca00a3db severity=High status=manual rule=secrets-outside-env file=messages.yml step=Collect_and_dispatch_messages
cfabd267ca00a3db severity=High status=manual rule=secrets-outside-env file=messages.yml step=Collect_and_dispatch_messages
cfabd267ca00a3db severity=High status=manual rule=secrets-outside-env file=messages.yml step=Collect_and_dispatch_messages
cfabd267ca00a3db severity=High status=manual rule=secrets-outside-env file=messages.yml step=Collect_and_dispatch_messages
cfabd267ca00a3db severity=High status=manual rule=secrets-outside-env file=messages.yml step=Collect_and_dispatch_messages
cfabd267ca00a3db severity=High status=manual rule=secrets-outside-env file=messages.yml step=Collect_and_dispatch_messages
cfabd267ca00a3db severity=High status=manual rule=secrets-outside-env file=messages.yml step=Collect_and_dispatch_messages
9db6a9b1de97282b severity=High status=manual rule=secrets-outside-env file=messages.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
6047346229d43326 severity=High status=manual rule=unpinned-uses file=messages.yml step=Checkout_repo
357fdd8a3af7f776 severity=High status=manual rule=secrets-outside-env file=messages.yml step=Checkout_repo
329d75c7d3db86c6 severity=High status=manual rule=unpinned-uses file=messages.yml step=Setup_Node.js
d4cbd1efaee90fef severity=High status=manual rule=secrets-outside-env file=messages.yml step=Run
d4cbd1efaee90fef severity=High status=manual rule=secrets-outside-env file=messages.yml step=Run
d4cbd1efaee90fef severity=High status=manual rule=secrets-outside-env file=messages.yml step=Run
d4cbd1efaee90fef severity=High status=manual rule=secrets-outside-env file=messages.yml step=Run
d4cbd1efaee90fef severity=High status=manual rule=secrets-outside-env file=messages.yml step=Run
d4cbd1efaee90fef severity=High status=manual rule=secrets-outside-env file=messages.yml step=Run
d4cbd1efaee90fef severity=High status=manual rule=secrets-outside-env file=messages.yml step=Run
d4cbd1efaee90fef severity=High status=manual rule=secrets-outside-env file=messages.yml step=Run
d4cbd1efaee90fef severity=High status=manual rule=secrets-outside-env file=messages.yml step=Run
d4cbd1efaee90fef severity=High status=manual rule=secrets-outside-env file=messages.yml step=Run
d4cbd1efaee90fef severity=High status=manual rule=secrets-outside-env file=messages.yml step=Run
d4cbd1efaee90fef severity=High status=manual rule=secrets-outside-env file=messages.yml step=Run
d4cbd1efaee90fef severity=High status=manual rule=secrets-outside-env file=messages.yml step=Run
d4cbd1efaee90fef severity=High status=manual rule=secrets-outside-env file=messages.yml step=Run
d4cbd1efaee90fef severity=High status=manual rule=secrets-outside-env file=messages.yml step=Run
9db6a9b1de97282b severity=High status=manual rule=secrets-outside-env file=messages.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
cf24a1f20068db16 severity=High status=manual rule=unpinned-uses file=sync-aeon-public-results.yml step=Checkout_aeon
ef8ca6ec06ac8aa5 severity=High status=manual rule=secrets-outside-env file=sync-aeon-public-results.yml step=Publish_sanitized_snapshot
7b14223863ca97b6 severity=High status=manual rule=unpinned-uses file=sync-upstream.yml step=Checkout_fork
e66aadf11f98b234 severity=High status=manual rule=secrets-outside-env file=sync-upstream.yml step=Checkout_fork
488f40a651ebedb8 severity=High status=manual rule=secrets-outside-env file=sync-upstream.yml step=Open_or_update_PR
1cdbc33b7e995daf severity=Medium status=open rule=artipacked file=aeon.yml step=Early_checkout
757f69e65b14d25e severity=Medium status=open rule=artipacked file=aeon.yml step=Checkout_repo
6f9e2fb0f04c8fd7 severity=Medium status=open rule=shellcheck-sc2129 file=aeon.yml step=(shell_script)
ae00f76cad452d85 severity=Medium status=open rule=shellcheck-sc2129 file=aeon.yml step=(shell_script)
a8e765b84ac107a8 severity=Medium status=open rule=artipacked file=chain-runner.yml step=Checkout_repo
4a7f1c29db32cfa3 severity=Medium status=open rule=shellcheck-sc2034 file=chain-runner.yml step=(shell_script)
134e72fc4b17acd1 severity=Medium status=open rule=shellcheck-sc2129 file=chain-runner.yml step=(shell_script)
995d981bcf4b69ab severity=Medium status=open rule=shellcheck-sc2129 file=chain-runner.yml step=(shell_script)
507a42d694fe654e severity=Medium status=open rule=shellcheck file=chain-runner.yml step=(shell_script)
410112011cab2692 severity=Medium status=open rule=shellcheck file=chain-runner.yml step=(shell_script)
03b6be1aa45b8db2 severity=Medium status=open rule=shellcheck file=chain-runner.yml step=(shell_script)
e2ead0de1bd9602d severity=Medium status=open rule=shellcheck file=chain-runner.yml step=(shell_script)
1d1bf6bd68771448 severity=Medium status=open rule=shellcheck file=chain-runner.yml step=(shell_script)
2a79f323d9a63f74 severity=Medium status=open rule=artipacked file=fleet-runner.yml step=Checkout
551203b0a4c65754 severity=Medium status=open rule=shellcheck file=fleet-runner.yml step=(shell_script)
87e6f5a29a54048b severity=Medium status=open rule=shellcheck file=fleet-runner.yml step=(shell_script)
890a7418fc05d712 severity=Medium status=open rule=shellcheck file=fleet-runner.yml step=(shell_script)
47ee1e744deaf0ce severity=Medium status=open rule=shellcheck file=fleet-runner.yml step=(shell_script)
712345bb2b80b893 severity=Medium status=open rule=shellcheck-sc2086 file=fleet-runner.yml step=(shell_script)
9d4013662cadad27 severity=Medium status=open rule=shellcheck-sc2086 file=fleet-runner.yml step=(shell_script)
aa128effe69bbc8d severity=Medium status=open rule=artipacked file=lint.yml step=Checkout
aa128effe69bbc8d severity=Medium status=open rule=artipacked file=lint.yml step=Checkout
aa128effe69bbc8d severity=Medium status=open rule=artipacked file=lint.yml step=Checkout
4520651bd0d7a0e1 severity=Medium status=open rule=artipacked file=messages.yml step=Checkout_repo
892a1c47429438de severity=Medium status=open rule=shellcheck-sc2034 file=messages.yml step=(shell_script)
c5b426b1bb0604ee severity=Medium status=open rule=shellcheck-sc2129 file=messages.yml step=(shell_script)
4520651bd0d7a0e1 severity=Medium status=open rule=artipacked file=messages.yml step=Checkout_repo
e7cd634c8012e631 severity=Medium status=open rule=shellcheck-sc2129 file=messages.yml step=(shell_script)
265a33368d9c4b60 severity=Medium status=open rule=shellcheck-sc2129 file=messages.yml step=(shell_script)
ebbe4d9a5d1bf725 severity=Medium status=open rule=artipacked file=sync-aeon-public-results.yml step=Checkout_aeon
367766388fe88330 severity=Medium status=open rule=artipacked file=sync-upstream.yml step=Checkout_fork
3e6464dac6af20ba severity=Low status=open rule=anonymous-definition file=aeon.yml step=top
5632f7b10e1f7d9f severity=Low status=open rule=undocumented-permissions file=aeon.yml step=top
289b7cfa1e254aa0 severity=Low status=open rule=template-injection file=aeon.yml step=Determine_skill
289b7cfa1e254aa0 severity=Low status=open rule=template-injection file=aeon.yml step=Determine_skill
289b7cfa1e254aa0 severity=Low status=open rule=template-injection file=aeon.yml step=Determine_skill
7bb7d48f4fdfc978 severity=Low status=open rule=template-injection file=aeon.yml step=Check_if_there's_work
7bb7d48f4fdfc978 severity=Low status=open rule=template-injection file=aeon.yml step=Check_if_there's_work
7a9a7fd87154afca severity=Low status=open rule=template-injection file=aeon.yml step=Validate_skill_secrets
a382ed1a63a2e2fe severity=Low status=open rule=template-injection file=aeon.yml step=Run_pre-fetch_scripts
c08760c972a36f1e severity=Low status=open rule=template-injection file=aeon.yml step=Run
c08760c972a36f1e severity=Low status=open rule=template-injection file=aeon.yml step=Run
b20c05722eaf6911 severity=Low status=open rule=template-injection file=aeon.yml step=Log_token_usage
b20c05722eaf6911 severity=Low status=open rule=template-injection file=aeon.yml step=Log_token_usage
b20c05722eaf6911 severity=Low status=open rule=template-injection file=aeon.yml step=Log_token_usage
b20c05722eaf6911 severity=Low status=open rule=template-injection file=aeon.yml step=Log_token_usage
b20c05722eaf6911 severity=Low status=open rule=template-injection file=aeon.yml step=Log_token_usage
b20c05722eaf6911 severity=Low status=open rule=template-injection file=aeon.yml step=Log_token_usage
fe5d9a0590165600 severity=Low status=open rule=template-injection file=aeon.yml step=Track_token_costs
fe5d9a0590165600 severity=Low status=open rule=template-injection file=aeon.yml step=Track_token_costs
fe5d9a0590165600 severity=Low status=open rule=template-injection file=aeon.yml step=Track_token_costs
fe5d9a0590165600 severity=Low status=open rule=template-injection file=aeon.yml step=Track_token_costs
fe5d9a0590165600 severity=Low status=open rule=template-injection file=aeon.yml step=Track_token_costs
fe5d9a0590165600 severity=Low status=open rule=template-injection file=aeon.yml step=Track_token_costs
34aa0bbfc1cdd541 severity=Low status=open rule=template-injection file=aeon.yml step=Capture_skill_output
36cd4e7eefca3d46 severity=Low status=open rule=template-injection file=aeon.yml step=Analyze_skill_output
36cd4e7eefca3d46 severity=Low status=open rule=template-injection file=aeon.yml step=Analyze_skill_output
095ea9341af2fc85 severity=Low status=open rule=template-injection file=aeon.yml step=Convert_feed_outputs
25ca22063319b2c7 severity=Low status=open rule=template-injection file=aeon.yml step=Commit_results
dafcbe7f45b400b8 severity=Low status=open rule=template-injection file=aeon.yml step=Update_cron_state
dafcbe7f45b400b8 severity=Low status=open rule=template-injection file=aeon.yml step=Update_cron_state
dafcbe7f45b400b8 severity=Low status=open rule=template-injection file=aeon.yml step=Update_cron_state
3588bc7eb68ce5d1 severity=Low status=open rule=anonymous-definition file=chain-runner.yml step=top
36efedce2105e4f9 severity=Low status=open rule=undocumented-permissions file=chain-runner.yml step=top
0ae5997526ae9384 severity=Low status=open rule=concurrency-limits file=fleet-runner.yml step=top
14d07e61e7bdde27 severity=Low status=open rule=anonymous-definition file=fleet-runner.yml step=top
9a056ab4884beed2 severity=Low status=open rule=undocumented-permissions file=fleet-runner.yml step=top
73fd9cfd551f9aa4 severity=Low status=open rule=template-injection file=fleet-runner.yml step=Restore_fleet_identities
73fd9cfd551f9aa4 severity=Low status=open rule=template-injection file=fleet-runner.yml step=Restore_fleet_identities
73fd9cfd551f9aa4 severity=Low status=open rule=template-injection file=fleet-runner.yml step=Restore_fleet_identities
73fd9cfd551f9aa4 severity=Low status=open rule=template-injection file=fleet-runner.yml step=Restore_fleet_identities
73fd9cfd551f9aa4 severity=Low status=open rule=template-injection file=fleet-runner.yml step=Restore_fleet_identities
73fd9cfd551f9aa4 severity=Low status=open rule=template-injection file=fleet-runner.yml step=Restore_fleet_identities
893def3ad37510de severity=Low status=open rule=template-injection file=fleet-runner.yml step=Commit_results
893def3ad37510de severity=Low status=open rule=template-injection file=fleet-runner.yml step=Commit_results
893def3ad37510de severity=Low status=open rule=template-injection file=fleet-runner.yml step=Commit_results
893def3ad37510de severity=Low status=open rule=template-injection file=fleet-runner.yml step=Commit_results
9dd1c45c0e0ee1e8 severity=Low status=open rule=template-injection file=fleet-runner.yml step=Notify
9dd1c45c0e0ee1e8 severity=Low status=open rule=template-injection file=fleet-runner.yml step=Notify
b8c4a95fde0a6bbc severity=Low status=open rule=anonymous-definition file=messages.yml step=top
895977a317fc6706 severity=Low status=open rule=anonymous-definition file=messages.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
dee7bbcfe5931e55 severity=Low status=open rule=undocumented-permissions file=messages.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
e90f3a89af5dd1b2 severity=Low status=open rule=template-injection file=messages.yml step=Extract_message
4174b82adab0f5b1 severity=Low status=open rule=anonymous-definition file=sync-aeon-public-results.yml step=top
6541abac62c312ea severity=Low status=open rule=anonymous-definition file=sync-upstream.yml step=top
589e836b45a7238a severity=Low status=open rule=undocumented-permissions file=sync-upstream.yml step=top
73123a22b3b6174b severity=Low status=open rule=template-injection file=sync-upstream.yml step=Push_sync_branch
75e9a1ea0531b235 severity=Low status=open rule=template-injection file=sync-upstream.yml step=Open_or_update_PR
75e9a1ea0531b235 severity=Low status=open rule=template-injection file=sync-upstream.yml step=Open_or_update_PR
75e9a1ea0531b235 severity=Low status=open rule=template-injection file=sync-upstream.yml step=Open_or_update_PR
-->
