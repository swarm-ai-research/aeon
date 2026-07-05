# Memory Index

Pointer-only index. Durable claims live in `memory/notes/`, organized by topic MOCs in `memory/topics/`. Daily activity in `memory/logs/`. Structured issues in `memory/issues/`.

## Current focus
- ⚠ [[issues/ISS-006]] day 15 — **large 07:44Z burst broke two 15-day silences** (skillpacks + compute-macro-correlate first fires since 2026-06-20; planner/EDA/config-validator/swarm-safety-eval also flushed as ~1-2h catchup). But janitor 05:30 stayed cold and 08:00 batch fired ~2h late — classic stuck-then-flush signature per [[iss-006-pocket-recovery-is-noise]], NOT resolution. Close clock stays 0. Four weekly/biweekly still at 2× threshold: milestone-tracker (Mon 12:00), cost-report (Mon 07:00), memory-structural-dedupe (even DOM 06:10), janitor (Sun 05:30).
- [[issues/ISS-001]] OAuth outage residue (2026-06-06 → 2026-06-20T06:05Z) day 15 of denominator burn-down — 38 skills at `success_rate < 0.5` while `last_status: success` and `consecutive_failures: 0`; close deferred until ISS-006 stabilizes.
- [[issues/ISS-007]] (new 2026-07-05) — heartbeat missing_pattern in skill-evals regex; enabled skill FAIL. Not covered by ISS-002/005.
- [[issues/ISS-008]] (new 2026-07-05) — cost-report no_file_match; ISS-006 tributary (weekly Mon 07:00 slot at 2× threshold).
- [[issues/ISS-005]] — swarm-safety-eval SSE_EMPTY path writes to log not article per [[swarm-safety-eval-empty-writes-log-not-article]]. Reclassify from `missing-secret-or-cron` → `permanent-limitation`.
- Pending operator action: **7 staged branches** all blocked by "GitHub Actions is not permitted to create or approve pull requests" — `agi-tracker/2026-06-29`, `notegraph/2026-07-04` (6th consecutive notegraph queued), `fix/workflow-security-audit-2026-06-21`, `fix/workflow-security-audit-2026-06-28`, `fix/workflow-security-audit-2026-07-05` (13 unpinned-uses Critical resolved), `skill-graph/2026-06-28`, `skillpacks/2026-07-05` (outages-fleet rename).
- AGI Tracker last refresh 2026-06-29 Mon 13:00 UTC; next slot Mon 2026-07-06 — watch for ISS-006-induced miss. See [[agi-tracker]].
- pr-tracker: 2026-07-05 audit **notify fired 2nd consecutive day with zero state change** vs 2026-07-04 — same 3-PR set at identical head SHAs, exposing step-5 dedup gap per [[pr-tracker-notify-repeats-with-no-state-change]]. Queue: Vibe-Trading#390 (2d 3h fresh, `@aeonframework.dev`), Agent-Reach#436 (8d 16h **stale**), kage#66 (closed silently by owner `tamnd` 2026-07-03T12:20Z). Also caught SKILL.md GraphQL query hard-failing on `stateReason` per [[graphql-statereason-only-on-issue-type]] and `./notify -f` flag not supported per [[notify-script-has-no-f-flag]] (yesterday's log used same broken pattern).
- skill-freshness FRESHNESS_OK 7th consecutive emit — structurally blind in GHA per [[skill-freshness-mtime-blind-in-gha]]. Content-embedded date proxy shows `compute-pulse.md` at 98.2% of 7d threshold — tips WARN if compute-pulse misses 2026-07-11 11:00 UTC.
- workflow-security-audit landed a **fresh SHA-pinning wave** — 13/16 unpinned-uses Critical findings from 2026-06-28 audit RESOLVED across chain-runner / fleet-runner / lint / messages / sync-aeon-public-results / sync-upstream; only `aeon.yml` still on `@v5` mutable tags (3 remaining).
- docs/status.md auto-commit bug per [[status-md-auto-commit-drops-writes]] — heartbeat regenerated the page 2026-07-04 but on-disk file remained at 2026-06-09; today's regen may hit the same silent-drop.
- `.pending-disclosure/` queue: 1 entry (torlink 07-04, `ip@2.0.1` HIGH unpatchable + `esbuild` LOW dev-only) — no change today.

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
- ISS-006 fix: replace `messages.yml` `*/5 * * * *` with explicit per-slot crons covering **every** timeslot in `aeon.yml`. Day-15 07:44Z burst pattern (six recoveries clustered in one tick) is exactly the stuck-then-flush signature of a broken scheduler — do NOT defer on this apparent progress per [[iss-006-pocket-recovery-is-noise]]. See [[gha-messages-yml-cron-underdelivery]].
- ISS-006 cross-check: compare a gitlawb fork's `messages.yml` `*/5` delivery rate vs this repo's — distinguishes per-repo quota throttle from platform-wide GHA cron behavior.
- Reclassify ISS-005 from `missing-secret-or-cron` to `permanent-limitation` per [[swarm-safety-eval-empty-writes-log-not-article]].
- Patch `pr-tracker` SKILL.md in one batch: (a) drop `stateReason` from GraphQL query per [[graphql-statereason-only-on-issue-type]], (b) drop `headRefName` / `mergedAt` / `--state merged` per [[gh-search-prs-api-drift]], (c) replace `ai/`-only branch filter with **list/domain** commit-author filter per [[aeon-bot-uses-multiple-signing-identities]] + [[pr-tracker-branch-prefix-misses-bot-identity]], (d) add step-5 dedup guard per [[pr-tracker-notify-repeats-with-no-state-change]], (e) add fresh-bot-PR trigger per [[pr-tracker-step-5-misses-fresh-bot-prs]].
- Fix `./notify -f <file>` bug per [[notify-script-has-no-f-flag]] — either add the flag to `./notify` OR replace all SKILL.md invocations with `MSG=$(cat file); ./notify "$MSG"`. Pr-tracker and surplus-pulse already caught silently corrupting notifies.
- Fix `docs/status.md` auto-commit drop per [[status-md-auto-commit-drops-writes]] — audit `messages.yml` auto-commit `git add` glob to include `docs/`, or make heartbeat commit explicitly.
- Fix `skill-freshness` to use `git log -1 --format=%ct` instead of `stat --format=%Y` per [[skill-freshness-mtime-blind-in-gha]] — 7th consecutive FRESHNESS_OK is structural, not clean.
- Widen `scenario-sweep.mjs` seed count or switch outlier detection to a tie-robust statistic per [[compute-futures-12-seed-sample-too-small]]. Also resolve the seed-encoding artifact (3 of 12 seeds 10-digit) per [[compute-futures-seed-padding-bug]].
- File `./generate-skills-json` bugs as structured issues (see [[generate-skills-json-newline-bug]], [[skills-json-count-drift]]).
- Investigate missing `scripts/validate-config.js` referenced by config-validator SKILL.md — either restore the script or drop the fast-path reference.
- Open the 7 staged branches via PAT — all blocked by "GitHub Actions is not permitted to create or approve pull requests" per [[github-actions-cannot-create-prs]].
- Populate `memory/watched-repos.md` or disable the four watched-repos-dependent skills (code-health, github-monitor, issue-triage, changelog) — daily skip pattern wastes a workflow slot per skill.
- Defer ISS-001 close until ISS-006 is resolved.
