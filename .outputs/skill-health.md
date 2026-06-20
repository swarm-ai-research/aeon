*Skill Health — 2026-06-20 18:05Z*
HEALTH: DEGRADED(38) — recovery from ISS-001 underway

🟡 DEGRADED (38, sample of top 5 by prior-fail count):
- compute-futures-eda — recovered 06:12Z, sr=0% (1/203)
- gitlawb-fleet-metrics — recovered 09:34Z, sr=1% (2/198)
- pr-review — recovered 09:35Z, sr=1% (2/198)
- skill-health — recovered 06:12Z, sr=1% (1/196)
- notegraph — recovered 06:14Z, sr=1% (1/189)
+33 more — all show consecutive_failures=0, last_status=success today

⚪ NO DATA (6): agi-tracker, ai-framework-watch, config-validator, run-frequency-guard, swarm-safety-eval, weekly-shiplog → DISPATCH-SKILL

SYSTEMIC: previous outage (zero-token cron runs, 2026-06-06→06-20) ended at 06:05Z when CLAUDE_CODE_OAUTH_TOKEN was restored. All 38 are healthy NOW; cumulative success_rate stays <60% (DEGRADED threshold) until ~weeks of clean runs raise the counters.

Open issues: 1 per INDEX.md (ISS-001 still 'investigating'; INDEX drift — ISS-002–005 are open on disk, missing from index). Resolved this run: 0. hash=89b162470bb193b6
