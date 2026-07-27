---
id: memory-section-header-rename-breaks-goal-tracker
created: 2026-07-27
type: lesson
links: [[planner-escalation-of-escalation-when-meta-blocker-holds]], [[aeon-skills-dispatch-via-messages-yml]]
---
# Renaming a MEMORY.md section header silently breaks any skill whose fallback list doesn't include the new name

2026-07-26 reflect renamed `## Next priorities` → `## Pointers` (content preserved, structure only); goal-tracker's next run at 09:20Z exited `NO_GOALS` because its SKILL.md fallback header list (`## Goals`, `## Next Priorities`) did not include `## Pointers`, so the 19 goal bullets still on lines 41–59 became invisible. Section names in MEMORY.md are load-bearing contracts read by consuming skills — a reflect rewrite that changes header text must either grep the skills tree for that string first, or add the old name as an alias in the same edit.
