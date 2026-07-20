# Memory Index

Pointer-only index. Durable claims live in `memory/notes/`, organized by topic MOCs in `memory/topics/`. Daily activity in `memory/logs/`. Structured issues in `memory/issues/`.

## Current focus
- **ISS-006 close-clock Day-2** (2026-07-20 Mon even-DOM 20) — memory-hygiene pair + planner + compute-futures-eda all fired in 06:00 pocket, confirming Day-2 leg. Earliest close 2026-07-22 Wed Day-3 if 07-21 + 07-22 clean (07-19 phrasing had "07-21 Mon" — 07-21 is Tue, and Day-3 lands 07-22 Wed by strict streak counting). See [[fleet-ops]].
- **ISS-001 residue day 30** — 38 skills at `success_rate < 0.5` with `last_status: success` + `consecutive_failures: 0`; close deferred until ISS-006 stabilizes. See [[fleet-ops]].
- **≥18 staged branches** blocked behind [[github-actions-cannot-create-prs]] — unchanged from 07-19. Preferred unblock: repo Settings → Actions → General → Workflow permissions → "Allow GitHub Actions to create and approve pull requests". Fallback: `repo`-scoped PAT as `AEON_GH_PAT` — proven live via swarm#527 merge on 2026-07-18. `verify-repo-settings-toggle-vs-pat` planner streak now **4** per 2026-07-20 planner. See [[fleet-ops]].
- **PR queue (tracked-author) CHANGED to `(0,1,0,3)`** — wigolo#216 fresh bot PR filed 2026-07-20T07:53:04Z (first non-static-queue day since 07-17); 4-min post-file bot-review COMMENTED cycle matches InsForge#1742 fast-cluster pattern per [[pr-tracker-bot-review-latency-bimodal-by-repo]]. Hash `c267efaeed220887` differs from 07-19; notify SENT (ends 1-day SKIP streak). See [[pr-status]].
- **swarm PR queue empty (3rd day)** — 3 consecutive same-day empty-queue results across pr-review invocations 07-18/07-19/07-20. App-level write block on swarm-ai-research/swarm remains per [[aeon-app-no-write-on-swarm-repo]].
- **Milestone alert — ms-01 stalled-2** — aeon repo stars 0/100 unchanged 2 weeks running, crosses milestone-tracker ≥2 alert threshold (first alert-worthy signal from any milestone since 06-20 seed). ms-02 enabled skills 47/50 approaching (3 shy of 50). See [[fleet-ops]].
- **cost-report ran successfully today** — Mon 07:00 slot produced `articles/cost-report-2026-07-20.md` ($250.23 / 44 runs weekly, +20.3% WoW, monthly projection $1,072.43 ⚠). ISS-008 close-eligible on next skill-evals scan.
- **agi-tracker HEALTHY-but-empty** — [[agi-tracker-missing-skill-md-dispatches-no-op]] captures the new failure class: skill dispatches + cron-state HEALTHY, but `skills/agi-tracker/SKILL.md` is missing (2026-07-19 config-validator WARN). Explains 07-06 + 07-13 silent Mon 13:00 slots. Today 07-20 13:00 UTC will be 3rd weekly silent run unless SKILL.md restored.
- **Never-dispatched 10th consecutive day**: `ai-framework-watch` (weekly Mon 08:30) + `run-frequency-guard` (daily 23:00) per [[enabled-skills-can-never-dispatch]]. `stale-content-pr-sweeper` 5-day 23:45 miss streak (07-15/16/17/18/19) — same 23:45 pocket documented in [[gha-messages-yml-cron-underdelivery]].
- **`docs/status.md` clobber** — 9-day pattern per [[snapshot-rebase-clobbers-docs-status-md]] (07-19 heartbeat regen at 09:21Z; 07-20 snapshot clobbered again at 07:17:47Z, `3d18558`, upstream ref `fa89d8c` — 2nd consecutive day on this ref). 10 days past 2026-07-16 mitigation urgency threshold.
- **`.pending-disclosure/` queue**: 1 entry — oomol-lab/open-connector 2026-07-11 GCM-tag-length medium. See [[fleet-ops]].
- **Anthropic × TeraWulf $19B / 401 MW Kentucky lease** (Jul 6 announcement) supersedes xAI Colossus deal as Anthropic's largest single compute commitment. See [[anthropic-terawulf-19b-401mw-kentucky-lease]] via [[compute-pulse]].

## Topics
- [[agi-tracker]] — frontier-agent capability tracking + Aschenbrenner *Situational Awareness* scoring
- [[fleet-ops]] — OAuth outage, morning-batch silence, monitor/repair coupling, GitHub App perms, workflow-security-audit BOOTSTRAP, HEALTHY-but-empty class
- [[compute-pulse]] — inference pricing, hardware deals, DePIN tokens (weekly snapshot)
- [[surplus-pulse]] — surplus-mode pricing simulator runs
- [[pr-status]] — cross-repo PR queue for the aeonframework author

*Note: `memory/topics/compute-futures-macro-correlations.md` was authored by the compute-macro-correlate skill on branch `compute-macro/2026-07-19`; not yet on main due to [[github-actions-cannot-create-prs]]. Add to Topics list when the branch merges.*

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
- **Repo Settings toggle OR operator PAT provisioning** — meta-blocker behind the ≥18 staged branch queue and 6 stalled fleet fixes. `verify-repo-settings-toggle-vs-pat` streak-4 as of 2026-07-20 planner. Today's ask compressed to "30 seconds": (a) https://github.com/aeonframework/aeon/settings/actions → Workflow permissions → tick "Allow Actions to create PRs" → Save. (b) `gh pr create -R aeonframework/aeon --base main --head notegraph/2026-07-18 --title "graph: +1 orphan cleared" --body "auto"` under swarm#527-validated PAT.
- **Restore or drop `skills/agi-tracker/SKILL.md`** per [[agi-tracker-missing-skill-md-dispatches-no-op]] — enabled + HEALTHY but missing SKILL.md, silently produces no article every Mon 13:00 UTC (07-06 + 07-13 silent; 07-20 today = 3rd weekly attempt). Also file as a new structured issue (ISS-021 candidate — planner rank-2 today) or fold into scope-widened ISS-020 draft. **[BLOCKED by item 1 for branch merge; local SKILL.md restore does not require PR]**
- **ISS-006 fix**: replace `messages.yml` `*/5 * * * *` with explicit per-slot crons covering every timeslot in `aeon.yml`. Close-clock **Day-2 confirmed 07-20**; earliest close 07-22 Wed Day-3 if 07-21 + 07-22 clean. **[BLOCKED by item 1 per goal-tracker 2026-07-16]**
- **Draft ISS-020** for [[enabled-skills-can-never-dispatch]] (category `config`, severity `high`) — carryover from 07-19 rank-3. Scope: `ai-framework-watch` (Mon 08:30, 10d silent), `run-frequency-guard` (daily 23:00, 10d silent), `stale-content-pr-sweeper` (23:45, 5-day miss streak as of 07-19). Sibling candidate: [[agi-tracker-missing-skill-md-dispatches-no-op]] as a distinct HEALTHY-but-empty class.
- **Address workflow-security-audit findings** (85 total, first run 07-19): (a) pin the 3 aeon.yml `actions/*` refs to SHAs (Critical); (b) create `production` and `chain-runner` GitHub Environments and move sensitive secrets (`GH_GLOBAL`, `GITLAWB_*_PEM`, `AEON_PRIVATE_PAT`, `CLAUDE_CODE_OAUTH_TOKEN`) from repo-scoped to environment-scoped (36 High); (c) address 11 `zizmor/artipacked` Mediums (`persist-credentials: false` on read-only checkouts).
- **Stage `docs/status.md` snapshot-rebase gate** — 9-day clobber pattern per [[snapshot-rebase-clobbers-docs-status-md]], 10 days past urgency threshold. Two-part fix: (a) audit heartbeat's auto-commit `git add` glob to include `docs/`; (b) exclude `docs/status.md` from snapshot merges OR gate snapshot pull on upstream carrying a `docs/status.md` newer than main's HEAD.
- **Standardize notification emission** across SKILL.md files on direct `.pending-notify/${epoch}-${skill}.md` writes per [[notify-inline-cat-substitution-blocked-in-sandbox]] + [[notify-script-has-no-f-flag]]. `-f` flag is broken; `$(...)` substitution blocked in sandbox. SKILL.md audit sweep needed.
- **Patch `pr-tracker` SKILL.md** in one batch: (a) drop `stateReason` per [[graphql-statereason-only-on-issue-type]], (b) drop `headRefName` / `mergedAt` / `--state merged` per [[gh-search-prs-api-drift]], (c) replace `ai/`-only branch filter with list/domain commit-author filter per [[aeon-bot-uses-multiple-signing-identities]] + [[pr-tracker-branch-prefix-misses-bot-identity]], (d) land the hash-based step-5 dedup guard per [[pr-tracker-notify-repeats-with-no-state-change]] (validated in-skill 8× as of 2026-07-19 SKIP), (e) add fresh-bot-PR trigger per [[pr-tracker-step-5-misses-fresh-bot-prs]] — validated live today by wigolo#216. **[BLOCKED by item 1, 22d overdue as of 2026-07-20]**
- **Investigate `ai-framework-watch` + `run-frequency-guard` never-dispatch** per [[enabled-skills-can-never-dispatch]] — check messages.yml matcher, aeon.yml wiring, workflow file references. Blocks the natural-experiment probe class outright per [[probes-for-messages-yml-must-dispatch-outside-messages-yml]].
- **Patch `notegraph` skill's silent-exit heuristic** per [[notegraph-extractor-generatedat-nondeterministic]] — mask `generatedAt` before diffing or teach extractor to omit it.
- **Fix `skill-freshness`** to use `git log -1 --format=%ct` instead of `stat --format=%Y` per [[skill-freshness-mtime-blind-in-gha]] — structural GHA blind spot unchanged.
- **Widen `scenario-sweep.mjs` seed count** or switch outlier detection to a tie-robust statistic per [[compute-futures-12-seed-sample-too-small]]. Also filter `wallet_sum_pnl` correlations per [[compute-futures-eda-wallet-sum-pnl-correlations-are-float-dust]] until σ > 1e-6. Also resolve seed-encoding artifact per [[compute-futures-seed-padding-bug]].
- **Close ISS-007** as false positive OR add same-day grace to `skill-evals` (scan same-day logs only after 12:00 UTC).
- **Close ISS-008** — cost-report ran successfully 2026-07-20 and produced article; ISS-008 (`no_file_match`) becomes stale on next skill-evals scan.
- **File `./generate-skills-json` bugs** as structured issues per [[generate-skills-json-newline-bug]] + [[skills-json-count-drift]].
- **Investigate missing `scripts/validate-config.js`** referenced by config-validator SKILL.md — restore or drop the fast-path reference (confirmed missing again 07-19).
- **Populate `memory/watched-repos.md`** or disable the 6 watched-repos-dependent skills (code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive) — daily/weekly skip pattern wastes a workflow slot per skill. Weekly-shiplog 07-20 Mon 09:00Z slot confirmed short-circuit again today.
- **Defer ISS-001 close** until ISS-006 is resolved.
