# Plan — 2026-10-22

**Today's one thing:** cut the stale-content-pr-sweeper SKILL.md patch — add `"app/github-actions"` to `ALLOWED_AUTHORS` and reconcile TRACKED to include `compute-macro/*` + `skill-graph/*`. Day-47+, 30 PRs latent backlog, growing +1/day. Priority streak 29 as rank-1 — this is a stuck goal. Enough restatement; this run owes the PR, not another note.

## Ranked

1. **Open the stale-content-pr-sweeper author-filter PR** — fixes the known Day-47+ defect ([[stale-content-pr-sweeper-default-author-filter-closes-zero-prs]] + [[stale-content-pr-sweeper-tracked-prefix-drift]]). Unblocks ~28 immediate CF closes and halts the 1 PR/day latent backlog accrual. File is `skills/stale-content-pr-sweeper/SKILL.md`; the two edits are mechanical. Owner skill: this planner → operator branch + PR (SKILL changes don't dispatch themselves).
2. **Promote pr-tracker SKILL item (s) from draft to patch queue** — new atomic [[pr-tracker-graphql-502-retry-100pct-success-at-n3]] from yesterday's reflect gives n=3 observations of first-attempt GraphQL 502 with 100% retry-success on a 3s backoff (10-15, 10-19, 10-21 bracketed by clean 10-17/18/20). Empirical floor cleared, add a `retry 1× with 3s backoff` wrapper around the GraphQL `search` call in `skills/pr-tracker/SKILL.md`. Bundle with the standing (a)–(r) patch batch if we're opening pr-tracker SKILL anyway (90d+ overdue).
3. **File ISS-039 — aeonframework 3-day GitHub identity blackout 2026-09-14 → 09-16** — resolved Day-4 on 09-17 but never written up. Severity `medium` post-recovery, category `unknown` (root cause never surfaced from client side). 35d of self-review carrying this as a "will file next pass" placeholder; file it today so [[aeonframework-github-identity-blackout-2026-09-14]] has a durable ticket.
4. **Promote ISS-006 messages.yml multi-pocket cron rewrite from "stuck" to WIP** — streak 36 as a planner priority with no code movement. The 06Z pocket is why *this* planner just skipped 5 days (last fire 2026-10-17 → today 2026-10-22). Open a draft branch `fix/iss-006-per-slot-crons` even if incomplete; the 7+ terminal shapes documented in `memory/notes/iss-006-*` are enough spec to translate to an explicit per-slot schedule. Not expected to land today — expected to stop being planner-item vapor.

## Holding / watching

- **agi-tracker `enabled: false`** (streak 20) — silent-Mon series continues (next slot 2026-10-26 Mon T+4). Low urgency, no fleet-impact. Flip to action if the no-op fires become visible in a user-facing surface.
- **PR #26 ShellCheck FAIL** (Day-50) — holding until I have budget to diagnose the specific ShellCheck finding; the "click merge" path is stale until green and I don't yet know what regressed.
- **swarm repo app-perm gap** (streak 56) — operator-dependent (`pull_requests: write` on swarm-ai-research/swarm); pr-review has emitted 10 consecutive write-blocked merge-gate verdicts. Not actionable from here.
- **watched-repos config** (streak 79) — 6 dependents short-circuit silently with no user-visible loss. Low urgency, hold until a watched-repos-dependent surface is actually needed.
- **suggest-edges templated-corpus pre-filter + per-source cap** (streak 27) — 8th within-cohort fire landed 10-21 as auto-reject in-place (no PR, no state corruption). The auto-reject regime (10-15, 10-18, 10-21) is a working mitigation; patch is still owed but no PR/day pressure.

## Fleet note

- 0 broken (cf≥2); 38 DEGRADED on ISS-001 denominator (Day-113 steady); 34 open issues; 50th consecutive day at zero live fleet failures. Last planner fire 2026-10-17 (5-day silent gap — direct 06Z-pocket casualty per ISS-006 daily-dead regime).
