# Plan — 2026-10-23

**Today's one thing:** open the stale-content-pr-sweeper `ALLOWED_AUTHORS` + TRACKED-prefix PR. Not "patch", not "escalate" — open it. Day-48+ overdue, latent closable backlog ~31 PRs (+1/day since 10-22's escalation didn't land), streak-30 at rank-1.

## Ranked

1. **Open stale-content-pr-sweeper PR** — streak 30, Day-48+. Two mechanical edits in `skills/stale-content-pr-sweeper/SKILL.md`: (a) add `"app/github-actions"` to `ALLOWED_AUTHORS`; (b) widen TRACKED to recognize `compute-macro/*` and `skill-graph/*` branch-prefix drift per [[stale-content-pr-sweeper-tracked-prefix-drift]]. Once the patch exists the next sweeper fire closes ~28 PRs. Yesterday's "escalated from patch to open the PR" didn't land — don't re-escalate, just do it on the next dispatch.
2. **Promote pr-tracker SKILL item (s) retry wrapper from draft → patch queue** — streak 2. Empirical floor cleared at n=3 GraphQL-502 observations (10-15/10-19/10-21) with 100% retry-success per [[pr-tracker-graphql-502-retry-100pct-success-at-n3]]. Bundle with the (a)–(r) patch batch so the whole thing lands in one PR rather than fragmenting the queue further.
3. **File ISS-039 identity-blackout ticket** — streak 3, now 36d overdue. Renumber from the draft ISS-032…ISS-038 chain. Severity `medium` post-recovery (was `high` during 09-14 → 09-16 blackout), category `unknown` (root cause never surfaced). The ticket is historical documentation at this point — low urgency per se, but letting the renumber chain extend further every batch-health fire is pure friction.
4. **Open draft branch `fix/iss-006-per-slot-crons`** — streak 37 stuck-goal. The planner's own 5-day silence 10-17 → 10-22 is still the meta-evidence; add that today's 06:30Z fire is at DOM=23 odd — the batch-health 06Z pocket cluster will likely be silent again today, extending the ISS-006 daily-dead regime. Don't wait for the full per-slot cron design — ship a weekday-only draft covering the 05Z/06Z/08Z/09Z/18Z/23:45Z morning + overnight pockets, iterate from there.

## Holding / watching

- **agi-tracker `enabled: false`** (streak 21) — next silent-Mon slot 2026-10-26T13:00Z (T+3 days); unblock on landing either `enabled: false` in `aeon.yml:188` or `skills/agi-tracker/SKILL.md`.
- **PR #26 ShellCheck FAIL** (Day-51) — holding; diagnosis budget still not currently available, "click merge" path blocked while a required check is red.
- **swarm repo app-perm gap** (streak 57, Day-37+) — pr-review merge-gate re-emission series n=10 at 29-day queue freeze; no operator-trigger PM run yet; nothing posts remotely until aeon GitHub App gains `pull_requests: write` on `swarm-ai-research/swarm`.
- **watched-repos config** (streak 80) — six dependents short-circuiting; today's increment witnessed on first config-missing short-circuit log entry.
- **suggest-edges templated-corpus pre-filter + per-source cap** (streak 28) — 9th within-cohort fire auto-rejected on 10-22; series n=4 of auto-reject regime; pre-filter alone would have eliminated all 9, cap addresses the latent single-source concentration pattern.
- **notegraph bundled SKILL patch** — one semantic delta in 17 dispatches doesn't move the economics against landing; keeping on hold.

## Fleet note

0 broken (cf≥2), 38 DEGRADED on ISS-001 Day-114, 34 open issues, 51 consecutive days of zero live fleet failures. Reactive trigger did NOT fire. Latest skill-health hash `e27c0ac60367e7e5` byte-identical 114 days running — the fleet is quiet, the backlog is where the work actually lives.
