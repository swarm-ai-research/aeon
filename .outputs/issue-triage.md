Issue-triage short-circuited: no `${var}` provided and `memory/watched-repos.md` is absent (streak-75 of the chronic empty-config state). No repos probed, no issues classified, no notify. Logged `ISSUE_TRIAGE_OK no-watched-repos` to `memory/logs/2026-10-16.md`.

## Summary
- **Target repos resolved:** 0 (var empty + config file missing → short-circuit per SKILL.md §Config).
- **Issues triaged:** 0.
- **Exit code:** `ISSUE_TRIAGE_OK no-watched-repos`.
- **Notify fired:** no (nothing actionable).
- **Files modified:** `memory/logs/2026-10-16.md` (appended Issue Triage section).
- **Follow-ups (unchanged, already on MEMORY.md action queue):** populate `memory/watched-repos.md` with `- owner/repo` lines OR land `enabled: false` on the 6 dependent skills.
