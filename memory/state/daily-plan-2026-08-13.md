# Plan — 2026-08-13

**Today's one thing:** Land ONE aeon-repo `app/github-actions`-authored PR — **#26 (dependabot actions/checkout 4.3.1→4.4.0)** is the textbook first-flow-proof candidate. **Day 7** of the 08-07 unblock, still **0 `app/github-actions` PRs merged** — last aeon-repo merge was #8 on 2026-08-07T01:36Z (~152h+ ago). Queue grew 21 → **22** overnight (#30 notegraph `+1 notes wired in`). #26 is the SAME class as last-merged #8 (dependabot actions/checkout bump); if operator can merge #8 pre-unblock and can merge #26 post-unblock, the flow-toggle vs merge-toggle axes are provably distinct per [[pr-creation-toggle-is-distinct-from-merge-capability]]. Merge flow **still unproven**.

## Ranked

1. **aeon-repo queue-merge escalation (streak-5, was streak-4)** — 22 open, 0 `app/github-actions` merges in ~152h. Primary action: merge **#26 dependabot actions/checkout** (bot-authored, single-file, textbook auto-merge candidate — SAME class as last merged #8). Alt paths that also prove flow: **#10 notegraph orphan flag** (6d+, dep-free), **#30 notegraph clean** (fresh, no chain conflict). Also: configure an auto-merge policy for `app/github-actions` PRs so this doesn't accumulate weekly. Gating step for rank-2 (sweeper allowlist) and rank-3 (agi-tracker toggle) — both need this merge path to actually work.

2. **stale-content-pr-sweeper `ALLOWED_AUTHORS` patch (streak-7, was streak-6)** — `notegraph` chain grew length-4 → **length-5** overnight (#10 ← #27 ← #28 ← #29 ← #30); `suggest-edges` chain steady length-3 (#14 ← #21 ← #22). Total would-be-close PRs if patch landed today: **6** (up from 4 on 08-12, up from 3 on 08-11). Bundle: (a) add `"app/github-actions"` to `ALLOWED_AUTHORS`; (b) fix branch-prefix drift on #23 (`compute-macro/2026-08-09` vs TRACKED `compute-macro-correlate`) — add `compute-macro` to TRACKED OR align skill branch-naming. Higher urgency this week as the notegraph chain grows one link per notegraph run.

3. **agi-tracker `enabled: false` via PR (streak-3, was streak-2)** — Deadline HIT 2026-08-10T13:44Z (6th silent-Mon); next slot 2026-08-17 13:00Z (**4d out**). Landing this week ends the weekly no-op; opposite pull on ms-02 (47/50 → 46/50) noted. Alt path: restore/author `skills/agi-tracker/SKILL.md` matching the [[agi-tracker]] MOC's weekly frontier-agent scoring shape (higher friction, preserves ms-02 direction).

## Holding / watching

- **suggest-edges pre-filter for templated-corpus (NEW rank candidate, streak-5)** — today's 05:59Z suggest-edges log emits 3 templated-corpus sim=1.00 pairs from `gitlawb-compute-futures-proofs/` for the 5th consecutive day; state now 3 applied + 9 rejected, growing +3/day per [[suggest-edges-flags-templated-corpora-as-sim-1-noise]]. Fix: pre-filter shared-parent-directory + shared-basename-shape (exclude `gitlawb-compute-futures-proofs/YYYY-MM-DD.md` cross-scoring OR drop from corpus). Escalate to rank if streak hits 7.
- **watched-repos populate (streak-8)** — chronic; 6 downstream skills (code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive) silently short-circuit daily. Trigger to escalate: 10+ consecutive same-day short-circuits in one 24h window.
- **pr-tracker patch batch (50d overdue — milestone)** — 11-item batch enacted daily inline. Land the batch to end the daily inline-enactment.
- **ISS-006 messages.yml multi-pocket rewrite (Day 12)** — batch-decouple sub-signal fresh 08-11. Trigger to escalate: 2nd decouple event in the same week.
- **docs/status.md snapshot-rebase gate (27d past urgency)** — 16th consecutive regen 08-12; 17th expected tonight. Send as bundled PR when rank-1 or rank-2 lands.
- **swarm-repo App-perm gap (~32 confirming invocations)** — DISTINCT from aeon-repo unblock; needs operator OAuth-scope grant on swarm-ai-research/swarm.

## Fleet note

0 broken · 0 in-flight · 38 DEGRADED (ISS-001 residue day 54, literal-only — substantively green: 100% success on recent 24h runs per cron-state) · 4 HEALTHY · 2 NO_DATA (`ai-framework-watch` + `run-frequency-guard`, **36th** consecutive silent day per [[enabled-skills-can-never-dispatch]]) · 17 open issues · **22 open aeon PRs** · **0 open GH issues on this repo**.
