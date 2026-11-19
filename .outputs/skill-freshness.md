*Skill Freshness — 2026-11-19*
❌ FRESHNESS_STALE — 1 of 10 deps flagged across 1 of 44 enabled consumers

Worst:
- fleet-control ← articles/fleet-status-2026-11-19.md (MISSING, class articles/daily, threshold 28h)

Action: Check fleet-control run history with `./scripts/skill-runs --skill fleet-control --hours 168`. No fleet-status article has ever been written to disk — fleet-control may be silently failing its article-write step.
Full: articles/skill-freshness-2026-11-19.md
