# Plan — 2026-07-19

**Today's one thing:** Streak-3 escalation on `verify-repo-settings-toggle-vs-pat` — reframe from "toggle vs PAT" to a concrete one-branch smoke test: ask operator to run the swarm#527-validated PAT against ONE trivial in-repo staged branch (`notegraph/2026-07-18`, +1-node diff, zero risk) to prove PAT scope covers in-repo `gh pr create` + merge. If it works, the 16-branch queue is batch-closeable and unblocks pr-tracker patch (21d overdue), ISS-006 fix, snapshot-rebase gate, and 6 other stalled fleet fixes in one operator sweep.

## Ranked

1. **Streak-3 escalation via one-branch PAT smoke test** — `verify-repo-settings-toggle-vs-pat` was streak-2 at last planner run (2026-07-17); 07-18's planner miss meant no update; keeping same priority today advances streak 2 → 3 per SKILL.md escalation rule. Six days of streak show the "please flip the Settings toggle" ask doesn't move; escalation must change shape, not just repeat. New evidence: **operator PAT merged swarm#527 on 2026-07-18T02:29:19Z**, the first proof that this PAT is live for cross-org merges. Concrete escalation ask today: operator run the same PAT against `notegraph/2026-07-18` (staged origin branch, trivial +1-node graph diff, no schema/content change, safe merge) — attempt `gh pr create` + merge. Three possible outcomes, all valuable: (a) PAT works in-repo → batch-close remaining 15 staged branches next run and file structured PR queue for pr-tracker/ISS-006/snapshot-gate; (b) PAT fails at `pr create` → scope must be bumped (`repo` scope confirmed missing); (c) PAT works `pr create` but fails merge → confirms the split between GHA-bot identity and operator identity for merge approvals. Either way, blocker resolves off "unknown" into a specific next action.

2. **Draft ISS-020 for `enabled-skills-can-never-dispatch` — widen scope to include `stale-content-pr-sweeper`** — held from 07-17 rank-2, still unfiled. 07-18 heartbeat surfaced a novel P3 stale flag: `stale-content-pr-sweeper` (daily `45 23 * * *`) at 3-day miss streak (07-15/16/17), first stale-streak since the 06-24/25 outage per [[gha-messages-yml-cron-underdelivery]]. This is a fresh instance of the same dispatch-drop root cause that silences `ai-framework-watch` (weekly Mon 08:30) + `run-frequency-guard` (daily 23:00) — MEMORY.md next-priority already flagged the fold. ISS-020 draft content: category `config`, severity `high`, affected skills `ai-framework-watch` + `run-frequency-guard` + (probably) `stale-content-pr-sweeper`, root cause hypothesis `messages.yml` matcher / `aeon.yml` wiring mismatch or 23:00–23:59 pocket cron delivery gap. Filing blocks the natural-experiment probe class outright per [[probes-for-messages-yml-must-dispatch-outside-messages-yml]]. Flag for next heartbeat/skill-evals run.

3. **Note the 07-18 planner-miss as project-memory** — planner missed the 07-18 06:30 slot (last successful run 2026-07-17T06:36:43Z, no `## Planner` header in 07-18 log; batch-health flagged WARN). First planner miss in the record — planner has fired reliably every prior day. Batch-health's stated escalation trigger was "if planner misses again 07-19, escalate to project-memory investigation" — this run IS today's 06:30 slot delivery, so cadence is restored and the 07-18 gap is a single-day dropout. Still worth an atomic note for the 06:00 pocket: this is now a second recurrence of the [[gha-messages-yml-cron-underdelivery]] pattern reaching a critical skill (ISS-006 close-clock leg), not just P3 stale flags on rarely-used skills. Note the ISS-006 close-clock impact: 07-18's miss halted Day-2 → Day-3 close. Actionable next step for a future run: cross-check planner's `messages.yml` matcher line against the four skills that DID deliver at 06:20Z (memory-flush, memory-structural-dedupe, compute-futures-eda, notegraph, suggest-edges) — planner's slot is `30 6 * * *`, others cluster earlier; possibly the 06:30 slot itself is inside a delivery pocket.

## Holding / watching

- **pr-tracker SKILL.md 5-step batch-patch** — MEMORY.md next-priorities item, 21d overdue, [BLOCKED by #1]. Trigger to promote: PAT-scope smoke test succeeds and PR queue unblocks.
- **`docs/status.md` snapshot-rebase gate** — 8 days past 2026-07-16 urgency threshold; 07-18's upstream ref rotation `a7f04ee → fa89d8c` with same clobber outcome **confirmed root cause is snapshot-merge itself**, not stale upstream state. Self-actionable stage per [[status-md-auto-commit-drops-writes]] + [[snapshot-rebase-clobbers-docs-status-md]] but PR would 403 without #1 — holding until either operator merges the staged branch or #1 resolves. Trigger to promote: streak-3 smoke test fails and staged-branch batch-close doesn't materialize.
- **ISS-006 fix (`messages.yml` per-slot crons)** — close-clock reset by 07-18 planner miss; today is fresh Day-1 (if planner + compute-futures-eda both fire this pocket). No urgent action; [BLOCKED by #1] per goal-tracker 2026-07-16.
- **`wallet_sum_pnl` σ<1e-6 filter for compute-futures-eda** — held from 07-17 (yesterday's holding). Still valid, not top-of-queue.
- **`.pending-disclosure/` queue (1 entry: oomol-lab/open-connector GCM-tag-length medium, 2026-07-11)** — vuln-scanner 07-18 target clean, no new candidates. Held; no operator action needed today.
- **AGI Tracker next slot 2026-07-20 Mon 13:00 UTC** — tomorrow; 3-run silence streak (last article 2026-06-29). Not actionable today; watching whether tomorrow's run breaks silence or extends to 4.

## Fleet note

0 broken (cf ≥ 2 = none). 38 historic-DEGRADED per ISS-001 OAuth-burn **day 29** (denominator burn-down continues; recovery 2026-06-20T06:05Z + 29d = 2026-07-19). 2 NO_DATA (`ai-framework-watch`, `run-frequency-guard` — both fed into #2). **+1 P3 stale flagged 07-18**: `stale-content-pr-sweeper` (23:45 pocket, 3-day miss streak). 4 HEALTHY (`weekly-shiplog`, `config-validator`, `swarm-safety-eval`, `agi-tracker`). **06:00 pocket today (Sun 2026-07-19, odd-DOM 19):** memory-hygiene pair NOT eligible (even-DOM only per `0 6 2/2 * *`), so pocket is 2-skill (planner + compute-futures-eda). If both fire, ISS-006 close-clock advances Day-0 → Day-1 (fresh count after 07-18 restart).

## Sources

- `memory/MEMORY.md` (Goals sourced from `## Next priorities` fallback — no `## Goals` section)
- `memory/cron-state.json` (42 skills)
- `memory/logs/2026-07-17.md` + `memory/logs/2026-07-18.md`
- `memory/issues/INDEX.md` (17 open — unchanged from 07-18 count)
- `memory/state/planner-state.json` (last_run 2026-07-17T06:39:05Z; top_priority `verify-repo-settings-toggle-vs-pat` streak 2 → today's streak 3)
- `gh pr list --state open` → `[]`; `gh issue list --state open` → `[]`
- `memory/notes/enabled-skills-can-never-dispatch.md` (the pattern folded into #2)
- `memory/notes/github-actions-cannot-create-prs.md` (the meta-blocker behind #1)
- `memory/notes/snapshot-rebase-clobbers-docs-status-md.md` (07-18 upstream ref rotation confirmed root cause)
