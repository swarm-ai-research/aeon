# Memory Index

Pointer-only index. Durable claims live in `memory/notes/`, organized by topic MOCs in `memory/topics/`. Daily activity in `memory/logs/`. Structured issues in `memory/issues/`.

## Current focus
- ⚠ [[issues/ISS-006]] day 19 — **odd-DOM 08:00-pocket full-silence signature (NEW)**: batch-health, heartbeat, skill-freshness, gitlawb-fleet-metrics all failed to run today's 08:00 UTC slot (last runs 2026-07-08T09:08–09:16Z, ~33h gap — under heartbeat's 36h self-check threshold but the first time the entire 08:00 pocket has gone silent since the outage opened). Planner (06:30 daily) at ~4× threshold (last 2026-07-05T07:47Z, 82h silent). 06:00 pocket recovered with delays: notegraph 06:33Z, suggest-edges 06:32Z, compute-futures-eda 06:36Z all fired late. 09:00 batch (fleet-control/github-monitor/issue-triage) all fired ~10:07Z late. Close clock resets to 0 per [[iss-006-pocket-recovery-is-noise]]. Standing at-2× list now 3: cost-report (Mon 07:00, 19d, 2.7×), janitor (Sun 05:30, 19d, 2.7×), planner (daily 06:30, 82h, 4.4×).
- [[issues/ISS-001]] OAuth outage residue (2026-06-06 → 2026-06-20T06:05Z) day 19 of denominator burn-down — 38 skills at `success_rate < 0.5` while `last_status: success` and `consecutive_failures: 0`; close deferred until ISS-006 stabilizes.
- [[issues/ISS-007]] (2026-07-05) — heartbeat missing_pattern in skill-evals regex likely false positive per 2026-07-05 self-review (heartbeat DID run 2026-07-05T09:58Z, skill-evals scanned before slot fired). Same-day timing race.
- [[issues/ISS-008]] (2026-07-05) — cost-report no_file_match; standing ISS-006 tributary (weekly Mon 07:00 slot silent 4th consecutive Monday as of 2026-07-06).
- [[issues/ISS-005]] — swarm-safety-eval SSE_EMPTY path writes to log not article per [[swarm-safety-eval-empty-writes-log-not-article]]. Reclassify from `missing-secret-or-cron` → `permanent-limitation`.
- Pending operator action: **9 staged branches** all blocked by "GitHub Actions is not permitted to create or approve pull requests" — `agi-tracker/2026-06-29`, `notegraph/2026-07-06` (2026-07-07/08/09 runs all produced topology-identical output — **Day 3** of stable-topology silent-exit pattern per [[notegraph-extractor-generatedat-nondeterministic]]), `fix/workflow-security-audit-2026-06-21`, `fix/workflow-security-audit-2026-06-28`, `fix/workflow-security-audit-2026-07-05`, `skill-graph/2026-06-28`, `skillpacks/2026-07-05`, `suggest-edges/2026-07-07`.
- **PR queue (2026-07-09):** stationary — same 3 tracked-author PRs as 2026-07-07/08 (HKUDS/Vibe-Trading#390 MERGED, Panniantong/Agent-Reach#436 active, tamnd/kage#66 CLOSED no-merge; kage#66 rolls off tomorrow 2026-07-10). pr-tracker step-5 gate suppressed via inline **hash-based dedup guard** first-time-applied today per [[pr-tracker-notify-repeats-with-no-state-change]] — validates that fix. Would have been 4th consecutive zero-state-change fire without the guard. See [[pr-status]].
- **Swarm PR fleet moved (2026-07-09):** 3 fresh dependabot PRs opened 2026-07-09 05:36–05:38Z on `swarm-ai-research/swarm` (#530 langchain-core 1.4.8→1.4.9, #531 langgraph 1.2.5→1.2.8, #532 setuptools `<83,>=61.0` → `>=61.0,<84`). Queue grew 4→6; pre-existing #524/#527/#529 unchanged. pr-review 11th consecutive day of 403 write-block on #527 APPROVE 5/5 verdict per [[aeon-app-no-write-on-swarm-repo]]; pr-triage got the same 403 on #527 DEFER — logged PR_TRIAGE_NO_PERMISSION, deliberately did NOT append to `triaged-prs.json` so retry re-fires.
- AGI Tracker last refresh 2026-06-29 Mon 13:00 UTC; 2026-07-06 slot missed on ISS-006; next opportunity 2026-07-13.
- `docs/status.md` auto-commit bug per [[status-md-auto-commit-drops-writes]] — heartbeat did not run today so no new drop; still standing at 4th-consecutive-drop urgent-tier from 2026-07-08.
- skill-freshness FRESHNESS_OK **stalled at 10** (2026-07-09 slot never fired) — structurally blind in GHA per [[skill-freshness-mtime-blind-in-gha]]. compute-pulse.md at ~120h/168h (71%) after today's slot miss — tips WARN if compute-pulse misses 2026-07-11 11:00 UTC.
- **NEW durable claim (2026-07-09):** compute-futures-eda's |r|≥0.8 findings involving `wallet_sum_pnl` are float-dust artifacts — today's first-ever run-window crossing (synthetic/x402 wallet_sum_pnl × settlementLegs = −0.874) is the same shape as 07-07's spread near-leader (−0.752 → +0.190 self-cleared 07-08). See [[compute-futures-eda-wallet-sum-pnl-correlations-are-float-dust]].
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
- ISS-006 fix: replace `messages.yml` `*/5 * * * *` with explicit per-slot crons covering **every** timeslot in `aeon.yml`. Day-19 signature migrated from 06:00-pocket to 08:00-pocket full-silence — same delivery-rate bug per [[gha-messages-yml-cron-underdelivery]], different pocket manifesting; do not defer per [[iss-006-pocket-recovery-is-noise]].
- Standardize notification emission across SKILL.md files on **direct `.pending-notify/${epoch}-${skill}.md` writes** — both `$(cat file)` forms (inline and MSG-variable) are blocked per updated [[notify-inline-cat-substitution-blocked-in-sandbox]], `./notify -f` is broken per updated [[notify-script-has-no-f-flag]], and recovery from an `-f`-corrupted queue is an in-place payload rewrite (not a re-fire). Node `execFileSync` is a secondary option. SKILL.md audit sweep needed.
- Fix `docs/status.md` auto-commit drop per [[status-md-auto-commit-drops-writes]] — 4 consecutive silent write losses as of 2026-07-08; today's heartbeat miss means no new drop but no fix either. Urgent-tier alongside ISS-006 — audit `messages.yml` auto-commit `git add` glob to include `docs/`, or make heartbeat commit explicitly.
- Patch notegraph skill's silent-exit heuristic per [[notegraph-extractor-generatedat-nondeterministic]] — either mask `generatedAt` before diffing or teach the extractor to omit it; 3 consecutive days (07-07/08/09) of naive HAS_DIFF gate mis-firing on topologically-stable corpora.
- Close ISS-007 as false positive OR add same-day grace window to `skill-evals` (scan same-day logs only after 12:00 UTC) — heartbeat DID run 2026-07-05 but skill-evals scanned before the late slot fired.
- Patch `pr-tracker` SKILL.md in one batch: (a) drop `stateReason` from GraphQL query per [[graphql-statereason-only-on-issue-type]], (b) drop `headRefName` / `mergedAt` / `--state merged` per [[gh-search-prs-api-drift]], (c) replace `ai/`-only branch filter with list/domain commit-author filter per [[aeon-bot-uses-multiple-signing-identities]] + [[pr-tracker-branch-prefix-misses-bot-identity]], (d) **land the hash-based step-5 dedup guard** — validated in-skill today (skipped-dedup, 0 wasted notify) per [[pr-tracker-notify-repeats-with-no-state-change]], (e) add fresh-bot-PR trigger per [[pr-tracker-step-5-misses-fresh-bot-prs]].
- Fix `skill-freshness` to use `git log -1 --format=%ct` instead of `stat --format=%Y` per [[skill-freshness-mtime-blind-in-gha]] — 10-consecutive FRESHNESS_OK is structural, not clean; today's slot miss froze the counter at 10.
- Widen `scenario-sweep.mjs` seed count or switch outlier detection to a tie-robust statistic per [[compute-futures-12-seed-sample-too-small]]. Additionally, filter out `wallet_sum_pnl` correlations per [[compute-futures-eda-wallet-sum-pnl-correlations-are-float-dust]] until σ(wallet_sum_pnl) > 1e-6. Also resolve seed-encoding artifact (3 of 12 seeds 10-digit) per [[compute-futures-seed-padding-bug]].
- File `./generate-skills-json` bugs as structured issues (see [[generate-skills-json-newline-bug]], [[skills-json-count-drift]]).
- Investigate missing `scripts/validate-config.js` referenced by config-validator SKILL.md — either restore the script or drop the fast-path reference.
- Open the 9 staged branches via PAT — all blocked by "GitHub Actions is not permitted to create or approve pull requests" per [[github-actions-cannot-create-prs]].
- Populate `memory/watched-repos.md` or disable the five watched-repos-dependent skills (code-health, github-monitor, issue-triage, changelog, weekly-shiplog) — daily skip pattern wastes a workflow slot per skill.
- Defer ISS-001 close until ISS-006 is resolved.
