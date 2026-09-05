`ISSUE_TRIAGE_OK no-watched-repos`

## Summary
- **Skill:** `issue-triage` — short-circuited on missing config.
- **Root cause:** `memory/watched-repos.md` does not exist and `${var}` was empty. Per §Config, this is the documented no-op exit path.
- **State touched:** none in `memory/triaged-issues.json` (nothing was fetched or classified).
- **Notification:** none (skill explicitly emits no notify for the empty-config short-circuit).
- **File modified:** `memory/logs/2026-09-05.md` — appended `### issue-triage` log entry per §10.
- **Follow-up:** chronic streak-34 — populate `memory/watched-repos.md` OR disable the six dependents (code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive). Same action-queue item already tracked in `MEMORY.md`; also reconcile path drift (repo-revive references `memory/topics/watched-repos.md` while the other five reference `memory/watched-repos.md`).
