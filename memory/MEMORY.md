# Memory Index

Pointer-only index. Durable claims live in `memory/notes/`, organized by topic MOCs in `memory/topics/`. Daily activity in `memory/logs/`. Structured issues in `memory/issues/`.

## Current focus
- ⚠ [[issues/ISS-006]] day 7 — multi-pocket cron-underdelivery pattern confirmed: morning 06:00–06:30 pocket **recovered today** (planner + compute-futures-eda fired ~07:34Z, 7-day silence broken); 23:45 sweeper pocket **also self-resolved** (last_success 06-27T00:19Z); but NEW 09:00 UTC dead zone surfaced — fleet-control, github-monitor, issue-triage, pr-triage, pr-review-09:00-slot all silent 5 days since 06-22T10:14Z, while pr-review's 18:00 sister slot fires fine. Root cause unchanged ([[gha-messages-yml-cron-underdelivery]]); mitigation still per-slot crons covering every `aeon.yml` timeslot.
- [[issues/ISS-001]] OAuth outage (2026-06-06 → 2026-06-20T06:05Z) — recovery batch holding, all 38 tracked skills at `last_status: success`. Cumulative `success_rate` < 0.6 takes weeks to clear by design; close decision still deferred until ISS-006 stabilizes.
- Pending operator action: land `fix/workflow-security-audit-2026-06-21` RCE patch on `fleet-runner.yml`; aeon App lacks `workflows` write so auto-fix blocked — needs `GH_GLOBAL` PAT.
- AGI Tracker live since 2026-06-10 — weekly skill maintains `docs/agi-tracker/data.js`. See [[agi-tracker]]. Still no `cron-state` row after 2026-06-15 and 2026-06-22 Mon slots; next chance Mon 2026-06-29 13:00 UTC.
- pr-tracker filter gap: today's `Panniantong/Agent-Reach#436` (security/-branch, aeonframework author) was dropped by the `ai/`-prefix filter — switch to commit-author email filter. See [[pr-tracker-branch-prefix-misses-bot-identity]].

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
- ISS-006 fix: replace `messages.yml` `*/5 * * * *` with explicit per-slot crons covering **every** timeslot in `aeon.yml` — multi-pocket evidence (morning 06:00–06:30, nightly 23:45, daily 09:00) rules out a morning-only fix. Keep the `messages-morning.yml` (`*/5 6 * * *`) redundancy for the worst-hit window. See [[gha-messages-yml-cron-underdelivery]].
- ISS-006 cross-check: compare a gitlawb fork's `messages.yml` `*/5` delivery rate vs this repo's — distinguishes per-repo quota throttle from platform-wide GHA cron behavior.
- ISS-006 follow-up: manual `workflow_dispatch` of a 09:00-slot skill (e.g. `fleet-control`) to confirm the dispatch path still works while the 09:00 pocket is broken.
- Patch `pr-tracker` SKILL.md: drop `headRefName` / `mergedAt` / `--state merged` per [[gh-search-prs-api-drift]], AND replace `ai/`-only branch filter with commit-author email filter (`BOT_EMAIL=aeonframework@users.noreply.github.com`) per [[pr-tracker-branch-prefix-misses-bot-identity]].
- File `./generate-skills-json` bugs as structured issues (see [[generate-skills-json-newline-bug]], [[skills-json-count-drift]]).
- Open the staged workflow-audit PR from `fix/workflow-security-audit-2026-06-21` via PAT (App perm gap). _[BLOCKED 2026-06-21: needs `GH_GLOBAL` PAT — Aeon App cannot self-grant workflows write]_
- File a structured issue for `agi-tracker`'s 2nd consecutive Mon miss (2026-06-15, 2026-06-22) if Mon 2026-06-29 also misses.
- Defer ISS-001 close until ISS-006 is resolved.
