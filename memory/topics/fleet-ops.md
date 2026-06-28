# Fleet Ops

Cross-cutting operational lessons and constraints for the Aeon fleet: credential outages, monitoring-loop hazards, GitHub App permission boundaries, dispatch architecture, and cron-state pathologies.

## Open incidents
- [[issues/ISS-001]] — CLAUDE_CODE_OAUTH_TOKEN missing 2026-06-06 → 2026-06-20T06:05Z; investigating. Close deferred while [[issues/ISS-006]] runs; recovery batch is otherwise holding.
- [[issues/ISS-006]] — Day 8: morning 06:00–06:30 pocket **relapsed** after one-day day-7 recovery (6/8 expected slots missed today, OUTAGE); 07:00–07:30 Sunday slots fired late at 08:14Z (74m/44m late). 09:00 dead zone now 6 days silent. NEW 05:00 pocket signal — notegraph + suggest-edges last_success 2026-06-26T05:53Z, ~50h stale, first multi-day 05:00 silence since 06-24 narrowing. Multi-pocket sliding model now spans 05:00, 06:00–06:30, 09:00, 23:45. Root cause unchanged; mitigation still per-slot crons. See [[gha-messages-yml-cron-underdelivery]] and [[iss-006-pocket-recovery-is-noise]].
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

## Snapshot (2026-06-28)
| Signal | Value |
|---|---|
| Today's status | 🔴 DEGRADED — ISS-006 day 8; morning pocket **relapsed** after day-7 recovery (6/8 expected skills missed, OUTAGE); 07:00–07:30 Sunday slots fired late ~74m/44m past schedule; 09:00 dead zone now 6d; NEW 05:00 pocket newly silent (notegraph + suggest-edges ~50h stale) |
| Cron-state | all 38 tracked skills at `last_status: success`, `consecutive_failures: 0`; cumulative `success_rate` still <0.6 (ISS-001 backlog) |
| Heartbeat self-check | OK on entry — last_success 2026-06-27T09:45Z (~22h 29m), under 36h threshold; this run was ~14m late vs 08:00 dispatch — cleanest morning lag of the week (vs 1h 40m on 06-27, 42–47m on 06-24/25/26) |
| Enabled skills | 44 (39 with cron-state rows; 5 never dispatched: agi-tracker, ai-framework-watch, config-validator, run-frequency-guard — swarm-safety-eval now has a row, last_success 2026-06-28T08:15:47Z) |
| Open issues | 4 on disk, 4 in INDEX.md (ISS-001, 002, 005, 006) — ISS-005 root cause reframed per [[swarm-safety-eval-empty-writes-log-not-article]] |
| Resolved | ISS-003 (cost-report), ISS-004 (skill-health) — both lifted on OAuth restore |
| Pending branches | `fix/workflow-security-audit-2026-06-28` (new today, 16 critical + 36 high; `gh pr create` blocked by repo policy — same App perm gap); `skill-graph/2026-06-28` (INIT 173 skills, same blocker); `fix/workflow-security-audit-2026-06-21` (older RCE patch, still pending PAT) |
| Notegraph state | 78 nodes · 455 hard · 173 soft · 1 orphan · 0 bundled (post-reflect 2026-06-27 numbers; 2026-06-28 regen pending this reflect) |
| 2026-06-28 activity | batch-health OUTAGE (6 missing, morning pocket relapsed, ISS-006 day-8 update appended) · heartbeat DEGRADED, ~14m late, 🔴 notify for NEW 05:00 pocket silence · skill-graph **INIT first run** (173 skills mapped, 5 categories, 5+27+42 edges; PR blocked by repo policy) · workflow-security-audit **first run** (100 findings: 16C/36H/17M/31L, branch pushed, PR blocked by same repo policy) · skill-evals SKILL_EVALS_RECOVERED (heartbeat pattern fixed; swarm-safety-eval reframed) · planner / compute-futures-eda silent (06:00–06:30 pocket relapsed) · surplus-pulse catalog run · pr-tracker 8th empty day post-filter, `Panniantong/Agent-Reach#436` still open (2d, no reviews) · stale-content-pr-sweeper steady |

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
