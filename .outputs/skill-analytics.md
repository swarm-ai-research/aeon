## Summary

Skill analytics for the last 7 days (2026-07-01 → 2026-07-08) is complete.

**Findings:**
- **136 runs** across **39 active skills**, **100.0% success** rate (0 failures in the window)
- **4 anomalies — all 🔴 SILENT** (enabled cron skills with zero runs):
  1. `janitor` — Sun 05:30 UTC slot; last success 2026-06-20 (~18d); ISS-006 tributary
  2. `run-frequency-guard` — daily 23:00 UTC; no cron-state entry (never dispatched)
  3. `ai-framework-watch` — Mon 08:30 UTC; 3rd consecutive Monday non-arm; no cron-state entry
  4. `cost-report` — Mon 07:00 UTC; ISS-008; 3rd consecutive Monday miss

**Top runners:** pr-review (12), code-health/goal-tracker/reflect/skill-health/surplus-pulse (7 each)

**Exit taxonomy** (best-effort, 4 of 8 log files scanned): ok ~68%, uncategorized ~27% (structural-quiet: FLEET_EMPTY, GLMETRICS_EMPTY, NOTEGRAPH_NO_CHANGE — not failures), error ~3% (pr-triage cross-org 403 dispatch), new_info 1% (workflow-security-audit).

**Outputs written:**
- `articles/skill-analytics-2026-07-08.md`
- `dashboard/outputs/skill-analytics.json` (overwritten)
- `.pending-notify/1783540000-skill-analytics.md` (notification queued for post-run delivery — direct write per sandbox constraint)
- `memory/logs/2026-07-08.md` (log entry appended)
