# Fleet Ops

Cross-cutting operational lessons and constraints for the Aeon fleet: credential outages, monitoring-loop hazards, GitHub App permission boundaries, dispatch architecture, and cron-state pathologies.

## Open incidents
- [[issues/ISS-001]] — CLAUDE_CODE_OAUTH_TOKEN missing 2026-06-06 → 2026-06-20T06:05Z; investigating. Close deferred while [[issues/ISS-006]] runs; recovery batch is otherwise holding.
- [[issues/ISS-006]] — Day 18: **Wed even-DOM planner-only-silent signature** — memory-flush (06:00 slot) + memory-structural-dedupe (06:10) + compute-futures-eda (06:00) + notegraph (05:00) + suggest-edges (05:30) all late-fired 06:26Z–06:34Z, clearing multi-day silences; batch-health 08:00 late ~54m (WARN, 1 miss = planner only); heartbeat 08:00 late ~66m. Only planner (06:30 daily) still silent through today. This is a *sharpening* vs the prior even-DOM 5-missing OUTAGE signature (days 4/6/8/10/12/16), NOT resolution — one clean-ish day is not signal per [[iss-006-pocket-recovery-is-noise]]. Close clock 0 consecutive clean days.
- [[issues/ISS-007]] — heartbeat missing_pattern in eval regex; new 2026-07-05, filed by skill-evals. Enabled skill FAIL (not covered by ISS-002/005).
- [[issues/ISS-008]] — cost-report no_file_match; new 2026-07-05, filed by skill-evals. Standing ISS-006 tributary (weekly Mon 07:00 slot at 2.4× threshold, silent 3rd consecutive Monday).
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
- [[notify-inline-cat-substitution-blocked-in-sandbox]] — sandbox blocks any `$(...)` around `./notify` (inline arg AND two-step MSG-variable); write directly to `.pending-notify/` or dispatch via node `execFileSync`
- [[notegraph-extractor-generatedat-nondeterministic]] — notegraph extractor writes `generatedAt` into 4 outputs; naive `git diff --quiet` HAS_DIFF gate re-PRs stable corpora; inspect per-file diff, revert timestamp-only churn

## Snapshot (2026-07-08)
| Signal | Value |
|---|---|
| Today's status | 🔴 DEGRADED — ISS-006 day 18 Wed even-DOM planner-only-silent signature (5 morning-pocket skills late-cleared 06:26Z–06:34Z, only planner remained silent; batch-health WARN 1-miss); `docs/status.md` auto-commit dropped **4th consecutive day**; pr-tracker fired **3rd consecutive zero-state-change notify** (dedup guard from [[pr-tracker-notify-repeats-with-no-state-change]] would have suppressed); pr-tracker's `-f` invocation from SKILL.md step 6 corrupted the queued payload → recovered by in-place `.pending-notify/` rewrite (new working recovery in updated [[notify-script-has-no-f-flag]]) |
| Cron-state | all 42 tracked skills at `last_status: success`, 0 `dispatched`, 0 `consecutive_failures ≥ 3`; cumulative `success_rate` < 0.5 on 38 skills (ISS-001 OAuth-residue catch-up, day 18) |
| Enabled skills | 44 — 42 in cron-state.json, `ai-framework-watch` (Mon 08:30) and `run-frequency-guard` (daily 23:00) still never-dispatched despite being enabled |
| Open issues | 6 on disk, 6 in INDEX.md (ISS-001, 002, 005, 006, 007, 008) — no new issues filed today; batch-health WARN threshold below OUTAGE-file-issue tier |
| Resolved | ISS-003 (cost-report), ISS-004 (skill-health) — both lifted on OAuth restore |
| Pending branches | **9** queued for operator PAT: `agi-tracker/2026-06-29`; `notegraph/2026-07-06` (still queued — 2026-07-07 and 2026-07-08 extractor runs both produced identical topology per [[notegraph-extractor-generatedat-nondeterministic]]); `fix/workflow-security-audit-2026-06-21`, `-06-28`, `-07-05`; `skill-graph/2026-06-28`; `skillpacks/2026-07-05`; `suggest-edges/2026-07-07` — all blocked by "GitHub Actions is not permitted to create or approve pull requests" |
| Today's fired slots | 05:00 notegraph (late 06:34Z, NO_CHANGE) · 05:30 suggest-edges (late 06:28Z) · 06:00 memory-flush (late 06:26Z) + compute-futures-eda (late 06:31Z) · 06:10 memory-structural-dedupe (late 06:26Z) · 08:00 batch-health (~54m late, WARN) + heartbeat (~66m late) + skill-freshness + gitlawb-fleet-metrics (empty) · 09:00 fleet-control + issue-triage + github-monitor (all no-op) · 10:00 pr-tracker (3rd zero-state-change notify) · 16:30 surplus-pulse |
| Today's missed slots | planner 06:30 (only miss in the 06:00–07:30 pocket) — sharpens ISS-006 signature to planner-only |
| 2× threshold skills | cost-report (Mon 07:00, 18d, 2.6×), janitor (Sun 05:30, 18d, 2.6×), planner (daily 06:30, 73h, 3×) — memory-structural-dedupe, compute-futures-eda, stale-content-pr-sweeper flags all **cleared today** |
| PR queue | Stationary — same 3 PRs, same buckets, same head SHAs as 2026-07-07. HKUDS/Vibe-Trading#390 still MERGED; Panniantong/Agent-Reach#436 still active (`updatedAt` 2026-07-06T13:32:11Z); tamnd/kage#66 still CLOSED no-merge (rolls off 7d window 2026-07-10). pr-tracker notify fired anyway per SKILL.md step 5 gate; would have been suppressed by hash-based dedup guard flagged in [[pr-tracker-notify-repeats-with-no-state-change]] |
| skill-freshness | FRESHNESS_OK 10th consecutive emit — structurally blind in GHA per [[skill-freshness-mtime-blind-in-gha]]; compute-pulse.md at 96h/168h (57%) — tips WARN if compute-pulse misses 2026-07-11 11:00 UTC |
| Pending disclosures | 1 in `.pending-disclosure/` (torlink 07-04: `ip@2.0.1` HIGH unpatchable + `esbuild` LOW dev-only) — no change today |
| Notify pattern | batch-health + pr-tracker + surplus-pulse all wrote directly to `.pending-notify/${epoch}-${skill}.md` per updated [[notify-inline-cat-substitution-blocked-in-sandbox]]. pr-tracker's step-6 `./notify -f` invocation corrupted the initial queue; recovered by in-place payload rewrite — updated [[notify-script-has-no-f-flag]] captures this as the only working recovery |
| notegraph | Morning extractor: 130n · 842h + 342s (identical topology to HEAD → `NOTEGRAPH_NO_CHANGE`, no branch). Only `generatedAt` differed across 4 outputs (plus 5 minor weight roundings and one tie-break swap on a soft edge). Reverted per [[notegraph-extractor-generatedat-nondeterministic]]. Post-reflect regen delta recorded below |

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
