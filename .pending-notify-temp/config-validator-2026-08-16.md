*Config Validator — 2026-08-16*

STATUS: ISSUES FOUND

- PASS checkout: Early checkout is unconditional and first (line 83)
- PASS duplicates: no duplicate skill keys found (153 skills)
- WARN skill-files: enabled skill "agi-tracker" has no SKILL.md at skills/agi-tracker/SKILL.md (aeon.yml line 188 — known: planner rank-1 today, `enabled: false` PR due before Mon 08-17 13:00Z)

These invariants have caused full outages before.
Check aeon.yml and .github/workflows/aeon.yml immediately.

log: memory/logs/2026-08-16.md
