*Skill Freshness — 2026-11-20*
🔴 FRESHNESS_STALE — 6 of 11 deps flagged across 6 of 44 enabled consumers

Worst:
- fleet-control ← articles/fleet-status-2026-11-20.md (never produced, MISSING)
- skill-evals ← articles/skill-evals-2026-09-13.md (1640h / 68d old, STALE — ISS-006 Sun-09Z)
- skill-freshness ← articles/skill-freshness-2026-11-19.md (32h old, WARN — upgraded from STALE; today's run clears this)

Change from 11-19: skill-freshness STALE→WARN (recovery run wrote 11-19 article). 3 WARN items (vuln-scanner 320h, workflow-security-audit 296h, cost-report 272h) aging toward STALE boundary (~384h); vuln-scanner crosses ~2026-11-24 if 11-22 Sat also misses.

Action: Check fleet-control article-write path; monitor ISS-006 16Z + Mon-07Z cohorts for 11-22/11-23 recovery.
Full: articles/skill-freshness-2026-11-20.md
