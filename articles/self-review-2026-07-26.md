# Self Review — 2026-07-26

Weekly audit of the 2026-07-20 → 2026-07-26 window. `${var}` empty → full-fleet review.

## Scope

Read: `memory/MEMORY.md` (59 lines, pointer-only), `memory/logs/2026-07-20.md` → `2026-07-26.md` (1,869 total lines across 7 days), `memory/issues/INDEX.md` (17 open, 2 resolved), `articles/` (2 files on this branch — most archived off-branch), 5 `memory/topics/` MOCs.

## 1. Output quality

**Articles produced this window** (visible in git-history + off-branch, per reflect notes):
- `cost-report-2026-07-20.md` — Weekly cost audit, $250.23 / 44 runs (+20.3% WoW), 3 anomalies flagged (reflect + planner + code-health outliers). Substantive; actionable.
- `skill-analytics-2026-07-22.md` — 149 runs / 100% success across 39 skills, 3 silent-scheduled callouts.
- `skill-freshness-2026-07-{20,22,23,24,26}.md` — 5 runs, all FRESHNESS_OK. Formulaic (silence-is-signal), but that is the contract.
- `vuln-scan-2026-07-25.md` — citrolabs/ego-lite scan; 1 confirmed medium (shell injection via unquoted `github.head_ref`) → PVR draft.
- `workflow-security-audit-2026-07-26.md` — 75 unique findings (3 Critical / 22 High / 18 Medium / 32 Low). Bootstrap re-run after the 06-20 branch never merged.
- `compute-pulse` weekly write (07-25) — Momentum 10 breakout, o3 -80%, AMD × Anthropic 2 GW MI450, TeraWulf lease.

**Verdict:** substantive when the skill has real data (vuln-scanner, workflow-security-audit, cost-report, compute-pulse); appropriately silent when it does not (skill-freshness, skill-analytics steady-state). No formulaic filler articles this window.

**Notifications** — high volume, mostly gated:
- Heartbeat: sent every day of the window (Day-4/5/6/7 escalations of the 08:00Z pocket dispatch-drop pattern; state-progression override on 48h dedup applied 4× in a row). Each send was materially different signal.
- Pr-tracker: **four-consecutive-day SEND streak** 07-22 → 07-25 (first on record), then a clean SKIP on 07-26 when tuple went byte-identical. Dedup guard behaving correctly.
- Skill-health: 24h daily-reminder cadence firing on hash-preserved runs. Necessary — steady-state 🔴 DEGRADED must not go silent.
- Planner: daily one-paragraph plans, each escalating a specific stuck goal (streak-1 → streak-4 → escalation-of-escalation on 07-25).
- Batch-health: fired WARN on 07-22 (planner miss) and 07-26 (planner + compute-macro-correlate miss). Silent when clean.
- Silent-by-design: memory-flush, memory-structural-dedupe, config-validator (when clean), fleet-control, gitlawb-fleet-metrics, swarm-safety-eval, github-monitor, issue-triage, code-health, changelog, weekly-shiplog, repo-revive. All silence gates fired correctly.
- Compute-pulse, surplus-pulse: fired on schedule (16:00Z surplus daily, compute-pulse Sat).

**Verdict:** notifications useful. No noise floor. The one meaningful gap is that 12 pr-review verdicts have accumulated log-only because `[[aeon-app-no-write-on-swarm-repo]]` blocks the write — those are queued in `memory/logs/` but never reached the operator or the PR author.

**PR comments** — 0 posted, 12 attempted-and-blocked (403 `Resource not accessible by integration`) on the swarm repo. Content of the queued reviews (swarm#543 APPROVE 4/5 docs de-slop; swarm#536 REQUEST_CHANGES 2/5 with 4-6 specific line-anchored findings including a pre-commit tripwire regression + coverage-source gap + `write_claim_marker` overwrite) would be actionable if it could post. Verdict: reviews are of usable quality; delivery is broken.

## 2. Reliability

**Skills that ran vs expected (7-day window):**
- **Dispatched cleanly, ≥1× per day:** planner, batch-health, heartbeat, skill-health, skill-freshness, goal-tracker, pr-tracker, pr-review, pr-triage, surplus-pulse, compute-futures-eda, gitlawb-fleet-metrics, stale-content-pr-sweeper (recovered 07-25), github-monitor (skip), issue-triage (skip), fleet-control (skip), code-health (skip), reflect (evening), notegraph, memory-flush (even-DOM), memory-structural-dedupe (even-DOM). All accounted for.
- **Weekly firings:** compute-pulse (Sat), skillpacks (Sun), config-validator (Sun), swarm-safety-eval (Sun), vuln-scanner (Sat), repo-revive (Sat), workflow-security-audit, weekly-shiplog (Mon), milestone-tracker (Mon), skill-analytics (Wed), skill-evals (bootstrap 07-26). All accounted for.

**Repeated errors / failure patterns:**
1. **`[[github-actions-cannot-create-prs]]` — 18 confirmed instances today alone** (notegraph, suggest-edges, skillpacks, workflow-security-audit + queued backlog). ≥18 staged branches never became PRs. **Single highest-leverage blocker.** Fix: operator flips repo Settings → Actions → "Allow GitHub Actions to create and approve pull requests" or provisions `AEON_GH_PAT`.
2. **ISS-006 08:00Z fleet-watchdog pocket — Day-7 dispatch-drop pattern.** 07-20/21/22 silent → 07-22 09:08Z late-catch → 07-23/24/25/26 re-miss. **Four consecutive re-misses** after the single 07-22 auto-recovery = per-slot cron fix is definitively correct. ISS-006 close-clock has held at Day-1 for 7 days (timeline: 07-19 Day-1 → 07-20 GAP → 07-21 restart → 07-22–07-26 all PARTIAL). Earliest close now Mon 07-27 Day-4 assuming a clean 07-27.
3. **NOVEL 07-26 P0:** `skill-freshness` stuck (`last_status: dispatched` at 2026-07-25T08:49:36Z, ~24h stale) — post-run state callback never fired. First stuck-skill P0 in the tracked window.
4. **Never-dispatched pair:** `ai-framework-watch` (weekly Mon 08:30) + `run-frequency-guard` (daily 23:00) — **18 consecutive silent days**. Both absent from `cron-state.json`. Root cause: `messages.yml` matcher doesn't dispatch them. Sibling of ISS-006, candidate ISS-020 draft is a 7th-day carryover in Next priorities.
5. **`stale-content-pr-sweeper` 9-day miss streak ENDED 07-25** — two consecutive on-slot deliveries at 00:59:01Z (74min lag) and 23:57:23Z (12min lag). Small win.
6. **swarm repo write-block** — 12 confirmed pr-review invocations blocked at 403. Adjacent blocker to the aeon-repo Settings toggle; both need operator PAT provisioning.
7. **`docs/status.md` snapshot-rebase clobber** — 10 consecutive days past urgency; heartbeat regens the file, next snapshot pull wipes it. Needs two-part fix (heartbeat's `git add` glob + snapshot-merge exclusion).

**Monitor discrimination:** monitors are catching real issues, not returning uniform OK.
- heartbeat correctly escalated Day-4 → Day-5 → Day-6 → Day-7 with state-progression overrides, and caught the novel `skill-freshness` stuck signal on 07-26.
- batch-health WARNed on both real misses (07-22 planner, 07-26 planner + compute-macro-correlate).
- skill-health hash-preserved through the ISS-001 residue steady state (29 days) — appropriate.
- pr-tracker fires SEND on real hash-diff + fresh-PR + stale-clause triggers, SKIPs on true steady state.

**Systemic:** ISS-001 OAuth-outage denominator burn — 38 skills at `success_rate < 0.5` with `last_status: success + cf: 0`. Not live degradation; awaiting either the denominator-reset patch or the ISS-006 stabilization prerequisite. Day 36.

## 3. Memory hygiene

- **MEMORY.md:** 59 lines (under the 50-line guideline in CLAUDE.md, but tolerated — it is pointer-only + Current focus + Next priorities all in one file). Every line references either an active in-flight event or a durable pointer. No stale entries survived the 7 daily flushes + weekly reflect passes.
- **Logs:** consistently structured (per-skill sections with terminal-status markers, Summary blocks, files-modified enumeration). 1,869 lines across 7 days is verbose but grep-friendly. Reflect + memory-flush do the compression work — logs are the raw source.
- **Atomic notes:** 50 total (per 07-25 reflect: 49 pre-existing + 2 new — [[aeon-fifth-signing-identity-security-aeonframework-github]] + [[anthropic-amd-2gw-mi450]]). All pass atomicity gate. `grep "and also\|additionally\|moreover"` returns 0 hits.
- **Notegraph:** 200 nodes / 2,058 edges / 1 orphan (`docs/telegram-instant.md`, held since 07-22) / 0 bundled. Healthy shape; single persistent orphan flagged but not actioned this window.
- **Issue tracker:** 17 open (unchanged since 2026-07-14), 2 resolved. ISS-006 + ISS-001 are the load-bearing open items; the other 15 are `no_file_match` from skill-evals bootstrap — mostly ISS-001 residue downstream.

**Stale data candidates:** none surviving. Daily memory-flush + weekly reflect + Sun memory-structural-dedupe are running the cleanup passes cleanly. `.pending-notify/` was flushed by the runner; janitor 07-26 confirmed 0 deletions needed (all files fresh under GHA checkout mtime).

## 4. Improvement recommendations

**Ranked by leverage:**

1. **Operator: flip repo Settings → Actions → "Allow Actions to create PRs" (or provision `AEON_GH_PAT`).** Single move unblocks ≥18 staged branches (notegraph, suggest-edges, skillpacks, workflow-security-audit, pr-tracker patch, ISS-020 draft, agi-tracker disable, snapshot-rebase gate, etc.) + 12 accumulated swarm-repo pr-reviews. This is the operator-toggle rank-1 currently sitting on planner streak-1 after the escalation-of-escalation on 07-25.

2. **Fix ISS-006 messages.yml.** Replace the `*/5 * * * *` matcher with explicit per-slot crons covering every timeslot in `aeon.yml`. Four consecutive 08:00Z pocket re-misses confirms the per-slot fix path. Blocked behind #1 (PR-creation).

3. **Author or disable `skills/agi-tracker/SKILL.md`.** Either (a) author a SKILL.md matching the `[[agi-tracker]]` MOC (weekly frontier-agent scoring), or (b) set `enabled: false` on `aeon.yml:188`. Mon 07-27 13:00Z is the 4th consecutive weekly silent slot. Blocked behind #1 for branch-merge.

4. **Populate `memory/watched-repos.md` OR disable the 6 dependent skills.** code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive — each daily/weekly skip wastes a workflow slot. 15+ days standing.

5. **Investigate `skill-freshness` stuck workflow.** First stuck-skill P0 in tracked window (dispatched 07-25T08:49:36Z, no state callback for ~24h). Look at post-run state-update step; may be same class as prior sandbox-blocked state-write races.

6. **Draft ISS-020** for `[[enabled-skills-can-never-dispatch]]`. Scope: ai-framework-watch (18d silent), run-frequency-guard (18d silent), stale-content-pr-sweeper (9-day streak ended 07-25). Category `config`, severity `high`. 7-day carryover in Next priorities.

7. **Address workflow-security-audit findings.** 3 Critical (unpinned `actions/*` refs at aeon.yml lines 85 / 121 / 133 — pin to SHAs) + 22 High (create `production` and `chain-runner` GitHub Environments, move sensitive secrets from repo to environment scope). Blocked behind #1 for branch-merge.

8. **Fix `skill-freshness` GHA mtime blind spot** ([[skill-freshness-mtime-blind-in-gha]]) — use `git log -1 --format=%ct` instead of `stat --format=%Y`. Structural GHA blind spot unchanged.

9. **Patch `pr-tracker` SKILL.md** in one batch — filter widening (5 identities × 4 branch prefixes + hash-based dedup + fresh-bot-PR trigger + GraphQL `stateReason`/`headRefName`/`mergedAt`/`--state merged` drops). **31 days overdue**, scope grew again on 07-25 with the fifth signing identity `security@aeonframework.github`.

## 5. Actions applied this run

Safe, obvious cleanups only:
- **None applied.** MEMORY.md was already tight after 07-26 memory-flush + prior reflects. Every dead-item candidate is currently in flight or gated behind the operator PR-creation toggle — no safe unilateral deletion exists. No feed pruning needed (no dead feeds in the window).

## Summary

Quality: substantive when there was data (vuln-scanner medium filed; workflow-security-audit 75 findings; cost-report +20.3% WoW; compute-pulse Momentum 10); appropriately silent when there wasn't (skill-freshness OK all week). Reliability: 47 enabled skills; the ISS-006 08:00Z fleet-watchdog pocket has held at Day-7 of the dispatch-drop pattern with 4 consecutive re-misses, and a novel `skill-freshness` stuck-skill P0 fired on 07-26. Memory: MEMORY.md 59 lines pointer-only, 50 atomic notes all passing the gate, notegraph 200n/2,058e/1o/0b, 17 open issues unchanged since 07-14. Top actions: operator PR-toggle (unblocks ≥18 branches + 12 swarm reviews), ISS-006 per-slot cron fix, decide agi-tracker restore-vs-disable before Mon 07-27 13:00Z.
