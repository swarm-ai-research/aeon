# Plan — 2026-07-20

**Today's one thing:** Escalate `verify-repo-settings-toggle-vs-pat` to streak-4 with a **30-second ask** — one URL to click OR one command to run — because four planner runs (07-16 → 07-17 → 07-19 → 07-20, with 07-18 miss) with the same top priority haven't moved the meta-blocker under 18 staged branches.

## Ranked

1. **Streak-4 escalation on `verify-repo-settings-toggle-vs-pat` — shrink the ask to a 30-second action.** Prior reframes (toggle-vs-PAT → PAT smoke test on `notegraph/2026-07-18`) haven't landed. Today's ask, in operator-actionable form: **(a) click** https://github.com/aeonframework/aeon/settings/actions → Workflow permissions → tick "Allow GitHub Actions to create and approve pull requests" → Save. **OR (b) run** `gh pr create -R aeonframework/aeon --base main --head notegraph/2026-07-18 --title "graph: +1 orphan cleared" --body "auto"` under the swarm#527-validated PAT. Either unblocks the queue (now **18 branches**) and 6 downstream fleet fixes. Serves goals 1, 2, 5 (all BLOCKED per 07-19 goal-tracker).
2. **File the agi-tracker missing-SKILL.md finding as a structured issue** (today, before the 13:00Z Mon slot). 07-19 config-validator flagged `skills/agi-tracker/SKILL.md` absent while `aeon.yml` has `agi-tracker: { enabled: true, schedule: "0 13 * * 1" }`. Explains the 07-06 + 07-13 silent Mon slots. **Third weekly attempt is today at 13:00Z** — will silently produce no article again unless surfaced. Category `config`, severity `high`; unblocks a weekly-cadence signal producer. This is the kind of finding ISS-020 was meant to formalize — file it as its own issue (call it ISS-021 or fold into ISS-020's scope-widening).
3. **Draft ISS-020 for `enabled-skills-can-never-dispatch`** (rank-2 on 07-19; still un-done today). Scope: `ai-framework-watch` (Mon 08:30, now 10-day silent), `run-frequency-guard` (daily 23:00, now 10-day silent), `stale-content-pr-sweeper` (23:45 slot, 5-day miss streak as of 07-19). Category `config`, severity `high`. Flag for next heartbeat/skill-evals run to file. Adding item #2 (agi-tracker) is a natural sibling — same root shape (enabled-but-doesn't-produce), different failure mode (missing SKILL.md vs. dispatch-drop).

## Holding / watching

- **pr-tracker SKILL.md patch (22d overdue)** — blocked behind item #1.
- **`docs/status.md` snapshot-rebase gate (9 days past urgency)** — needs branch/PR to land; blocked behind item #1. Watch today's snapshot commit for 8th-day upstream ref pattern.
- **wallet_sum_pnl σ<1e-6 filter + seed-padding + 12-seed sample size** — waiting on next weekly compute-futures batch to add signal; no action today.
- **`.pending-disclosure/` oomol-lab entry** — awaiting operator send.
- **Weekly cadence today (Mon 07-20):** `weekly-shiplog` 09:00Z (last 07-06, ~336h threshold — first opportunity in ~14d), `milestone-tracker` 12:00Z, `ai-framework-watch` 08:30Z (10-day silent test). If any of the three fire, it's fresh cadence data.

## Fleet note

0 broken (cf ≥ 2 = none). 38 DEGRADED historic per ISS-001 OAuth-burn day 30 (denominator burn-down; not live degradation). 2 NO_DATA (`ai-framework-watch`, `run-frequency-guard` — 10th consecutive day). 4 HEALTHY per cron-state (agi-tracker, config-validator, swarm-safety-eval, weekly-shiplog) — but agi-tracker's HEALTHY status is misleading given the missing SKILL.md per item #2. **Today Mon 07-20 even-DOM 06:00 pocket** = 4-skill (planner + compute-futures-eda + memory-flush + memory-structural-dedupe). Successful pocket delivery advances ISS-006 close-clock from 07-19's Day-1 → Day-2; earliest close **Tue 07-21 Day-3** assuming clean 07-20 + 07-21 pockets.

## Source footer

`memory/MEMORY.md` ✓ (via `## Next priorities` fallback — no `## Goals`) · `memory/cron-state.json` ✓ (42 skills) · `memory/logs/2026-07-19.md` + `2026-07-18.md` ✓ · `memory/issues/INDEX.md` ✓ (17 open, unchanged from 07-19) · `memory/state/planner-state.json` ✓ (streak 3 → 4) · `gh pr list` = empty · `gh issue list` = empty · `soul/` absent → clear-direct-first-person voice default · `skills/agi-tracker/` ✓ VERIFIED ABSENT.
