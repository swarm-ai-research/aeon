Heartbeat complete.

**HEARTBEAT_OK · STATUS_PAGE=DEGRADED** — wrote `docs/status.md`

## Summary
- **Findings:** 0 failed, 0 stuck, 0 API-degradation. All P0/P1/P3 items (ISS-001 residue day 41, ISS-006 4th-consecutive 08:00Z pocket drop, dependabot #8 stalled ~128h, ai-framework-watch + run-frequency-guard 23rd silent day) have 48h precedents → notification skipped per dedup.
- **Status page:** `🔴 DEGRADED` (P0 chronic failures from ISS-001 OAuth burn). Wrote `docs/status.md` wholesale — 5th consecutive rebase-clobber-then-regen from the 2026-06-09 baseline; snapshot-rebase gate still open (15d past urgency).
- **ISS-006 close-clock:** slides Day-7 → Day-8; earliest possible clean-close 08-02 → 08-03.
- **Files modified:** `docs/status.md`, `memory/logs/2026-07-31.md`.
