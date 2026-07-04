# Memory Index

Pointer-only index. Durable claims live in `memory/notes/`, organized by topic MOCs in `memory/topics/`. Daily activity in `memory/logs/`. Structured issues in `memory/issues/`.

## Current focus
- ⚠ [[issues/ISS-006]] day 14 — **memory-flush pocket half-recovered**: memory-flush fired 06:02Z (14-day even-day silence broken from 2026-06-20T06:07Z) but memory-structural-dedupe 06:10 slot **confirmed silent**, so the recovery is single-slot noise per [[iss-006-pocket-recovery-is-noise]]. Sixth consecutive pocket-swap day (D10 EDA↔08:00, D11 reversed, D12 flipped, D13 EDA-recover, D14 memory-flush-recover, D15 memory-flush-holds-but-dedupe-still-silent-+-planner-miss). Six weekly/biweekly skills at 2× threshold (janitor / skillpacks / compute-macro-correlate on Sun, milestone-tracker / cost-report on Mon, memory-structural-dedupe on even DOM) all trace to ISS-006. Close clock stays 0 until 3 consecutive clean days across every slot.
- [[issues/ISS-001]] OAuth outage (2026-06-06 → 2026-06-20T06:05Z) — recovery batch holding, all 38 tracked skills at `last_status: success`. Cumulative `success_rate` < 0.6 takes weeks to clear; close decision deferred until ISS-006 stabilizes.
- [[issues/ISS-005]] — swarm-safety-eval running successfully; SSE_EMPTY path writes to daily log not an article. Reclassify from `missing-secret-or-cron` → `permanent-limitation` per [[swarm-safety-eval-empty-writes-log-not-article]].
- Pending operator action: five staged branches (`agi-tracker/2026-06-29`, `notegraph/2026-06-29` +3n/+51e today, `fix/workflow-security-audit-2026-06-28`, `skill-graph/2026-06-28`, `fix/workflow-security-audit-2026-06-21`) all blocked by repo policy "GitHub Actions is not permitted to create or approve pull requests". notegraph now on 6th consecutive queued branch (06-26/06-29/07-01/07-02/07-04).
- AGI Tracker live since 2026-06-10. Last refresh 2026-06-29 Mon 13:00 UTC; next slot Mon 2026-07-06 — watch for ISS-006-induced miss. See [[agi-tracker]].
- pr-tracker: 2026-07-04 audit **notify fired** (step-5 met: stale ≥ 1 AND closed-no-merge ≥ 1, first notify since 2026-06-26). Queue: Vibe-Trading#390 (1d, fresh, `@aeonframework.dev`), Agent-Reach#436 (7d 15h **stale**), kage#66 **closed no-merge silently** by owner `tamnd` on 2026-07-03T12:20Z after 12h 50m open (COMPLETED, no comment). Bot multiplicity: [[aeon-bot-uses-multiple-signing-identities]]; step-5 notify gap: [[pr-tracker-step-5-misses-fresh-bot-prs]]. Inline OR-filter widening 6+ days.
- skill-freshness FRESHNESS_OK 6th consecutive emit — structurally blind in GHA per [[skill-freshness-mtime-blind-in-gha]]; the OK verdicts mean `git checkout` reset every mtime, not that deps are fresh. Content-embedded date proxy in today's article showed `compute-pulse.md` at 98.2% of 7d threshold (165h) — tips WARN if compute-pulse misses Sat 2026-07-05 11:00 UTC.
- `.pending-disclosure/` queue: 1 entry (torlink 07-04, `ip@2.0.1` HIGH unpatchable + `esbuild` LOW dev-only). vuln-scanner cannot fork upstream repos with runtime token; operator PAT needed to submit.

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
- ISS-006 fix: replace `messages.yml` `*/5 * * * *` with explicit per-slot crons covering **every** timeslot in `aeon.yml`. Day-10 → Day-15 pocket-swap sequence (6 consecutive days each flipping which pocket recovers) plus 6 weekly/biweekly skills at 2× threshold all trace to the same underdelivery; per [[iss-006-pocket-recovery-is-noise]] do NOT defer on any single clean pocket. See [[gha-messages-yml-cron-underdelivery]].
- ISS-006 cross-check: compare a gitlawb fork's `messages.yml` `*/5` delivery rate vs this repo's — distinguishes per-repo quota throttle from platform-wide GHA cron behavior.
- ISS-006 follow-up: manual `workflow_dispatch` of a 09:00-slot skill (e.g. `fleet-control`) to confirm the dispatch path still works while the 09:00 pocket is broken.
- Reclassify ISS-005 from `missing-secret-or-cron` to `permanent-limitation` and either add a log-based eval assertion or document NO_OUTPUT as expected when ledger is absent. See [[swarm-safety-eval-empty-writes-log-not-article]].
- Patch `pr-tracker` SKILL.md: drop `headRefName` / `mergedAt` / `--state merged` per [[gh-search-prs-api-drift]], AND replace `ai/`-only branch filter with a **list/domain** commit-author filter accepting both `aeonframework@users.noreply.github.com` and any `@aeonframework.dev` per [[aeon-bot-uses-multiple-signing-identities]] + [[pr-tracker-branch-prefix-misses-bot-identity]]. Inline OR-filter has held 6 days (06-29 → 07-04). Agent-Reach#436 crossed 7d threshold at 19:24Z 2026-07-03; today's run flagged stale + notified.
- Add a fourth `pr-tracker` step-5 notify trigger for "N ≥ 1 fresh bot PRs opened in last 24h" per [[pr-tracker-step-5-misses-fresh-bot-prs]]. Today two 2h/11h-old bot PRs silently landed while notify was skipped — the operator's primary signal for "bot did work today" never fires.
- Fix `skill-freshness` to use `git log -1 --format=%ct` (producer-commit timestamp) instead of `stat --format=%Y` — per [[skill-freshness-mtime-blind-in-gha]], the current mtime check can never flag anything in GHA because `actions/checkout` resets all mtimes to the run instant. Explains 5 consecutive FRESHNESS_OK emits.
- Widen `scenario-sweep.mjs` seed count or switch outlier detection to a tie-robust statistic (MAD-based) per [[compute-futures-12-seed-sample-too-small]]. Also resolve the seed-encoding artifact (3 of 12 seeds 10-digit) per [[compute-futures-seed-padding-bug]].
- File `./generate-skills-json` bugs as structured issues (see [[generate-skills-json-newline-bug]], [[skills-json-count-drift]]).
- Open the five staged branches via PAT (see Current focus above) — all blocked by "GitHub Actions is not permitted to create or approve pull requests" repo policy.
- Populate `memory/watched-repos.md` or disable the four watched-repos-dependent skills (code-health, github-monitor, issue-triage, changelog) — current daily skip pattern wastes a workflow slot per skill.
- Defer ISS-001 close until ISS-006 is resolved.

