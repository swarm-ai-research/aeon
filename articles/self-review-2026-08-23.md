# Self-Review — 2026-08-23

Weekly audit of what the agent did, what failed, and what to improve. Window: 2026-08-17 → 2026-08-23 (7 days, Mon → Sun).

## TL;DR

- **Reliability is strong on the surface** — 0 fresh failures, 0 dispatched-stuck, 4/42 truly healthy, 38 chronic-DEGRADED via ISS-001 residue (Day-66; substantively green per skill-health 57th steady-state day).
- **Quality has one structural leak: article outputs don't land on main.** `git log` shows a **single commit on `main` this week** (`73eba91 chore(cron): skill-graph success`). Every article-based skill writes to `articles/` on an ephemeral GHA runner; nothing commits. Today's skill-evals BOOTSTRAP flagged **13 skills as `no_file_match`** for exactly this reason. This is the highest-leverage single fix on the board.
- **Merge-flow proof stuck at Day 17.** 23 open aeon-repo PRs, 0 `app/github-actions` merged since #8 on 2026-08-07 (~389h+). Planner escalation now at day 6, path collapsed to a one-liner (`gh pr comment 26 -b "@dependabot rebase"`) operator hasn't posted. Agi-tracker deadline hits **tomorrow 2026-08-24T13:00Z** — 8th silent-Mon fire imminent.
- **Notifications hygiene is working.** Queue-level hash-dedup live (dropped identical pr-tracker payloads across the 4-day byte-freeze); `.pending-notify/` and `.notify-sent-hashes` both empty at self-review time; heartbeat correctly suppressed almost every day this week via 48h dedup rule.
- **Recommendations (2–3):** (a) audit `articles/` write vs. commit paths and land a single commit-outputs fix (unblocks ISS-002/005/008–018 in one shot); (b) trim MEMORY.md from 64 → ≤50 lines by demoting focus bullets that have been static ≥7 days into `memory/topics/`; (c) escalate the agi-tracker `enabled: false` PR before Monday's 13:00Z fire.

## 1. Quality audit

### Articles
`ls articles/` shows **3 files** total today (skill-evals-2026-08-23, skill-freshness-2026-08-23, workflow-security-audit-2026-08-23). All three were written by today's Sunday cadence and are only present because the runner hasn't torn down yet. Locally-produced files this week per the log transcripts:

| Day | Articles written locally | Committed to main? |
|-----|--------------------------|--------------------|
| 08-17 | cost-report, skill-freshness | no |
| 08-18 | skill-freshness | no |
| 08-19 | skill-analytics, skill-freshness | no |
| 08-20 | skill-freshness | no |
| 08-21 | skill-freshness | no |
| 08-22 | vuln-scan (`.pending-disclosure/`), skill-freshness | no |
| 08-23 | skill-evals, skill-freshness, workflow-security-audit | pending |

Compute-futures-eda writes daily findings under `memory/topics/compute-futures-eda/`, and those DO reach `fleet-state`. But nothing on `articles/` reaches `main` — daily-log traces show reasoned, substantive output; the delivery path drops it.

**Substantive or formulaic?** The daily logs are substantive: today's planner isolated a specific ShellCheck job blocking PR #26 by name (`95256043957`); today's pr-tracker caught the deepsec#161 fresh-open that broke the 4-day byte-freeze; today's compute-futures-eda flagged the basket/synth 2.5000× multiplier hitting its rename threshold at n=5. The reasoning is there. The artifact form (log entry under `memory/logs/`) is wrong for downstream consumption.

**Formulaic areas worth naming:**
- **pr-review** on swarm-ai-research/swarm — 58 invocations, byte-identical skip verdicts (7 bot-author + 2 dup-SHA), standing verdicts frozen at APPROVE 5/5 (#543) / REQUEST_CHANGES 2/5 (#549) for ~16d. Under dup-SHA suppression these produce zero on-GitHub writes but still log ~300 words per invocation. Combined with pr-triage (40 invocations, 100%-skip cohort), **98 operator invocations against the same frozen queue with zero writes attempted** ([[aeon-app-no-write-on-swarm-repo]] gap unexercised).
- **pr-tracker** — 4 consecutive byte-identical tuples `(0, 9, 1, 0)` across 08-19→08-22; today (08-23) broke to `(0, 9, 1, 1)` on the deepsec#161 fresh-open, so the class isn't fully static, but the SKILL-level hash dedup (patch bundle item (d)) remains 60d overdue. Queue-layer dedup masks the log churn from operator view but doesn't eliminate the `.pending-notify/` writes.
- **notegraph + suggest-edges** — each opens one PR per day (5m–7m cadence, all clean since 08-20). Sweeper closed 8 stale in operator-invocations 08-21 + 08-22, but next-morning cron re-supersedes. Churn without merges.

### PR comments posted
Two operator-visible posts this week: pr-review 57th (08-22) → posted verdicts on swarm#543 + #549. All other pr-review / pr-triage invocations correctly suppressed writes under dup-SHA / bot-author rules.

### Notifications
Roughly 5–8 notifies per day per the log summaries. Distribution mostly good — planner + heartbeat correctly dedup most days. One P0-fresh notify triggered 08-19 (notegraph stuck-callback recurrence, resolved 08-20 with 5m30s success). Cost-report 08-17 flagged $396.85 / 69 runs (+50.8% WoW, monthly projection $1,700.77). No noisy or fabricated notifies this week.

## 2. Reliability audit

### Skills ran vs expected
- **42 skills tracked in cron-state.json.** Sunday snapshot: 0 `last_status: failed`, 0 `last_status: dispatched`, 0 `total_runs: 0`. Every tracked skill shows `last_status: success` + `consecutive_failures: 0`.
- **4 truly healthy** (`agi-tracker` HEALTHY-but-empty, `config-validator`, `swarm-safety-eval`, `weekly-shiplog`).
- **38 DEGRADED** by success_rate ≥ 5 runs & < 0.5 — chronic ISS-001 residue Day-66, all substantively green per skill-health hash `e27c0ac6` steady-state 57th day. Status page shows 🔴 but this is structural noise, not fresh-fresh.
- **2 never-dispatched (absent from cron-state.json entirely):** `ai-framework-watch` (weekly Mon 08:30) + `run-frequency-guard` (daily 23:00) — **47 consecutive silent days**. Structurally broken per [[enabled-skills-can-never-dispatch]]; ISS-021 draft is a carryover item.
- **`agi-tracker` (weekly Mon 13:00)** — dispatches as no-op because SKILL.md is missing per [[agi-tracker-missing-skill-md-dispatches-no-op]]. 7th silent-Mon fire logged 2026-08-17T13:25Z; 8th fires tomorrow 2026-08-24T13:00Z.

### Repeated errors / failure patterns
- **1 fresh P0** this week: notegraph stuck 08-19 (dispatched 05:25Z, still elapsed at heartbeat 2h38m past 45-min threshold). Resolved 08-20 with 5m30s success. Recurrence of [[skill-freshness-stuck-dispatched-callback-never-fires]] (first since 2026-07-25).
- **Batch outages:** none this week (batch-health OK on all 7 days). Note: three Sunday-morning skills drifted past scheduled minute today (planner ~30m, compute-macro-correlate ~30m, swarm-safety-eval ~10m past window) — all completed successfully, so batch-health counted OK.
- **6-skill silent-short-circuit cluster** on missing `memory/watched-repos.md` — streak-18 chronic (code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive). 3-of-6 same-day today (code-health, issue-triage, github-monitor).

### Are monitors catching real issues?
- **heartbeat:** correctly caught the 08-19 notegraph stuck, sent fresh notify (not a dedup). Suppressed on every other day via 48h dedup — correct.
- **skill-evals:** BOOTSTRAP today; caught 13 NO_OUTPUT article-based skills as regressions vs. existing open ISSs (correct — every one matched an existing issue, no false positives filed). Closed ISS-007 (heartbeat missing_pattern) — real close, pattern now found.
- **workflow-security-audit:** UNCHANGED verdict, 78 findings carried over from 08-09 baseline (13 with fingerprint drift on top-level blocks — flagged for fingerprint-algo standardization in SKILL body).
- **skill-freshness:** all-green every day, but [[skill-freshness-mtime-blind-in-gha]] structural gap active — checks always pass on ephemeral runners regardless of true age. Still filing FRESHNESS_OK verdicts — under-catching real staleness.
- **pr-tracker:** predictor for today's tuple missed `(0, 9, 1, 1)` because deepsec#161 opened AFTER yesterday's scan window; anniversary-only rolloff predictor is blind to fresh opens per [[pr-tracker-step-5-misses-fresh-bot-prs]]. Correctly flagged.
- **milestone-tracker:** ms-01 stalled-6 (stars 0/100 unchanged for 6 weeks) — signal is real; landed 08-17 12:00Z on schedule, next fire tomorrow 2026-08-24T12:00Z.

## 3. Memory hygiene

- **MEMORY.md is 64 lines** — target ≤50 per CLAUDE.md convention, **+14 lines over**. Content is index-shape (pointer-only) but focus bullets have grown dense (each ~2–5 lines of nested status). Candidates for demotion to topic files:
  - Operator PR-authoring UNBLOCK / merge-path bullet → collapse into `memory/topics/pr-status.md` header snapshot
  - ISS-006 pocket-slot migration Day-20 → `memory/topics/fleet-ops.md`
  - `.pending-disclosure/` queue at 6 → `memory/topics/pr-status.md` or a new `vuln-scanner.md`
  - Cost pulse Mon 08-17 → `memory/topics/cost.md` (would be new) OR left in place, but note new cost-report is due tomorrow 08-24 and will supersede
- **Structured logs:** every day this week uses consistent per-skill sections + `## Summary (skill)`. Good.
- **Stale data:**
  - `memory/state/daily-plan-2026-*` accumulates one file per day — 30+ files, oldest 2026-06-20. Nothing prunes them. Not harmful but growing.
  - `memory/notes/daily/` has a gap 07-11 → 08-17 (reflect skill stopped producing daily indexes for 5 weeks). Not urgent, but worth reconciling.
  - `.audit/` directory (per today's workflow-security-audit log) is not in `.gitignore` — untracked here but worth adding.
- **Issue tracker:** 18 open + 3 resolved (ISS-007 closed today). INDEX.md accurate. ISS-021 (never-dispatched) still draft-pending, 34-day carryover per today's planner.

## 4. Recommendations

### Skills to add / modify / disable
1. **Fix the `articles/` commit path** (highest single-fix leverage). 13 skills silently produce no committed output. Root cause: article-writing skills write to `articles/` on ephemeral runners but don't `git add articles/... && git commit` before the runner tears down. Two-part audit:
   - (a) grep each of the 13 SKILL.md files (`cost-report`, `changelog`, `swarm-safety-eval`, `repo-pulse`, `push-recap`, `fork-fleet`, `repo-article`, `repo-actions`, `deep-research`, `hn-digest`, `rss-digest`, `polymarket`, `token-alert`) for their commit step; land the commit step where absent.
   - (b) audit chain-runner behavior for whether `articles/` reaches `main` post-run vs. `fleet-state`. Would unblock ISS-002/005/008–018 in one PR.
2. **Ship `agi-tracker: enabled: false`** on `aeon.yml:188` — 8th silent-Mon fire hits tomorrow 2026-08-24T13:00Z. Same MEMORY.md pointer bullet has been active for weeks; today it compresses to 1d out.
3. **Populate `memory/watched-repos.md` OR set `enabled: false`** on the 6 short-circuiting skills. Path-mismatch note: repo-revive SKILL.md references `memory/topics/watched-repos.md`; other five reference `memory/watched-repos.md` — reconcile in the same fix.
4. **Patch pr-tracker SKILL.md** — 60-day-overdue bundle (a)–(k) per MEMORY.md pointer bullet, especially (d) SKILL-level hash-dedup guard and (e) fresh-bot-PR trigger (would have caught yesterday's deepsec#161 correctly in today's predictor).
5. **Draft ISS-021** for [[enabled-skills-can-never-dispatch]] class — 34-day carryover; scope: `ai-framework-watch` + `run-frequency-guard`.

### Schedule adjustments
- No urgent cron changes this week. Sunday-morning drift (30m planner, 30m compute-macro-correlate, 10m swarm-safety-eval) is inside batch-health tolerance and does not warrant a schedule shuffle. [[morning-pocket-splits-into-two-de-facto-clusters]] class still holds.
- ISS-006 pocket-slot migration (Day-21) fix path unchanged — replace `messages.yml` `*/5 * * * *` with explicit per-slot crons modeling the three regimes. Blocks on merge-path proof (PR #26 unblock).

### Config changes (feeds, repos, addresses)
- Nothing to add/remove this week. `memory/watched-repos.md` is the load-bearing missing file — see #3 above.

### Quality improvements
- **Trim MEMORY.md to ≤50 lines** by moving 3–4 dense focus bullets into topic files. Preserves pointer-shape without losing detail.
- **Skill-freshness:** switch mtime check to `git log -1 --format=%ct` per [[skill-freshness-mtime-blind-in-gha]] — currently under-catches real staleness on GHA runners.
- **workflow-security-audit fingerprint standardization** — algorithm currently only in comments; codifying it in the SKILL body would eliminate the 13-finding fuzzy-anchor drift observed today.

## 5. Actions taken this run

- Wrote this article to `articles/self-review-2026-08-23.md`.
- No safe/obvious auto-fixes applied — the two candidates in the SKILL (prune stale MEMORY.md entries; update feeds.yml if dead) both need careful curation (MEMORY.md bullets link out heavily; there is no `feeds.yml` in this repo). Deferring to operator judgment rather than trimming in-place.
- Logged to `memory/logs/2026-08-23.md`.
- Sent summary notify via `./notify` (direct `.pending-notify/` write per [[notify-inline-cat-substitution-blocked-in-sandbox]] + [[notify-script-has-no-f-flag]]).

## Sources

- `memory/MEMORY.md` (64 lines) — index-shape, focus bullets dense
- `memory/logs/2026-08-17.md`…`2026-08-23.md` (2725 lines total)
- `memory/cron-state.json` (42 skills) — 4 healthy / 38 chronic DEGRADED / 0 fresh-broken
- `memory/issues/INDEX.md` (18 open / 3 resolved after today's ISS-007 close)
- `ls articles/` — 3 files today (skill-evals, skill-freshness, workflow-security-audit)
- `git log --since=2026-08-16 -- articles/` — no article commits in 7 days
- `git log --since=2026-08-16` on `main` — 1 commit total (`73eba91 chore(cron): skill-graph success`)
- `gh pr list --state open --limit 30` — 23 open aeon-repo PRs (21 `app/github-actions` + 1 dependabot + 1 freebuff-web)
