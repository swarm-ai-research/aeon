`ISSUE_TRIAGE_OK no-watched-repos`

## Summary

- **Skill:** issue-triage
- **Verdict:** short-circuit — `memory/watched-repos.md` is missing and `${var}` empty → per SKILL §Config the run logs `ISSUE_TRIAGE_OK no-watched-repos` and exits without probing any repo.
- **Files modified:** `memory/logs/2026-08-19.md` (appended `### issue-triage` section).
- **Notify:** none (SKILL §9 — nothing actionable).
- **Class note:** 13th-day recurrence of `watched-repos-config-missing-silent-short-circuits-6-skills` (sibling skills code-health, github-monitor, changelog, weekly-shiplog, repo-revive share the same no-op).
- **Follow-up:** unchanged from MEMORY.md planner hold — either populate `memory/watched-repos.md` OR set `enabled: false` on the six watched-repos-dependent skills. Neither action taken here (out of this skill's scope).
