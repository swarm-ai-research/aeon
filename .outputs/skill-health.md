*Skill Health — 2026-06-21*
HEALTH: DEGRADED(38) [systemic: OAuth-outage residue → ISS-001]

🟡 DEGRADED (38) — all share one root cause
- success_rate <0.6 from 2026-06-06→06-20 OAuth outage; counters lag the recovery.
- All 38 now last_status=success, consecutive_failures=0 (~1.5 days clean since 2026-06-20T06:05Z restore).
- Sample (oldest last_success): memory-structural-dedupe, memory-flush, changelog, skill-update-check, planner
- +33 more — see memory/issues/ISS-001

⚪ NO DATA (6): agi-tracker, ai-framework-watch, config-validator, run-frequency-guard, swarm-safety-eval, weekly-shiplog — DISPATCH-SKILL

🟢 HEALTHY: 0

Open issues: 4 (ISS-001/002/005/006) · Resolved this run: 0
