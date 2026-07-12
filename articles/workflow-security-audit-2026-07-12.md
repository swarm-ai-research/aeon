# Workflow Security Audit — 2026-07-12

**Verdict:** WORKFLOW_AUDIT_NEW_CRITICAL — 3 new critical finding(s)
**Repo:** [swarm-ai-research/aeon](https://github.com/swarm-ai-research/aeon)
**Files audited:** 7 (7 workflows, 0 composite actions)
**Findings this run:** 77 (3 critical, 17 high, 26 medium, 31 low)
**Delta vs (no prior audit):** 77 new, 0 reintroduced, 0 unchanged, 0 resolved
**Auto-fixed:** 0

## Regressions (previously-fixed findings now present again)

_None._

## New findings

### [CRITICAL] unpinned-uses — unpinned action reference
**File:** `.github/workflows/aeon.yml` · **Step:** `Early checkout` · **Line:** 85

**Pattern:**
```yaml
uses: actions/checkout@v5
```

**Attack chain:**
1. **Entry:** `workflow_dispatch, issues` — repo owner or scheduled cron dispatches the job.
2. **Vector:** third-party action `actions/checkout@v5` resolved by mutable tag/branch. A future compromise of the action's tag (or the maintainer namespace) replays into every run.
3. **Sink:** the resolved action runs with the workflow's `GITHUB_TOKEN` + any secrets exported in the surrounding `env:`.
4. **Reachable secrets:** AEON_PRIVATE_PAT, ALCHEMY_API_KEY, ANTHROPIC_API_KEY, BANKR_API_KEY, BANKR_LLM_KEY, CLAUDE_CODE_OAUTH_TOKEN…
5. **Blast radius:** action can arbitrary-exec on the runner, exfiltrate the OAuth token in-memory, push crafted commits, or steal the passthrough Claude/GH tokens the aeon runner holds. Compromise persists until pin is bumped.

**Fix:**
```yaml
# BEFORE
- uses: actions/checkout@v5
# AFTER — pin to a verified full-length commit SHA (look up the SHA of the tag on GitHub)
- uses: actions/checkout@<40-char-sha>  # v5
```

**Status:** Manual review required (SHA pinning needs operator verification of the intended commit)

---

### [CRITICAL] unpinned-uses — unpinned action reference
**File:** `.github/workflows/aeon.yml` · **Step:** `Checkout repo` · **Line:** 121

**Pattern:**
```yaml
uses: actions/checkout@v5
```

**Attack chain:**
1. **Entry:** `workflow_dispatch, issues` — repo owner or scheduled cron dispatches the job.
2. **Vector:** third-party action `actions/checkout@v5` resolved by mutable tag/branch. A future compromise of the action's tag (or the maintainer namespace) replays into every run.
3. **Sink:** the resolved action runs with the workflow's `GITHUB_TOKEN` + any secrets exported in the surrounding `env:`.
4. **Reachable secrets:** AEON_PRIVATE_PAT, ALCHEMY_API_KEY, ANTHROPIC_API_KEY, BANKR_API_KEY, BANKR_LLM_KEY, CLAUDE_CODE_OAUTH_TOKEN…
5. **Blast radius:** action can arbitrary-exec on the runner, exfiltrate the OAuth token in-memory, push crafted commits, or steal the passthrough Claude/GH tokens the aeon runner holds. Compromise persists until pin is bumped.

**Fix:**
```yaml
# BEFORE
- uses: actions/checkout@v5
# AFTER — pin to a verified full-length commit SHA (look up the SHA of the tag on GitHub)
- uses: actions/checkout@<40-char-sha>  # v5
```

**Status:** Manual review required (SHA pinning needs operator verification of the intended commit)

---

### [CRITICAL] unpinned-uses — unpinned action reference
**File:** `.github/workflows/aeon.yml` · **Step:** `Setup Node.js` · **Line:** 133

**Pattern:**
```yaml
uses: actions/setup-node@v5
```

**Attack chain:**
1. **Entry:** `workflow_dispatch, issues` — repo owner or scheduled cron dispatches the job.
2. **Vector:** third-party action `actions/setup-node@v5` resolved by mutable tag/branch. A future compromise of the action's tag (or the maintainer namespace) replays into every run.
3. **Sink:** the resolved action runs with the workflow's `GITHUB_TOKEN` + any secrets exported in the surrounding `env:`.
4. **Reachable secrets:** AEON_PRIVATE_PAT, ALCHEMY_API_KEY, ANTHROPIC_API_KEY, BANKR_API_KEY, BANKR_LLM_KEY, CLAUDE_CODE_OAUTH_TOKEN…
5. **Blast radius:** action can arbitrary-exec on the runner, exfiltrate the OAuth token in-memory, push crafted commits, or steal the passthrough Claude/GH tokens the aeon runner holds. Compromise persists until pin is bumped.

**Fix:**
```yaml
# BEFORE
- uses: actions/setup-node@v5
# AFTER — pin to a verified full-length commit SHA (look up the SHA of the tag on GitHub)
- uses: actions/setup-node@<40-char-sha>  # v5
```

**Status:** Manual review required (SHA pinning needs operator verification of the intended commit)

---

### [HIGH] secrets-outside-env — secrets referenced without a dedicated environment
**File:** `.github/workflows/chain-runner.yml` · **Step:** `Checkout repo` · **Line:** 31

**Pattern:**
```yaml
token: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }}
```

**Attack chain:**
1. **Entry:** `workflow_dispatch` — job runs without a GitHub deployment environment gate.
2. **Vector:** `secrets.GH_GLOBAL` is accessed at job/step scope; any prior step in the same job (including malicious third-party actions) can read it via `$SECRET` or `$ENV`.
3. **Sink:** `run:` blocks and `with:` bindings inside the job.
4. **Reachable secrets:** AEON_PRIVATE_PAT, GH_GLOBAL, GITHUB_TOKEN
5. **Blast radius:** without an environment wall + required reviewers, one compromised step in this job exfiltrates every secret listed at job scope. Impact scales with the token's write scope.

**Fix:**
```yaml
# BEFORE — secret exposed at job/step scope
jobs:
  run:
    steps:
      - env:
          SECRET: ${{ secrets.SECRET }}

# AFTER — gate the job behind a GitHub deployment environment with required reviewers
jobs:
  run:
    environment: prod    # define under repo Settings → Environments
    steps:
      - env:
          SECRET: ${{ secrets.SECRET }}
```

**Status:** Manual review required (moving secrets behind a GitHub deployment environment is a workflow structural change)

---

### [HIGH] secrets-outside-env — secrets referenced without a dedicated environment
**File:** `.github/workflows/chain-runner.yml` · **Step:** `Run chain` · **Line:** 40

**Pattern:**
```yaml
GH_TOKEN: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }}
```

**Attack chain:**
1. **Entry:** `workflow_dispatch` — job runs without a GitHub deployment environment gate.
2. **Vector:** `secrets.GH_GLOBAL` is accessed at job/step scope; any prior step in the same job (including malicious third-party actions) can read it via `$SECRET` or `$ENV`.
3. **Sink:** `run:` blocks and `with:` bindings inside the job.
4. **Reachable secrets:** AEON_PRIVATE_PAT, GH_GLOBAL, GITHUB_TOKEN
5. **Blast radius:** without an environment wall + required reviewers, one compromised step in this job exfiltrates every secret listed at job scope. Impact scales with the token's write scope.

**Fix:**
```yaml
# BEFORE — secret exposed at job/step scope
jobs:
  run:
    steps:
      - env:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}

# AFTER — gate the job behind a GitHub deployment environment with required reviewers
jobs:
  run:
    environment: prod    # define under repo Settings → Environments
    steps:
      - env:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
```

**Status:** Manual review required (moving secrets behind a GitHub deployment environment is a workflow structural change)

---

### [HIGH] secrets-outside-env — secrets referenced without a dedicated environment
**File:** `.github/workflows/chain-runner.yml` · **Step:** `Update cron state` · **Line:** 288

**Pattern:**
```yaml
GH_TOKEN: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }}
```

**Attack chain:**
1. **Entry:** `workflow_dispatch` — job runs without a GitHub deployment environment gate.
2. **Vector:** `secrets.GH_GLOBAL` is accessed at job/step scope; any prior step in the same job (including malicious third-party actions) can read it via `$SECRET` or `$ENV`.
3. **Sink:** `run:` blocks and `with:` bindings inside the job.
4. **Reachable secrets:** AEON_PRIVATE_PAT, GH_GLOBAL, GITHUB_TOKEN
5. **Blast radius:** without an environment wall + required reviewers, one compromised step in this job exfiltrates every secret listed at job scope. Impact scales with the token's write scope.

**Fix:**
```yaml
# BEFORE — secret exposed at job/step scope
jobs:
  run:
    steps:
      - env:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}

# AFTER — gate the job behind a GitHub deployment environment with required reviewers
jobs:
  run:
    environment: prod    # define under repo Settings → Environments
    steps:
      - env:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
```

**Status:** Manual review required (moving secrets behind a GitHub deployment environment is a workflow structural change)

---

### [HIGH] secrets-outside-env — secrets referenced without a dedicated environment
**File:** `.github/workflows/chain-runner.yml` · **Step:** `Sync state to aeon-private (Phase 1 dual-write)` · **Line:** 347

**Pattern:**
```yaml
AEON_PRIVATE_PAT: ${{ secrets.AEON_PRIVATE_PAT }}
```

**Attack chain:**
1. **Entry:** `workflow_dispatch` — job runs without a GitHub deployment environment gate.
2. **Vector:** `secrets.AEON_PRIVATE_PAT` is accessed at job/step scope; any prior step in the same job (including malicious third-party actions) can read it via `$SECRET` or `$ENV`.
3. **Sink:** `run:` blocks and `with:` bindings inside the job.
4. **Reachable secrets:** AEON_PRIVATE_PAT, GH_GLOBAL, GITHUB_TOKEN
5. **Blast radius:** without an environment wall + required reviewers, one compromised step in this job exfiltrates every secret listed at job scope. Impact scales with the token's write scope.

**Fix:**
```yaml
# BEFORE — secret exposed at job/step scope
jobs:
  run:
    steps:
      - env:
          AEON_PRIVATE_PAT: ${{ secrets.AEON_PRIVATE_PAT }}

# AFTER — gate the job behind a GitHub deployment environment with required reviewers
jobs:
  run:
    environment: prod    # define under repo Settings → Environments
    steps:
      - env:
          AEON_PRIVATE_PAT: ${{ secrets.AEON_PRIVATE_PAT }}
```

**Status:** Manual review required (moving secrets behind a GitHub deployment environment is a workflow structural change)

---

### [HIGH] secrets-outside-env — secrets referenced without a dedicated environment
**File:** `.github/workflows/fleet-runner.yml` · **Step:** `Restore fleet identities` · **Line:** 150

**Pattern:**
```yaml
echo '${{ secrets.GITLAWB_OPERATOR_PEM }}' > ~/.gitlawb/identity.pem
```

**Attack chain:**
1. **Entry:** `schedule, workflow_dispatch` — job runs without a GitHub deployment environment gate.
2. **Vector:** `secrets.GITLAWB_OPERATOR_PEM` is accessed at job/step scope; any prior step in the same job (including malicious third-party actions) can read it via `$SECRET` or `$ENV`.
3. **Sink:** `run:` blocks and `with:` bindings inside the job.
4. **Reachable secrets:** AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN, GITHUB_TOKEN, GITLAWB_DEPLOYER_PEM, GITLAWB_OPERATOR_PEM, GITLAWB_OPERATOR_UCAN…
5. **Blast radius:** without an environment wall + required reviewers, one compromised step in this job exfiltrates every secret listed at job scope. Impact scales with the token's write scope.

**Fix:**
```yaml
# BEFORE — secret exposed at job/step scope
jobs:
  run:
    steps:
      - env:
          SECRET: ${{ secrets.SECRET }}

# AFTER — gate the job behind a GitHub deployment environment with required reviewers
jobs:
  run:
    environment: prod    # define under repo Settings → Environments
    steps:
      - env:
          SECRET: ${{ secrets.SECRET }}
```

**Status:** Manual review required (moving secrets behind a GitHub deployment environment is a workflow structural change)

---

### [HIGH] secrets-outside-env — secrets referenced without a dedicated environment
**File:** `.github/workflows/fleet-runner.yml` · **Step:** `Prefetch live Surplus prices (best-effort, outside sandbox)` · **Line:** 271

**Pattern:**
```yaml
SURPLUS_PRICING_URL: ${{ secrets.SURPLUS_PRICING_URL }}
```

**Attack chain:**
1. **Entry:** `schedule, workflow_dispatch` — job runs without a GitHub deployment environment gate.
2. **Vector:** `secrets.SURPLUS_PRICING_URL` is accessed at job/step scope; any prior step in the same job (including malicious third-party actions) can read it via `$SECRET` or `$ENV`.
3. **Sink:** `run:` blocks and `with:` bindings inside the job.
4. **Reachable secrets:** AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN, GITHUB_TOKEN, GITLAWB_DEPLOYER_PEM, GITLAWB_OPERATOR_PEM, GITLAWB_OPERATOR_UCAN…
5. **Blast radius:** without an environment wall + required reviewers, one compromised step in this job exfiltrates every secret listed at job scope. Impact scales with the token's write scope.

**Fix:**
```yaml
# BEFORE — secret exposed at job/step scope
jobs:
  run:
    steps:
      - env:
          SURPLUS_PRICING_URL: ${{ secrets.SURPLUS_PRICING_URL }}

# AFTER — gate the job behind a GitHub deployment environment with required reviewers
jobs:
  run:
    environment: prod    # define under repo Settings → Environments
    steps:
      - env:
          SURPLUS_PRICING_URL: ${{ secrets.SURPLUS_PRICING_URL }}
```

**Status:** Manual review required (moving secrets behind a GitHub deployment environment is a workflow structural change)

---

### [HIGH] secrets-outside-env — secrets referenced without a dedicated environment
**File:** `.github/workflows/fleet-runner.yml` · **Step:** `Run fleet task runner` · **Line:** 287

**Pattern:**
```yaml
CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

**Attack chain:**
1. **Entry:** `schedule, workflow_dispatch` — job runs without a GitHub deployment environment gate.
2. **Vector:** `secrets.CLAUDE_CODE_OAUTH_TOKEN` is accessed at job/step scope; any prior step in the same job (including malicious third-party actions) can read it via `$SECRET` or `$ENV`.
3. **Sink:** `run:` blocks and `with:` bindings inside the job.
4. **Reachable secrets:** AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN, GITHUB_TOKEN, GITLAWB_DEPLOYER_PEM, GITLAWB_OPERATOR_PEM, GITLAWB_OPERATOR_UCAN…
5. **Blast radius:** without an environment wall + required reviewers, one compromised step in this job exfiltrates every secret listed at job scope. Impact scales with the token's write scope.

**Fix:**
```yaml
# BEFORE — secret exposed at job/step scope
jobs:
  run:
    steps:
      - env:
          CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}

# AFTER — gate the job behind a GitHub deployment environment with required reviewers
jobs:
  run:
    environment: prod    # define under repo Settings → Environments
    steps:
      - env:
          CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

**Status:** Manual review required (moving secrets behind a GitHub deployment environment is a workflow structural change)

---

### [HIGH] secrets-outside-env — secrets referenced without a dedicated environment
**File:** `.github/workflows/fleet-runner.yml` · **Step:** `Sync state to aeon-private (Phase 1 dual-write)` · **Line:** 354

**Pattern:**
```yaml
AEON_PRIVATE_PAT: ${{ secrets.AEON_PRIVATE_PAT }}
```

**Attack chain:**
1. **Entry:** `schedule, workflow_dispatch` — job runs without a GitHub deployment environment gate.
2. **Vector:** `secrets.AEON_PRIVATE_PAT` is accessed at job/step scope; any prior step in the same job (including malicious third-party actions) can read it via `$SECRET` or `$ENV`.
3. **Sink:** `run:` blocks and `with:` bindings inside the job.
4. **Reachable secrets:** AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN, GITHUB_TOKEN, GITLAWB_DEPLOYER_PEM, GITLAWB_OPERATOR_PEM, GITLAWB_OPERATOR_UCAN…
5. **Blast radius:** without an environment wall + required reviewers, one compromised step in this job exfiltrates every secret listed at job scope. Impact scales with the token's write scope.

**Fix:**
```yaml
# BEFORE — secret exposed at job/step scope
jobs:
  run:
    steps:
      - env:
          AEON_PRIVATE_PAT: ${{ secrets.AEON_PRIVATE_PAT }}

# AFTER — gate the job behind a GitHub deployment environment with required reviewers
jobs:
  run:
    environment: prod    # define under repo Settings → Environments
    steps:
      - env:
          AEON_PRIVATE_PAT: ${{ secrets.AEON_PRIVATE_PAT }}
```

**Status:** Manual review required (moving secrets behind a GitHub deployment environment is a workflow structural change)

---

### [HIGH] secrets-outside-env — secrets referenced without a dedicated environment
**File:** `.github/workflows/messages.yml` · **Step:** `Checkout repo` · **Line:** 59

**Pattern:**
```yaml
token: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }}
```

**Attack chain:**
1. **Entry:** `schedule, workflow_dispatch, repository_dispatch` — job runs without a GitHub deployment environment gate.
2. **Vector:** `secrets.GH_GLOBAL` is accessed at job/step scope; any prior step in the same job (including malicious third-party actions) can read it via `$SECRET` or `$ENV`.
3. **Sink:** `run:` blocks and `with:` bindings inside the job.
4. **Reachable secrets:** AEON_PRIVATE_PAT, ALCHEMY_API_KEY, ANTHROPIC_API_KEY, CLAUDE_CODE_OAUTH_TOKEN, COINGECKO_API_KEY, DISCORD_BOT_TOKEN…
5. **Blast radius:** without an environment wall + required reviewers, one compromised step in this job exfiltrates every secret listed at job scope. Impact scales with the token's write scope.

**Fix:**
```yaml
# BEFORE — secret exposed at job/step scope
jobs:
  run:
    steps:
      - env:
          SECRET: ${{ secrets.SECRET }}

# AFTER — gate the job behind a GitHub deployment environment with required reviewers
jobs:
  run:
    environment: prod    # define under repo Settings → Environments
    steps:
      - env:
          SECRET: ${{ secrets.SECRET }}
```

**Status:** Manual review required (moving secrets behind a GitHub deployment environment is a workflow structural change)

---

### [HIGH] secrets-outside-env — secrets referenced without a dedicated environment
**File:** `.github/workflows/messages.yml` · **Step:** `Determine and dispatch scheduled skills` · **Line:** 68

**Pattern:**
```yaml
GH_TOKEN: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }}
```

**Attack chain:**
1. **Entry:** `schedule, workflow_dispatch, repository_dispatch` — job runs without a GitHub deployment environment gate.
2. **Vector:** `secrets.GH_GLOBAL` is accessed at job/step scope; any prior step in the same job (including malicious third-party actions) can read it via `$SECRET` or `$ENV`.
3. **Sink:** `run:` blocks and `with:` bindings inside the job.
4. **Reachable secrets:** AEON_PRIVATE_PAT, ALCHEMY_API_KEY, ANTHROPIC_API_KEY, CLAUDE_CODE_OAUTH_TOKEN, COINGECKO_API_KEY, DISCORD_BOT_TOKEN…
5. **Blast radius:** without an environment wall + required reviewers, one compromised step in this job exfiltrates every secret listed at job scope. Impact scales with the token's write scope.

**Fix:**
```yaml
# BEFORE — secret exposed at job/step scope
jobs:
  run:
    steps:
      - env:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}

# AFTER — gate the job behind a GitHub deployment environment with required reviewers
jobs:
  run:
    environment: prod    # define under repo Settings → Environments
    steps:
      - env:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
```

**Status:** Manual review required (moving secrets behind a GitHub deployment environment is a workflow structural change)

---

### [HIGH] secrets-outside-env — secrets referenced without a dedicated environment
**File:** `.github/workflows/messages.yml` · **Step:** `Collect and dispatch messages` · **Line:** 551

**Pattern:**
```yaml
GH_TOKEN: ${{ secrets.GH_GLOBAL || secrets.GITHUB_TOKEN }}
```

**Attack chain:**
1. **Entry:** `schedule, workflow_dispatch, repository_dispatch` — job runs without a GitHub deployment environment gate.
2. **Vector:** `secrets.GH_GLOBAL` is accessed at job/step scope; any prior step in the same job (including malicious third-party actions) can read it via `$SECRET` or `$ENV`.
3. **Sink:** `run:` blocks and `with:` bindings inside the job.
4. **Reachable secrets:** AEON_PRIVATE_PAT, ALCHEMY_API_KEY, ANTHROPIC_API_KEY, CLAUDE_CODE_OAUTH_TOKEN, COINGECKO_API_KEY, DISCORD_BOT_TOKEN…
5. **Blast radius:** without an environment wall + required reviewers, one compromised step in this job exfiltrates every secret listed at job scope. Impact scales with the token's write scope.

**Fix:**
```yaml
# BEFORE — secret exposed at job/step scope
jobs:
  run:
    steps:
      - env:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}

# AFTER — gate the job behind a GitHub deployment environment with required reviewers
jobs:
  run:
    environment: prod    # define under repo Settings → Environments
    steps:
      - env:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
```

**Status:** Manual review required (moving secrets behind a GitHub deployment environment is a workflow structural change)

---

### [HIGH] secrets-outside-env — secrets referenced without a dedicated environment
**File:** `.github/workflows/messages.yml` · **Step:** `Sync state to aeon-private (Phase 1 dual-write)` · **Line:** 648

**Pattern:**
```yaml
AEON_PRIVATE_PAT: ${{ secrets.AEON_PRIVATE_PAT }}
```

**Attack chain:**
1. **Entry:** `schedule, workflow_dispatch, repository_dispatch` — job runs without a GitHub deployment environment gate.
2. **Vector:** `secrets.AEON_PRIVATE_PAT` is accessed at job/step scope; any prior step in the same job (including malicious third-party actions) can read it via `$SECRET` or `$ENV`.
3. **Sink:** `run:` blocks and `with:` bindings inside the job.
4. **Reachable secrets:** AEON_PRIVATE_PAT, ALCHEMY_API_KEY, ANTHROPIC_API_KEY, CLAUDE_CODE_OAUTH_TOKEN, COINGECKO_API_KEY, DISCORD_BOT_TOKEN…
5. **Blast radius:** without an environment wall + required reviewers, one compromised step in this job exfiltrates every secret listed at job scope. Impact scales with the token's write scope.

**Fix:**
```yaml
# BEFORE — secret exposed at job/step scope
jobs:
  run:
    steps:
      - env:
          AEON_PRIVATE_PAT: ${{ secrets.AEON_PRIVATE_PAT }}

# AFTER — gate the job behind a GitHub deployment environment with required reviewers
jobs:
  run:
    environment: prod    # define under repo Settings → Environments
    steps:
      - env:
          AEON_PRIVATE_PAT: ${{ secrets.AEON_PRIVATE_PAT }}
```

**Status:** Manual review required (moving secrets behind a GitHub deployment environment is a workflow structural change)

---

### [HIGH] secrets-outside-env — secrets referenced without a dedicated environment
**File:** `.github/workflows/messages.yml` · **Step:** `Run` · **Line:** 717

**Pattern:**
```yaml
ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

**Attack chain:**
1. **Entry:** `schedule, workflow_dispatch, repository_dispatch` — job runs without a GitHub deployment environment gate.
2. **Vector:** `secrets.ANTHROPIC_API_KEY` is accessed at job/step scope; any prior step in the same job (including malicious third-party actions) can read it via `$SECRET` or `$ENV`.
3. **Sink:** `run:` blocks and `with:` bindings inside the job.
4. **Reachable secrets:** AEON_PRIVATE_PAT, ALCHEMY_API_KEY, ANTHROPIC_API_KEY, CLAUDE_CODE_OAUTH_TOKEN, COINGECKO_API_KEY, DISCORD_BOT_TOKEN…
5. **Blast radius:** without an environment wall + required reviewers, one compromised step in this job exfiltrates every secret listed at job scope. Impact scales with the token's write scope.

**Fix:**
```yaml
# BEFORE — secret exposed at job/step scope
jobs:
  run:
    steps:
      - env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

# AFTER — gate the job behind a GitHub deployment environment with required reviewers
jobs:
  run:
    environment: prod    # define under repo Settings → Environments
    steps:
      - env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

**Status:** Manual review required (moving secrets behind a GitHub deployment environment is a workflow structural change)

---

### [HIGH] secrets-outside-env — secrets referenced without a dedicated environment
**File:** `.github/workflows/sync-upstream.yml` · **Step:** `Checkout fork` · **Line:** 29

**Pattern:**
```yaml
token: ${{ secrets.GH_GLOBAL }}
```

**Attack chain:**
1. **Entry:** `schedule, workflow_dispatch` — job runs without a GitHub deployment environment gate.
2. **Vector:** `secrets.GH_GLOBAL` is accessed at job/step scope; any prior step in the same job (including malicious third-party actions) can read it via `$SECRET` or `$ENV`.
3. **Sink:** `run:` blocks and `with:` bindings inside the job.
4. **Reachable secrets:** GH_GLOBAL
5. **Blast radius:** without an environment wall + required reviewers, one compromised step in this job exfiltrates every secret listed at job scope. Impact scales with the token's write scope.

**Fix:**
```yaml
# BEFORE — secret exposed at job/step scope
jobs:
  run:
    steps:
      - env:
          SECRET: ${{ secrets.SECRET }}

# AFTER — gate the job behind a GitHub deployment environment with required reviewers
jobs:
  run:
    environment: prod    # define under repo Settings → Environments
    steps:
      - env:
          SECRET: ${{ secrets.SECRET }}
```

**Status:** Manual review required (moving secrets behind a GitHub deployment environment is a workflow structural change)

---

### [HIGH] secrets-outside-env — secrets referenced without a dedicated environment
**File:** `.github/workflows/sync-upstream.yml` · **Step:** `Open or update PR` · **Line:** 76

**Pattern:**
```yaml
GH_TOKEN: ${{ secrets.GH_GLOBAL }}
```

**Attack chain:**
1. **Entry:** `schedule, workflow_dispatch` — job runs without a GitHub deployment environment gate.
2. **Vector:** `secrets.GH_GLOBAL` is accessed at job/step scope; any prior step in the same job (including malicious third-party actions) can read it via `$SECRET` or `$ENV`.
3. **Sink:** `run:` blocks and `with:` bindings inside the job.
4. **Reachable secrets:** GH_GLOBAL
5. **Blast radius:** without an environment wall + required reviewers, one compromised step in this job exfiltrates every secret listed at job scope. Impact scales with the token's write scope.

**Fix:**
```yaml
# BEFORE — secret exposed at job/step scope
jobs:
  run:
    steps:
      - env:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}

# AFTER — gate the job behind a GitHub deployment environment with required reviewers
jobs:
  run:
    environment: prod    # define under repo Settings → Environments
    steps:
      - env:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
```

**Status:** Manual review required (moving secrets behind a GitHub deployment environment is a workflow structural change)

---

### [HIGH] actionlint/shellcheck — shellcheck reported issue in this script
**File:** `.github/workflows/fleet-runner.yml` · **Step:** `Run fleet task runner` · **Line:** 294

**Pattern:**
```yaml
run: |
```

**Attack chain:**
1. **Entry:** `schedule, workflow_dispatch` — operator-triggered dispatch of the fleet runner.
2. **Vector:** `$ARGS` is built from `$AGENT` (which binds to `${{ inputs.agent }}`) and left unquoted on the `node …` invocation, so word-splitting + globbing happens on operator-supplied input.
3. **Sink:** `timeout 480 node prototypes/gitlawb-safety/task-runner.mjs … $ARGS` — expansion happens in the shell.
4. **Reachable secrets:** AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN, GITHUB_TOKEN, GITLAWB_DEPLOYER_PEM, GITLAWB_OPERATOR_PEM, GITLAWB_OPERATOR_UCAN…
5. **Blast radius:** operator with dispatch permission can smuggle shell metacharacters through `inputs.agent`, but the trigger is already write-authenticated so the marginal risk is confused-deputy + audit-log evasion, not privilege escalation.

**Fix:**
```yaml
# BEFORE — $ARGS unquoted; operator-supplied $AGENT can word-split
run: |
  ARGS=""
  [ -n "$AGENT" ] && ARGS="$ARGS --agent $AGENT"
  timeout 480 node prototypes/gitlawb-safety/task-runner.mjs loop --poll "$POLL" $ARGS

# AFTER — bash array preserves argument boundaries
run: |
  ARGS=()
  [ -n "$AGENT" ] && ARGS+=(--agent "$AGENT")
  timeout 480 node prototypes/gitlawb-safety/task-runner.mjs loop --poll "$POLL" "${ARGS[@]}"
```

**Status:** Manual review required (SC2086 on `$ARGS` needs a bash-array refactor, not the env-intermediary template)

---

### [HIGH] actionlint/shellcheck — shellcheck reported issue in this script
**File:** `.github/workflows/fleet-runner.yml` · **Step:** `Run fleet task runner` · **Line:** 294

**Pattern:**
```yaml
run: |
```

**Attack chain:**
1. **Entry:** `schedule, workflow_dispatch` — operator-triggered dispatch of the fleet runner.
2. **Vector:** `$ARGS` is built from `$AGENT` (which binds to `${{ inputs.agent }}`) and left unquoted on the `node …` invocation, so word-splitting + globbing happens on operator-supplied input.
3. **Sink:** `timeout 480 node prototypes/gitlawb-safety/task-runner.mjs … $ARGS` — expansion happens in the shell.
4. **Reachable secrets:** AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN, GITHUB_TOKEN, GITLAWB_DEPLOYER_PEM, GITLAWB_OPERATOR_PEM, GITLAWB_OPERATOR_UCAN…
5. **Blast radius:** operator with dispatch permission can smuggle shell metacharacters through `inputs.agent`, but the trigger is already write-authenticated so the marginal risk is confused-deputy + audit-log evasion, not privilege escalation.

**Fix:**
```yaml
# BEFORE — $ARGS unquoted; operator-supplied $AGENT can word-split
run: |
  ARGS=""
  [ -n "$AGENT" ] && ARGS="$ARGS --agent $AGENT"
  timeout 480 node prototypes/gitlawb-safety/task-runner.mjs loop --poll "$POLL" $ARGS

# AFTER — bash array preserves argument boundaries
run: |
  ARGS=()
  [ -n "$AGENT" ] && ARGS+=(--agent "$AGENT")
  timeout 480 node prototypes/gitlawb-safety/task-runner.mjs loop --poll "$POLL" "${ARGS[@]}"
```

**Status:** Manual review required (SC2086 on `$ARGS` needs a bash-array refactor, not the env-intermediary template)

---

### Medium & Low new findings (compact)

| Severity | Rule | File | Line | Step |
|---|---|---|---|---|
| Medium | `actionlint/shellcheck` | `.github/workflows/aeon.yml` | 286 | Run |
| Medium | `actionlint/shellcheck` | `.github/workflows/aeon.yml` | 601 | Log token usage |
| Medium | `actionlint/shellcheck` | `.github/workflows/chain-runner.yml` | 42 | Run chain |
| Medium | `actionlint/shellcheck` | `.github/workflows/chain-runner.yml` | 42 | Run chain |
| Medium | `actionlint/shellcheck` | `.github/workflows/chain-runner.yml` | 42 | Run chain |
| Medium | `actionlint/shellcheck` | `.github/workflows/chain-runner.yml` | 42 | Run chain |
| Medium | `actionlint/shellcheck` | `.github/workflows/chain-runner.yml` | 42 | Run chain |
| Medium | `actionlint/shellcheck` | `.github/workflows/chain-runner.yml` | 42 | Run chain |
| Medium | `actionlint/shellcheck` | `.github/workflows/chain-runner.yml` | 42 | Run chain |
| Medium | `actionlint/shellcheck` | `.github/workflows/chain-runner.yml` | 42 | Run chain |
| Medium | `actionlint/shellcheck` | `.github/workflows/fleet-runner.yml` | 179 | Bootstrap fleet registry |
| Medium | `actionlint/shellcheck` | `.github/workflows/fleet-runner.yml` | 179 | Bootstrap fleet registry |
| Medium | `actionlint/shellcheck` | `.github/workflows/fleet-runner.yml` | 179 | Bootstrap fleet registry |
| Medium | `actionlint/shellcheck` | `.github/workflows/fleet-runner.yml` | 179 | Bootstrap fleet registry |
| Medium | `actionlint/shellcheck` | `.github/workflows/messages.yml` | 69 | Determine and dispatch scheduled skills |
| Medium | `actionlint/shellcheck` | `.github/workflows/messages.yml` | 669 | Extract message |
| Medium | `actionlint/shellcheck` | `.github/workflows/messages.yml` | 734 | Run |
| Medium | `actionlint/shellcheck` | `.github/workflows/messages.yml` | 815 | Log token usage |
| Medium | `artipacked` | `.github/workflows/aeon.yml` | 83 | Early checkout |
| Medium | `artipacked` | `.github/workflows/aeon.yml` | 119 | Checkout repo |
| Medium | `artipacked` | `.github/workflows/chain-runner.yml` | 28 | Checkout repo |
| Medium | `artipacked` | `.github/workflows/fleet-runner.yml` | 56 | Checkout |
| Medium | `artipacked` | `.github/workflows/lint.yml` | 32 | Checkout |
| Medium | `artipacked` | `.github/workflows/messages.yml` | 56 | Checkout repo |
| Medium | `artipacked` | `.github/workflows/sync-aeon-public-results.yml` | 28 | Checkout aeon |
| Medium | `artipacked` | `.github/workflows/sync-upstream.yml` | 22 | Checkout fork |
| Low | `anonymous-definition` | `.github/workflows/aeon.yml` | 72 | (unnamed) |
| Low | `anonymous-definition` | `.github/workflows/chain-runner.yml` | 20 | (unnamed) |
| Low | `anonymous-definition` | `.github/workflows/fleet-runner.yml` | 44 | (unnamed) |
| Low | `anonymous-definition` | `.github/workflows/messages.yml` | 47 | (unnamed) |
| Low | `anonymous-definition` | `.github/workflows/messages.yml` | 651 | Sync state to aeon-private (Phase 1 dual-write) |
| Low | `anonymous-definition` | `.github/workflows/sync-aeon-public-results.yml` | 23 | (unnamed) |
| Low | `anonymous-definition` | `.github/workflows/sync-upstream.yml` | 16 | (unnamed) |
| Low | `concurrency-limits` | `.github/workflows/fleet-runner.yml` | 4 | (unnamed) |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 98 | Determine skill |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 112 | Check if there's work |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 150 | Validate skill secrets |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 194 | Run pre-fetch scripts |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 288 | Run |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 602 | Log token usage |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 625 | Track token costs |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 630 | Capture skill output |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 651 | Analyze skill output |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 752 | Convert feed outputs |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 863 | Commit results |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 927 | Update cron state |
| Low | `template-injection` | `.github/workflows/fleet-runner.yml` | 150 | Restore fleet identities |
| Low | `template-injection` | `.github/workflows/fleet-runner.yml` | 315 | Commit results |
| Low | `template-injection` | `.github/workflows/fleet-runner.yml` | 347 | Notify |
| Low | `template-injection` | `.github/workflows/messages.yml` | 670 | Extract message |
| Low | `template-injection` | `.github/workflows/sync-upstream.yml` | 71 | Push sync branch |
| Low | `template-injection` | `.github/workflows/sync-upstream.yml` | 78 | Open or update PR |
| Low | `undocumented-permissions` | `.github/workflows/aeon.yml` | 77 | (unnamed) |
| Low | `undocumented-permissions` | `.github/workflows/chain-runner.yml` | 24 | (unnamed) |
| Low | `undocumented-permissions` | `.github/workflows/fleet-runner.yml` | 48 | (unnamed) |
| Low | `undocumented-permissions` | `.github/workflows/messages.yml` | 658 | Sync state to aeon-private (Phase 1 dual-write) |
| Low | `undocumented-permissions` | `.github/workflows/sync-upstream.yml` | 19 | (unnamed) |

## Carried over (unchanged)

_None._

## Resolved since (no prior audit)

_None._

## Source status

- zizmor: ok (SARIF: 116 raw results; version 1.25.2)
- actionlint: ok (20 raw findings; version 1.7.12)
- hand-rolled: ok (no additional findings — the messages.yml:577 toJson pattern is already gated via `_CLIENT_PAYLOAD_MESSAGE` env)

<!--
workflow-security-audit-fingerprints
098273477d4c2049 severity=Medium status=info rule=artipacked file=.github/workflows/aeon.yml step=Early_checkout
c532628fb9c78a69 severity=Medium status=info rule=artipacked file=.github/workflows/aeon.yml step=Checkout_repo
004a5bf63b972708 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=Determine_skill
2e5fdc2df2df60d8 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=Check_if_there's_work
1f2f68495a8848ca severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=Validate_skill_secrets
339a23fa646d80fa severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=Run_pre-fetch_scripts
d06cd31b0565bb63 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=Run
8cc01c60785c8304 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=Log_token_usage
883a81dae7ecd841 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=Track_token_costs
2c759b0b1f8e1882 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=Capture_skill_output
0baf49dd530c1dce severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=Analyze_skill_output
bc43189d9e231688 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=Convert_feed_outputs
7bea73c606a0ef8d severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=Commit_results
c25bb1f1ac73558b severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=Update_cron_state
950d36a1de77c180 severity=Critical status=manual rule=unpinned-uses file=.github/workflows/aeon.yml step=Early_checkout
f8ab9c300bf519c5 severity=Critical status=manual rule=unpinned-uses file=.github/workflows/aeon.yml step=Checkout_repo
2356e1a110ed47ac severity=Critical status=manual rule=unpinned-uses file=.github/workflows/aeon.yml step=Setup_Node.js
20c9f644148df279 severity=Low status=info rule=undocumented-permissions file=.github/workflows/aeon.yml step=L77
39ac8411c7669df6 severity=Low status=info rule=anonymous-definition file=.github/workflows/aeon.yml step=L72
1aff3826dae795dc severity=Medium status=info rule=artipacked file=.github/workflows/chain-runner.yml step=Checkout_repo
cb7f1b6befa54ab6 severity=Low status=info rule=undocumented-permissions file=.github/workflows/chain-runner.yml step=L24
786047e506ca7d53 severity=Low status=info rule=anonymous-definition file=.github/workflows/chain-runner.yml step=L20
7ee6deb6ceb7124f severity=High status=manual rule=secrets-outside-env file=.github/workflows/chain-runner.yml step=Checkout_repo
082bd159ec47117d severity=High status=manual rule=secrets-outside-env file=.github/workflows/chain-runner.yml step=Run_chain
6bb6de3b937ea32c severity=High status=manual rule=secrets-outside-env file=.github/workflows/chain-runner.yml step=Update_cron_state
781bd28c5c4aa2d4 severity=High status=manual rule=secrets-outside-env file=.github/workflows/chain-runner.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
fea5106dd502696b severity=Medium status=info rule=artipacked file=.github/workflows/fleet-runner.yml step=Checkout
39e3c332200bc315 severity=Low status=info rule=template-injection file=.github/workflows/fleet-runner.yml step=Restore_fleet_identities
d7ad306ff33384ac severity=Low status=info rule=template-injection file=.github/workflows/fleet-runner.yml step=Commit_results
4512260bedca1359 severity=Low status=info rule=template-injection file=.github/workflows/fleet-runner.yml step=Notify
db0ddb6a10e8f614 severity=Low status=info rule=undocumented-permissions file=.github/workflows/fleet-runner.yml step=L48
3ed0978e6efb3f66 severity=Low status=info rule=anonymous-definition file=.github/workflows/fleet-runner.yml step=L44
0e1882ead34ead23 severity=Low status=info rule=concurrency-limits file=.github/workflows/fleet-runner.yml step=L4
9dd9ccf4a8b13cb1 severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=Restore_fleet_identities
3dd10bb370389d6a severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=Prefetch_live_Surplus_prices_(best-effort,_outside_sandbox)
2e256187f4044ca3 severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=Run_fleet_task_runner
19d68e1b1c840f2b severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
e62807ce42c490c3 severity=Medium status=info rule=artipacked file=.github/workflows/lint.yml step=Checkout
794adcb750726f00 severity=Medium status=info rule=artipacked file=.github/workflows/messages.yml step=Checkout_repo
66f52f3d354469af severity=Low status=info rule=template-injection file=.github/workflows/messages.yml step=Extract_message
a2b3d736d9431f73 severity=Low status=info rule=undocumented-permissions file=.github/workflows/messages.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
4fba331c91463257 severity=Low status=info rule=anonymous-definition file=.github/workflows/messages.yml step=L47
085cad7229d7b76a severity=Low status=info rule=anonymous-definition file=.github/workflows/messages.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
0c6f05644978091e severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=Checkout_repo
04bf5202a52c6262 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=Determine_and_dispatch_scheduled_skills
9d0c80627bbda874 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=Collect_and_dispatch_messages
8834386b7343ce3f severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=Sync_state_to_aeon-private_(Phase_1_dual-write)
657ecac2d7c8deaa severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=Run
8639b641ebcf9473 severity=Medium status=info rule=artipacked file=.github/workflows/sync-aeon-public-results.yml step=Checkout_aeon
1ea56755046bdc99 severity=Low status=info rule=anonymous-definition file=.github/workflows/sync-aeon-public-results.yml step=L23
51e649cc0aebc1c2 severity=Medium status=info rule=artipacked file=.github/workflows/sync-upstream.yml step=Checkout_fork
f851f0b58d824c3e severity=Low status=info rule=template-injection file=.github/workflows/sync-upstream.yml step=Push_sync_branch
a86edd31b84a2422 severity=Low status=info rule=template-injection file=.github/workflows/sync-upstream.yml step=Open_or_update_PR
c87a44f480625395 severity=Low status=info rule=undocumented-permissions file=.github/workflows/sync-upstream.yml step=L19
61867be0fe7e4c9e severity=Low status=info rule=anonymous-definition file=.github/workflows/sync-upstream.yml step=L16
fa28dc3d61fcc6ee severity=High status=manual rule=secrets-outside-env file=.github/workflows/sync-upstream.yml step=Checkout_fork
bab05f277f41ad6b severity=High status=manual rule=secrets-outside-env file=.github/workflows/sync-upstream.yml step=Open_or_update_PR
fa993412d044f2ef severity=Medium status=info rule=actionlint/shellcheck file=.github/workflows/aeon.yml step=Run
fbeb05c3d666ed10 severity=Medium status=info rule=actionlint/shellcheck file=.github/workflows/aeon.yml step=Log_token_usage
12a0f3a689fc9ab9 severity=Medium status=info rule=actionlint/shellcheck file=.github/workflows/chain-runner.yml step=Run_chain
4b461cb289a9dc69 severity=Medium status=info rule=actionlint/shellcheck file=.github/workflows/chain-runner.yml step=Run_chain
3b07af54bd4380af severity=Medium status=info rule=actionlint/shellcheck file=.github/workflows/chain-runner.yml step=Run_chain
5d3a763809012810 severity=Medium status=info rule=actionlint/shellcheck file=.github/workflows/chain-runner.yml step=Run_chain
23bcc312610119c8 severity=Medium status=info rule=actionlint/shellcheck file=.github/workflows/chain-runner.yml step=Run_chain
be4087dd883c63c4 severity=Medium status=info rule=actionlint/shellcheck file=.github/workflows/chain-runner.yml step=Run_chain
25d6310192ef869b severity=Medium status=info rule=actionlint/shellcheck file=.github/workflows/chain-runner.yml step=Run_chain
67af4425b2454c39 severity=Medium status=info rule=actionlint/shellcheck file=.github/workflows/chain-runner.yml step=Run_chain
f469c926003872da severity=Medium status=info rule=actionlint/shellcheck file=.github/workflows/fleet-runner.yml step=Bootstrap_fleet_registry
8d04be0add8568a8 severity=Medium status=info rule=actionlint/shellcheck file=.github/workflows/fleet-runner.yml step=Bootstrap_fleet_registry
afc414751aa67cec severity=Medium status=info rule=actionlint/shellcheck file=.github/workflows/fleet-runner.yml step=Bootstrap_fleet_registry
fc4289c20f564205 severity=Medium status=info rule=actionlint/shellcheck file=.github/workflows/fleet-runner.yml step=Bootstrap_fleet_registry
e83eb553073afc10 severity=High status=manual rule=actionlint/shellcheck file=.github/workflows/fleet-runner.yml step=Run_fleet_task_runner
e198266ddaae6ad5 severity=High status=manual rule=actionlint/shellcheck file=.github/workflows/fleet-runner.yml step=Run_fleet_task_runner
3d5d3c61d3a77f34 severity=Medium status=info rule=actionlint/shellcheck file=.github/workflows/messages.yml step=Determine_and_dispatch_scheduled_skills
3662ea204b833a46 severity=Medium status=info rule=actionlint/shellcheck file=.github/workflows/messages.yml step=Extract_message
891b1b5b6bfe0d29 severity=Medium status=info rule=actionlint/shellcheck file=.github/workflows/messages.yml step=Run
15e318816be0f8e7 severity=Medium status=info rule=actionlint/shellcheck file=.github/workflows/messages.yml step=Log_token_usage
-->
