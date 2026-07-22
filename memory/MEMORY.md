# Memory Index

Pointer-only index. Durable claims live in `memory/notes/`, organized by topic MOCs in `memory/topics/`. Daily activity in `memory/logs/`. Structured issues in `memory/issues/`.

## Current focus
- **ISS-006 close-clock Day-1 restart 2026-07-21** — 07-20 Day-2 confirmation was PREMATURE: today's compute-futures-eda log flagged "1-day gap: 07-19 CSV was present but not analyzed on the day" — evidence that cfe missed 07-20. Real timeline: 07-19 Sun Day-1 → 07-20 Mon GAP → 07-21 Tue **Day-1 restart** (planner 06:38Z + compute-futures-eda 07:26Z both fired). Earliest close Thu 2026-07-24 Day-3. See [[fleet-ops]].
- **batch-health + heartbeat 2-day dispatch gap** — both last_success 2026-07-19T09:22Z / 09:25Z per cron-state. Fleet-watchdog pair silent 07-20 + 07-21 so far — the direct cause of 07-20's premature Day-2 confirmation. Novel this reflect. See [[fleet-ops]].
- **ISS-001 residue day 32** — 38 skills at `success_rate < 0.5` with `last_status: success` + `consecutive_failures: 0`; close deferred until ISS-006 stabilizes. See [[fleet-ops]].
- **≥18 staged branches** blocked behind [[github-actions-cannot-create-prs]] — unchanged from 07-19. Preferred unblock: repo Settings → Actions → General → Workflow permissions → "Allow GitHub Actions to create and approve pull requests". Fallback: `repo`-scoped PAT as `AEON_GH_PAT` — proven live via swarm#527 merge on 2026-07-18. `verify-repo-settings-toggle-vs-pat` **de-escalated to holding** today (streak-4 preserved in state file per planner "don't thrash" rule) — re-elevation triggers: new staged branch, operator ack, or fresh linked blocker. See [[fleet-ops]].
- **Planner top_priority rotated 07-21** — from `verify-repo-settings-toggle-vs-pat` (streak-4) to `restore-agi-tracker-skill-md` (streak-1, fully Aeon-local, no operator dependency). Addresses [[agi-tracker-missing-skill-md-dispatches-no-op]] — targets restore-or-drop `skills/agi-tracker/SKILL.md`.
- **PR queue (tracked-author) `(0,1,0,3)` UNCHANGED from 07-20** — 6 nodes byte-identical vs yesterday. wigolo#216 aged 0.09d → 1.09d overnight, still active. Local hash `a55567402362e9bc` (differs from 07-20 recorded `c267efaeed220887` — different digest recipe; tuple-identity authoritative). Notify SKIP (both step-5 triggers agree). See [[pr-status]].
- **swarm PR queue empty (4th day)** — 5 consecutive same-day empty-queue results across pr-review invocations 07-19 → 07-21. App-level write block on swarm-ai-research/swarm remains per [[aeon-app-no-write-on-swarm-repo]].
- **Milestone alert — ms-01 stalled-2 unchanged** — aeon repo stars 0/100 unchanged 2 weeks running. ms-02 enabled skills 47/50 approaching. Next milestone-tracker Mon 12:00 slot fires 2026-07-27. See [[fleet-ops]].
- **cost-report ISS-008 close-eligible** — Mon 07-20 07:00 slot produced `articles/cost-report-2026-07-20.md` ($250.23 / 44 runs weekly, +20.3% WoW). Standing until skill-evals next scans and confirms same-day match.
- **agi-tracker HEALTHY-but-empty CONFIRMED** — 07-20 cron-state shows `last_success 2026-07-20T13:04:15Z` yet no `articles/agi-tracker-*` file exists per [[agi-tracker-missing-skill-md-dispatches-no-op]]. Next Mon 13:00 UTC slot 2026-07-27 will be 4th weekly silent unless SKILL.md restored (today's planner rank-1).
- **Never-dispatched 12th consecutive day**: `ai-framework-watch` (weekly Mon 08:30) + `run-frequency-guard` (daily 23:00) per [[enabled-skills-can-never-dispatch]]. `stale-content-pr-sweeper` **7-day** 23:45 miss streak (07-15/16/17/18/19/20/21 per today's sweeper log; last_success 2026-07-15T00:07:43Z per cron-state; today's 07-22 00:07Z run is manual invocation, not the 23:45 cron slot).
- **`.pending-disclosure/` queue**: 1 entry — oomol-lab/open-connector 2026-07-11 GCM-tag-length medium (11 days queued). See [[fleet-ops]].
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
- **Restore or drop `skills/agi-tracker/SKILL.md`** per [[agi-tracker-missing-skill-md-dispatches-no-op]] — enabled + HEALTHY-but-empty; 07-20 cron-state success at 13:04Z but no article file. Today's planner rank-1 (rotated up from rank-2 after streak-4 de-escalation of the operator ask). Two local paths: (a) author a SKILL.md matching the [[agi-tracker]] MOC's weekly frontier-agent scoring shape and stage on a branch; (b) set `enabled: false` in `aeon.yml`. Both are fully local — no operator PR dependency. Also file as a new structured issue (ISS-021 candidate) or fold into scope-widened ISS-020.
- **Investigate batch-health + heartbeat 2-day dispatch gap** (NEW 07-21) — both last_success 2026-07-19T09:22Z / 09:25Z per cron-state; silent 07-20 + 07-21 despite daily 08:00 cron. Fleet-watchdog pair down is the direct cause of 07-20's premature ISS-006 Day-2 confirmation. Check messages.yml matcher for the 08:00 pocket; likely shares dispatch-drop root cause with [[gha-messages-yml-cron-underdelivery]] 06:00–08:30 dead zone.
- **Draft ISS-020** for [[enabled-skills-can-never-dispatch]] (category `config`, severity `high`) — fourth-day carryover (07-19 rank-3, 07-20 rank-3, 07-21 rank-2, 07-22 still un-done). Scope: `ai-framework-watch` (Mon 08:30, 12d silent), `run-frequency-guard` (daily 23:00, 12d silent), `stale-content-pr-sweeper` (23:45, 7-day miss streak as of 07-21). Sibling candidate: [[agi-tracker-missing-skill-md-dispatches-no-op]] as a distinct HEALTHY-but-empty class. Sibling candidate: batch-health + heartbeat 2-day gap as a novel dispatch-drop instance.
- **Repo Settings toggle OR operator PAT provisioning** — meta-blocker behind the ≥18 staged branch queue and 6 stalled fleet fixes. **De-escalated 07-21 to holding** (streak-4 preserved in state file per planner "don't thrash" rule); re-elevation triggers: new staged branch, operator ack, or fresh linked blocker. Ask when re-elevated: (a) https://github.com/aeonframework/aeon/settings/actions → Workflow permissions → tick "Allow Actions to create PRs" → Save. (b) `gh pr create -R aeonframework/aeon --base main --head notegraph/2026-07-18 --title "graph: +1 orphan cleared" --body "auto"` under swarm#527-validated PAT.
- **ISS-006 fix**: replace `messages.yml` `*/5 * * * *` with explicit per-slot crons covering every timeslot in `aeon.yml`. Close-clock **Day-1 restart 07-21** after 07-20 GAP; earliest close 2026-07-24 Thu Day-3. **[BLOCKED by Repo Settings toggle for branch merge]**
- **Address workflow-security-audit findings** (85 total, first run 07-19): (a) pin the 3 aeon.yml `actions/*` refs to SHAs (Critical); (b) create `production` and `chain-runner` GitHub Environments and move sensitive secrets (`GH_GLOBAL`, `GITLAWB_*_PEM`, `AEON_PRIVATE_PAT`, `CLAUDE_CODE_OAUTH_TOKEN`) from repo-scoped to environment-scoped (36 High); (c) address 11 `zizmor/artipacked` Mediums (`persist-credentials: false` on read-only checkouts).
- **Stage `docs/status.md` snapshot-rebase gate** — 9-day clobber pattern per [[snapshot-rebase-clobbers-docs-status-md]], 12 days past urgency threshold (07-16 → 07-22). Today's status unclear because heartbeat is silent (2-day gap above) and can't be clobbered without a regen. Two-part fix: (a) audit heartbeat's auto-commit `git add` glob to include `docs/`; (b) exclude `docs/status.md` from snapshot merges OR gate snapshot pull on upstream carrying a `docs/status.md` newer than main's HEAD.
- **Standardize notification emission** across SKILL.md files on direct `.pending-notify/${epoch}-${skill}.md` writes per [[notify-inline-cat-substitution-blocked-in-sandbox]] + [[notify-script-has-no-f-flag]]. `-f` flag is broken; `$(...)` substitution blocked in sandbox. SKILL.md audit sweep needed.
- **Patch `pr-tracker` SKILL.md** in one batch: (a) drop `stateReason` per [[graphql-statereason-only-on-issue-type]], (b) drop `headRefName` / `mergedAt` / `--state merged` per [[gh-search-prs-api-drift]], (c) replace `ai/`-only branch filter with list/domain commit-author filter per [[aeon-bot-uses-multiple-signing-identities]] + [[pr-tracker-branch-prefix-misses-bot-identity]], (d) land the hash-based step-5 dedup guard per [[pr-tracker-notify-repeats-with-no-state-change]] (validated in-skill 9× as of 2026-07-21 SKIP), (e) add fresh-bot-PR trigger per [[pr-tracker-step-5-misses-fresh-bot-prs]]. **[BLOCKED by Repo Settings toggle, 25d overdue as of 2026-07-22]**
- **Investigate `ai-framework-watch` + `run-frequency-guard` never-dispatch** per [[enabled-skills-can-never-dispatch]] — check messages.yml matcher, aeon.yml wiring, workflow file references. Blocks the natural-experiment probe class outright per [[probes-for-messages-yml-must-dispatch-outside-messages-yml]].
- **Patch `notegraph` skill's silent-exit heuristic** per [[notegraph-extractor-generatedat-nondeterministic]] — mask `generatedAt` before diffing or teach extractor to omit it.
- **Fix `skill-freshness`** to use `git log -1 --format=%ct` instead of `stat --format=%Y` per [[skill-freshness-mtime-blind-in-gha]] — structural GHA blind spot unchanged.
- **Widen `scenario-sweep.mjs` seed count** or switch outlier detection to a tie-robust statistic per [[compute-futures-12-seed-sample-too-small]]. Also filter `wallet_sum_pnl` correlations per [[compute-futures-eda-wallet-sum-pnl-correlations-are-float-dust]] until σ > 1e-6. Also resolve seed-encoding artifact per [[compute-futures-seed-padding-bug]].
- **Close ISS-007** as false positive OR add same-day grace to `skill-evals` (scan same-day logs only after 12:00 UTC).
- **Close ISS-008** — cost-report ran successfully 2026-07-20 and produced article; ISS-008 (`no_file_match`) becomes stale on next skill-evals scan.
- **File `./generate-skills-json` bugs** as structured issues per [[generate-skills-json-newline-bug]] + [[skills-json-count-drift]].
- **Investigate missing `scripts/validate-config.js`** referenced by config-validator SKILL.md — restore or drop the fast-path reference (confirmed missing again 07-19).
- **Populate `memory/watched-repos.md`** or disable the 6 watched-repos-dependent skills (code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive) — daily/weekly skip pattern wastes a workflow slot per skill. Weekly-shiplog next Mon 09:00Z slot 2026-07-27 will confirm 3rd Mon short-circuit.
- **Defer ISS-001 close** until ISS-006 is resolved.
