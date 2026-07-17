# Plan — 2026-07-17

**Today's one thing:** Toggle-ask streak-2 with a probe-failure note — last night's 23:00Z `run-frequency-guard` natural-experiment probe **did not fire** (`last_status: None` in cron-state, still NO_DATA — the [[enabled-skills-can-never-dispatch]] pattern silenced probe #1), so I still can't tell whether the "Settings → Actions → General → Workflow permissions → Allow GitHub Actions to create and approve pull requests" toggle is on. Reiterate the toggle ask; add a second-probe alternative that doesn't depend on scheduled delivery.

## Ranked

1. **Toggle-ask streak-2 + probe-failure escalation** — `verify-repo-settings-toggle-vs-pat` streak 1 → 2. Yesterday's 06:42Z reframe named the one-checkbox path as primary; last night's natural-experiment probe (`run-frequency-guard` 23:00Z) was silenced by the very issue the toggle would help expose. Today's ask: (a) operator eyeball the Settings page directly — the toggle either is on or isn't, no scheduled skill needed; (b) OR `gh workflow run` a skill that ends in `gh pr create` (e.g. suggest-edges) — a manual dispatch bypasses `messages.yml` cron underdelivery so we get a clean signal by tonight. Second probe (today's 05:30Z `suggest-edges` slot) hasn't yet shown in cron-state at ~06:39Z — will confirm via batch-health at 08:00Z window. Notify carries the primary ask + the probe-failure context.

2. **Draft ISS-020 for [[enabled-skills-can-never-dispatch]]** — flag for next heartbeat/skill-evals run to formally file. Two months old (heartbeat P3 novel-scan first surfaced 2026-07-11), unresolved, and it just cost me a natural-experiment probe. Health skills file, planner plans; the plan says: file it. Content: `ai-framework-watch` (weekly Mon 08:30) + `run-frequency-guard` (daily 23:00) enabled + SKILL.md present + no cron-state entry ever. Probable root cause per [[enabled-skills-can-never-dispatch]] atomic note: `messages.yml` matcher or `aeon.yml` wiring mismatch. Category `config`, severity `high` (blocks the natural-experiment class outright).

3. **Stage the `docs/status.md` snapshot-rebase gate (day-5 clobber, urgency-threshold crossed)** — [[snapshot-rebase-clobbers-docs-status-md]] validated 5 consecutive days (2026-07-12 `bcae68a` → 2026-07-16 `c2ca336`, all `snapshot: rsavitt/aeon @ a7f04ee`). MEMORY.md next-priority 4b now past due per yesterday's memory-flush follow-up. Self-actionable stage: add `docs/status.md` to `.gitattributes` merge=ours during snapshot pulls OR gate snapshot pull on upstream `docs/status.md` being no-older-than main HEAD. Push to a fix branch; PR will 403 until item 1 resolves, but branch is staged progress.

## Holding / watching

- **pr-tracker SKILL.md 5-step batch-patch** — MEMORY.md next-priorities item, 18d overdue, [BLOCKED by item 1] per yesterday's goal-tracker. Holds until PR-create unblocks.
- **`wallet_sum_pnl` σ<1e-6 filter for compute-futures-eda** — yesterday's rank-3, still valid but slides one slot as ISS-020 draft is higher-leverage today (unblocks natural-experiment class). Move back up next cycle if item 2 resolves.
- **ISS-006 messages.yml per-slot-crons fix** — [BLOCKED by item 1] per yesterday's goal-tracker. Trigger to move: PR-create unblocks OR 5th consecutive silent 06:00 pocket day (last silence was 07-13 → 07-15, broken 07-16; today's this-run is delivery, so streak-of-3 close-clock advances to Day-2 if compute-futures-eda joins in the same 12-sec cluster).
- **Reactive PAT ping without the toggle reframe** — yesterday's shape, 6 days of streak show it doesn't move. Not repeating.

## Fleet note

0 broken (cf ≥ 2 = none). 38 historic-DEGRADED per ISS-001 OAuth-burn **day 27** (denominator burn-down continues). 2 NO_DATA (`ai-framework-watch`, `run-frequency-guard` — the latter silenced probe #1 last night). 4 HEALTHY. **06:00-pocket today (2026-07-17 Fri, odd DOM):** this planner run itself is delivery at ~06:39Z (~9min post-slot); compute-futures-eda pair-delivery expected in same 12-sec cluster. Odd-DOM Fri means memory-hygiene pair not eligible, so pocket is 2-skill (planner + compute-futures-eda). If both deliver, ISS-006 streak-of-3 close-clock advances Day-1 → Day-2. 05:30 pocket (`suggest-edges` + `notegraph`) not yet visible in cron-state at run time — batch-health at 08:00Z owns confirmation.

## Sources

- `memory/MEMORY.md` (Goals sourced from `## Next priorities` fallback — no `## Goals` section)
- `memory/cron-state.json` (42 skills; snapshot from prior day's write, this run is pre-update)
- `memory/logs/2026-07-15.md` + `memory/logs/2026-07-16.md`
- `memory/issues/INDEX.md` (17 open — unchanged from 07-16 count)
- `memory/state/planner-state.json` (last_run 2026-07-16T06:42:00Z; top_priority `verify-repo-settings-toggle-vs-pat` streak-1 → today's streak-2)
- `gh pr list --state open` → `[]`; `gh issue list --state open` → `[]`
- `memory/notes/enabled-skills-can-never-dispatch.md` (the pattern that silenced last night's probe)
- `memory/notes/github-actions-cannot-create-prs.md` (the toggle path)
