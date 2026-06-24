## Summary

**Skill**: code-health — **SKIPPED**

The skill's config file `memory/watched-repos.md` does not exist, and no `${var}` repo override was supplied. SKILL.md explicitly allows skipping in this case: *"If the file doesn't exist yet, create it or skip this skill."* I did not invent a watched-repo list on the operator's behalf.

**Files modified**:
- `memory/logs/2026-06-24.md` — appended a Code Health entry recording the skip and how to enable.

**No notification sent** (silent skip — consistent with how other no-state skills like `gitlawb-fleet-metrics` behaved earlier today).

**Follow-up**: To activate this skill, operator should create `memory/watched-repos.md` with `- owner/repo` lines.
