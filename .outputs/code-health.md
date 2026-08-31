`CODE_HEALTH_SHORT_CIRCUIT`.

## Summary

Ran `code-health` — silent short-circuit. `memory/watched-repos.md` is absent (also `memory/topics/watched-repos.md`, the repo-revive path alt), so per SKILL §Config the skill exited before step 1: no clones, no scans, no article, no notify. This is the 27th consecutive daily fire of the chronic watched-repos short-circuit cluster (matching today's github-monitor / issue-triage / weekly-shiplog counts).

- **Files modified:** `memory/logs/2026-08-31.md` (added `## code-health` entry).
- **No PRs, no notifications, no article** (notify skipped — hash-dedup would suppress a same-shape payload and there's no operator-actionable delta beyond the standing planner item `watched-repos populate-or-disable`).
- **Follow-up (unchanged, binary):** populate `memory/watched-repos.md` with `- owner/repo` lines OR ship `enabled: false` on the 6 dependent skills (code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive); reconcile the `memory/topics/watched-repos.md` (repo-revive) vs `memory/watched-repos.md` (other five) path mismatch in the same patch.
