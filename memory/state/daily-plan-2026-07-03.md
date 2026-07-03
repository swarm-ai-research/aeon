# Plan — 2026-07-03

**Today's one thing:** Ship the ISS-006 mitigation to a branch — rewrite `.github/workflows/messages.yml` with explicit per-slot crons covering every `aeon.yml` timeslot, so the operator can open the PR and end the 13-day multi-pocket dead zone.

## Context

I'm firing right now as a day-13 pocket recovery — I caught the ~07:35Z catch-up tick alongside `compute-futures-eda`, ~65 min late. Last recorded planner success was 2026-06-27T07:40Z (5+ days silent, per `cron-state.json`). This is the same delivery-rate variance called out in [[iss-006-pocket-recovery-is-noise]]; today's firing doesn't change the underlying `messages.yml` `*/5` ~3% delivery rate. The top priority is unchanged from the 2026-06-27 plan — that's day 2 of the streak on `iss-006-messages-yml-per-slot-crons`, and it's earned an escalation. I can create the branch; the operator opens the PR.

## Ranked

1. **Draft ISS-006 mitigation on a branch (`fix/iss-006-per-slot-crons`)** — Replace `messages.yml`'s `*/5 * * * *` with explicit per-slot crons matching every `aeon.yml` timeslot (05:00, 05:30, 06:00, 06:30, 07:00, 07:30, 08:00, 09:00, 09:30, 13:00 Mon, 14:00, 15:00, 17:00, 18:00, 18:30, 19:00, 21:00, 23:00, 23:45). Keep `messages-morning.yml` redundancy until 3 consecutive clean days. Escalation move: this has been queued since day 5 and I can materially advance it by shipping the diff to a branch — the operator only needs to open the PR (still blocked by the "GitHub Actions is not permitted to create or approve pull requests" repo policy, same gap as the other 5 staged branches).
2. **Reclassify ISS-005 → `permanent-limitation`** — Per [[swarm-safety-eval-empty-writes-log-not-article]], `swarm-safety-eval` is running successfully; its SSE_EMPTY path writes to the daily log by design (no `articles/*.md` when the swarm-safety ledger is absent). The `no_file_match` classification is a health-check assumption failure, not a real skill failure. Cheap update to `memory/issues/ISS-005.md` frontmatter + INDEX row — closes an "open" issue that isn't actually broken.
3. **Watch `Panniantong/Agent-Reach#436`** — Crosses the 7d stale threshold **today** (last `updatedAt` 2026-06-26T19:24Z). When `pr-tracker` fires this afternoon (schedule permitting) it will notify. This is passive on my part — noting so I don't re-flag if `pr-tracker` handles it.

## Holding / watching

- **Gitlawb fork `messages.yml` cross-check** — Still on the priority list. Cheap evidence that distinguishes per-repo throttle vs GHA platform behavior. Deferring until #1 lands on a branch — no point splitting attention.
- **Populate `memory/watched-repos.md`** — Standing operator-decision item; 4 skills (`code-health`, `github-monitor`, `issue-triage`, `changelog`) silently skip every day. Not moving today.
- **`pr-tracker` SKILL.md durable patch** (AND→OR filter + drop `headRefName`/`mergedAt`/`--state merged`) — Inline OR-filter has held 4 days. Patch when I touch pr-tracker for anything else.
- **`skill-freshness` mtime-blind fix** — Swap `stat --format=%Y` for `git log -1 --format=%ct` per [[skill-freshness-mtime-blind-in-gha]]. Not top-3 today; the current false-green isn't causing new failures, just hiding staleness signal.
- **The 5 staged operator-action branches** (`agi-tracker/2026-06-29`, `notegraph/2026-06-29`, `fix/workflow-security-audit-2026-06-28`, `skill-graph/2026-06-28`, `fix/workflow-security-audit-2026-06-21`) — All blocked by the same App perm gap that #1 will run into. If #1 escalates the perm gap it may unblock these too.
- **ISS-001 close** — Deferred until ISS-006 stabilizes, per existing MEMORY.md guidance.

## Fleet note

- 0 broken (`consecutive_failures >= 2`) · 0 dispatched-stuck · 38 degrading `success_rate < 0.5` — all ISS-001 OAuth-residue denominator drag, every one `last_status: success`, not actionable.
- 27 skills stale (last_success >72h): 8 of them are weekly/biweekly (`skillpacks` Sun, `compute-macro-correlate` Sun, `weekly-shiplog`, `memory-flush`/`-structural-dedupe` even-day) — expected. The remaining 19 include the 09:00 pocket (`fleet-control`, `github-monitor`, `issue-triage`, `pr-triage`, `skill-evals`) all silent since 2026-06-28, matching ISS-006's day-7 finding.
- Sources: cron-state ok, skill-runs ok, `gh pr list` = 0 open, `gh issue list` = 0 open. Local plan; no external blockers on producing it.
