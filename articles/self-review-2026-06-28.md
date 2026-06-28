# Self Review — 2026-06-28

Window: 2026-06-21 → 2026-06-28 (8 days). One full week since the OAuth recovery; 8th consecutive day of ISS-006 dispatch underdelivery.

## TL;DR

- **Reliability: completed runs are clean, but the fleet is delivery-starved.** 100% success (104/104) across 109 workflow runs in 168h. The story isn't quality, it's *quantity*: ISS-006 — `messages.yml`'s single `*/5 * * * *` cron — has been silently dropping scheduled dispatches across multiple time-of-day pockets (06:00–06:30, 09:00, 23:45, and now 05:00) for 8 straight days. Pockets are sliding day-to-day rather than fixed.
- **Output quality: substantive when it runs, formulaic when it repeats.** Vuln-scan (vercel/eve), skill-evals, skill-analytics, surplus-pulse, compute-pulse, workflow-security-audit, and skill-graph all produced detailed, cited, actionable artifacts. The 7 daily skill-freshness articles are 95% identical (sha1 da39a3ee fingerprint hasn't moved since 2026-06-20) — the skill correctly suppresses *notifications* on no-change but still writes the *article* every day.
- **Memory: clean and current.** MEMORY.md is 38 lines (under the 50-line cap), reflect ran daily, 24 atomic notes + 6 topic MOCs + 6 structured issues. Standard hygiene is holding.
- **Operator-blocked work: stacking.** The same 6 items have ridden the `Next priorities` list for a week — most need a `GH_GLOBAL` PAT (App perm gap) or a manual cron-config edit only the operator can land.

## 1. Output quality

| Output type | Count | Verdict |
|---|---|---|
| Articles authored (window) | 11 | 7 formulaic (skill-freshness daily), 4 substantive (skill-evals, skill-analytics, vuln-scan, this review) |
| Notifications sent | ~daily-cadence | reasonable — dedup suppression working |
| PR reviews issued | 0 reviewed / 5 skipped | all dup-SHA; verdicts log-only (App perm gap) |
| PRs opened (agent) | 2 branches pushed, 0 PRs | `gh pr create` blocked by repo policy + App perm gap |
| Commits | 1 (`chore(cron): skill-graph success`) | cron-state writeback only |

**Substantive wins this week:**
- `vuln-scan-2026-06-27.md` (vercel/eve) — full scanner table, 72 GHSA advisories triaged, dep-bump PR drafted with DCO-signing instructions for the operator. Quality output.
- `skill-evals-2026-06-28.md` — recovered heartbeat eval, surfaced ISS-005 reclassification (NO_OUTPUT is expected when ledger absent — pattern is wrong, not the skill).
- `skill-analytics-2026-06-24.md` — caught 5 SILENT skills (agi-tracker, config-validator, swarm-safety-eval, ai-framework-watch, run-frequency-guard).
- `workflow-security-audit-2026-06-28.md` — 16 NEW Critical findings; branch pushed (`fix/workflow-security-audit-2026-06-28`), PR open blocked by repo policy.
- `skill-graph` init — 173 skills mapped, 5 categories, edge graph built.

**Noise:**
- 7 near-identical `skill-freshness-*.md` articles in 8 days (diff today vs 06-26 is the date string and one cell — fingerprint identical). The notify is suppressed; the *article emission* should be too. Easy fix in the skill spec.
- pr-review producing duplicate "all-skipped" log entries on the same head SHAs day after day — useful as a heartbeat, noisy as output.

**PR comments:**
- Cross-org write-perm gap on `swarm-ai-research/swarm` persists. pr-triage verdicts on @go165's #517 (DEFER, 710 lines) and #518 (ACCEPTED, first-PR welcome queued) are correct but log-only. Needs operator to install App on swarm repo OR provision a PAT.

## 2. Reliability

### Workflow execution (last 168h)

```
Total: 109 | OK: 104 | Fail: 0 | Running: 5 | Cancelled: 0
Success rate (completed): 100%
```

Pure-execution health is the best it's been since this repo started tracking. Zero auth failures, zero stuck runs, zero failed completions. ISS-001 is operationally over; the only thing keeping it `investigating` is the `success_rate < 0.6` denominator carry-over, which takes weeks to wash out by design.

### Delivery health — ISS-006 is the live problem

`messages.yml` runs `*/5 * * * *` and dispatches per-skill cron ticks. For 8 days running, dispatches have been *missing in pockets across the day*:

| Pocket (UTC) | Status (today) | Skills affected | Days silent |
|---|---|---|---|
| 05:00 ± 30m | **NEW today** | notegraph, suggest-edges | 2 (since 06-26 05:53Z) |
| 06:00–06:30 | **relapsed today** | planner, compute-futures-eda, memory-flush, memory-structural-dedupe, skillpacks, compute-macro-correlate | recovered briefly 06-27, missed again today |
| 09:00 ± 30m | **dead 6 days** | fleet-control, github-monitor, issue-triage, pr-triage, pr-review-09:00-slot | 6 (since 06-22T10:14Z) |
| 23:45 | self-resolved | stale-content-pr-sweeper | recovered 06-27 |

Cleanest evidence the problem is slot-level, not skill-level: `pr-review` is scheduled `0 9,18 * * *`. The 18:00 slot fires reliably (last_success 2026-06-27T18:53Z); the 09:00 slot has been silent for 6 days. Same workflow, same secrets, same code — only the cron hour differs.

13 enabled skills last_success >72h ago (3 are weekly so expected, 10 are ISS-006 collateral).

### Repeated error patterns

- **Cross-org App perm gap** on `swarm-ai-research/swarm` — `Resource not accessible by integration` on every pr-comment / pr-edit / label-create. Hits pr-triage and pr-review every run. Operator needs to install the Aeon GitHub App on the swarm repo, OR provision `GH_GLOBAL` PAT.
- **Repo policy: "GitHub Actions is not permitted to create or approve pull requests"** — blocks `gh pr create` from agent-initiated branches (workflow-security-audit, skill-graph). Branch push succeeds; PR open requires manual UI step or PAT.
- **`memory/watched-repos.md` missing** — 5 skills (github-monitor, issue-triage, repo-revive, code-health, weekly-shiplog) exit cleanly with `EMPTY_CONFIG` every run. Either populate the file (3-line fix) or disable the skills until needed.
- **pr-review `run-name` leak** (carried over from 2026-06-20 self-review, still unfixed) — the multi-line `var:` policy block interpolates into workflow `run-name`, producing 10-line workflow titles in the GitHub Actions UI. Cosmetic; truncate to first line.

### Monitors — signal vs noise

| Monitor | Today's signal | Verdict |
|---|---|---|
| heartbeat | Caught NEW 05:00 pocket (notegraph + suggest-edges) → notify fired | Good signal |
| batch-health | 6/8 morning skills missing → OUTAGE → ISS-006 day-8 update | Good signal |
| skill-health | NOOP (state unchanged, daily cadence skip) | Correct — DEGRADED(38) is ISS-001 residue |
| skill-evals | Heartbeat recovered, ISS-005 reclassification surfaced | Good signal |
| skill-freshness | FRESHNESS_NO_CHANGE for 8 days | Notify-correct; article emission wasteful |
| config-validator | Sun 07:00 slot missed (ISS-006 collateral) | N/A — itself a victim |

Monitors are catching real issues. The only false-positive risk is the chronic `success_rate < 0.5` flag from ISS-001 — already suppressed via `systemic` carve-out in skill-health.

## 3. Memory hygiene

| Check | Finding |
|---|---|
| `MEMORY.md` length | 38 lines (cap: 50) ✅ |
| `MEMORY.md` currency | Reflects 2026-06-27 state; today's reflect hasn't fired yet (Sunday evening slot) — staleness expected and self-healing |
| Logs | 10 files; 8 inside this window (one per day, structured, single-skill sections) ✅ |
| Topics MOCs | 6 (agi-tracker, compute-pulse, fleet-ops, pr-status, surplus-pulse, skill-freshness-state) ✅ |
| Atomic notes | 24, each ≤3 sentences, single-claim ✅ |
| Daily indexes | 8 in `memory/notes/daily/` ✅ |
| Structured issues | 6 (ISS-001..006), 4 open / 2 resolved, INDEX in sync ✅ |
| Stale `Next priorities` | 6 items unchanged ≥4 days — operator-blocked, not stale-in-content |

No pruning required this run. Memory subsystem is healthy.

## 4. Recommendations

### Apply now (safe, in-scope for self-review)

1. **None this run** — every meaningful improvement requires operator action (PAT, App install, workflow edit). Pruning MEMORY.md or feeds.yml would be cosmetic; both are already in good shape. Recording recommendations is the right output.

### Operator action needed (ordered by impact)

1. **Land ISS-006 mitigation.** Replace `messages.yml`'s single `*/5 * * * *` with explicit per-slot crons covering every `aeon.yml` timeslot. The slot-level evidence (pr-review 09:00 dead / 18:00 fine, same workflow) rules out a morning-only patch. Planner has ranked this "today's one thing" for 2 consecutive days; needs a human commit. Branch suggestion: keep `*/5` for the polling path, add discrete `:00 :05 :10 ... :45 :50 :55` per the hours `aeon.yml` actually uses.
2. **Provision `GH_GLOBAL` PAT** (or install the Aeon GitHub App on `swarm-ai-research/swarm` and add `workflows: write` to this repo's installation). Unblocks: workflow-security-audit PR open, skill-graph PR open, pr-review/pr-triage cross-org write paths. Three current `Next priorities` items collapse into one action.
3. **Suppress skill-freshness article writes when fingerprint is unchanged.** Today's skill writes the article *and* the dedup-suppressed notification line. Match notify behavior on the article: don't emit unless content changes. ~5 lines in SKILL.md.
4. **Truncate `pr-review` `run-name`.** Still leaking 10-line workflow titles 8 days after first flagged in `self-review-2026-06-20.md`. Change `aeon.yml` `run-name` interpolation to take only `inputs.var` line 1.
5. **Decide on `memory/watched-repos.md`.** 5 enabled skills depend on a file that doesn't exist. Either populate it (one entry per line, e.g. `- swarm-ai-research/swarm`) to activate them, or set them `enabled: false` until you do. Current state is "scheduled work that always no-ops."
6. **File `generate-skills-json` bugs as structured issues** (8+ days overdue per goal-tracker caveat — `[[generate-skills-json-newline-bug]]`, `[[skills-json-count-drift]]` notes exist but no ISS-NNN files).
7. **Patch `pr-tracker` SKILL.md** — both gh-search API drift (drop `headRefName`/`mergedAt`/`--state merged`) AND switch from `ai/` branch prefix filter to commit-author email filter (`BOT_EMAIL=aeonframework@users.noreply.github.com`). 8 consecutive empty days under the current filter while `Panniantong/Agent-Reach#436` (security/ branch, aeonframework author) was silently dropped.

### Watch / deferred

- **agi-tracker Monday slot.** Missed 2026-06-15 + 2026-06-22 (2 consecutive). Next slot 2026-06-29 13:00 UTC. File a structured issue if it misses a 3rd time.
- **ISS-001 close decision.** Operationally over since 2026-06-20 recovery. Cumulative `success_rate < 0.6` will keep flagging for ~2 more weeks. Current policy: defer close until ISS-006 stabilizes — keep deferred.
- **Skill set sizing.** 47 `enabled: true` skills out of 174 SKILL.md files in `skills/`. The disabled 127 are mostly content/social/finance pipelines on `enabled: false`. No additions or removals recommended from this review.

## 5. Numbers, for the record

- 109 workflow runs in last 168h; 104 OK / 0 fail / 5 in-progress.
- 100% success rate on completed runs.
- 47 skills `enabled: true` in `aeon.yml`; 41 tracked in `cron-state.json`; 6 enabled-but-untracked (likely first-run pending).
- 11 articles authored in window (7 formulaic freshness, 4 substantive).
- 1 commit (`chore(cron): skill-graph success`).
- 0 PRs merged by aeon (2 branches pushed, both PR-create-blocked).
- 38-line `MEMORY.md`; 24 atomic notes; 6 topic MOCs; 6 structured issues (4 open, 2 resolved).
- 8 consecutive days of ISS-006 multi-pocket cron underdelivery; 4 distinct pockets observed across the window (05:00, 06:00–06:30, 09:00, 23:45).

— Self Review, 2026-06-28.
