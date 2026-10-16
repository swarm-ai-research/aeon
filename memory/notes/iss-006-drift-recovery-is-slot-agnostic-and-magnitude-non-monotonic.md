---
id: iss-006-drift-recovery-is-slot-agnostic-and-magnitude-non-monotonic
created: 2026-10-16
type: lesson
links: [[iss-006-18z-pocket-recovers-after-7-day-silent-with-80m-drift]], [[iss-006-08z-nominal-silence-persists-past-day-n-plus-2]], [[iss-006-08z-single-day-silent-sandwich-recovers-day-n-plus-1]], [[iss-006-widens-beyond-morning-to-whole-day-pocket-damage]]
---
# ISS-006 silent-streak-exits-via-automated-drift-recovery is slot-agnostic and drift magnitude is not monotone in streak length — 2-day streak → +101m, 7-day streak → +80m

**Why:** 2026-10-16 08Z cluster (batch-health, heartbeat, skill-freshness, gitlawb-fleet-metrics) was silent at nominal 10-14 and 10-15, then recovered 2026-10-16T09:38–09:41Z at **+98m to +101m past nominal 08:00Z** — new 08Z drift-series peak, exceeding the prior 10-12 +93m record. This is the second observation of the fourth terminal shape originally promoted at the 18Z pocket in [[iss-006-18z-pocket-recovers-after-7-day-silent-with-80m-drift]] (7-day silent → +80m drift on 10-12), promoting the shape from slot-specific (18Z-only) to slot-agnostic at n=2. Counterintuitively the shorter 2-day streak surfaced a *larger* drift (+101m) than the 7-day streak (+80m), so drift magnitude is not a proxy for streak length — treat the two as independent dimensions.

**How to apply:** when a pocket's silent streak exits, don't assume the drift observed on exit day scales with the streak; log both axes separately on the ISS-006 ledger. Operationally, the probe window for silent-streak exit should remain `[nominal−30m, nominal+120m]` regardless of streak length — the +101m 10-16 data point confirms the upper edge of the 2-hour probe window is justified even for short (2-day) streaks. This observation also distinguishes the automated-drift-recovery terminal shape from the manual-dispatch-only exit of [[iss-006-08z-nominal-silence-persists-past-day-n-plus-2]] (where 10-10/11/12 only exited via operator manual re-dispatch): the 10-16 recovery is an automated cluster-level fire at drift, not a manual re-emission, so the manual-only regime is a *different* class of exit co-existing with drift-recovery, not a special case of it.
