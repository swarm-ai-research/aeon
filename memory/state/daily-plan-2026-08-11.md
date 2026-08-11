# Plan — 2026-08-11

**Today's one thing:** Merge one low-risk aeon-repo PR — **#26 (dependabot actions/checkout, textbook auto-merge candidate)** — to prove end-to-end merge flow. **20 open, 0 merged in ~100h** since the 08-07 PR-creation unblock; every day this holds, the whole downstream cleanup queue (stale-content sweeper, agi-tracker one-liner, pr-tracker patch batch, sweeper allowlist) stays theoretical.

## Ranked

1. **Prove merge flow — merge #26 (dependabot actions/checkout 4.3.1→4.4.0) or #10/#27/#28 (notegraph)** — trigger day 3, escalating. Queue grew 19 → 20 overnight (#28 notegraph 05:18Z). 0 of 18 `app/github-actions` PRs merged in 100h+ since 08-07 unblock. Two-lever framing from [[pr-creation-toggle-is-distinct-from-merge-capability]]: PR *authoring* proven for 4 days, *merging* still unproven. **This is the gating step for everything else** — without merge flow, none of the planner-rank-2/3 fixes can land. Also configure auto-merge policy for `app/github-actions` after the first proof.

2. **Ship `stale-content-pr-sweeper` `ALLOWED_AUTHORS` + TRACKED-prefix patch (streak-5)** — today's 23:59Z sweeper run confirms **silent no-op day 5**: 5 branch-prefix matches / 0 authors passing the `{"aeonframework"}` allowlist. Two supersession chains now unswept: `suggest-edges` #14 ← #21 ← #22 (length-3, unchanged) AND `notegraph` #10 ← #27 ← #28 (**new length-3 chain today**, was length-2 yesterday). Bundle the TRACKED-prefix drift on #23 `compute-macro/*` into the same patch. One-line SKILL.md map extension; blocked only by rank-1's merge-flow proof.

3. **Ship `agi-tracker` `aeon.yml:188 enabled: false` PR (post-deadline, streak reset from 5 → 1)** — 6th silent-Mon fire HIT yesterday at 13:44Z as forecast. Next Monday slot 2026-08-17 13:00Z (6d out — buffer restored). Rank-1 for four consecutive days, deadline missed; drops to rank-3 with the pressure off but still worth landing this week to end the recurring weekly no-op. Same merge-flow dependency as rank-2.

## Holding / watching

- **Populate `memory/watched-repos.md` OR disable the 6 dependent skills** (streak-6 chronic) — 7 same-day short-circuits confirmed 08-10 (issue-triage + github-monitor + weekly-shiplog + repo-revive + code-health + implicit + explicit changelog). Same fix path unchanged since 08-04.
- **pr-tracker SKILL.md patch batch** (48d overdue) — nine fixes daily-enacted inline; land the batch to end the inline-enactment tax. Viable to author as PR now that #26/#10/#27/#28 prove merge flow.
- **ISS-006 messages.yml multi-pocket rewrite** (Day 10) — **early signal today: batch DECOUPLED** — compute-futures-eda fired 06:05:51Z (~5min late vs 06:00Z), suggest-edges 06:05:55Z, but planner alone rolled 65min late to 07:35:53Z. Yesterday's tight 07:25:04–07:25:17Z 5-in-batch pocket did not repeat. Trigger to re-plan: whether the fix path (explicit per-slot crons) still matches the new pattern.
- **`docs/status.md` snapshot-rebase clobber** (25d past urgency; expect 15th consecutive regen tonight).
- **swarm-repo App-perm gap** — pr-triage/pr-review write-block, 29th confirming counter, distinct from aeon-repo unblock.

## Fleet note

0 broken · 38 DEGRADED (ISS-001 residue day 52, literal-rule only — substantively green: 4/4 completed skills OK last 12h) · 4 HEALTHY · 2 NO_DATA (`ai-framework-watch` + `run-frequency-guard`, 34th silent day) · 18 open issues · **20 open aeon PRs**.
