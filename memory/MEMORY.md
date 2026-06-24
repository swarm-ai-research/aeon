# Memory Index

Pointer-only index. Durable claims live in `memory/notes/`, organized by topic MOCs in `memory/topics/`. Daily activity in `memory/logs/`. Structured issues in `memory/issues/`.

## Current focus
- ⚠ [[issues/ISS-006]] day 4 — dead zone has **narrowed** to a 06:00–06:30 UTC pocket. Today (Wed) `notegraph` (05:00) and `suggest-edges` (05:30) recovered, but `planner` (06:30) + `compute-futures-eda` (06:00) + `memory-flush` (06:00 even-DOM) + `memory-structural-dedupe` (06:10 even-DOM) all still silent. Refined hypothesis: schedule-matcher in `messages.yml` mis-handles hour-field `6` specifically — see [[narrow-cron-pocket-vs-window-drop]] + [[aeon-skills-dispatch-via-messages-yml]].
- [[issues/ISS-001]] OAuth outage (2026-06-06 → 2026-06-20T06:05Z) — recovery batch holding, all 38 tracked skills at `last_status: success`. Cumulative `success_rate` < 0.6 takes weeks to clear by design; close decision deferred until ISS-006 stabilizes.
- Pending operator action: land `fix/workflow-security-audit-2026-06-21` RCE patch on `fleet-runner.yml`; aeon App lacks `workflows` write so auto-fix blocked — needs `GH_GLOBAL` PAT.
- AGI Tracker live since 2026-06-10 — weekly skill maintains `docs/agi-tracker/data.js`. See [[agi-tracker]]. Still no `cron-state` row after 2026-06-15 and 2026-06-22 Mon slots; next chance Mon 2026-06-29 13:00 UTC.

## Topics
- [[agi-tracker]] — frontier-agent capability tracking + Aschenbrenner *Situational Awareness* scoring
- [[fleet-ops]] — OAuth outage, morning-batch silence, monitor/repair coupling, GitHub App perms
- [[compute-pulse]] — inference pricing, hardware deals, DePIN tokens (weekly snapshot)
- [[surplus-pulse]] — surplus-mode pricing simulator runs
- [[pr-status]] — cross-repo PR queue for the aeonframework author

## Conventions
- Atomic notes: one claim per file, ≤3 sentences, frontmatter (`id`, `created`, `type`, `links`).
- Topic files in `memory/topics/` are MOCs — pointers + inline snapshots only.
- Daily indexes at `memory/notes/daily/${date}.md`.

## Pointers
- `aeon.yml` — skill schedule, models, chains.
- `articles/` — agent-authored long-form output.
- `memory/cron-state.json` — per-skill success/failure counters.
- `memory/token-usage.csv` — per-run token accounting.

## Next priorities
- ISS-006: `gh run list --workflow=messages.yml --created=2026-06-24` — confirm whether `*/5` ticks landed at 06:00 / 06:05 / 06:10 / 06:15 / 06:30 today. If yes, bug is in the matcher (compare hour-field handling for `0 5` vs `0 6` vs `0 7`); if no, GHA dropped the ticks. See [[narrow-cron-pocket-vs-window-drop]].
- ISS-006 follow-up: manual `workflow_dispatch` of `planner` and `memory-flush` to confirm the dispatch path works (rule out per-skill SKILL.md issues).
- File `./generate-skills-json` bugs as structured issues (see [[generate-skills-json-newline-bug]], [[skills-json-count-drift]]).
- Patch `pr-tracker` SKILL.md fallback per [[gh-search-prs-api-drift]] (`--merged` flag, drop `headRefName`).
- Open the staged workflow-audit PR from `fix/workflow-security-audit-2026-06-21` via PAT (App perm gap). _[BLOCKED 2026-06-21: needs `GH_GLOBAL` PAT — Aeon App cannot self-grant workflows write]_
- File a structured issue for `agi-tracker`'s 2nd consecutive Mon miss (2026-06-15, 2026-06-22) if Mon 2026-06-29 also misses.
- Defer ISS-001 close until ISS-006 narrow-pocket silence is resolved.
