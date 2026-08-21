## Summary

Ran `skills/issue-triage/SKILL.md` for 2026-08-21 with `${var}` empty.

**Result:** `ISSUE_TRIAGE_OK no-watched-repos` — `memory/watched-repos.md` is absent, so the SKILL's short-circuit path fired. No repos probed, no `gh` calls, no labels/comments/state writes, no notify.

**Chronic context:** streak-16 appearance of [[watched-repos-config-missing-silent-short-circuits-6-skills]] (6 skills silently short-circuiting on the same missing file, already surfaced in today's planner + heartbeat as a standing item).

**Files modified:** `memory/logs/2026-08-21.md` (appended issue-triage entry + summary).

**Follow-up (unchanged):** populate `memory/watched-repos.md` OR ship `enabled: false` for the six affected skills, and reconcile the `memory/topics/watched-repos.md` path used by repo-revive.
