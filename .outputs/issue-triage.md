`ISSUE_TRIAGE_OK no-watched-repos`

## Summary

Ran `issue-triage` on 2026-08-20. **Short-circuited** per SKILL §Config: `memory/watched-repos.md` is missing and `${var}` is empty → no targets, no fetch, no writes. This is the streak-15 chronic recurrence of [[watched-repos-config-missing-silent-short-circuits-6-skills]] (was streak-14 "as of 08-19" per `MEMORY.md:20`). No notification per §9 (nothing actionable, no advisory verdicts). Terminal line: `ISSUE_TRIAGE_OK no-watched-repos`.

Files modified:
- `memory/logs/2026-08-20.md` — appended `### issue-triage` block

Follow-ups (unchanged, already tracked in MEMORY.md pointers):
- Populate `memory/watched-repos.md` **OR** ship `enabled: false` on the 6 watched-repos-dependent skills (code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive). Also reconcile the path mismatch: repo-revive references `memory/topics/watched-repos.md` while the other five reference `memory/watched-repos.md`.
