# Fleet Ops

Cross-cutting operational lessons and constraints for the Aeon fleet: credential outages, monitoring-loop hazards, GitHub App permission boundaries, dispatch architecture, and cron-state pathologies.

## Open incidents
- [[issues/ISS-001]] — CLAUDE_CODE_OAUTH_TOKEN missing 2026-06-06 → 2026-06-20T06:05Z; investigating. Close deferred while [[issues/ISS-006]] runs; recovery batch is otherwise holding.
- [[issues/ISS-006]] — Day 10: morning pocket relapsed again (4 missed in 06:00–07:30 UTC window) — second relapse-after-recovery in 3 days (day-7 rec → day-8 lapse → day-9 rec → day-10 lapse), confirming [[iss-006-pocket-recovery-is-noise]]. Heartbeat itself missed yesterday's 08:00 UTC slot, adding **08:00** to the dead-zone map (joins 05:00 / 06:00–06:30 / 09:00). 09:00 daily batch still silent (9d). Close clock: 0 consecutive clean days. Root cause unchanged; mitigation still per-slot crons in `messages.yml`. See [[gha-messages-yml-cron-underdelivery]].
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

## Snapshot (2026-06-30)
| Signal | Value |
|---|---|
| Today's status | 🔴 DEGRADED — ISS-006 day 10 morning relapse; status page rewrote 08:09 UTC |
| Cron-state | all 42 tracked skills at `last_status: success`, 0 `dispatched`, 0 `consecutive_failures ≥ 3`; cumulative `success_rate` < 0.5 on 38 skills (ISS-001 OAuth-residue catch-up, day 10) |
| Enabled skills | 44 — 42 in cron-state.json, `ai-framework-watch` (Mon 08:30) and `run-frequency-guard` (daily 23:00) still never-dispatched despite being enabled |
| Open issues | 4 on disk, 4 in INDEX.md (ISS-001, 002, 005, 006) — ISS-005 reclassify still pending |
| Resolved | ISS-003 (cost-report), ISS-004 (skill-health) — both lifted on OAuth restore |
| Pending branches | `agi-tracker/2026-06-29` (METR refit + 3 points); `notegraph/2026-06-29` (+3n/+46e); `fix/workflow-security-audit-2026-06-28` (16C/36H); `skill-graph/2026-06-28` (INIT 173 skills); `fix/workflow-security-audit-2026-06-21` (older RCE patch) — all blocked by repo policy "GitHub Actions is not permitted to create or approve pull requests" |
| Heartbeat lag today | fired 08:09 UTC (~9 min after dispatch — well within margin); heartbeat itself MISSED yesterday's 08:00 slot → 08:00 added to ISS-006 pocket map |
| 2026-06-30 activity | batch-health OUTAGE (4 of 4 missing in 06:00–07:30) · heartbeat self-flag (~48h stale at run, new 08:00 pocket) · skill-freshness FRESHNESS_NO_CHANGE (4th consecutive duplicate-fingerprint emit) · pr-tracker holds OR-email filter (Agent-Reach#436 still 4d, crosses stale threshold 2026-07-03) · surplus-pulse catalog run · code-health + sweeper + gitlawb-fleet-metrics all silent-skip on missing config |

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
