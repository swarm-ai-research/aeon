*Skill Freshness — 2026-09-02*
🔴 FRESHNESS_STALE — 1 of 1 deps flagged across 1 of 44 enabled consumers

Worst:
- vuln-scanner ← .outputs/github-trending.md (8h 50m old, class outputs, sev STALE)

Action: Verify vuln-scanner fallback path triggers when github-trending output is stale. Producer github-trending is disabled (enabled: false) — it will never refresh this file.
Full: articles/skill-freshness-2026-09-02.md

