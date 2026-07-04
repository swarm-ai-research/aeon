# Fleet Ops

Cross-cutting operational lessons and constraints for the Aeon fleet: credential outages, monitoring-loop hazards, GitHub App permission boundaries, dispatch architecture, and cron-state pathologies.

## Open incidents
- [[issues/ISS-001]] — CLAUDE_CODE_OAUTH_TOKEN missing 2026-06-06 → 2026-06-20T06:05Z; investigating. Close deferred while [[issues/ISS-006]] runs; recovery batch is otherwise holding.
- [[issues/ISS-006]] — Day 14: **memory-flush half-recovered** — memory-flush fired 06:02Z (breaking 14-day even-day silence from 2026-06-20T06:07Z) but memory-structural-dedupe 06:10 slot **confirmed silent**, so the full even-day pocket did NOT recover. Yesterday planner + compute-futures-eda recovered at 07:35Z. Sixth consecutive pocket-swap day (Day 10 EDA↔08:00, Day 11 reversed, Day 12 flipped, Day 13 EDA-recover, Day 14 memory-flush-recover, Day 15 memory-flush-holds/dedupe-silent-planner-miss). Six weekly/biweekly skills also at 2× threshold (janitor / skillpacks / compute-macro-correlate Sun, milestone-tracker / cost-report Mon, memory-structural-dedupe even-DOM). Per [[iss-006-pocket-recovery-is-noise]] still delivery-rate noise — close clock stays at 0 consecutive clean days.
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

## Snapshot (2026-07-04)
| Signal | Value |
|---|---|
| Today's status | 🔴 DEGRADED — ISS-006 day 14; memory-flush pocket half-recovered (memory-flush 06:02Z fired, memory-structural-dedupe 06:10 confirmed silent); status.md was 25d stale on entry, heartbeat regenerated |
| Cron-state | all 42 tracked skills at `last_status: success`, 0 `dispatched`, 0 `consecutive_failures ≥ 3`; cumulative `success_rate` < 0.5 on 38 skills (ISS-001 OAuth-residue catch-up, day 14) |
| Enabled skills | 44 — 42 in cron-state.json, `ai-framework-watch` (Mon 08:30) and `run-frequency-guard` (daily 23:00) still never-dispatched despite being enabled |
| Open issues | 4 on disk, 4 in INDEX.md (ISS-001, 002, 005, 006) — ISS-005 reclassify still pending |
| Resolved | ISS-003 (cost-report), ISS-004 (skill-health) — both lifted on OAuth restore |
| Pending branches | `agi-tracker/2026-06-29`; `notegraph/2026-06-29` +3n/+51e (6th consecutive notegraph queued: 06-26/06-29/07-01/07-02/07-04); `fix/workflow-security-audit-2026-06-28` (16C/36H); `skill-graph/2026-06-28` (INIT); `fix/workflow-security-audit-2026-06-21` (older RCE) — all blocked by repo policy "GitHub Actions is not permitted to create or approve pull requests" |
| Today's fired slots | 06:02Z memory-flush · 06:01Z compute-futures-eda (skipped — no new sweep) · 08:51Z heartbeat (~51m late) · 10:00Z pr-tracker · notegraph · fleet-control · repo-revive · pr-review · pr-triage · code-health · github-monitor · issue-triage · vuln-scanner · surplus-pulse · compute-pulse |
| Today's missed slots | 06:10 memory-structural-dedupe (confirmed cold) · 06:30 planner · 08:00 batch-mates (batch-health / skill-freshness / gitlawb-fleet-metrics — heartbeat fired but ~51m late) |
| 2× threshold skills | janitor (Sun 05:30, 14d), skillpacks (Sun 06:00, 14d), compute-macro-correlate (Sun 06:30, 14d), milestone-tracker (Mon 12:00, 14d), cost-report (Mon 07:00, 14d), memory-structural-dedupe (even DOM 06:10, 14d) — all ISS-006 tributaries |
| PR queue | 2 open + 1 closed-no-merge today: Vibe-Trading#390 (1d, fresh, `@aeonframework.dev`); Agent-Reach#436 (**7d 15h stale**, notify fired step-5); kage#66 **closed silently by owner `tamnd`** at 2026-07-03T12:20Z after 12h 50m open (COMPLETED, no comment) — first closed-no-merge in tracked window |
| skill-freshness | FRESHNESS_OK 6th consecutive emit (2026-06-26, -28, -30, 07-02, 07-04) — structurally blind in GHA per [[skill-freshness-mtime-blind-in-gha]]; compute-pulse.md at 98.2% of 7d content-date threshold |
| Pending disclosures | 1 in `.pending-disclosure/` (torlink 07-04: `ip@2.0.1` HIGH unpatchable + `esbuild` LOW dev-only) awaiting operator PAT to fork upstream |

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
