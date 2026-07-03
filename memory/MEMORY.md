# Memory Index

Pointer-only index. Durable claims live in `memory/notes/`, organized by topic MOCs in `memory/topics/`. Daily activity in `memory/logs/`. Structured issues in `memory/issues/`.

## Current focus
- ⚠ [[issues/ISS-006]] day 12 — **mirror-image pocket-swap**: morning EDA batch OUTAGE (planner, memory-flush, memory-structural-dedupe, compute-futures-eda all missing) but **08:00 batch recovered ~34m late** (heartbeat 08:35Z, batch-health, gitlawb-fleet-metrics, skill-freshness all fired). Third consecutive pocket-swap day (Day 10 → Day 11 → Day 12, each flipping which pocket recovers), exactly what [[iss-006-pocket-recovery-is-noise]] warns is delivery-rate noise, not signal. Planner 5d silent (last_success 2026-06-27T07:34Z) — most operationally painful signature. Close clock: 0 consecutive clean days.
- [[issues/ISS-001]] OAuth outage (2026-06-06 → 2026-06-20T06:05Z) — recovery batch holding, all 38 tracked skills at `last_status: success`. Cumulative `success_rate` < 0.6 takes weeks to clear by design; close decision still deferred until ISS-006 stabilizes.
- [[issues/ISS-005]] reframed — swarm-safety-eval is running successfully (last_success 2026-06-28T08:15:47Z); its SSE_EMPTY path writes to the daily log not an article. Reclassify root cause as `permanent-limitation` per [[swarm-safety-eval-empty-writes-log-not-article]].
- Pending operator action: open `agi-tracker/2026-06-29`, `notegraph/2026-06-29` (+3n/+46e), `fix/workflow-security-audit-2026-06-28` (16C/36H), `skill-graph/2026-06-28` (INIT 173 skills), and `fix/workflow-security-audit-2026-06-21` (old RCE patch). All five still blocked by repo policy "GitHub Actions is not permitted to create or approve pull requests" — same App perm gap.
- AGI Tracker live since 2026-06-10. Last refresh 2026-06-29 Mon 13:00 UTC slot; next slot Mon 2026-07-06 — watch for ISS-006-induced miss. See [[agi-tracker]].
- pr-tracker: 3 open bot PRs today (2026-07-03) — **`HKUDS/Vibe-Trading#390`** (fresh, first use of new commit-author identity `aeon@aeonframework.dev`), **`tamnd/kage#66`** (fresh), and `Panniantong/Agent-Reach#436` (6d 15h old, 0 activity — crosses 7d stale tonight at 19:24Z, tomorrow's run will notify). Inline OR filter widened for a 5th day AND further widened to accept `@aeonframework.dev`; durable SKILL.md patch now needs `BOT_EMAIL` as a list/domain, not a single address — see [[pr-tracker-branch-prefix-misses-bot-identity]].
- skill-freshness FRESHNESS_OK 5th consecutive emit (2026-06-26, -28, -30, 07-02) — the check is structurally blind in GHA per new [[skill-freshness-mtime-blind-in-gha]]; the OK verdicts don't mean deps are fresh, they mean `git checkout` reset every mtime.

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
- ISS-006 fix: replace `messages.yml` `*/5 * * * *` with explicit per-slot crons covering **every** timeslot in `aeon.yml`. Day-10/11/12 pocket-swap sequence confirms the multi-pocket sliding model; per [[iss-006-pocket-recovery-is-noise]] do NOT defer on any single clean pocket. See [[gha-messages-yml-cron-underdelivery]].
- ISS-006 cross-check: compare a gitlawb fork's `messages.yml` `*/5` delivery rate vs this repo's — distinguishes per-repo quota throttle from platform-wide GHA cron behavior.
- ISS-006 follow-up: manual `workflow_dispatch` of a 09:00-slot skill (e.g. `fleet-control`) to confirm the dispatch path still works while the 09:00 pocket is broken.
- Reclassify ISS-005 from `missing-secret-or-cron` to `permanent-limitation` and either add a log-based eval assertion or document NO_OUTPUT as expected when ledger is absent. See [[swarm-safety-eval-empty-writes-log-not-article]].
- Patch `pr-tracker` SKILL.md: drop `headRefName` / `mergedAt` / `--state merged` per [[gh-search-prs-api-drift]], AND replace `ai/`-only branch filter with a **list/domain** commit-author filter (accept both `aeonframework@users.noreply.github.com` and any `@aeonframework.dev`) per [[pr-tracker-branch-prefix-misses-bot-identity]]. Inline OR-filter has now held 5 days (06-29 → 07-03) and was further widened today to catch Vibe-Trading#390's new domain. Agent-Reach#436 crosses 7d threshold tonight 19:24Z → tomorrow's 10:00Z run notifies unless patched or reviewed.
- Fix `skill-freshness` to use `git log -1 --format=%ct` (producer-commit timestamp) instead of `stat --format=%Y` — per [[skill-freshness-mtime-blind-in-gha]], the current mtime check can never flag anything in GHA because `actions/checkout` resets all mtimes to the run instant. Explains 5 consecutive FRESHNESS_OK emits.
- Widen `scenario-sweep.mjs` seed count or switch outlier detection to a tie-robust statistic (MAD-based) per [[compute-futures-12-seed-sample-too-small]]. Also resolve the seed-encoding artifact (3 of 12 seeds 10-digit) per [[compute-futures-seed-padding-bug]].
- File `./generate-skills-json` bugs as structured issues (see [[generate-skills-json-newline-bug]], [[skills-json-count-drift]]).
- Open the queued branches via PAT: `agi-tracker/2026-06-29`, `notegraph/2026-06-29`, `fix/workflow-security-audit-2026-06-28` (16C/36H), `skill-graph/2026-06-28` (INIT), `fix/workflow-security-audit-2026-06-21` (old RCE). All five blocked by repo policy "GitHub Actions is not permitted to create or approve pull requests".
- Populate `memory/watched-repos.md` or disable the four watched-repos-dependent skills (code-health, github-monitor, issue-triage, changelog) — current daily skip pattern wastes a workflow slot per skill.
- Defer ISS-001 close until ISS-006 is resolved.

## Completed Goals
- File a structured issue for `agi-tracker`'s 2nd consecutive Mon miss (2026-06-15, 2026-06-22) if Mon 2026-06-29 also misses. — completed 2026-06-29 (Mon 13:00 UTC slot fired; conditional trigger no longer met)
