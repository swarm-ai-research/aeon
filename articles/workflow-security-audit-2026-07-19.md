# Workflow Security Audit — 2026-07-19

**Verdict:** WORKFLOW_AUDIT_NEW_CRITICAL — 3 new critical finding(s)
**Repo:** [swarm-ai-research/aeon](https://github.com/swarm-ai-research/aeon)
**Files audited:** 7 (7 workflows, 0 composite actions)
**Findings this run:** 85 (3 critical, 36 high, 15 medium, 31 low)
**Delta vs (no prior audit):** 85 new, 0 reintroduced, 0 unchanged, 0 resolved
**Auto-fixed:** 0
**Manual review:** 39

## New findings

### [CRITICAL] zizmor/unpinned-uses — third-party actions not SHA-pinned
**File:** `.github/workflows/aeon.yml` · **Instances:** 3 (all `actions/*` refs pinned by tag, not SHA)

**Occurrences:**

| Line | Step | Reference |
|---|---|---|
| 85 | `actions/checkout@v5` | `actions/checkout@v5` |
| 121 | `actions/checkout@v5` | `actions/checkout@v5` |
| 133 | `actions/setup-node@v5` | `actions/setup-node@v5` |

**Pattern (aeon.yml:85):**
```yaml
- name: Early checkout
  if: github.event_name == 'issues'
  uses: actions/checkout@v5
  with:
    token: ${{ secrets.GITHUB_TOKEN }}
```

**Attack chain:**
1. **Entry:** `issues.labeled` (label `ai-build`) — any repo collaborator with issue-write access can label. `workflow_dispatch` is also present on this workflow but requires actor with actions:write.
2. **Vector:** `actions/checkout@v5` (and `actions/setup-node@v5` at line 133) resolve at run time to whatever commit `v5` currently points at. GitHub's release-tag SHAs are compromised via three known vectors: (a) attacker with push to the action repo force-pushes the tag; (b) an intermediate maintainer publishes a malicious minor; (c) the tag ref itself is redirected. `actions/*` is a first-party org so the residual risk is compromise of that org's release process — real, but low relative to third-party actions.
3. **Sink:** the checkout action runs arbitrary JavaScript from the resolved SHA with the job's `GITHUB_TOKEN` available. `setup-node` similarly executes with runner privileges and can write `~/.npmrc`.
4. **Reachable secrets:** `GITHUB_TOKEN` (scoped to job perms: `contents: write`, `pull-requests: write`, `issues: read`, `actions: read`), plus all workflow-level env: `FLEET_ENDPOINT`, `FLEET_TOKEN` (from `secrets.FLEET_*`), and every subsequent step's secret exposures on this runner.
5. **Blast radius:** push to `main`, open/close PRs, dispatch downstream workflows (`gh workflow run`). Because the `run` job also installs `@anthropic-ai/claude-code` (line 139), a compromised checkout SHA can plant a malicious binary before the CLI executes user prompts on this runner and every future run until a pin is set.

**Fix:**
```yaml
# BEFORE
- uses: actions/checkout@v5
- uses: actions/setup-node@v5

# AFTER — replace with the specific commit SHA of the release tag
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v5.0.0
- uses: actions/setup-node@a0853c24544627f65ddf259abe73b1d18a591444 # v5.0.0
```

Verify SHAs against `git ls-remote https://github.com/actions/checkout refs/tags/v5.0.0` before committing.

**Status:** Manual review required — the skill's step-7 rules never auto-fix `unpinned-uses` (operator must verify each intended commit SHA against the published release).

### [HIGH] zizmor/secrets-outside-env — secrets referenced without a dedicated GitHub Environment
**Instances:** 36 across 4 files.

**Distribution:**

| File | Count | Secrets referenced |
|---|---:|---|
| `.github/workflows/chain-runner.yml` | 2 | `secrets.AEON_PRIVATE_PAT`, `secrets.GH_GLOBAL` |
| `.github/workflows/fleet-runner.yml` | 10 | `secrets.AEON_PRIVATE_PAT`, `secrets.CLAUDE_CODE_OAUTH_TOKEN`, `secrets.GITLAWB_DEPLOYER_PEM`, `secrets.GITLAWB_OPERATOR_PEM`, `secrets.GITLAWB_OPERATOR_UCAN`, `secrets.GITLAWB_RESEARCHER_PEM`, … (4 more) |
| `.github/workflows/messages.yml` | 23 | `secrets.AEON_PRIVATE_PAT`, `secrets.ALCHEMY_API_KEY`, `secrets.ANTHROPIC_API_KEY`, `secrets.CLAUDE_CODE_OAUTH_TOKEN`, `secrets.COINGECKO_API_KEY`, `secrets.DISCORD_BOT_TOKEN`, … (9 more) |
| `.github/workflows/sync-upstream.yml` | 1 | `secrets.GH_GLOBAL` |

**Pattern (representative — `fleet-runner.yml:287`):**
```yaml
jobs:
  run:
    runs-on: ubuntu-latest
    # no `environment:` declared
    steps:
      - name: Run fleet task runner
        env:
          CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
          GH_TOKEN:                ${{ secrets.GITHUB_TOKEN }}
        run: |
          ...
```

**Attack chain:**
1. **Entry:** any commit that lands on `main` (via merged PR, direct push with a `contents: write` PAT, or a workflow that opens+merges its own PR) causes the next scheduled or dispatched run of these workflows to use whatever secret bindings are declared. Without a GitHub Environment, there is no approval gate, no branch-protection tie, and no per-secret audit trail — the secret is available on any ref.
2. **Vector:** a malicious PR that mutates the workflow itself (e.g. exfiltrating `CLAUDE_CODE_OAUTH_TOKEN`, `GH_GLOBAL`, or the `GITLAWB_*_PEM` fleet keys via `curl` or an added step) merges into a branch that a scheduled run picks up. GitHub's default `pull_request` guard does not run first-time-contributor code with secrets, but this repo runs `workflow_dispatch` and `schedule` events which do execute with the full secret scope.
3. **Sink:** shell interpolation into `run:` blocks (e.g. `echo '${{ secrets.GITLAWB_OPERATOR_PEM }}' > ~/.gitlawb/identity.pem` at `fleet-runner.yml:150`), and env-var passthroughs to helper scripts (`scripts/fleet-executors/*.mjs`, `scripts/prefetch-surplus.sh`).
4. **Reachable secrets:** `GH_GLOBAL` (fine-grained PAT with **Workflows** write permission — can push to `.github/workflows/*` and bypass GITHUB_TOKEN restrictions), `AEON_PRIVATE_PAT`, 5 × `GITLAWB_*_PEM` fleet identity keys, `GITLAWB_OPERATOR_UCAN`, `CLAUDE_CODE_OAUTH_TOKEN` (Anthropic subscription), `SURPLUS_PRICING_URL`, `SURPLUS_API_KEY`, `TELEGRAM_BOT_TOKEN`, `DISCORD_WEBHOOK_URL`, `SLACK_WEBHOOK_URL`, `SENDGRID_API_KEY`.
5. **Blast radius:** exfiltration of `GH_GLOBAL` alone enables persistence — the attacker can rewrite any workflow file and push directly to `main`, since it is scoped past the default GITHUB_TOKEN's `.github/workflows/*` block (this is the reason the PAT exists per the `sync-upstream.yml` comment at line 26). Exfiltration of `GITLAWB_*_PEM` compromises the multi-agent fleet identity (researcher/reviewer/deployer/sentinel) — each has distinct `gl register` capabilities up to `repo:admin` (sentinel). Exfiltration of `CLAUDE_CODE_OAUTH_TOKEN` gives free Anthropic subscription-tier compute to the attacker until rotated.

**Fix (per-file):**
```yaml
# BEFORE — job that reads secrets directly
jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - env:
          GH_TOKEN: ${{ secrets.GH_GLOBAL }}
        ...

# AFTER — declare an Environment, then bind protection rules in repo Settings
jobs:
  run:
    runs-on: ubuntu-latest
    environment:
      name: production
      # optional: url: ${{ steps.deploy.outputs.url }}
    steps:
      - env:
          GH_TOKEN: ${{ secrets.GH_GLOBAL }}
        ...
```

Then in **Repo Settings → Environments → production**: (a) add required reviewers if you want a manual approval gate; (b) restrict to `main` branch; (c) move the sensitive secrets (`GH_GLOBAL`, `GITLAWB_*_PEM`, `AEON_PRIVATE_PAT`, `CLAUDE_CODE_OAUTH_TOKEN`) from repo-scoped to environment-scoped so they only decrypt inside jobs that opt into this environment.

Recommended environments for this repo:
- **`production`** — fleet-runner (owns fleet identity keys + Claude OAuth), messages.yml scheduler (owns `GH_GLOBAL` dispatch), sync-upstream (owns `GH_GLOBAL` for workflow-file pushes).
- **`chain-runner`** — chain-runner.yml (owns `GH_GLOBAL` and `AEON_PRIVATE_PAT` for skill orchestration).

**Status:** Manual review required — environment topology and reviewer policy are operator judgment calls; auto-fix cannot pick the boundary.

## Medium-severity findings (compact)

| # | Rule | File | Line | Signal |
|---|---|---|---:|---|
| 1 | `zizmor/artipacked` | `.github/workflows/aeon.yml` | 83 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |
| 2 | `zizmor/artipacked` | `.github/workflows/aeon.yml` | 119 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |
| 3 | `actionlint-shellcheck` | `.github/workflows/aeon.yml` | 286 | shellcheck reported issue in this script: SC2129:style:259:1: Consider using { cmd1; cmd2; } >> file |
| 4 | `zizmor/artipacked` | `.github/workflows/chain-runner.yml` | 28 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |
| 5 | `actionlint-shellcheck` | `.github/workflows/chain-runner.yml` | 42 | shellcheck reported issue in this script: SC2034:warning:3:1: NOW_ISO appears unused. Verify use (or |
| 6 | `zizmor/artipacked` | `.github/workflows/fleet-runner.yml` | 56 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |
| 7 | `actionlint-shellcheck` | `.github/workflows/fleet-runner.yml` | 179 | shellcheck reported issue in this script: SC2155:warning:2:8: Declare and assign separately to avoid |
| 8 | `zizmor/artipacked` | `.github/workflows/lint.yml` | 32 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |
| 9 | `zizmor/artipacked` | `.github/workflows/lint.yml` | 70 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |
| 10 | `zizmor/artipacked` | `.github/workflows/lint.yml` | 91 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |
| 11 | `zizmor/artipacked` | `.github/workflows/messages.yml` | 56 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |
| 12 | `actionlint-shellcheck` | `.github/workflows/messages.yml` | 69 | shellcheck reported issue in this script: SC2034:warning:247:5: IN_STEPS appears unused. Verify use  |
| 13 | `zizmor/artipacked` | `.github/workflows/messages.yml` | 691 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |
| 14 | `zizmor/artipacked` | `.github/workflows/sync-aeon-public-results.yml` | 28 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |
| 15 | `zizmor/artipacked` | `.github/workflows/sync-upstream.yml` | 22 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |

**`zizmor/artipacked` (11 instances):** `actions/checkout` steps run with the default `persist-credentials: true`, which leaves `.git/config` on the runner with the `GITHUB_TOKEN` baked in. Fix by adding `persist-credentials: false` to each `with:` block unless the step later performs a `git push` that needs the token (in which case, use a scoped `token: ${{ secrets.GITHUB_TOKEN }}` and unset after the push).

**`actionlint-shellcheck` (4 instances):** SC2129 style hints (individual `echo >>` redirects should be grouped `{ ...; } >> file`) and SC2034/SC2155 (unused / declaration-mask). Style-only — not exploitable, but worth clean-up when the surrounding blocks are touched.

## Low-severity findings (compact)

| Rule | Count | Notes |
|---|---:|---|
| `zizmor/template-injection` | 18 | `${{ ... }}` interpolations into `run:` blocks. Most are safe because the source is `steps.*.outputs.*` or `github.run_id`, but review each to confirm the source is not attacker-controlled. |
| `zizmor/anonymous-definition` | 7 | Composite/reusable steps without a `name:` field. Purely cosmetic — makes attack-chain triage harder later. |
| `zizmor/undocumented-permissions` | 5 | Jobs granting `permissions:` without a comment explaining why each scope is needed. Low but worth adding a `# scope-rationale:` line each. |
| `zizmor/concurrency-limits` | 1 | A workflow allows concurrent execution that could race on shared state. |

## Carried over (unchanged)

_None (this is the first audit — no prior report to compare against)._

## Resolved since (n/a)

_None._

## Source status

- zizmor: ok (v1.25.2 from `.audit-bin/zizmor`, persona=auditor, SARIF)
- actionlint: ok (from `.audit-bin/actionlint`, JSON output)
- hand-rolled: ok (toJson-into-shell, persist-creds-pr-head, GITHUB_ENV injection, inputs-to-gh-dispatch, mutable-third-party-ref — all clean this run)

<!--
workflow-security-audit-fingerprints
bc09e996c19bee00 severity=Critical status=manual rule=zizmor/unpinned-uses file=.github/workflows/aeon.yml step=actions/checkout@v5
9d5b7e76307fa646 severity=Critical status=manual rule=zizmor/unpinned-uses file=.github/workflows/aeon.yml step=actions/checkout@v5
6b647aca1bb4273b severity=Critical status=manual rule=zizmor/unpinned-uses file=.github/workflows/aeon.yml step=actions/setup-node@v5
02b2a57dd0a60445 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/chain-runner.yml step=secrets.GH_GLOBAL
ce5feb86b40f7b69 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/chain-runner.yml step=secrets.AEON_PRIVATE_PAT
938fedeeb2409c8a severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=secrets.GITLAWB_OPERATOR_PEM
a37f87baa2daf6f2 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=secrets.GITLAWB_OPERATOR_UCAN
b477fb148a0129c3 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=secrets.GITLAWB_RESEARCHER_PEM
b0801e6e2cd6b18c severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=secrets.GITLAWB_REVIEWER_PEM
0c330da6e3cebbaf severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=secrets.GITLAWB_DEPLOYER_PEM
77cc1875a8cf7938 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=secrets.GITLAWB_SENTINEL_PEM
f4f8439c6b60e8ac severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=secrets.SURPLUS_PRICING_URL
1621315578ca0bb4 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=secrets.SURPLUS_API_KEY
99a038e961624de8 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=secrets.CLAUDE_CODE_OAUTH_TOKEN
aee24729cdf25d44 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=secrets.AEON_PRIVATE_PAT
804753d97fa119b6 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.GH_GLOBAL
ebd899f957039539 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.TELEGRAM_BOT_TOKEN
8e59c79cd49a15cc severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.TELEGRAM_CHAT_ID
1599d6179b83c9d0 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.DISCORD_BOT_TOKEN
33123b7289853b8e severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.DISCORD_CHANNEL_ID
cddc7b0d505c9bd4 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.SLACK_BOT_TOKEN
45784a42430ff362 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.SLACK_CHANNEL_ID
1e26ce35bfe5d66c severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.AEON_PRIVATE_PAT
3b430937edf22475 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.GH_GLOBAL
e8252b756e017457 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.ANTHROPIC_API_KEY
3ac0423931e2373d severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.CLAUDE_CODE_OAUTH_TOKEN
e3ad7e690d9eafab severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.TELEGRAM_BOT_TOKEN
187a57d762078b80 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.TELEGRAM_CHAT_ID
42713b777cba999d severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.DISCORD_BOT_TOKEN
f20b2aaa708ff0f0 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.DISCORD_CHANNEL_ID
8c18be5b224dd49c severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.DISCORD_WEBHOOK_URL
5e30d6ef83c933ef severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.SLACK_BOT_TOKEN
01f39fed27d1c1cb severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.SLACK_CHANNEL_ID
07fa0c013c685431 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.SLACK_WEBHOOK_URL
af178cb8c4ea9557 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.XAI_API_KEY
1fbeb453f2b64558 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.COINGECKO_API_KEY
599d21c0d4c9ecae severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.ALCHEMY_API_KEY
49c528b21a08be9b severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=secrets.AEON_PRIVATE_PAT
59adbdf23f816a0b severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/sync-upstream.yml step=secrets.GH_GLOBAL
dc62b22b7e6b194d severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/aeon.yml step=name:_Early_checkout
7f4b63fd4e9dfb55 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/aeon.yml step=name:_Checkout_repo
41cfb4da0fe54dcd severity=Medium status=manual rule=actionlint-shellcheck file=.github/workflows/aeon.yml step=run:_|
780e2f59890acc5d severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/chain-runner.yml step=name:_Checkout_repo
19a7ac0123fc318f severity=Medium status=manual rule=actionlint-shellcheck file=.github/workflows/chain-runner.yml step=run:_|
add19efede894e43 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/fleet-runner.yml step=name:_Checkout
d9779159cd5a6a7a severity=Medium status=manual rule=actionlint-shellcheck file=.github/workflows/fleet-runner.yml step=run:_|
c040878621a937e2 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/lint.yml step=name:_Checkout
bb46098505705c37 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/lint.yml step=name:_Checkout
f4834d554fb62889 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/lint.yml step=name:_Checkout
5c4f2dbb0166bad9 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/messages.yml step=name:_Checkout_repo
9cc8584f3ac3f750 severity=Medium status=manual rule=actionlint-shellcheck file=.github/workflows/messages.yml step=run:_|
e54c2ff1101bb008 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/messages.yml step=name:_Checkout_repo
2572b7f963c34194 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/sync-aeon-public-results.yml step=name:_Checkout_aeon
4a755250b386fe19 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/sync-upstream.yml step=name:_Checkout_fork
86acdfbec61d80df severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/aeon.yml step=run
b52bcbc02f2dea1d severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/aeon.yml step=contents:_write
5ce2142ccbd94fb0 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=|
bc22535ec66d8eaa severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=|
bf9d81b6122895c9 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=|
522b76066033da55 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=|
e727f31d25dba310 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=|
a66b15671e81b7e3 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=|
958bdbfa1390908b severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=|
fc9a366620fa6297 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=|
24d241efbac92ca6 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=|
11e5b1c6948443eb severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=|
81cd448216b27fc9 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=|
617feda5e376a959 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=|
ed2c462f57282c0b severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/chain-runner.yml step=run
f01824742677d6fd severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/chain-runner.yml step=contents:_write
75a0ede57363f047 severity=Low status=manual rule=zizmor/concurrency-limits file=.github/workflows/fleet-runner.yml step=on:
d8465411cfca8321 severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/fleet-runner.yml step=run
b651f95bcf9ff276 severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/fleet-runner.yml step=contents:_write
0d1a3ca79be8bbe8 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=|
03815cf8841c31c6 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=|
b1a6b69db9f2154b severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=|
82128ad8cf219aa1 severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/messages.yml step=tick
92cf58a41e74770b severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/messages.yml step=run
cf7ac130bafb8541 severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/messages.yml step=issues:_read
8d119f5aef391d50 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/messages.yml step=|
29beed7a7a99ae39 severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/sync-aeon-public-results.yml step=sync
d38c01212ecf7263 severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/sync-upstream.yml step=sync
17055d0874a059e6 severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/sync-upstream.yml step=contents:_write
1ad9d321d3d79db7 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/sync-upstream.yml step=git_push_origin_"${{_steps.merge.outputs
12bc517bf1a1cd8d severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/sync-upstream.yml step=|
-->
