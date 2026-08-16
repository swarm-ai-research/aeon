# Self Review — 2026-08-16

Window: **2026-08-10 → 2026-08-16** (7 days). Focus: everything (`${var}` empty).

## Verdict at a glance

- **Quality:** thin — 3 substantive articles this week (`skill-evals`, `skill-freshness`, `workflow-security-audit`, all filed today 08-16). Most output lives in `memory/logs/` daily entries, not `articles/`. Notification signal-to-noise remains high after dedup work; `goal-tracker NO_GOALS` is the only recurring noisy channel.
- **Reliability:** 100% workflow success — **169/169 completed, 0 failed, 5 still running** over 168h per `./scripts/skill-runs`. But green ≠ healthy: the fleet is dispatching-but-no-op'ing at scale (see §2).
- **Memory hygiene:** MEMORY.md steady at 64 lines (target ~50, 28% over). Topic files well-scoped. Logs verbose (~430 lines/day) but consistently structured.
- **Merge flow:** still unproven — **0 `app/github-actions` PRs merged since 2026-08-07** (~9 days, queue grew 19 → 24).
- **NEW critical finding this run:** the `notegraph` skill's 08-16 run silently discarded ~159 nodes of graph growth by reverting to HEAD based on a false "PR #32 merged" claim. Detail below.

## 1. Output quality

### Articles filed this week (3)

| Article | Substance |
|---|---|
| `skill-evals-2026-08-16.md` | BOOTSTRAP: 14/49 covered, 13 pre-existing chronic issues classified as NEW_FAIL (labeling artifact, not regression). Actionable queue with concrete evals.json patches. Real work. |
| `skill-freshness-2026-08-16.md` | Reclassified 2 prior flags as non-flaggable (implicit wildcard refs to disabled producers) per SKILL.md rule. Correct call, but relies on GHA-mtime blind spot flagged in [[skill-freshness-mtime-blind-in-gha]] — verdict is technically-correct-but-optimistic. |
| `workflow-security-audit-2026-08-16.md` | `WORKFLOW_AUDIT_UNCHANGED` — 78 findings carried over from 08-09, no delta, no PR, no notify. Silent correctness per SKILL step-5 gating. |

Everything else — pr-tracker, planner, notegraph, suggest-edges, compute-futures-eda, surplus-pulse, heartbeat, reflect, skill-health, etc. — writes to `memory/logs/YYYY-MM-DD.md`, not to `articles/`. That's by design for state-tracking skills, but it means `skill-evals` will keep classifying them `no_file_match` until evals.json is patched (queued as rank-4 in today's `skill-evals` action list).

### Notifications

Estimated ~10/day, ~70/week. Substantive channels: pr-tracker (daily tuples + class events), planner (daily), compute-futures-eda + surplus-pulse (daily), notegraph (only when chain grows), reflect + skill-health (weekly).

**Noise:** `goal-tracker NO_GOALS` fires the same body every day (heading-mismatch bug, streak-3+). Dedup + bland-suppression correctly silence: heartbeat, sweeper on `n_closed=0`, watched-repos cluster, pr-review/pr-triage skip-days, gitlawb-fleet-metrics, fleet-control.

### PR comments

Not posted this week from cron. `pr-review` (swarm) ran 14× with standing advisory verdicts (`#549 REQUEST_CHANGES 2/5`, `#543 APPROVE 5/5`, both ~8d frozen). App-perm gap blocks actual comment posting per [[aeon-app-no-write-on-swarm-repo]]; verdicts are locally logged only.

## 2. Reliability

### Raw numbers (168h)

- **Total workflow runs:** 174
- **Completed OK:** 169 (100% of terminal states)
- **Still running:** 5
- **Failed:** 0
- **Failure detail:** none in the last 168h

### Why 100% success is misleading

The fleet is dispatching-but-no-op'ing at scale. Green in `./scripts/skill-runs` conflates "workflow exited 0" with "workflow did work." This week's no-op inventory:

| Class | Skills | Days silent | Root cause |
|---|---|---|---|
| watched-repos short-circuit | code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive | day-10 → day-11 chronic | Missing `memory/watched-repos.md` (and path-mismatch: repo-revive references `memory/topics/watched-repos.md`) |
| never-dispatched | ai-framework-watch (Mon 08:30), run-frequency-guard (daily 23:00) | 39d consecutive | Cron-state absence per [[enabled-skills-can-never-dispatch]] |
| HEALTHY-but-empty | agi-tracker (Mon 13:00) | 6th silent-Mon fired 08-10; 7th fires 08-17 | `skills/agi-tracker/SKILL.md` missing per [[agi-tracker-missing-skill-md-dispatches-no-op]] |
| FLEET_EMPTY | fleet-control, gitlawb-fleet-metrics | daily silent | No managed instances / missing fleet.json |
| ALLOWED_AUTHORS gate | stale-content-pr-sweeper | 7 runs, 0 closes; day-10 streak | Hardcoded `{"aeonframework"}` excludes all 21 `app/github-actions` post-unblock PRs |
| 100%-skip | pr-review, pr-triage on swarm | every run (47th / 34th 100%-skip invocation on 08-15) | Dependabot bot-author + dup-SHA filters + App-perm gap |
| dedupe idempotent | memory-structural-dedupe | every even-day run | 0 sections match, 0 changes |
| byte-frozen | skill-health hash `e27c0ac6…` | 50+ consecutive days by 08-15 | Nothing on the fleet has moved that report |

Rough count: **~42 no-op dispatches from the watched-repos cluster alone this week**, plus ~15 more across the other classes. All green, all producing zero work.

### Recurring failures / degradations

- **ISS-001 residue** (day 51 → day 58): 38–39 skills at `success_rate < 0.5` with `last_status: success` + `consecutive_failures: 0`. Chronic literal-rule artifact; substantively green per today's heartbeat.
- **ISS-006 messages.yml late delivery** (day 9 → day 15): late-pocket recouple 08-13, decoupled slow-slot 08-11/08-12, persistent 06:30Z gap.
- **snapshot-rebase clobbers docs/status.md** (day 14 → day 20; 29d past urgency threshold): heartbeat regenerates wholesale AGAIN, 18th consecutive rebase-clobber-then-regen.
- **stale-content-pr-sweeper allowlist patch missing** (streak-4 → streak-10): 0 closes daily; would-be-closes grew 3 → 9 as the notegraph chain grew.
- **pr-tracker SKILL.md patch batch** (47d → 53d overdue): now includes items (a)–(k) covering GraphQL drift, email-filter fan-out, tuple-predictor scan-hour math, stale-bot inversion, self-owned-repo index lag, archived-repo direct-fetch. Item (d) — hash-based step-5 dedup guard — newly urgent: **3-consecutive-day byte-identical `sent` cycle 08-13/08-14/08-15**.
- **goal-tracker NO_GOALS** (streak-3+): heading-mismatch bug, notify fires daily with identical body.

### New / clarified failure classes this week

- 08-11: [[pr-tracker-repo-deletion-loses-pr-permanently]] (0xprogrammable/aeon-launch-models 404 both search + direct-fetch; day-5 persist by 08-15)
- 08-12: [[pr-tracker-stale-bot-comment-inverts-stale-classification]] — n=2 confirmed 08-13 (Baileys#2732 + PostHog#78346, distinct bot handles)
- 08-12: [[pr-tracker-search-indexing-lag-drops-self-owned-prs]] — resolved as transient 08-13
- 08-14: [[compute-futures-basket-synth-3025x-multiplier]] promoted to atomic (deterministic constant, n=3 → n=5 by 08-15)

### **NEW CRITICAL — notegraph silent regression today (08-16)**

Filed as `NEW-08-16` for triage — no ISS number yet.

- Extractor produced **280 nodes / 2134 hard edges / 703 soft**.
- Run logged: `byte-identical to HEAD notegraph.json (already at 280n from merged #32)`.
- **Reality:** PR #32 is `state: OPEN, mergedAt: null` (verified via `gh pr view 32 --repo swarm-ai-research/aeon`); HEAD `notegraph.json` is at **121 nodes / 856 edges**.
- SKILL took the interpretive silent-exit path, ran `git checkout --` on `notegraph.json`, `docs/notegraph.md`, `docs/notegraph.html`, `docs/notegraph-speedrun.html` — reverting the 280n extractor output back to 121n HEAD.
- No PR opened. No notify. Skill exited `NOTEGRAPH_NO_CHANGE`.
- Net effect: **~159 nodes and ~1278 hard edges of real graph growth were silently discarded** because the SKILL's byte-identity check trusted a fabricated "merged" state instead of comparing extractor output to actual HEAD content.
- The mistake propagated: today's memory-flush faithfully carried the "chain stays length-7 / 0 merges" line while separately marking `memory/state/notegraph.json` as advanced to fingerprint `832a210f…`. Two contradictory sources of truth now.

This is exactly the class of failure `heartbeat` + `skill-health` + `skill-evals` cannot catch: workflow succeeded, article was not expected today, notification was correctly suppressed. Only self-review sees it.

## 3. Memory hygiene

- **MEMORY.md:** 64 lines. Target is ~50 (SKILL.md line 39). 28% over budget but every line is still load-bearing under an active planner rank or chronic-carry status per today's memory-flush.
- **Topic files:** aeon-signing-identity-fragmentation (22), agi-tracker (46), compute-pulse (77), fleet-ops (239), pr-status (95), surplus-pulse (57). fleet-ops is fat but reasonable for a rolling incident log; no evidence of stale.
- **Log volume:** 3009 lines over 7 days (~430/day). Consistently structured (`## Skill / ## Summary` sections). No hygiene concerns beyond size.
- **Issues index:** 17 open, 2 resolved. No new ISS filings this week despite two new failure classes (pr-tracker-repo-deletion, pr-tracker-stale-bot-inversion) and one drafted-but-not-filed (ISS-021 for never-dispatched pair, 27-day carryover). Filing rhythm has stalled.
- **`.notify-sent-hashes` + `notify/` dir show up in `git status`** (untracked at review start) — noise, not danger, but worth deciding whether to gitignore or clean.
- **`.pending-notify/` empty** at review-start — postprocess is clearing on schedule.
- **Contradiction surfaced this run:** MEMORY.md line 12 says "chain stays length-7 / still 0 merges" while memory-flush entry line 61 treats #32 as merged (`280n from merged #32`). Both are wrong-ish — #32 is OPEN, and HEAD is at 121n, not 280n. Real state: chain still length-7, 0 merges, but the state-file refresh in memory-flush was operating on the notegraph run's fabricated premise.

## 4. Standout wins

- **08-10:** pr-tracker **CLEAN 4-of-4 HIT** — first n=3 lockstep cohort transition (ruvnet + block + jamiepine crossed 7d frozen inside a 4-minute anniversary window), validating [[same-day-file-cohort-stales-in-lockstep]] as a distinct class.
- **08-11:** suggest-edges self-caught templated-corpus noise for the first time and aborted before PR — pattern now formalized as `SUGGEST_EDGES_NO_PROPOSALS` interpretive-exit and rejection-loop is holding at exactly +3/day for 8 days.
- **08-14:** first **4-of-4 letter+substantive double-HIT** on pr-tracker tuple predictor since rebase; 3rd consecutive byte-identical tuple day (08-13/08-14/08-15).
- **08-15:** vuln-scanner 10th run drafted `SMNETSTUDIO/WeChat-AI` disclosure with 3 code + 5 dep findings covering 23 CVEs; PVR-enabled disclosure path exercised.
- **Reflect + memory-flush chain is healthy** — contradictions resolve in-place, no correction-append thrash, wikilink density holding.

## 5. Recommendations

Ranked by urgency-adjusted impact.

### Rank 1 — Investigate the notegraph 08-16 silent regression (NEW today)

- Verify `notegraph` extractor really produced 280n on today's run and whether HEAD `notegraph.json` @ 121n is the truth.
- Add a hard invariant to SKILL step-3: **compare extractor node count to HEAD `notegraph.json`'s stats.nodes before taking the silent-exit path.** If they differ by >1, exit LOUD (open PR, notify), never revert.
- File ISS-024 (severity: high, category: prompt-bug or quality-regression) with the exact log excerpt + git evidence.
- Recover the 280n extractor output — open a PR carrying it explicitly, breaking the "state-file drifts silently while HEAD stays behind" pattern.

### Rank 2 — Merge one aeon-repo PR to prove the flow

Unchanged from last week's rec. Zero merges in the 21 `app/github-actions` PRs since 2026-08-07 (9+ days). Textbook first-flow-proof: PR #26 (dependabot actions/checkout, same class as merged #8), or #10 (notegraph orphan flag, 8d+ old, dep-free). Blocks planner rank-2 (sweeper allowlist), rank-3 (agi-tracker toggle), and Rank 1 above (if the notegraph fix is a PR, it needs a merge path).

### Rank 3 — Land `agi-tracker: enabled: false` OR restore SKILL.md by 2026-08-17 13:00Z (~1 day)

7th silent-Mon fire ~1 day out. Missed deadline reset streak from 5 → 1 on 08-10. Lower-friction path: `enabled: false` on `aeon.yml:188`. Higher-quality path: author SKILL.md matching the [[agi-tracker]] MOC's weekly frontier-agent scoring shape.

### Rank 4 — Batch-patch pr-tracker SKILL.md (item d newly urgent)

53d overdue. Items (a)–(k) in MEMORY.md pointer. Item (d) hash-based dedup guard now demonstrated by 3-consecutive-day byte-identical `sent` cycle 08-13/08-14/08-15.

### Rank 5 — Fix `goal-tracker` heading-match to stop daily NO_GOALS noise

Streak-3+ of identical daily body. Either populate goals or fix the parser to stop firing when there's nothing to say.

### Rank 6 — Populate `memory/watched-repos.md` OR ship `enabled: false` on the 6 dependent skills

Chronic streak-10. Six healthy-looking dispatches/day producing zero work. Reconcile the path mismatch in the same PR (repo-revive references `memory/topics/watched-repos.md`, other five reference `memory/watched-repos.md`).

### Rank 7 — File ISS-021 (never-dispatched pair) and ISS-022 (agi-tracker HEALTHY-but-empty)

27-day carryover on the draft. Filing is cheap; the value is having repair skills key on the ID.

## 6. Actions taken this run

- **None applied inline.** Every candidate — MEMORY.md pruning, ISS filing, notegraph fix, sweeper allowlist — warrants a deliberate PR with a review-worthy commit message, not a self-review-scoped drive-by. MEMORY.md is 28% over target but every line is load-bearing.
- Verified PR #32 open (not merged) via `gh pr view`.
- Verified HEAD `notegraph.json` at 121n (not 280n) via `jq`.
- Left the notegraph run's revert in place — reverting the revert without a linked ISS/PR would compound the confusion.

## 7. Follow-up files

- `articles/self-review-2026-08-16.md` (this file, new)
- `memory/logs/2026-08-16.md` (appended below)
- `.pending-notify/{epoch}-self-review.md` (new — fans out via `scripts/postprocess-notify.sh`)

## Summary

Weekly self-review over 2026-08-10 → 2026-08-16. Fleet is 100% green (169/169 completed) but that hides a large no-op surface (~50+ empty dispatches/week) and one **new critical silent regression today**: `notegraph` reverted 280 extractor nodes back to HEAD's 121 based on a fabricated "PR #32 merged" claim (#32 is OPEN). Recommendation Rank 1 is a hard invariant on the extractor-vs-HEAD comparison plus ISS-024. Merge-flow to aeon repo still unproven (0 merges in 9+ days across 21 `app/github-actions` PRs); this blocks the sweeper allowlist, the agi-tracker toggle, and Rank 1's fix path. Memory hygiene healthy; MEMORY.md 28% over target but every line load-bearing.
