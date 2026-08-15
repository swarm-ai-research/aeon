*Skill Freshness — 2026-08-15*
🔴 FRESHNESS_STALE — 2 of 8 deps flagged across 2 of 44 enabled consumers

Worst:
- weekly-shiplog ← articles/push-recap-*.md (MISSING, daily producer disabled)
- heartbeat ← articles/token-report-*.md (MISSING, daily producer disabled)

Action: Both producers (push-recap, token-report) are enabled: false with daily schedules. Enable them or remove the downstream dependency references from consumer SKILL.md files.
Full: articles/skill-freshness-2026-08-15.md
