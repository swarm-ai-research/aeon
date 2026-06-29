# Memory Index

Pointer-only index. Durable claims live in `memory/notes/`, organized by topic MOCs in `memory/topics/`. Daily activity in `memory/logs/`. Structured issues in `memory/issues/`.

## Current focus
- ⚠ [[issues/ISS-006]] day 8 — morning 06:00–06:30 pocket **relapsed** after one-day day-7 recovery (6/8 expected skills missed today, OUTAGE); 07:00–07:30 Sunday slots fired late (~74m/44m past schedule); 09:00 dead zone now 6 days silent; NEW 05:00 pocket silent (notegraph + suggest-edges ~50h stale, first multi-day 05:00 silence). Multi-pocket sliding model now spans 05:00, 06:00–06:30, 09:00, 23:45. Root cause unchanged ([[gha-messages-yml-cron-underdelivery]]); mitigation still per-slot crons. Treat recoveries as noise per [[iss-006-pocket-recovery-is-noise]].
- [[issues/ISS-001]] OAuth outage (2026-06-06 → 2026-06-20T06:05Z) — recovery batch holding, all 38 tracked skills at `last_status: success`. Cumulative `success_rate` < 0.6 takes weeks to clear by design; close decision still deferred until ISS-006 stabilizes.
- [[issues/ISS-005]] reframed — swarm-safety-eval is running successfully (last_success 2026-06-28T08:15:47Z); its SSE_EMPTY path writes to the daily log not an article. Reclassify root cause as `permanent-limitation` per [[swarm-safety-eval-empty-writes-log-not-article]].
- Pending operator action: open the workflow-security-audit branches via PAT — `fix/workflow-security-audit-2026-06-21` (old RCE patch) AND `fix/workflow-security-audit-2026-06-28` (new today, 16 critical + 36 high). Both blocked by repo policy "GitHub Actions is not permitted to create or approve pull requests" — same App perm gap. Also `skill-graph/2026-06-28` (INIT 173 skills mapped) blocked by the same policy.
- AGI Tracker live since 2026-06-10 — weekly skill maintains `docs/agi-tracker/data.js`. See [[agi-tracker]]. Still no `cron-state` row after 2026-06-15 and 2026-06-22 Mon slots; next chance Mon 2026-06-29 13:00 UTC.
- pr-tracker filter gap: `Panniantong/Agent-Reach#436` (security/-branch, aeonframework author) is now 2 days open with 0 reviews/comments, still dropped by the `ai/`-prefix filter — switch to commit-author email filter. See [[pr-tracker-branch-prefix-misses-bot-identity]].

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
- ISS-006 fix: replace `messages.yml` `*/5 * * * *` with explicit per-slot crons covering **every** timeslot in `aeon.yml` — multi-pocket evidence (05:00, 06:00–06:30, 09:00, 23:45) rules out a morning-only fix. Keep the `messages-morning.yml` (`*/5 6 * * *`) redundancy for the worst-hit window. See [[gha-messages-yml-cron-underdelivery]].
- ISS-006 cross-check: compare a gitlawb fork's `messages.yml` `*/5` delivery rate vs this repo's — distinguishes per-repo quota throttle from platform-wide GHA cron behavior.
- ISS-006 follow-up: manual `workflow_dispatch` of a 09:00-slot skill (e.g. `fleet-control`) to confirm the dispatch path still works while the 09:00 pocket is broken.
- Reclassify ISS-005 from `missing-secret-or-cron` to `permanent-limitation` and either add a log-based eval assertion or document NO_OUTPUT as expected when ledger is absent. See [[swarm-safety-eval-empty-writes-log-not-article]].
- Patch `pr-tracker` SKILL.md: drop `headRefName` / `mergedAt` / `--state merged` per [[gh-search-prs-api-drift]], AND replace `ai/`-only branch filter with commit-author email filter (`BOT_EMAIL=aeonframework@users.noreply.github.com`) per [[pr-tracker-branch-prefix-misses-bot-identity]].
- File `./generate-skills-json` bugs as structured issues (see [[generate-skills-json-newline-bug]], [[skills-json-count-drift]]).
- Open the staged workflow-audit PRs via PAT — both `fix/workflow-security-audit-2026-06-21` (old) AND `fix/workflow-security-audit-2026-06-28` (new today, 16C/36H) — plus `skill-graph/2026-06-28` (INIT). All three blocked by repo policy "GitHub Actions is not permitted to create or approve pull requests" — same App perm gap.
- Defer ISS-001 close until ISS-006 is resolved.

## Completed Goals
- File a structured issue for `agi-tracker`'s 2nd consecutive Mon miss (2026-06-15, 2026-06-22) if Mon 2026-06-29 also misses. — completed 2026-06-29 (Mon 13:00 UTC slot fired; conditional trigger no longer met)
