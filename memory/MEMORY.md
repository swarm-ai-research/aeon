# Memory Index

Pointer-only index. Durable claims live in `memory/notes/`, organized by topic MOCs in `memory/topics/`. Daily activity in `memory/logs/`. Structured issues in `memory/issues/`.

## Current focus
- ⚠ [[issues/ISS-006]] day 10 — morning pocket **relapsed** after yesterday's recovery (planner, compute-futures-eda, memory-flush, memory-structural-dedupe all missing 06:00–07:30 UTC today). Second relapse-after-recovery in 3 days (day-7 rec → day-8 lapse → day-9 rec → day-10 lapse), confirming [[iss-006-pocket-recovery-is-noise]] — single clean days are delivery-rate noise. Close clock resets: 0 consecutive clean days. Root cause unchanged ([[gha-messages-yml-cron-underdelivery]]); mitigation still per-slot crons in `messages.yml`.
- [[issues/ISS-001]] OAuth outage (2026-06-06 → 2026-06-20T06:05Z) — recovery batch holding, all 38 tracked skills at `last_status: success`. Cumulative `success_rate` < 0.6 takes weeks to clear by design; close decision still deferred until ISS-006 stabilizes.
- [[issues/ISS-005]] reframed — swarm-safety-eval is running successfully (last_success 2026-06-28T08:15:47Z); its SSE_EMPTY path writes to the daily log not an article. Reclassify root cause as `permanent-limitation` per [[swarm-safety-eval-empty-writes-log-not-article]].
- Pending operator action: open today's `agi-tracker/2026-06-29` (METR refit + 3 new points) and `notegraph/2026-06-29` (+3n/+46e) branches via PAT, plus carry-over `fix/workflow-security-audit-2026-06-21` (old RCE patch), `fix/workflow-security-audit-2026-06-28` (16C/36H), `skill-graph/2026-06-28` (INIT 173 skills). All five blocked by repo policy "GitHub Actions is not permitted to create or approve pull requests" — same App perm gap.
- AGI Tracker live since 2026-06-10. Mon 2026-06-29 13:00 UTC slot **fired** — closed the 19-day data gap (06-15 + 06-22 misses). Added GPT-5.2, Gemini 3.1 Pro, Claude Mythos Preview; METR central fit refit to ~3.5 mo per [[metr-doubling-3-5mo]]. See [[agi-tracker]].
- pr-tracker inline email-OR filter caught `Panniantong/Agent-Reach#436` today — first non-empty post-filter day in 10 runs, validating [[pr-tracker-branch-prefix-misses-bot-identity]]; durable SKILL.md patch (AND→OR or drop prefix) still pending.

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
- ISS-006 fix: replace `messages.yml` `*/5 * * * *` with explicit per-slot crons covering **every** timeslot in `aeon.yml`. Today's three pocket recoveries are noise per [[iss-006-pocket-recovery-is-noise]] — do NOT defer the fix on the basis of one clean day. See [[gha-messages-yml-cron-underdelivery]].
- ISS-006 cross-check: compare a gitlawb fork's `messages.yml` `*/5` delivery rate vs this repo's — distinguishes per-repo quota throttle from platform-wide GHA cron behavior.
- ISS-006 follow-up: manual `workflow_dispatch` of a 09:00-slot skill (e.g. `fleet-control`) to confirm the dispatch path still works while the 09:00 pocket is broken.
- Reclassify ISS-005 from `missing-secret-or-cron` to `permanent-limitation` and either add a log-based eval assertion or document NO_OUTPUT as expected when ledger is absent. See [[swarm-safety-eval-empty-writes-log-not-article]].
- Patch `pr-tracker` SKILL.md: drop `headRefName` / `mergedAt` / `--state merged` per [[gh-search-prs-api-drift]], AND replace `ai/`-only branch filter with commit-author email filter (`BOT_EMAIL=aeonframework@users.noreply.github.com`) per [[pr-tracker-branch-prefix-misses-bot-identity]]. Today's run proved the OR filter works inline (caught `Panniantong/Agent-Reach#436` — first non-empty post-filter day in 10).
- Widen `scenario-sweep.mjs` seed count or switch outlier detection to a tie-robust statistic (MAD-based) per [[compute-futures-12-seed-sample-too-small]]. Also resolve the seed-encoding artifact (3 of 12 seeds 10-digit) per [[compute-futures-seed-padding-bug]].
- File `./generate-skills-json` bugs as structured issues (see [[generate-skills-json-newline-bug]], [[skills-json-count-drift]]).
- Open the staged workflow-audit PRs via PAT — both `fix/workflow-security-audit-2026-06-21` (old) AND `fix/workflow-security-audit-2026-06-28` (new today, 16C/36H) — plus `skill-graph/2026-06-28` (INIT). All three blocked by repo policy "GitHub Actions is not permitted to create or approve pull requests" — same App perm gap.
- Open the queued branches via PAT: today's `agi-tracker/2026-06-29` + `notegraph/2026-06-29`, plus carry-over `fix/workflow-security-audit-2026-06-28` (16C/36H), `skill-graph/2026-06-28` (INIT), `fix/workflow-security-audit-2026-06-21` (old RCE). All five blocked by repo policy "GitHub Actions is not permitted to create or approve pull requests".
- Defer ISS-001 close until ISS-006 is resolved.

## Completed Goals
- File a structured issue for `agi-tracker`'s 2nd consecutive Mon miss (2026-06-15, 2026-06-22) if Mon 2026-06-29 also misses. — completed 2026-06-29 (Mon 13:00 UTC slot fired; conditional trigger no longer met)
