# Fleet Ops

Cross-cutting operational lessons and constraints for the Aeon fleet: credential outages, monitoring-loop hazards, GitHub App permission boundaries, dispatch architecture, and cron-state pathologies.

## Open incidents
- [[issues/ISS-001]] — CLAUDE_CODE_OAUTH_TOKEN missing 2026-06-06 → 2026-06-20T06:05Z; investigating. Close deferred while [[issues/ISS-006]] runs; recovery batch is otherwise holding.
- [[issues/ISS-006]] — Day 12: **mirror-image pocket-swap** — morning EDA pocket silent (planner, memory-flush, memory-structural-dedupe, compute-futures-eda all missing) but **08:00 batch recovered ~34m late** (heartbeat 08:35Z, batch-health, gitlawb-fleet-metrics, skill-freshness all fired). Third consecutive pocket-swap day (Day 10 EDA↔08:00, Day 11 EDA↔08:00 reversed, Day 12 EDA↔08:00 flipped again), exactly the pattern [[iss-006-pocket-recovery-is-noise]] warns against. Planner now 5 days silent (last_success 2026-06-27T07:34Z) — most operationally painful signature; daily plan/re-plan loop is functionally offline until per-slot-cron fix ships. 09:00 daily batch still silent (11d). Close clock: 0 consecutive clean days.
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

## Snapshot (2026-07-02)
| Signal | Value |
|---|---|
| Today's status | 🔴 DEGRADED — ISS-006 day 12; morning EDA pocket silent, 08:00 batch recovered ~34m late (mirror image of 07-01) |
| Cron-state | all 42 tracked skills at `last_status: success`, 0 `dispatched`, 0 `consecutive_failures ≥ 3`; cumulative `success_rate` < 0.5 on 38 skills (ISS-001 OAuth-residue catch-up, day 12) |
| Enabled skills | 44 — 42 in cron-state.json, `ai-framework-watch` (Mon 08:30) and `run-frequency-guard` (daily 23:00) still never-dispatched despite being enabled |
| Open issues | 4 on disk, 4 in INDEX.md (ISS-001, 002, 005, 006) — ISS-005 reclassify still pending |
| Resolved | ISS-003 (cost-report), ISS-004 (skill-health) — both lifted on OAuth restore |
| Pending branches | `agi-tracker/2026-06-29` (METR refit + 3 points); `notegraph/2026-06-29` (+3n/+46e); `fix/workflow-security-audit-2026-06-28` (16C/36H); `skill-graph/2026-06-28` (INIT 173 skills); `fix/workflow-security-audit-2026-06-21` (older RCE patch) — all blocked by repo policy "GitHub Actions is not permitted to create or approve pull requests" |
| Today's fired slots | 08:00 batch (heartbeat 08:35Z, batch-health, gitlawb-fleet-metrics, skill-freshness) · 11:00 pr-tracker · 16:00 code-health (skipped, no watched-repos.md) · surplus-pulse |
| Today's missed slots | 06:00 compute-futures-eda · 06:30 planner (5d silent since 2026-06-27T07:34Z, most painful signature) · 06:xx memory-flush · 06:xx memory-structural-dedupe |
| 2026-07-02 activity | Morning EDA batch OUTAGE (4/4 missing) · 08:00 batch recovered ~34m late · 3rd consecutive pocket-swap day per [[iss-006-pocket-recovery-is-noise]] · pr-tracker OR-filter 4th-day hold (Agent-Reach#436 6d, crosses stale threshold 2026-07-03 → tomorrow's run notifies) · skill-freshness FRESHNESS_OK (5th consecutive; mtime-blind constraint atomized as [[skill-freshness-mtime-blind-in-gha]]) |

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
