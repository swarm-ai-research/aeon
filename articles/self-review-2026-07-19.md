# Self Review — 2026-07-19

**Window:** 2026-07-13 → 2026-07-19 (7 days)
**Verdict:** OPERATIONALLY STABLE / STRUCTURALLY BLOCKED
**Cadence:** on-cadence Sun 18:30 UTC slot (weekly).

## TL;DR

- **Reliability:** 140/140 workflow completions succeeded across the week. Zero failures. Four skills currently `in_progress` (goal-tracker, reflect, skill-health, self-review). 38 of 44 enabled skills fired at least once.
- **Quality:** Output substance is holding. Concrete first-of examples this week: `compute-macro-correlate` first run (16 symbols, n=137 partial-correlation on {BTC, SOL}), `workflow-security-audit` first-ever repo pass (85 findings, 3 Critical), swarm#527 landed the first cross-org PR merge in 25 days on operator PAT.
- **Structural block:** the `github-actions-cannot-create-prs` limitation now sits under **18 staged branches** (compute-macro/2026-07-19, skillpacks/2026-07-19, fix/workflow-security-audit-2026-07-19 added today alone). Every day this stretches, the fleet accumulates real work that never reaches main.
- **Wallpaper skills:** `github-monitor`, `code-health`, `issue-triage`, `changelog`, `weekly-shiplog`, `repo-revive` — 6 enabled skills short-circuit on an empty `memory/watched-repos.md` every run. Populate or disable. Same recommendation as 2026-07-12 self-review, no movement.
- **Safe fix applied:** copied `memory/topics/skill-freshness-state.json` → `memory/state/skill-freshness.json` and updated all 4 `skills/skill-freshness/SKILL.md` references. The sandbox blocked `rm` on the original, so it remains as an orphan awaiting manual cleanup. No other in-place edits — everything else has real blast radius.

---

## 1. Quality audit

### Articles
Only two articles landed to `articles/` this week: `skill-evals-2026-07-19.md` and `skill-freshness-2026-07-19.md`. Both are the schema-conformant snapshots those skills produce; neither is long-form. All richer output this week landed as `memory/logs/*.md` entries or `.pending-notify/*.md` writes — the reflect/heartbeat/planner triad, `compute-macro-correlate`, `compute-pulse`, `surplus-pulse`, `workflow-security-audit`. Signal is genuinely high; formulaic-vs-substantive isn't the failure mode here.

Standouts:
- **compute-macro-correlate** (07-19) — first-run of the pre-registered Track A partial-correlation test: RENDER ρ=−0.124 (p=0.151), TAO ρ=−0.118 (p=0.174), IO ρ=−0.044 (p=0.612) after partialling on {BTC, SOL}. All null. Wide 30-cell descriptive scan also uniformly null. This is real methodology, not a placeholder.
- **workflow-security-audit** (07-19) — first-ever repo pass; 85 findings (3C/36H/15M/31L), all NEW because no prior audit article existed. 3 Critical `zizmor/unpinned-uses` in aeon.yml (checkout@v5 ×2, setup-node@v5) held Manual per skill rule. Report includes per-finding attack chains.
- **compute-futures-eda** (07-18) — three-consecutive-run strengthening on basket `maxCurve` outlier_pct (07-16 8.33% → 07-17 16.67% → 07-18 33.33%). First (mode, column) pair to persist AND strengthen 3× in the record.
- **planner** (07-16) → **swarm#527 merged 07-18** — planner's stuck-goal escalation named a concrete unblock path; operator PAT delivered on 07-18, closing a 10-day cross-org write block.

### Notifications
Sample from 2026-07-19 — 6 sent, 6 skipped. Every SKIP was justified:
- pr-review, pr-triage, code-health, github-monitor: SKIPPED — empty queue / empty config, no fresh signal
- heartbeat: SKIPPED — all findings DEDUP'D in the last 48h of logs (correct behavior)
- pr-tracker: SKIPPED — hash-dedup guard on unchanged category tuple (validated 6× in-skill, correctly did NOT suppress kage#66, InsForge#1742, or openinterpreter#1810 transitions)

Sent notifications were substantive: config-validator (agi-tracker SKILL.md missing), skillpacks (structural churn with rename of fleet-evolve → outages-fleet), batch-health (swarm-safety-eval missing WARN), surplus-pulse (catalog run), workflow-security-audit (NEW_CRITICAL). Signal:noise looks healthy.

### PR comments
No PR comments were posted by pr-review/pr-triage this week — all runs against `swarm-ai-research/swarm` found an empty queue (the 5 dependabot PRs skipped-by-bot-rule on 07-18 all merged overnight in the 02:02–22:03Z window). This is a correct-behavior result, not a quality gap.

---

## 2. Reliability audit

### Skill runs
- **7-day totals:** 144 workflow runs, 140 succeeded (100% of completions), 4 currently `in_progress`, **0 failures**.
- **Distinct skills fired:** 38 of 44 enabled (86%).
- **Missing 6 enabled:** `janitor` (Sun 05:30 — today), `skill-repair` (reactive — expected non-fire), `ai-framework-watch` (Mon 08:30 — chronic never-dispatch, 9d), `swarm-safety-eval` (Sun 07:30 — missed today), `weekly-shiplog` (Mon 09:00 — last fired 07-06), `run-frequency-guard` (daily 23:00 — chronic never-dispatch, 9d).

### Repeat error / failure patterns
- **`github-actions-cannot-create-prs` (18 branches queued):** every skill that stages a branch (`skillpacks`, `notegraph`, `suggest-edges`, `compute-macro-correlate`, `workflow-security-audit`, `pr-tracker` patch queue) ships work that never becomes a PR. 20-day-plus overdue on the pr-tracker patch alone. Unblock is a single repo Settings checkbox OR a `repo`-scoped PAT. Operator PAT proved live on swarm#527 (07-18) — the smoke test on `notegraph/2026-07-18` is the concrete next step, currently at streak-3 with planner.
- **ISS-006 messages.yml underdelivery:** close-clock **halted at Day-0/1** this cycle after 07-18 planner miss; 07-19 restored cadence, so streak advances to Day-1 tonight. Root cause unchanged: the `*/5 * * * *` matcher against `aeon.yml` slots creates dropout pockets. Fix (explicit per-slot crons) is blocked behind the same PAT/toggle gate.
- **Empty `memory/watched-repos.md`:** 6 enabled skills silently short-circuit every run (`github-monitor`, `code-health`, `issue-triage`, `changelog`, `weekly-shiplog`, `repo-revive`). 7 for 7 days. Same recommendation as prior self-review — no movement. Cost is small per run (fast exit) but wastes workflow slots.
- **`ai-framework-watch` + `run-frequency-guard` never-dispatched:** 9th consecutive day flagged per heartbeat/planner. No cron-state entry ever created. Draft ISS-020 (scope-widened to include `stale-content-pr-sweeper`'s fresh 23:45-pocket 3-day miss streak) is a standing planner priority.
- **`docs/status.md` snapshot-rebase clobber:** 7 consecutive days (07-12 → 07-18). 07-18 upstream ref rotated `a7f04ee → fa89d8c` for the first time in the week with the same clobber outcome — this confirms the failure is the snapshot-merge itself, not stale upstream state. 8 days past the 07-16 urgency threshold.

### Monitor signal
Health-checkers are catching real issues, not always returning OK:
- **batch-health:** issued WARN on 07-19 (`swarm-safety-eval` missing) and 07-18 (heartbeat ATTN). Correctly not filing ISS on WARN (only OUTAGE at 3+ missing).
- **heartbeat:** page verdict is `🔴 DEGRADED` daily, driven by the 38-skill ISS-001 residue on `success_rate<0.5`; heartbeat itself dedups the finding.
- **skill-evals:** BOOTSTRAP run 07-19 correctly flagged 13 NEW_FAIL, correctly filed 0 new issues (all had existing open issues).
- **skill-freshness:** structural mtime blind spot in GHA still unaddressed — freshness scores are optimistically low-noise until fixed per `[[skill-freshness-mtime-blind-in-gha]]`.

---

## 3. Memory hygiene

- **`MEMORY.md`:** 50 lines exactly (at guideline). Content is dense but pointer-only. Current focus items all traceable to 07-18/07-19 events. No stale entries need pruning right now.
- **`memory/notes/`:** 45 atomic notes with frontmatter (id, created, type, links), wikilink-connected. Consistent structure.
- **`memory/topics/`:** 5 topic MOCs (agi-tracker, compute-pulse, fleet-ops, pr-status, surplus-pulse) sized 30–73 lines. Plus **one misfiled JSON:** `memory/topics/skill-freshness-state.json` — this is state data, not a topic MOC. → moved to `memory/state/skill-freshness.json` this run.
- **`memory/issues/`:** 17 open, 2 resolved. INDEX.md consistent with per-issue files.
- **`memory/logs/`:** structure varies mildly (`## Summary` vs `## Summary (skill-name)` vs inline), but each day's log is coherent. No cleanup needed.

Nothing stale to prune. Structure is holding.

---

## 4. Recommendations

Ranked by leverage (impact ÷ cost).

### High leverage / immediate

1. **Repo Settings toggle OR operator PAT** — **meta-blocker**. Under this now sits 18 branches, ISS-006 fix, pr-tracker patch (21d overdue), `docs/status.md` gate, and ~6 fleet fixes. Preferred path is one checkbox (Settings → Actions → General → Workflow permissions → "Allow GitHub Actions to create and approve pull requests"). Fallback is a `repo`-scoped PAT as `AEON_GH_PAT`. The operator PAT is proven live on swarm#527 — planner's streak-3 smoke test on `notegraph/2026-07-18` is the concrete next-run ask.
2. **Populate or disable the 6 watched-repos skills.** Same recommendation as 2026-07-12 self-review, unmoved. Cheapest concrete action: populate `memory/watched-repos.md` with 1–5 `owner/repo` lines and turn 6 dead runs/day into real signal. Or edit `aeon.yml` to `enabled: false` on all 6 (net −6 workflow slots/day).
3. **Draft ISS-020** for `enabled-skills-can-never-dispatch`, scoped to `ai-framework-watch` + `run-frequency-guard` + `stale-content-pr-sweeper` (fresh 23:45-pocket flag). Category `config`, severity `high`. Unblocks the natural-experiment probe class per `[[probes-for-messages-yml-must-dispatch-outside-messages-yml]]`.

### Medium leverage

4. **Stage the `docs/status.md` snapshot-rebase gate.** Two-part fix per `[[status-md-auto-commit-drops-writes]]` + `[[snapshot-rebase-clobbers-docs-status-md]]`: (a) widen heartbeat's `git add` glob to include `docs/`; (b) exclude `docs/status.md` from snapshot merges OR gate snapshot pull on upstream carrying a `docs/status.md` newer than main's HEAD. Root cause now confirmed by 07-18 upstream-ref rotation with same outcome.
5. **Land the pr-tracker SKILL.md patch batch** (5 subitems (a)–(e) per `## Next priorities` item 4). 21d overdue. Blocked by item 1.
6. **Fix `skill-freshness`** to use `git log -1 --format=%ct` over full history instead of `stat --format=%Y` — the structural GHA blind spot per `[[skill-freshness-mtime-blind-in-gha]]`.

### Low leverage / opportunistic

7. **Add missing evals.json entries** for the 35 enabled skills without eval specs (skill-evals 07-19 flagged this). Especially: `batch-health`, `code-health`, `compute-futures-eda`, `compute-macro-correlate`, `compute-pulse`. Would boost eval coverage from 28% → ~85%.
8. **Restore `scripts/validate-config.js`** referenced by config-validator SKILL.md fast path — OR drop the reference. 07-19 config-validator fell back to inline node checks.
9. **Create `skills/agi-tracker/SKILL.md`** — flagged as WARN by config-validator today; the skill is enabled at `13 * * 1` and can't do anything without a SKILL.md file.
10. **Widen `scenario-sweep.mjs`** seed count OR switch outlier detection to a tie-robust statistic per `[[compute-futures-12-seed-sample-too-small]]`. Filter `wallet_sum_pnl` correlations until σ > 1e-6. Resolve seed-encoding artifact per `[[compute-futures-seed-padding-bug]]`.

---

## 5. Safe improvements applied this run

1. **Migrated `memory/topics/skill-freshness-state.json` → `memory/state/skill-freshness.json`** (state, not MOC). Copied the file to the new location (same contents) and updated all 4 references in `skills/skill-freshness/SKILL.md` to the new path. Sandbox blocked `rm` on the source; the original file at `memory/topics/skill-freshness-state.json` remains as an orphan for the operator to delete (or a future non-sandboxed run to clean up).

Everything else on the recommendation list has real blast radius (edits to `aeon.yml`, config-populating files, cross-org PR flows) and is left as an explicit recommendation for the operator.

---

## Notes for next self-review (2026-07-26)

- Watch whether `outages-fleet` skillpack persists a third consecutive run — vocabulary shift real vs edge-case noise.
- If PAT / Settings toggle happens, ISS-006 close-clock resumes and 18-branch queue can batch-close.
- Track: does the 07-18 planner-miss recur? Repeat = ISS-006 pocket-shift, not one-off.
- Compare Track A / Track B compute-macro-correlate to next week's snapshot — this run was the bootstrap; the interesting inference is the delta.
