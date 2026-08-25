HEARTBEAT_OK · STATUS_PAGE=DEGRADED — wrote docs/status.md.

## Summary

Ran `heartbeat` on 2026-08-25T08:10Z. **No fresh findings.** All P0 checks came back clean — yesterday's cost-report failure recovered on the very next run (`last_success: 2026-08-24T08:30:52Z`). The 38-skill ISS-001 Day-67 chronic-failure residue still trips the `success_rate < 0.5` P0 rule per spec, so the status-page verdict stays 🔴 DEGRADED, but every chronic entry has `last_status: success` + `cf: 0` and is exhaustively documented in the last 48h of logs — nothing fresh crosses the notify threshold. P1 stalled-PR queue (23 open) and P3 never-dispatched pair (`ai-framework-watch` + `run-frequency-guard`, 48d silent) both chronic and dedup'd. Regenerated `docs/status.md` (28th consecutive rebase-clobber-then-regen cycle) with all 44 enabled skills tabled and sorted by last-run desc; Token pulse section fully omitted (no `articles/` directory in the workspace).

- **Files modified:** `docs/status.md`, `memory/logs/2026-08-25.md`
- **Notification:** none sent (all findings dedup'd)
- **PRs / issues:** none opened
- **Follow-ups:** unchanged carryovers — docs/status.md snapshot-rebase-clobber gate patch (39d past threshold), ISS-021 draft for never-dispatched pair (37th-day carryover), ISS-001 close deferred until ISS-006 resolves.
