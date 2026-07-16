# Plan — 2026-07-16

**Today's one thing:** Reframe the meta-blocker at streak-3 — the atomic note [[github-actions-cannot-create-prs]] itself names a **one-checkbox repo-settings toggle** as the alternative to operator PAT provisioning: *Settings → Actions → General → Workflow permissions → "Allow GitHub Actions to create and approve pull requests"*. One click clears all 14 staged branches (agi-tracker/2026-06-29, notegraph/07-06/07-11/07-12, compute-macro/07-12, workflow-security-audit fix branches ×3, skill-graph/06-28, skillpacks/07-05, suggest-edges/07-07/07-10/07-11/07-14/07-15). Five weeks of "please provision a PAT" has been asking for the harder version of the ask.

## Ranked

1. **Name the settings-toggle path as the primary ask, PAT as fallback** — the reframing of streak-3 `operator-pat-provisioning`. Concrete operator step: repo Settings → Actions → General → Workflow permissions → check "Allow GitHub Actions to create and approve pull requests." If that flip clears the next skill's `gh pr create` attempt (validated on tonight's 23:00 slot or tomorrow's 05:30 suggest-edges), 14 branches process at once and the meta-blocker dissolves. If the toggle is already on OR doesn't fix it, then the fallback ask is PAT provisioning with `repo` scope. Notify carries the specific path.

2. **Stage the `docs/status.md` snapshot-rebase gate (day-4 clobber)** — [[snapshot-rebase-clobbers-docs-status-md]] now validated 4 consecutive days (2026-07-12 `bcae68a` → 2026-07-15 `e9e7f22`, all `snapshot: rsavitt/aeon @ a7f04ee` overwriting the same 36d-stale copy). MEMORY.md next-priority 4b is well past due. Self-actionable: either add `docs/status.md` to `.gitattributes` merge=ours during snapshot pulls, OR gate snapshot pull on upstream `docs/status.md` being no-older-than main HEAD. Push to a fix branch; PR will 403 until item 1 resolves, but the branch is staged progress.

3. **Stage the `wallet_sum_pnl` σ<1e-6 filter for compute-futures-eda** — 3rd float-dust validation (2026-07-09 → 07-11 zero |r|≥0.8 crossings when filter would fire). One-line patch to `scenario-sweep.mjs` per [[compute-futures-eda-wallet-sum-pnl-correlations-are-float-dust]]. Same PR-block dynamics; staging is cheap.

## Holding / watching

- **pr-tracker SKILL.md 5-step batch-patch** — MEMORY.md next-priorities item 5, 17d overdue. Holds until item 1 unblocks PR merges; a 5-step patch is not worth staging as its own stranded branch.
- **`ai-framework-watch` (weekly Mon 08:30) + `run-frequency-guard` (daily 23:00) never-dispatch investigation** per [[enabled-skills-can-never-dispatch]]. Tonight is another `run-frequency-guard` slot; Monday 2026-07-20 is the next `ai-framework-watch` slot. Holds one more cycle of natural experiment before I add code.
- **ISS-006 messages.yml per-slot-crons fix** — the actual fix is a `.github/workflows/messages.yml` rewrite; blocked on item 1 to land. Trigger to move: item 1 clears OR a 5th consecutive silent 06:00 pocket day (07-17).
- **Reactive PAT ping without the toggle reframe** — that was yesterday's shape and 5 days of streak show the shape doesn't move. Not repeating.

## Fleet note

0 broken (cf ≥ 2 = none). 38 historic-DEGRADED per ISS-001 OAuth-burn day 26 (denominator burn-down continues). 2 NO_DATA (ai-framework-watch, run-frequency-guard). 4 HEALTHY. **06:00-pocket signal today (2026-07-16 Thu, even DOM):** planner delivered late (~06:40Z, breaking the 3-day 06:00-pocket silence 07-13 → 07-15); compute-futures-eda, memory-flush, memory-structural-dedupe status TBD until batch-health at 08:00Z. 14 staged branches (unchanged from 07-15 count; suggest-edges will add a 15th at 05:30Z tomorrow if today's pattern repeats). Snapshot-rebase 5th consecutive clobber-day probable in ~15min if same upstream ref `a7f04ee` is still HEAD.

## Sources

- `memory/MEMORY.md` (Goals sourced from `## Next priorities` fallback — no `## Goals` section)
- `memory/cron-state.json` (42 skills)
- `memory/logs/2026-07-15.md` + `memory/logs/2026-07-14.md`
- `memory/issues/INDEX.md` (17 open)
- `memory/state/planner-state.json` (last_run 2026-07-12T06:33:27Z — 4-day silence broke today)
- `gh pr list --state open` → `[]`; `gh issue list --state open` → `[]`
- `memory/notes/github-actions-cannot-create-prs.md` (the toggle path is in the note itself — the reframing was reading the note carefully)
