# Self Review — 2026-07-12

**Window:** 2026-07-05 → 2026-07-12 (7 days · ISS-006 days 15 → 22)
**Verdict:** DEGRADED_STABLE
Fleet dispatches when it fires, but the same **three meta-blockers** stall every downstream fix — cron underdelivery (ISS-006), GitHub Actions PR-creation policy, and OAuth-outage denominator burn (ISS-001). One net-new failure class emerged this week: `docs/status.md` writes have now failed in three distinct ways.

## Headline numbers

| Metric | Value |
|---|---|
| Skills tracked in `cron-state.json` | 42 |
| Skills `last_status: success` | 42 / 42 (100%) |
| Skills with `success_rate < 0.5` while currently OK | 38 (denominator burn from ISS-001) |
| Skills stale > 48h | 7 (weekly cadence + skill-analytics 95h) |
| Open issues start / end of window | 6 / 16 (+10 today from skill-evals BOOTSTRAP) |
| Staged branches blocked from PR | 11 (unchanged) |
| MEMORY.md length | 57 lines (target ≤50) |
| New articles committed to main | 2 (both today; content skills continue writing to blocked branches) |
| ISS-006 clean days in trailing 7 | 1 (2026-07-11 only) |

## 1. Output quality

**Substantive this week:**
- `vuln-scanner` 2026-07-11 — real GCM-tag-length finding on `oomol-lab/open-connector` with 3-line fix documented (PVR draft queued to `.pending-disclosure/`).
- `compute-pulse` 2026-07-11 — Anthropic × TeraWulf $19B / 401 MW Kentucky lease (Jul 6 announcement) surfaced and durabilized as an atomic claim.
- `planner` 2026-07-11 — first fire in 142 h and delivered a stuck-goal escalation from `iss-006-messages-yml-per-slot-crons` → `operator-pat-provisioning`, reframing the top priority correctly.
- `workflow-security-audit` 2026-07-05 — 70 findings + 13/16 critical unpinned-uses tracked as RESOLVED across prior runs.
- `notegraph` 2026-07-11 — first genuine corpus-growth run in 5 days (+2 nodes / +38 edges); fingerprint scheme correctly detected drift and let the extractor proceed.
- `compute-futures-eda` (multi-day) — 3rd consecutive-day validation that `wallet_sum_pnl` |r|≥0.8 crossings collapse under a σ filter; 07-11 produced zero |r|≥0.8 pairs in any mode.
- `reflect` — 5 new atomic notes across the window, single-claim and well-linked.

**Formulaic / repeat wallpaper:**
- `surplus-pulse` — 7 identical spot / curve / x402 blocks; catalog mode has no new signal.
- `skill-freshness` — same template `FRESHNESS_OK` for 10+ consecutive runs; structurally mtime-blind in GHA per [[skill-freshness-mtime-blind-in-gha]].
- `skill-health` — 15 consecutive days of identical `DEGRADED(38)` classification driven by ISS-001 denominator; the cadence-only fires are wallpaper, not signal.

**Chronic no-op (produced zero useful output all week):**
- Watched-repos-dependent quintet: `code-health`, `github-monitor`, `issue-triage`, `changelog`, `weekly-shiplog` — silent skip every run for 22 consecutive days.
- Empty-config skips: `fleet-control` (FLEET_EMPTY), `gitlawb-fleet-metrics` (GLMETRICS_EMPTY), `swarm-safety-eval` (SSE_EMPTY), `stale-content-pr-sweeper` (0 PRs), `skill-update-check` (no lock), `repo-revive` (REPO_REVIVE_NO_CONFIG).

## 2. Reliability

**Repeated failure patterns (all still open):**

| Pattern | Days | Root cause |
|---|---|---|
| `gh pr create` → 403 "GitHub Actions is not permitted to create or approve PRs" | 22 | Org policy — needs operator PAT |
| swarm-repo 403 `Resource not accessible by integration` on PR write | 17 | `aeon` GitHub App has no write on `swarm-ai-research/swarm` |
| `./notify -f` documented but unsupported; `$(cat file)` blocked; `MSG=$(...)` also blocked | ≥7 | Sandbox blocks command substitution — only direct `.pending-notify/` writes work |
| `pr-tracker` ships broken `stateReason` GraphQL + AND-filter drop | ≥12 | SKILL.md drift; batched patch pending |
| `docs/status.md` write loss | ≥7 | Three distinct failure modes now observed: silent drop → delayed landing via sweeper → snapshot-rebase clobber |
| `notegraph` `generatedAt` non-determinism triggers false NO_CHANGE gate | 4 (07-07 → 07-10 stable-topology streak broken 07-11) | Extractor timestamp masking missing |

**Monitor efficacy:**
- **heartbeat** — catching real problems (P3 novel-scan flagged `ai-framework-watch` + `run-frequency-guard` as never-dispatched; caught snapshot-rebase clobber). **Signal, not wallpaper.**
- **batch-health** — correctly caught 08:00-pocket outage 07-09/07-10 (2 consecutive days first-ever) and recovery 07-11. **Signal.**
- **skill-health** — 15 identical DEGRADED(38) days on ISS-001 denominator burn. **Wallpaper until ISS-001 closes.**
- **skill-freshness** — 10+ identical FRESHNESS_OK. **Wallpaper.**
- **skill-evals** — bootstrap fire today filed 10 new issues (ISS-009 → ISS-018), all `no_file_match` on skills that never dispatched. Likely all tributaries of ISS-006 / ISS-001 rather than independent bugs. **Noise until BOOTSTRAP settles.**

**Novel this week:**
- 2026-07-09 — first-ever full 08:00-pocket silence (batch-health / heartbeat / skill-freshness / gitlawb-fleet-metrics all missed).
- 2026-07-11 — heartbeat P3 discovered two enabled skills (`ai-framework-watch`, `run-frequency-guard`) that never once dispatched despite `enabled: true` + present SKILL.md.
- 2026-07-11 — `docs/status.md` write actually landed (delayed 15+h) via stale-content-pr-sweeper — reclassifies the failure from "silent drop" to "delayed landing", and heartbeat then caught a snapshot-rebase clobber shortly after.

## 3. Memory hygiene

- `MEMORY.md`: 57 lines (target ≤50). Content is load-bearing and mostly < 4 days old; no obviously stale entries safe to prune from self-review. Recommend memory-flush trim the `docs/status.md` block once the atomic note is updated to reflect "delay not drop."
- Logs are well-structured across all 7 days — every log has per-skill sections, verdicts, and a `_OK / _WARN / _EMPTY` suffix.
- `.pending-disclosure/` reconciled today: canonical count is **1 entry** (07-11 GCM-tag), not "2" as the 2026-07-11 flush claimed — the 07-04 torlink entry was silently wiped by snapshot `323965d0` at 2026-07-05T07:16:05Z. Contradiction resolved in MEMORY.md line 23.
- Issue tracker grew from 6 → 16 open. 10 of the 10 new are BOOTSTRAP `no_file_match` — likely need to be re-scoped as tributaries of ISS-006 rather than independent issues, or those skills should be disabled outright.

## 4. Recommendations

**Top 3 (do these first):**
1. **Provision the operator PAT.** This is the single unblocker for 11 staged branches, ~6 skill-fix PRs, and every recurring `gh pr create` 403. `planner` correctly reframed this as the top priority on 07-11 — the review agrees.
2. **Land the `pr-tracker` SKILL.md batch patch** (a–e in MEMORY.md line 51). Every day it runs with the shipped SKILL.md is a day the fix hasn't landed. Batch-e (fresh-bot-PR trigger) closes the most user-visible gap.
3. **Disable or reclassify the never-dispatched decile.** `repo-pulse`, `push-recap`, `fork-fleet`, `repo-article`, `repo-actions`, `deep-research`, `hn-digest`, `rss-digest`, `polymarket`, `token-alert`, `ai-framework-watch`, `run-frequency-guard` — either wire them into `messages.yml` / `aeon.yml` or set `enabled: false`. Otherwise skill-evals will re-file ISS-009 → ISS-018 every run and the issue tracker becomes noise.

**Secondary:**
4. Populate `memory/watched-repos.md` or set `enabled: false` on the 5 watched-repos skills — 22 consecutive daily wasted workflow slots each.
5. Fix `messages.yml` heartbeat auto-commit `git add` glob to include `docs/` — reduces the ~15 h status.md staleness to same-run.
6. Add a σ filter to `compute-futures-eda` — filter `wallet_sum_pnl` correlations until σ > 1e-6. Three consecutive days of validation is enough to promote from atomic claim to skill patch.
7. Widen `scenario-sweep.mjs` seed count and switch outlier detection to a tie-robust statistic per [[compute-futures-12-seed-sample-too-small]].
8. Close ISS-007 as false positive (heartbeat *did* run 2026-07-05; skill-evals scanned before the late slot fired) OR add a same-day grace window (scan after 12:00 UTC).
9. Move ISS-005 from `missing-secret-or-cron` → `permanent-limitation` (SSE_EMPTY writes to log by design).
10. Fix `skill-freshness` to use `git log -1 --format=%ct` instead of `stat --format=%Y` (structural GHA blind spot).

**Deferred:**
- ISS-001 close — hold until ISS-006 stabilizes (streak-of-3 clean days; currently at 1).

## 5. Actions taken this run

- Wrote this review to `articles/self-review-2026-07-12.md`.
- Logged to `memory/logs/2026-07-12.md`.
- Notification queued via `./notify`.
- No unilateral MEMORY.md pruning: everything in the file is < 4 days old and load-bearing.
- No aeon.yml edits: disabling the never-dispatched decile is a real config change with blast radius; leaving as an operator recommendation.

## Sources
- `memory/MEMORY.md` (57 lines, current)
- `memory/logs/2026-07-05.md` … `2026-07-12.md` (2,119 lines total)
- `memory/cron-state.json` (42 skills)
- `memory/issues/INDEX.md` (16 open)
- `articles/skill-evals-2026-07-12.md` (BOOTSTRAP)
- `articles/skill-freshness-2026-07-12.md`
