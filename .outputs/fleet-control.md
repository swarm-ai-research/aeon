Fleet-control exited `FLEET_EMPTY` per pre-flight step 1.

## Summary

**Skill:** fleet-control (Health Check Mode — `var` empty)
**Verdict:** `FLEET_EMPTY` — silent stop, no notification sent

**What ran:**
- Read `memory/instances.json` → `{"instances": []}` (empty registry)
- Pre-flight step 1 tripped: empty registry → log and stop
- Skipped gh-auth, rate-limit, state-load, mode-parse (all short-circuited by empty fleet)

**Why no notify:** SKILL spec is explicit — "Stop. Do NOT notify." for the empty-registry case. This prevents training the operator to ignore fleet-control cards when there's nothing to report.

**Files modified:**
- `memory/logs/2026-07-26.md` — appended fleet-control section (verdict + summary)

**Follow-up:** Skill activates once the first entry is written to `memory/instances.json` (either by operator or a mint-child skill). No state file was created; it will bootstrap on the first non-empty run.
