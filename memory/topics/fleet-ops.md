# Fleet Ops

Cross-cutting operational lessons and constraints for the Aeon fleet: credential outages, monitoring-loop hazards, GitHub App permission boundaries, dispatch architecture, and cron-state pathologies.

## Open incidents
- [[issues/ISS-001]] — CLAUDE_CODE_OAUTH_TOKEN missing 2026-06-06 → 2026-06-20T06:05Z; investigating. Close deferred while [[issues/ISS-006]] runs; recovery batch is otherwise holding.
- [[issues/ISS-006]] — Day 19: **odd-DOM 08:00-pocket full-silence signature (NEW)** — batch-health / heartbeat / skill-freshness / gitlawb-fleet-metrics ALL silent on today's 08:00 UTC slot; first day the entire 08:00 pocket has failed since the outage opened (prior pocket-miss days always at least late-fired the 08:00 batch). 06:00 pocket late-fired 06:32Z–06:36Z (notegraph, suggest-edges, compute-futures-eda). Planner (06:30) still silent — now at 82h / ~4.4× threshold. Sharpens vs Day-18 planner-only-silent (which was a partial 06:00 recovery, 08:00 fully delivered). Same underlying delivery-rate bug per [[gha-messages-yml-cron-underdelivery]], different pocket manifesting. Close clock resets 0 consecutive clean days.
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
- [[compute-futures-eda-wallet-sum-pnl-correlations-are-float-dust]] — wallet_sum_pnl σ ≈ 6e-12 means |r|≥0.8 crossings against volume columns (settlementLegs, realizedAbs, x402Total) are float-dust artifacts, not P&L signal; drop from the finding ladder
- [[skill-freshness-mtime-blind-in-gha]] — `actions/checkout` resets every file's mtime to the run instant, so skill-freshness's `stat --format=%Y` age check can never flag anything in GHA; switch to `git log -1 --format=%ct` producer-commit timestamp
- [[aeon-bot-uses-multiple-signing-identities]] — aeon bot signs commits under both `aeonframework@users.noreply.github.com` and `aeon@aeonframework.dev`; single-value `BOT_EMAIL` drops PRs silently
- [[pr-tracker-step-5-misses-fresh-bot-prs]] — pr-tracker only notifies on merges / stale / closed-no-merge; brand-new bot PRs land invisibly until they age into staleness
- [[pr-tracker-notify-repeats-with-no-state-change]] — step-5 has no dedup guard; a persistent stale/closed-no-merge state fires an identical notify every day until the wall clock rolls a PR off the 7d window
- [[notify-script-has-no-f-flag]] — `./notify -f <file>` is documented across multiple SKILLs but the actual script takes message as `$1`; using `-f` writes the literal `-f` as the message body
- [[status-md-auto-commit-drops-writes]] — heartbeat rewrites of `docs/status.md` are silently lost by the workflow auto-commit step; on-disk status page ages indefinitely
- [[graphql-statereason-only-on-issue-type]] — SKILL.md GraphQL query requests `stateReason` on `PullRequest`; that field exists only on `Issue` and the query hard-fails
- [[notify-inline-cat-substitution-blocked-in-sandbox]] — sandbox blocks any `$(...)` around `./notify` (inline arg AND two-step MSG-variable); write directly to `.pending-notify/` or dispatch via node `execFileSync`
- [[notegraph-extractor-generatedat-nondeterministic]] — notegraph extractor writes `generatedAt` into 4 outputs; naive `git diff --quiet` HAS_DIFF gate re-PRs stable corpora; inspect per-file diff, revert timestamp-only churn

## Snapshot (2026-07-09)
| Signal | Value |
|---|---|
| Today's status | 🔴 DEGRADED — ISS-006 day 19 **odd-DOM 08:00-pocket full-silence signature (first-ever)**: batch-health / heartbeat / skill-freshness / gitlawb-fleet-metrics all silent today; 06:00 pocket late-fired 06:32Z–06:36Z; planner (06:30) still silent, now 82h / ~4.4×; pr-tracker **skipped-dedup** via inline hash-based guard (first-time-applied — validates the fix from [[pr-tracker-notify-repeats-with-no-state-change]]) |
| Cron-state | all 42 tracked skills at `last_status: success`, 0 `dispatched`, 0 `consecutive_failures ≥ 3`; cumulative `success_rate` < 0.5 on 38 skills (ISS-001 OAuth-residue catch-up, day 19) |
| Enabled skills | 44 — 42 in cron-state.json, `ai-framework-watch` (Mon 08:30) and `run-frequency-guard` (daily 23:00) still never-dispatched despite being enabled |
| Open issues | 6 on disk, 6 in INDEX.md (ISS-001, 002, 005, 006, 007, 008) — no new issues filed today; batch-health didn't run so no OUTAGE/WARN classification generated |
| Resolved | ISS-003 (cost-report), ISS-004 (skill-health) — both lifted on OAuth restore |
| Pending branches | **9** queued for operator PAT: `agi-tracker/2026-06-29`; `notegraph/2026-07-06` (still queued — 2026-07-07/08/09 extractor runs ALL produced identical topology, Day 3 stable-topology silent-exit per [[notegraph-extractor-generatedat-nondeterministic]]); `fix/workflow-security-audit-2026-06-21`, `-06-28`, `-07-05`; `skill-graph/2026-06-28`; `skillpacks/2026-07-05`; `suggest-edges/2026-07-07` — all blocked by "GitHub Actions is not permitted to create or approve pull requests" |
| Today's fired slots | 05:00 notegraph (late 06:33Z, NO_CHANGE Day 3) · 05:30 suggest-edges (late 06:32Z) · 06:00 compute-futures-eda (late 06:36Z, first-ever wallet_sum_pnl \|r\|≥0.8 crossing — float dust per new [[compute-futures-eda-wallet-sum-pnl-correlations-are-float-dust]]) · 09:00 fleet-control + issue-triage + github-monitor (all no-op, late 10:07Z) · 09:30 pr-triage (10:10Z, PR_TRIAGE_NO_PERMISSION on #527) · 10:00 pr-tracker (10:09Z, skipped-dedup via inline hash-guard) · 16:00 code-health (no-op) · 16:30 surplus-pulse (17:55Z) · 18:00 pr-review (11th day 403 on #527 verdict post) |
| Today's missed slots | planner 06:30 · **08:00 pocket full-silence: batch-health + heartbeat + skill-freshness + gitlawb-fleet-metrics all silent** (first-ever full-08:00 miss); memory-flush / -structural-dedupe not eligible (odd-DOM) |
| 2× threshold skills | cost-report (Mon 07:00, 19d, 2.7×), janitor (Sun 05:30, 19d, 2.7×), planner (daily 06:30, 82h, 4.4×) |
| PR queue (tracked-author) | Stationary — same 3 PRs, same buckets, same head SHAs as 2026-07-07/08. HKUDS/Vibe-Trading#390 MERGED; Panniantong/Agent-Reach#436 active; tamnd/kage#66 CLOSED no-merge (rolls off 7d window 2026-07-10). pr-tracker inline hash-dedup guard applied → skipped-dedup (validates SKILL.md patch line-item from [[pr-tracker-notify-repeats-with-no-state-change]]) |
| PR queue (swarm-repo) | Moved — 3 fresh dependabot PRs opened 2026-07-09 05:36–05:38Z (#530 langchain-core, #531 langgraph 1.2.8, #532 setuptools) join #524/#527/#529; 4→6. pr-review still blocked (11th day 403); pr-triage got same 403 on #527 DEFER verdict (PR_TRIAGE_NO_PERMISSION, no state file append so retry re-fires) per [[aeon-app-no-write-on-swarm-repo]] |
| skill-freshness | FRESHNESS_OK counter **stalled at 10** (2026-07-09 08:00 slot never fired); compute-pulse.md at ~120h/168h (71%) after skipping today's audit — tips WARN if compute-pulse misses 2026-07-11 11:00 UTC |
| Pending disclosures | 1 in `.pending-disclosure/` (torlink 07-04: `ip@2.0.1` HIGH unpatchable + `esbuild` LOW dev-only) — no change today |
| Notify pattern | pr-tracker + surplus-pulse both wrote directly to `.pending-notify/${epoch}-${skill}.md` per updated [[notify-inline-cat-substitution-blocked-in-sandbox]]. No `-f`-corruption incidents today (SKILL.md step 6 mishap from 07-08 not repeated) |
| notegraph | Morning extractor: 134n · 909h + 365s / 1 orphan / 0 bundled (identical topology to HEAD — **Day 3** stable-topology silent-exit per [[notegraph-extractor-generatedat-nondeterministic]]). Only `generatedAt` + a few weight-rounding lines diff'd; reverted via `git checkout --`. State realigned from stale 130n/1184e (2026-07-08 state file lag) to actual 134n/1274e. Post-reflect regen delta below |

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
