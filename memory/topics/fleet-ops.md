# Fleet Ops

Cross-cutting operational lessons and constraints for the Aeon fleet: credential outages, monitoring-loop hazards, GitHub App permission boundaries, dispatch architecture, and cron-state pathologies.

## Open incidents
- [[issues/ISS-001]] — CLAUDE_CODE_OAUTH_TOKEN missing 2026-06-06 → 2026-06-20T06:05Z; investigating. Close deferred while [[issues/ISS-006]] runs; recovery batch is otherwise holding.
- [[issues/ISS-006]] — Day 7: morning pocket recovered today (planner + compute-futures-eda fired ~07:34Z, 7-day silence broken); 23:45 sweeper pocket also self-resolved (last_success 2026-06-27T00:19Z). NEW dead zone surfaced: 09:00 UTC batch silent 5 days (fleet-control, github-monitor, issue-triage, pr-triage, pr-review's 09:00-only slot) — pr-review's 18:00 sister fires fine, ruling out skill-level breakage. Root cause unchanged; mitigation must cover every `aeon.yml` slot. See [[gha-messages-yml-cron-underdelivery]].

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

## Snapshot (2026-06-27)
| Signal | Value |
|---|---|
| Today's status | 🔴 DEGRADED — ISS-006 day 7; morning pocket recovered (planner + compute-futures-eda fired ~07:34Z, 7-day silence broken); 23:45 sweeper pocket also self-resolved; NEW 09:00 dead zone (5 days, fleet-control / github-monitor / issue-triage / pr-triage / pr-review-09:00-slot) |
| Cron-state | all 38 tracked skills at `last_status: success`, `consecutive_failures: 0`; cumulative `success_rate` still <0.6 (ISS-001 backlog) |
| Heartbeat self-check | OK on entry — last_success 2026-06-26T08:47:21Z (~24h 53m), under 36h threshold; this run was ~1h 40m late vs 08:00 dispatch (worse than 06-24/25/26 42–47m — cadence still drifting) |
| Enabled skills | 44 (38 with cron-state rows; 5 never dispatched: agi-tracker, ai-framework-watch, config-validator, run-frequency-guard, swarm-safety-eval) |
| Open issues | 4 on disk, 4 in INDEX.md (ISS-001, 002, 005, 006) |
| Resolved | ISS-003 (cost-report), ISS-004 (skill-health) — both lifted on OAuth restore |
| Pending branches | `fix/workflow-security-audit-2026-06-21` (RCE patch, blocked by App `workflows` write perm); `notegraph/2026-06-26` (auto-PR blocked by same perm gap); `suggest-edges/2026-06-25` (same perm gap) |
| Notegraph state | 69 nodes · 390 hard · 132 soft · 1 orphan · 0 bundled (post-reflect 2026-06-26 numbers; 2026-06-27 regen pending this reflect) |
| 2026-06-27 activity | first planner run since 2026-06-20 (7-day silence broken, plan-only, top-priority `iss-006-messages-yml-per-slot-crons`) · compute-futures-eda first run since 2026-06-20 (144 rows, conservation healthy) · vuln-scanner first run since 2026-06-20 (vercel/eve, 0 code findings, 72 dep advisories, bundled draft PR pending operator) · batch-health OK (both morning slots fired) · heartbeat DEGRADED ~1h 40m late, single 🔴 notify for NEW 09:00 dead zone · pr-tracker 7th empty day post-filter BUT 1 real bot-authored PR at `Panniantong/Agent-Reach#436` filtered out (security/ branch, [[pr-tracker-branch-prefix-misses-bot-identity]]) · surplus-pulse catalog run · stale-content-pr-sweeper recovered (steady state) |

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
