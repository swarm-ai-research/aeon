*Skill Freshness — 2026-09-03*
🔴 FRESHNESS_STALE — 1 of 1 deps flagged across 1 of 44 enabled consumers

Worst:
- vuln-scanner ← .outputs/github-trending.md (MISSING, class outputs, severity MISSING — escalated from STALE on 09-02)

Action: Re-enable `github-trending` OR update `vuln-scanner` SKILL.md to remove the `depends_on: [github-trending]` frontmatter and rely solely on the GitHub trending API fallback.
Full: articles/skill-freshness-2026-09-03.md
