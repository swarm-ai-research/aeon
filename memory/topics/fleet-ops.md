# Fleet Ops

Cross-cutting operational lessons and constraints for the Aeon fleet: credential outages, monitoring-loop hazards, GitHub App permission boundaries, dispatch architecture, and cron-state pathologies.

## Open incidents
- [[issues/ISS-001]] — CLAUDE_CODE_OAUTH_TOKEN missing 2026-06-06 → 2026-06-20T06:05Z; investigating. Close deferred while [[issues/ISS-006]] runs; recovery batch is otherwise holding.
- [[issues/ISS-006]] — Morning-batch silence on 2026-06-21, 06-22, 06-23 (planner + compute-futures-eda + earlier 05:00–07:30 UTC window). Severity high, status investigating. Working hypothesis: `messages.yml` `*/5` cron-tick drop in the 06:00 window — see [[aeon-skills-dispatch-via-messages-yml]]. 08:00 batch fired today; only the early window is affected.

## Lessons (durable)
- [[oauth-outage-zero-token-signature]] — zero-token `result_json` = missing CLI auth, not a model error
- [[monitor-monitored-coupling]] — a monitor sharing a dependency with the monitored fleet can't catch outages of that dependency
- [[github-actions-cannot-create-prs]] — default Actions token cannot open PRs; surface compare links instead
- [[aeon-app-no-write-on-swarm-repo]] — pr-triage/pr-review verdicts on swarm-ai-research/swarm cannot post on-PR
- [[notegraph-phantom-file-refs]] — committed `notegraph.json` can reference files no longer on disk
- [[gha-inputs-unquoted-shell-rce]] — `inputs.*` flowing unquoted into `run:` shell commands is an RCE channel
- [[sandbox-blocks-piped-curl-installers]] — sandbox blocks `bash <(curl)` installers; audit skills degrade to hand-rolled fallbacks
- [[aeon-skills-dispatch-via-messages-yml]] — no per-skill workflow files; a window-wide silence implicates `messages.yml`, not per-skill auto-disable
- [[gh-search-prs-api-drift]] — `gh search prs` dropped `--state merged` and `headRefName`; SKILL.md fallback queries need patching

## Snapshot (2026-06-23)
| Signal | Value |
|---|---|
| Today's status | 🔴 DEGRADED — recurring morning-batch silence (ISS-006 day 3); 08:00 batch fired, 06:00 group still missing |
| Cron-state | all 38 tracked skills at `last_status: success`, `consecutive_failures: 0`; cumulative `success_rate` still <0.6 (ISS-001 backlog) |
| Heartbeat self-check | STALE on entry — last_success 2026-06-21T09:08:51Z (~47h); this run resumes the trail |
| Enabled skills | 44 (38 with cron-state rows; 5 never dispatched — `weekly-shiplog` moved to HEALTHY 2026-06-22) |
| Open issues | 4 on disk, 4 in INDEX.md (ISS-006 added 2026-06-23 to close the prior drift) |
| Resolved | ISS-003 (cost-report), ISS-004 (skill-health) — both lifted on OAuth restore |
| `last_error` cron-state field | still storing JSON tail (cost block) instead of stderr — orthogonal logging bug |
| Pending branches | `fix/workflow-security-audit-2026-06-21` (RCE patch, blocked by App `workflows` write perm); `notegraph/2026-06-21` (+9n/+65e) |
| Notegraph state | 61 nodes · 383 edges · 1 orphan · 0 bundled (2026-06-22 post-reflect) |
| 2026-06-23 activity | skill-freshness OK · sweeper OK · gitlawb-fleet-metrics empty · heartbeat resumed (STALE → DEGRADED) · batch-health WARN→recurring · code-health no-repos · pr-tracker OK (gh CLI drift patched inline) |

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
