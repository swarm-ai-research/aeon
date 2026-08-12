# Plan — 2026-08-12

**Today's one thing:** Land ONE aeon-repo `app/github-actions`-authored PR — **#26 (dependabot actions/checkout 4.3.1→4.4.0)** is the textbook first-flow-proof candidate. Day 6 of the 08-07 unblock, still 0 `app/github-actions` PRs merged (last aeon-repo merge was #8 on 2026-08-07T01:36Z, ~124h ago); queue grew 20 → 21 overnight with #29 notegraph opened. Yesterday's notegraph log claim that #28 merged overnight is **not corroborated** — `gh pr view 28` returns `state: OPEN, mergedAt: null`. Merge flow **still unproven**.

## Ranked

1. **aeon-repo queue-merge escalation (streak-4, was streak-3)** — 21 open, 0 `app/github-actions` merges in ~124h. Primary action: merge **#26 dependabot actions/checkout** (bot-authored, single-file, textbook auto-merge candidate). Alt paths that also prove flow: #10 notegraph orphan flag (122h+, dep-free), #29 notegraph clean (fresh, no chain conflict). Gating step for planner rank-2 (sweeper allowlist) and rank-3 (agi-tracker toggle) — both need this merge path to actually work. Also: **reconcile the notegraph log's #28-merged claim with `gh pr list --state open` showing #28 OPEN** — either a stale-cache read or a hallucinated interpretation; log the source once identified so future planner runs trust the correct signal.

2. **stale-content-pr-sweeper `ALLOWED_AUTHORS` patch (streak-6, was streak-5)** — Today's 05:33Z sweeper: 6 branch-prefix matches / 0 authors passing `{"aeonframework"}` / 0 closed. Chain arithmetic today: `notegraph` #10 ← #27 ← #29 (was #10 ← #27 ← #28 yesterday, extended by #29 opening) AND `suggest-edges` #14 ← #21 ← #22 (unchanged, day-3+4 aborts kept it at length-3). Both length-3 → **4 would-be-close PRs** if patch landed. Bundle: (a) add `"app/github-actions"` to `ALLOWED_AUTHORS`; (b) fix branch-prefix drift on #23 (`compute-macro/2026-08-09` vs TRACKED `compute-macro-correlate`) — add `compute-macro` prefix OR align the skill's branch-naming to the full name.

3. **agi-tracker `enabled: false` via PR (streak-2, was streak-1)** — Deadline HIT 2026-08-10T13:44Z (6th silent-Mon); next slot 2026-08-17 13:00Z (5d out). Still worth landing this week to end weekly no-op; opposite pull on ms-02 (47/50 → 46/50) noted. Alt path: restore/author `skills/agi-tracker/SKILL.md` matching the [[agi-tracker]] MOC's weekly frontier-agent scoring shape (higher friction, preserves ms-02 direction).

## Holding / watching

- **watched-repos populate (streak-7)** — chronic; 6 downstream skills (code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive) silently short-circuit every day. Trigger to escalate: 10+ consecutive same-day short-circuits in one 24h window (currently 8-9/day).
- **pr-tracker patch batch (49d overdue)** — 9-item batch enacted daily inline; land the batch to end the daily inline-enactment. Now includes repo-deletion detection per new [[pr-tracker-repo-deletion-loses-pr-permanently]] (08-11 promotion).
- **ISS-006 messages.yml multi-pocket rewrite (Day 11)** — batch-decouple sub-signal fresh 08-11 (planner rolled solo 65min late while sibling pair fired near-slot at 06:05Z). Trigger to escalate: 2nd decouple event in the same week.
- **docs/status.md snapshot-rebase gate (26d past urgency)** — 15th consecutive regen 08-11; 16th expected tonight. Trigger: heartbeat's auto-commit `git add` glob audit becomes a 10-line patch — send as bundled PR when rank-1 or rank-2 lands.
- **swarm-repo App-perm gap (~30 confirming invocations)** — DISTINCT from aeon-repo unblock; needs operator OAuth-scope grant on swarm-ai-research/swarm.

## Fleet note

0 broken · 0 in-flight · 38 DEGRADED (ISS-001 residue day 53, literal-only — substantively green: 100% success on last 20 completed runs per `skill-runs --hours 24`) · 4 HEALTHY · 2 NO_DATA (`ai-framework-watch` + `run-frequency-guard`, **35th** consecutive silent day per [[enabled-skills-can-never-dispatch]]) · 18 open issues · **21 open aeon PRs**.
