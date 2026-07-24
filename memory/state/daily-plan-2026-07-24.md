# Plan — 2026-07-24

**Today's one thing:** Escalate `restore-agi-tracker-skill-md` from vague "restore or drop" to a specific unilateral action — set `agi-tracker: { enabled: false, ... }` on `aeon.yml` line 188. Streak-3 hits my own SKILL.md's "stuck goal — escalate, don't just re-list" line; two prior planner cycles (07-21, 07-23) produced no action under the vague framing. Fully Aeon-local, reversible, and lands before Mon 07-27 13:00Z would be the 4th weekly silent slot.

## Ranked

1. **Set `enabled: false` on `aeon.yml:188` for `agi-tracker`.** Priority streak-3 (07-21 → 07-23 → today; 07-22 planner missed the 06:30Z slot). Per SKILL.md ranking heuristic, 3+ days as "today's priority" without a log entry closing it = stuck goal, escalate. Disable is the lower-friction of the two 07-21 options (vs authoring a full SKILL.md matching the [[agi-tracker]] MOC's weekly frontier-agent scoring shape) — no evidence anyone is drafting a SKILL.md, and disabling immediately reclaims the weekly slot without commit-history mess. Trivially reversible: flip back to `enabled: true` when a SKILL.md gets authored. Ships as a one-line branch that doesn't hit the [[github-actions-cannot-create-prs]] PR-open block. Serves goal: HEALTHY-but-empty class cleanup.

2. **Draft ISS-020 for [[enabled-skills-can-never-dispatch]].** Sixth-day carryover (07-19 rank-3, 07-20 rank-3, 07-21 rank-2, 07-22 planner missed, 07-23 rank-2, today rank-2). Scope: `ai-framework-watch` (weekly Mon 08:30, **14-day silent** as of today), `run-frequency-guard` (daily 23:00, **14-day silent**), `stale-content-pr-sweeper` (23:45, **9-day miss streak** 07-15 → 07-23). Category `config`, severity `high`. Distinct from item #1: this class is dispatch-drop on files that DO exist; item #1 is dispatch-hits-but-no-work on a file that doesn't exist. Sibling scope candidate — fold in the 06:30Z planner + 08:00Z fleet-watchdog pocket delivery-reliability findings if today's 08:00Z pocket misses again. Filing today lets skill-repair pick it up rather than the priority carrying to streak-7.

3. **Watch today's 08:00Z fleet-watchdog pocket (Day-5 of the dispatch-drop pattern).** Timeline: 07-20 silent · 07-21 silent · 07-22 late auto-recovery (~09:08Z, ~1h late) · 07-23 silent → operator manual (~09:55Z). Today = Day-5. If auto-delivery lands, the 07-22 auto-recovery wasn't a one-off; if it silently misses again, the pattern hardens and folds into ISS-020 scope. Per [[iss-006-day-n-needs-witness-independent-of-outage]] the Day-2 ISS-006 close-clock advance requires today's pocket to deliver on independent witness — a manual heartbeat doesn't count. Sun 07-26 remains earliest Day-3 close-eligibility; every additional partial pushes it to Mon 07-27+.

## Holding / watching

- **`verify-repo-settings-toggle-vs-pat`** — streak-4 preserved in state. No operator movement despite the 07-22 `suggest-edges/2026-07-22` staged branch. Re-elevate only on: (a) operator ack, (b) fresh blocker linked to it, (c) 20th staged branch. Not thrashing this today.
- **Mon 07-27 13:00Z agi-tracker slot** — 4th weekly silent-if-SKILL.md-missing test; direct gate on item #1. If item #1 lands today or over the weekend, the slot goes silent by design (correct) rather than silent by config-drift (broken).
- **ISS-006 close-clock Day-2 test today.** Yesterday was Day-1 restart (07-23 PARTIAL — the 08:00Z manual heartbeat doesn't count as independent witness); today's clean pocket delivery = Day-2. Sun 07-26 = earliest Day-3 close-eligibility.
- **pr-tracker SKILL.md patch — 29d overdue** (28 → 29 today). Five-part patch still [BLOCKED by Repo Settings toggle]. Scope unchanged: 3 signing identities × 3 branch prefixes + hash dedup + fresh-bot-PR trigger + `stateReason`/`headRefName`/`mergedAt` drops.
- **`docs/status.md` snapshot-rebase gate — 14d past urgency threshold** (07-16 + 14 = today). 07-23 heartbeat wholesale-rewrote from 44d-stale baseline; next snapshot pull will re-test the [[snapshot-rebase-clobbers-docs-status-md]] clobber pattern.
- **PR queue tuple change expected today** — 07-23 was `(0,1,0,6)`; openinterpreter#1810 + InsForge#1742 stale-clocks roll today → next pr-tracker run likely `(0,3,0,4)` on hash change alone even absent new files. Would trigger a SEND on the SKILL.md step-5 stale-clause.
- **`.pending-disclosure/` oomol-lab entry** — 13 days queued (12 → 13). Operator send required; the queue itself isn't on-disk, MEMORY-tracked only.

## Fleet note

0 broken (cf ≥ 2 = none). 38 DEGRADED (ISS-001 OAuth-burn residue day 34). 2 NO_DATA (`ai-framework-watch` + `run-frequency-guard`, 14th consecutive day). 4 HEALTHY (agi-tracker HEALTHY-but-empty pending item #1). Today's planner running ~50 min late (07:19Z vs 06:30Z scheduled slot), consistent with 07-23's ~47min late delivery — late-dispatch not lost-dispatch. 06:00Z pocket (compute-futures-eda + memory-flush + memory-structural-dedupe on even-DOM) has not delivered at 07:19Z either; will fold into today's batch-health report.

## Source footer

`memory/MEMORY.md` ✓ (`## Next priorities` fallback — no `## Goals` header) · `memory/cron-state.json` ✓ (42 tracked, 0 broken cf≥2, 38 DEGRADED per ISS-001, 4 HEALTHY, 2 never-dispatched) · `memory/logs/2026-07-23.md` + `2026-07-22.md` ✓ · `memory/issues/INDEX.md` ✓ (17 open, unchanged since 2026-07-14) · `memory/state/planner-state.json` ✓ (last_run 2026-07-23T07:19:46Z, top_priority `restore-agi-tracker-skill-md` streak-2 → increments to streak-3 today; `verify-repo-settings-toggle-vs-pat` streak-4 held) · `gh pr list --state open` → empty · `gh issue list --state open` → empty · `skills/agi-tracker/` VERIFIED ABSENT · `aeon.yml:188` located · `soul/` absent → default clear-direct-first-person voice. `${var}` empty → plan-only, no dispatch.
