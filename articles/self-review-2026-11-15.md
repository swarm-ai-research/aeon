# Self Review — 2026-11-15

Window: 2026-11-08 → 2026-11-15 (7 days, logs 11-08/09/10/11/13/14/15; 11-12 was a fleet-wide silent day).

## 1. Quality of outputs

**Articles (`articles/`) — week count = 6 files, 4 duplicates.** Fresh longform this window is thin:

| Article | Substantive? |
|---|---|
| `cost-report-2026-11-09.md` | Yes — numeric WoW with projection. One of one. |
| `workflow-security-audit-2026-11-08.md` | Partially — CLEAN footer, but zizmor/actionlint both `fail` (sandbox denial), so the "0 findings" is a toolchain-degraded result, not a real audit. |
| `skill-freshness-2026-11-10/11/13/14.md` | Formulaic — three of the four are `FRESHNESS_OK` with identical "no flagged dependencies"; the 11-14 one is `FRESHNESS_STALE` only because a `fleet-control` article template was missing. Daily churn without new insight. |

**No compute-pulse, agi-tracker, skill-health, skill-evals, pr-triage, changelog, weekly-shiplog, repo-revive, repo-pulse, push-recap, deep-research, hn-digest, rss-digest, token-alert, polymarket, fork-fleet, repo-article, repo-actions article for the week.** The week's long-form voice is essentially one cost-report plus one degraded security audit — everything else lives in `memory/logs/` and `memory/topics/`.

**Notifications.** Operator-useful notifies this window: heartbeat on 11-13 (novel slot-agnostic silent day) and 11-14 (split-cohort regime extension) are substantive, net-new findings; skill-health 11-09 NOTIFY (hash unchanged but 70.95h gap), surplus-pulse catalog-mode replicas (9th n= byte-identical), cost-report 11-09, batch-health 11-13 WARN + 11-14 OUTAGE (ISS-045), compute-futures-eda 11-15, suggest-edges auto-reject (silent per-design). Heartbeat 11-13 + 11-14 are the highest-signal items — classifying a new fleet-wide shape and watching it extend by one day.

**PR comments.** Zero this window. `pr-review` has been `addPullRequestReview` 403-blocked for Day-55+ on swarm; 26th consecutive full-skip cycle. Verdicts carry-forward in logs only (5 APPROVE / 3 REQUEST_CHANGES / 0 BLOCK, 6th identical distribution). This is noise accumulation — every daily run re-emits the same unchanged ledger.

**Verdict:** Signal is concentrated in heartbeat prose and compute-futures-eda numerical findings. The rest is formulaic — skill-freshness duplicates, pr-review carry-forwards, surplus-pulse catalog replicas. The fleet produces more bookkeeping than new information per day.

## 2. Reliability

**Raw GHA counts (last 168h):** 53 runs total, 47 succeeded, 0 failed, 6 in_progress (includes this self-review). **0% stated failure rate — misleading.**

**True picture:** ~24 distinct skills executed in the window, against 44 enabled in `aeon.yml`. The missing ~20 are all ISS-006 silent-outage casualties — skills whose cron pockets dispatched nothing while the workflow runner shows "success" on anything that did fire. GHA failure conclusion does not capture dispatch silence.

**Standing silent-slot summary (as of 11-14):**
- **06Z cohort continuous silent Day-10 (11-05 → 11-14 inclusive)** — `compute-futures-eda` (0 6), `memory-flush` (0 6 2/2), `memory-structural-dedupe` (10 6 2/2), `planner` (30 6).
- **11-12 was a first-observed fleet-wide slot-agnostic silent day** — ~40h of continuous silence 11-11 17:20Z → 11-13 08:47Z. Distinct from prior per-slot pocket casualties. Novel pattern; may warrant atomic promotion next reflect.
- **11-13 / 11-14 widened split-cohort regime** — 08Z + 16Z preserved; 09Z, 18Z, 23:45Z silent. 11-14 added nominal-08Z to the silent set for the first time in this sub-regime. Heartbeat drift accelerated +47m → +86m day-over-day.
- **ISS-006 tributary count:** 26 filings (ISS-019 … ISS-045). ISS-045 filed 11-14 for Sat-EVEN 4-tuple.
- **ISS-001 denominator residue:** 38 skills at `success_rate < 0.5` with `last_status: success` + `cf=0`. Day-132 steady-state at hash `e27c0ac60367e7e5`. Byte-identical back to Day-109. Close deferred until ISS-006 stabilizes.
- **pr-review Day-55+ write-block:** standing 403 on `addPullRequestReview`. 26 consecutive full-skip cycles; verdicts in log only.
- **watched-repos config missing: streak-105 on 11-14 (6 dependent skills short-circuited).**

**Monitors catching real issues?** Yes — the batch-health → ISS-00X tributary pipeline is actively firing on every OUTAGE-tier window; heartbeat novel-pattern detection caught 11-12 slot-agnostic silence and 11-13/14 split-cohort extension within 24h of occurrence. **Monitors are working; the problem is the fleet cadence they monitor.**

**Verdict:** The fleet runs clean *on what runs* but the dispatch backbone is >2 months into continuous ISS-006 degradation. "0 failed" is cosmetic.

## 3. Memory hygiene

- **`memory/MEMORY.md` = 72 lines** (target ≤50 per CLAUDE.md). Current-focus bullets routinely exceed 1500 chars; several carry 20+ `[[atomic-slug]]` links each. Hard to scan; essentially a prose status report with pointers rather than an index.
- **Log structure inconsistency.** 2026-11-10 contains **six `# 2026-11-10` H1 headers** interleaved with skill sections — appears to be per-skill append-without-reading. Other days use single H1 + `##` per skill. 2026-11-15 is missing a date H1 entirely.
- **Topic files:** `memory/topics/` present and growing. 157 atomics per last notegraph regen. Reflect 11-09 is the most recent consolidation (promoted [[pr-tracker-bucket-tuple-attractor-exits-on-endogenous-active-to-stale-aging]]). Healthy.
- **Stale references:** MEMORY.md top bullet ("STATUS_PAGE=DEGRADED; 08Z-cohort settled-slot sub-regime BROKE at n=3 on 11-05") is 10 days old and the regime has since shifted to the 11-13/14 split-cohort shape per heartbeat logs — the bullet is outdated.
- **No duplicate atomic sprawl detected** this window — reflect's atomic-pass 11-09 returned 0 splits.

## 4. Recommendations (ranked by leverage / cost)

### A. Carry-forward blockers (operator-level, not patchable from here)

1. **Ship ISS-006 per-slot cron migration.** 26 tributaries, 06Z cohort Day-10 silent, cross-day drift acceleration. Planner 11-09 already selected `iss-006-08z-cohort-incremental-cron-migration-pr` as top priority (streak 1). The 39-day-stuck multi-pocket rewrite can be sliced into a single 4-skill PR moving `compute-futures-eda` + `memory-flush` + `memory-structural-dedupe` + `planner` out of the 06Z dead window.
2. **Install aeon GitHub App with `pull_requests: write` on `swarm-ai-research/swarm`** OR reclass swarm as report-only and stop re-emitting pr-review daily. 26 full-skip cycles at zero write-success is pure noise.
3. **Populate `memory/watched-repos.md`** OR disable the 6 dependents (`code-health`, `github-monitor`, `issue-triage`, `changelog`, `weekly-shiplog`, `repo-revive`). Streak-105 as of 11-14. Also reconcile the path mismatch (`repo-revive` → `memory/topics/watched-repos.md`; the other five → `memory/watched-repos.md`).

### B. SKILL-patch backlog (concrete, ready to land)

4. **`batch-health` SKILL.md:** replace `./notify -f <path>` (known no-op) with direct `.pending-notify/${epoch}-${skill}.md` write. Workaround currently applied inline every tributary filing.
5. **`pr-review` SKILL.md:** gate `memory/triaged-prs.json` write on successful post confirmation per [[pr-review-dedup-saturation-freezes-write-blocked-repo-queues]].
6. **`stale-content-pr-sweeper` SKILL.md:** add `"app/github-actions"` to `ALLOWED_AUTHORS`. The 2026-11-15 log shows the defect's counterfactual diverging for the first time — it would have closed `notegraph/2026-10-29` and `notegraph/2026-10-26` today but closed zero.
7. **`pr-tracker` SKILL.md batch (a)–(u):** 83+ days overdue. Includes new axis-5 enumeration per [[pr-tracker-bucket-tuple-attractor-exits-on-endogenous-active-to-stale-aging]].
8. **`suggest-edges` SKILL:** within-cohort pre-filter + symmetric per-node source∪target cap. The 2026-11-15 fire's single-target clustering (`2026-10-25` as target in 3/3 proposals) is another observation the symmetric cap would catch but a source-only cap would miss.
9. **`compute-futures-eda` SKILL:** bundle a stdlib fallback for pandas, OR add pandas to the prefetch step. Stdlib fallback used again on 11-15 (6-day content gap catch-up for the 11-14 CSV).

### C. Quality / schedule

10. **Collapse pr-review daily re-emission to weekly** while swarm remains write-blocked. Carry-forward spam dilutes the useful signal.
11. **Collapse skill-freshness `FRESHNESS_OK` daily articles into a single weekly summary.** 3-of-4 this week were identical templates. Keep `FRESHNESS_STALE` articles daily.
12. **Rewrite MEMORY.md top bullet** when the 11-05 sub-regime framing is factually stale (it is — superseded by 11-12 slot-agnostic + 11-13/14 split-cohort). Deferred to next reflect pass.
13. **Adopt a single log append convention** — one `# YYYY-MM-DD` H1 per day, `## <Skill>` per entry, so grep/tooling can rely on structure. 11-10 and 11-15 both violate this today.

## 5. Actions applied directly

- None applied inline this review. MEMORY.md is in a load-bearing state (every bullet is actively referenced by the next heartbeat/reflect), so pruning without a reflect pass risks dropping atomic-link anchors mid-week. Deferred to the next scheduled reflect dispatch.
- No dead feeds in `feeds.yml` to prune — RSS-digest/HN-digest/token-alert are among the ISS-002/009/015/016/018 `no_file_match` disabled skills; their feed configs are not currently consumed.

## 6. Follow-ups queued

- Flag to next reflect: refresh MEMORY.md top bullet from "11-05 sub-regime BROKE" to "11-12 slot-agnostic + 11-13/14 split-cohort" framing with heartbeat drift acceleration series.
- Flag to next planner: ship the 08Z-cohort incremental cron migration PR (ranked #1 on 11-09, streak now 7).
- Flag to next skill-repair dispatch: close `batch-health` `./notify -f` call-form patch — it has been workaround-only for 26 tributary filings.

## Summary

- Quality: mixed — heartbeat + compute-futures-eda carry the week's signal; pr-review, skill-freshness, surplus-pulse produce duplicate daily output.
- Reliability: `0 failed` across 47 GHA successes is cosmetic; the real story is ~20 skills didn't dispatch at all due to ISS-006 pocket silence (06Z Day-10, split-cohort 09Z/18Z/23:45Z, 11-12 fleet-wide silent day as novel shape).
- Memory: MEMORY.md 72 lines (target 50), top bullet stale, log structure drift on 11-10 + 11-15.
- Actions taken: review written, no inline edits applied.
- Top 3 recommendations: (1) ship ISS-006 08Z-cohort incremental cron migration PR; (2) resolve swarm write-block or stop daily pr-review re-emission; (3) populate `memory/watched-repos.md` to unblock 6 short-circuited skills.
