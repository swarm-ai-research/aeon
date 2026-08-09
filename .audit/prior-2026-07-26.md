# Workflow Security Audit — 2026-07-26

**Verdict:** WORKFLOW_AUDIT_NEW_CRITICAL — 3 new critical finding(s) (bootstrap run; no prior audit on main)
**Repo:** [swarm-ai-research/aeon](https://github.com/swarm-ai-research/aeon)
**Files audited:** 7 (7 workflows, 0 composite actions)
**Findings this run:** 75 unique (3 critical, 22 high, 18 medium, 32 low) — 145 total occurrences before dedup by rule×file×step
**Delta vs (no prior audit):** 75 new, 0 reintroduced, 0 unchanged, 0 resolved
**Auto-fixed:** 0  ·  **Manual review required:** 25

> **Why zero auto-fixes on a NEW_CRITICAL run:** every Critical (`unpinned-uses`) and every High finding (`ref-version-mismatch`, `secrets-outside-env`, and the actionlint `SC2086` in a fleet task-runner argument) falls under a category the skill's constraints hold as Manual. `unpinned-uses`, permissions, and `persist-credentials` need operator judgment about which commit SHA to pin (choosing a specific tag → SHA is a review call). `secrets-outside-env` needs the operator to create the `production` and `chain-runner` GitHub Environments and re-scope every secret through the repo Settings UI — the workflow edit alone would break every skill until the environment exists. Auto-fix would produce runs that appear to succeed but silently downgrade security or break the fleet.

---

## Regressions

_None — bootstrap run, no prior audit on main to regress against. Memory notes the operator ran a prior scan on 2026-07-19 whose report and staged fixes never merged (blocked behind the same Repo Settings toggle that blocks the ≥18-branch queue); those findings are treated as NEW here._

---

## New findings

### [CRITICAL] zizmor/unpinned-uses — Early checkout
**File:** `.github/workflows/aeon.yml` · **Step:** `Early checkout` · **Line:** 85
**Pattern:**
```yaml
uses: actions/checkout@v5
```

**Attack chain:**
1. **Entry:** any trigger for this workflow — schedule (cron every 5 min), workflow_dispatch, workflow_call, issues:labeled
2. **Vector:** supply chain — the mutable tag `v5`/`v4` can be moved to a malicious commit by anyone with write access to that action's repo (compromised maintainer account, insider, or a moved tag pushed as a hijack)
3. **Sink:** `uses: actions/checkout@v5` runs as the first step of every skill invocation; the action code executes with the job's full permissions
4. **Reachable secrets:** the aeon `run` job has `contents: write`, `pull-requests: write`, `issues: read`, `actions: read`, plus every notification / API secret exposed via workflow env (`FLEET_ENDPOINT`, `FLEET_TOKEN`) and inherited via `GITHUB_TOKEN`
5. **Blast radius:** arbitrary code executes with push access to `main`, ability to open PRs from any branch, and the `GITHUB_TOKEN` bearer scope — full self-modification of the aeon agent

**Fix:**
```yaml
# BEFORE
uses: actions/checkout@v5
# AFTER (pin to the commit SHA of the intended tag; keep the tag as a review comment)
uses: actions/checkout@93cb6efe18208431cddfb8368fd83d5badbf9bfd # v5.0.0
```

**Status:** Manual review required · **Fingerprint:** `9fb519eb4fdb`

---

### [CRITICAL] zizmor/unpinned-uses — Checkout repo
**File:** `.github/workflows/aeon.yml` · **Step:** `Checkout repo` · **Line:** 121
**Pattern:**
```yaml
uses: actions/checkout@v5
```

**Attack chain:**
1. **Entry:** any trigger for this workflow — schedule (cron every 5 min), workflow_dispatch, workflow_call, issues:labeled
2. **Vector:** supply chain — the mutable tag `v5`/`v4` can be moved to a malicious commit by anyone with write access to that action's repo (compromised maintainer account, insider, or a moved tag pushed as a hijack)
3. **Sink:** `uses: actions/checkout@v5` runs as the first step of every skill invocation; the action code executes with the job's full permissions
4. **Reachable secrets:** the aeon `run` job has `contents: write`, `pull-requests: write`, `issues: read`, `actions: read`, plus every notification / API secret exposed via workflow env (`FLEET_ENDPOINT`, `FLEET_TOKEN`) and inherited via `GITHUB_TOKEN`
5. **Blast radius:** arbitrary code executes with push access to `main`, ability to open PRs from any branch, and the `GITHUB_TOKEN` bearer scope — full self-modification of the aeon agent

**Fix:**
```yaml
# BEFORE
uses: actions/checkout@v5
# AFTER (pin to the commit SHA of the intended tag; keep the tag as a review comment)
uses: actions/checkout@93cb6efe18208431cddfb8368fd83d5badbf9bfd # v5.0.0
```

**Status:** Manual review required · **Fingerprint:** `7491c14fbe74`

---

### [CRITICAL] zizmor/unpinned-uses — Setup Node.js
**File:** `.github/workflows/aeon.yml` · **Step:** `Setup Node.js` · **Line:** 133
**Pattern:**
```yaml
uses: actions/setup-node@v5
```

**Attack chain:**
1. **Entry:** any trigger for this workflow — schedule (cron every 5 min), workflow_dispatch, workflow_call, issues:labeled
2. **Vector:** supply chain — the mutable tag `v5`/`v4` can be moved to a malicious commit by anyone with write access to that action's repo (compromised maintainer account, insider, or a moved tag pushed as a hijack)
3. **Sink:** `uses: actions/setup-node@v5` runs as the first step of every skill invocation; the action code executes with the job's full permissions
4. **Reachable secrets:** the aeon `run` job has `contents: write`, `pull-requests: write`, `issues: read`, `actions: read`, plus every notification / API secret exposed via workflow env (`FLEET_ENDPOINT`, `FLEET_TOKEN`) and inherited via `GITHUB_TOKEN`
5. **Blast radius:** arbitrary code executes with push access to `main`, ability to open PRs from any branch, and the `GITHUB_TOKEN` bearer scope — full self-modification of the aeon agent

**Fix:**
```yaml
# BEFORE
uses: actions/setup-node@v5
# AFTER (pin to the commit SHA of the intended tag; keep the tag as a review comment)
uses: actions/setup-node@2028fbc5c25fe9cf00d9f06a71cc4710d4507903 # v5.0.0
```

**Status:** Manual review required · **Fingerprint:** `920a2c40af77`

---

### [HIGH] zizmor/ref-version-mismatch — Checkout repo
**File:** `.github/workflows/chain-runner.yml` · **Step:** `Checkout repo` · **Line:** 29
**Pattern:**
```yaml
uses: actions/checkout@93cb6efe18208431cddfb8368fd83d5badbf9bfd # v5
```

**Attack chain:**
1. **Entry:** any run of the workflow
2. **Vector:** the comment says `v5` (or `v4`) but the pin points to a specific commit — if the comment ever drifts from the commit (during a review, a rebase, or a copy-paste), a reviewer approving the intent (`v5` = presumably-vetted release) may inadvertently approve an unvetted commit
3. **Sink:** `uses: actions/checkout@93cb6efe18208431cddfb8368fd83d5badbf9bfd # v5` — the SHA is what runs, but the review signal is the version tag comment
4. **Reachable secrets:** same scope as unpinned-uses for the same job
5. **Blast radius:** low-friction supply-chain attack via reviewer misalignment — a malicious maintainer swaps SHA to attacker-controlled build while comment still reads `v5`

**Fix:**
```yaml
# BEFORE (comment drifted from the pinned SHA — reviewer sees the tag but the commit is what runs):
uses: actions/checkout@93cb6efe18208431cddfb8368fd83d5badbf9bfd # v5
# AFTER (verify the SHA is the current stable tag and update the comment to match):
uses: actions/checkout@<SHA of intended tag> # v5.0.0
```

**Status:** Manual review required · **Fingerprint:** `92de995e00e5`

---

### [HIGH] zizmor/secrets-outside-env — Checkout repo
**File:** `.github/workflows/chain-runner.yml` · **Step:** `Checkout repo` · **Line:** 31
**Pattern:**
```yaml
token: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }}
```

**Attack chain:**
1. **Entry:** any trigger that reaches this job — for messages.yml/chain-runner.yml, the `*/5 * * * *` schedule + `repository_dispatch` events; for fleet-runner.yml, `workflow_dispatch` and `schedule`
2. **Vector:** repo-scoped secret is available to every job in every workflow with no environment gate; a compromised action or a malicious workflow_dispatch input that reaches a bash sink can exfiltrate the secret without any deploy-review approval
3. **Sink:** `token: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }}` — no `environment:` clause on the job, so no reviewer approval, no branch protection, and no logging tie-back beyond the repo-audit-log
4. **Reachable secrets:** GH_GLOBAL (org-wide PAT), AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN (subscription auth), GITLAWB_*_PEM (fleet keys), Telegram/Discord/Slack tokens, Anthropic/xAI/CoinGecko/Alchemy keys
5. **Blast radius:** compromise of any of these secrets = full impersonation of the aeonframework identity across the org, or full drain of API credit, or takeover of the notification fan-out (Telegram/Discord/Slack chatops)

**Fix:**
```yaml
# BEFORE (secret referenced directly at job scope):
jobs:
  run:
    permissions: { contents: write }
    steps:
      - run: echo "${{ secrets.GH_GLOBAL }}"
# AFTER (gate the job behind a dedicated GitHub Environment):
jobs:
  run:
    environment: chain-runner  # or `production` — must be created in repo Settings > Environments first
    permissions: { contents: write }
    steps:
      - run: echo "$_GH_GLOBAL"
        env:
          _GH_GLOBAL: ${{ secrets.GH_GLOBAL }}  # now sourced from the environment scope
```

**Status:** Manual review required · **Fingerprint:** `cfad683f1a80`

---

### [HIGH] zizmor/secrets-outside-env — Run chain
**File:** `.github/workflows/chain-runner.yml` · **Step:** `Run chain` · **Line:** 40
**Pattern:**
```yaml
GH_TOKEN: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }}
```

**Attack chain:**
1. **Entry:** any trigger that reaches this job — for messages.yml/chain-runner.yml, the `*/5 * * * *` schedule + `repository_dispatch` events; for fleet-runner.yml, `workflow_dispatch` and `schedule`
2. **Vector:** repo-scoped secret is available to every job in every workflow with no environment gate; a compromised action or a malicious workflow_dispatch input that reaches a bash sink can exfiltrate the secret without any deploy-review approval
3. **Sink:** `GH_TOKEN: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }}` — no `environment:` clause on the job, so no reviewer approval, no branch protection, and no logging tie-back beyond the repo-audit-log
4. **Reachable secrets:** GH_GLOBAL (org-wide PAT), AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN (subscription auth), GITLAWB_*_PEM (fleet keys), Telegram/Discord/Slack tokens, Anthropic/xAI/CoinGecko/Alchemy keys
5. **Blast radius:** compromise of any of these secrets = full impersonation of the aeonframework identity across the org, or full drain of API credit, or takeover of the notification fan-out (Telegram/Discord/Slack chatops)

**Fix:**
```yaml
# BEFORE (secret referenced directly at job scope):
jobs:
  run:
    permissions: { contents: write }
    steps:
      - run: echo "${{ secrets.GH_GLOBAL }}"
# AFTER (gate the job behind a dedicated GitHub Environment):
jobs:
  run:
    environment: chain-runner  # or `production` — must be created in repo Settings > Environments first
    permissions: { contents: write }
    steps:
      - run: echo "$_GH_GLOBAL"
        env:
          _GH_GLOBAL: ${{ secrets.GH_GLOBAL }}  # now sourced from the environment scope
```

**Status:** Manual review required · **Fingerprint:** `92be19585492`

---

### [HIGH] zizmor/secrets-outside-env — Update cron state
**File:** `.github/workflows/chain-runner.yml` · **Step:** `Update cron state` · **Line:** 288
**Pattern:**
```yaml
GH_TOKEN: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }}
```

**Attack chain:**
1. **Entry:** any trigger that reaches this job — for messages.yml/chain-runner.yml, the `*/5 * * * *` schedule + `repository_dispatch` events; for fleet-runner.yml, `workflow_dispatch` and `schedule`
2. **Vector:** repo-scoped secret is available to every job in every workflow with no environment gate; a compromised action or a malicious workflow_dispatch input that reaches a bash sink can exfiltrate the secret without any deploy-review approval
3. **Sink:** `GH_TOKEN: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }}` — no `environment:` clause on the job, so no reviewer approval, no branch protection, and no logging tie-back beyond the repo-audit-log
4. **Reachable secrets:** GH_GLOBAL (org-wide PAT), AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN (subscription auth), GITLAWB_*_PEM (fleet keys), Telegram/Discord/Slack tokens, Anthropic/xAI/CoinGecko/Alchemy keys
5. **Blast radius:** compromise of any of these secrets = full impersonation of the aeonframework identity across the org, or full drain of API credit, or takeover of the notification fan-out (Telegram/Discord/Slack chatops)

**Fix:**
```yaml
# BEFORE (secret referenced directly at job scope):
jobs:
  run:
    permissions: { contents: write }
    steps:
      - run: echo "${{ secrets.GH_GLOBAL }}"
# AFTER (gate the job behind a dedicated GitHub Environment):
jobs:
  run:
    environment: chain-runner  # or `production` — must be created in repo Settings > Environments first
    permissions: { contents: write }
    steps:
      - run: echo "$_GH_GLOBAL"
        env:
          _GH_GLOBAL: ${{ secrets.GH_GLOBAL }}  # now sourced from the environment scope
```

**Status:** Manual review required · **Fingerprint:** `bde515abcfd3`

---

### [HIGH] zizmor/secrets-outside-env — Sync state to aeon-private (Phase 1 dual-write)
**File:** `.github/workflows/chain-runner.yml` · **Step:** `Sync state to aeon-private (Phase 1 dual-write)` · **Line:** 347
**Pattern:**
```yaml
AEON_PRIVATE_PAT: ${{ secrets.AEON_PRIVATE_PAT }}
```

**Attack chain:**
1. **Entry:** any trigger that reaches this job — for messages.yml/chain-runner.yml, the `*/5 * * * *` schedule + `repository_dispatch` events; for fleet-runner.yml, `workflow_dispatch` and `schedule`
2. **Vector:** repo-scoped secret is available to every job in every workflow with no environment gate; a compromised action or a malicious workflow_dispatch input that reaches a bash sink can exfiltrate the secret without any deploy-review approval
3. **Sink:** `AEON_PRIVATE_PAT: ${{ secrets.AEON_PRIVATE_PAT }}` — no `environment:` clause on the job, so no reviewer approval, no branch protection, and no logging tie-back beyond the repo-audit-log
4. **Reachable secrets:** GH_GLOBAL (org-wide PAT), AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN (subscription auth), GITLAWB_*_PEM (fleet keys), Telegram/Discord/Slack tokens, Anthropic/xAI/CoinGecko/Alchemy keys
5. **Blast radius:** compromise of any of these secrets = full impersonation of the aeonframework identity across the org, or full drain of API credit, or takeover of the notification fan-out (Telegram/Discord/Slack chatops)

**Fix:**
```yaml
# BEFORE (secret referenced directly at job scope):
jobs:
  run:
    permissions: { contents: write }
    steps:
      - run: echo "${{ secrets.GH_GLOBAL }}"
# AFTER (gate the job behind a dedicated GitHub Environment):
jobs:
  run:
    environment: chain-runner  # or `production` — must be created in repo Settings > Environments first
    permissions: { contents: write }
    steps:
      - run: echo "$_GH_GLOBAL"
        env:
          _GH_GLOBAL: ${{ secrets.GH_GLOBAL }}  # now sourced from the environment scope
```

**Status:** Manual review required · **Fingerprint:** `07c66694806a`

---

### [HIGH] zizmor/ref-version-mismatch — Checkout
**File:** `.github/workflows/fleet-runner.yml` · **Step:** `Checkout` · **Line:** 57
**Pattern:**
```yaml
uses: actions/checkout@93cb6efe18208431cddfb8368fd83d5badbf9bfd # v5
```

**Attack chain:**
1. **Entry:** any run of the workflow
2. **Vector:** the comment says `v5` (or `v4`) but the pin points to a specific commit — if the comment ever drifts from the commit (during a review, a rebase, or a copy-paste), a reviewer approving the intent (`v5` = presumably-vetted release) may inadvertently approve an unvetted commit
3. **Sink:** `uses: actions/checkout@93cb6efe18208431cddfb8368fd83d5badbf9bfd # v5` — the SHA is what runs, but the review signal is the version tag comment
4. **Reachable secrets:** same scope as unpinned-uses for the same job
5. **Blast radius:** low-friction supply-chain attack via reviewer misalignment — a malicious maintainer swaps SHA to attacker-controlled build while comment still reads `v5`

**Fix:**
```yaml
# BEFORE (comment drifted from the pinned SHA — reviewer sees the tag but the commit is what runs):
uses: actions/checkout@93cb6efe18208431cddfb8368fd83d5badbf9bfd # v5
# AFTER (verify the SHA is the current stable tag and update the comment to match):
uses: actions/checkout@<SHA of intended tag> # v5.0.0
```

**Status:** Manual review required · **Fingerprint:** `d5fac004ec2a`

---

### [HIGH] zizmor/secrets-outside-env — Restore fleet identities
**File:** `.github/workflows/fleet-runner.yml` · **Step:** `Restore fleet identities` · **Line:** 150
**Pattern:**
```yaml
echo '${{ secrets.GITLAWB_OPERATOR_PEM }}' > ~/.gitlawb/identity.pem
```

**Attack chain:**
1. **Entry:** any trigger that reaches this job — for messages.yml/chain-runner.yml, the `*/5 * * * *` schedule + `repository_dispatch` events; for fleet-runner.yml, `workflow_dispatch` and `schedule`
2. **Vector:** repo-scoped secret is available to every job in every workflow with no environment gate; a compromised action or a malicious workflow_dispatch input that reaches a bash sink can exfiltrate the secret without any deploy-review approval
3. **Sink:** `echo '${{ secrets.GITLAWB_OPERATOR_PEM }}' > ~/.gitlawb/identity.pem` — no `environment:` clause on the job, so no reviewer approval, no branch protection, and no logging tie-back beyond the repo-audit-log
4. **Reachable secrets:** GH_GLOBAL (org-wide PAT), AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN (subscription auth), GITLAWB_*_PEM (fleet keys), Telegram/Discord/Slack tokens, Anthropic/xAI/CoinGecko/Alchemy keys
5. **Blast radius:** compromise of any of these secrets = full impersonation of the aeonframework identity across the org, or full drain of API credit, or takeover of the notification fan-out (Telegram/Discord/Slack chatops)

**Fix:**
```yaml
# BEFORE (secret referenced directly at job scope):
jobs:
  run:
    permissions: { contents: write }
    steps:
      - run: echo "${{ secrets.GH_GLOBAL }}"
# AFTER (gate the job behind a dedicated GitHub Environment):
jobs:
  run:
    environment: chain-runner  # or `production` — must be created in repo Settings > Environments first
    permissions: { contents: write }
    steps:
      - run: echo "$_GH_GLOBAL"
        env:
          _GH_GLOBAL: ${{ secrets.GH_GLOBAL }}  # now sourced from the environment scope
```

**Status:** Manual review required · **Fingerprint:** `8970a9ecf814`

---

### [HIGH] zizmor/secrets-outside-env — Prefetch live Surplus prices (best-effort, outside sandbox)
**File:** `.github/workflows/fleet-runner.yml` · **Step:** `Prefetch live Surplus prices (best-effort, outside sandbox)` · **Line:** 271
**Pattern:**
```yaml
SURPLUS_PRICING_URL: ${{ secrets.SURPLUS_PRICING_URL }}
```

**Attack chain:**
1. **Entry:** any trigger that reaches this job — for messages.yml/chain-runner.yml, the `*/5 * * * *` schedule + `repository_dispatch` events; for fleet-runner.yml, `workflow_dispatch` and `schedule`
2. **Vector:** repo-scoped secret is available to every job in every workflow with no environment gate; a compromised action or a malicious workflow_dispatch input that reaches a bash sink can exfiltrate the secret without any deploy-review approval
3. **Sink:** `SURPLUS_PRICING_URL: ${{ secrets.SURPLUS_PRICING_URL }}` — no `environment:` clause on the job, so no reviewer approval, no branch protection, and no logging tie-back beyond the repo-audit-log
4. **Reachable secrets:** GH_GLOBAL (org-wide PAT), AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN (subscription auth), GITLAWB_*_PEM (fleet keys), Telegram/Discord/Slack tokens, Anthropic/xAI/CoinGecko/Alchemy keys
5. **Blast radius:** compromise of any of these secrets = full impersonation of the aeonframework identity across the org, or full drain of API credit, or takeover of the notification fan-out (Telegram/Discord/Slack chatops)

**Fix:**
```yaml
# BEFORE (secret referenced directly at job scope):
jobs:
  run:
    permissions: { contents: write }
    steps:
      - run: echo "${{ secrets.GH_GLOBAL }}"
# AFTER (gate the job behind a dedicated GitHub Environment):
jobs:
  run:
    environment: chain-runner  # or `production` — must be created in repo Settings > Environments first
    permissions: { contents: write }
    steps:
      - run: echo "$_GH_GLOBAL"
        env:
          _GH_GLOBAL: ${{ secrets.GH_GLOBAL }}  # now sourced from the environment scope
```

**Status:** Manual review required · **Fingerprint:** `492f5627d723`

---

### [HIGH] zizmor/secrets-outside-env — Run fleet task runner
**File:** `.github/workflows/fleet-runner.yml` · **Step:** `Run fleet task runner` · **Line:** 287
**Pattern:**
```yaml
CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

**Attack chain:**
1. **Entry:** any trigger that reaches this job — for messages.yml/chain-runner.yml, the `*/5 * * * *` schedule + `repository_dispatch` events; for fleet-runner.yml, `workflow_dispatch` and `schedule`
2. **Vector:** repo-scoped secret is available to every job in every workflow with no environment gate; a compromised action or a malicious workflow_dispatch input that reaches a bash sink can exfiltrate the secret without any deploy-review approval
3. **Sink:** `CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}` — no `environment:` clause on the job, so no reviewer approval, no branch protection, and no logging tie-back beyond the repo-audit-log
4. **Reachable secrets:** GH_GLOBAL (org-wide PAT), AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN (subscription auth), GITLAWB_*_PEM (fleet keys), Telegram/Discord/Slack tokens, Anthropic/xAI/CoinGecko/Alchemy keys
5. **Blast radius:** compromise of any of these secrets = full impersonation of the aeonframework identity across the org, or full drain of API credit, or takeover of the notification fan-out (Telegram/Discord/Slack chatops)

**Fix:**
```yaml
# BEFORE (secret referenced directly at job scope):
jobs:
  run:
    permissions: { contents: write }
    steps:
      - run: echo "${{ secrets.GH_GLOBAL }}"
# AFTER (gate the job behind a dedicated GitHub Environment):
jobs:
  run:
    environment: chain-runner  # or `production` — must be created in repo Settings > Environments first
    permissions: { contents: write }
    steps:
      - run: echo "$_GH_GLOBAL"
        env:
          _GH_GLOBAL: ${{ secrets.GH_GLOBAL }}  # now sourced from the environment scope
```

**Status:** Manual review required · **Fingerprint:** `9e568b8ce48d`

---

### [HIGH] actionlint/SC2086 — Run fleet task runner
**File:** `.github/workflows/fleet-runner.yml` · **Step:** `Run fleet task runner` · **Line:** 294
**Pattern:**
```yaml
shellcheck reported issue in this script: SC2086:info:6:82: Double quote to prevent globbing and word splitting
```

**Attack chain:**
1. **Entry:** workflow_dispatch on fleet-runner — external actor with `actions:write` on the repo (only the aeonframework identity today, but bar for compromise is low with unrotated PATs)
2. **Vector:** `inputs.agent` reaches `$AGENT` env → unquoted `$AGENT` in `--agent $AGENT` → word split lets a payload like `foo --secret-leak $(cat /etc/passwd)` inject shell arguments
3. **Sink:** line 297 `ARGS="$ARGS --agent $AGENT"` inside `run:` of `Run fleet task runner`
4. **Reachable secrets:** CLAUDE_CODE_OAUTH_TOKEN, GH_TOKEN (GITHUB_TOKEN)
5. **Blast radius:** argument injection into task-runner.mjs — could exfiltrate the CLAUDE_CODE_OAUTH_TOKEN or GITHUB_TOKEN via a crafted --agent value if any downstream command interpolates it into a shell

**Fix:**
```yaml
# BEFORE:
ARGS="$ARGS --agent $AGENT"
# AFTER (quote everywhere the value reaches the shell; use an array to avoid word-split entirely):
EXTRA_ARGS=()
[ -n "$AGENT" ] && EXTRA_ARGS+=(--agent "$AGENT")
# ...then invoke:
node prototypes/gitlawb-safety/task-runner.mjs once "${EXTRA_ARGS[@]}"
```

**Status:** Manual review required · **Fingerprint:** `a4607c388772`

---

### [HIGH] zizmor/secrets-outside-env — Sync state to aeon-private (Phase 1 dual-write)
**File:** `.github/workflows/fleet-runner.yml` · **Step:** `Sync state to aeon-private (Phase 1 dual-write)` · **Line:** 354
**Pattern:**
```yaml
AEON_PRIVATE_PAT: ${{ secrets.AEON_PRIVATE_PAT }}
```

**Attack chain:**
1. **Entry:** any trigger that reaches this job — for messages.yml/chain-runner.yml, the `*/5 * * * *` schedule + `repository_dispatch` events; for fleet-runner.yml, `workflow_dispatch` and `schedule`
2. **Vector:** repo-scoped secret is available to every job in every workflow with no environment gate; a compromised action or a malicious workflow_dispatch input that reaches a bash sink can exfiltrate the secret without any deploy-review approval
3. **Sink:** `AEON_PRIVATE_PAT: ${{ secrets.AEON_PRIVATE_PAT }}` — no `environment:` clause on the job, so no reviewer approval, no branch protection, and no logging tie-back beyond the repo-audit-log
4. **Reachable secrets:** GH_GLOBAL (org-wide PAT), AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN (subscription auth), GITLAWB_*_PEM (fleet keys), Telegram/Discord/Slack tokens, Anthropic/xAI/CoinGecko/Alchemy keys
5. **Blast radius:** compromise of any of these secrets = full impersonation of the aeonframework identity across the org, or full drain of API credit, or takeover of the notification fan-out (Telegram/Discord/Slack chatops)

**Fix:**
```yaml
# BEFORE (secret referenced directly at job scope):
jobs:
  run:
    permissions: { contents: write }
    steps:
      - run: echo "${{ secrets.GH_GLOBAL }}"
# AFTER (gate the job behind a dedicated GitHub Environment):
jobs:
  run:
    environment: chain-runner  # or `production` — must be created in repo Settings > Environments first
    permissions: { contents: write }
    steps:
      - run: echo "$_GH_GLOBAL"
        env:
          _GH_GLOBAL: ${{ secrets.GH_GLOBAL }}  # now sourced from the environment scope
```

**Status:** Manual review required · **Fingerprint:** `6a78074b9b49`

---

### [HIGH] zizmor/ref-version-mismatch — Checkout
**File:** `.github/workflows/lint.yml` · **Step:** `Checkout` · **Line:** 33
**Pattern:**
```yaml
uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4
```

**Attack chain:**
1. **Entry:** any run of the workflow
2. **Vector:** the comment says `v5` (or `v4`) but the pin points to a specific commit — if the comment ever drifts from the commit (during a review, a rebase, or a copy-paste), a reviewer approving the intent (`v5` = presumably-vetted release) may inadvertently approve an unvetted commit
3. **Sink:** `uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4` — the SHA is what runs, but the review signal is the version tag comment
4. **Reachable secrets:** same scope as unpinned-uses for the same job
5. **Blast radius:** low-friction supply-chain attack via reviewer misalignment — a malicious maintainer swaps SHA to attacker-controlled build while comment still reads `v5`

**Fix:**
```yaml
# BEFORE (comment drifted from the pinned SHA — reviewer sees the tag but the commit is what runs):
uses: actions/checkout@93cb6efe18208431cddfb8368fd83d5badbf9bfd # v5
# AFTER (verify the SHA is the current stable tag and update the comment to match):
uses: actions/checkout@<SHA of intended tag> # v5.0.0
```

**Status:** Manual review required · **Fingerprint:** `e04aa697aeac`

---

### [HIGH] zizmor/ref-version-mismatch — Checkout repo
**File:** `.github/workflows/messages.yml` · **Step:** `Checkout repo` · **Line:** 57
**Pattern:**
```yaml
uses: actions/checkout@93cb6efe18208431cddfb8368fd83d5badbf9bfd # v5
```

**Attack chain:**
1. **Entry:** any run of the workflow
2. **Vector:** the comment says `v5` (or `v4`) but the pin points to a specific commit — if the comment ever drifts from the commit (during a review, a rebase, or a copy-paste), a reviewer approving the intent (`v5` = presumably-vetted release) may inadvertently approve an unvetted commit
3. **Sink:** `uses: actions/checkout@93cb6efe18208431cddfb8368fd83d5badbf9bfd # v5` — the SHA is what runs, but the review signal is the version tag comment
4. **Reachable secrets:** same scope as unpinned-uses for the same job
5. **Blast radius:** low-friction supply-chain attack via reviewer misalignment — a malicious maintainer swaps SHA to attacker-controlled build while comment still reads `v5`

**Fix:**
```yaml
# BEFORE (comment drifted from the pinned SHA — reviewer sees the tag but the commit is what runs):
uses: actions/checkout@93cb6efe18208431cddfb8368fd83d5badbf9bfd # v5
# AFTER (verify the SHA is the current stable tag and update the comment to match):
uses: actions/checkout@<SHA of intended tag> # v5.0.0
```

**Status:** Manual review required · **Fingerprint:** `43037ab85149`

---

### [HIGH] zizmor/secrets-outside-env — Checkout repo
**File:** `.github/workflows/messages.yml` · **Step:** `Checkout repo` · **Line:** 59
**Pattern:**
```yaml
token: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }}
```

**Attack chain:**
1. **Entry:** any trigger that reaches this job — for messages.yml/chain-runner.yml, the `*/5 * * * *` schedule + `repository_dispatch` events; for fleet-runner.yml, `workflow_dispatch` and `schedule`
2. **Vector:** repo-scoped secret is available to every job in every workflow with no environment gate; a compromised action or a malicious workflow_dispatch input that reaches a bash sink can exfiltrate the secret without any deploy-review approval
3. **Sink:** `token: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }}` — no `environment:` clause on the job, so no reviewer approval, no branch protection, and no logging tie-back beyond the repo-audit-log
4. **Reachable secrets:** GH_GLOBAL (org-wide PAT), AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN (subscription auth), GITLAWB_*_PEM (fleet keys), Telegram/Discord/Slack tokens, Anthropic/xAI/CoinGecko/Alchemy keys
5. **Blast radius:** compromise of any of these secrets = full impersonation of the aeonframework identity across the org, or full drain of API credit, or takeover of the notification fan-out (Telegram/Discord/Slack chatops)

**Fix:**
```yaml
# BEFORE (secret referenced directly at job scope):
jobs:
  run:
    permissions: { contents: write }
    steps:
      - run: echo "${{ secrets.GH_GLOBAL }}"
# AFTER (gate the job behind a dedicated GitHub Environment):
jobs:
  run:
    environment: chain-runner  # or `production` — must be created in repo Settings > Environments first
    permissions: { contents: write }
    steps:
      - run: echo "$_GH_GLOBAL"
        env:
          _GH_GLOBAL: ${{ secrets.GH_GLOBAL }}  # now sourced from the environment scope
```

**Status:** Manual review required · **Fingerprint:** `e619ae84091a`

---

### [HIGH] zizmor/secrets-outside-env — Determine and dispatch scheduled skills
**File:** `.github/workflows/messages.yml` · **Step:** `Determine and dispatch scheduled skills` · **Line:** 68
**Pattern:**
```yaml
GH_TOKEN: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }}
```

**Attack chain:**
1. **Entry:** any trigger that reaches this job — for messages.yml/chain-runner.yml, the `*/5 * * * *` schedule + `repository_dispatch` events; for fleet-runner.yml, `workflow_dispatch` and `schedule`
2. **Vector:** repo-scoped secret is available to every job in every workflow with no environment gate; a compromised action or a malicious workflow_dispatch input that reaches a bash sink can exfiltrate the secret without any deploy-review approval
3. **Sink:** `GH_TOKEN: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }}` — no `environment:` clause on the job, so no reviewer approval, no branch protection, and no logging tie-back beyond the repo-audit-log
4. **Reachable secrets:** GH_GLOBAL (org-wide PAT), AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN (subscription auth), GITLAWB_*_PEM (fleet keys), Telegram/Discord/Slack tokens, Anthropic/xAI/CoinGecko/Alchemy keys
5. **Blast radius:** compromise of any of these secrets = full impersonation of the aeonframework identity across the org, or full drain of API credit, or takeover of the notification fan-out (Telegram/Discord/Slack chatops)

**Fix:**
```yaml
# BEFORE (secret referenced directly at job scope):
jobs:
  run:
    permissions: { contents: write }
    steps:
      - run: echo "${{ secrets.GH_GLOBAL }}"
# AFTER (gate the job behind a dedicated GitHub Environment):
jobs:
  run:
    environment: chain-runner  # or `production` — must be created in repo Settings > Environments first
    permissions: { contents: write }
    steps:
      - run: echo "$_GH_GLOBAL"
        env:
          _GH_GLOBAL: ${{ secrets.GH_GLOBAL }}  # now sourced from the environment scope
```

**Status:** Manual review required · **Fingerprint:** `eb3f904202e5`

---

### [HIGH] zizmor/secrets-outside-env — Collect and dispatch messages
**File:** `.github/workflows/messages.yml` · **Step:** `Collect and dispatch messages` · **Line:** 551
**Pattern:**
```yaml
GH_TOKEN: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }}
```

**Attack chain:**
1. **Entry:** any trigger that reaches this job — for messages.yml/chain-runner.yml, the `*/5 * * * *` schedule + `repository_dispatch` events; for fleet-runner.yml, `workflow_dispatch` and `schedule`
2. **Vector:** repo-scoped secret is available to every job in every workflow with no environment gate; a compromised action or a malicious workflow_dispatch input that reaches a bash sink can exfiltrate the secret without any deploy-review approval
3. **Sink:** `GH_TOKEN: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }}` — no `environment:` clause on the job, so no reviewer approval, no branch protection, and no logging tie-back beyond the repo-audit-log
4. **Reachable secrets:** GH_GLOBAL (org-wide PAT), AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN (subscription auth), GITLAWB_*_PEM (fleet keys), Telegram/Discord/Slack tokens, Anthropic/xAI/CoinGecko/Alchemy keys
5. **Blast radius:** compromise of any of these secrets = full impersonation of the aeonframework identity across the org, or full drain of API credit, or takeover of the notification fan-out (Telegram/Discord/Slack chatops)

**Fix:**
```yaml
# BEFORE (secret referenced directly at job scope):
jobs:
  run:
    permissions: { contents: write }
    steps:
      - run: echo "${{ secrets.GH_GLOBAL }}"
# AFTER (gate the job behind a dedicated GitHub Environment):
jobs:
  run:
    environment: chain-runner  # or `production` — must be created in repo Settings > Environments first
    permissions: { contents: write }
    steps:
      - run: echo "$_GH_GLOBAL"
        env:
          _GH_GLOBAL: ${{ secrets.GH_GLOBAL }}  # now sourced from the environment scope
```

**Status:** Manual review required · **Fingerprint:** `d07b94573673`

---

### [HIGH] zizmor/secrets-outside-env — Sync state to aeon-private (Phase 1 dual-write)
**File:** `.github/workflows/messages.yml` · **Step:** `Sync state to aeon-private (Phase 1 dual-write)` · **Line:** 648
**Pattern:**
```yaml
AEON_PRIVATE_PAT: ${{ secrets.AEON_PRIVATE_PAT }}
```

**Attack chain:**
1. **Entry:** any trigger that reaches this job — for messages.yml/chain-runner.yml, the `*/5 * * * *` schedule + `repository_dispatch` events; for fleet-runner.yml, `workflow_dispatch` and `schedule`
2. **Vector:** repo-scoped secret is available to every job in every workflow with no environment gate; a compromised action or a malicious workflow_dispatch input that reaches a bash sink can exfiltrate the secret without any deploy-review approval
3. **Sink:** `AEON_PRIVATE_PAT: ${{ secrets.AEON_PRIVATE_PAT }}` — no `environment:` clause on the job, so no reviewer approval, no branch protection, and no logging tie-back beyond the repo-audit-log
4. **Reachable secrets:** GH_GLOBAL (org-wide PAT), AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN (subscription auth), GITLAWB_*_PEM (fleet keys), Telegram/Discord/Slack tokens, Anthropic/xAI/CoinGecko/Alchemy keys
5. **Blast radius:** compromise of any of these secrets = full impersonation of the aeonframework identity across the org, or full drain of API credit, or takeover of the notification fan-out (Telegram/Discord/Slack chatops)

**Fix:**
```yaml
# BEFORE (secret referenced directly at job scope):
jobs:
  run:
    permissions: { contents: write }
    steps:
      - run: echo "${{ secrets.GH_GLOBAL }}"
# AFTER (gate the job behind a dedicated GitHub Environment):
jobs:
  run:
    environment: chain-runner  # or `production` — must be created in repo Settings > Environments first
    permissions: { contents: write }
    steps:
      - run: echo "$_GH_GLOBAL"
        env:
          _GH_GLOBAL: ${{ secrets.GH_GLOBAL }}  # now sourced from the environment scope
```

**Status:** Manual review required · **Fingerprint:** `9cff378b979c`

---

### [HIGH] zizmor/secrets-outside-env — Run
**File:** `.github/workflows/messages.yml` · **Step:** `Run` · **Line:** 717
**Pattern:**
```yaml
ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

**Attack chain:**
1. **Entry:** any trigger that reaches this job — for messages.yml/chain-runner.yml, the `*/5 * * * *` schedule + `repository_dispatch` events; for fleet-runner.yml, `workflow_dispatch` and `schedule`
2. **Vector:** repo-scoped secret is available to every job in every workflow with no environment gate; a compromised action or a malicious workflow_dispatch input that reaches a bash sink can exfiltrate the secret without any deploy-review approval
3. **Sink:** `ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}` — no `environment:` clause on the job, so no reviewer approval, no branch protection, and no logging tie-back beyond the repo-audit-log
4. **Reachable secrets:** GH_GLOBAL (org-wide PAT), AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN (subscription auth), GITLAWB_*_PEM (fleet keys), Telegram/Discord/Slack tokens, Anthropic/xAI/CoinGecko/Alchemy keys
5. **Blast radius:** compromise of any of these secrets = full impersonation of the aeonframework identity across the org, or full drain of API credit, or takeover of the notification fan-out (Telegram/Discord/Slack chatops)

**Fix:**
```yaml
# BEFORE (secret referenced directly at job scope):
jobs:
  run:
    permissions: { contents: write }
    steps:
      - run: echo "${{ secrets.GH_GLOBAL }}"
# AFTER (gate the job behind a dedicated GitHub Environment):
jobs:
  run:
    environment: chain-runner  # or `production` — must be created in repo Settings > Environments first
    permissions: { contents: write }
    steps:
      - run: echo "$_GH_GLOBAL"
        env:
          _GH_GLOBAL: ${{ secrets.GH_GLOBAL }}  # now sourced from the environment scope
```

**Status:** Manual review required · **Fingerprint:** `b38245804892`

---

### [HIGH] zizmor/ref-version-mismatch — Checkout aeon
**File:** `.github/workflows/sync-aeon-public-results.yml` · **Step:** `Checkout aeon` · **Line:** 29
**Pattern:**
```yaml
uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4
```

**Attack chain:**
1. **Entry:** any run of the workflow
2. **Vector:** the comment says `v5` (or `v4`) but the pin points to a specific commit — if the comment ever drifts from the commit (during a review, a rebase, or a copy-paste), a reviewer approving the intent (`v5` = presumably-vetted release) may inadvertently approve an unvetted commit
3. **Sink:** `uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4` — the SHA is what runs, but the review signal is the version tag comment
4. **Reachable secrets:** same scope as unpinned-uses for the same job
5. **Blast radius:** low-friction supply-chain attack via reviewer misalignment — a malicious maintainer swaps SHA to attacker-controlled build while comment still reads `v5`

**Fix:**
```yaml
# BEFORE (comment drifted from the pinned SHA — reviewer sees the tag but the commit is what runs):
uses: actions/checkout@93cb6efe18208431cddfb8368fd83d5badbf9bfd # v5
# AFTER (verify the SHA is the current stable tag and update the comment to match):
uses: actions/checkout@<SHA of intended tag> # v5.0.0
```

**Status:** Manual review required · **Fingerprint:** `f77041a532da`

---

### [HIGH] zizmor/ref-version-mismatch — Checkout fork
**File:** `.github/workflows/sync-upstream.yml` · **Step:** `Checkout fork` · **Line:** 23
**Pattern:**
```yaml
uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4
```

**Attack chain:**
1. **Entry:** any run of the workflow
2. **Vector:** the comment says `v5` (or `v4`) but the pin points to a specific commit — if the comment ever drifts from the commit (during a review, a rebase, or a copy-paste), a reviewer approving the intent (`v5` = presumably-vetted release) may inadvertently approve an unvetted commit
3. **Sink:** `uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4` — the SHA is what runs, but the review signal is the version tag comment
4. **Reachable secrets:** same scope as unpinned-uses for the same job
5. **Blast radius:** low-friction supply-chain attack via reviewer misalignment — a malicious maintainer swaps SHA to attacker-controlled build while comment still reads `v5`

**Fix:**
```yaml
# BEFORE (comment drifted from the pinned SHA — reviewer sees the tag but the commit is what runs):
uses: actions/checkout@93cb6efe18208431cddfb8368fd83d5badbf9bfd # v5
# AFTER (verify the SHA is the current stable tag and update the comment to match):
uses: actions/checkout@<SHA of intended tag> # v5.0.0
```

**Status:** Manual review required · **Fingerprint:** `63faf96ee9e4`

---

### [HIGH] zizmor/secrets-outside-env — Checkout fork
**File:** `.github/workflows/sync-upstream.yml` · **Step:** `Checkout fork` · **Line:** 29
**Pattern:**
```yaml
token: ${{ secrets.GH_GLOBAL }}
```

**Attack chain:**
1. **Entry:** any trigger that reaches this job — for messages.yml/chain-runner.yml, the `*/5 * * * *` schedule + `repository_dispatch` events; for fleet-runner.yml, `workflow_dispatch` and `schedule`
2. **Vector:** repo-scoped secret is available to every job in every workflow with no environment gate; a compromised action or a malicious workflow_dispatch input that reaches a bash sink can exfiltrate the secret without any deploy-review approval
3. **Sink:** `token: ${{ secrets.GH_GLOBAL }}` — no `environment:` clause on the job, so no reviewer approval, no branch protection, and no logging tie-back beyond the repo-audit-log
4. **Reachable secrets:** GH_GLOBAL (org-wide PAT), AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN (subscription auth), GITLAWB_*_PEM (fleet keys), Telegram/Discord/Slack tokens, Anthropic/xAI/CoinGecko/Alchemy keys
5. **Blast radius:** compromise of any of these secrets = full impersonation of the aeonframework identity across the org, or full drain of API credit, or takeover of the notification fan-out (Telegram/Discord/Slack chatops)

**Fix:**
```yaml
# BEFORE (secret referenced directly at job scope):
jobs:
  run:
    permissions: { contents: write }
    steps:
      - run: echo "${{ secrets.GH_GLOBAL }}"
# AFTER (gate the job behind a dedicated GitHub Environment):
jobs:
  run:
    environment: chain-runner  # or `production` — must be created in repo Settings > Environments first
    permissions: { contents: write }
    steps:
      - run: echo "$_GH_GLOBAL"
        env:
          _GH_GLOBAL: ${{ secrets.GH_GLOBAL }}  # now sourced from the environment scope
```

**Status:** Manual review required · **Fingerprint:** `7b4cecdf97db`

---

### [HIGH] zizmor/secrets-outside-env — Open or update PR
**File:** `.github/workflows/sync-upstream.yml` · **Step:** `Open or update PR` · **Line:** 76
**Pattern:**
```yaml
GH_TOKEN: ${{ secrets.GH_GLOBAL }}
```

**Attack chain:**
1. **Entry:** any trigger that reaches this job — for messages.yml/chain-runner.yml, the `*/5 * * * *` schedule + `repository_dispatch` events; for fleet-runner.yml, `workflow_dispatch` and `schedule`
2. **Vector:** repo-scoped secret is available to every job in every workflow with no environment gate; a compromised action or a malicious workflow_dispatch input that reaches a bash sink can exfiltrate the secret without any deploy-review approval
3. **Sink:** `GH_TOKEN: ${{ secrets.GH_GLOBAL }}` — no `environment:` clause on the job, so no reviewer approval, no branch protection, and no logging tie-back beyond the repo-audit-log
4. **Reachable secrets:** GH_GLOBAL (org-wide PAT), AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN (subscription auth), GITLAWB_*_PEM (fleet keys), Telegram/Discord/Slack tokens, Anthropic/xAI/CoinGecko/Alchemy keys
5. **Blast radius:** compromise of any of these secrets = full impersonation of the aeonframework identity across the org, or full drain of API credit, or takeover of the notification fan-out (Telegram/Discord/Slack chatops)

**Fix:**
```yaml
# BEFORE (secret referenced directly at job scope):
jobs:
  run:
    permissions: { contents: write }
    steps:
      - run: echo "${{ secrets.GH_GLOBAL }}"
# AFTER (gate the job behind a dedicated GitHub Environment):
jobs:
  run:
    environment: chain-runner  # or `production` — must be created in repo Settings > Environments first
    permissions: { contents: write }
    steps:
      - run: echo "$_GH_GLOBAL"
        env:
          _GH_GLOBAL: ${{ secrets.GH_GLOBAL }}  # now sourced from the environment scope
```

**Status:** Manual review required · **Fingerprint:** `8ea38df05599`

---

## Medium findings

| # | Rule | File | Line | Step |
|---|---|---|---|---|
| 1 | `zizmor/artipacked` | `.github/workflows/aeon.yml` | 83 | Early checkout |
| 2 | `zizmor/artipacked` | `.github/workflows/aeon.yml` | 119 | Checkout repo |
| 3 | `actionlint/SC2129` | `.github/workflows/aeon.yml` | 286 | line286 |
| 4 | `actionlint/SC2129` | `.github/workflows/aeon.yml` | 601 | Log token usage |
| 5 | `zizmor/artipacked` | `.github/workflows/chain-runner.yml` | 28 | Checkout repo |
| 6 | `actionlint/SC2034` | `.github/workflows/chain-runner.yml` | 42 | Run chain |
| 7 | `actionlint/SC2129` | `.github/workflows/chain-runner.yml` | 42 | Run chain |
| 8 | `actionlint/SC2155` | `.github/workflows/chain-runner.yml` | 42 | Run chain |
| 9 | `zizmor/artipacked` | `.github/workflows/fleet-runner.yml` | 56 | Checkout |
| 10 | `actionlint/SC2155` | `.github/workflows/fleet-runner.yml` | 179 | Bootstrap fleet registry |
| 11 | `zizmor/artipacked` | `.github/workflows/lint.yml` | 32 | Checkout |
| 12 | `zizmor/artipacked` | `.github/workflows/messages.yml` | 56 | Checkout repo |
| 13 | `actionlint/SC2034` | `.github/workflows/messages.yml` | 69 | Determine and dispatch scheduled skills |
| 14 | `actionlint/SC2129` | `.github/workflows/messages.yml` | 669 | Extract message |
| 15 | `actionlint/SC2129` | `.github/workflows/messages.yml` | 734 | Run |
| 16 | `actionlint/SC2129` | `.github/workflows/messages.yml` | 815 | Log token usage |
| 17 | `zizmor/artipacked` | `.github/workflows/sync-aeon-public-results.yml` | 28 | Checkout aeon |
| 18 | `zizmor/artipacked` | `.github/workflows/sync-upstream.yml` | 22 | Checkout fork |

## Low findings

| # | Rule | File | Line | Step |
|---|---|---|---|---|
| 1 | `zizmor/anonymous-definition` | `.github/workflows/aeon.yml` | 72 | line72 |
| 2 | `zizmor/undocumented-permissions` | `.github/workflows/aeon.yml` | 77 | line77 |
| 3 | `zizmor/template-injection` | `.github/workflows/aeon.yml` | 98 | Determine skill |
| 4 | `zizmor/template-injection` | `.github/workflows/aeon.yml` | 112 | Check if there's work |
| 5 | `zizmor/template-injection` | `.github/workflows/aeon.yml` | 150 | Validate skill secrets |
| 6 | `zizmor/template-injection` | `.github/workflows/aeon.yml` | 194 | Run pre-fetch scripts |
| 7 | `zizmor/template-injection` | `.github/workflows/aeon.yml` | 288 | line288 |
| 8 | `zizmor/template-injection` | `.github/workflows/aeon.yml` | 480 | line480 |
| 9 | `zizmor/template-injection` | `.github/workflows/aeon.yml` | 602 | Log token usage |
| 10 | `zizmor/template-injection` | `.github/workflows/aeon.yml` | 625 | Track token costs |
| 11 | `zizmor/template-injection` | `.github/workflows/aeon.yml` | 630 | Capture skill output |
| 12 | `zizmor/template-injection` | `.github/workflows/aeon.yml` | 651 | Analyze skill output |
| 13 | `zizmor/template-injection` | `.github/workflows/aeon.yml` | 752 | Convert feed outputs |
| 14 | `zizmor/template-injection` | `.github/workflows/aeon.yml` | 863 | Commit results |
| 15 | `zizmor/template-injection` | `.github/workflows/aeon.yml` | 927 | Update cron state |
| 16 | `zizmor/anonymous-definition` | `.github/workflows/chain-runner.yml` | 20 | Chain Runner |
| 17 | `zizmor/undocumented-permissions` | `.github/workflows/chain-runner.yml` | 24 | Chain Runner |
| 18 | `zizmor/concurrency-limits` | `.github/workflows/fleet-runner.yml` | 4 | Fleet Runner |
| 19 | `zizmor/anonymous-definition` | `.github/workflows/fleet-runner.yml` | 44 | line44 |
| 20 | `zizmor/undocumented-permissions` | `.github/workflows/fleet-runner.yml` | 48 | line48 |
| 21 | `zizmor/template-injection` | `.github/workflows/fleet-runner.yml` | 150 | Restore fleet identities |
| 22 | `zizmor/template-injection` | `.github/workflows/fleet-runner.yml` | 315 | Commit results |
| 23 | `zizmor/template-injection` | `.github/workflows/fleet-runner.yml` | 347 | Notify |
| 24 | `zizmor/anonymous-definition` | `.github/workflows/messages.yml` | 47 | line47 |
| 25 | `zizmor/anonymous-definition` | `.github/workflows/messages.yml` | 651 | Sync state to aeon-private (Phase 1 dual-write) |
| 26 | `zizmor/undocumented-permissions` | `.github/workflows/messages.yml` | 658 | Sync state to aeon-private (Phase 1 dual-write) |
| 27 | `zizmor/template-injection` | `.github/workflows/messages.yml` | 670 | Extract message |
| 28 | `zizmor/anonymous-definition` | `.github/workflows/sync-aeon-public-results.yml` | 23 | Sync from public mirror |
| 29 | `zizmor/anonymous-definition` | `.github/workflows/sync-upstream.yml` | 16 | Sync from upstream |
| 30 | `zizmor/undocumented-permissions` | `.github/workflows/sync-upstream.yml` | 19 | Sync from upstream |
| 31 | `zizmor/template-injection` | `.github/workflows/sync-upstream.yml` | 71 | Push sync branch |
| 32 | `zizmor/template-injection` | `.github/workflows/sync-upstream.yml` | 78 | Open or update PR |

## Carried over (unchanged)

_None — bootstrap run._

## Resolved since (no prior audit)

_None — bootstrap run._

## Source status

- zizmor 1.25.2 (via `.audit-bin/zizmor`): **ok** — 125 raw results, 3 rules → Critical, 3 rules → High per SKILL mapping
- actionlint 1.7.12 (via `.audit-bin/actionlint`): **ok** — 20 shellcheck results, 2 upgraded to High under the `SC2086` + `${{ github.* }}` rule
- hand-rolled backstops (`toJson-into-shell`, `persist-credentials + head.sha`, `GITHUB_ENV` write injection, fleet inputs passthrough, mutable third-party ref): **ok** — 0 hits (April 11 `messages.yml:577` pattern remains fixed)

## Top attack chains to read first

1. `zizmor/unpinned-uses` on `aeon.yml:85/121/133` — every skill run pulls unpinned `actions/checkout@v5` and `actions/setup-node@v5`; a moved tag or maintainer compromise on either action gives an attacker `contents:write` + `pull-requests:write` on this repo, i.e. the ability to self-modify the aeon agent between two runs.
2. `zizmor/secrets-outside-env` × 43 across `messages.yml`, `fleet-runner.yml`, `chain-runner.yml`, `sync-upstream.yml` — every sensitive secret (`GH_GLOBAL`, `AEON_PRIVATE_PAT`, `CLAUDE_CODE_OAUTH_TOKEN`, `GITLAWB_*_PEM`, notification tokens, API keys) is repo-scoped; no environment gate, no reviewer approval, no per-run audit trail. One compromised action or one malicious workflow_dispatch input landing in a bash sink is enough to exfiltrate.
3. `actionlint/SC2086` on `fleet-runner.yml:294` — unquoted `$AGENT` (originating from `inputs.agent` on workflow_dispatch) reaches `--agent $AGENT` in the fleet task-runner invocation. A crafted input like `x --secret-leak $(...)` word-splits into extra CLI args. Blast is bounded by task-runner.mjs's arg parsing, but the CLAUDE_CODE_OAUTH_TOKEN and GITHUB_TOKEN are both in scope.

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
a4607c388772 severity=High status=manual rule=actionlint/SC2086 file=.github/workflows/fleet-runner.yml step=Run_fleet_task_runner
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
334c42a63d7c severity=Medium status=manual rule=actionlint/SC2129 file=.github/workflows/aeon.yml step=line286
7a1f9fdf91af severity=Medium status=manual rule=actionlint/SC2129 file=.github/workflows/aeon.yml step=Log_token_usage
d2fc7a994dfa severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/chain-runner.yml step=Checkout_repo
702850a97b82 severity=Medium status=manual rule=actionlint/SC2034 file=.github/workflows/chain-runner.yml step=Run_chain
dd98f1f6a2c9 severity=Medium status=manual rule=actionlint/SC2129 file=.github/workflows/chain-runner.yml step=Run_chain
29d03232aa7d severity=Medium status=manual rule=actionlint/SC2155 file=.github/workflows/chain-runner.yml step=Run_chain
66f9cf0a3bde severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/fleet-runner.yml step=Checkout
5d41bf641832 severity=Medium status=manual rule=actionlint/SC2155 file=.github/workflows/fleet-runner.yml step=Bootstrap_fleet_registry
20e02889fa19 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/lint.yml step=Checkout
026cbff74a33 severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/messages.yml step=Checkout_repo
18034f95d5c4 severity=Medium status=manual rule=actionlint/SC2034 file=.github/workflows/messages.yml step=Determine_and_dispatch_scheduled_skills
a29cbcbd68f8 severity=Medium status=manual rule=actionlint/SC2129 file=.github/workflows/messages.yml step=Extract_message
6891f7605ed3 severity=Medium status=manual rule=actionlint/SC2129 file=.github/workflows/messages.yml step=Run
698da72eb125 severity=Medium status=manual rule=actionlint/SC2129 file=.github/workflows/messages.yml step=Log_token_usage
e227de85a27c severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/sync-aeon-public-results.yml step=Checkout_aeon
7c001f1bd15a severity=Medium status=manual rule=zizmor/artipacked file=.github/workflows/sync-upstream.yml step=Checkout_fork
785abd2ebb28 severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/aeon.yml step=line72
dd80fdbef2c4 severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/aeon.yml step=line77
f102d53867b2 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Determine_skill
5535ba0c284b severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Check_if_there's_work
51de415c8adb severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Validate_skill_secrets
b63d3b0e1177 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Run_pre-fetch_scripts
9e2d05e269a4 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=line288
0161d10d9ac4 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=line480
1b9eeff4363e severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Log_token_usage
051949b55347 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Track_token_costs
7aafea20960b severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Capture_skill_output
3332f8b86f42 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Analyze_skill_output
5ba103396fae severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Convert_feed_outputs
cf45a18cee4a severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Commit_results
f2d8296c0167 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/aeon.yml step=Update_cron_state
e0307ca942f4 severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/chain-runner.yml step=Chain_Runner
7b882d81724b severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/chain-runner.yml step=Chain_Runner
f2bd25abbf6c severity=Low status=manual rule=zizmor/concurrency-limits file=.github/workflows/fleet-runner.yml step=Fleet_Runner
f58e305ea1b5 severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/fleet-runner.yml step=line44
e1b8430c54f1 severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/fleet-runner.yml step=line48
58b55d8838c8 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=Restore_fleet_identities
93c5d3921f5c severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=Commit_results
5b3558adc1dc severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/fleet-runner.yml step=Notify
762e0b5fef12 severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/messages.yml step=line47
ab0972e6be9a severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/messages.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
17e914f3a957 severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/messages.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
c8163d0d9e92 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/messages.yml step=Extract_message
2b2df0cba03e severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/sync-aeon-public-results.yml step=Sync_from_public_mirror
8b7aa1385c14 severity=Low status=manual rule=zizmor/anonymous-definition file=.github/workflows/sync-upstream.yml step=Sync_from_upstream
18d4cf1a9964 severity=Low status=manual rule=zizmor/undocumented-permissions file=.github/workflows/sync-upstream.yml step=Sync_from_upstream
f90eb9ea17da severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/sync-upstream.yml step=Push_sync_branch
0b8717f70ea1 severity=Low status=manual rule=zizmor/template-injection file=.github/workflows/sync-upstream.yml step=Open_or_update_PR
-->
