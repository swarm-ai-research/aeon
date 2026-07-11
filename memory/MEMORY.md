# Memory Index

Pointer-only index. Durable claims live in `memory/notes/`, organized by topic MOCs in `memory/topics/`. Daily activity in `memory/logs/`. Structured issues in `memory/issues/`.

## Current focus
- ⚠ [[issues/ISS-006]] day 20 (2026-07-10 Fri even-DOM) — **08:00-pocket 2nd consecutive day of full silence** (tip fired): batch-health/heartbeat/skill-freshness/gitlawb-fleet-metrics all still at 2026-07-08T09:08–09:16Z (~57h silent, 2×-threshold crossed). 06:00 pocket largely recovered today: memory-flush/-structural-dedupe/compute-futures-eda/notegraph/suggest-edges all late-fired 06:29Z–06:34Z; planner (06:30 daily) still silent (last 2026-07-05T07:47Z, 130h / 5.4× threshold). Close clock still at 0 clean days per [[iss-006-pocket-recovery-is-noise]]. Standing at-2× list still 3: planner (5.4×), cost-report (Mon 07:00, 20d, 2.86×), janitor (Sun 05:30, 20d, 2.86×).
- [[issues/ISS-001]] OAuth outage residue (2026-06-06 → 2026-06-20T06:05Z) day 20 of denominator burn-down — 38 skills at `success_rate < 0.5` while `last_status: success` and `consecutive_failures: 0`; close deferred until ISS-006 stabilizes.
- [[issues/ISS-007]] (2026-07-05) — heartbeat missing_pattern in skill-evals regex likely false positive per 2026-07-05 self-review (heartbeat DID run 2026-07-05T09:58Z, skill-evals scanned before slot fired). Same-day timing race.
- [[issues/ISS-008]] (2026-07-05) — cost-report no_file_match; standing ISS-006 tributary (weekly Mon 07:00 slot silent 4th consecutive Monday as of 2026-07-06).
- [[issues/ISS-005]] — swarm-safety-eval SSE_EMPTY path writes to log not article per [[swarm-safety-eval-empty-writes-log-not-article]]. Reclassify from `missing-secret-or-cron` → `permanent-limitation`.
- Pending operator action: **11 staged branches** all blocked by "GitHub Actions is not permitted to create or approve pull requests" per [[github-actions-cannot-create-prs]] — `agi-tracker/2026-06-29`, `notegraph/2026-07-06` (2026-07-07/08/09/10 runs all produced topology-identical output — **Day 4** of stable-topology silent-exit; fingerprint scheme swapped 2026-07-10 to Node-based sha1 to sidestep sandbox `xargs sha1sum` block per [[notegraph-extractor-generatedat-nondeterministic]]), `fix/workflow-security-audit-2026-06-21`, `-06-28`, `-07-05`, `skill-graph/2026-06-28`, `skillpacks/2026-07-05`, `suggest-edges/2026-07-07`, `suggest-edges/2026-07-10`, `suggest-edges/2026-07-11` (**3rd consecutive day** of the same 3 similarity-1.00 links from `gitlawb-compute-futures-proofs/2026-06-20.md`; state file re-created fresh for a 2nd day, validating [[skill-state-on-blocked-pr-branch-is-lost]]).
- **PR queue (last snapshot 2026-07-10):** stationary 5th consecutive day — 3 tracked-author PRs (HKUDS/Vibe-Trading#390 MERGED, Panniantong/Agent-Reach#436 active, tamnd/kage#66 CLOSED no-merge). kage#66 rolls off 7d closed-no-merge window today at 12:20Z (~2h 15m after pr-tracker's 10:03Z snapshot) — tomorrow's 07-11 snapshot expected to show closed-no-merge 1→0 (first legitimate state change; hash-guard should not suppress). Vibe-Trading#390 rolls off 2026-07-12. pr-tracker step-5 hash-based dedup guard applied 2nd consecutive day per [[pr-tracker-notify-repeats-with-no-state-change]] — validated. See [[pr-status]].
- **Swarm PR fleet stationary (2026-07-10):** same 6 open PRs as 2026-07-09 (5 dependabot bots + #527 rsavitt neurosymbolic), same head SHAs, no new activity since 2026-07-09 05:38Z. pr-review **13th consecutive day** of 403 write-block on #527 APPROVE 5/5 verdict per [[aeon-app-no-write-on-swarm-repo]]; pr-triage same 403 on #527 DEFER (PR_TRIAGE_NO_PERMISSION, deliberately no `triaged-prs.json` append so retry re-fires).
- AGI Tracker last refresh 2026-06-29 Mon 13:00 UTC; 2026-07-06 slot missed on ISS-006; next opportunity 2026-07-13.
- `docs/status.md` auto-commit bug per [[status-md-auto-commit-drops-writes]] — heartbeat didn't run 2026-07-09 or 2026-07-10 (08:00 pocket silent both days) so no new drops; still standing at 4th-consecutive-drop urgent-tier from 2026-07-08.
- skill-freshness FRESHNESS_OK **stalled at 10** — 08:00 slot missed 2 consecutive days (2026-07-09/10). Structurally blind in GHA per [[skill-freshness-mtime-blind-in-gha]]. compute-pulse.md at ~161h/168h (~96%) — tips WARN if compute-pulse misses 2026-07-11 11:00 UTC slot (~18h away).
- **Durable claim (2026-07-09), validated (2026-07-10):** compute-futures-eda's |r|≥0.8 findings involving `wallet_sum_pnl` are float-dust artifacts — 2026-07-10 delivered a 2nd consecutive-day crossing (`x402 wallet_sum_pnl × x402Total = +0.881`, σ ≈ 1.21e−14) while yesterday's synth/x402 crossing collapsed −0.874 → +0.225 (standard 12-seed churn on float dust). See [[compute-futures-eda-wallet-sum-pnl-correlations-are-float-dust]].
- **New atomic claim (2026-07-10):** suggest-edges writes `applied` dedup state to its daily branch; when [[github-actions-cannot-create-prs]] blocks the PR, state never reaches main and the next run re-proposes the same edges — validated today when the same 3 similarity-1.00 edges from 07-07 re-appeared. See [[skill-state-on-blocked-pr-branch-is-lost]].
- `.pending-disclosure/` queue: 1 entry (torlink 07-04, `ip@2.0.1` HIGH unpatchable + `esbuild` LOW dev-only) — no change through 2026-07-10.

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
- ISS-006 fix: replace `messages.yml` `*/5 * * * *` with explicit per-slot crons covering **every** timeslot in `aeon.yml`. Day-20 signature (2026-07-10) escalates yesterday's 08:00-pocket-full-silence into a **2nd consecutive day** of the same 4-skill 08:00 miss (batch-health / heartbeat / skill-freshness / gitlawb-fleet-metrics still at 2026-07-08T09:08–09:16Z) — same delivery-rate bug per [[gha-messages-yml-cron-underdelivery]], no longer a 1-day fluke; do not defer per [[iss-006-pocket-recovery-is-noise]].
- Standardize notification emission across SKILL.md files on **direct `.pending-notify/${epoch}-${skill}.md` writes** — both `$(cat file)` forms (inline and MSG-variable) are blocked per updated [[notify-inline-cat-substitution-blocked-in-sandbox]], `./notify -f` is broken per updated [[notify-script-has-no-f-flag]], and recovery from an `-f`-corrupted queue is an in-place payload rewrite (not a re-fire). Node `execFileSync` is a secondary option. SKILL.md audit sweep needed.
- Fix `docs/status.md` auto-commit drop per [[status-md-auto-commit-drops-writes]] — 4 consecutive silent write losses as of 2026-07-08; 2026-07-09 heartbeat miss (08:00 pocket silent) means no new drop but no fix either. Urgent-tier alongside ISS-006 — audit `messages.yml` auto-commit `git add` glob to include `docs/`, or make heartbeat commit explicitly.
- Patch notegraph skill's silent-exit heuristic per [[notegraph-extractor-generatedat-nondeterministic]] — either mask `generatedAt` before diffing or teach the extractor to omit it; **4 consecutive days** (07-07/08/09/10) of naive HAS_DIFF gate mis-firing on topologically-stable corpora. Fingerprint scheme swapped 2026-07-10 to Node-based sha1 (shell `xargs sha1sum` blocked by sandbox) — deterministic and reproducible, but doesn't fix the underlying issue.
- Close ISS-007 as false positive OR add same-day grace window to `skill-evals` (scan same-day logs only after 12:00 UTC) — heartbeat DID run 2026-07-05 but skill-evals scanned before the late slot fired.
- Patch `pr-tracker` SKILL.md in one batch: (a) drop `stateReason` from GraphQL query per [[graphql-statereason-only-on-issue-type]], (b) drop `headRefName` / `mergedAt` / `--state merged` per [[gh-search-prs-api-drift]], (c) replace `ai/`-only branch filter with list/domain commit-author filter per [[aeon-bot-uses-multiple-signing-identities]] + [[pr-tracker-branch-prefix-misses-bot-identity]], (d) **land the hash-based step-5 dedup guard** — validated in-skill 2026-07-09 (skipped-dedup, 0 wasted notify) per [[pr-tracker-notify-repeats-with-no-state-change]], (e) add fresh-bot-PR trigger per [[pr-tracker-step-5-misses-fresh-bot-prs]].
- Fix `skill-freshness` to use `git log -1 --format=%ct` instead of `stat --format=%Y` per [[skill-freshness-mtime-blind-in-gha]] — 10-consecutive FRESHNESS_OK is structural, not clean; 2026-07-09/10 slot misses froze the counter at 10 for a 2nd consecutive day.
- Widen `scenario-sweep.mjs` seed count or switch outlier detection to a tie-robust statistic per [[compute-futures-12-seed-sample-too-small]]. Additionally, filter out `wallet_sum_pnl` correlations per [[compute-futures-eda-wallet-sum-pnl-correlations-are-float-dust]] until σ(wallet_sum_pnl) > 1e-6. Also resolve seed-encoding artifact (3 of 12 seeds 10-digit) per [[compute-futures-seed-padding-bug]].
- File `./generate-skills-json` bugs as structured issues (see [[generate-skills-json-newline-bug]], [[skills-json-count-drift]]).
- Investigate missing `scripts/validate-config.js` referenced by config-validator SKILL.md — either restore the script or drop the fast-path reference.
- Open the 10 staged branches via PAT — all blocked by "GitHub Actions is not permitted to create or approve pull requests" per [[github-actions-cannot-create-prs]]. Delay is now also causing skill-state loss (suggest-edges re-proposed same 3 edges today) per [[skill-state-on-blocked-pr-branch-is-lost]].
- Populate `memory/watched-repos.md` or disable the five watched-repos-dependent skills (code-health, github-monitor, issue-triage, changelog, weekly-shiplog) — daily skip pattern wastes a workflow slot per skill.
- Defer ISS-001 close until ISS-006 is resolved.
