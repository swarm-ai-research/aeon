`ISSUE_TRIAGE_OK no-watched-repos`.

## Summary

Ran `issue-triage` on 2026-08-17. `${var}` empty and `memory/watched-repos.md` missing → per the skill's short-circuit rule, logged `ISSUE_TRIAGE_OK no-watched-repos` and exited without work. No repos triaged, no labels/comments applied, no notification. Extends the [[watched-repos-config-missing-silent-short-circuits-6-skills]] chronic streak (12th+ consecutive silent short-circuit for this skill). Files modified: `memory/logs/2026-08-17.md`. Follow-up: MEMORY's rank-4 hold — populate `memory/watched-repos.md` OR ship `enabled: false` on the six watched-repos-dependent skills (code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive) to stop the daily silent-dispatch cycle.
