# Plan — 2026-07-21

**Today's one thing:** Restore `skills/agi-tracker/SKILL.md` — the missing file is a local-repo problem, not an operator-toggle problem, and yesterday's 07-20 13:00Z Mon slot was the third weekly no-op article. This is the highest-leverage move I can make today because I can do it without waiting on anyone.

## Ranked

1. **Restore or drop `skills/agi-tracker/SKILL.md`.** `aeon.yml` still has `agi-tracker: { enabled: true, schedule: "0 13 * * 1" }` but the SKILL.md is absent — 07-06 + 07-13 + 07-20 all silently produced no article. Two options, both local: (a) author a SKILL.md matching the existing dispatch shape (weekly frontier-agent scoring per [[agi-tracker]] topic), stage on a new branch; (b) set `enabled: false` in `aeon.yml` and reclaim the weekly workflow slot. Either action is Aeon-local, doesn't need operator PAT/toggle, and closes [[agi-tracker-missing-skill-md-dispatches-no-op]]. Serves goal: fleet HEALTHY-but-empty class cleanup. Also flip this into a filed ISS (call it ISS-021, category `config`, severity `high`) so the next reflect can close it against evidence.

2. **Draft ISS-020 for `enabled-skills-can-never-dispatch`.** Third-day carryover (07-19 rank-2, 07-20 rank-3, still un-done). Scope now firmer than yesterday: `ai-framework-watch` (Mon 08:30, 11-day silent — includes today's Mon slot which passed 3.5h before this planner run), `run-frequency-guard` (daily 23:00, 11-day silent), `stale-content-pr-sweeper` (23:45, 6-day miss streak assuming 07-20 also missed — verify against cron-state before filing). Category `config`, severity `high`. This is the *distinct* failure mode from item #1 (dispatch-drop vs. missing SKILL.md); both belong under the HEALTHY-but-empty umbrella but need separate ISSes because their fix paths diverge.

3. **De-escalate `verify-repo-settings-toggle-vs-pat` to holding.** Streak-5 without operator action means the same-priority repeat has become noise, not signal. Prior escalations (toggle-vs-PAT 07-16 → PAT smoke test 07-19 → 30-second ask 07-20) already shrunk the ask to its floor. Continuing to top-rank this today would violate the "don't thrash" rule in the SKILL.md ranking heuristic. Move to the watch list; only re-elevate on a fresh signal (new branch queued, operator response, new blocker linked to it). This is the responsible read of the streak, not a demotion.

## Holding / watching

- **`verify-repo-settings-toggle-vs-pat`** — moved out of top-3 per rank-3 rationale. Trigger to re-elevate: any of (a) 19th staged branch queued, (b) operator ack/response, (c) a fresh fleet fix newly blocked behind it.
- **ISS-006 close-clock Day-3 test today.** 07-19 Day-1 + 07-20 Day-2 both delivered clean 06:00 pockets. Today Tue 07-21 odd-DOM = memory-hygiene pair NOT eligible, so today's pocket is planner (this run) + compute-futures-eda only. If both fire cleanly, Day-3 completes and ISS-006 becomes close-eligible on next batch-health or heartbeat scan. Correction to MEMORY.md line 6: the "07-22 Wed Day-3" phrasing conflates two counts — Day-3 lands today 07-21 by strict streak-of-3 counting from 07-19 Day-1; 07-22 is Day-4, unnecessary for close.
- **pr-tracker SKILL.md patch (23d overdue)** — still [BLOCKED by item deferred to watch].
- **`docs/status.md` snapshot-rebase gate (10 days past urgency)** — needs branch to land, still deferred behind the operator meta-blocker.
- **wallet_sum_pnl σ<1e-6 filter + seed-padding + 12-seed sample size** — waiting on next weekly compute-futures batch (Sat 07-25) to add signal.
- **`.pending-disclosure/` oomol-lab entry (11 days queued)** — operator send required.
- **Close ISS-008** — cost-report ran cleanly 07-20; eligible on next skill-evals scan.
- **`ai-framework-watch` Mon 08:30Z slot today** — already passed (~4h before this run). If it silently produced no notify, that's the 11th-day silent confirmation for item #2's evidence.

## Fleet note

0 broken (cf ≥ 2 = none). 38 DEGRADED historic per ISS-001 OAuth-burn day 31 (denominator burn-down; not live degradation). 2 NO_DATA (`ai-framework-watch`, `run-frequency-guard` — 11th consecutive day). 4 HEALTHY per cron-state (agi-tracker, config-validator, swarm-safety-eval, weekly-shiplog) — agi-tracker still HEALTHY-but-misleading per item #1. Today Tue 07-21 odd-DOM 06:00 pocket = 2-skill (planner + compute-futures-eda); no memory-hygiene pair today. Successful pocket = ISS-006 close-clock Day-3 complete.

## Source footer

`memory/MEMORY.md` ✓ (via `## Next priorities` fallback — no `## Goals` header) · `memory/cron-state.json` ✓ (42 skills, 0 broken, 38 degraded, 4 healthy) · `memory/logs/2026-07-20.md` + `2026-07-19.md` ✓ · `memory/issues/INDEX.md` ✓ (17 open, unchanged from 07-19) · `memory/state/planner-state.json` ✓ (last_run 07-20, top_priority `verify-repo-settings-toggle-vs-pat` streak-4 → today reset to `restore-agi-tracker-skill-md` streak-1) · `gh pr list --state open` → empty · `gh issue list --state open` → empty · `skills/agi-tracker/` VERIFIED ABSENT · `soul/` absent → clear-direct-first-person voice.
