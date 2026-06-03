# Fleet Runner — operations runbook

`fleet-runner.yml` runs Aeon's **goal-loop fleet**: the genuinely autonomous,
goal-driven engine under `scripts/fleet-executors/` (`task-generator.mjs` →
`goal-loop.mjs` with `doom-loop.mjs` detection, `signal-action-map.mjs`,
`wake-up-stack.mjs`). It is the layer that *decides and executes* multi-step
work without a human picking each task — distinct from the cron skill fleet in
`aeon.yml`, which runs pre-scheduled skills.

## Status: LIVE (not off)

> **Operator intent:** running + armed is the **desired** state. Do not disable
> the workflow or add `--dry-run` to "tidy up" — it is on deliberately. Pause or
> disarm only as a temporary, explicit operator decision (see below).

The runner is **active and armed**, regardless of the `fleet-runner: enabled:
false` line in `aeon.yml`. That flag is inert for this workflow — it exists only
because there is **no `skills/fleet-runner/SKILL.md`**, so it must stay
`enabled: false` or the generic scheduler (`messages.yml`) would try to dispatch
a non-existent skill every 5 minutes (and `config-validator` would fail).

What actually controls the runner:

| Control | Where | Effect |
|---|---|---|
| Schedule | `.github/workflows/fleet-runner.yml` → `on.schedule` `*/5 * * * *` | Fires every 5 min |
| Credentials | `GITLAWB_*` GitHub Actions secrets (see below) | Absent → identity/registration steps no-op; no fleet work happens |
| Arming | `prototypes/gitlawb-safety/fleet-heal.mjs` invocation (no `--dry-run`) | Self-heal takes **real corrective action** on the live fleet |

Last confirmed run is recorded on the **`fleet-state`** branch (commits
`chore(fleet-runner): processed N tasks, generated M`). Runtime state persists
there — never on `main`. Inspect with:

```bash
git fetch origin fleet-state --depth=5
git log --format="%ci %s" origin/fleet-state --grep="chore(fleet-runner)" -5
```

## Required secrets

The runner reads these from GitHub Actions secrets. Without the `GITLAWB_*` set,
identity restore writes empty PEMs and registration silently no-ops (`|| true`),
so the fleet does nothing — but the workflow still "succeeds".

| Secret | Purpose |
|---|---|
| `GITLAWB_OPERATOR_PEM` | Operator identity (task creation) |
| `GITLAWB_OPERATOR_UCAN` | Operator capability token |
| `GITLAWB_RESEARCHER_PEM` | `aeon-researcher` agent identity |
| `GITLAWB_REVIEWER_PEM` | `aeon-reviewer` agent identity |
| `GITLAWB_DEPLOYER_PEM` | `aeon-deployer` agent identity |
| `GITLAWB_SENTINEL_PEM` | `aeon-sentinel` agent identity |
| `ANTHROPIC_API_KEY` | LLM inference for the goal loop |
| `CLAUDE_CODE_OAUTH_TOKEN` | `claude` CLI auth for `aeon-reviewer`'s code review (falls back to regex analysis if absent) |
| `GITHUB_TOKEN` | Checkout + push to `fleet-state` |

## Arming, pausing, and disarming

**`fleet-heal.mjs` is ARMED.** On each run it can **renew, respawn, or kill**
fleet instances classified `degraded`/`expiring`/`expired`/`revoked` (healthy
instances are left untouched; renewals are gated by the reviewer-routed
red-team). These are real, outward-facing actions on the live GitLawb fleet.

- **Disarm self-heal (recommended before any experimentation):** re-add the
  `--dry-run` flag to the `node prototypes/gitlawb-safety/fleet-heal.mjs`
  invocation in the `Self-heal fleet` step. It then classifies and logs intended
  actions without acting.
- **Pause the whole runner:** disable the *Fleet Runner* workflow in the GitHub
  Actions UI (Actions → Fleet Runner → ⋯ → Disable workflow), or comment out the
  `schedule:` block in `fleet-runner.yml`. The `aeon.yml` flag does **not** pause
  it.
- **Re-arm / resume:** re-enable the workflow (or restore the cron) and remove
  `--dry-run`.

## Manual runs

`workflow_dispatch` inputs: `mode` (`once` | `loop`), `agent` (limit to one
role), `poll` (loop poll seconds). A `once` run does a single generate + process
pass; `loop` keeps polling for up to ~8 minutes.

## Tuning task / PR volume

The workflow fires every 5 minutes (GitHub Actions' shortest reliable schedule
interval — going lower won't run faster). How *busy* the fleet is each cycle is
governed by the per-agent cooldowns at the top of
`scripts/fleet-executors/task-generator.mjs`:

| Constant | Agent | Effect |
|---|---|---|
| `RESEARCH_COOLDOWN_H` | researcher (`issue:create`) | min hours between research tasks |
| `REVIEW_COOLDOWN_H` | reviewer (`pr:open`) | min hours between review tasks — **primary PR lever** |
| `AUDIT_COOLDOWN_H` | sentinel (`repo:admin`) | min hours between security audits |
| `DEPLOY_PROOF_COOLDOWN_H` | deployer | min hours between deploy-proof tasks |

Lower a constant → more tasks of that kind → more PRs. Each agent tracks its
**own** last-created timestamp in `memory/fleet-task-generator-state.json`
(`lastResearcherTask`, `lastReviewerTask`, `lastAudit`, `lastDeployProof`,
`lastOpenPRReview`).

The researcher and reviewer additionally gate on a **HEAD-advanced check**
(`lastResearchedHead` / `lastReviewedHead`): `changedFiles` is always populated
(the diff falls back to the last 10 commits, or to `HEAD` under the depth-1
checkout), so without this check the cooldown alone would recreate the same
"analyze/review recent changes" task every window during idle periods and flood
the fleet. They only regenerate work when `main`'s HEAD has actually moved since
the last task — i.e. when there's genuinely something new to look at.

**Reviewer open-PR fallback.** When the HEAD-advanced gate is closed (main is
quiet) but `gl pr list aeon` returns >0 open PRs, the reviewer gets a fallback
task to review one of them. Gated by `OPEN_PR_REVIEW_COOLDOWN_H` and
`state.lastOpenPRReview` so it doesn't fire every 5-min cycle. This keeps the
reviewer producing during idle stretches without re-firing on the same HEAD.

**Reviewer fan-out.** The reviewer emits one task per changed file (code
files first), capped at `MAX_REVIEW_FANOUT` (default 5). Each task is an
independent PR surface.

**Code-quality passes.** When changed files include code, the generator also
emits the kinds in `CODE_PASS_KINDS` (`docs-pass`, `refactor-pass`, `test-pass`)
to the reviewer DID (each needs `pr:open`). Gated by `CODE_PASS_COOLDOWN_H`
and `state.lastCodePass` / `state.lastCodePassHead`.

**Forker.** Daily fork task assigned to the deployer DID, reading targets from
`memory/fork-targets.json`. Each target is either a `github-mirror` (executor
runs `gl mirror` then `gl repo fork`) or a gitlawb-resident upstream. The
executor is responsible for idempotency (skip if already forked). Set
`active: false` on a target to pause it without deleting.

> **History:** the researcher and reviewer previously gated on the shared
> `lastRun` field, which the generator rewrites on *every* 5-minute run — so
> their multi-hour thresholds were never met and **neither agent ever fired in
> production**. The researcher additionally required `commitCount > 3`, which
> the depth-1 CI checkout could never satisfy. Both are fixed: per-agent timers
> + a changed-files gate. If you see researcher/reviewer tasks disappear from
> the `tasksCreated` log again, suspect a regression here first.

The compute-futures sims (cash / x402 / sweep / surplus) keep their own 24h
timers and are intentionally daily — they prove the rail still executes, so
running them more often adds noise, not signal.

## Relationship to the cron fleet

- **`aeon.yml` / `messages.yml`** — the scheduled *skill* fleet. Add autonomy
  here via the `planner` skill (decides the day) and the `reactive:` block
  (wakes skills on fleet-health signals).
- **`fleet-runner.yml` / `scripts/fleet-executors/`** — the goal-loop fleet. The
  higher autonomy ceiling: pursues multi-step goals across the researcher /
  reviewer / deployer / sentinel agents.
