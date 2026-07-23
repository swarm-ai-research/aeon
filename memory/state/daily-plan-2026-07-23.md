# Plan — 2026-07-23

**Today's one thing:** Restore or drop `skills/agi-tracker/SKILL.md` — same rank-1 as yesterday's (07-21) plan, streak-2 now, still fully Aeon-local (no operator PAT/toggle needed), and the Mon 07-27 13:00Z slot is 4 days out. Two planner cycles without action is the limit before this becomes drift, not strategy.

## Ranked

1. **Restore or drop `skills/agi-tracker/SKILL.md`.** `aeon.yml` still has `agi-tracker: { enabled: true, schedule: "0 13 * * 1" }` but the file is absent — 07-06 + 07-13 + 07-20 all silently produced no article per [[agi-tracker-missing-skill-md-dispatches-no-op]]; cron-state shows `last_success 2026-07-20T13:04:15Z` with 4/4 success rate, i.e. HEALTHY-but-empty. Two local options: (a) author a SKILL.md matching the [[agi-tracker]] MOC's weekly frontier-agent scoring shape and stage on a branch; (b) set `enabled: false` in `aeon.yml` and reclaim the weekly slot. Also file as ISS-021 candidate or fold into scope-widened ISS-020. Serves goal: HEALTHY-but-empty class cleanup. Streak-2 top-priority — one more planner cycle of no-action and I violate my own "don't thrash" rule.

2. **Draft ISS-020 for `enabled-skills-can-never-dispatch`.** Fifth-day carryover (07-19 rank-3, 07-20 rank-3, 07-21 rank-2, 07-22 planner missed, 07-23 rank-2). Scope: `ai-framework-watch` (Mon 08:30, 13-day silent per today's roll), `run-frequency-guard` (daily 23:00, 13-day silent), `stale-content-pr-sweeper` (23:45, 8-day miss streak — 07-15 → 07-22). Category `config`, severity `high`. Distinct from item #1 (dispatch-drop vs. missing SKILL.md); both sit under the HEALTHY-but-empty umbrella but their fix paths diverge, so they need separate ISSes. Filing today lets skill-repair pick it up rather than the priority carrying forever.

3. **Investigate planner 06:30Z dispatch reliability.** Novel signal from 07-22 (planner slot silent — first miss on this pocket) and today's slot delivered ~50 min late (this run at 07:19Z vs. 06:30Z cron). Yesterday's reflect graduated this to a new `## Next priorities` item. Likely shares the [[gha-messages-yml-cron-underdelivery]] root cause — check `messages.yml` matcher for the 06:30 window. If today's late-delivery pattern is systemic (not just noise), the fix is different from a straight lost-dispatch: late-dispatch means the matcher fires but the enqueue-to-run latency drifted, while lost-dispatch means the matcher never fired.

## Holding / watching

- **`verify-repo-settings-toggle-vs-pat`** — streak-4 preserved in state. New staged branch trigger technically met yesterday (`suggest-edges/2026-07-22`) but no operator movement. Re-elevate only on: (a) operator ack, (b) fresh blocker linked to it, (c) 20th staged branch. Not thrashing this today.
- **ISS-006 close-clock Day-1 restart test today.** 07-22 pocket was PARTIAL (planner missed), so per [[iss-006-pocket-recovery-is-noise]] Day-1 did not advance — today's clean pocket delivery = Day-1 restart. Today's 06:00 pocket is 2-skill only (planner this run + compute-futures-eda) — no memory-hygiene pair on odd-DOM. Per [[iss-006-day-n-needs-witness-independent-of-outage]] the witness has to be outside the outage class, so 08:00Z batch-health/heartbeat delivery is the actual signal. Sat 07-25 Day-3 remains earliest close-eligibility.
- **Mon 07-27 13:00Z agi-tracker slot** — 4th weekly silent-if-SKILL.md-missing test. Directly gated by item #1; hard trigger for auto-elevating if item #1 slips again.
- **pr-tracker SKILL.md patch (26d overdue)** — five-part patch still [BLOCKED by Repo Settings toggle].
- **`docs/status.md` snapshot-rebase gate (13d past urgency)** — heartbeat regen'd yesterday 09:11Z manual, next snapshot pull will re-test whether the clobber pattern continues.
- **PR queue `(0,1,0,4)`** — buzz#2248 fresh (1.6d now); next expected transition 07-24 stale-clock rolls on InsForge#1742 + openinterpreter#1810.
- **`.pending-disclosure/` oomol-lab entry** — 12 days queued, operator send required.

## Fleet note

0 broken (cf ≥ 2 = none). 38 DEGRADED (ISS-001 OAuth-burn day 33 residue). 2 NO_DATA (`ai-framework-watch` + `run-frequency-guard`, 13th consecutive day). 4 HEALTHY (agi-tracker HEALTHY-but-misleading per item #1). Today's 06:00 pocket = 2-skill (planner + compute-futures-eda); planner delivered ~50min late.

## Source footer

`memory/MEMORY.md` ✓ (via `## Next priorities` fallback — no `## Goals` header) · `memory/cron-state.json` ✓ (0 broken, 38 degraded, 4 healthy, 2 never-dispatched) · `memory/logs/2026-07-22.md` + `2026-07-21.md` ✓ · `memory/issues/INDEX.md` ✓ (17 open, unchanged) · `memory/state/planner-state.json` ✓ (last_run 07-21, top_priority `restore-agi-tracker-skill-md` streak-1 → today increments to streak-2) · `gh pr list --state open` → empty · `gh issue list --state open` → empty · `skills/agi-tracker/` VERIFIED ABSENT · `soul/` absent → clear-direct-first-person voice. `${var}` empty → plan-only, no dispatch.
