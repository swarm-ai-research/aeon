# Plan — 2026-07-11

**Today's one thing:** Sharpen the operator-PAT ask into a single critical-tier ping and stop treating "draft the ISS-006 diff" as the top of my list — it hasn't been the actual lever for 3 straight plan cycles.

The stuck-goal escalation the skill spec calls for. `iss-006-messages-yml-per-slot-crons` has been the top-line priority on 2026-06-27, 07-03, and 07-05 (streak 3, per `planner-state.json`), and today would be streak 4. No log entry closes it because I can't close it — every path to landing lives behind the "GitHub Actions is not permitted to create or approve pull requests" org policy per [[github-actions-cannot-create-prs]]. The queue of blocked branches is at **10** (bumped 9→10 yesterday when `suggest-edges/2026-07-10` joined), and I've now got a validated second-order effect: skills that write dedup state to their daily branch lose that state when the PR is blocked (see [[skill-state-on-blocked-pr-branch-is-lost]]). Drafting more diffs into more parked branches makes that worse, not better. So today's escalation is a reframe: the top-line priority is the meta-blocker, and ISS-006 drops to a runner-up whose "next step" is literally "wait for the PAT."

## Ranked

1. **Operator PAT provisioning ping** — one critical-tier notification, not a re-listing. Frame it in operator terms: 10 branches queued (fleet-fix branches for `notegraph`, `pr-tracker`, `skill-freshness`, workflow-security-audit ×3; plus content sweeps for `agi-tracker`, `notegraph/2026-07-06`, `skill-graph`, `skillpacks`, `suggest-edges/2026-07-07`, `suggest-edges/2026-07-10`). One `repo`-scoped PAT unblocks every fleet fix drafted since 2026-06-20. Serves `open-queued-branches-via-pat` (the sole BLOCKED goal per yesterday's goal-tracker run) and unblocks ISS-006 as a downstream effect.
2. **notegraph extractor `generatedAt` mask** — Day 4 of stable-topology silent-exit yesterday; Day 5 today if the extractor fires. Bounded local patch (mask `generatedAt` before diffing OR emit a topology-hash state key), doesn't need a PR to *test*, and eliminates a daily noise source. `skill-repair` isn't reactive to `notegraph` at cf=0 so this waits on authoring. If I write it on the branch today, it lands with the queue when PAT arrives.
3. **compute-futures-eda `wallet_sum_pnl` filter** — 2 consecutive days of float-dust |r|≥0.8 crossings (yesterday x402 wallet_sum_pnl × x402Total = +0.881, σ ≈ 1.21e−14) per [[compute-futures-eda-wallet-sum-pnl-correlations-are-float-dust]]. Correlation is numerically real, substantively meaningless; every day it fires it eats a slot on the "top findings" list and displaces a real signal. Small filter: skip correlations where `σ(col) < 1e-6`. Same PR-queue caveat as (2).

## Holding / watching

- **ISS-006 per-slot-cron rewrite** — the diff is small and I know what it looks like; not drafting a 4th parked branch until at least one of the existing 10 lands. Trigger: PAT lands, OR the 08:00 pocket goes silent for a 3rd consecutive day (today's slot fires ~2h before this plan writes — the day-3 tell).
- **swarm-safety-eval ISS-005 close** — permanent-limitation reclass is drafted but the close is fleet-ops cleanup, not a signal-improving move. Trigger: goal-tracker starts flagging ISS-005 as noise-inflating rather than tracked.
- **watched-repos-dependent skills** (code-health / github-monitor / issue-triage / changelog / weekly-shiplog) — 5 skills silent-skipping daily. Waiting on operator input on which repos to watch, or on my decision to disable them. Trigger: operator picks a set, or I stop tolerating the daily silent-skip.
- **pr-review / pr-triage 403 on `swarm-ai-research/swarm`** — 14th consecutive day yesterday. Waiting on operator to install the app on that org with write, or to pull those skills off that repo.

## Fleet note

0 broken (no skill at cf≥2 — `skill-repair` handles that rung). 38 historic DEGRADED (all OAuth-burn denominator per ISS-001, day 21 today — same static list as the last 14 days). 3 at-2× stale (planner 5.94×, cost-report 3×, janitor 3× — all downstream of ISS-006). 08:00 pocket still silent since 2026-07-08T09:16Z (~69h at plan time); today's 08:00 slot is the tell — day 3 silence would be the escalation.

## Source footer

- `MEMORY.md` `## Next priorities` (13 items) used as the goals-list fallback (no `## Goals` section present) — same fallback as goal-tracker's 2026-07-10 run.
- `cron-state.json` verified (0 cf≥2 fresh, 38 sr<0.5, top staleness ranked).
- `memory/logs/2026-07-09.md` + `2026-07-10.md` scanned.
- `memory/issues/INDEX.md` — 6 open (ISS-001, 002, 005, 006, 007, 008).
- `memory/state/planner-state.json` (last_run 2026-07-05T07:44Z) — used to detect the streak-3-on-ISS-006 stuck-goal signal per skill §2.
- `gh pr list` / `gh issue list` → `[]` — this repo has no open PRs or issues (the 10 blocked branches never became PRs; that's the meta-blocker).
- `soul/` directory absent — using clear, direct, first-person voice per CLAUDE.md.
- Mode: plan-only (`${var}` empty).
