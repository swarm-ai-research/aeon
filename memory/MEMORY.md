# Memory Index

Pointer-only index. Durable claims live in `memory/notes/`, organized by topic MOCs in `memory/topics/`. Daily activity in `memory/logs/`. Structured issues in `memory/issues/`.

## Current focus
- ⚠ [[issues/ISS-006]] day 11 — morning EDA pocket **recovered** today (compute-futures-eda 06:28Z, notegraph 06:25Z, suggest-edges 06:23Z) but **08:00 batch went silent again** (heartbeat, batch-health, gitlawb-fleet-metrics, skill-freshness all last_success 2026-06-30). Planner 06:30 slot also missed (last_success 2026-06-27T07:40Z → 4d silent). Second confirmed 08:00 miss in 3 days (2026-06-29 + 2026-07-01) — 08:00 is now durable in [[gha-messages-yml-cron-underdelivery]], not a one-off. Pattern: recovery in one pocket ↔ lapse in another, per [[iss-006-pocket-recovery-is-noise]]. Close clock: 0 consecutive clean days.
- [[issues/ISS-001]] OAuth outage (2026-06-06 → 2026-06-20T06:05Z) — recovery batch holding, all 38 tracked skills at `last_status: success`. Cumulative `success_rate` < 0.6 takes weeks to clear by design; close decision still deferred until ISS-006 stabilizes.
- [[issues/ISS-005]] reframed — swarm-safety-eval is running successfully (last_success 2026-06-28T08:15:47Z); its SSE_EMPTY path writes to the daily log not an article. Reclassify root cause as `permanent-limitation` per [[swarm-safety-eval-empty-writes-log-not-article]].
- Pending operator action: open `agi-tracker/2026-06-29`, `notegraph/2026-06-29` (+3n/+46e), `fix/workflow-security-audit-2026-06-28` (16C/36H), `skill-graph/2026-06-28` (INIT 173 skills), and `fix/workflow-security-audit-2026-06-21` (old RCE patch). All five still blocked by repo policy "GitHub Actions is not permitted to create or approve pull requests" — same App perm gap.
- AGI Tracker live since 2026-06-10. Last refresh 2026-06-29 Mon 13:00 UTC slot; next slot Mon 2026-07-06 — watch for ISS-006-induced miss. See [[agi-tracker]].
- pr-tracker inline email-OR filter holding for 3rd day — `Panniantong/Agent-Reach#436` still tracked (5d old today, 0 reviews); crosses 7d stale threshold on 2026-07-03 if untouched. Durable SKILL.md patch (AND→OR or drop prefix) still pending per [[pr-tracker-branch-prefix-misses-bot-identity]].

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
- ISS-006 fix: replace `messages.yml` `*/5 * * * *` with explicit per-slot crons covering **every** timeslot in `aeon.yml`. Day-11 pattern (morning EDA recovers, 08:00 batch silent again) confirms multi-pocket sliding; per [[iss-006-pocket-recovery-is-noise]] do NOT defer on the basis of any single clean day. See [[gha-messages-yml-cron-underdelivery]].
- ISS-006 cross-check: compare a gitlawb fork's `messages.yml` `*/5` delivery rate vs this repo's — distinguishes per-repo quota throttle from platform-wide GHA cron behavior.
- ISS-006 follow-up: manual `workflow_dispatch` of a 09:00-slot skill (e.g. `fleet-control`) to confirm the dispatch path still works while the 09:00 pocket is broken.
- Reclassify ISS-005 from `missing-secret-or-cron` to `permanent-limitation` and either add a log-based eval assertion or document NO_OUTPUT as expected when ledger is absent. See [[swarm-safety-eval-empty-writes-log-not-article]].
- Patch `pr-tracker` SKILL.md: drop `headRefName` / `mergedAt` / `--state merged` per [[gh-search-prs-api-drift]], AND replace `ai/`-only branch filter with commit-author email filter (`BOT_EMAIL=aeonframework@users.noreply.github.com`) per [[pr-tracker-branch-prefix-misses-bot-identity]]. Inline OR-filter has now held three days (06-29, 06-30, 07-01) — durable patch still pending.
- Widen `scenario-sweep.mjs` seed count or switch outlier detection to a tie-robust statistic (MAD-based) per [[compute-futures-12-seed-sample-too-small]]. Also resolve the seed-encoding artifact (3 of 12 seeds 10-digit) per [[compute-futures-seed-padding-bug]].
- File `./generate-skills-json` bugs as structured issues (see [[generate-skills-json-newline-bug]], [[skills-json-count-drift]]).
- Open the queued branches via PAT: `agi-tracker/2026-06-29`, `notegraph/2026-06-29`, `fix/workflow-security-audit-2026-06-28` (16C/36H), `skill-graph/2026-06-28` (INIT), `fix/workflow-security-audit-2026-06-21` (old RCE). All five blocked by repo policy "GitHub Actions is not permitted to create or approve pull requests".
- Populate `memory/watched-repos.md` or disable the four watched-repos-dependent skills (code-health, github-monitor, issue-triage, changelog) — current daily skip pattern wastes a workflow slot per skill.
- Defer ISS-001 close until ISS-006 is resolved.

## Completed Goals
- File a structured issue for `agi-tracker`'s 2nd consecutive Mon miss (2026-06-15, 2026-06-22) if Mon 2026-06-29 also misses. — completed 2026-06-29 (Mon 13:00 UTC slot fired; conditional trigger no longer met)
