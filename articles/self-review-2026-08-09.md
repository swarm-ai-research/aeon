# Self Review — 2026-08-09

**Window:** 2026-08-03 → 2026-08-09 (7 days)
**Scope:** all skills (no `${var}`)
**Author:** aeon (self-review skill)

## Verdict at a glance

- **Quality:** thin — long-form article surface is nearly empty (2 articles on disk, both today, both dashboard-shaped). Substantive standalone output this week = **vuln-scan 08-08 on yc-software/qm**. Everything else is either dashboard status (heartbeat, skill-freshness, skill-health), evidence-gathering (compute-futures-eda, pr-review verdicts), or memory hygiene (reflect, memory-flush, notegraph). Notifications were disciplined — dedup and bland-suppression worked; no notify spam.
- **Reliability:** the 08-07 unblock of `github-actions-cannot-create-prs` (creation channel) is the biggest positive delta in weeks. The **new emergent problem** is that the merge channel is unproven: 17 open aeon-repo PRs, only 1 merged this week (dependabot #8), 0 of ≥15 `app/github-actions` PRs merged in 48h+.
- **Memory hygiene:** healthy. MEMORY.md held 61 lines throughout, 3 reflect runs added 7 new atomic notes (66 → 73), 2 memory-flushes resolved contradictions, 2 notegraph deterministic-no-op days exercised the silent-exit path correctly.
- **Systemic:** ISS-001 residue day 50 (denominator burn, substantively green), ISS-006 pocket migration Day-8 (bimodal delivery pattern stable), never-dispatch day 32 (`ai-framework-watch` + `run-frequency-guard`), swarm write-perm gap 28th confirming invocation.

---

## 1. Quality audit

### Articles produced (7 days)

| Date | Article | Class | Quality |
|---|---|---|---|
| 08-05 | `skill-freshness-2026-08-05.md` | dashboard | formulaic, expected — no consumer-flag events |
| 08-05 | `skill-analytics-2026-08-05.md` | dashboard | substantive — analytics runs are novel-signal-per-run |
| 08-07 | `skill-freshness-2026-08-07.md` | dashboard | formulaic |
| 08-08 | `skill-freshness-2026-08-08.md` | dashboard | formulaic |
| 08-08 | `vuln-scan-2026-08-08.md` | **substantive** | 2 code findings + 9 fixable dep bumps + 2 disclosure drafts |
| 08-09 | `skill-freshness-2026-08-09.md` | dashboard | formulaic |
| 08-09 | `skill-evals-2026-08-09.md` | dashboard | BOOTSTRAP — 14/49 coverage, 13 NEW_FAIL |

**Total:** 7 articles in 7 days, of which **1 substantive** (vuln-scan). Everything else is dashboard/status.

Long-form skills that could have produced substantive articles are `enabled: false` in `aeon.yml`: `changelog`, `weekly-shiplog`, `deep-research`, `hn-digest`, `rss-digest`, `polymarket`, `token-alert`, `repo-pulse`, `push-recap`, `fork-fleet`, `repo-article`, `repo-actions`, `cost-report`. The 13 open `no_file_match` issues (ISS-002/005/008–018) are a direct symptom of this.

### Notifications

~35–40 `.pending-notify/*.md` writes this window. Dedup + bland-suppression worked well:
- Heartbeat suppressed notify 4/4 days via the 48h-log-dedup rule (all P0/P1/P3 findings had recent precedents).
- Skill-health hash byte-identical 40→44 consecutive days but fired the 24h cadence-reminder appropriately.
- Notegraph fired 3 times, 2 with `notify_suppressed: true` on deterministic no-ops (healthy path exercised).
- Pr-triage skip-only runs stayed quiet.
- No repeated identical messages observed.

Substantive notifications: reflect 08-05, 08-07 (unblock), 08-08; planner 08-07/08/09 (rank shakeup around the aeon queue); pr-tracker 08-08 (first-ever CLEAN 4-of-4 predictor hit); vuln-scanner 08-08.

### PR comments posted

**Zero** on-PR comments landed anywhere this week:
- Aeon repo: no PR review activity (aeon opens PRs but doesn't review them; no maintainer role).
- Swarm repo: 8 `pr-review` invocations 31st→38th, **all write endpoints 403** (23rd→28th confirming `aeon-app-no-write-on-swarm-repo`). Verdicts are log-only.
- One notable off-fleet event: `0xprogrammable/aeon-launch-models#1` received the first-ever author-response to a maintainer CHANGES_REQUESTED on a non-security bot PR (08-08 19:18Z) — this is downstream of a prior week's review that DID post, so it's a signal the log-only fallback still moves some things.

---

## 2. Reliability audit

### Skills invoked (7 days)

Regular daily fires (5/5 days): pr-tracker, issue-triage, github-monitor, fleet-control, code-health, gitlawb-fleet-metrics, surplus-pulse.
Regular near-daily (4/5): heartbeat, batch-health, skill-freshness, compute-futures-eda, planner, pr-triage.
Weekly / on-cadence: reflect ×3, skill-health ×3, memory-flush ×2, memory-structural-dedupe ×2, notegraph ×3, goal-tracker ×3, stale-content-pr-sweeper ×4, skillpacks ×1, skill-analytics ×1, skill-evals ×1, config-validator ×1, swarm-safety-eval ×1, compute-macro-correlate ×1, vuln-scanner ×1, compute-pulse ×1, repo-revive ×1, janitor ×1, suggest-edges ×1 (first-ever).
Operator-triggered: pr-review ×8.

### No-op / short-circuit skills (structural silence)

Chronic no-ops every run, no signal produced:
- **6 watched-repos-dependent skills** (github-monitor, issue-triage, code-health, changelog, weekly-shiplog, repo-revive) — `memory/watched-repos.md` absent. 30+ same-day short-circuits across the window. Standing MEMORY.md pointer.
- **fleet-control + gitlawb-fleet-metrics** — `memory/instances.json` empty / `memory/gitlawb-fleet.json` absent. Silent-stop by design ("empty fleet is not news") but they still burn workflow slots.
- **swarm-safety-eval** — `memory/agent-first/` absent → SSE_EMPTY.
- **goal-tracker** — MEMORY.md has no `## Goals` section → NO_GOALS (3 fires, 3 identical notifies).
- **skillpacks** — 14th consecutive fingerprint-identical day (last change 07-26). Silent-exit is correct.

### Failures / errors / patterns

**Cleared this window:**
- `github-actions-cannot-create-prs` (creation channel) — cleared overnight 08-06 → 08-07. First-ever `app/github-actions` authored PRs #10–13 landed 05:16–05:50Z on 08-07. Mechanism: most likely the Repo Settings → Actions → "Allow Actions to create PRs" toggle (GH_GLOBAL PAT was pre-wired for weeks; no `AEON_GH_PAT` anywhere).

**Persistent blockers (day counts as of 08-09):**
- ISS-001 OAuth-outage denominator residue — **day 50**. 38 skills at `success_rate < 0.5` with `last_status: success` + `cf: 0`. Literal-rule DEGRADED, substantively green.
- ISS-006 morning-pocket cron migration — **Day 8**. Bimodal delivery (~06:11–06:22Z + ~09:00–09:58Z clusters); planner slot still drifts ~30–50min.
- `enabled-skills-can-never-dispatch` — **day 32**. `ai-framework-watch` (weekly Mon 08:30) + `run-frequency-guard` (daily 23:00) never fire (no cron-state entry).
- `agi-tracker-missing-skill-md-dispatches-no-op` — 5 silent Mon slots so far; 6th at Mon **2026-08-10 13:00Z** (tomorrow).
- `aeon-app-no-write-on-swarm-repo` — 28th confirming invocation. Distinct from aeon-repo unblock.
- `snapshot-rebase-clobbers-docs-status-md` — 13th consecutive regen-clobber-then-rewrite cycle, **23d past urgency**.
- **NEW emergent problem** (post-unblock): aeon-repo merge channel unproven. 17 open PRs, only dependabot #8 merged this week. All `app/github-actions` PRs stalled with `mergeStateStatus: UNKNOWN`, `statusCheckRollup: []` — no CI or branch-protection gating; purely awaiting operator merge. No auto-merge policy configured.

**New failure modes discovered this week:**
- `github-app-cannot-fork-third-party-repos` (08-08) — vuln-scanner `gh repo fork` returned 403 on external repos. Worked around locally by direct clone. SKILL.md patch pending.
- Scope-expansion of `sandbox-blocks-shell-redirect-to-workdir` (08-08) — `>`, `>>`, and `cp` now blocked in-workdir (previously outside-workdir only).
- `pr-tracker-search-drops-archived-repo-prs` — PostHog/code#4007 hidden from search 82h+ post-archive. Eventual-consistency hypothesis falsified; treat as permanent-until-unarchive.
- `stale-content-pr-sweeper` `ALLOWED_AUTHORS = {"aeonframework"}` — post-unblock, all cron-authored PRs are from `app/github-actions`. Sweeper is now strict no-op; will break the moment two date-stamped `notegraph/*` or `suggest-edges/*` PRs coexist (already trending — #14 + #21 + #22 are three suggest-edges branches).
- **skill-evals BOOTSTRAP** (08-09) — 14/49 coverage (28%), 13 NEW_FAIL (all no_file_match dedup-suppressed against existing ISS-002/005/008–018).

### Monitors — real signal or always-OK?

- **heartbeat** — dedup rule fired appropriately; would have escalated if novel P0 emerged. Correctly did not spam. Good.
- **skill-health** — 44-day steady-state hash, 24h cadence-reminder cadence correct. But: no fresh findings in 40+ days because ISS-001 denominator dominates. This monitor is doing what it can with the data, but the P0-trigger is stuck-on.
- **batch-health** — flagged ISS-020 on 08-03 (real 3-skill outage); reported OUTAGE/WARN/OK correctly across the window as pocket-migration stabilized. Good signal.
- **skill-freshness** — 4 runs, 0 flagged all week. The GHA mtime blind spot ([[skill-freshness-mtime-blind-in-gha]]) is a known structural gap. Combined with the mostly-empty `articles/` directory, this monitor has very little to work with — currently more OK-noise than signal.
- **config-validator** — flags `scripts/validate-config.js` missing (49th day). Real issue, not being fixed.
- **skill-evals** — first ever run today; 28% coverage means most skills are unmonitored end-to-end. Adding it to the fleet was the right move.

---

## 3. Memory hygiene audit

- **MEMORY.md**: 61 lines. Pointer-only index, no drift. Reflect keeps this lean.
- **memory/logs/**: 271–503 lines per day, structured consistently by skill section. Verbose but parseable — every skill self-documents its inputs, decision, files touched, follow-up.
- **memory/notes/**: 66 → 73 atomic notes across the window. All single-claim, ≤4 sentences. 0 splits required in the 08-05 and 08-08 reflects.
- **memory/topics/**: 6 MOCs + compute-futures-eda subdir. fleet-ops MOC gets a daily snapshot rotation (full → single-row after 2 days).
- **memory/issues/INDEX.md**: 18 open. ISS-001 held open for 50 days pending ISS-006 resolution (correct — coupling documented).
- **notegraph**: 249 nodes · 1854 hard · 639 soft · 1 orphan (docs/telegram-instant.md, persistent, harmless).
- **Stale data**: none obviously stale in MEMORY.md itself. `memory/goal-state.json` is 15 days old but held intentionally per goal-tracker SKILL.md rule (no `## Goals` section to compare against).

**Verdict:** memory hygiene is the healthiest surface of the whole fleet. Reflect + memory-flush + memory-structural-dedupe form a working three-layer maintenance stack.

---

## 4. Recommendations

### Ship-ready fixes (rank by ROI)

1. **[Rank-1, deadline tomorrow] Ship `agi-tracker: enabled: false` on `aeon.yml:188` via PR** — planner rank-1 streak-3; Mon 2026-08-10 13:00Z is the 6th silent Mon slot. Even if the PR doesn't merge in time (queue-merge is unproven), it joins the queue for the moment operator moves.
2. **Merge one low-risk PR from the aeon queue** — the only unproven part of the 08-07 unblock. Candidates:
   - #10 `notegraph: 1 new orphan(s)` (50h+, dep-free, small)
   - #21 + #22 (twin `suggest-edges` runs, similarity-1.00 low-risk)
   - #17 or #20 (`docs-pass` — README additions)
   A single merge would prove end-to-end flow and unblock ≥15 similar PRs.
3. **Add `"app/github-actions"` to `stale-content-pr-sweeper` `ALLOWED_AUTHORS`** — one-line map extension in the SKILL.md step-1 snippet. Currently silently no-ops on all post-unblock cron PRs; will break the moment two date-stamped branches coexist (already imminent for `suggest-edges/*`).
4. **Populate `memory/watched-repos.md` OR flip `enabled: false` on the 6 dependent skills** — 30+ same-day short-circuits/week is pure workflow waste. Either action ends the pattern.
5. **Land the pr-tracker SKILL.md patch batch** — 9 items, **46d overdue**. Every scan enacts all 9 inline. Now viable as a PR (creation channel unblocked). MEMORY.md line 52.
6. **Fix `docs/status.md` snapshot-rebase clobber** — 13 consecutive regen-clobber cycles. Two-line fix: either exclude `docs/status.md` from snapshot merges OR extend heartbeat's auto-commit `git add` glob to include `docs/`.

### Skill fleet — add / modify / disable

- **Modify:** `stale-content-pr-sweeper` (add app/github-actions author).
- **Modify:** `pr-tracker` (9-item patch batch, 46d overdue).
- **Modify:** `notegraph` — silent-exit heuristic per [[notegraph-extractor-generatedat-nondeterministic]] (mask `generatedAt` before diffing).
- **Modify:** `skill-freshness` — use `git log -1 --format=%ct` instead of `stat --format=%Y` per [[skill-freshness-mtime-blind-in-gha]].
- **Modify:** `vuln-scanner` step-2 — replace `gh repo fork` with direct `git clone` per new [[github-app-cannot-fork-third-party-repos]].
- **Add:** batch-health + skill-freshness to `evals.json` (skill-evals recommended coverage additions — will lift coverage from 28% to ~32%).
- **Disable / clean up:** 13 disabled long-form skills are the root cause of the 13 ISS-002/005/008–018 `no_file_match` issues. Either re-enable a curated subset (e.g. hn-digest, weekly-shiplog) or remove them from `evals.json` so skill-evals stops flagging them.
- **Investigate:** `ai-framework-watch` + `run-frequency-guard` never-dispatch (32d silent).

### Schedule adjustments

- **ISS-006 fix path** — replace `messages.yml` `*/5 * * * *` with explicit per-slot crons covering every timeslot in `aeon.yml`. Model the two migrated pockets (~06:11–06:22Z + ~09:00–09:58Z) and the persistent ~06:30Z planner gap per [[morning-pocket-splits-into-two-de-facto-clusters]]. Now viable as a PR (creation unblocked).
- **Auto-merge policy** — the aeon-repo queue is the single largest blocker of end-to-end fleet health. Either configure GitHub auto-merge on aeon-authored PRs, or add a scheduled `pr-merge-sweeper` skill with an explicit safety allowlist (notegraph, suggest-edges, docs-pass).

### Config changes

- **Populate `memory/watched-repos.md`** — even a starter set of 2–3 repos unlocks 6 skills.
- **Add `## Goals` section to `memory/MEMORY.md`** — currently `goal-tracker` NO_GOALS every run. Candidate seed: the top 5 pointer items.

### Quality improvements

- **Enable ≥1 substantive article-producing skill** — the `articles/` directory has 2 dashboard files today; the fleet is producing near-zero long-form content. Recommend enabling `weekly-shiplog` or `changelog` once `watched-repos.md` is populated, or standing up a curated `hn-digest`/`rss-digest` behind a feeds.yml (does not currently exist).
- **Address 85 workflow-security-audit findings** (from 07-19 run) — pin 3 `actions/*` refs to SHAs (Critical), move sensitive secrets to environment-scoped, add `persist-credentials: false` on 11 read-only checkouts.

---

## 5. Actions taken this run

Direct, safe changes applied:
- **None** — MEMORY.md is up-to-date after the 08-08 reflect; no stale entries to prune; `feeds.yml` doesn't exist so no dead feeds to clean; the top-priority fixes (agi-tracker PR, sweeper patch, watched-repos populate) all warrant deliberate PRs rather than in-line commits from this skill.

Files created:
- `articles/self-review-2026-08-09.md` (this file)
- Notification queued to `.pending-notify/`
- Log entry appended to `memory/logs/2026-08-09.md`

---

## Summary

Aeon spent the week transitioning from a 42-day PR-creation deadlock to a new merge-channel deadlock. The unblock on 08-07 landed 15+ PRs but 0 have merged. Skill runs, memory hygiene, and notifications are healthy; long-form output surface is nearly empty because most content-producing skills are `enabled: false`. Top-two actions for the operator: (a) merge one aeon-repo PR to prove the flow, (b) ship the `agi-tracker: enabled: false` PR before Mon 13:00Z. Top self-help action: land the 46d-overdue pr-tracker SKILL.md patch batch — now viable as a PR.
