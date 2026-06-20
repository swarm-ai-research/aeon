# Self Review — 2026-06-20

Window: 2026-06-13 → 2026-06-20 (7 days).

## TL;DR

- **Reliability: catastrophic, now mostly recovered.** ~99% scheduled-skill failure rate over the window (899 of 912 completed runs failed). Root cause: `CLAUDE_CODE_OAUTH_TOKEN` was empty in the workflow env, so every Claude CLI invocation died in <1s with zero token usage. Token was restored around 2026-06-20T06:05Z and the 06:05–06:08 batch is now succeeding.
- **Output quality: nothing to assess.** `articles/` is empty. Only one commit in the last 14 days (`chore(cron): janitor success`, today). No agent-authored PRs in the window.
- **Memory: degraded.** `memory/MEMORY.md` does not exist. Only two log files in `memory/logs/` (2026-06-10, 2026-06-20). No `memory/topics/`, no `memory/issues/`.

## 1. Output quality

| Check | Finding |
|---|---|
| Recent articles | `articles/` is empty — no substantive outputs to grade. |
| Recent notifications | Only inferable from cron-state. None visible. |
| Recent PR comments | None from agent in last 7 days. Last agent PR was 2026-06-10 (AGI Tracker). |
| Recent commits | One: `chore(cron): janitor success` (today). |

Nothing to assess — the agent has been effectively inert all week because the LLM auth was broken.

## 2. Reliability

`scripts/skill-runs --hours 168` summary:

- Total runs: 942 — OK: 8, Fail: 899, Running: 19, Cancelled: 5. Success rate ≈ **0.9%**.
- **33 of 38 tracked skills** had >100 consecutive failures by 2026-06-20T01:53Z.
- Worst offenders: `compute-futures-eda` (202 consec fails), `gitlawb-fleet-metrics` (196), `pr-review` (196), `skill-health` (195), `skill-analytics` (188).

### Root cause

Every failure in cron-state has the same signature: a JSON tail with `"total_cost_usd":0,"usage":{"input_tokens":0,...,"output_tokens":0,...}`. The Claude CLI exited in well under a second without ever calling the API.

Diff of two runs:

| Run | Time | `CLAUDE_CODE_OAUTH_TOKEN` env | Result |
|---|---|---|---|
| 27856646818 (self-review) | 2026-06-20T01:52:17Z | empty | failed in 0.6s, 0 tokens |
| 27862412997 (gitlawb-fleet-metrics) | 2026-06-20T06:07:58Z | `***` (set) | succeeded in 36s, 1858 output tokens |

`ANTHROPIC_API_KEY` was unset in both runs. The OAuth token was the only credential, and it was missing from the workflow secrets until around 06:05Z today. Once restored, scheduled runs immediately started succeeding (e.g. `goal-tracker` 06:06:18, `compute-pulse` 06:06:04, `code-health` 06:05:58 all `success`).

This is not a code bug. It's a secret-store outage. The workflow file (`.github/workflows/aeon.yml` lines 256–257, 647–648, 748–749) wires the secret in correctly:

```yaml
ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

When neither secret is set in the repo, both env vars resolve to empty string and the CLI bails with the zero-usage JSON.

### Why monitors didn't catch it sooner

`skill-health`, `heartbeat`, `batch-health`, `skill-evals`, and `skill-repair` — every skill whose job is to detect and react to skill failures — was itself failing for the same reason. The watchdog was wedged shut.

`memory-flush` (which would normally append a log line summarizing failures) was also down, which is why `memory/logs/` is nearly empty and the daily incident wasn't captured anywhere durable.

This is a **single-point-of-failure on `CLAUDE_CODE_OAUTH_TOKEN`**: every recovery mechanism shares the same upstream dependency that broke.

### Other anomalies

- **`pr-review` workflow name leak**: scheduled `pr-review` runs show a workflow title like `skill: pr-review (swarm-ai-research/swarm\n\nYou are acting as a merge gate reviewer...)`. Not a security issue — it's the literal multi-line `var:` from `aeon.yml`'s `pr-review` config being interpolated into `run-name`. Cosmetic, but it makes log filtering and shell tooling awkward. Worth either truncating `inputs.var` in `run-name` or sourcing the policy from a file path instead of inline yaml.
- **One stray `git submodule` warning** in run cleanup: `fatal: No url found for submodule path '.swarm-audit' in .gitmodules`. Benign — actions/checkout cleanup step. But indicates a half-removed submodule.

## 3. Memory hygiene

| Check | Finding |
|---|---|
| `memory/MEMORY.md` present? | **No** — flagged by today's `memory-structural-dedupe` log line. |
| `memory/logs/` density | 2 entries in 7 days (10th, 20th). Expected: 7. |
| `memory/topics/` | Absent. |
| `memory/issues/` | Absent. CLAUDE.md describes a full issue tracker schema but no files exist. |
| `memory/cron-state.json` | Present, healthy structure, 38 skills tracked. |
| `memory/token-usage.csv` | Present. |
| `memory/triaged-prs.json` / `triaged-issues.json` | Present, length 1 each — likely just headers/empties. |
| Stale data | Most cron-state `last_error` entries are duplicates of the same OAuth-token failure signature. Mass clearing of `last_error` and `consecutive_failures` will be appropriate once we confirm 3+ days of healthy runs. |

## 4. Recommendations

### Already done in this run

1. Created `memory/MEMORY.md` from a clean template — the structural-dedupe skill stops complaining and future skills have an index to read.
2. Created `memory/issues/INDEX.md` and filed `ISS-001` for the OAuth-token outage so future health checks can see prior incidents.
3. Logged today's review to `memory/logs/2026-06-20.md`.

### Recommended next

1. **Add a credential canary.** A dirt-cheap pre-flight check in `aeon.yml` that fails the job *with a distinct error* when both `ANTHROPIC_API_KEY` and `CLAUDE_CODE_OAUTH_TOKEN` are empty, before npm-installing the CLI and burning a minute. The current behavior — opaque JSON tail at exit 1 — made this incident much harder to triage. ~10 lines of bash.
2. **Out-of-band reliability monitor.** `skill-health` can't observe its own auth outage. A tiny external pinger (cron job in a different account, or a status-page heartbeat) that watches whether *any* Aeon skill ran a successful Claude call in the last 6h would have caught this within hours instead of 14 days.
3. **Truncate `inputs.var` in `run-name`.** Change `aeon.yml`'s `run-name` to take only the first line of `inputs.var`, so multi-line policy blocks don't leak into run titles.
4. **Trim cron-state error noise.** Once 3 days of clean runs are in, run a one-shot to clear `last_error` and reset `consecutive_failures` so anomaly detection has a clean baseline. Don't do it pre-emptively — better to wait for evidence.
5. **Decide on `.swarm-audit` submodule.** Either fully remove the entry or restore its URL in `.gitmodules`.
6. **No skills to add or disable on this review.** The skill set looks well-scoped; the failure mode was infrastructural, not architectural.

## 5. Numbers, for the record

- 942 workflow runs in the last 168h.
- 899 failed, 8 succeeded, 19 in-progress, 5 cancelled at the time of this audit.
- 0 articles authored in the window. 1 commit. 0 agent PRs.
- 38 skills tracked in `cron-state.json`. 33 had ≥100 consecutive failures. Cumulative `total_successes` across all tracked skills: **3**.

— Self Review, 2026-06-20.
