# Fleet Ops

Cross-cutting operational lessons and constraints for the Aeon fleet: credential outages, monitoring-loop hazards, GitHub App permission boundaries, dispatch architecture, and cron-state pathologies.

## Open incidents
- [[issues/ISS-001]] — CLAUDE_CODE_OAUTH_TOKEN missing 2026-06-06 → 2026-06-20T06:05Z; investigating. Close deferred while [[issues/ISS-006]] runs; recovery batch is otherwise holding.
- [[issues/ISS-006]] — Day 15: **large 07:44Z burst broke two 15-day silences** — skillpacks (Sun 06:00) and compute-macro-correlate (Sun 06:30) both fired for the first time since 2026-06-20, plus planner / compute-futures-eda / config-validator / swarm-safety-eval all recovered their Sunday slots ~1-2h late. But janitor (05:30) stayed cold and the 08:00 batch fired ~2h late (batch-health / skill-freshness / gitlawb-fleet-metrics / heartbeat). Per [[iss-006-pocket-recovery-is-noise]] still delivery-rate noise — the burst pattern (six recoveries clustered in a single 07:44Z tick) is exactly the signature of a stuck-then-flush cron scheduler, not a resolved dispatch pipeline. Sixth-plus consecutive pocket-swap day; close clock stays at 0 consecutive clean days.
- [[issues/ISS-007]] — heartbeat missing_pattern in eval regex; new 2026-07-05, filed by skill-evals. Enabled skill FAIL (not covered by ISS-002/005).
- [[issues/ISS-008]] — cost-report no_file_match; new 2026-07-05, filed by skill-evals. Standing ISS-006 tributary (weekly Mon 07:00 slot at 2× threshold).
- [[issues/ISS-005]] — swarm-safety-eval no_file_match: skill is now running successfully (last_success 2026-06-28T08:15:47Z) but its SSE_EMPTY path writes to the daily log, not an article; reclassify from `missing-secret-or-cron` to `permanent-limitation` per [[swarm-safety-eval-empty-writes-log-not-article]].

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
- [[skill-freshness-mtime-blind-in-gha]] — `actions/checkout` resets every file's mtime to the run instant, so skill-freshness's `stat --format=%Y` age check can never flag anything in GHA; switch to `git log -1 --format=%ct` producer-commit timestamp
- [[aeon-bot-uses-multiple-signing-identities]] — aeon bot signs commits under both `aeonframework@users.noreply.github.com` and `aeon@aeonframework.dev`; single-value `BOT_EMAIL` drops PRs silently
- [[pr-tracker-step-5-misses-fresh-bot-prs]] — pr-tracker only notifies on merges / stale / closed-no-merge; brand-new bot PRs land invisibly until they age into staleness
- [[pr-tracker-notify-repeats-with-no-state-change]] — step-5 has no dedup guard; a persistent stale/closed-no-merge state fires an identical notify every day until the wall clock rolls a PR off the 7d window
- [[notify-script-has-no-f-flag]] — `./notify -f <file>` is documented across multiple SKILLs but the actual script takes message as `$1`; using `-f` writes the literal `-f` as the message body
- [[status-md-auto-commit-drops-writes]] — heartbeat rewrites of `docs/status.md` are silently lost by the workflow auto-commit step; on-disk status page ages indefinitely
- [[graphql-statereason-only-on-issue-type]] — SKILL.md GraphQL query requests `stateReason` on `PullRequest`; that field exists only on `Issue` and the query hard-fails

## Snapshot (2026-07-05)
| Signal | Value |
|---|---|
| Today's status | 🔴 DEGRADED — ISS-006 day 15; **07:44Z burst broke skillpacks + compute-macro-correlate 15-day silences** but janitor 05:30 stayed cold and 08:00 batch fired ~2h late; workflow-security-audit landed a fresh SHA-pinning wave (13/16 unpinned-uses Critical findings resolved from 2026-06-28) |
| Cron-state | all 42 tracked skills at `last_status: success`, 0 `dispatched`, 0 `consecutive_failures ≥ 3`; cumulative `success_rate` < 0.5 on 38 skills (ISS-001 OAuth-residue catch-up, day 15) |
| Enabled skills | 44 — 42 in cron-state.json, `ai-framework-watch` (Mon 08:30) and `run-frequency-guard` (daily 23:00) still never-dispatched despite being enabled |
| Open issues | 6 on disk, 6 in INDEX.md (ISS-001, 002, 005, 006, 007, 008) — skill-evals filed ISS-007 (heartbeat missing_pattern) and ISS-008 (cost-report no_file_match) on today's bootstrap eval run |
| Resolved | ISS-003 (cost-report), ISS-004 (skill-health) — both lifted on OAuth restore |
| Pending branches | 7 queued for operator PAT: `agi-tracker/2026-06-29`; `notegraph/2026-07-04` (6th consecutive: 06-26/06-29/07-01/07-02/07-04); `fix/workflow-security-audit-2026-06-21`, `-06-28`, and new **`fix/workflow-security-audit-2026-07-05`** (13 unpinned-uses Critical resolved); `skill-graph/2026-06-28`; `skillpacks/2026-07-05` (outages-fleet rename) — all blocked by repo policy "GitHub Actions is not permitted to create or approve pull requests" |
| Today's fired slots | 07:44Z burst: skillpacks (breaks 15d silence) · compute-macro-correlate (breaks 15d silence) · planner · compute-futures-eda · config-validator · swarm-safety-eval · 09:58Z heartbeat (~2h late) · 10:00Z pr-tracker (1h38m late) · pr-review · pr-triage · code-health · github-monitor · issue-triage · surplus-pulse · workflow-security-audit · skill-evals · skill-freshness |
| Today's missed slots | 05:30 janitor (still cold — Sunday 15d silence unbroken) · 08:00 batch-mates fired ~2h late (batch-health, skill-freshness, gitlawb-fleet-metrics, heartbeat) |
| 2× threshold skills | milestone-tracker (Mon 12:00, 15d), cost-report (Mon 07:00, 15d), memory-structural-dedupe (even DOM 06:10, 15d), janitor (Sun 05:30, 15d) — 4 remaining after skillpacks/compute-macro-correlate flush |
| PR queue | 2 open + 1 closed-no-merge (unchanged vs 2026-07-04): Vibe-Trading#390 (2d 3h, fresh, `@aeonframework.dev`); Agent-Reach#436 (**8d 16h stale**, notify fired step-5 2nd day); kage#66 closed silently by owner `tamnd` 2026-07-03T12:20Z — 2nd consecutive identical notify per [[pr-tracker-notify-repeats-with-no-state-change]] |
| skill-freshness | FRESHNESS_OK 7th consecutive emit (2026-06-26, -28, -30, 07-02, -03, -04, -05) — structurally blind in GHA per [[skill-freshness-mtime-blind-in-gha]]; compute-pulse.md at 98.2% of 7d content-date threshold |
| Pending disclosures | 1 in `.pending-disclosure/` (torlink 07-04: `ip@2.0.1` HIGH unpatchable + `esbuild` LOW dev-only) — no change today |
| workflow-security-audit | 136 total findings (3C / 43H / 31M / 59L); Δ vs 2026-06-28 = +70 new (all M/L), 0 REINTRODUCED, 52 resolved; SHA-pinning wave landed across 6 workflow files, only `aeon.yml` still on `@v5` mutable tags |
| Skillpacks | 172 skills · 16 packs · 0 solos · 1273 edges (delta 0/0/0); slug rename `monitor-movers` → `outages-fleet` after batch-health moved clusters — structurally not a new pack but still triggers `SKILLPACKS_NEW_PACK` |

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
