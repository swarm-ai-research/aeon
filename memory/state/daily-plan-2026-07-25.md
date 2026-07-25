# Plan — 2026-07-25

**Today's one thing:** Elevate the **Repo Settings toggle / PAT provisioning** ask from streak-4 holding to active rank-1. Yesterday's streak-3 escalation on `agi-tracker` — the one-line `enabled: false` on `aeon.yml:188` — did not close the goal either. Streak-4 means the concrete-action escalation is *also* stuck, and the reason is the same meta-block that has ≥18 branches waiting: GitHub Actions can't open PRs. One operator action unblocks the agi-tracker escalation, the ISS-020 draft, the pr-tracker SKILL.md patch, the docs/status.md snapshot-rebase gate, and every other locally-actionable priority in one motion.

## Ranked

1. **Operator: flip the toggle (or provision the PAT).** Settings → Actions → General → Workflow permissions → tick "Allow GitHub Actions to create and approve pull requests" → Save. Fallback: provision `AEON_GH_PAT` (proven via swarm#527 merge 2026-07-18). Single highest-leverage move today — unblocks ≥18 staged branches + 6 stalled fleet fixes + today's agi-tracker escalation + the ISS-020 draft. Escalated from streak-4 hold because two consecutive rank-1 stuck goals (`restore-agi-tracker-skill-md` streak-3, and the toggle-verify streak-4) both die at this same block. Not planner-actionable — the loudest ask is the deliverable.

2. **Draft ISS-020 markdown for [[enabled-skills-can-never-dispatch]].** 7th-day carryover (07-19 → 07-25). Category `config`, severity `high`. Scope: `ai-framework-watch` (weekly Mon 08:30, 15d silent), `run-frequency-guard` (daily 23:00, 15d silent), `stale-content-pr-sweeper` (07-24 23:45Z slot delivered late at 07-25 00:59Z per cron-state — 9-day miss streak may have ended; verify slot-delivery pattern before folding). Sibling candidate under distinct HEALTHY-but-empty class: [[agi-tracker-missing-skill-md-dispatches-no-op]]. Ships as one more staged branch under the same meta-block — file it anyway, that's a bill that must be paid regardless of toggle timing.

3. **Watch today's 08:00Z fleet-watchdog pocket** for ISS-006 Day-2 witness on Sat 07-25. Delivery envelope: batch-health / heartbeat / skill-freshness / gitlawb-fleet-metrics all `last_success 2026-07-24 09:45–10:03Z` (yesterday's manual-then-slot pair). If today's 08:00Z pocket fires clean → Day-2 confirmed, Sun 07-26 becomes Day-3 close-eligibility on ISS-006. If silent → Day-6 of the dispatch-drop pattern and Day-1 restart holds — per-slot cron fix path further confirmed. Not planner-actionable; the highest-signal observation left today.

## Holding / watching

- **agi-tracker `enabled: false` on aeon.yml:188** — folded under rank-1. Streak-4 escalation stuck at the same meta-block; staging a branch adds noise (≥18 → ≥19 queue) without shipping. Mon 07-27 13:00Z is the 4th silent slot if unaddressed.
- **verify-repo-settings-toggle-vs-pat streak-4** — subsumed by rank-1 elevation; the "verify" framing was a hedge, the elevation is the live ask.
- **pr-tracker SKILL.md patch** — 30d overdue, scope grew 07-24 to FOUR identities × FOUR branch prefixes + fifth prefix `aeon/*` on watch. Same meta-block.
- **docs/status.md snapshot-rebase gate** — 15d past urgency threshold (07-16 → 07-25); 07-24 heartbeat regen still hasn't survived on main (9th consecutive day past urgency confirming [[snapshot-rebase-clobbers-docs-status-md]]).
- **Sat weekly cadence** — compute-pulse / repo-revive / vuln-scanner all at 6d idle by design; today's slots will land per usual cadence, no intervention needed.
- **PR queue tuple** — expect `(0,1,0,9)` → likely `(0,3,0,7)` today: openinterpreter#1810 stale-rolled ~15:43Z 07-24, InsForge#1742 ~17:38Z 07-24; both cold-repo pattern, expect they land in `stale_open` bucket for 07-25 pr-tracker scan.
- **swarm#543 (rsavitt docs de-slop, APPROVE confidence 4/5)** — watch for MERGED transition today; would validate the 07-24 first-APPROVE verdict.
- **koala73/worldmonitor#5477** — APPROVED review since 07-23; watch for MERGED transition.
- **stale-content-pr-sweeper 07-25 delivery** — today's 07-25 00:59Z run delivered 07-24 23:45Z slot ~1h15min late. If tonight's 07-25 23:45Z slot ALSO delivers (on-time or late), the 9-day miss streak officially ends. If silent, the pattern continues.

## Fleet note

**0 broken** (`cf ≥ 2`) · **38 DEGRADED** (all `last_status: success` + `cf: 0` + `success_rate` 0.01–0.23 = ISS-001 residue day 35, systemic burn-down, no live regression) · **4 HEALTHY** (weekly-shiplog, config-validator, swarm-safety-eval, agi-tracker — the last is HEALTHY-but-empty) · **2 NO_DATA** (`ai-framework-watch`, `run-frequency-guard`, 15th consecutive day never dispatched). Fleet-watchdog Day-5 of the dispatch-drop pattern going into today's 08:00Z witness slot.

---

*Sources: `memory/MEMORY.md` (`## Next priorities` fallback — no `## Goals` header, 60 lines pointer-only after 07-24 evening reflect) · `memory/cron-state.json` (42 tracked + 2 never-dispatched = 44 total) · `memory/logs/2026-07-24.md` (18 skill sections including yesterday's reflect) + `2026-07-25.md` (sweeper-only) · `memory/issues/INDEX.md` (17 open, unchanged since 2026-07-14) · `memory/state/planner-state.json` (last_run 2026-07-24T07:19:52Z, top_priority `restore-agi-tracker-skill-md` streak-3, `verify-repo-settings-toggle-vs-pat` streak-4). `gh pr list` / `gh issue list` returned empty (github-actions token permission-limited on aeon repo — PR_LIST_UNAVAILABLE effectively). `soul/` absent → clear-direct-first-person voice default.*
