# Plan — 2026-08-19

**Today's one thing:** Merge one low-risk aeon-repo PR — **#26 (dependabot actions/checkout 4.3.1→4.4.0, same class as last-merged #8)** or **#36 (notegraph fresh head-of-chain, dep-free vs main)** — to prove the end-to-end app/github-actions merge flow on Day-13 of the streak. 22 open aeon PRs, ~292h since last aeon merge (#8 on 2026-08-07T01:36Z).

## Ranked

1. **Merge one low-risk aeon-repo PR to prove end-to-end flow (streak-11).** Escalated framing since 08-10: creation works, merge does not, queue grows daily. Today's queue is 22 (+#38 suggest-edges opened 05:56Z; up 1 net vs 08-18). Concrete candidates: **#26 dependabot** (textbook auto-merge, exact class as the only 2026 aeon-repo merge #8) or **#36 notegraph** (dep-free, against `main`, first PR of the post-06-25-baseline era). Bundle step-2: configure auto-merge policy for `app/github-actions` PRs so this doesn't accumulate weekly. See [[pr-creation-toggle-is-distinct-from-merge-capability]].
2. **Ship `enabled: false` on `aeon.yml:188` for `agi-tracker` via PR (streak-4).** 7th silent-Mon fire fired 2026-08-17T13:25Z; **8th fires 2026-08-24T13:00Z (~5d out)**. Alt-path (a) restore `skills/agi-tracker/SKILL.md` matching [[agi-tracker]] MOC (higher-value, higher-friction); (b) `enabled: false` (lower-friction, pulls ms-02 47/50 → 46/50). See [[agi-tracker-missing-skill-md-dispatches-no-op]]. Natural rank-1-of-tomorrow candidate if queue-merge lands.
3. **Patch `stale-content-pr-sweeper` `ALLOWED_AUTHORS` + TRACKED prefixes (streak-13).** Live 08-18 sweeper confirmed 5 tracked-prefix PRs matched, 0 groups reached supersession — all `app/github-actions`, all rejected. **Under patched allowlist: 2 closes today** (#32 → #36, #22 → #37; #35 skipped by 2d min-age gate). Bundle TRACKED-prefix drift fix (streak-7 per [[stale-content-pr-sweeper-tracked-prefix-drift]]) — `compute-macro` vs `compute-macro-correlate` naming mismatch. One PR patches both.

## Holding / watching

- **watched-repos populate-or-disable (streak-14).** Chronic. Reconcile path mismatch (`memory/topics/watched-repos.md` vs `memory/watched-repos.md`) in fix. Trigger: any operator-visible downstream false-positive.
- **suggest-edges pre-filter (streak-11).** Day-11 recurrence; PR #38 opened 05:56Z. Trigger: 3rd consecutive same-signature PR this week.
- **ISS-006 messages.yml multi-pocket rewrite (streak-17).** Trigger: morning-batch miss inside 26h scan.
- **docs/status.md snapshot-rebase gate (streak-33).** 21st rebase-clobber-regen 08-18. Trigger: status-page regression that survives past next heartbeat.
- **pr-tracker patch bundle a–k (streak-56).** Today's predictor `(0, 8, 0, 1)` letter / `(0, 9, 0, 0)` substantive (Baileys#2732 stale-bot window expires 02:17Z). Trigger: 3rd consecutive byte-identical notify.
- **swarm App write-perm gap (streak-38).** Combined 89 invocations vs frozen queue 08-18, zero writes attempted. Trigger: human PR churn on that queue.

## Fleet note

**0 broken · 0 in-flight failure · 1 dispatched (`notegraph` running its 05:00Z slot — normal) · 38 DEGRADED (ISS-001 Day-61 residue, all `last_status: success`) · 4 truly healthy (`agi-tracker`, `config-validator`, `swarm-safety-eval`, `weekly-shiplog`) · 2 NO_DATA (`ai-framework-watch` + `run-frequency-guard`, 43rd silent day) · 18 open issues · 22 open aeon PRs · 0 open GH issues.**

## Source footer

- Read: `memory/MEMORY.md`, `memory/state/planner-state.json` (last run 2026-08-18T06:30Z, `top_priority: aeon-repo-queue-merge-escalation` streak-10), `memory/cron-state.json` (42 skills, 41 success, 1 dispatched notegraph, agi-tracker HEALTHY-but-empty), last 2 days of `memory/logs/`, `memory/issues/INDEX.md` (18 open — MEMORY.md caption of 17 is 1d stale), `gh pr list --state open` (22 rows), `gh pr view 26` + `gh pr view 36` (both OPEN, `mergeable: UNKNOWN`), `gh issue list --state open` (0), `git log --oneline main --since=2026-08-18` (empty).
- Sandbox note: all `gh` calls succeeded via internal auth; `soul/` absent → clear-direct first-person tone; `${var}` empty → plan-only, no dispatch.
