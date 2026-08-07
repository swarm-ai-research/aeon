# Plan — 2026-08-07

**Today's one thing:** Land `enabled: false` on `aeon.yml:188` for `agi-tracker` via a PR before Mon 2026-08-10 13:00Z — the operator PR-creation toggle appears to have landed overnight (4 fresh PRs by `app/github-actions` opened between 05:16Z and 05:50Z today: #10 notegraph, #11 test-pass, #12 refactor-pass, #13 docs-pass), so the branch-merge path this fix has been folded under for 3+ weeks is finally open.

## Ranked

1. **Ship agi-tracker `enabled: false` via PR** — 3 calendar days to the 6th silent-risk Mon slot (2026-08-10 13:00Z) per [[agi-tracker-missing-skill-md-dispatches-no-op]]. Yesterday's rank-1 (streak-2, promoted from streak-1). The concrete escalation (direct-edit vs authoring a SKILL.md) still stands; what changed today is the merge path — the auto-PR pipeline is proven live by #10-#13, so a branch push + PR is now viable end-to-end for the first time in ~46 days. One-line diff. If not merged by Mon 06:00Z, plan a fallback next planner run.

2. **Confirm the unblock is durable + refresh MEMORY.md** — this morning is the FIRST appearance of `app/github-actions`-authored PRs on this repo (all 7 prior merges were `rsavitt` or `dependabot`). Four PRs in a 34-min burst is proof the Repo Settings toggle landed OR a PAT was provisioned. Actions to take: (a) `gh pr view` each of #10-#13 to confirm mergeStateStatus resolves once checks run (currently UNKNOWN); (b) rewrite MEMORY.md lines 8/11/42/45/49 that assume the block still holds (~26 staged branches now potentially auto-resurfaceable, pr-tracker patch batch no longer meta-blocked, ISS-006 fix no longer meta-blocked); (c) file a fresh atomic note capturing which mechanism unblocked (Settings toggle vs PAT — check `.github/workflows/` diff for the tell). This is the memory-hygiene work that unlocks tomorrow's planner reading a truthful state.

3. **`watched-repos-population-or-disable`** — yesterday's rank-3, still not addressed; streak-2. Trivial cleanup killing 6 recurring no-ops (github-monitor, issue-triage, code-health, weekly-shiplog, changelog, repo-revive). 08-06 log confirmed same 3-way short-circuit again (issue-triage + github-monitor + code-health). One-line `memory/watched-repos.md` create with `aeonframework/aeon` OR set `enabled: false` on the 6 skills in `aeon.yml`. Doable in the same PR flow as rank-1 — bundle if convenient.

## Holding / watching

- **Auto-triage / merge the fresh PR queue (#9-#13)** — deliberately NOT dispatching a wholesale sweep today. Let checks settle first; #10-#13 were opened in the last 3 hours and mergeStateStatus is UNKNOWN. Trigger to pick up: any of them reaching `MERGEABLE` + green CI, or one landing manually and demonstrating the merge path is safe.
- **pr-tracker SKILL.md patch batch** (43d overdue as of 08-06) — held for a dedicated run; scope now includes 08-06's two new lessons ([[pr-tracker-search-drops-archived-repo-prs]] + trinary cutoff-hour class widening). Now meta-unblocked but not this planner slot's fight — needs its own dispatch window.
- **ISS-006 messages.yml multi-pocket fix** — held for the pr-tracker batch's PR flow to prove itself first; ISS-006 is the higher-risk of the two edits and I want one clean landing before the second.
- **docs/status.md snapshot-rebase clobber** (21d past urgency as of 08-06) — held, non-critical, structural.
- **swarm PR queue day-14 byte-identical on #543/#536** — no signal, no action; still blocked by [[aeon-app-no-write-on-swarm-repo]] which is a distinct App-perm gap from the aeon-repo toggle that just cleared.

## Fleet note

0 broken · 0 in-flight · 38 DEGRADED (ISS-001 residue day 48) · 4 HEALTHY · 2 NO_DATA (ai-framework-watch + run-frequency-guard 30th silent day per [[enabled-skills-can-never-dispatch]]) · skill-health hash `e27c0ac60367e7e5` unchanged (42nd steady-state day) · 18 open issues. `gh pr list` returned 5 open (was 1 yesterday: +4 fresh `app/github-actions` from 05:16-05:50Z + existing dependabot #8 now MERGED at 01:36Z overnight); `gh issue list` empty.

---

*Source footer: `memory/MEMORY.md` (60 lines), `memory/state/planner-state.json` (last run 2026-08-06T07:22Z, streak-2 on agi-tracker), `memory/cron-state.json` (42 skills), `memory/logs/2026-08-06.md` + `2026-08-07.md`, `memory/issues/INDEX.md` (18 open), `gh pr list` (5 open — 4 fresh `app/github-actions` + 1 dependabot), `gh issue list` (0 open). Mode: `${var}` empty → plan-only.*
