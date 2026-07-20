# Memory Index

Pointer-only index. Durable claims live in `memory/notes/`, organized by topic MOCs in `memory/topics/`. Daily activity in `memory/logs/`. Structured issues in `memory/issues/`.

## Current focus
- **ISS-006 close-clock restarts at Day-1** (2026-07-19) — Sun odd-DOM pocket delivered all 5 expected skills in a 12-second window at 07:14:49–07:15:01Z (planner, compute-macro-correlate, compute-futures-eda, config-validator, skillpacks). Memory-hygiene pair not eligible on odd-DOM. Streak fresh count after 07-18 miss per [[iss-006-pocket-recovery-is-noise]]; earliest close 2026-07-21 Mon Day-3. See [[fleet-ops]].
- **ISS-001 residue day 30** — 38 skills at `success_rate < 0.5` with `last_status: success` + `consecutive_failures: 0`; close deferred until ISS-006 stabilizes. See [[fleet-ops]].
- **≥18 staged branches** blocked behind [[github-actions-cannot-create-prs]] — today added `compute-macro/2026-07-19` (17th), `skillpacks/2026-07-19` (18th), `fix/workflow-security-audit-2026-07-19` (versioned; `fix/workflow-security-audit` already existed from 2026-06-20 audit). Preferred unblock: repo Settings → Actions → General → Workflow permissions → "Allow GitHub Actions to create and approve pull requests". Fallback: `repo`-scoped PAT as `AEON_GH_PAT` — proven live via swarm#527 merge on 2026-07-18. See [[fleet-ops]].
- **PR queue (tracked-author) UNCHANGED** — category tuple `(0,1,0,2)` byte-for-byte identical to 2026-07-18; hash-dedup blocked step-5 notify (first SKIP since 2026-07-16, ends 2-day SEND streak). See [[pr-status]].
- **swarm PR queue empty** — 5 dependabot PRs (#524/#529/#530/#532/#533) merged in the 02:02–22:03Z window between 07-18 and 07-19, first cross-org batch-merge since [[aeon-app-no-write-on-swarm-repo]] block ended on swarm#527 per-PR on 07-18. App-level write block on swarm-ai-research/swarm remains for future PRs.
- **workflow-security-audit BOOTSTRAP** — first ever run: 85 findings (3C / 36H / 15M / 31L), 3 Critical `zizmor/unpinned-uses` in aeon.yml (checkout@v5 ×2, setup-node@v5), 36 High `zizmor/secrets-outside-env`. Report: `articles/workflow-security-audit-2026-07-19.md`. All Critical/High flagged Manual (SHA verification + env-topology are operator decisions). See [[fleet-ops]].
- **skill-evals BOOTSTRAP** — first run: 13 NEW_FAIL / 0 fixed, coverage 14/49 (28%), 10 of 13 failing skills are disabled/workflow_dispatch (no output expected — eval regex needs same-day grace or disabled-skill skip). Article: `articles/skill-evals-2026-07-19.md`.
- **compute-macro-correlate first run** — Track A DePIN proxy (RENDER/TAO/IO × 13 macros): all null at n=137, |ρ|<0.15 threshold; Track B sweep P&L: n=28 deferring (need 30, expected next 1-2 weekly runs). First snapshot in `memory/topics/compute-futures-macro-correlations.md`.
- **skillpacks structural churn** — new pack `outages-fleet` (18 members, persisted 2nd consecutive run) formed from dissolved `fleet-evolve`; `batch-health` moved from `monitor-movers` to `outages-fleet`, signaling outage/repair vocabulary has densified enough this fortnight to dominate.
- **compute-futures-eda basket `maxCurve`** — third consecutive strengthening run (07-16 8.33% → 07-17 16.67% → 07-18 33.33% outlier_pct), first (mode, column) pair to persist AND strengthen 3× in a row.
- **Never-dispatched skills 9th consecutive day**: `ai-framework-watch` (weekly Mon 08:30) + `run-frequency-guard` (daily 23:00) per [[enabled-skills-can-never-dispatch]]. `stale-content-pr-sweeper` (daily 23:45) 5-day stale-streak (07-15/16/17/18/19 missed per cron-state `last_dispatch: 2026-07-15T00:06:10Z`, extends yesterday's 4-day flag by one day) — same 23:45 pocket documented in [[gha-messages-yml-cron-underdelivery]].
- **`docs/status.md` clobber** — 8-day pattern per [[snapshot-rebase-clobbers-docs-status-md]], 07-19 heartbeat regenerated at 09:21Z; 07-20 snapshot clobbered again at 07:17:47Z (`3d18558`, upstream ref `fa89d8c` unchanged from 07-19 — 2nd day on this ref). 10 days past 2026-07-16 mitigation urgency threshold.
- **AGI Tracker** — last article 2026-06-29 Mon; 07-06 + 07-13 workflow runs produced no scorecard article (2-run streak); next opportunity **today** 2026-07-20 Mon 13:00 UTC. See [[agi-tracker]].
- **`.pending-disclosure/` queue**: 1 entry — oomol-lab/open-connector 2026-07-11 GCM-tag-length medium. See [[fleet-ops]].
- **Anthropic × TeraWulf $19B / 401 MW Kentucky lease** (Jul 6 announcement) supersedes xAI Colossus deal as Anthropic's largest single compute commitment. See [[anthropic-terawulf-19b-401mw-kentucky-lease]] via [[compute-pulse]].

## Topics
- [[agi-tracker]] — frontier-agent capability tracking + Aschenbrenner *Situational Awareness* scoring
- [[fleet-ops]] — OAuth outage, morning-batch silence, monitor/repair coupling, GitHub App perms, workflow-security-audit BOOTSTRAP
- [[compute-pulse]] — inference pricing, hardware deals, DePIN tokens (weekly snapshot)
- [[surplus-pulse]] — surplus-mode pricing simulator runs
- [[pr-status]] — cross-repo PR queue for the aeonframework author

*Note: `memory/topics/compute-futures-macro-correlations.md` was authored by the compute-macro-correlate skill on branch `compute-macro/2026-07-19` today; not yet on main due to [[github-actions-cannot-create-prs]]. Add to Topics list when the branch merges.*

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
- **Repo Settings toggle OR operator PAT provisioning** — meta-blocker behind the ≥18 staged branch queue and 6 stalled fleet fixes. `verify-repo-settings-toggle-vs-pat` streak-3 as of 2026-07-19 planner. Preferred: one-checkbox Settings toggle named inside [[github-actions-cannot-create-prs]]. Fallback: repo-scoped PAT (proven live via swarm#527 07-18 merge). Today's planner reframed the ask as a concrete smoke test — operator run the swarm#527-validated PAT against `notegraph/2026-07-18` (trivial +1-node diff) to prove PAT scope covers in-repo `gh pr create` + merge (three-way outcome map, all valuable).
- **ISS-006 fix**: replace `messages.yml` `*/5 * * * *` with explicit per-slot crons covering every timeslot in `aeon.yml`. Close-clock **Day-1 restored** 07-19 after 07-18 planner miss; earliest close 2026-07-21 Mon assuming 07-19 + 07-20 + 07-21 all clean. **[BLOCKED by item 1 per goal-tracker 2026-07-16]**
- **Draft ISS-020** for [[enabled-skills-can-never-dispatch]] (category `config`, severity `high`) — scope-widened to include 07-18's `stale-content-pr-sweeper` novel P3 flag (now 4-day 23:45 miss streak) as broadened dispatch-drop category. Flag for next heartbeat/skill-evals run to file. Unblocks probe #1 and formally captures the natural-experiment silencing pattern.
- **Address workflow-security-audit findings** (85 total, first run): (a) pin the 3 aeon.yml `actions/*` refs to SHAs (Critical); (b) create `production` and `chain-runner` GitHub Environments and move sensitive secrets (`GH_GLOBAL`, `GITLAWB_*_PEM`, `AEON_PRIVATE_PAT`, `CLAUDE_CODE_OAUTH_TOKEN`) from repo-scoped to environment-scoped (36 High); (c) address 11 `zizmor/artipacked` Mediums (`persist-credentials: false` on read-only checkouts).
- **Stage `docs/status.md` snapshot-rebase gate** — 7-day clobber pattern per [[snapshot-rebase-clobbers-docs-status-md]], 9 days past urgency threshold. Two-part fix: (a) audit heartbeat's auto-commit `git add` glob to include `docs/`; (b) exclude `docs/status.md` from snapshot merges OR gate snapshot pull on upstream carrying a `docs/status.md` newer than main's HEAD.
- **Standardize notification emission** across SKILL.md files on direct `.pending-notify/${epoch}-${skill}.md` writes per [[notify-inline-cat-substitution-blocked-in-sandbox]] + [[notify-script-has-no-f-flag]]. `-f` flag is broken; `$(...)` substitution blocked in sandbox. SKILL.md audit sweep needed.
- **Patch `pr-tracker` SKILL.md** in one batch: (a) drop `stateReason` per [[graphql-statereason-only-on-issue-type]], (b) drop `headRefName` / `mergedAt` / `--state merged` per [[gh-search-prs-api-drift]], (c) replace `ai/`-only branch filter with list/domain commit-author filter per [[aeon-bot-uses-multiple-signing-identities]] + [[pr-tracker-branch-prefix-misses-bot-identity]], (d) land the hash-based step-5 dedup guard per [[pr-tracker-notify-repeats-with-no-state-change]] (validated in-skill 7× as of 2026-07-19 SKIP), (e) add fresh-bot-PR trigger per [[pr-tracker-step-5-misses-fresh-bot-prs]]. **[BLOCKED by item 1, 21d overdue as of 2026-07-19]**
- **Investigate `ai-framework-watch` + `run-frequency-guard` never-dispatch** per [[enabled-skills-can-never-dispatch]] — check messages.yml matcher, aeon.yml wiring, workflow file references. Blocks the natural-experiment probe class outright per [[probes-for-messages-yml-must-dispatch-outside-messages-yml]].
- **Patch `notegraph` skill's silent-exit heuristic** per [[notegraph-extractor-generatedat-nondeterministic]] — mask `generatedAt` before diffing or teach extractor to omit it.
- **Fix `skill-freshness`** to use `git log -1 --format=%ct` instead of `stat --format=%Y` per [[skill-freshness-mtime-blind-in-gha]] — structural GHA blind spot unchanged.
- **Widen `scenario-sweep.mjs` seed count** or switch outlier detection to a tie-robust statistic per [[compute-futures-12-seed-sample-too-small]]. Also filter `wallet_sum_pnl` correlations per [[compute-futures-eda-wallet-sum-pnl-correlations-are-float-dust]] until σ > 1e-6. Also resolve seed-encoding artifact per [[compute-futures-seed-padding-bug]].
- **Close ISS-007** as false positive OR add same-day grace to `skill-evals` (scan same-day logs only after 12:00 UTC).
- **File `./generate-skills-json` bugs** as structured issues per [[generate-skills-json-newline-bug]] + [[skills-json-count-drift]].
- **Investigate missing `scripts/validate-config.js`** referenced by config-validator SKILL.md — restore or drop the fast-path reference (confirmed missing again 07-19).
- **Populate `memory/watched-repos.md`** or disable the 6 watched-repos-dependent skills (code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive) — daily/weekly skip pattern wastes a workflow slot per skill.
- **Defer ISS-001 close** until ISS-006 is resolved.
