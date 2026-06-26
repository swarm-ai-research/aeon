# Fleet Ops

Cross-cutting operational lessons and constraints for the Aeon fleet: credential outages, monitoring-loop hazards, GitHub App permission boundaries, dispatch architecture, and cron-state pathologies.

## Open incidents
- [[issues/ISS-001]] — CLAUDE_CODE_OAUTH_TOKEN missing 2026-06-06 → 2026-06-20T06:05Z; investigating. Close deferred while [[issues/ISS-006]] runs; recovery batch is otherwise holding.
- [[issues/ISS-006]] — Morning-batch silence day 6: root cause is `messages.yml` `*/5` cron under-delivery (~3% delivery, daily 3–6h morning dead zone). 2026-06-26 widened the affected-slot list — `stale-content-pr-sweeper` (`45 23 * * *`) missed two nights running, so the fix must cover **every** `aeon.yml` slot, not just the 06:00–06:30 morning pocket. See [[gha-messages-yml-cron-underdelivery]].

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

## Snapshot (2026-06-26)
| Signal | Value |
|---|---|
| Today's status | 🔴 DEGRADED — ISS-006 day 6; root cause holds (`messages.yml` `*/5` ~3% delivery); new evidence widens affected slots beyond morning (23:45 sweeper miss 2 nights) |
| Cron-state | all 38 tracked skills at `last_status: success`, `consecutive_failures: 0`; cumulative `success_rate` still <0.6 (ISS-001 backlog) |
| Heartbeat self-check | OK on entry — last_success 2026-06-25T08:44:06Z (~24h 0m), under 36h threshold; this run was ~43m late vs 08:00 dispatch (matches 06-24/25 post-ISS-006 cadence) |
| Enabled skills | 44 (38 with cron-state rows; 5 never dispatched: agi-tracker, ai-framework-watch, config-validator, run-frequency-guard, swarm-safety-eval) |
| Open issues | 4 on disk, 4 in INDEX.md (ISS-001, 002, 005, 006) |
| Resolved | ISS-003 (cost-report), ISS-004 (skill-health) — both lifted on OAuth restore |
| Pending branches | `fix/workflow-security-audit-2026-06-21` (RCE patch, blocked by App `workflows` write perm); `notegraph/2026-06-26` (auto-PR blocked by same perm gap) |
| Notegraph state | 69 nodes · 393 hard · 130 soft · 1 orphan · 0 bundled (2026-06-26 notegraph regen, Δ +2n / +31e vs 2026-06-25) |
| 2026-06-26 activity | notegraph branch pushed (+2n/+31e) · gitlawb-fleet-metrics empty · batch-health OUTAGE (4 missing, ISS-006 day-6, even-DOM) · heartbeat DEGRADED ~43m late, single 🟡 notify for new sweeper signal · skill-freshness OK · code-health SKIPPED · pr-tracker OK (6th empty day) · surplus-pulse catalog run · ⚠ stale-content-pr-sweeper missed 23:45 slot 2 nights running (widens ISS-006) |

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
