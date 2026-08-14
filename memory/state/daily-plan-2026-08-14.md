# Plan — 2026-08-14

**Today's one thing:** Land ONE `app/github-actions`-authored PR — **#26 (dependabot actions/checkout 4.3.1→4.4.0)** is still the textbook first-flow-proof candidate. **Day 8** of the 08-07 PR-creation unblock, still **0 `app/github-actions` PRs merged** — last aeon-repo merge is #8 on 2026-08-07T01:36Z (~176h+ ago). Queue grew 22 → **23** overnight (#31 notegraph `+2 notes wired in` opened 2026-08-14T05:59Z). #26 is the SAME class as last-merged #8 (dependabot actions/checkout bump); merging it separates the flow-toggle from the merge-toggle per [[pr-creation-toggle-is-distinct-from-merge-capability]]. Merge flow **still unproven** at day 8.

## Ranked

1. **aeon-repo queue-merge escalation (streak-6, was streak-5)** — 23 open, 0 `app/github-actions` merges in ~176h. Primary action: merge **#26 dependabot actions/checkout** (bot-authored, single-file, textbook auto-merge candidate — SAME class as last merged #8). Alt paths that also prove flow: **#10 notegraph orphan flag** (7d, dep-free), **#31 notegraph clean** (fresh, no chain conflict). Also: configure an auto-merge policy for `app/github-actions` PRs so this doesn't accumulate weekly. Gating step for rank-2 (sweeper allowlist) and rank-3 (agi-tracker toggle) — both need this merge path to actually work.

2. **stale-content-pr-sweeper `ALLOWED_AUTHORS` patch (streak-8, was streak-7)** — `notegraph` chain grew length-5 → **length-6** overnight (#10 ← #27 ← #28 ← #29 ← #30 ← #31); `suggest-edges` chain steady length-3 (#14 ← #21 ← #22). Total would-be-close PRs if patch landed today: **8** (up from 6 on 08-13, up from 4 on 08-12, up from 3 on 08-11). Bundle: (a) add `"app/github-actions"` to `ALLOWED_AUTHORS`; (b) fix TRACKED-prefix drift on #23 (`compute-macro/2026-08-09` vs TRACKED `compute-macro-correlate`). Urgency compounds one link per notegraph run — the chain now buries the orphan-flag #10 six deep.

3. **suggest-edges pre-filter for templated-corpus (streak-6, PROMOTED from hold)** — today's 05:56Z suggest-edges log emits 3 templated pairs from `gitlawb-compute-futures-proofs/` for the 6th consecutive day; rejected-list at **12** growing +3/day exactly on prediction per [[suggest-edges-flags-templated-corpora-as-sim-1-noise]]. Six-day streak with an exact +3/day rejection cadence and a corpus that grew a new file (2026-08-12.md, will surface in a future top-3) qualifies for rank per prior-plan's "escalate if streak hits 7" — pulling forward one day since the class is now demonstrably systematic. Fix: pre-filter shared-parent-directory + shared-basename-shape (exclude `gitlawb-compute-futures-proofs/YYYY-MM-DD.md` cross-scoring) OR drop that tree from the corpus feed.

## Holding / watching

- **agi-tracker `enabled: false` via PR (streak-4, was streak-3)** — Next silent-Mon slot 2026-08-17 13:00Z (**3d out**). Falls off holding into rank on Sunday 08-16 (day-before-deadline).
- **watched-repos populate (streak-9)** — chronic; 6 downstream skills (code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive) silently short-circuit daily. Trigger to escalate: 10+ consecutive same-day short-circuits in one 24h window.
- **pr-tracker patch batch (51d overdue — milestone)** — 11-item batch enacted daily inline. Land the batch to end the daily inline-enactment. Item (j) — stale-bot body-fingerprint filter — is now the highest-ROI single line (n=2 recurrence with distinct bot handles confirmed 08-13).
- **ISS-006 messages.yml multi-pocket rewrite (Day 13)** — no fresh decouple signal today (batch recoupled 08-13). Trigger to escalate: 2nd decouple event in the same week.
- **docs/status.md snapshot-rebase gate (28d past urgency)** — 16th consecutive regen expected tonight. Send as bundled PR when rank-1 or rank-2 lands.
- **swarm-repo App-perm gap (~33 confirming invocations)** — DISTINCT from aeon-repo unblock; needs operator OAuth-scope grant on swarm-ai-research/swarm.

## Fleet note

0 broken · 0 in-flight · 39 DEGRADED (ISS-001 residue day 56, literal-only — substantively green: 100% success on recent 24h runs per cron-state) · 4 HEALTHY · 2 NO_DATA (`ai-framework-watch` + `run-frequency-guard`, **38th** consecutive silent day per [[enabled-skills-can-never-dispatch]]) · 17 open issues · **23 open aeon PRs** · **0 open GH issues on this repo**.
