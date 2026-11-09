# Plan — 2026-11-09

**Today's one thing:** Draft the PR that pulls the 08Z-cohort out of the dead 06Z pocket — start with `compute-futures-eda` (06:00 → 10:15), `memory-flush` (06:00 → 10:25), `memory-structural-dedupe` (06:10 → 10:35), and `planner` itself (06:30 → 10:45). Smallest ISS-006 slice that unblocks the loudest casualties.

## Ranked

1. **Open PR against `aeon.yml` migrating the four 08Z-cohort skills to post-10Z slots** — ISS-006 top-priority streak hits 40 today; the 10-29 → 11-05 "settles at new slot" story explicitly broke at n=3 (11-05 silent-no-manual regressed past the +110m attractor). Status quo: `compute-futures-eda` silent 11 days, `planner` 14 days (I am the lone morning-pocket survivor today), `memory-flush`/`memory-structural-dedupe` 14 days, `compute-macro-correlate` 43 days. Serve the "escalate stuck goals with a concrete unblock action" rule from step 2 — the 39-day restatement run has produced no motion, so the move today is not another atomic, it is the diff. Per-slot cron rewrite for every pocket is the long-horizon fix per the 22-tributary chain; pulling four skills out of the loudest pocket is the T-shirt-sized first step.
2. **Decide the watched-repos centenary — draft a one-line `enabled: false` PR for the six dependents** — streak-100 landed yesterday on the Sunday 11-08 code-health witness; that is the operator-decision moment the series has been waiting for. Draft the disable PR today (code-health + issue-triage + github-monitor + changelog + weekly-shiplog + repo-revive) with a revert note for when `memory/watched-repos.md` gets populated; stop the daily short-circuit silently burning cadence. Reconcile the `topics/watched-repos.md` vs `watched-repos.md` path mismatch in the same patch.
3. **File ISS-044 locally (identity blackout 09-14 → 09-17)** — pure local Write, no PR, no permission dependency, no bundle coordination. Prior planner carried streak 5 on this item at 10-26; renumbers cleanly now that batch-health has filed through ISS-043. Today's run is the first opportunity since the 10-26 → 11-08 planner silence window to actually land it. Clears the top of the action queue and reduces draft-work-in-flight count by 1.

## Holding / watching

- **ISS-006 `messages.yml` multi-pocket rewrite (streak 39 → still-stuck, paused as top-priority after rank-1 incremental slice above)** — the full rewrite is the correct long-horizon fix but needs the simpler 08Z move to prove the pattern first. Re-promote to rank-1 when the rank-1 PR merges and the next cadence day lands clean fires in the new 10Z slots.
- **`stale-content-pr-sweeper` `ALLOWED_AUTHORS` patch** — defect re-engaged 11-07 (would close #107, actually closed 0). Operator-blocked on the patch PR, not planner-actionable today.
- **`pr-tracker` items (a)–(u) batch — 83d overdue** — permission-gated (needs `pull_requests: write` on swarm), bundle-coordinated across 21 items. Carry forward.
- **PR #26 ShellCheck regression** — upstream dependabot force-rebase stuck; no new signal since 09-14 regression. Hold.
- **`agi-tracker` `enabled: false` OR restore SKILL.md** — 14 silent-Mon fires accumulated; operator decision.
- **`aeon` swarm-repo app-perm gap** — install `pull_requests: write` + `issues: write` on the aeon app for `aeonframework/swarm`, OR document swarm as report-only. Day-49+ 403.
- **Dispatch not firing** — `${var}` empty, mode is plan-only; the three ranked items are deliverables for the human operator (PRs 1 & 2) and a local write (3) that doesn't need dispatch.

## Fleet note

- **0 skills at `consecutive_failures >= 2`** — all casualties are silent-at-nominal (the ISS-006 mode), not hard-fail; `skill-repair` cannot react to silence by design. The 58+ consecutive-day zero-live-failures streak holds purely because the dead-slot skills never reach dispatch.
- **38 skills at `success_rate < 0.5` with `cf=0`** — ISS-001 residue, Day-123+, byte-identical skill-health hash streak. Close deferred until ISS-006 stabilizes per standing decision.
- **Morning-pocket casualty roster today (2026-11-09 Sunday 06Z batch):** 1/4 fired (planner, this run). Expected set was `{compute-futures-eda, planner, compute-macro-correlate, skillpacks}` (memory-flush/dedupe skip on odd DOM). The 3 silent peers will likely prompt an OUTAGE-tier `batch-health` fire + an ISS-044 renumber at the Monday-10-cadence.

## Sources

- `memory/MEMORY.md` (goals + action queue) · `memory/cron-state.json` (all 39 skills) · `memory/logs/2026-11-07.md` + `memory/logs/2026-11-08.md` · `memory/issues/INDEX.md` (ISS-001/006 open, 39-row open table) · `memory/state/planner-state.json` (prior top: `iss-039-identity-blackout-filing` streak 5 from 10-26). PR list via `gh pr list` OK; `gh issue list` returned empty — repo has no open issues, only PRs.
