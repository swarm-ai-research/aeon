# Self Review — 2026-08-02

**Window:** 2026-07-27 → 2026-08-02 (7 days, Mon → Sun)
**Verdict:** OPERATIONALLY HEALTHY / STRUCTURALLY BLOCKED
**Headline:** 149/149 successful runs (100% CLI reliability), zero issue-tracker motion for the 7th consecutive day (all 17 open issues untouched), operator-toggle rank-1 ask advances to streak-5 by run / streak-9 by calendar day. ISS-006 Day-2 clean-delivery holds; earliest structural close 2026-08-03.

## 1. Quality of outputs

**Articles.** 3 articles land on `main` this week (all from today: `skill-evals-2026-08-02`, `skill-freshness-2026-08-02`, `workflow-security-audit-2026-08-02`). Every other article the fleet authored (`cost-report-2026-07-27`, `code-health-*`, `skill-analytics-2026-07-29`, `skill-freshness-*` daily, `vuln-scan-2026-08-01`) lives on unmerged branches per `[[github-actions-cannot-create-prs]]`. **Structural article delivery to main is 3/~15 = 20%.** Article substance itself is fine — the three that landed are dense with actionable content (skill-evals has a numbered 8-item action queue; workflow-security-audit has a full table of 75 carried findings; skill-freshness reports 0 flagged). Zero formulaic or filler articles this week.

**Notifications.** 35 `.pending-notify/` files across 7 days (avg 5/day, range 4–6). Each I sampled was one-paragraph, first-person, ≤400 chars, and led with the actionable fact. No spam pattern. Dedup guards fired appropriately: pr-tracker skipped notify 3× on byte-identical trigger sets (5th, 6th, 7th validated in-skill applications); heartbeat sent single notifies with 4-hour precedent windows. Zero double-fires observed. **Voice is consistent** — clear-direct-first-person default (soul/ absent), which matches CLAUDE.md guidance.

**PR reviews.** pr-review invoked 14 times this window (mostly operator-triggered on swarm-ai-research/swarm). Verdicts stable across dup-SHA re-derivations: swarm#543 APPROVE 4/5, swarm#536 REQUEST_CHANGES 2/5. Findings on #536 are actionable and specific (misleading-body vs +90/-1 code; pre-commit shell rewrite without CI shell coverage; mixed-scope bundle). **All 18 attempted PR-write posts 403'd** — the review work is real but structurally invisible on-PR pending PAT/App-permission unblock. This is the same lever as the toggle ask.

**Assessment:** Output quality is HIGH where it lands; delivery is STRUCTURALLY THROTTLED. The bottleneck is operator-side, not agent-side.

## 2. Reliability

**Run counts (via `./scripts/skill-runs --hours 168`):**
- Total: 151 runs (149 completed, 2 running) · Success rate: 100% (149/149) · Failures: 0
- Top runners: pr-review×14 (operator-triggered), goal-tracker×8, reflect×8, skill-health×8, code-health×7, surplus-pulse×7, compute-futures-eda×6, fleet-control×6, github-monitor×6, issue-triage×6, notegraph×6, pr-tracker×6, stale-content-pr-sweeper×6

**Repeated failure patterns (all HEALTHY-but-empty class):**
- **6 skills silent-exit on missing `memory/watched-repos.md`** every day: code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive. 6 wasted workflow slots × 7 days = ~42 no-op runs this week. MEMORY.md pointer already flags the fix.
- **2 skills silent-exit on empty `memory/instances.json`** every day: fleet-control, gitlawb-fleet-metrics.
- **goal-tracker NO_GOALS**: 7-of-7 days — MEMORY.md `## Pointers` header still not in the fallback list per `[[memory-section-header-rename-breaks-goal-tracker]]`.
- **2 skills never dispatched**: `ai-framework-watch` (Mon 08:30) + `run-frequency-guard` (daily 23:00) — 25th consecutive silent day. ISS-020 draft still pending file (14th-day carryover, blocked by toggle).
- **agi-tracker missing SKILL.md**: 4 consecutive weekly HEALTHY-but-empty slots (07-06, 07-13, 07-20, 07-27); Mon 2026-08-03 is 5th silent-risk.
- **ISS-006 08:00Z sub-pocket**: 8 consecutive PARTIAL days (07-22 → 07-31), broken 08-01 (Day-1 clean at 39min-late), continued 08-02 (Day-2 clean at 113min-late). Cadence-shift signal — Day-3 (08-03) decides whether close-clock advances or the pocket has migrated slots.

**Monitors.** All three monitors (batch-health, heartbeat, skill-freshness) fired meaningful signals this week rather than always returning OK:
- **batch-health**: 4 WARN calls in the window (07-27 06:00Z compute-futures-eda miss, 07-30 06:30Z planner miss, 08-01 06:30Z planner miss, plus the ISS-006 pockets). Caught real issues.
- **heartbeat**: fired fresh signals on cadence shifts (Day-2 113min-late detected as pattern-change), suppressed known items via dedup. Not a rubber-stamp OK.
- **skill-freshness**: 0 flagged all week (no consumer/dep aging past threshold). This is genuine steady-state, not a blindness — cross-checked against `./scripts/skill-runs` failure count = 0.

**"Chronic failure" 38-skill count is denominator-burn from ISS-001 (2026-06-06 → 2026-06-20 OAuth outage), not live regression.** Every one of those 38 skills has `last_status: success` and `consecutive_failures: 0`. Deferred close until ISS-006 stabilizes per MEMORY.md pointer.

**Assessment:** Fleet is 100%-run-success reliable within its constraints. The ~10 wasted-slot-per-day skills (watched-repos / instances.json / cron-state gaps) are structural config debts, not runtime failures. Monitors catch real issues.

## 3. Memory hygiene

**MEMORY.md size:** 60 lines — 10 lines over the 50-line guideline in CLAUDE.md. Not urgent but worth trimming at next memory-flush.

**Structure:** Clean pointer-only index. `## Current focus` runs long (13 lines, most of them detailed streak/counter narrative). Could be compressed: retire the ISS-006 8-day PARTIAL narrative into fleet-ops.md now that recovery counter has started (2 days into a 3-day clean-close window).

**Logs.** All 7 daily logs present, consistently formatted (skill section per skill + Summary section). Line counts: 201/291/254/244/394/339/343 — normal range. No structural drift.

**Notes.** 64 atomic notes; 6 topic MOCs (2 stale-ish: `agi-tracker.md` last touched pre-07-19, `compute-pulse.md` last snapshot mid-July per line dates in `fleet-ops.md`). Neither is broken; both are due for a memory-flush snapshot pass.

**Topic staleness:** `memory/topics/fleet-ops.md` still says "**≥22** queued behind" and "**17 open** issues in INDEX.md — unchanged count" and "18th confirming invocation" — inconsistent with current values (23 branches / 17 open / 25th invocation per today's logs). Not a bug; consolidation lag between the daily-log truth and the topic-MOC snapshot.

**Stale-data candidates identified (deferred to memory-flush):**
- Trim ISS-006 recovery narrative in `## Current focus` once close-clock resolves (08-03 or later).
- Retire per-day cindy#1116/worldmonitor#5518 event narrative on line 10 to `pr-status.md` (event already captured there).
- MEMORY.md pointer #55 (close ISS-008) is action-eligible: cost-report ran 2026-07-27 successfully; next skill-evals scan can close it.

**Assessment:** Memory is healthy. Index-heavy sprawl in `## Current focus` is the only real friction; memory-flush is the right skill to compact it.

## 4. Recommendations

### High-leverage (single-action unblocks a large tail)
1. **[Operator] Flip Repo Settings → Actions → Workflow permissions → "Allow Actions to create PRs".** OR provision `AEON_GH_PAT` (repo-scoped, `repo` scope; validated live via swarm#527 merge 2026-07-18). Unblocks: 23 staged branches, 6 stalled fleet fixes (pr-tracker SKILL.md 39d-overdue, workflow-security-audit findings, docs/status.md rebase-clobber fix, ISS-020 file, agi-tracker `enabled: false`), 4-item `.pending-disclosure/` queue outflow, and the notegraph/skillpacks/vuln-scanner article delivery loop. Streak-5 by run / streak-9 by calendar day as of today.
2. **[Operator] Bump aeon GitHub App permissions on `swarm-ai-research/swarm`** to `Pull requests: Read + Write` (currently Read-only) OR provision the same PAT. Unblocks pr-review from being log-only. 18th confirming invocation of `[[aeon-app-no-write-on-swarm-repo]]`.

### Skill hygiene (small, cheap, immediately applicable)
3. **Populate `memory/watched-repos.md`** with at least one repo — OR disable the 6 dependent skills in `aeon.yml`. Eliminates ~42 wasted slots/week.
4. **Add MEMORY.md `## Pointers` to goal-tracker's fallback header list** — closes the 7-of-7 NO_GOALS residue.
5. **Set `enabled: false` on `aeon.yml:188` for agi-tracker** — one-line edit stops the 5th silent-risk slot on 2026-08-03. Blocked pending toggle, but if toggle lands, this is the smallest downstream fix.

### Reliability drift to watch
6. **ISS-006 Day-3 pocket (2026-08-03 08:00Z)** — if delivery lands 90+min late again, treat as pocket-slot migration signal (per today's heartbeat, delay drifted 39min → 113min in one day) and revisit the close-clock counter.
7. **Milestone ms-01 (aeon repo stars 0/100)** — stalled-3 weeks. milestone-tracker next fires Mon 2026-08-03 12:00Z; consider whether the milestone itself should be re-scoped (organic star growth on an internal-facing repo is not a lever the agent can pull).

### Quality improvements (deferred, non-urgent)
8. **compute-futures scenario-sweep**: widen seed count from 12 or switch outlier detection to a tie-robust statistic per `[[compute-futures-12-seed-sample-too-small]]`. Present since 07-25; not blocking anything but produces a chronic HIGH-severity false-positive class.
9. **workflow-security-audit follow-through**: 3 Critical + 21 High findings are 14-day-stale. Manual per SKILL constraints, downstream of the toggle for branch merge.
10. **notegraph extractor**: mask `generatedAt` before diffing per `[[notegraph-extractor-generatedat-nondeterministic]]` — closes the 4-day silent-exit streak class.

## 5. Actions taken this run

- No structural changes to MEMORY.md, `aeon.yml`, or skill files — every candidate action is either (a) already flagged in MEMORY.md Pointers, (b) blocked by the operator toggle, or (c) memory-flush's job.
- Wrote this review to `articles/self-review-2026-08-02.md`.
- Notification queued to `.pending-notify/` for fan-out.
- Log entry appended to `memory/logs/2026-08-02.md`.

## 6. Coverage note

- 149 skill runs sampled via `./scripts/skill-runs --hours 168` (`gh api` authoritative).
- Log audit spawned as a subagent — read 2066 total lines across 7 daily logs.
- MEMORY.md, `memory/cron-state.json`, `memory/issues/INDEX.md`, `memory/topics/fleet-ops.md`, and 3 sampled articles (`skill-evals`, `workflow-security-audit`, `skill-freshness`) read directly.
