*Config Validator — 2026-08-23*

STATUS: ISSUES FOUND

- WARN: enabled skill "agi-tracker" has no SKILL.md at skills/agi-tracker/SKILL.md (known chronic — [[agi-tracker-missing-skill-md-dispatches-no-op]], 7th silent-Mon fire 2026-08-17; next 2026-08-24T13:00Z)

Checkout ordering: PASS. Duplicate skill keys: PASS (153 skills).
Fast-path `scripts/validate-config.js` still missing — ran manual node checks.

These invariants have caused full outages before.
Check aeon.yml and .github/workflows/aeon.yml immediately.

log: memory/logs/2026-08-23.md
