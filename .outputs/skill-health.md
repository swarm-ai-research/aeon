*Skill Health — 2026-06-22*
HEALTH: DEGRADED(38)  [systemic: OAuth-outage residue — ISS-001]

🟡 DEGRADED (38, collapsed)
- All 38 carry-over skills from the 2026-06-06→2026-06-20 OAuth outage. Every one now last_status=success, consecutive_failures=0 — but cumulative success_rate stays <0.6 for ~weeks of clean runs. WAIT — no per-skill action. See [[issues/ISS-001]].

⚪ NO DATA (5): agi-tracker, ai-framework-watch, config-validator, run-frequency-guard, swarm-safety-eval — DISPATCH-SKILL (still never run since cron-state was last cleaned)
🟢 HEALTHY: 1 (weekly-shiplog promoted from NO DATA after first run 10:17Z)

Δ vs yesterday: NO DATA 6→5, HEALTHY 0→1, DEGRADED unchanged.
Open issues: 4 (ISS-001 investigating, ISS-002 changelog, ISS-005 swarm-safety-eval, ISS-006 batch outage) · Resolved this run: 0
INDEX.md drift: ISS-006 on disk but missing from Open table — operator fix.
