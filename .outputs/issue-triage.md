Task tracking not warranted for a single-step pre-flight exit.

## Summary

Ran `issue-triage` per `skills/issue-triage/SKILL.md`. `${var}` was empty and `memory/watched-repos.md` is absent, so the skill exits cleanly at the pre-flight gate (SKILL.md line 34) with `ISSUE_TRIAGE_OK no-watched-repos`.

- No `gh` calls issued, no probes, no writes.
- `memory/triaged-issues.json` preserved untouched.
- No notify (nothing actionable).
- Log entry appended to `memory/logs/2026-08-11.md`.

The chronic `watched-repos populate` hold (planner streak-6 today) is the upstream cause — issue-triage is one of the skills silently no-op'd by that missing config.
