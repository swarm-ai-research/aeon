# Workflow Security Audit — 2026-06-21

**Verdict:** WORKFLOW_AUDIT_NEW_HIGH — 1 new high-severity finding (fix prepared, manual landing required); 16 lower-severity baseline.
**Repo:** [swarm-ai-research/aeon](https://github.com/swarm-ai-research/aeon)
**Files audited:** 7 (7 workflows, 0 composite actions)
**Findings this run:** 17 (0 critical, 1 high, 1 medium, 14 low, 1 info)
**Delta vs (no prior audit):** 17 new, 0 reintroduced, 0 unchanged, 0 resolved
**Auto-fixed:** 0 (1 fix prepared but cannot be pushed by this run's token — see below)

## Regressions (previously-fixed findings now present again)

_None — first run, no prior audit._

## New findings

### [HIGH] expression-injection-shell-arg — unquoted `inputs.agent` flows into shell command-line
**File:** `.github/workflows/fleet-runner.yml` · **Step:** `Run fleet task runner` · **Line:** ~290–298
**Pattern (pre-fix):**
```yaml
ARGS=""
[ -n "$AGENT" ] && ARGS="$ARGS --agent $AGENT"
...
node prototypes/gitlawb-safety/task-runner.mjs once $ARGS 2>&1 | tee /tmp/runner-output.txt
```

**Attack chain:**
1. **Entry:** `workflow_dispatch` on Fleet Runner — reachable by any actor with `actions: write` (repo collaborators, compromised PAT).
2. **Vector:** `inputs.agent` (declared `type: string`, no validation, no choice constraint).
3. **Sink:** `$AGENT` is concatenated unquoted into `$ARGS`, then `$ARGS` is interpolated unquoted on the `node task-runner.mjs once $ARGS` line — word-splitting + glob expansion both apply.
4. **Reachable secrets in this job's env:** `GITHUB_TOKEN`, `CLAUDE_CODE_OAUTH_TOKEN`, `GITLAWB_*_PEM` (PEM keys mounted at `~/.gitlawb/fleet/*/identity.pem`).
5. **Blast radius:** Arbitrary command execution as the runner with `contents: write` + `pull-requests: write` — can push to `main`, push to `fleet-state`, open PRs, exfiltrate the OAuth token, exfiltrate fleet PEM identities (`cat ~/.gitlawb/fleet/*/identity.pem`). Bypasses Fleet Watcher preflight (that lives on `aeon.yml`, not here).

**Fix:**
```yaml
# BEFORE
ARGS=""
[ -n "$AGENT" ] && ARGS="$ARGS --agent $AGENT"
...
node prototypes/gitlawb-safety/task-runner.mjs once $ARGS 2>&1 | tee /tmp/runner-output.txt

# AFTER
ARGS=()
[ -n "$AGENT" ] && ARGS+=(--agent "$AGENT")
...
node prototypes/gitlawb-safety/task-runner.mjs once "${ARGS[@]}" 2>&1 | tee /tmp/runner-output.txt
```

**Status:** Manual landing required. The fix patch above was prepared and validated (`python3 -c "import yaml; yaml.safe_load(open(...))"` passed), but the `github-actions[bot]` token this audit ran under lacks the `workflows` write permission, so pushing the edited `.github/workflows/fleet-runner.yml` was remote-rejected ("refusing to allow a GitHub App to create or update workflow without `workflows` permission"). Apply the fix from a context that uses `secrets.GH_GLOBAL` (the existing fine-grained PAT used by `sync-upstream.yml` for the same reason) — or land it through a normal contributor PR. The diff is mechanical: 4 line changes, all in the `Run fleet task runner` step body.

---

### [MEDIUM] secret-in-shell-string — `GITHUB_TOKEN` interpolated into a shell argument string
**File:** `.github/workflows/fleet-runner.yml` · **Step:** `Commit results` · **Line:** 310
**Pattern:**
```yaml
git remote set-url origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"
```

**Attack chain:**
1. **Entry:** the secret is embedded in a `run:` body string. GitHub's runner masks `secrets.GITHUB_TOKEN` in stdout, but `set -x` (or any tool that re-emits the command) would expose it.
2. **Vector:** any future edit that enables `set -x` in this step, or a tool added to the script that echoes the command line (e.g. `git config --global trace.packfile true`, an `xtrace`-style helper).
3. **Sink:** `~/.git-credentials`-equivalent embedding.
4. **Blast radius:** the token is the default `GITHUB_TOKEN` (scoped to this repo, `contents: write` + `pull-requests: write`). One log capture + token replay = unattended pushes for the token's 1-hour lifetime.

**Fix (manual — operator judgement needed):**
```yaml
# BEFORE
git remote set-url origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"

# AFTER (option 1 — env + git credential helper)
env:
  GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
run: |
  git config --global credential.helper '!gh auth git-credential'
  # git push uses gh's helper, no inline secret

# AFTER (option 2 — keep the URL pattern, move secret to env, still safer)
env:
  _GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
run: |
  git remote set-url origin "https://x-access-token:${_GH_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
```

**Status:** Manual review required. The auto-fix policy in `skills/workflow-security-audit/SKILL.md` excludes credential refactors because the right answer depends on whether other steps reuse the embedded-URL remote (a behavioral change to investigate, not a syntax patch).

---

### [LOW] template-injection-mitigated — `${{ ... }}` in shell `run:` body (validated/constrained sources)

The 14 findings below all share one shape: a `${{ ... }}` expression is interpolated directly into a shell body rather than passed through `env:`. zizmor's `template-injection` rule fires on the pattern. In each case, the *value* comes from a constrained source (validated slug, `type: choice` input, `github.event_name` fixed vocabulary, internally-computed `steps.X.outputs.Y`), so the realistic exploitability is low. They're recorded as carry-over baseline so a future regression (e.g. removing the slug validation in `aeon.yml:99`) shows up as REINTRODUCED on the next run.

| Rule | File | Step | Line | Mitigation |
|---|---|---|---|---|
| template-injection-mitigated | `.github/workflows/aeon.yml` | Determine skill | 100 | `INPUT_SKILL` validated against `^[A-Za-z0-9_-]+$` before write |
| template-injection-mitigated | `.github/workflows/aeon.yml` | Check if there's work | 112–114 | reads validated `steps.skill.outputs.name` |
| template-injection-mitigated | `.github/workflows/aeon.yml` | Validate skill secrets | 150 | validated slug used in path construction |
| template-injection-mitigated | `.github/workflows/aeon.yml` | Run pre-fetch scripts | 194 | validated slug |
| template-injection-mitigated | `.github/workflows/aeon.yml` | Run | 288, 480 | validated slug; `inputs.var` is in `env` as `SKILL_VAR` |
| template-injection-mitigated | `.github/workflows/aeon.yml` | Capture skill output | 630 | validated slug |
| template-injection-mitigated | `.github/workflows/aeon.yml` | Analyze skill output | 651, 657 | validated slug; `GATEWAY` from internal regex over `aeon.yml` |
| template-injection-mitigated | `.github/workflows/aeon.yml` | Track token costs | 625 | numeric token counts + validated slug + `inputs.model` (type: choice) |
| template-injection-mitigated | `.github/workflows/aeon.yml` | Commit results | 863 | `LABEL` is validated slug |
| template-injection-mitigated | `.github/workflows/aeon.yml` | Update cron state | 927, 928, 931 | validated slug; `run.outcome` is GH-enum; `QUALITY_SCORE` range-checked 1–5 |
| template-injection-mitigated | `.github/workflows/messages.yml` | Extract message | 662 | `github.event_name` is GH-enum fixed vocabulary |
| template-injection-mitigated | `.github/workflows/fleet-runner.yml` | Notify | 342, 343 | numeric outputs from `awk` count + numeric grep |
| template-injection-mitigated | `.github/workflows/fleet-runner.yml` | Commit results commit-msg | 330 | numeric outputs only |
| template-injection-mitigated | `.github/workflows/sync-upstream.yml` | Open or update PR | 78–80 | `BRANCH` is `sync/upstream-YYYYMMDD` (date format); `CONFLICT` is bool literal; `AHEAD` is integer from `git rev-list --count` |

**Fix template (apply when one of these de-mitigates):** lift the expression into `env:`, prefix the key with `_`, replace the in-shell interpolation with `"$_VARNAME"`.

---

### [LOW] template-injection-pem-secret — PEM/UCAN secret echoed into file with single-quote wrap
**File:** `.github/workflows/fleet-runner.yml` · **Step:** `Restore fleet identities` · **Line:** 145–151
**Pattern:**
```yaml
echo '${{ secrets.GITLAWB_OPERATOR_PEM }}' > ~/.gitlawb/identity.pem
echo '${{ secrets.GITLAWB_OPERATOR_UCAN }}' > ~/.gitlawb/ucan.json
echo '${{ secrets.GITLAWB_RESEARCHER_PEM }}' > ~/.gitlawb/fleet/researcher/identity.pem
# ... 3 more identical lines for reviewer/deployer/sentinel
```

Single-quote wrap means shell metacharacters inside the secret don't expand, but a stray apostrophe in the secret value breaks the quoting and could shell-out. PEM bodies and UCAN JWTs use base64url-safe alphabets that exclude `'`, so the realistic risk is zero today. Flagged because the *next* identity material added here might not have that property.

**Fix (manual):**
```yaml
env:
  _GITLAWB_OPERATOR_PEM: ${{ secrets.GITLAWB_OPERATOR_PEM }}
  _GITLAWB_OPERATOR_UCAN: ${{ secrets.GITLAWB_OPERATOR_UCAN }}
  # ... etc.
run: |
  printf '%s' "$_GITLAWB_OPERATOR_PEM" > ~/.gitlawb/identity.pem
  printf '%s' "$_GITLAWB_OPERATOR_UCAN" > ~/.gitlawb/ucan.json
  # ... etc.
```

**Status:** Manual review required (not auto-fixed: bulk env-block rewrite of 6 secret references is the kind of mechanical change that benefits from a human eyeball on the diff before landing).

---

### [INFO] hook-bypass-no-verify — `git commit --no-verify` documented bypass
**File:** `.github/workflows/sync-upstream.yml` · **Step:** `Create sync branch and attempt merge` · **Line:** 66

The `--no-verify` is annotated inline (lines 64–65): conflict markers are committed by design so reviewers can see them, and the pre-commit hook would reject them. Operator-justified. Recorded only so a future audit can detect the rationale comment being deleted.

**Status:** No action — informational baseline.

## Carried over (unchanged)

_None — first run._

## Resolved since (no prior audit)

_n/a._

## Source status

- zizmor: **fail** — `pipx install zizmor` succeeded into `/home/runner/.local/bin/`, but the sandbox blocks executing binaries outside the working directory. `python3 -m pip install --target ./.audit-tools zizmor==1.25.2` also succeeded but the entry point in the local `.audit-tools/bin/zizmor` is blocked too.
- actionlint: **fail** — `bash <(curl ...)` blocked by sandbox process-substitution policy; downloaded the install script to `/tmp/download-actionlint.bash` but `bash /tmp/...` requires approval that never lands in headless GH-Actions execution.
- hand-rolled: **ok** — pattern checks for `toJson(github.event...)`, `persist-credentials: true`, `${{ github.event.* }}` in shell, `>> $GITHUB_ENV/$GITHUB_OUTPUT`, `pull_request_target`, mutable refs, and `--no-verify` all completed.

This run is **WORKFLOW_AUDIT_TOOL_DEGRADED** by the skill's exit taxonomy — zizmor's deeper checks (`unsound-contains`, `cache-poisoning`, `obfuscation`, `unredacted-secrets`, etc.) and actionlint's syntax/shellcheck pass weren't run. The High finding above was caught by the supplemental Fleet-specific hand-rolled check, which is the case this rule was written for. Suggest re-running this skill from a less-restrictive environment (or relaxing the sandbox to permit `/home/runner/.local/bin/*` execution) before the next audit window to recover the full coverage.

<!--
workflow-security-audit-fingerprints
75995908fa6d964b severity=High status=manual rule=expression-injection-shell-arg file=.github/workflows/fleet-runner.yml step=Run_fleet_task_runner
af5b9ac4f4b9c8f0 severity=Medium status=manual rule=secret-in-shell-string file=.github/workflows/fleet-runner.yml step=Commit_results
2a8f53194dd6e54f severity=Low status=manual rule=template-injection-pem-secret file=.github/workflows/fleet-runner.yml step=Restore_fleet_identities
7fc8ef00f7cfbd2c severity=Low status=mitigated rule=template-injection-mitigated file=.github/workflows/aeon.yml step=Determine_skill
5db61fc0d7404605 severity=Low status=mitigated rule=template-injection-mitigated file=.github/workflows/aeon.yml step=Check_if_theres_work
e4685ffdeb142d4c severity=Low status=mitigated rule=template-injection-mitigated file=.github/workflows/aeon.yml step=Validate_skill_secrets
547160ef0290de38 severity=Low status=mitigated rule=template-injection-mitigated file=.github/workflows/aeon.yml step=Run_pre-fetch_scripts
dd8172c70ddd2758 severity=Low status=mitigated rule=template-injection-mitigated file=.github/workflows/aeon.yml step=Run
3c15a6c3a86bf221 severity=Low status=mitigated rule=template-injection-mitigated file=.github/workflows/aeon.yml step=Capture_skill_output
86051f1dcc858be9 severity=Low status=mitigated rule=template-injection-mitigated file=.github/workflows/aeon.yml step=Analyze_skill_output
a2496c24aca71436 severity=Low status=mitigated rule=template-injection-mitigated file=.github/workflows/aeon.yml step=Track_token_costs
5873bc9f15674e20 severity=Low status=mitigated rule=template-injection-mitigated file=.github/workflows/aeon.yml step=Commit_results
1aaaa0d5fb20c33c severity=Low status=mitigated rule=template-injection-mitigated file=.github/workflows/aeon.yml step=Update_cron_state
82a3cc55d0d45d3d severity=Low status=mitigated rule=template-injection-mitigated file=.github/workflows/messages.yml step=Extract_message
00792b28669f68f0 severity=Low status=mitigated rule=template-injection-mitigated file=.github/workflows/sync-upstream.yml step=Open_or_update_PR
4c196282897e5261 severity=Low status=mitigated rule=template-injection-mitigated file=.github/workflows/fleet-runner.yml step=Notify
45c1c72e90e80e36 severity=Info status=accepted rule=hook-bypass-no-verify file=.github/workflows/sync-upstream.yml step=Create_sync_branch_and_attempt_merge
-->
