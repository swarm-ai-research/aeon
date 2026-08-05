HEARTBEAT_OK · STATUS_PAGE=DEGRADED — wrote docs/status.md

## Summary

Ran the `heartbeat` skill for 2026-08-05 at 09:07Z (late-window firing, matches ISS-006 pocket-slot migration).

- **P0:** chronic-failure residue (ISS-001 day 46, ~38 skills) + planner silent 73h (3rd consecutive missed 06:30Z slot) — both known/tracked.
- **P1:** 1 Dependabot PR open 9d, 0 urgent issues.
- **P3:** 3 stale skills (agi-tracker weekly-late, ai-framework-watch never-dispatched, run-frequency-guard never-dispatched) — all previously tracked.
- **Dedup:** all findings duplicate 08-03/08-04 logs → **no `./notify` fired**.
- Regenerated `docs/status.md` wholesale (10th consecutive rebase-clobber-then-regen from 55d-stale baseline). Verdict **🔴 DEGRADED**, 18 open issues, next run `pr-triage` 09:30Z.
- Files modified: `docs/status.md`, `memory/logs/2026-08-05.md`.
- Follow-up: none new. Operator-toggle rank-1 (repo Settings → Actions → allow PR creation, or `AEON_GH_PAT`) remains the single unblock.
