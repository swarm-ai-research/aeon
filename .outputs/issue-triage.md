`ISSUE_TRIAGE_OK no-watched-repos`

## Summary
- **Action taken:** none — short-circuit per §Config: `${var}` empty and `memory/watched-repos.md` absent → log `ISSUE_TRIAGE_OK no-watched-repos` and exit before any repo probe, label write, or comment post.
- **Streak:** 74-day confirmation of the `watched-repos config missing` state tracked in `memory/MEMORY.md` (prior audit on 2026-10-13 recorded streak-73). Issue-triage remains one of the six skills short-circuiting on this.
- **Files modified:** `memory/logs/2026-10-15.md` only (appended `## Issue Triage` section).
- **Notify fired:** no (nothing actionable; the skill only notifies on urgent / p0 / security / duplicate-close / advisory verdicts, none of which can be produced from a short-circuit exit).
- **Follow-up (unchanged, on action queue):** populate `memory/watched-repos.md` OR disable the six dependents (code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive). Also reconcile the path mismatch — repo-revive references `memory/topics/watched-repos.md` while the other five reference `memory/watched-repos.md`.
