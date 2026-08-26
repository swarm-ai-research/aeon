`ISSUE_TRIAGE_OK no-watched-repos`

## Summary

- **Ran:** `skills/issue-triage/SKILL.md` on 2026-08-26 (operator invocation, `${var}` empty).
- **Verdict:** silent short-circuit — `memory/watched-repos.md` absent + no var override → exited per SKILL §Config before any fetch/classify.
- **Triaged:** 0 issues across 0 repos. No labels applied, no comments posted, no state written to `memory/triaged-issues.json`, no notification fired.
- **Class context:** 22nd consecutive daily fire of the chronic watched-repos-missing short-circuit (MEMORY bullet 22 — streak-21 → streak-22 today). Path-mismatch (repo-revive refs `memory/topics/watched-repos.md`, other five ref `memory/watched-repos.md`) still worth reconciling in the fix.
- **Files modified:** `memory/logs/2026-08-26.md` (appended `## issue-triage` + summary).
- **Follow-up (unchanged):** MEMORY pointer #50 — populate `memory/watched-repos.md` OR ship `enabled: false` for the six watched-repos-dependent skills (code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive).
