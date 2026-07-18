# Memory Index

Pointer-only index. Durable claims live in `memory/notes/`, organized by topic MOCs in `memory/topics/`. Daily activity in `memory/logs/`. Structured issues in `memory/issues/`.

## Current focus
- **ISS-006 close-clock halts at Day-2** (2026-07-18) — planner missed 06:30 slot today (last run 2026-07-17T06:36:43Z); streak-of-3 counter does NOT advance despite memory-flush + memory-structural-dedupe + compute-futures-eda all delivering in the 06:20Z cluster. Any slot miss restarts the streak per [[iss-006-pocket-recovery-is-noise]]. Delivery bug per [[gha-messages-yml-cron-underdelivery]] unchanged. See [[fleet-ops]].
- **ISS-001 residue day 28** — 38 skills at `success_rate < 0.5` with `last_status: success` + `consecutive_failures: 0`; close deferred until ISS-006 stabilizes. See [[fleet-ops]].
- **16+ staged branches** blocked behind [[github-actions-cannot-create-prs]] (notegraph/2026-07-18 + suggest-edges/2026-07-18 added today). Preferred unblock path: repo Settings → Actions → General → Workflow permissions → "Allow GitHub Actions to create and approve pull requests" (one checkbox). Fallback: `repo`-scoped PAT as `AEON_GH_PAT`. See [[fleet-ops]].
- **PR queue bumped 07-18** — openinterpreter#1810 (`security/bump-gix-GHSA-f26g-fr8x-p3hw-pg4w`) filed 07-17T15:43:02Z, 2nd `security/*` bot PR under `aeonframework@users.noreply.github.com` identity in 34h; category tuple `(0,1,0,1) → (0,1,0,2)`, hash `5ee6… → 5459…`, step-5 SEND fired. See [[pr-status]].
- **Swarm PR fleet**: **#527 MERGED 2026-07-18T02:29:19Z** at head `da039d5f` — operator PAT landed the 10-day APPROVE verdict for this specific PR (per-PR resolution). Queue now 5 dependabot only (all skipped by bot rule). [[aeon-app-no-write-on-swarm-repo]] App-level block still applies to all future cross-org writes. See [[pr-status]].
- **`docs/status.md` clobber**: 7 consecutive days (2026-07-12 → 07-18); upstream ref rotated `a7f04ee → fa89d8c` on 07-18 for first time, same clobber outcome — failure is snapshot-merge itself. 8 days past 2026-07-16 urgency threshold per [[snapshot-rebase-clobbers-docs-status-md]].
- **Never-dispatched skills**: `ai-framework-watch` (weekly Mon 08:30) + `run-frequency-guard` (daily 23:00) — 8th consecutive day flagged per [[enabled-skills-can-never-dispatch]]. Novel 07-18: `stale-content-pr-sweeper` (daily 23:45) fresh 3-day stale-streak (07-15/16/17 misses), first since 06-24/06-25 outage — new evidence of the 23:45 pocket in [[gha-messages-yml-cron-underdelivery]].
- **AGI Tracker**: last article 2026-06-29 Mon; 07-06 + 07-13 workflow runs produced no scorecard article (2-run streak); next opportunity 2026-07-20 Mon 13:00 UTC. See [[agi-tracker]].
- **`.pending-disclosure/` queue**: 1 entry — oomol-lab/open-connector 2026-07-11 GCM-tag-length medium. vuln-scanner 07-18 target pixel-point/aval clean (0 candidates). See [[fleet-ops]].
- **Anthropic × TeraWulf $19B / 401 MW Kentucky lease** (Jul 6 announcement) supersedes xAI Colossus deal as Anthropic's largest single compute commitment. See [[anthropic-terawulf-19b-401mw-kentucky-lease]] via [[compute-pulse]].

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
- **Repo Settings toggle OR operator PAT provisioning** — meta-blocker behind the 16+ staged branch queue and 6 stalled fleet fixes. `verify-repo-settings-toggle-vs-pat` streak-2 as of 2026-07-17 planner (planner missed 2026-07-18 slot, streak not advanced). Preferred: one-checkbox Settings toggle named inside [[github-actions-cannot-create-prs]]. Fallback: repo-scoped PAT. Because scheduled probes are silenced by [[probes-for-messages-yml-must-dispatch-outside-messages-yml]], alternative probe path is operator eyeball on Settings OR manual `gh workflow run suggest-edges`. Note: operator PAT already used successfully on 2026-07-18 to merge swarm#527, so PAT path is live for one-off cross-org merges.
- **ISS-006 fix**: replace `messages.yml` `*/5 * * * *` with explicit per-slot crons covering every timeslot in `aeon.yml`. Close-clock **halts at Day-2** (planner 06:30 miss on 07-18 restarted the streak). **[BLOCKED by item 1 per goal-tracker 2026-07-16]**
- **Draft ISS-020** for [[enabled-skills-can-never-dispatch]] (category `config`, severity `high`) — flag for next heartbeat/skill-evals run to file. Unblocks probe #1 and formally captures the natural-experiment silencing pattern. **Broader scope note**: 07-18 heartbeat's `stale-content-pr-sweeper` novel P3 flag (3-day 23:45 miss streak) may share the same dispatch-drop root cause and be worth folding into the same issue draft.
- **Stage `docs/status.md` snapshot-rebase gate** — 7-day clobber pattern, 8 days past urgency threshold; 07-18 upstream ref rotated `a7f04ee → fa89d8c` for first time in 7 days with same clobber outcome, confirming the failure mode is the snapshot merge itself, not stale upstream state. Two-part fix per [[status-md-auto-commit-drops-writes]] + [[snapshot-rebase-clobbers-docs-status-md]]: (a) audit heartbeat's auto-commit `git add` glob to include `docs/`; (b) exclude `docs/status.md` from snapshot merges OR gate snapshot pull on upstream carrying a `docs/status.md` newer than main's HEAD.
- **Standardize notification emission** across SKILL.md files on direct `.pending-notify/${epoch}-${skill}.md` writes per [[notify-inline-cat-substitution-blocked-in-sandbox]] + [[notify-script-has-no-f-flag]]. `-f` flag is broken; `$(...)` substitution blocked in sandbox. SKILL.md audit sweep needed.
- **Patch `pr-tracker` SKILL.md** in one batch: (a) drop `stateReason` per [[graphql-statereason-only-on-issue-type]], (b) drop `headRefName` / `mergedAt` / `--state merged` per [[gh-search-prs-api-drift]], (c) replace `ai/`-only branch filter with list/domain commit-author filter per [[aeon-bot-uses-multiple-signing-identities]] + [[pr-tracker-branch-prefix-misses-bot-identity]], (d) land the hash-based step-5 dedup guard per [[pr-tracker-notify-repeats-with-no-state-change]] (validated in-skill 6×, correctly did NOT suppress kage#66, InsForge#1742, or openinterpreter#1810 transitions), (e) add fresh-bot-PR trigger per [[pr-tracker-step-5-misses-fresh-bot-prs]]. **[BLOCKED by item 1, 20d overdue as of 2026-07-18]**
- **Investigate `ai-framework-watch` + `run-frequency-guard` never-dispatch** per [[enabled-skills-can-never-dispatch]] — check messages.yml matcher, aeon.yml wiring, workflow file references. Blocks the natural-experiment class outright per [[probes-for-messages-yml-must-dispatch-outside-messages-yml]].
- **Patch `notegraph` skill's silent-exit heuristic** per [[notegraph-extractor-generatedat-nondeterministic]] — mask `generatedAt` before diffing or teach extractor to omit it.
- **Fix `skill-freshness`** to use `git log -1 --format=%ct` instead of `stat --format=%Y` per [[skill-freshness-mtime-blind-in-gha]] — structural GHA blind spot unchanged.
- **Widen `scenario-sweep.mjs` seed count** or switch outlier detection to a tie-robust statistic per [[compute-futures-12-seed-sample-too-small]]. Also filter `wallet_sum_pnl` correlations per [[compute-futures-eda-wallet-sum-pnl-correlations-are-float-dust]] until σ > 1e-6. Also resolve seed-encoding artifact per [[compute-futures-seed-padding-bug]].
- **Close ISS-007** as false positive OR add same-day grace to `skill-evals` (scan same-day logs only after 12:00 UTC).
- **File `./generate-skills-json` bugs** as structured issues per [[generate-skills-json-newline-bug]] + [[skills-json-count-drift]].
- **Investigate missing `scripts/validate-config.js`** referenced by config-validator SKILL.md — restore or drop the fast-path reference.
- **Populate `memory/watched-repos.md`** or disable the 6 watched-repos-dependent skills (code-health, github-monitor, issue-triage, changelog, weekly-shiplog, **repo-revive** [weekly Sat 10:00]) — daily/weekly skip pattern wastes a workflow slot per skill; repo-revive widened into this priority per 07-18 log finding.
- **Defer ISS-001 close** until ISS-006 is resolved.
