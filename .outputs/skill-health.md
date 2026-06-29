*Skill Health — 2026-06-29*
HEALTH: DEGRADED(38)  [systemic: ISS-001 OAuth-outage residue — 38 skills, denominator catch-up]

🟡 DEGRADED (38) — same set as 2026-06-28, no new failures since 2026-06-20T01:5xZ (9 days clean)
- All 38 sit at last_status=success / consecutive_failures=0; low cumulative success_rate is catch-up math, not live failure — WAIT-RECOVERY
- Runtime fleet 168h (./scripts/skill-runs): 105/109 success, 0 failures, 4 in-progress — runtime healthy

⚪ NO DATA (2): ai-framework-watch, run-frequency-guard — DISPATCH-SKILL
🟢 HEALTHY: 4 (+1 vs prev — agi-tracker recovered, Mon 13:00 slot fired today after 19-day gap)

Δ vs 2026-06-28: agi-tracker NO_DATA→HEALTHY; classification set otherwise identical.
Distinct pattern (not classified by skill-health): ISS-006 multi-pocket dispatch silence day 8 — this skill's 18:00 slot itself slid ~82m late (fired 19:22Z).

Open issues: 4 (ISS-001, ISS-002, ISS-005, ISS-006) · Resolved this run: 0
Reconciliation: 0 CRITICAL/FLAPPING → 0 filed. HEALTHY config-validator + swarm-safety-eval in ISS-005/006 affected_skills NOT auto-removed (root causes orthogonal to success_rate signal; deferred to skill-evals/skill-repair per CLAUDE.md health/repair contract).
