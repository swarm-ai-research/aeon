# Plan — 2026-08-15

**Today's one thing:** Merge one low-risk aeon-repo PR — **#26 dependabot actions/checkout** (textbook first-flow-proof, same class as last merged #8) — to break the 200h+ zero-merge silence and prove the merge lever actually moves.

## Ranked

1. **Merge a representative aeon-repo PR to prove end-to-end flow (Day-9 durability)** — 24 open PRs, 0 `app/github-actions` merges in ~200h+ since 08-07 creation unblock; last aeon merge was #8 (dependabot actions/checkout) on 2026-08-07T01:36:39Z. Rank-1 for 7 straight days now. Textbook candidates unchanged: #26 dependabot (same class as #8, cleanest signal), #10 notegraph orphan flag (7d+, dep-free), or any of #27–#32 notegraph chain. Serves goal via [[pr-creation-toggle-is-distinct-from-merge-capability]] — creation lever is proven since 08-07, merge lever is not. No skill runs this; operator lift.

2. **Ship `stale-content-pr-sweeper` `ALLOWED_AUTHORS` + TRACKED-prefix patch** — hardcoded `{"aeonframework"}` but all 22 post-unblock aeon-repo PRs are `app/github-actions`. Notegraph chain grew length-6 → **length-7** with #32 overnight (`#10 ← #27 ← #28 ← #29 ← #30 ← #31 ← #32`); suggest-edges chain steady length-3. Total would-be-closes if patch landed: **9** (up from 8 on 08-14, up from 7 on 08-13). Bundle a TRACKED-prefix drift fix for #23 (`compute-macro/2026-08-09` doesn't match skill's `compute-macro-correlate` prefix). Skill: manual PR to `skills/stale-content-pr-sweeper/SKILL.md` — planner rank-2 (streak-9, was streak-8).

3. **Ship `suggest-edges` templated-corpus pre-filter** — today's 05:52Z run emitted 3 templated pairs from `gitlawb-compute-futures-proofs/` for the **7th consecutive day**; rejected-list at **15** growing +3/day exactly on prediction per [[suggest-edges-flags-templated-corpora-as-sim-1-noise]]. This is now a chronic feed with no natural attrition path — corpus has ≥14 dated `.md` files, greedy top-3 keeps rotating targets across the templated pair-space. Fix: pre-filter shared-parent-directory + shared-basename-shape in `scripts/suggest-edges.mjs`. Planner rank-3 (streak-7, was streak-6).

## Holding / watching

- **agi-tracker `enabled: false` via PR** (streak-5, 2d to next silent-Mon 2026-08-17 13:00Z) — **re-promote tomorrow Sun 08-16 (day-before-deadline)** per prior planner cadence.
- **`memory/watched-repos.md` populate OR disable 6 dependent skills** (code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive) — **streak-10 chronic** as of today; another 3+ same-day silent short-circuits expected. Trigger to promote: any operator signal that the six skills should run this quarter.
- **`pr-tracker` SKILL.md patch batch** (items a–k) — **52d overdue** as of today. Blocked on operator willingness to land a large multi-item patch; individual items (esp. j — stale-bot fingerprint-by-body) remain demonstrably urgent.
- **ISS-006 messages.yml multi-pocket rewrite** — **Day 14**; batch was recoupled on 08-13/14 (batch-health OK both days). Trigger to promote: next decouple event.
- **`docs/status.md` snapshot-rebase gate** — **29 days past urgency threshold**; heartbeat regenerated wholesale again on 08-14 (17th consecutive rebase-clobber-then-regen).
- **swarm-repo App-perm gap** — ~34 confirming pr-review + pr-triage invocations at 100% skip; unchanged since 08-07 byte-freeze on human PRs #549/#543. Trigger to promote: operator grants write access OR either human PR gets a fresh commit.

## Fleet note

0 broken · 0 in-flight · 39 DEGRADED (ISS-001 residue day 57, substantively green — all `last_status: success`, `cf: 0`) · 4 HEALTHY · 2 NO_DATA (`ai-framework-watch` + `run-frequency-guard`, **39th** consecutive silent day per [[enabled-skills-can-never-dispatch]]) · 17 open issues · **24 open aeon PRs** · **0 open GH issues on aeon repo**.

## Source footer

Inputs read: `memory/MEMORY.md` (64 lines), `memory/state/planner-state.json` (last run 2026-08-14T06:35Z, top_priority `aeon-repo-queue-merge-escalation` streak-6), `memory/cron-state.json` (all 44 skills `last_status: success`, 0 cf≥2), `memory/logs/2026-08-14.md` (partial-view, notegraph/suggest-edges/planner/memory-flush/eda/heartbeat/status entries) + `memory/logs/2026-08-15.md` (today's notegraph + suggest-edges entries), `memory/issues/INDEX.md` (17 open, 2 resolved), `gh pr list --state open` (24 open, up +1 from 23 yesterday — #32 notegraph `+1 notes wired in` opened 2026-08-15T05:25:20Z), `gh pr list --state merged --limit 10` (last aeon merge #8 dependabot on 2026-08-07T01:36:39Z, ~200h+ ago), `gh issue list --state open` (0). `soul/` absent → clear-direct first-person tone.
