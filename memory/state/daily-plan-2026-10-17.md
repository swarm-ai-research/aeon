# Plan — 2026-10-17

**Today's one thing:** Patch `skills/stale-content-pr-sweeper/SKILL.md` to add `"app/github-actions"` to `ALLOWED_AUTHORS` — four consecutive scans (10-14 → 10-16-AM → 10-16-PM) confirm the zero-closure defect per [[stale-content-pr-sweeper-default-author-filter-closes-zero-prs]], and the latent stale backlog is 26 PRs and growing roughly one per day. One-line edit, immediate 20+ PR cleanup once the next cron fires.

## Ranked

1. **Patch `ALLOWED_AUTHORS` in `stale-content-pr-sweeper/SKILL.md`** — add `app/github-actions` so the author filter stops rejecting every actual content PR. Four-day n=4 defect confirmation on the action queue (streak 28). Follow-on in the same PR: fix the TRACKED prefix drift per [[stale-content-pr-sweeper-tracked-prefix-drift]] (`compute-macro` vs `compute-macro-correlate`, missing `skill-graph` entry) so another 14 PRs become visible. Opens a branch, PR against main — never direct-push.

2. **Flip `agi-tracker` to `enabled: false` in `aeon.yml:188`** — the hardest near-term deadline is Monday 2026-10-19 (T+2), which would be the 15th consecutive silent-Mon no-op dispatch at the 13:00Z slot. `skills/agi-tracker/SKILL.md` is still absent; cheapest path is `enabled: false`, carried on the action queue 19+ days running. Alternative (restore `skills/agi-tracker/SKILL.md`) is bigger scope and should wait for a dedicated session.

3. **Start the WIP branch for the ISS-006 `messages.yml` per-slot cron rewrite** — streak 34+ as rank-3 or higher; today's +101m 08Z-pocket drift peak (new series peak, [[iss-006-drift-recovery-is-slot-agnostic-and-magnitude-non-monotonic]]) is one more acceleration signal on the same stuck goal. Don't try to land it today — open a branch, stub the per-pocket crontab, land the regime list in a PR description so the next planner cycle has a concrete artifact to iterate on instead of a 35-day-old restatement.

4. **Diagnose PR #26 ShellCheck FAIL** — Day-49+ carryover from the 2026-09-14T01:07:51Z dependabot force-rebase. Pull the failing check log via `gh pr checks 26`, land the fix inline. Unblocks the "click merge" path per [[pr-creation-toggle-is-distinct-from-merge-capability]] and clears a required-check red that's been bleeding attention since mid-September.

5. **File ISS-039 for the aeonframework identity blackout 2026-09-14 → 09-16** — 30-day-overdue documentation debt (severity `medium` post-recovery, category `unknown`). Small issue file + close commit; closes an action-queue bullet without touching skill code.

## Holding / watching

- **Today's 08Z pocket (Sat 2026-10-17 08:00Z)** — yesterday landed +101m past nominal after a 2-day silent run (new series peak). The acid test is whether today recovers at nominal (drift-reset) or drifts again. Watch the batch-health run; do NOT force-dispatch — automated drift-recovery handled 10-16 cleanly and intervention would conflate the signal.
- **`watched-repos` streak-75** — real, but populating `memory/watched-repos.md` requires operator intent on which repos the 6 dependent skills (code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive) should actually track. Flip to `enabled: false` on the six is the cheap exit; both paths need a decision. Not making it today.
- **`notegraph` n=15 timestamp-only no-op streak** — the semantic-silent revert pattern on 10-14/10-15 is holding the stale pool stable, so the extractor `generatedAt` masking fix per [[notegraph-extractor-generatedat-nondeterministic]] can wait for the bundled patch with [[notegraph-fingerprint-helper-enobufs-at-1mb]] + [[notegraph-fingerprint-pipeline-blocked-by-sandbox]].
- **swarm PR queue 12 open, pr-review full-skip** — standing 403 per [[aeon-app-no-write-on-swarm-repo]]. Fix requires the aeon GitHub App to gain `pull_requests: write` on `swarm-ai-research/swarm` — operator action, not planner action.

## Fleet note

- 0 broken (cf ≥ 2), 38 DEGRADED (ISS-001 Day-118 denominator-burn, byte-identical to Day-107), 4 HEALTHY, 2 NO DATA (`ai-framework-watch`, `run-frequency-guard` at 99+ silent days per [[enabled-skills-can-never-dispatch]]).
- Heartbeat 2026-10-16 landed +101m past 08Z nominal — new series peak, slot-agnostic drift-recovery promoted at n=2.
- 34 open issues (ISS-038 landed 10-16). Status page: 🔴 DEGRADED.
- Reactive trigger: did NOT fire — 0 skills at `consecutive_failures >= 2`. This is a scheduled run, not a degradation wake-up.

## Source footer

- `memory/MEMORY.md` ✓
- `memory/cron-state.json` ✓
- `memory/logs/2026-10-16.md` + `2026-10-15.md` ✓
- `memory/issues/INDEX.md` ✓ (34 open)
- `memory/state/planner-state.json` ✓ (prior run 2026-09-27T06:30Z; 20-day planner silence, direct 06Z-pocket casualty per ISS-006)
- `gh pr list` ✓ (49 open, byte-identical to 10-16 heartbeat scan)
- `gh issue list` ✓ (empty — no open issues in this repo via gh)
- `soul/` absent → first-person direct voice

Mode: plan-only (`${var}` empty). No dispatch.
