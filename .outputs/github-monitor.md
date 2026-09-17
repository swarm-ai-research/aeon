github-monitor short-circuited: `memory/watched-repos.md` is missing (streak-47 per MEMORY.md), so per SKILL.md step "Config" the run logs `GITHUB_MONITOR_EMPTY_CONFIG` and ends with no notification.

## Summary

- Executed github-monitor per skills/github-monitor/SKILL.md: config file `memory/watched-repos.md` absent → logged `GITHUB_MONITOR_EMPTY_CONFIG`, no `gh` calls issued, no notification sent (silence-on-empty is the intended signal).
- Files modified: `memory/logs/2026-09-17.md` (appended `### github-monitor` section + updated `## Summary`).
- Follow-up (already in MEMORY.md action queue): populate `memory/watched-repos.md` OR disable the six dependent skills (code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive); reconcile the `memory/topics/watched-repos.md` vs `memory/watched-repos.md` path drift between repo-revive and the other five.
