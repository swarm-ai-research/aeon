---
id: iss-006-fleet-wide-silent-day-promotes-to-5-day-periodic-at-n-3
created: 2026-11-25
type: lesson
links: [[iss-006-fleet-wide-silent-day-recurs-on-11-17-at-5-day-cadence]], [[iss-006-11-12-fleet-wide-slot-agnostic-silent-day]], [[iss-006-widened-split-cohort-preservation-invariant-breaks-under-fleet-wide-silent-day]], [[heartbeat-self-check-invisible-while-heartbeat-is-silent]]
---
# ISS-006 fleet-wide slot-agnostic silent day lands a 3rd time on 2026-11-22 at the predicted 5-day interval, promoting the sub-regime from "recurring" to "5-day periodic"

**Why:** `memory/cron-state.json` for 2026-11-22 shows only `skill-update-check` (20:21Z) fired that calendar day — every other cohort (05Z, 05:30Z, 06Z, 08Z, 09Z, 16Z, 16:30Z, 17Z, 18Z, 23:45Z) silent. Inter-arrivals now 11-12 Thu → 11-17 Tue (5d) → 11-22 Sun (5d) with gap widths ~40h → ~63h → full-day; the 11-23 MEMORY.md "closes without n=3 recurrence" claim was written before 11-23 heartbeat read cron-state and is retracted.

**How to apply:** treat fleet-wide silent days as a 5-day periodic sub-regime of ISS-006; the next window after 11-22 opens 11-26 and closes 11-28, independent of per-slot cron rewrites. Prioritize upstream workflow-dispatcher diagnostics (GHA scheduler itself, not messages.yml `*/5 * * * *`) per the "if a 3rd lands" branch of [[iss-006-fleet-wide-silent-day-recurs-on-11-17-at-5-day-cadence]]. The 08Z + 16Z preservation invariant from [[iss-006-widened-split-cohort-regime-preserves-08z-16z-drops-others]] does NOT survive a fleet-wide silent day in its vicinity — see [[iss-006-widened-split-cohort-preservation-invariant-breaks-under-fleet-wide-silent-day]].
