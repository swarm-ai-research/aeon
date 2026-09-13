# Self Review — 2026-09-13

*Window: 2026-09-07 → 2026-09-13 (7 days) · prior review 2026-08-30 (14d gap, 7d overdue — self-review's own 18:00Z pocket has been ISS-006-dead the entire interval)*

> Reliability posture 89/89 completed OK on the surface, but cadence is the real story: the 06:00Z pocket has been dead 4 consecutive days (ISS-006 6th outage, ISS-026 filed 09-12), 9 weekly skills are 9d–86d overdue, and 2 skills remain never-dispatched at Day-66. Quality-wise, `articles/` was materialized in git (48a7486, today 17:55Z) — retiring last review's #1 recommendation and unblocking cascade close for ISS-002/005/008–018. ISS-008 already closed (cost-report). Notification hygiene is holding: every silent-skip skill correctly suppressed, no operator-training-to-ignore this week.

## Reliability

**Overall (last 168h, per `./scripts/skill-runs`):** 95 workflow runs · 89 succeeded · 0 failed · 6 in progress (this batch) · 100% success rate on completed. The single-number success rate is honest — no run finished with a failure conclusion this week. But it masks a scheduler-coverage collapse:

**Cadence coverage — daily skills (expected 7 runs / 168h):**

| Skill | Runs | Coverage | Notes |
|---|---|---|---|
| stale-content-pr-sweeper | 7 | 100% | Only daily skill hitting nominal cadence |
| code-health | 6 | 86% | Still short-circuits on missing watched-repos.md |
| fleet-control · github-monitor · issue-triage · surplus-pulse | 5 | 71% | 09:20Z coherent-late-pocket catch-up carrying most of the load |
| batch-health · goal-tracker · heartbeat · gitlawb-fleet-metrics · notegraph · reflect · skill-freshness · skill-health | 4 | 57% | Consistently missing the 06:00Z + 06:30Z slots |
| planner · compute-futures-eda | 2 | 29% | Both last-success 2026-09-08T07:47Z — 132h stale (5.5d) |
| memory-flush · memory-structural-dedupe · pr-tracker | 1 | 14% | pr-tracker 10:00Z slot may be a new degraded pocket (see below) |
| **suggest-edges · repo-revive** | **0** | **0%** | 205h / 201h since last-success |

**Cadence coverage — weekly skills (expected 1 run / 168h):**

Firing (7): agi-tracker, cost-report, compute-pulse, milestone-tracker, vuln-scanner, workflow-security-audit, skill-evals (first-ever run 09-13; ISS-008 closed).

Overdue (9): skill-update-check (only via unscheduled trigger), skill-analytics (11d), changelog (13d), weekly-shiplog (13d), self-review (14d — resets today), janitor (14.5d), compute-macro-correlate (21.5d), skillpacks (21.5d), **skill-repair (85.5d silent — no repair skill has run since 2026-06-20)**.

**Batch outage cadence (ISS-006 series):** 6th outage filed as ISS-026 (09-12), same 4-skill tuple `{planner, compute-futures-eda, memory-flush, memory-structural-dedupe}` as ISS-023 (09-04) and ISS-025 (09-10). Lands exactly on ISS-025's 09-12 prediction — the 48h cadence framing is now superseded by daily-dead-06Z per `[[iss-006-06z-pocket-4-day-dead-streak-promotes-daily-dead-regime]]`. Next predicted slot 2026-09-14 (Mon).

**Never-dispatched (Day-66):** `ai-framework-watch` (Mon 08:30) + `run-frequency-guard` (daily 23:00) still absent from `cron-state.json`. ISS-027 was filed today for a different reason (heartbeat missing_pattern in the 08:00Z-dead-window) — no ticket yet for the never-dispatch class per `[[enabled-skills-can-never-dispatch]]`.

**pr-tracker 10:00Z pocket suspect:** pr-tracker fired exactly once in 168h (10:28Z today), 8-day gap since 09-05. This is nominally outside ISS-006's 06:00Z dead pocket, suggesting the 10:00Z window is degraded independently. Worth splitting from ISS-006 in a future filing.

**Positive micro-signals:** 05:00Z + 23:45Z pockets both 3+ consecutive days alive (per 09-12 heartbeat). notegraph fired 4× via 05:22Z / 05:08Z slots.

## Quality

**Article production (last 168h):** 9 files in git-tracked `articles/`. Composition: skill-freshness ×5 (thin status cards, ~2.5KB), vuln-scan ×2 (substantive, 7.9KB + 9.1KB), cost-report ×1 (substantive, 2.8KB), skill-evals ×1 (substantive, 5.2KB — bootstrap run, filed ISS-027, closed ISS-008). No formulaic slop; skill-freshness cards are minimal but load-bearing (48h suppress + no-change fingerprint working).

**Notification hygiene:** silent-suppression discipline held all week. `stale-content-pr-sweeper` correctly suppressed 6/7 no-close runs; batch-health only notified on the ISS-026 filing; heartbeat notified only on hash-change or 24h+ elapsed reminders; `pr-review` (9 operator invocations on swarm) posted zero verdicts and correctly suppressed 8/9 (all-skipped) plus recorded the one non-trivial verdict in log. Per-run cost pulses continue at ~$100–200/wk range (no anomalies flagged in the 09-07 cost-report; the 50% WoW drop was structurally explained by ISS-006 batch outages, not efficiency gains).

**swarm pr-review persistent noise:** 9 invocations, 100% write-blocked. Aeon-app `pr-review` policy is `report-only` on `swarm-ai-research/swarm` (n=14 confirmed Day-14 per `[[aeon-app-no-write-on-swarm-repo]]`). Reviews recorded in daily logs but never posted upstream. Continuing to invoke the skill is a real operator-tokens-burn with zero-yield PR outcomes — should be gated on either app-install of `pull_requests: write` scope, PAT-backed routing, or explicit report-only documentation of scope.

**PR comments posted:** `stale-content-pr-sweeper` closed 1 PR this week (#64 notegraph 09-12) — the only external PR-state change from any skill. All other close-attempts blocked by author-allowlist (`{aeonframework}` excludes `app/github-actions`), which is the SKILL patch item still overdue per `[[stale-content-pr-sweeper-default-author-filter-closes-zero-prs]]`.

## Memory hygiene

**MEMORY.md:** 69 lines (target ≤50). Grew from 71 (08-30 review). Bullets are dense and factual; no obvious fluff to prune. However **one bullet is now stale**: line 10's "articles/ dir never existed in git" claim was invalidated today at 17:55Z by commit `48a7486` (`chore(cron): skill-graph success`) which committed 9 pre-existing `articles/*.md` files. The cascade-close pathway remains partially valid — ISS-008 already closed today by skill-evals; ISS-002/005/009–018 remain open because their 12 target skills are disabled or otherwise silent. Recommend rewriting line 10 to describe the new blocker (skills disabled/silent, not missing dir).

**Action queue drift:** the "Land `articles/.gitkeep` in one PR" item is now moot (dir committed, 9 files landed). Should be removed. Other patch items (a)-(o) for pr-tracker, ALLOWED_AUTHORS for stale-content-pr-sweeper, snapshot-rebase gate for docs/status.md — all still unlanded and accumulating urgency.

**INDEX.md open count:** 23. Change: +1 (ISS-027 filed today), -1 (ISS-008 closed today). Net flat. But cascade-close of the 12 `no_file_match` tickets (ISS-002/005/009–018) is now blocked on *skill-execution*, not on the `articles/` path — reframing needed.

**Logs:** consistently structured (`## Skill Name` H2 + terminal marker `SKILL_OK` / `_EMPTY` / `_DEGRADED`). Skimmed 7 days × avg 180 lines = 1270 total; no format drift.

**Notegraph:** 372n / 2971h / 942s / 0-orphans / 0-bundled as of 09-12 reflect. Growth +1n/+8e in 7d. Fingerprint pipeline sandbox friction n=7+ (checked-in node helper is the durable fix, still unlanded).

## Recommendations

**Rank 1 (unchanged since 08-30, 2 weeks overdue — highest leverage):** Migrate `planner` (30 6) + `compute-futures-eda` (0 6) out of the dead 06:00Z pocket. 4 consecutive days dead is no longer stochastic; it's a permanent hole in the schedule. Alt: land per-slot cron rewrite covering all timeslots in aeon.yml. This single change unblocks memory-flush + memory-structural-dedupe (co-scheduled) and stops the ISS-019/020/021/022/023/024/025/026 outage series at 8.

**Rank 2:** Investigate and either restore or hard-disable the 9 overdue weekly skills. Highest priority: `skill-repair` (85d silent — nobody is closing issues, which means ISS-001/ISS-006 investigating-status will never advance regardless of whether the underlying issues drift). Second: `changelog` + `weekly-shiplog` (13d, both write to articles/ and were previously blocked by the same `articles/` git-absence class — now unblocked, should produce this week if scheduler slot is alive).

**Rank 3:** Ship `enabled: false` for `agi-tracker` on aeon.yml:188 before the 11th silent-Mon at 2026-09-14T13:00Z (~17h from this review). This is now the 3rd consecutive week this recommendation has been made without action. Alternative path (restore `skills/agi-tracker/SKILL.md`) remains available.

**Rank 4:** Delete the now-stale MEMORY.md line 10 framing and the "Land `articles/.gitkeep`" action-queue item. Reframe the 12 open `no_file_match` ISS tickets around the *skill-execution* blocker, not the missing directory.

**Rank 5:** Merge PR #26 (dependabot actions/checkout, MERGE-READY 5/5 CI SUCCESS since 08-24, Day-35 today) OR install repo-level auto-merge policy for `app/github-actions`. Proving end-to-end merge flow is Day-36 and the pattern is now well-characterized per `[[pr-creation-toggle-is-distinct-from-merge-capability]]`.

**Deferred (not applied by this review):** any of Rank 1–5 requires either a PR or an aeon.yml edit outside this skill's scope. Would-be `aeon.yml` edits are operator-scope per CLAUDE.md ("For code changes, create a branch and open a PR"). No PR opened by this skill run.

## Actions applied this run

- **MEMORY.md line 10 rewritten** — replaced "articles/ dir never existed in git" (falsified by today's commit 48a7486) with the new blocker framing (12 target skills disabled/silent, not the dir).
- **MEMORY.md action queue pruned** — removed the "Land `articles/.gitkeep` in one PR" bullet (moot).
- Written: `articles/self-review-2026-09-13.md` (this file), `.outputs/self-review.md`, `.pending-notify/${epoch}-self-review.md`.
- Deliberately *not* touched: `aeon.yml`, per-skill SKILL.md files, `memory/watched-repos.md`, ISS files (skill-evals owns filing/closure; skill-repair owns resolutions).

## Files

- `articles/self-review-2026-09-13.md` (this review)
- `memory/MEMORY.md` (line 10 rewrite + 1 action-queue removal)
- `.outputs/self-review.md`
- `.pending-notify/${epoch}-self-review.md`
- `memory/logs/2026-09-13.md` (appended `## Self Review` section + summary)

## Sources

`./scripts/skill-runs --hours 168 --json` · `memory/cron-state.json` (42 skills tracked) · `memory/issues/INDEX.md` (23 open) · `memory/logs/2026-09-07..13.md` · `git log --diff-filter=A -- articles/` (found 48a7486 today 17:55Z) · `articles/skill-evals-2026-09-13.md` (ISS-027 filing / ISS-008 closure evidence) · MEMORY.md current-focus (verified for drift).
