## Summary

Heartbeat ran at 2026-06-28 08:14 UTC (~14m after dispatch — cleanest morning lag of the week).

**P0:** clean — no failed/stuck/degrading skills. ISS-001 OAuth residue (38 skills with `success_rate < 0.5`) still triggers the 🔴 DEGRADED verdict but stays dedup'd. Heartbeat self-check OK (~22h 29m).

**New finding (notified):** the 05:00 UTC pocket is newly silent — `notegraph` and `suggest-edges` last_success 2026-06-26T05:50–53Z (~50h stale, >2x daily threshold). Both missed 06-27 and 06-28 dispatches. This widens **ISS-006** beyond morning/09:00/23:45 into a fourth pocket and suggests the dead zones are sliding day-to-day rather than fixed. Action unchanged: per-slot crons in `messages.yml` covering every `aeon.yml` timeslot.

**Dedup'd:** 09:00 batch dead 6d (carry-over), memory-flush/memory-structural-dedupe 194h stale (ISS-006), 5 never-run skills.

**Files modified:**
- `docs/status.md` — regenerated, 🔴 DEGRADED, 44 enabled skills, 4 open issues, next run = fleet-control at 09:00 UTC, Token Pulse section omitted (no `articles/token-report-*.md`).
- `memory/logs/2026-06-28.md` — heartbeat log entry appended.
- `.pending-notify/heartbeat-2026-06-28.md` — notification queued for post-run delivery (sandbox fallback; `./notify` direct invocation blocked by shell-syntax guard).

HEARTBEAT_DEGRADED · STATUS_PAGE=DEGRADED
