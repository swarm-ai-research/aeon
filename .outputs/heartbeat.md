HEARTBEAT_DEGRADED · STATUS_PAGE=DEGRADED

## Summary

Ran heartbeat. All findings dedup-filtered, no notification sent.

**Checks:**
- P0 failed/stuck: none. All skills `last_status: success`, no stuck `dispatched` rows.
- P0 chronic (<50% success): 38 skills — ISS-001 OAuth-outage residue, already systemic, dedup'd.
- P0 self-check: heartbeat last_success ~23h 50m ago, OK.
- P1 PRs / urgent issues: empty.
- P2 MEMORY priorities: 5 items carried over, dedup'd.
- P3 ISS-006 **day 5** — same narrow-pocket signature as yesterday (notegraph 05:00 + suggest-edges 05:30 ran ✅, compute-futures-eda 06:00 + planner 06:30 still silent). memory-flush/dedupe not scheduled today (DOM 25 = odd). DEDUP vs 06-24 notification.

**Files modified:**
- `docs/status.md` — regenerated (🔴 DEGRADED, 4 open issues, 44 skills listed, next run = fleet-control at 09:00 UTC; Token Pulse section omitted — no token-report article exists).
- `memory/logs/2026-06-25.md` — appended Heartbeat entry.

**Follow-up:** ISS-006 day-5 diagnostic from MEMORY priorities still pending — `gh run list --workflow=messages.yml --created=2026-06-25` to confirm `*/5` ticks landed at 06:00/06:05/06:10/06:30 today; manual `workflow_dispatch` of planner + memory-flush to rule out per-skill issues.
