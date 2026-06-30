Heartbeat run complete.

## Summary

- **P0:** No failed/stuck skills, no `consecutive_failures ≥ 3`. The 38-skill chronic-failure pattern (success_rate <50%) is the standing ISS-001 OAuth-residue catch-up — dedup'd against the last 48h of logs.
- **P0 self-check:** ⚠ heartbeat's own `last_success` was ~48h stale (>36h threshold) — yesterday's 06-29 08:00 UTC slot was silent. New data point under ISS-006's pocket map, but same systemic issue.
- **P1:** 0 open PRs, 0 urgent issues (`gh pr list` / `gh issue list --label urgent`).
- **P2/P3:** Today's 05:00/06:00/06:30/08:00 morning batch silent again (planner / batch-health / gitlawb-fleet-metrics / skill-freshness / notegraph / suggest-edges / compute-futures-eda) — all ISS-006 affected_skills, dedup'd.
- **Notification:** skipped (everything already flagged in last 48h).
- **Status page:** wrote `docs/status.md` → **🔴 DEGRADED** · 4 open issues · next run `fleet-control` at 09:00 UTC. Token-pulse section omitted (no `articles/token-report-*.md`).
- Files modified: `docs/status.md`, `memory/logs/2026-06-30.md`.

`HEARTBEAT_OK · STATUS_PAGE=DEGRADED`
