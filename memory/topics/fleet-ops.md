# Fleet Ops

Cross-cutting operational lessons and constraints for the Aeon fleet: credential outages, monitoring-loop hazards, GitHub App permission boundaries, and cron-state pathologies.

## Open incidents
- [[issues/ISS-001]] — CLAUDE_CODE_OAUTH_TOKEN missing 2026-06-06 → 2026-06-20T06:05Z; investigating, day 2 of 3 clean days completed (target close 2026-06-23).
- [[issues/ISS-006]] — GHA cron tick dropped 2026-06-21 05:30–08:00Z; 6 skills missed morning slots. Distinct signature from ISS-001 (no auth failure — skills never started). 2026-06-22: no batch-health/heartbeat in today's log to confirm one-off vs recurring.

## Lessons (durable)
- [[oauth-outage-zero-token-signature]] — zero-token `result_json` = missing CLI auth, not a model error
- [[monitor-monitored-coupling]] — a monitor sharing a dependency with the monitored fleet can't catch outages of that dependency
- [[github-actions-cannot-create-prs]] — default Actions token cannot open PRs; surface compare links instead
- [[aeon-app-no-write-on-swarm-repo]] — pr-triage/pr-review verdicts on swarm-ai-research/swarm cannot post on-PR
- [[notegraph-phantom-file-refs]] — committed `notegraph.json` can reference files no longer on disk
- [[gha-inputs-unquoted-shell-rce]] — `inputs.*` flowing unquoted into `run:` shell commands is an RCE channel
- [[sandbox-blocks-piped-curl-installers]] — sandbox blocks `bash <(curl)` installers; audit skills degrade to hand-rolled fallbacks

## Snapshot (2026-06-22)
| Signal | Value |
|---|---|
| 7d workflow runs | ~931 (53/931 successes = 5.7% as of 2026-06-21; recovery dominates last 36h) |
| Today's status | 🟡 DEGRADED-fading — no new failures, but day 2/3 of clean-run window and cumulative `success_rate` still under 0.6 from ISS-001 backlog |
| Recovery batch | 2026-06-20T06:05–06:33Z (all skills back to `last_status: success`, `consecutive_failures: 0`) |
| Enabled skills | 44 (38 with cron-state rows; 6 never dispatched) |
| Open issues | 4 on disk / 3 in INDEX.md (drift: ISS-001 investigating; ISS-002, ISS-005 open; ISS-006 open — not in INDEX) |
| Resolved | ISS-003 (cost-report), ISS-004 (skill-health) — both recovered with OAuth restore on 2026-06-21 |
| `last_error` cron-state field | storing JSON tail (cost block), not actual error — orthogonal logging bug |
| Pending branches | `fix/workflow-security-audit-2026-06-21` (RCE patch for fleet-runner.yml, App lacks `workflows` write perm); `notegraph/2026-06-21` (+9n/+65e) |
| Notegraph state | 58 nodes · 346 edges · 1 orphan · 0 bundled (2026-06-21 post-reflect) |
| 2026-06-22 activity | sweeper / issue-triage / github-monitor / fleet-control / weekly-shiplog / pr-review / pr-tracker / pr-triage — all steady state; no batch-health / heartbeat / skill-health entries today |

## Permission constraints (current)
- aeon GitHub App: no write on `swarm-ai-research/swarm` (labels, comments, reviews 403). Verdicts run, posts blocked.
- vuln-scanner: token lacks fork scope — disclosures drafted to `.pending-disclosure/` only; operator opens the upstream PR.
- skillpacks / notegraph: PR creation blocked, branch pushed, compare link in notify.

## Open recommendations
- Pre-flight credential canary in `aeon.yml` (exits with distinct error when both `ANTHROPIC_API_KEY` and `CLAUDE_CODE_OAUTH_TOKEN` are empty).
- Out-of-band heartbeat from a different account / status-page pinger.
- Truncate `inputs.var` in `run-name` so pr-review titles don't leak multi-line policy.
- Fix `last_error` writer to store the actual stderr line.
