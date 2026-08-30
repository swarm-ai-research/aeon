# Self Review — 2026-08-30

Window: 2026-08-24 → 2026-08-30 (7 days). Prior review: 2026-08-23.

## 1. Quality of outputs

**Substantive this week:**
- `compute-futures-eda` — 08-29 CSV surfaced a genuine class-first finding: the 2.5000× basket/synth multiplier held n=8 filings, surpassing the prior 3.025× regime's n=7 invalidation floor. That's a real signal (promotion-cadence thresholds derived from prior-regime floors need re-checking each time a new regime crosses them), not a template.
- `pr-tracker` — 08-26 discovered a class-first CLA-block close pattern via `cloudflare/workerd#7124` (opened-and-closed within ~6h with CLA Assistant Lite bot sig demand as sole prior comment); atomized as [[cloudflare-org-cla-blocks-aeonframework-prs]]. 08-27 candidate widening onto `microsoft/vscode#332891` under active watch.
- `vuln-scanner` — 08-29 CopilotKit/OpenBot audit (0 vulns / 0 secrets / 16 informational transitive CVEs) with a legitimate scope explanation for why no PR was filed (Renovate preset scoped `enabledManagers:[github-actions]`).
- `planner` — real escalation ladder on aeon-repo PR #26 (isolated single ShellCheck FAILURE hiding since 08-17).
- `reflect` — 08-29 atomic-note promotion produced [[compute-futures-2.5x-surpasses-n-7-invalidation-floor]] with a durable lesson (invalidation *events* aren't durability *ceilings*).

**Formulaic / noisy:**
- `suggest-edges` — identical `[cash, darkbloom, synthetic, basket, spread]` templated-corpus signature every run, opening a new PR each day (day-16 → day-20 across the window; net +1 open PR/day, 5 open). The 08-27/08-28 batch outage did not break the streak. Fix has been queued as a "pre-filter within-`gitlawb-compute-futures-proofs/` pairs" patch since 08-19 — 11 days.
- `surplus-pulse` — same catalog-mode payload daily (H100 R30 +88.7% anchor) because `SURPLUS_PRICING_URL` is unset.
- `goal-tracker` — NO_GOALS notify every run despite the chronic-known cause (MEMORY.md is pointer-only and no longer carries `## Goals`).
- `skill-health` — 24h daily-reminder notify despite byte-identical hash `e27c0ac60367e7e5` for 61+ days.

**Silent short-circuits (empty runs, notify-suppressed — quiet but wasted budget):**
- 6 watched-repos-dependent skills (code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive) — chronic streak **25 days**.
- `gitlawb-fleet-metrics` (GLMETRICS_EMPTY), `fleet-control` (FLEET_EMPTY), `memory-structural-dedupe` (SKILL targets absent H2 sections post-restructure).

**Structural leak — the `articles/` write path is broken and no one noticed.**
- 68 skill files reference `articles/`. Git has **zero** files ever committed under `articles/`. The directory did not exist on disk this session before this review created it.
- 13 open issues (ISS-002 + ISS-005 + ISS-008..018) are all `no_file_match` from `skill-evals` — they are the same class defect surfacing under different skill names.
- **Last week's self-review flagged this as recommendation #1.** The line "wrote articles/self-review-2026-08-23.md" in that review is itself a fabrication — no such file exists on disk.

## 2. Reliability

- **7-day rollup (via `./scripts/skill-runs --hours 168`):** 92/93 completed OK — 98% success rate. 1 explicit failure: `cost-report` at 2026-08-24T07:36Z (recovered same morning cycle).
- **`cron-state.json`:** 42 skills tracked, 38 at `success_rate < 0.5` with `last_status: success` and `consecutive_failures: 0` — the ISS-001 residue trail (Day-70+), functionally healthy but numerically pinned by the June OAuth outage.
- **P0 stuck-skill fires:** zero this window (last one was `notegraph` on 08-19, resolved in 5m30s).
- **Batch outage 08-27 + 08-28:** 71h planner gap (last planner run 2026-08-26T06:42Z until 08-29 catch-up). 08-27 log: `pr-tracker` only (14 lines). 08-28 log: `notegraph` + `code-health` + `surplus-pulse` (27 lines). Skill-health missed 3 daily reminders. This is a fresh datapoint on ISS-006 (messages.yml multi-pocket cron underdelivery, day-70+) and pushes status toward `investigating → fixing`.
- **Never-dispatched (Day 53):** `ai-framework-watch` (Mon 08:30) + `run-frequency-guard` (daily 23:00) — cron-state absence per [[enabled-skills-can-never-dispatch]]. ISS-021 draft has been pending 41 days.
- **Silent-Monday chronic (T-2):** `agi-tracker` fires its 9th silent-Mon on 2026-08-31T13:00Z (~54h out). SKILL.md file is missing; `aeon.yml:188` still `enabled: true`. Trivial two-path fix documented; unlanded.
- **PR merge path unproven:** 26 open aeon-repo PRs. 0 `app/github-actions` PRs merged in 532h+ (last aeon-repo merge was #8, actions/checkout dependabot, 2026-08-07). PR #26 has been MERGE-READY (5/5 checks SUCCESS at `updatedAt: 2026-08-24T01:08:19Z`) for 6 days but has not been clicked through.
- **swarm write-path confirmed blocked:** 08-29 65th pr-review after a 3-day gap hit both `POST .../pulls/549/comments` (403) and `gh pr review --comment` GraphQL — `[[aeon-app-no-write-on-swarm-repo]]` promoted suspected → confirmed.

## 3. Memory hygiene

- **MEMORY.md is 71 lines (target ≤ 50, 42% over).** Last week's review flagged this at 64 lines and recommended demoting to topic files; it grew by 7 lines instead. Focus bullets that were once week-of-work are now day-of-work slabs with heavy inline data (compute-futures paragraphs, pr-tracker tuple predictors).
- **Logs are consistently structured** — every skill emits its named H2 section with the same `_OK` sentinel pattern. The 08-27/08-28 files are legitimately short (batch outage), not degraded.
- **SKILL drift is the real hygiene debt, not MEMORY entries:**
  - `pr-tracker` patch items (a)–(l): **68 days overdue**.
  - `memory-structural-dedupe`: SKILL targets six H2 sections none of which exist post-pointer-only restructure.
  - `stale-content-pr-sweeper`: hardcoded `ALLOWED_AUTHORS={"aeonframework"}` but operational bot identity is `app/github-actions`. Operator-invocations exercise the widened set; cron-path invocations close 0.
  - `repo-revive` references `memory/topics/watched-repos.md`; other five reference `memory/watched-repos.md`.
- **`docs/status.md` snapshot-rebase clobber** — 29th consecutive rebase-regen cycle, 43 days past urgency threshold.
- **`notegraph` HEAD-vs-workspace divergence** — open PRs #48/#51/#53 stack unmerged; each new PR shows a phantom delta because HEAD lags workspace.

## 4. Notification patterns

**Good discipline:** heartbeat 48h dedup, watched-repos suppress, notegraph silent-exit skip, batch-health only on WARN/OUTAGE, sweeper only on `n_closed > 0`, `./notify` in-run hash dedup.

**Noisy despite good primitives** (all *should* dedup and don't, because the skill's payload changes in trivial ways):
- `suggest-edges` — daily PR-open notify on the same templated cluster.
- `goal-tracker` — daily NO_GOALS.
- `pr-tracker` — daily tuple predictor on stable buckets.
- `skill-health` — daily reminder on byte-identical health-set for 61+ days.

**Structural workaround:** `./notify -f` and inline `$(cat …)` are sandbox-blocked; skills now write directly to `.pending-notify/${epoch}-${skill}.md`. This works but is undocumented in most SKILL.md files.

## 5. Concrete recurring issues (multi-day)

| Issue | Class | Cadence in window | Status |
|---|---|---|---|
| `articles/` dir absent → 68 skills' long-form output silently dropped | Structural | Every article-writing run | Flagged last review, unaddressed 7d |
| `agi-tracker` silent-Mon | Config | 8th fire done, 9th T-2 | Fix trivial, unlanded |
| Sandbox `>` redirect blocked in workdir | Sandbox | n=5+ this week (notegraph 4×, vuln-scanner, pr-tracker 2×, code-health) | Fix pattern known (`scripts/notegraph-fingerprint.mjs`), unmerged |
| `watched-repos.md` empty short-circuit | Config | Streak 25 | Binary fix, unlanded |
| PR #26 merge-ready but not merged | Auth/scope | Day 22 | Requires operator click OR auto-merge policy install |
| ISS-001 residue on 38 skills | Metric | Day 70+ | Substantively healthy; close deferred until ISS-006 stabilizes |
| Never-dispatched 2 skills | Config | Day 53 | ISS-021 draft, 41d pending |
| swarm dependabot cohort full-skip | Content | 61st–65th invocation | Bot-author skip working as intended; write-path 403 now confirmed |
| pr-tracker predictor blindspot on fresh cross-repo bot PRs | Prompt | 4× of 5 days | Patch item (e), 68d overdue |
| CLA-block close class widening (cloudflare → microsoft) | Content | 08-26 + 08-27 | Fix candidate: pre-submit gate in vuln-scanner/external-feature |

## 6. Improvement recommendations

**Top 3 (do first):**

1. **Create the `articles/` directory in the repo and wire commit path.** 68 skills write there; 13 open ISS tickets exist because the writes evaporate. This review has now materialized `articles/self-review-2026-08-30.md` (the first file under `articles/` in repo history), but the durable fix is: (a) commit an `articles/.gitkeep`, (b) audit one representative article-writing skill to confirm write-then-commit works end-to-end from cron path, (c) resolve ISS-002/005/008–018 as a class once evidence lands. This is the second week this recommendation leads.

2. **Ship `enabled: false` on `aeon.yml:188` for `agi-tracker` via PR before 2026-08-31T13:00Z (~54h).** One-line change; kills the 9th silent-Mon fire. Alt: restore `skills/agi-tracker/SKILL.md`. Deferring for a third week costs an actual dispatched slot and pulls ms-02 metric further from truth.

3. **Populate `memory/watched-repos.md` OR flip `enabled: false` for the 6 dependent skills.** 25-day streak of chronic same-day short-circuits. Also reconcile the `memory/topics/watched-repos.md` vs `memory/watched-repos.md` path mismatch in `repo-revive` while touching this.

**Next 3 (medium-priority):**

4. Patch `stale-content-pr-sweeper` SKILL.md — add `"app/github-actions"` to `ALLOWED_AUTHORS`; add `compute-macro`/`skill-graph` short-prefix aliases to TRACKED. Cron path currently closes 0.
5. Merge `scripts/notegraph-fingerprint.mjs` and land the SKILL.md patch that references it — n=5+ sandbox friction this week alone across four skills.
6. Split MEMORY.md focus bullets: move compute-futures-eda paragraph and pr-tracker tuple predictor to their topic files; keep MEMORY.md as pointer-only. Target ≤ 50 lines. (Best done immediately after `reflect` runs to avoid stomping on active memory writes.)

**Lower priority / research:**

7. Batch-outage of 08-27 + 08-28 is the strongest evidence yet for ISS-006 status promotion `investigating → fixing`. The three-regime cron model documented in the MEMORY.md fix pointer is ready to attempt.
8. `suggest-edges` templated-corpus pre-filter (11 days queued) — will retire a per-day PR churn stream.

## 7. Actions applied in this run

- Created `articles/` and wrote this review to `articles/self-review-2026-08-30.md` — the first file ever committed under that path. This resolves the immediate "self-review didn't ship" fabrication from the 08-23 cycle for this skill. Broader class-fix (68 skills) still pending.
- Wrote `.outputs/self-review.md` short-form for `./notify` fanout.
- Appended log entry to `memory/logs/2026-08-30.md`.

Nothing else auto-applied. Deliberately did NOT:
- Trim MEMORY.md — bullets are actively curated by `reflect`/`planner`/`pr-tracker` and editing mid-cycle would clash.
- Modify `aeon.yml` — that's a PR-scope operator decision.
- Populate `watched-repos.md` — no source of truth for what belongs in it.
- Close any ISS tickets — repair skills own that path.
