# Self Review — 2026-07-05

**Window:** 2026-06-28 → 2026-07-05 (8 daily logs, 1,455 total lines)
**Focus (`${var}`):** empty — full review

## Verdict

- **Quality:** GOOD. Logs are substantive, cross-linked to durable claims, and honest about false positives. No formulaic filler.
- **Reliability:** DEGRADED but stable. 38/42 skills at `success_rate<0.5` remain ISS-001 denominator drag (all `last_status=success`, `consecutive_failures=0`). Live fleet is green.
- **Memory hygiene:** CLEAN. MEMORY.md 50 lines (at cap), 33 atomic notes + 16 daily indexes + 5 topic MOCs, reflect ran daily.
- **Systemic blockers:** ISS-006 day 15 (cron underdelivery) and 7-branch operator PAT queue are still the two structural bottlenecks — neither self-solves.

## 1. Output quality

**Articles on disk (2026-07-05):** `skill-evals-2026-07-05.md`, `skill-freshness-2026-07-05.md`. Other agent output lands in `memory/logs/` daily files and `memory/topics/` MOCs — the article directory is not the whole surface.

**Log substance (last 7 days):** each skill run captures state, deltas vs prior run, drift claims, and follow-ups. No boilerplate. Examples worth calling out:
- `pr-tracker 2026-07-05` self-caught two SKILL.md drift bugs mid-run (GraphQL `stateReason` on `PullRequest`; `./notify -f` unsupported) and atomized both as durable claims within the same day's `reflect`.
- `reflect 2026-07-05` produced 4 new atomic notes distilled from a single day's log — high signal density.
- `workflow-security-audit 2026-07-05` shipped SHA-pinning across 6 workflows, resolving 13/16 Critical `unpinned-uses` from the 2026-06-28 audit. Real progress.

**Notification noise:** two problem patterns this week:
1. **pr-tracker sent identical notify 2 consecutive days** (2026-07-04, 2026-07-05) with zero state change — same 3-PR set at same SHAs. Step-5 has no dedup guard. Durable claim atomized as [[pr-tracker-notify-repeats-with-no-state-change]].
2. **skill-health cadence-gate fires every ~24h** at unchanged hash `ab229111a167c4a2` for 9 straight days. Signal degraded to wallpaper — the "38 DEGRADED, all ISS-001 residue" message is now familiar and no longer actionable.

**Article coverage gap:** `skill-evals-2026-07-05.md` shows only 14/49 skills (28%) have `evals.json` entries. 30+ enabled skills have no eval regex — coverage bootstrap started today but list is long.

## 2. Reliability

**Fleet snapshot (cron-state.json, 42 tracked):**
- `success_rate ≥ 0.5`: 4 (agi-tracker, config-validator, swarm-safety-eval, weekly-shiplog)
- `success_rate < 0.5`: 38 — all ISS-001 OAuth-outage residue, denominator drag
- Recent success (<48h): 31
- Stale (>48h since last_success): 11 — cost-report (374h), janitor (374h), memory-structural-dedupe (374h), milestone-tracker (374h), skill-repair (374h), weekly-shiplog (322h), skill-analytics (264h), self-review (169h), skill-update-check (168h), changelog (146h), agi-tracker (149h)

All 11 stale entries are weekly/biweekly skills whose slots have been eaten by ISS-006 pocket misses — not skill defects.

**Live failure count:** zero (0 `consecutive_failures ≥ 2` across the fleet).

**Open issues (6):** ISS-001 (OAuth), ISS-002 (changelog no_file), ISS-005 (swarm-safety-eval), ISS-006 (cron underdelivery), ISS-007 (heartbeat missing_pattern — **false positive today**), ISS-008 (cost-report no_file).

**ISS-007 is a false positive.** skill-evals ran at 09:00Z; heartbeat ran at 09:58Z (~2h late per ISS-006 pocket miss). By the time heartbeat wrote its section into `memory/logs/2026-07-05.md`, skill-evals's regex scan had already completed and recorded `missing_pattern:heartbeat|Heartbeat|HEARTBEAT`. The heartbeat entry IS in the log (with `HEARTBEAT_OK · STATUS_PAGE=DEGRADED`). Recommend skill-evals adds a same-day grace window or reads the log twice.

**ISS-006 progress signal (day 15):** the 07:44Z GHA burst broke two 15-day silences (skillpacks + compute-macro-correlate first success since 2026-06-20). But janitor (05:30) stayed cold and the 08:00 batch fired ~2h late — classic stuck-then-flush signature per [[iss-006-pocket-recovery-is-noise]], not resolution. Correctly classified as noise by today's `reflect`.

**Repeated errors:** none live. The recurring log patterns (5 watched-repos-dependent skills silent-skipping, cross-org write-permission 403s, GHA-cannot-create-PRs) are all traced to durable claims — no fresh failure classes this week.

## 3. Memory hygiene

- **MEMORY.md:** 50 lines exactly, at the ~50-line cap. Today's reflect bundled the 5 pr-tracker patch items into one line and consolidated Next-priorities — good discipline.
- **Notes:** 33 atomic notes, all single-claim (verified by today's reflect — 0 splits required).
- **Daily indexes:** 16 in `memory/notes/daily/`.
- **Topic MOCs:** 5 files — `agi-tracker`, `compute-pulse`, `fleet-ops`, `pr-status`, `surplus-pulse` (plus `compute-futures-eda/` subdirectory).
- **Notegraph:** 121 nodes · 754 hard + 333 soft edges, 1 orphan, 0 bundled (2026-07-05 post-reflect). Edge:node ratio ~20× is healthy density.
- **Stale data:** none flagged by today's reflect. Log format is consistent across all 8 files (per-skill sections + summaries).

## 4. Actions taken this run

- **None applied.** Per CLAUDE.md health-skills / repair-skills contract, self-review files findings but does not close issues or patch SKILL.md files.
- MEMORY.md is at cap and was just consolidated by today's reflect — no pruning warranted.
- `feeds.yml` does not exist in this repo — nothing to prune there.

## 5. Recommendations (ranked)

1. **Ship ISS-006 `messages.yml` per-slot cron rewrite.** Day 15, third consecutive planner top-priority, 6 weekly/biweekly skills at 2× threshold. The 07:44Z burst is stuck-then-flush noise, not recovery. Draft branch `fix/iss-006-per-slot-crons` — operator opens the PR.
2. **Close ISS-007 as false positive OR add same-day grace to skill-evals.** Today's regex scan raced heartbeat's late fire. Two clean fixes: (a) skill-evals waits until 12:00Z before scanning same-day logs, OR (b) skill-evals re-scans at reflect time and closes false positives. Recommend (a).
3. **Fix `./notify -f <file>` documentation-vs-implementation gap.** Two skills used the flag this week (pr-tracker + surplus-pulse); both silently corrupted their notifies to the literal string `-f`. Either add `-f` support to `./notify` OR patch every SKILL.md invocation to `MSG=$(cat file); ./notify "$MSG"`. See [[notify-script-has-no-f-flag]].
4. **Patch pr-tracker SKILL.md in one batch.** Five drift items already bundled in MEMORY.md line 41: (a) drop `stateReason` from GraphQL, (b) drop `headRefName`/`mergedAt`/`--state merged`, (c) list/domain commit-author filter, (d) step-5 dedup guard, (e) fresh-bot-PR trigger.
5. **Provision cross-repo PAT to clear the 7-branch operator queue.** Blocked branches: `agi-tracker/2026-06-29`, `notegraph/2026-07-04`, three `fix/workflow-security-audit-*`, `skill-graph/2026-06-28`, `skillpacks/2026-07-05`. The PAT is the actual unblock; queuing more branches only lengthens the tail.
6. **Populate `memory/watched-repos.md` OR disable the four watched-repos-dependent skills** (code-health, github-monitor, issue-triage, changelog). Daily wasted-slot pattern held all 7 days.
7. **Expand skill-evals coverage.** 14/49 skills covered (28%). Add regex entries for the 30+ enabled skills currently uncovered — top-10 list already in `articles/skill-evals-2026-07-05.md`.
8. **Fix `docs/status.md` auto-commit drop.** heartbeat regenerated the page on 07-04 and 07-05 but the workflow auto-commit step doesn't stage `docs/`. See [[status-md-auto-commit-drops-writes]].
9. **Fix `skill-freshness` to use `git log -1 --format=%ct` with deep clone.** 7th consecutive FRESHNESS_OK is structurally blind, not clean. See [[skill-freshness-mtime-blind-in-gha]].

## 6. Sources
- `memory/MEMORY.md` (50 lines)
- `memory/logs/2026-06-28.md` … `2026-07-05.md` (1,455 lines total)
- `memory/cron-state.json` (42 entries)
- `memory/issues/INDEX.md` (6 open, 2 resolved)
- `articles/skill-evals-2026-07-05.md`, `articles/skill-freshness-2026-07-05.md`
- `memory/notes/` (33 atomic notes, 16 daily indexes)
- `memory/topics/` (5 topic MOCs)
