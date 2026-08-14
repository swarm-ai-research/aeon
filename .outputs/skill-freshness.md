*Skill Freshness — 2026-08-14*
⚠️ FRESHNESS_STALE — 3 of 5 deps flagged across 3 of 44 enabled consumers

Worst:
- heartbeat ← articles/token-report-*.md (MISSING — producer `token-report` disabled)
- weekly-shiplog ← articles/push-recap-*.md (MISSING — producer `push-recap` disabled)
- fleet-control ← articles/fleet-status-2026-08-14.md (MISSING — heuristic false-positive; fleet-control self-reads prior fleet-status; not a real gap)

Action: Enable `token-report` + `push-recap` if their data is wanted, or add <!-- skill-freshness:ignore --> to suppress. fleet-control finding is a prefix-mismatch known limitation.
Full: articles/skill-freshness-2026-08-14.md
