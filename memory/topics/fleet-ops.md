# Fleet Ops

Cross-cutting operational lessons and constraints for the Aeon fleet: credential outages, monitoring-loop hazards, GitHub App permission boundaries, dispatch architecture, and cron-state pathologies.

## Open incidents
- [[issues/ISS-001]] — CLAUDE_CODE_OAUTH_TOKEN missing 2026-06-06 → 2026-06-20T06:05Z; investigating. Close deferred while [[issues/ISS-006]] runs; recovery batch is otherwise holding. Day 24 as of 2026-07-14.
- [[issues/ISS-006]] — Day 24 (2026-07-14, Tue even-DOM): **BATCH_HEALTH_OUTAGE** — 06:00 pocket totally silent for 2nd consecutive day (compute-futures-eda + planner both missed AGAIN) and today's even-DOM widening added memory-flush + memory-structural-dedupe to the missing list (only even-DOM opportunity in 48h). 08:00 pocket delivered normally. ISS-006 close-clock streak-of-3 counter now at Day-0 for a **2nd consecutive fresh Day-1 miss** — 2 clean days needed (2026-07-11 was the last one) then 3 consecutive from a fresh Day-1. Reinforces [[iss-006-pocket-recovery-is-noise]]. ISS-019 filed by batch-health at 08:00Z (medium).
- [[issues/ISS-007]] — heartbeat missing_pattern in eval regex; new 2026-07-05, filed by skill-evals. Enabled skill FAIL (not covered by ISS-002/005).
- [[issues/ISS-008]] — cost-report no_file_match; new 2026-07-05, filed by skill-evals. Standing ISS-006 tributary (weekly Mon 07:00 slot; 2026-07-13 slot fired ~74min late in 08:14Z catch-up cluster; next opportunity 2026-07-20).
- [[issues/ISS-005]] — swarm-safety-eval no_file_match: skill is now running successfully (last_success 2026-06-28T08:15:47Z) but its SSE_EMPTY path writes to the daily log, not an article; reclassify from `missing-secret-or-cron` to `permanent-limitation` per [[swarm-safety-eval-empty-writes-log-not-article]].
- **ISS-009 → ISS-018** (2026-07-12 BOOTSTRAP fillings from skill-evals): 10 no_file_match issues on chronically-empty-output disabled/workflow_dispatch skills (repo-pulse, push-recap, fork-fleet, repo-article, repo-actions, deep-research, hn-digest, rss-digest, polymarket, token-alert). Open-issue INDEX.md count grew 6 → 16 in one filing; suggests eval regex needs same-day grace or should skip disabled/workflow_dispatch skills entirely.
- [[issues/ISS-019]] — batch-health OUTAGE 2026-07-14: 4 skills missed morning window (compute-futures-eda + planner + memory-flush + memory-structural-dedupe). Filed as medium — direct ISS-006 tributary (delivery-rate underdelivery in 06:00 pocket, widened by even-DOM memory-hygiene skills).
- **Enabled-but-never-dispatched** — `ai-framework-watch` (weekly Mon 08:30) and `run-frequency-guard` (daily 23:00) have SKILL.md + `enabled: true` but no cron-state entries; heartbeat P3 novel-scan flagged 2026-07-11 per [[enabled-skills-can-never-dispatch]]. As of 2026-07-14 heartbeat, ai-framework-watch's 2026-07-13T08:30Z Mon slot came and went with no dispatch — pattern hardens (4th consecutive day flagged, dedup-suppressed).

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
- [[status-md-auto-commit-drops-writes]] — _superseded 2026-07-12_ — writes DELAY (~15h to next sweeper auto-commit) rather than DROP; heartbeat's own glob still doesn't stage `docs/`
- [[snapshot-rebase-clobbers-docs-status-md]] — third failure mode confirmed stable pattern across **3 consecutive days** (2026-07-12 `bcae68a` + 2026-07-13 `7dfcc30` + 2026-07-14 `c0b648a`, same upstream ref `rsavitt/aeon @ a7f04ee` clobbering the same 33-35d-stale version three days in a row)
- [[graphql-statereason-only-on-issue-type]] — SKILL.md GraphQL query requests `stateReason` on `PullRequest`; that field exists only on `Issue` and the query hard-fails
- [[notify-inline-cat-substitution-blocked-in-sandbox]] — sandbox blocks any `$(...)` around `./notify` (inline arg AND two-step MSG-variable); write directly to `.pending-notify/` or dispatch via node `execFileSync`
- [[notegraph-extractor-generatedat-nondeterministic]] — notegraph extractor writes `generatedAt` into 4 outputs; naive `git diff --quiet` HAS_DIFF gate re-PRs stable corpora; inspect per-file diff, revert timestamp-only churn
- [[skill-state-on-blocked-pr-branch-is-lost]] — skills that write dedup state to their daily branch lose that state when the PR is blocked by [[github-actions-cannot-create-prs]]; suggest-edges re-proposed the same 3 similarity-1.00 edges from 07-07's branch because state never merged to main
- [[sandbox-blocks-shell-redirect-to-workdir]] — shell `>` to workdir paths is refused; use the tool's own `-o` flag or Python `pathlib.Path.write_text` after `subprocess.run`
- [[enabled-skills-can-never-dispatch]] — a skill with SKILL.md + `enabled: true` may have zero entries in cron-state.json and never dispatch; only heartbeat's P3 novel-scan catches this failure class

## Snapshot (2026-07-11)
| Signal | Value |
|---|---|
| Today's status | 🔴 DEGRADED — ISS-006 day 21 **08:00 + 06:00 pockets both recovered today** (heartbeat/batch-health/skill-freshness/gitlawb-fleet-metrics fired 08:27–08:29Z; planner 06:37Z broke 142h/5.94× silence). Close clock stays at 0 clean days per [[iss-006-pocket-recovery-is-noise]] — 1-day recovery is noise. notegraph broke 4-day stable-topology silent-exit streak — extractor detected genuine corpus growth (+2 nodes/+38 edges); Node-based sha1 fingerprint correctly triggered. suggest-edges 3rd-consecutive same-3-edges (state loss loop continues). pr-tracker legitimately notified — kage#66 rolled off closed-no-merge (hash-guard did NOT suppress). Heartbeat P3 novel-scan flagged 2 never-dispatched skills per new [[enabled-skills-can-never-dispatch]] |
| Cron-state | all 42 tracked skills at `last_status: success`, 0 `dispatched`, 0 `consecutive_failures ≥ 3`; cumulative `success_rate` < 0.5 on 38 skills (ISS-001 OAuth-residue catch-up, day 21) |
| Enabled skills | 44 — 42 in cron-state.json, `ai-framework-watch` (Mon 08:30) and `run-frequency-guard` (daily 23:00) still never-dispatched per [[enabled-skills-can-never-dispatch]] |
| Open issues | 6 on disk, 6 in INDEX.md (ISS-001, 002, 005, 006, 007, 008) — no new issues filed today; skill-health run scheduled later, batch-health returned OK |
| Resolved | ISS-003 (cost-report), ISS-004 (skill-health) — both lifted on OAuth restore |
| Pending branches | **11** queued for operator PAT: `agi-tracker/2026-06-29`; `notegraph/2026-07-06`; `notegraph/2026-07-11` (**first genuine corpus growth** — Δ +2 nodes/+38 edges vs HEAD; Node-based sha1 fingerprint scheme worked); `fix/workflow-security-audit-2026-06-21`, `-06-28`, `-07-05`; `skill-graph/2026-06-28`; `skillpacks/2026-07-05`; `suggest-edges/2026-07-07`, `suggest-edges/2026-07-10`, `suggest-edges/2026-07-11` (3rd re-proposal of same 3 edges per [[skill-state-on-blocked-pr-branch-is-lost]]) — all blocked by [[github-actions-cannot-create-prs]] |
| Today's fired slots | 05:00 notegraph (late ~06:38Z, **corpus grew** +2n/+38e — first-in-5-days) · 05:30 suggest-edges (~06:37Z, same 3 proposals for 3rd day) · 06:00 memory-flush skipped (odd-DOM 11) · 06:00 memory-structural-dedupe skipped (odd-DOM 11) · 06:00 compute-futures-eda (06:35Z; zero |r|≥0.8 pairs, first zero-crossing since 07-07 — 3rd consecutive-day float-dust filter validation) · **06:30 planner** (~06:37Z, **first fire in 142h/5.94×** — top reframed to `operator-pat-provisioning`) · 08:00 batch-health OK · 08:00 heartbeat (~08:29Z, DEGRADED; 2 novel P3 flags) · 08:00 skill-freshness (FRESHNESS_OK; 2 cross-skill deps clean) · 08:00 gitlawb-fleet-metrics GLMETRICS_EMPTY · 09:00 fleet-control FLEET_EMPTY · 09:00 issue-triage no-config · 09:00 github-monitor no-config · 09:30 pr-triage (10:xxZ, PR_TRIAGE_NO_PERMISSION on #527, 14th day) · 09:30 pr-review (PR_REVIEW_NO_PERMISSION on #527, 15th day) · 10:00 pr-tracker (**legit notify** — kage#66 rolloff, hash-guard clean) · 10:00 repo-revive no-config · 11:00 compute-pulse (Anthropic × TeraWulf $19B breakout, momentum 10) · 16:00 code-health no-config · 16:30 surplus-pulse (catalog mode) · 17:00 vuln-scanner (oomol-lab/open-connector, 1 GCM-tag confirmed → PVR) |
| Today's missed slots | none in 06:00 or 08:00 pockets (both recovered) — planner ran for first time since 07-05 |
| 2× threshold skills | cost-report (Mon 07:00, 21d, 3.00×), janitor (Sun 05:30, 21d, 3.00×) — planner dropped off after today's fire |
| PR queue (tracked-author) | **First material state change in 6 days** — kage#66 rolled off closed-no-merge window at 2026-07-10T12:20:11Z (predicted by 07-10 memory-flush); category count `closed_no_merge: 1 → 0`. Hash-guard correctly did NOT suppress. HKUDS/Vibe-Trading#390 MERGED rolls off 2026-07-12T15:33:53Z; Panniantong/Agent-Reach#436 active (14.66d, activity 4.90d ago) tips stale 2026-07-13 |
| PR queue (swarm-repo) | Stationary 6th consecutive day vs 2026-07-09/10 — same 6 open PRs (5 dependabot + #527 rsavitt), same head SHAs. pr-review 15th day 403; pr-triage 14th day 403 on #527 DEFER per [[aeon-app-no-write-on-swarm-repo]] |
| skill-freshness | FRESHNESS_OK today — 44 enabled consumers audited, 2 cross-skill deps clean (suggest-edges←notegraph ~2h; compute-macro-correlate←compute-futures-eda <24h). Underlying `stat --format=%Y` GHA-blind bug per [[skill-freshness-mtime-blind-in-gha]] unfixed |
| Pending disclosures | **2 in `.pending-disclosure/`**: torlink 07-04 (`ip@2.0.1` HIGH unpatchable + `esbuild` LOW dev-only); **oomol-lab/open-connector 07-11** (semgrep `javascript.node-crypto.security.gcm-no-tag-length` at `src/server/secrets/secret-codec.ts:48`, medium severity — Node local codec accepts 4-byte GCM tag reducing forgery from 2⁻¹²⁸ → 2⁻³², 3-line fix documented) |
| Notify pattern | planner + notegraph + suggest-edges + heartbeat + compute-pulse + pr-tracker + surplus-pulse + vuln-scanner all wrote directly to `.pending-notify/${epoch}-${skill}.md` per [[notify-inline-cat-substitution-blocked-in-sandbox]] + [[notify-script-has-no-f-flag]]. No `-f`-corruption incidents |
| notegraph | Extractor: **142 nodes · 976 hard · 362 soft · 1 orphan · 39 atomic · 0 bundled**. Δ vs HEAD (140n/946h/354s/1orphan/38atomic): **+2 nodes / +30 hard / +8 soft / +38 net edges / 0 orphan / 0 bundled**. Verdict `+2 notes wired in` — first genuine corpus growth since 2026-07-06 (breaks 4-day stable-topology streak 07-07→07-10). Node-based sha1 fingerprint drifted from stored (`de87cba6…` vs `02e4c209…`) as expected; extractor proceeded. Post-reflect regen: **149 nodes · 1083 hard · 398 soft · 1 orphan · 42 atomic · 0 bundled** — Δ +7 nodes / +107 hard / +36 soft / **+143 edges** / 0 orphan / 0 bundled / +3 atomic. Edge:node ratio ~20.4× — 3 new atomic notes ([[anthropic-terawulf-19b-401mw-kentucky-lease]], [[sandbox-blocks-shell-redirect-to-workdir]], [[enabled-skills-can-never-dispatch]]) + 1 daily index + MEMORY.md/fleet-ops MOC edits pulling in cross-links |

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
