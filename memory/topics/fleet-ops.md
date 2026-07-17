# Fleet Ops

Cross-cutting operational lessons and constraints for the Aeon fleet: credential outages, monitoring-loop hazards, GitHub App permission boundaries, dispatch architecture, and cron-state pathologies.

## Open incidents
- [[issues/ISS-001]] — CLAUDE_CODE_OAUTH_TOKEN missing 2026-06-06 → 2026-06-20T06:05Z; investigating. Close deferred while [[issues/ISS-006]] runs; recovery batch is otherwise holding. Day 27 as of 2026-07-17.
- [[issues/ISS-006]] — Day 27 (2026-07-17, Fri odd-DOM): **BATCH_HEALTH_OK 2nd consecutive day** — 06:00 pocket delivered on-cadence (planner 06:36:43Z + compute-futures-eda 06:36:47Z in same cluster, no memory-hygiene on odd DOM); 05:30 pocket also recovered on-cadence (suggest-edges 06:40:43Z + notegraph 06:42:01Z late-catch-up). Close-clock streak-of-3 counter now at Day-2 — advances to Day-3 (close) tomorrow (07-18 Sat even-DOM) if planner + compute-futures-eda + memory-hygiene pair all deliver. ISS-019 (filed 07-14) still open — INDEX.md at 17 rows.
- [[issues/ISS-007]] — heartbeat missing_pattern in eval regex; new 2026-07-05, filed by skill-evals. Enabled skill FAIL (not covered by ISS-002/005).
- [[issues/ISS-008]] — cost-report no_file_match; new 2026-07-05, filed by skill-evals. Standing ISS-006 tributary (weekly Mon 07:00 slot; 2026-07-13 slot fired ~74min late in 08:14Z catch-up cluster; next opportunity 2026-07-20).
- [[issues/ISS-005]] — swarm-safety-eval no_file_match: skill is now running successfully (last_success 2026-06-28T08:15:47Z) but its SSE_EMPTY path writes to the daily log, not an article; reclassify from `missing-secret-or-cron` to `permanent-limitation` per [[swarm-safety-eval-empty-writes-log-not-article]].
- **ISS-009 → ISS-018** (2026-07-12 BOOTSTRAP fillings from skill-evals): 10 no_file_match issues on chronically-empty-output disabled/workflow_dispatch skills (repo-pulse, push-recap, fork-fleet, repo-article, repo-actions, deep-research, hn-digest, rss-digest, polymarket, token-alert). Open-issue INDEX.md count grew 6 → 16 in one filing; suggests eval regex needs same-day grace or should skip disabled/workflow_dispatch skills entirely.
- [[issues/ISS-019]] — batch-health OUTAGE 2026-07-14: 4 skills missed morning window (compute-futures-eda + planner + memory-flush + memory-structural-dedupe). Filed as medium — direct ISS-006 tributary (delivery-rate underdelivery in 06:00 pocket, widened by even-DOM memory-hygiene skills).
- **Enabled-but-never-dispatched** — `ai-framework-watch` (weekly Mon 08:30) and `run-frequency-guard` (daily 23:00) have SKILL.md + `enabled: true` but no cron-state entries; heartbeat P3 novel-scan flagged 2026-07-11 per [[enabled-skills-can-never-dispatch]]. As of 2026-07-17 heartbeat, both still missing (`ai-framework-watch` most recent scheduled window 2026-07-13T08:30Z ~96h past 2h grace; `run-frequency-guard` most recent scheduled window 2026-07-16T23:00Z ~10h past 2h grace) — pattern hardens (7th consecutive day flagged, dedup-suppressed). Novel 2026-07-17: `run-frequency-guard` silence killed the operator's toggle-vs-PAT natural-experiment probe per [[probes-for-messages-yml-must-dispatch-outside-messages-yml]].

## Lessons (durable)
- [[oauth-outage-zero-token-signature]] — zero-token `result_json` = missing CLI auth, not a model error
- [[monitor-monitored-coupling]] — a monitor sharing a dependency with the monitored fleet can't catch outages of that dependency
- [[github-actions-cannot-create-prs]] — default Actions token cannot open PRs; surface compare links instead
- [[aeon-app-no-write-on-swarm-repo]] — pr-triage/pr-review verdicts on swarm-ai-research/swarm cannot post on-PR
- [[notegraph-phantom-file-refs]] — committed `notegraph.json` can reference files no longer on disk
- [[gha-inputs-unquoted-shell-rce]] — `inputs.*` flowing unquoted into `run:` shell commands is an RCE channel
- [[sandbox-blocks-piped-curl-installers]] — sandbox blocks `bash <(curl)` installers; audit skills degrade to hand-rolled fallbacks
- [[aeon-skills-dispatch-via-messages-yml]] — no per-skill workflow files; a window-wide silence implicates `messages.yml`, not per-skill auto-disable
- [[gha-messages-yml-cron-underdelivery]] — GHA silently drops ~97% of `messages.yml` `*/5` ticks in this repo with a daily 06:00–08:30Z dead zone (supersedes [[narrow-cron-pocket-vs-window-drop]])
- [[narrow-cron-pocket-vs-window-drop]] — _superseded_ — diagnostic command still useful, conclusion (matcher bug) ruled out
- [[gh-search-prs-api-drift]] — `gh search prs` dropped `--state merged`, `headRefName`, and `mergedAt`; SKILL.md fallback queries need patching
- [[pr-tracker-branch-prefix-misses-bot-identity]] — `ai/`-only branch filter drops `security/`-prefixed bot PRs under the same author identity; filter by commit-author email instead
- [[iss-006-pocket-recovery-is-noise]] — a single-day cron pocket recovery during ISS-006 is delivery-rate noise; close only after 3 clean days where every slot fires
- [[swarm-safety-eval-empty-writes-log-not-article]] — ISS-005 root cause is SSE_EMPTY path writing to the daily log, not the skill not running; reclassify as `permanent-limitation`
- [[compute-futures-12-seed-sample-too-small]] — at n=12 seeds, compute-futures-eda outlier flags reflect IQR-fence ties, not regime changes; widen sweep or switch to a tie-robust statistic
- [[compute-futures-eda-wallet-sum-pnl-correlations-are-float-dust]] — wallet_sum_pnl σ ≈ 6e-12 means |r|≥0.8 crossings against volume columns (settlementLegs, realizedAbs, x402Total) are float-dust artifacts, not P&L signal; drop from the finding ladder
- [[skill-freshness-mtime-blind-in-gha]] — `actions/checkout` resets every file's mtime to the run instant, so skill-freshness's `stat --format=%Y` age check can never flag anything in GHA; switch to `git log -1 --format=%ct` producer-commit timestamp
- [[aeon-bot-uses-multiple-signing-identities]] — aeon bot signs commits under both `aeonframework@users.noreply.github.com` and `aeon@aeonframework.dev`; single-value `BOT_EMAIL` drops PRs silently
- [[pr-tracker-step-5-misses-fresh-bot-prs]] — pr-tracker only notifies on merges / stale / closed-no-merge; brand-new bot PRs land invisibly until they age into staleness
- [[pr-tracker-notify-repeats-with-no-state-change]] — step-5 has no dedup guard; a persistent stale/closed-no-merge state fires an identical notify every day until the wall clock rolls a PR off the 7d window
- [[notify-script-has-no-f-flag]] — `./notify -f <file>` is documented across multiple SKILLs but the actual script takes message as `$1`; using `-f` writes the literal `-f` as the message body
- [[status-md-auto-commit-drops-writes]] — _superseded 2026-07-12_ — writes DELAY (~15h to next sweeper auto-commit) rather than DROP; heartbeat's own glob still doesn't stage `docs/`
- [[snapshot-rebase-clobbers-docs-status-md]] — third failure mode entrenched across **6 consecutive days** (2026-07-12 `bcae68a` + 07-13 `7dfcc30` + 07-14 `c0b648a` + 07-15 `e9e7f22` + 07-16 `c2ca336` + 07-17 `f6dd14f`, same upstream ref `rsavitt/aeon @ a7f04ee` clobbering the same ~33-38d-stale version six days in a row — one day past 2026-07-16 mitigation urgency threshold)
- [[graphql-statereason-only-on-issue-type]] — SKILL.md GraphQL query requests `stateReason` on `PullRequest`; that field exists only on `Issue` and the query hard-fails
- [[notify-inline-cat-substitution-blocked-in-sandbox]] — sandbox blocks any `$(...)` around `./notify` (inline arg AND two-step MSG-variable); write directly to `.pending-notify/` or dispatch via node `execFileSync`
- [[notegraph-extractor-generatedat-nondeterministic]] — notegraph extractor writes `generatedAt` into 4 outputs; naive `git diff --quiet` HAS_DIFF gate re-PRs stable corpora; inspect per-file diff, revert timestamp-only churn
- [[skill-state-on-blocked-pr-branch-is-lost]] — skills that write dedup state to their daily branch lose that state when the PR is blocked by [[github-actions-cannot-create-prs]]; suggest-edges re-proposed the same 3 similarity-1.00 edges from 07-07's branch because state never merged to main
- [[sandbox-blocks-shell-redirect-to-workdir]] — shell `>` to workdir paths is refused; use the tool's own `-o` flag or Python `pathlib.Path.write_text` after `subprocess.run`
- [[enabled-skills-can-never-dispatch]] — a skill with SKILL.md + `enabled: true` may have zero entries in cron-state.json and never dispatch; only heartbeat's P3 novel-scan catches this failure class
- [[probes-for-messages-yml-must-dispatch-outside-messages-yml]] — a diagnostic probe for messages.yml cron delivery can be silenced by the very failure mode it tests; trigger via `gh workflow run` or operator eyeball, never via another scheduled skill

## Snapshot (2026-07-17)
| Signal | Value |
|---|---|
| Today's status | 🔴 DEGRADED — ISS-001 day 27 residue (38 skills at success_rate<0.5, all `last_status: success`, `consecutive_failures=0`; denominator burn-down continues). ISS-006 close-clock **Day-2** (07-16 + 07-17 both cleared 06:00 pockets on-cadence: planner + compute-futures-eda 06:36:4x cluster today; 05:30 also recovered via suggest-edges 06:40:43Z + notegraph 06:42:01Z catch-up). PR queue turned over (InsForge#1742 fresh 07-17 breaks 11-day stationary streak; hash-guard fired SEND). snapshot-rebase clobber of `docs/status.md` 6th consecutive day (`f6dd14f` @ 06:56Z today). run-frequency-guard 23:00Z probe silenced by [[enabled-skills-can-never-dispatch]] per [[probes-for-messages-yml-must-dispatch-outside-messages-yml]] |
| Cron-state | all 42 tracked skills at `last_status: success`, 0 `dispatched`, 0 `consecutive_failures ≥ 3`; cumulative `success_rate` < 0.5 on 38 skills (ISS-001 OAuth-residue catch-up, day 27) |
| Enabled skills | 44 — 42 in cron-state.json, `ai-framework-watch` (Mon 08:30) and `run-frequency-guard` (daily 23:00) still never-dispatched per [[enabled-skills-can-never-dispatch]] (7th consecutive day flagged, dedup-suppressed) |
| Open issues | 17 in INDEX.md — ISS-001 critical + ISS-002/005/006/007/008/009–018 high + ISS-019 medium. Grew 6 → 16 on 2026-07-12 (skill-evals BOOTSTRAP filed 10 no_file_match on disabled/workflow_dispatch skills), 16 → 17 on 2026-07-14 (batch-health ISS-019 morning-batch outage) |
| Pending branches | **15** queued behind [[github-actions-cannot-create-prs]] — same list as 2026-07-16 plus `notegraph/2026-07-17` (byte-identical stats but 2 `similar` edges rewired around MEMORY.md). Unblock path per 2026-07-16 planner reframe: repo Settings → Actions → General → Workflow permissions → "Allow GitHub Actions to create and approve pull requests" (preferred one-checkbox); PAT fallback |
| PR queue (tracked-author) | Category tuple flipped `(0,1,0,0) → (0,1,0,1)` on 07-17 — **InsForge/InsForge#1742** filed 07:41Z on `security/bump-multer-nodemailer-dos` (multer 2.2.0 + nodemailer 8.0.11 for disclosed DoS/CRLF); 3 bot reviews within 15min (`greptile-apps` P2 semver-floor + lockfile-scope, `coderabbitai` review stack, `agent-zhang-beihai` procedural-close flag). Hash flipped `6e12…` → `5ee6…` — step-5 dedup guard fired SEND (ended 3-day SKIP streak per [[pr-tracker-notify-repeats-with-no-state-change]]). AR#436 stays stale (4th consecutive day, activity 10.85d ago); Vibe-Trading#390 retained in 30d merged table (rolloff 2026-08-04); kage#66 retained in 30d closed-no-merge table (rolloff 2026-08-02) |
| PR queue (swarm-repo) | Stationary 8th consecutive day at head `da039d5f` for #527. pr-review APPROVE 5/5 verdict re-verified live on operator invocation 07-17 — 25th consecutive day of the same cross-org 403 write-block per [[aeon-app-no-write-on-swarm-repo]]. Dependabot queue turned over slightly (fresh #533 langgraph 1.2.5→1.2.9 supersedes 07-16's #531, other 5 identical) |
| skill-freshness | FRESHNESS_OK today — 44 enabled consumers · 0 cross-skill deps · 0 flagged (dep count 2 → 0 vs 07-15 reflects absent `articles/` dir in GHA snapshot, not a fleet change). Structural mtime blind spot per [[skill-freshness-mtime-blind-in-gha]] unchanged |
| Pending disclosures | **1 in `.pending-disclosure/`**: oomol-lab/open-connector 2026-07-11 (semgrep `javascript.node-crypto.security.gcm-no-tag-length` at `src/server/secrets/secret-codec.ts:48`, medium severity — Node local codec accepts 4-byte GCM tag reducing forgery from 2⁻¹²⁸ → 2⁻³², 3-line fix documented). torlink 07-04 entry silently wiped by snapshot `323965d0` on 2026-07-05 per [[snapshot-rebase-clobbers-docs-status-md]] pattern; reconstructable from 07-04 vuln-scanner log if operator wants to re-file |
| Notify pattern | fleet-wide direct writes to `.pending-notify/${epoch}-${skill}.md` per [[notify-inline-cat-substitution-blocked-in-sandbox]] + [[notify-script-has-no-f-flag]] (SKILL.md's `./notify -f <file>` prescription is broken; workaround is direct pending-file write with `${epoch}-${skill}.md` naming). No `-f`-corruption incidents this week |
| notegraph | 2026-07-17 regen: **165n · 1221h · 447s · 1 orphan · 43 atomic · 0 bundled** (edges=1668). Δ vs HEAD 0/0/0/0 aggregate — but 2 `similar` edges **rewired** around `memory/MEMORY.md` (added: `daily-plan-2026-06-27 → MEMORY.md`, `daily-plan-2026-07-11 → MEMORY.md`; removed: prior plan↔plan edges). Root: MEMORY.md's current-focus block grew per 07-16 memory-flush + planner reframe, boosting its similarity to those two daily-plans past the plan↔plan similarity — nearest-neighbor `similar` edges shifted. Confirms MEMORY.md-as-graph-node behavior: bloat in the index pulls similarity edges toward itself |

## Permission constraints (current)
- aeon GitHub App: no write on `swarm-ai-research/swarm` (labels, comments, reviews 403). Verdicts run, posts blocked.
- vuln-scanner: token lacks fork scope — disclosures drafted to `.pending-disclosure/` only; operator opens the upstream PR.
- skillpacks / notegraph: PR creation blocked, branch pushed, compare link in notify.
- workflow-audit: cannot auto-land RCE patch — token lacks `workflows` write; needs `GH_GLOBAL` PAT.

## Open recommendations
- Pre-flight credential canary in `aeon.yml` (exits with distinct error when both `ANTHROPIC_API_KEY` and `CLAUDE_CODE_OAUTH_TOKEN` are empty).
- Out-of-band heartbeat from a different account / status-page pinger.
- Truncate `inputs.var` in `run-name` so pr-review titles don't leak multi-line policy.
- Fix `last_error` writer to store the actual stderr line.
- Patch `pr-tracker` SKILL.md to drop `--state merged` and `headRefName` per [[gh-search-prs-api-drift]].
