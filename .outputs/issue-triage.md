`ISSUE_TRIAGE_OK no-watched-repos`

## Summary
- Ran `skills/issue-triage/SKILL.md`. Per §config, `${var}` is empty and `memory/watched-repos.md` is absent → short-circuited before any `gh` call.
- Verdict: `ISSUE_TRIAGE_OK no-watched-repos`. No repo probes, no classifications, no writes to `memory/triaged-issues.json`.
- Notify suppressed per §9 (nothing actionable). Log entry appended to `memory/logs/2026-08-13.md`.
- Follow-up (unchanged from planner rank holding item, streak-8): populate `memory/watched-repos.md` or disable the 6 watched-repos-dependent skills.
