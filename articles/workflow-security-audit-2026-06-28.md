# Workflow Security Audit — 2026-06-28

**Verdict:** WORKFLOW_AUDIT_NEW_CRITICAL — 16 new critical finding(s)
**Repo:** [swarm-ai-research/aeon](https://github.com/swarm-ai-research/aeon)
**Files audited:** 7 (7 workflows, 0 composite actions)
**Findings this run:** 100 (16 critical, 36 high, 17 medium, 31 low)
**Delta vs (no prior audit):** 100 new, 0 reintroduced, 0 unchanged, 0 resolved
**Auto-fixed:** 0

## Regressions (previously-fixed findings now present again)

_None — no prior audit to compare against._

## New findings

### Critical and High — 52 finding(s) with attack-chain narratives

#### [CRITICAL] unpinned-uses — Action referenced by mutable tag, not SHA (16 occurrence(s))

**Attack chain (applies to all occurrences in this group):**
1. **Entry:** workflow `aeon.yml` is triggered by workflow_dispatch, workflow_call, issues — any update to the upstream tag is silently consumed on next run
2. **Vector:** `actions/checkout@v5` resolves at runtime to whatever commit the tag currently points to; the tag owner can rewrite history
3. **Sink:** action code executes inside the job with the job's `GITHUB_TOKEN`, `env:` block, and file-system access
4. **Reachable secrets:** secrets.AEON_PRIVATE_PAT, secrets.ALCHEMY_API_KEY, secrets.ANTHROPIC_API_KEY, secrets.BANKR_API_KEY, secrets.BANKR_LLM_KEY, secrets.CLAUDE_CODE_OAUTH_TOKEN, secrets.COINGECKO_API_KEY, secrets.DEVTO_API_KEY, secrets.DISCORD_BOT_TOKEN, secrets.DISCORD_CHANNEL_ID, secrets.DISCORD_WEBHOOK_URL, secrets.FLEET_ENDPOINT, secrets.FLEET_TOKEN, secrets.GH_GLOBAL, secrets.GITHUB_TOKEN, secrets.NEYNAR_API_KEY, secrets.NEYNAR_SIGNER_UUID, secrets.NOTIFY_EMAIL_TO, secrets.REPLICATE_API_TOKEN, secrets.RUNPOD_API_KEY, secrets.SENDGRID_API_KEY, secrets.SLACK_BOT_TOKEN, secrets.SLACK_CHANNEL_ID, secrets.SLACK_WEBHOOK_URL, secrets.SUPERNOTES_API_KEY, secrets.SURPLUS_API_KEY, secrets.SURPLUS_PRICING_URL, secrets.TELEGRAM_BOT_TOKEN, secrets.TELEGRAM_CHAT_ID, secrets.VERCEL_TOKEN, secrets.XAI_API_KEY
5. **Blast radius:** with `permissions: {}` the malicious action can still exfiltrate any env-scoped secret (FLEET_TOKEN, GH_GLOBAL, etc.) regardless of permissions

**Occurrences:**

| File | Line | Step | Pattern |
|---|---|---|---|
| `.github/workflows/aeon.yml` | 85 | (job-level) | `actions/checkout@v5` |
| `.github/workflows/aeon.yml` | 121 | (job-level) | `actions/checkout@v5` |
| `.github/workflows/aeon.yml` | 133 | (job-level) | `actions/setup-node@v5` |
| `.github/workflows/chain-runner.yml` | 29 | (job-level) | `actions/checkout@v5` |
| `.github/workflows/fleet-runner.yml` | 52 | (job-level) | `actions/checkout@v5` |
| `.github/workflows/fleet-runner.yml` | 91 | (job-level) | `actions/setup-node@v5` |
| `.github/workflows/lint.yml` | 33 | (job-level) | `actions/checkout@v4` |
| `.github/workflows/lint.yml` | 71 | (job-level) | `actions/checkout@v4` |
| `.github/workflows/lint.yml` | 74 | (job-level) | `actions/setup-node@v4` |
| `.github/workflows/lint.yml` | 92 | (job-level) | `actions/checkout@v4` |
| `.github/workflows/lint.yml` | 95 | (job-level) | `actions/setup-node@v4` |
| `.github/workflows/messages.yml` | 49 | (job-level) | `actions/checkout@v5` |
| `.github/workflows/messages.yml` | 685 | (job-level) | `actions/checkout@v5` |
| `.github/workflows/messages.yml` | 697 | (job-level) | `actions/setup-node@v5` |
| `.github/workflows/sync-aeon-public-results.yml` | 29 | (job-level) | `actions/checkout@v4` |
| `.github/workflows/sync-upstream.yml` | 23 | (job-level) | `actions/checkout@v4` |

**Fix (manual — never auto-applied per skill constraint):** pin each `uses:` to a 40-char commit SHA, with a comment for the tag it points to. Example:
```yaml
# BEFORE
- uses: actions/checkout@v5
# AFTER
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v5.0.0
```
Use `gh api repos/{owner}/{repo}/git/refs/tags/{tag}` to resolve the SHA; verify the commit's signed by the action owner before pinning.

**Status:** Manual review required

---

#### [HIGH] secrets-outside-env — Secret accessed outside dedicated environment (36 occurrence(s))

**Attack chain (applies to all occurrences in this group):**
1. **Entry:** workflow `chain-runner.yml` triggered by workflow_dispatch
2. **Vector:** secret `secrets.GH_GLOBAL` is wired into `env:` at the job (or step) level, not behind a deployment `environment:` gate
3. **Sink:** every step in the job — including pre-existing untrusted-content steps and any newly added `run:` block — can read the secret via process env
4. **Reachable secrets:** secrets.AEON_PRIVATE_PAT, secrets.GH_GLOBAL, secrets.GITHUB_TOKEN
5. **Blast radius:** if any step is later trivially compromised (template injection, dependency takeover, malicious skill), the secret can be exfiltrated without further escalation

**Occurrences:**

| File | Line | Step | Pattern |
|---|---|---|---|
| `.github/workflows/chain-runner.yml` | 31 | (job-level) | `secrets.GH_GLOBAL` |
| `.github/workflows/chain-runner.yml` | 347 | (job-level) | `secrets.AEON_PRIVATE_PAT` |
| `.github/workflows/fleet-runner.yml` | 145 | (job-level) | `secrets.GITLAWB_OPERATOR_PEM` |
| `.github/workflows/fleet-runner.yml` | 146 | (job-level) | `secrets.GITLAWB_OPERATOR_UCAN` |
| `.github/workflows/fleet-runner.yml` | 148 | (job-level) | `secrets.GITLAWB_RESEARCHER_PEM` |
| `.github/workflows/fleet-runner.yml` | 149 | (job-level) | `secrets.GITLAWB_REVIEWER_PEM` |
| `.github/workflows/fleet-runner.yml` | 150 | (job-level) | `secrets.GITLAWB_DEPLOYER_PEM` |
| `.github/workflows/fleet-runner.yml` | 151 | (job-level) | `secrets.GITLAWB_SENTINEL_PEM` |
| `.github/workflows/fleet-runner.yml` | 266 | (job-level) | `secrets.SURPLUS_PRICING_URL` |
| `.github/workflows/fleet-runner.yml` | 267 | (job-level) | `secrets.SURPLUS_API_KEY` |
| `.github/workflows/fleet-runner.yml` | 282 | (job-level) | `secrets.CLAUDE_CODE_OAUTH_TOKEN` |
| `.github/workflows/fleet-runner.yml` | 349 | (job-level) | `secrets.AEON_PRIVATE_PAT` |
| `.github/workflows/messages.yml` | 51 | (job-level) | `secrets.GH_GLOBAL` |
| `.github/workflows/messages.yml` | 544 | (job-level) | `secrets.TELEGRAM_BOT_TOKEN` |
| `.github/workflows/messages.yml` | 545 | (job-level) | `secrets.TELEGRAM_CHAT_ID` |
| `.github/workflows/messages.yml` | 546 | (job-level) | `secrets.DISCORD_BOT_TOKEN` |
| `.github/workflows/messages.yml` | 547 | (job-level) | `secrets.DISCORD_CHANNEL_ID` |
| `.github/workflows/messages.yml` | 548 | (job-level) | `secrets.SLACK_BOT_TOKEN` |
| `.github/workflows/messages.yml` | 549 | (job-level) | `secrets.SLACK_CHANNEL_ID` |
| `.github/workflows/messages.yml` | 640 | (job-level) | `secrets.AEON_PRIVATE_PAT` |
| `.github/workflows/messages.yml` | 687 | (job-level) | `secrets.GH_GLOBAL` |
| `.github/workflows/messages.yml` | 709 | (job-level) | `secrets.ANTHROPIC_API_KEY` |
| `.github/workflows/messages.yml` | 710 | (job-level) | `secrets.CLAUDE_CODE_OAUTH_TOKEN` |
| `.github/workflows/messages.yml` | 713 | (job-level) | `secrets.TELEGRAM_BOT_TOKEN` |
| `.github/workflows/messages.yml` | 714 | (job-level) | `secrets.TELEGRAM_CHAT_ID` |
| `.github/workflows/messages.yml` | 715 | (job-level) | `secrets.DISCORD_BOT_TOKEN` |
| `.github/workflows/messages.yml` | 716 | (job-level) | `secrets.DISCORD_CHANNEL_ID` |
| `.github/workflows/messages.yml` | 717 | (job-level) | `secrets.DISCORD_WEBHOOK_URL` |
| `.github/workflows/messages.yml` | 718 | (job-level) | `secrets.SLACK_BOT_TOKEN` |
| `.github/workflows/messages.yml` | 719 | (job-level) | `secrets.SLACK_CHANNEL_ID` |
| `.github/workflows/messages.yml` | 720 | (job-level) | `secrets.SLACK_WEBHOOK_URL` |
| `.github/workflows/messages.yml` | 721 | (job-level) | `secrets.XAI_API_KEY` |
| `.github/workflows/messages.yml` | 722 | (job-level) | `secrets.COINGECKO_API_KEY` |
| `.github/workflows/messages.yml` | 723 | (job-level) | `secrets.ALCHEMY_API_KEY` |
| `.github/workflows/messages.yml` | 881 | (job-level) | `secrets.AEON_PRIVATE_PAT` |
| `.github/workflows/sync-upstream.yml` | 29 | (job-level) | `secrets.GH_GLOBAL` |

**Fix (manual):** move secrets into a deployment `environment:` block so they're only mountable when the workflow run targets that environment, and so audit logs distinguish prod-secret access from dev:
```yaml
jobs:
  run:
    environment: prod          # secrets gated behind protection rules
    env:
      MY_KEY: ${{ secrets.MY_KEY }}
```
For workflows where an `environment:` is overkill, push the `env:` declaration down from job level to the single step that actually needs it.

**Status:** Manual review required

---

### Medium and Low — compact summary

| Severity | Rule | File | Line | Pattern |
|---|---|---|---|---|
| Medium | `artipacked` | `.github/workflows/aeon.yml` | 83 | `name: Early checkout` |
| Medium | `artipacked` | `.github/workflows/aeon.yml` | 119 | `name: Checkout repo` |
| Medium | `actionlint-shellcheck` | `.github/workflows/aeon.yml` | 286 | `shellcheck reported issue in this script: SC2129:style:259:1: Consider using { c` |
| Medium | `actionlint-shellcheck` | `.github/workflows/aeon.yml` | 601 | `shellcheck reported issue in this script: SC2129:style:7:1: Consider using { cmd` |
| Medium | `artipacked` | `.github/workflows/chain-runner.yml` | 28 | `name: Checkout repo` |
| Medium | `actionlint-shellcheck` | `.github/workflows/chain-runner.yml` | 42 | `shellcheck reported issue in this script: SC2034:warning:3:1: NOW_ISO appears un` |
| Medium | `artipacked` | `.github/workflows/fleet-runner.yml` | 51 | `name: Checkout` |
| Medium | `actionlint-shellcheck` | `.github/workflows/fleet-runner.yml` | 174 | `shellcheck reported issue in this script: SC2155:warning:2:8: Declare and assign` |
| Medium | `actionlint-shellcheck` | `.github/workflows/fleet-runner.yml` | 289 | `shellcheck reported issue in this script: SC2086:info:6:82: Double quote to prev` |
| Medium | `artipacked` | `.github/workflows/lint.yml` | 32 | `name: Checkout` |
| Medium | `artipacked` | `.github/workflows/messages.yml` | 48 | `name: Checkout repo` |
| Medium | `actionlint-shellcheck` | `.github/workflows/messages.yml` | 61 | `shellcheck reported issue in this script: SC2034:warning:247:5: IN_STEPS appears` |
| Medium | `actionlint-shellcheck` | `.github/workflows/messages.yml` | 661 | `shellcheck reported issue in this script: SC2129:style:16:3: Consider using { cm` |
| Medium | `actionlint-shellcheck` | `.github/workflows/messages.yml` | 726 | `shellcheck reported issue in this script: SC2129:style:64:1: Consider using { cm` |
| Medium | `actionlint-shellcheck` | `.github/workflows/messages.yml` | 807 | `shellcheck reported issue in this script: SC2129:style:7:1: Consider using { cmd` |
| Medium | `artipacked` | `.github/workflows/sync-aeon-public-results.yml` | 28 | `name: Checkout aeon` |
| Medium | `artipacked` | `.github/workflows/sync-upstream.yml` | 22 | `name: Checkout fork` |
| Low | `anonymous-definition` | `.github/workflows/aeon.yml` | 72 | `run` |
| Low | `undocumented-permissions` | `.github/workflows/aeon.yml` | 77 | `      contents: write` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 98 | `\|` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 112 | `\|` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 150 | `\|` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 194 | `\|` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 288 | `\|` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 602 | `\|` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 625 | `\|` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 630 | `\|` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 651 | `\|` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 752 | `\|` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 863 | `\|` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 927 | `\|` |
| Low | `anonymous-definition` | `.github/workflows/chain-runner.yml` | 20 | `run` |
| Low | `undocumented-permissions` | `.github/workflows/chain-runner.yml` | 24 | `      contents: write` |
| Low | `concurrency-limits` | `.github/workflows/fleet-runner.yml` | 4 | `on:` |
| Low | `anonymous-definition` | `.github/workflows/fleet-runner.yml` | 39 | `run` |
| Low | `undocumented-permissions` | `.github/workflows/fleet-runner.yml` | 43 | `      contents: write` |
| Low | `template-injection` | `.github/workflows/fleet-runner.yml` | 145 | `\|` |
| Low | `template-injection` | `.github/workflows/fleet-runner.yml` | 310 | `\|` |
| Low | `template-injection` | `.github/workflows/fleet-runner.yml` | 342 | `\|` |
| Low | `anonymous-definition` | `.github/workflows/messages.yml` | 39 | `tick` |
| Low | `anonymous-definition` | `.github/workflows/messages.yml` | 643 | `run` |
| Low | `undocumented-permissions` | `.github/workflows/messages.yml` | 650 | `      issues: read` |
| Low | `template-injection` | `.github/workflows/messages.yml` | 662 | `\|` |
| Low | `anonymous-definition` | `.github/workflows/sync-aeon-public-results.yml` | 23 | `sync` |
| Low | `anonymous-definition` | `.github/workflows/sync-upstream.yml` | 16 | `sync` |
| Low | `undocumented-permissions` | `.github/workflows/sync-upstream.yml` | 19 | `      contents: write` |
| Low | `template-injection` | `.github/workflows/sync-upstream.yml` | 71 | `git push origin "${{ steps.merge.outputs.branch }}"` |
| Low | `template-injection` | `.github/workflows/sync-upstream.yml` | 78 | `\|` |

## Carried over (unchanged)

_None — no prior audit to compare against._

## Resolved since (no prior audit)

_N/A — first audit run._

## Source status

- zizmor: ok (1.25.2, persona=auditor)
- actionlint: ok (1.7.12)
- hand-rolled: ok (toJson-into-shell, poisoned-pipeline, GITHUB_ENV-write, gh-dispatch, third-party-pin checks all ran — no findings)

## Notes

- All 16 `unpinned-uses` Critical findings are first-party (`actions/checkout`, `actions/setup-node`) using major-version tags (`@v4`, `@v5`). zizmor's `auditor` persona enforces a blanket SHA-pin policy regardless of trust tier. Operator judgment required: keep tags for ergonomics + GitHub's verified-org tier, or pin to SHAs and accept the maintenance overhead. The skill explicitly lists this rule as never-auto-fix.
- All 36 `secrets-outside-env` High findings are the same shape — secrets wired into the job-level `env:` block rather than gated behind a `environment:` deployment. The repo currently has no GitHub Environments configured; resolving these would require introducing one (e.g. `prod`) with protection rules.
- The previously-flagged `toJson(github.event.client_payload.message)` shell-injection pattern in `messages.yml` is now fixed in-place (line 659: routed through `_CLIENT_PAYLOAD_MESSAGE` env then `printf '%s' "$_CLIENT_PAYLOAD_MESSAGE" | jq -r '.'`). Hand-rolled check confirms no regressions.
- `lint.yml` runs on the `pull_request` trigger and executes `npm install` (line 79) against the PR's `package.json` — preinstall scripts from an attacker fork can run, but the job has `permissions: contents: read` and references no secrets, so blast radius is confined to the runner.

<!--
workflow-security-audit-fingerprints
a20b5e834f8f425c severity=Critical status=manual rule=unpinned-uses file=.github/workflows/aeon.yml step=jobs/run/steps/[0]/uses_actions/checkout@v5
dca2f84dbf9fb2d8 severity=Critical status=manual rule=unpinned-uses file=.github/workflows/aeon.yml step=jobs/run/steps/[3]/uses_actions/checkout@v5
bd7656d9e1fad40f severity=Critical status=manual rule=unpinned-uses file=.github/workflows/aeon.yml step=jobs/run/steps/[5]/uses_actions/setup-node@v5
f146d5d506c3bfd7 severity=Critical status=manual rule=unpinned-uses file=.github/workflows/chain-runner.yml step=jobs/run/steps/[0]/uses_actions/checkout@v5
f1fc94a8f8a884b1 severity=Critical status=manual rule=unpinned-uses file=.github/workflows/fleet-runner.yml step=jobs/run/steps/[0]/uses_actions/checkout@v5
8c2f59e43b009c59 severity=Critical status=manual rule=unpinned-uses file=.github/workflows/fleet-runner.yml step=jobs/run/steps/[3]/uses_actions/setup-node@v5
a1e19b5a4ac947dc severity=Critical status=manual rule=unpinned-uses file=.github/workflows/lint.yml step=jobs/shellcheck/steps/[0]/uses_actions/checkout@v4
f376731f9ec450a2 severity=Critical status=manual rule=unpinned-uses file=.github/workflows/lint.yml step=jobs/typecheck/steps/[0]/uses_actions/checkout@v4
69ec9c5157bd40d5 severity=Critical status=manual rule=unpinned-uses file=.github/workflows/lint.yml step=jobs/typecheck/steps/[1]/uses_actions/setup-node@v4
90b353ae44278314 severity=Critical status=manual rule=unpinned-uses file=.github/workflows/lint.yml step=jobs/compute-futures-tests/steps/[0]/uses_actions/checkout@v
68e7ddaa1849efcd severity=Critical status=manual rule=unpinned-uses file=.github/workflows/lint.yml step=jobs/compute-futures-tests/steps/[1]/uses_actions/setup-node
c182c4b09856e45e severity=Critical status=manual rule=unpinned-uses file=.github/workflows/messages.yml step=jobs/tick/steps/[0]/uses_actions/checkout@v5
af2a5276951f0282 severity=Critical status=manual rule=unpinned-uses file=.github/workflows/messages.yml step=jobs/run/steps/[1]/uses_actions/checkout@v5
d40d25c58d3f1121 severity=Critical status=manual rule=unpinned-uses file=.github/workflows/messages.yml step=jobs/run/steps/[3]/uses_actions/setup-node@v5
57704566d1e2a4a9 severity=Critical status=manual rule=unpinned-uses file=.github/workflows/sync-aeon-public-results.yml step=jobs/sync/steps/[0]/uses_actions/checkout@v4
3bd7922c53c26092 severity=Critical status=manual rule=unpinned-uses file=.github/workflows/sync-upstream.yml step=jobs/sync/steps/[0]/uses_actions/checkout@v4
fcc86af96deeb128 severity=High status=manual rule=secrets-outside-env file=.github/workflows/chain-runner.yml step=jobs/run_secrets.GH_GLOBAL
f4ec362840222df6 severity=High status=manual rule=secrets-outside-env file=.github/workflows/chain-runner.yml step=jobs/run_secrets.AEON_PRIVATE_PAT
4b37fe93962380dc severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=jobs/run_secrets.GITLAWB_OPERATOR_PEM
1d5119114e187ff2 severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=jobs/run_secrets.GITLAWB_OPERATOR_UCAN
d92cdf70d7d02be9 severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=jobs/run_secrets.GITLAWB_RESEARCHER_PEM
9c926371a6a4f193 severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=jobs/run_secrets.GITLAWB_REVIEWER_PEM
7d4f294ae1f9c689 severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=jobs/run_secrets.GITLAWB_DEPLOYER_PEM
21abdc5171fb6688 severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=jobs/run_secrets.GITLAWB_SENTINEL_PEM
4b38abe3e09287c5 severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=jobs/run_secrets.SURPLUS_PRICING_URL
6b7170399fd80b2e severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=jobs/run_secrets.SURPLUS_API_KEY
10b63d97b04de873 severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=jobs/run_secrets.CLAUDE_CODE_OAUTH_TOKEN
f187cfe7245b7b7b severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=jobs/run_secrets.AEON_PRIVATE_PAT
9f1439b29d531c57 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/tick_secrets.GH_GLOBAL
f90f3353429e512b severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/tick_secrets.TELEGRAM_BOT_TOKEN
e28650f1777c937c severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/tick_secrets.TELEGRAM_CHAT_ID
b98bda3743744359 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/tick_secrets.DISCORD_BOT_TOKEN
8a686506dafdb4b8 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/tick_secrets.DISCORD_CHANNEL_ID
2af1c6cf607e9cc3 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/tick_secrets.SLACK_BOT_TOKEN
912c47813332c9eb severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/tick_secrets.SLACK_CHANNEL_ID
1ee37dc18089160e severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/tick_secrets.AEON_PRIVATE_PAT
d555d37269c365a3 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.GH_GLOBAL
cccd1fce5bbba854 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.ANTHROPIC_API_KEY
8ec3373d805fa9b0 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.CLAUDE_CODE_OAUTH_TOKEN
010ced2bb254f2e3 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.TELEGRAM_BOT_TOKEN
91f4a3b80717f7c2 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.TELEGRAM_CHAT_ID
29eb7896129b6ca6 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.DISCORD_BOT_TOKEN
cb22c9067f985003 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.DISCORD_CHANNEL_ID
d8762b5179854e5e severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.DISCORD_WEBHOOK_URL
71eb21d233f8c902 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.SLACK_BOT_TOKEN
9eb7c8142e3d70e7 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.SLACK_CHANNEL_ID
399d2bc066cee184 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.SLACK_WEBHOOK_URL
f172d1094d71b91d severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.XAI_API_KEY
e3e742eb1ecae50f severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.COINGECKO_API_KEY
b43f59d6ad20bd99 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.ALCHEMY_API_KEY
bc888b749cb910ad severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.AEON_PRIVATE_PAT
8fd7c24cac6fa3fc severity=High status=manual rule=secrets-outside-env file=.github/workflows/sync-upstream.yml step=jobs/sync_secrets.GH_GLOBAL
098273477d4c2049 severity=Medium status=info rule=artipacked file=.github/workflows/aeon.yml step=Early_checkout
c532628fb9c78a69 severity=Medium status=info rule=artipacked file=.github/workflows/aeon.yml step=Checkout_repo
34f769ea5d7ada7e severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/aeon.yml step=
f7f986071e1a844d severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/aeon.yml step=
1aff3826dae795dc severity=Medium status=info rule=artipacked file=.github/workflows/chain-runner.yml step=Checkout_repo
d134e2dc063e6a49 severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/chain-runner.yml step=
fea5106dd502696b severity=Medium status=info rule=artipacked file=.github/workflows/fleet-runner.yml step=Checkout
60ffa53aab8306ae severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/fleet-runner.yml step=
7f3a1bdd5ffb750b severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/fleet-runner.yml step=
e62807ce42c490c3 severity=Medium status=info rule=artipacked file=.github/workflows/lint.yml step=Checkout
794adcb750726f00 severity=Medium status=info rule=artipacked file=.github/workflows/messages.yml step=Checkout_repo
78c3dedbd19198e0 severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/messages.yml step=
195215533d641199 severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/messages.yml step=
a7a60aa1a7597c81 severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/messages.yml step=
469d57d06efb0e27 severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/messages.yml step=
8639b641ebcf9473 severity=Medium status=info rule=artipacked file=.github/workflows/sync-aeon-public-results.yml step=Checkout_aeon
51e649cc0aebc1c2 severity=Medium status=info rule=artipacked file=.github/workflows/sync-upstream.yml step=Checkout_fork
bfb64b0b70648404 severity=Low status=info rule=anonymous-definition file=.github/workflows/aeon.yml step=jobs/run_run
5e2ab20bf3488907 severity=Low status=info rule=undocumented-permissions file=.github/workflows/aeon.yml step=jobs/run/permissions/contents_contents:_write
4547139a532a914c severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[1]/run__
c84af8217080efb3 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[2]/run__
47cbc3dec30daa29 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[7]/run__
921cce7f7bb69fb9 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[8]/run__
802ab34fd6a80030 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[10]/run__
da8302f3485d0eee severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[12]/run__
7aab4abd172546ae severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[13]/run__
f8d55bb2871a14ed severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[14]/run__
5c3292fe3f7ac871 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[15]/run__
c227d79cbc5b55b5 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[16]/run__
45a2a413e2a7a16b severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[19]/run__
6373308cf86e41b9 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[20]/run__
36340b5f870098ca severity=Low status=info rule=anonymous-definition file=.github/workflows/chain-runner.yml step=jobs/run_run
ea0f2044c7cc25e5 severity=Low status=info rule=undocumented-permissions file=.github/workflows/chain-runner.yml step=jobs/run/permissions/contents_contents:_write
374561afef7a4cd4 severity=Low status=info rule=concurrency-limits file=.github/workflows/fleet-runner.yml step=on_on:
2a6630e97fc3d899 severity=Low status=info rule=anonymous-definition file=.github/workflows/fleet-runner.yml step=jobs/run_run
670ebea2a9d5d2c9 severity=Low status=info rule=undocumented-permissions file=.github/workflows/fleet-runner.yml step=jobs/run/permissions/contents_contents:_write
095c4f508d908059 severity=Low status=info rule=template-injection file=.github/workflows/fleet-runner.yml step=jobs/run/steps/[6]/run__
e5aa801ac91554b0 severity=Low status=info rule=template-injection file=.github/workflows/fleet-runner.yml step=jobs/run/steps/[15]/run__
f99ea9f308914904 severity=Low status=info rule=template-injection file=.github/workflows/fleet-runner.yml step=jobs/run/steps/[16]/run__
775240a474702818 severity=Low status=info rule=anonymous-definition file=.github/workflows/messages.yml step=jobs/tick_tick
84430babfdcd30b9 severity=Low status=info rule=anonymous-definition file=.github/workflows/messages.yml step=jobs/run_run
5f9fc571bf19306a severity=Low status=info rule=undocumented-permissions file=.github/workflows/messages.yml step=jobs/run/permissions/issues_issues:_read
d7dad935ab3641cc severity=Low status=info rule=template-injection file=.github/workflows/messages.yml step=jobs/run/steps/[0]/run__
a05d92f0e2ac5f5f severity=Low status=info rule=anonymous-definition file=.github/workflows/sync-aeon-public-results.yml step=jobs/sync_sync
7631a1c62654fb2b severity=Low status=info rule=anonymous-definition file=.github/workflows/sync-upstream.yml step=jobs/sync_sync
6fc43160799f815d severity=Low status=info rule=undocumented-permissions file=.github/workflows/sync-upstream.yml step=jobs/sync/permissions/contents_contents:_write
3b6b3e58b92c931c severity=Low status=info rule=template-injection file=.github/workflows/sync-upstream.yml step=jobs/sync/steps/[6]/run_git_push_origin_"${{_steps.merge.out
c7d958e988b03cc9 severity=Low status=info rule=template-injection file=.github/workflows/sync-upstream.yml step=jobs/sync/steps/[7]/run__
-->
