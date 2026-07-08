# Memory Index

Pointer-only index. Durable claims live in `memory/notes/`, organized by topic MOCs in `memory/topics/`. Daily activity in `memory/logs/`. Structured issues in `memory/issues/`.

## Current focus
- ⚠ [[issues/ISS-006]] day 18 — **Wed even-DOM planner-only-silent signature** (memory-flush + memory-structural-dedupe + compute-futures-eda + notegraph + suggest-edges all late-fired between 06:26Z–06:34Z, clearing their multi-day silences; batch-health 08:00 late by ~54m; heartbeat 08:00 late by ~66m). Only planner (06:30 daily) stayed silent through today's slot — a *sharpening* of the pocket signature, not resolution. Close clock stays 0 per [[iss-006-pocket-recovery-is-noise]]. stale-content-pr-sweeper cleared last night (23:45 slot late-fired 2026-07-08T00:14:46Z). Standing at-2× list shrunk 5 → 3: cost-report (Mon 07:00, 2.6×), janitor (Sun 05:30, 2.6×), planner (daily 06:30, 3×) — memory-structural-dedupe / compute-futures-eda flags cleared today.
- [[issues/ISS-001]] OAuth outage residue (2026-06-06 → 2026-06-20T06:05Z) day 18 of denominator burn-down — 38 skills at `success_rate < 0.5` while `last_status: success` and `consecutive_failures: 0`; close deferred until ISS-006 stabilizes.
- [[issues/ISS-007]] (2026-07-05) — heartbeat missing_pattern in skill-evals regex likely false positive per 2026-07-05 self-review (heartbeat DID run 2026-07-05T09:58Z, skill-evals scanned before slot fired). Same-day timing race.
- [[issues/ISS-008]] (2026-07-05) — cost-report no_file_match; standing ISS-006 tributary (weekly Mon 07:00 slot silent 3rd consecutive Monday).
- [[issues/ISS-005]] — swarm-safety-eval SSE_EMPTY path writes to log not article per [[swarm-safety-eval-empty-writes-log-not-article]]. Reclassify from `missing-secret-or-cron` → `permanent-limitation`.
- Pending operator action: **9 staged branches** all blocked by "GitHub Actions is not permitted to create or approve pull requests" — `agi-tracker/2026-06-29`, `notegraph/2026-07-06` (2026-07-07 and 2026-07-08 runs both produced topology-identical output per [[notegraph-extractor-generatedat-nondeterministic]]), `fix/workflow-security-audit-2026-06-21`, `fix/workflow-security-audit-2026-06-28`, `fix/workflow-security-audit-2026-07-05`, `skill-graph/2026-06-28`, `skillpacks/2026-07-05`, `suggest-edges/2026-07-07`.
- **PR queue (2026-07-08):** stationary — same 3 PRs, same buckets, same head SHAs as 2026-07-07 (HKUDS/Vibe-Trading#390 MERGED, Panniantong/Agent-Reach#436 active, tamnd/kage#66 CLOSED no-merge). pr-tracker fired **3rd consecutive zero-state-change notify** per [[pr-tracker-notify-repeats-with-no-state-change]] — hash-based dedup guard from that note would have suppressed today's fire. See [[pr-status]].
- AGI Tracker last refresh 2026-06-29 Mon 13:00 UTC; 2026-07-06 slot missed on ISS-006; next opportunity 2026-07-13.
- `docs/status.md` auto-commit bug per [[status-md-auto-commit-drops-writes]] — as of 2026-07-08 heartbeat run, **4th consecutive day** heartbeat regenerated the page but on-disk file remained at 2026-06-09. Auto-commit `git add` glob does not stage `docs/`. Urgent-tier alongside ISS-006.
- **In-place update (2026-07-08):** [[notify-script-has-no-f-flag]] recovery instruction fixed — old instruction ("re-invoke inline `MSG=$(cat file); ./notify "$MSG"`") is broken since 2026-07-07 invalidation; the working recovery is to overwrite the bogus `.pending-notify/<ts>.md` in place with the intended body and NOT re-fire notify (post-run processor dispatches what's on disk). Triggered today after pr-tracker's SKILL.md step 6 `./notify -f …` invocation wrote `-f` as the message body.
- skill-freshness FRESHNESS_OK 10th consecutive emit — structurally blind in GHA per [[skill-freshness-mtime-blind-in-gha]]. compute-pulse.md at 96h/168h threshold — tips WARN if compute-pulse misses 2026-07-11 11:00 UTC.
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
- ISS-006 fix: replace `messages.yml` `*/5 * * * *` with explicit per-slot crons covering **every** timeslot in `aeon.yml`. Day-18 planner-only signature is a sharpened pattern of the same delivery-rate bug per [[gha-messages-yml-cron-underdelivery]]; do not defer per [[iss-006-pocket-recovery-is-noise]].
- Standardize notification emission across SKILL.md files on **direct `.pending-notify/${epoch}-${skill}.md` writes** — both `$(cat file)` forms (inline and MSG-variable) are blocked per updated [[notify-inline-cat-substitution-blocked-in-sandbox]], `./notify -f` is broken per updated [[notify-script-has-no-f-flag]], and recovery from an `-f`-corrupted queue is now an in-place payload rewrite (not a re-fire). Node `execFileSync` is a secondary option. SKILL.md audit sweep needed.
- Fix `docs/status.md` auto-commit drop per [[status-md-auto-commit-drops-writes]] — **4 consecutive silent write losses now**. Urgent-tier alongside ISS-006 as a durable-fix priority — audit `messages.yml` auto-commit `git add` glob to include `docs/`, or make heartbeat commit explicitly.
- Patch notegraph skill's silent-exit heuristic per [[notegraph-extractor-generatedat-nondeterministic]] — either mask `generatedAt` before diffing or teach the extractor to omit it; today's naive HAS_DIFF gate would have re-PRed a topologically-stable corpus.
- Close ISS-007 as false positive OR add same-day grace window to `skill-evals` (scan same-day logs only after 12:00 UTC) — heartbeat DID run 2026-07-05 but skill-evals scanned before the late slot fired.
- Patch `pr-tracker` SKILL.md in one batch: (a) drop `stateReason` from GraphQL query per [[graphql-statereason-only-on-issue-type]], (b) drop `headRefName` / `mergedAt` / `--state merged` per [[gh-search-prs-api-drift]], (c) replace `ai/`-only branch filter with list/domain commit-author filter per [[aeon-bot-uses-multiple-signing-identities]] + [[pr-tracker-branch-prefix-misses-bot-identity]], (d) add step-5 dedup guard (hash-based per today's OPEN→MERGED reveal, not day-based) per [[pr-tracker-notify-repeats-with-no-state-change]], (e) add fresh-bot-PR trigger per [[pr-tracker-step-5-misses-fresh-bot-prs]].
- Fix `skill-freshness` to use `git log -1 --format=%ct` instead of `stat --format=%Y` per [[skill-freshness-mtime-blind-in-gha]] — 9th consecutive FRESHNESS_OK is structural, not clean.
- Widen `scenario-sweep.mjs` seed count or switch outlier detection to a tie-robust statistic per [[compute-futures-12-seed-sample-too-small]]. Also resolve seed-encoding artifact (3 of 12 seeds 10-digit) per [[compute-futures-seed-padding-bug]].
- File `./generate-skills-json` bugs as structured issues (see [[generate-skills-json-newline-bug]], [[skills-json-count-drift]]).
- Investigate missing `scripts/validate-config.js` referenced by config-validator SKILL.md — either restore the script or drop the fast-path reference.
- Open the 9 staged branches via PAT — all blocked by "GitHub Actions is not permitted to create or approve pull requests" per [[github-actions-cannot-create-prs]].
- Populate `memory/watched-repos.md` or disable the five watched-repos-dependent skills (code-health, github-monitor, issue-triage, changelog, weekly-shiplog) — daily skip pattern wastes a workflow slot per skill.
- Defer ISS-001 close until ISS-006 is resolved.
