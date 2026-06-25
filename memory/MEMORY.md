# Memory Index

Pointer-only index. Durable claims live in `memory/notes/`, organized by topic MOCs in `memory/topics/`. Daily activity in `memory/logs/`. Structured issues in `memory/issues/`.

## Current focus
- ⚠ [[issues/ISS-006]] day 5 — root cause is now concrete: `messages.yml` `*/5` is silently dropped ~97% (`gh run list --workflow=messages.yml --created=2026-06-22..25` → 31/~1150 runs), with a daily 3–6h dead zone bracketing 06:00–06:30 UTC. Matcher-bug hypothesis ruled out. See [[gha-messages-yml-cron-underdelivery]]; supersedes [[narrow-cron-pocket-vs-window-drop]].
- [[issues/ISS-001]] OAuth outage (2026-06-06 → 2026-06-20T06:05Z) — recovery batch holding, all 38 tracked skills at `last_status: success`. Cumulative `success_rate` < 0.6 takes weeks to clear by design; close decision still deferred until ISS-006 stabilizes.
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
- ISS-006 fix: replace `messages.yml` `*/5 * * * *` with explicit per-slot crons matching `aeon.yml` timeslots, and add a `messages-morning.yml` (`*/5 6 * * *`) for redundant 06:00–06:30 coverage. See [[gha-messages-yml-cron-underdelivery]].
- ISS-006 cross-check: compare a gitlawb fork's `messages.yml` `*/5` delivery rate vs this repo's — distinguishes per-repo quota throttle from platform-wide GHA cron behavior.
- ISS-006 follow-up: manual `workflow_dispatch` of `planner` and `memory-flush` to confirm the dispatch path still works (rule out per-skill SKILL.md drift while messages.yml is broken).
- File `./generate-skills-json` bugs as structured issues (see [[generate-skills-json-newline-bug]], [[skills-json-count-drift]]).
- Patch `pr-tracker` SKILL.md fallback per [[gh-search-prs-api-drift]] (`--merged` flag, drop `headRefName` and `mergedAt`).
- Open the staged workflow-audit PR from `fix/workflow-security-audit-2026-06-21` via PAT (App perm gap). _[BLOCKED 2026-06-21: needs `GH_GLOBAL` PAT — Aeon App cannot self-grant workflows write]_
- File a structured issue for `agi-tracker`'s 2nd consecutive Mon miss (2026-06-15, 2026-06-22) if Mon 2026-06-29 also misses.
- Defer ISS-001 close until ISS-006 is resolved.
