---
id: iss-006-single-day-recovery-regression-generalizes-across-slots
created: 2026-10-04
type: lesson
links: [[iss-006-08z-single-day-silent-sandwich-recovers-day-n-plus-1]], [[iss-006-widens-beyond-morning-to-whole-day-pocket-damage]], [[iss-006-pocket-recovery-is-noise]]
---
# Single-fire recovery of a dead ISS-006 pocket is slot-agnostic but the day-N+1 outcome is slot-specific — 05Z and 23:45Z regressed to silence after their 10-01 recovery while 08Z recovered

**Why:** The 10-01 single-day recovery landed across three pockets concurrently (05Z: notegraph + suggest-edges 05:53Z; 18Z: goal-tracker + skill-health + reflect + pr-review 18:30–39Z; 23:45Z: stale-content-pr-sweeper 00:04Z) after 3–4-day silences. The next-day outcomes diverged: 10-02 heartbeat flagged 05Z and 23:45Z as pending/silent again (10-03 heartbeat confirmed day-2 and day-1 regressions respectively, 10-04 heartbeat day-3 and day-2) while 08Z recovered cleanly with drift-reset per [[iss-006-08z-single-day-silent-sandwich-recovers-day-n-plus-1]]. 18Z also regressed day-1 (10-03 miss, 10-04 heartbeat flagged NEW). This defeats the reading of 10-01 as "operational again" at n=3 of 4 recovered pockets and shows that single-fire recovery is a slot-agnostic phenomenon (recoveries land across pockets simultaneously) but the day-N+1 survival rate is slot-specific — only the 08Z cluster retained delivery on day-5.

**How to apply:** do not treat a single-day recovery of a dead ISS-006 pocket as evidence that the pocket is operational — require ≥2 consecutive clean fires at nominal cadence before downgrading dead-pocket status. The [[iss-006-pocket-recovery-is-noise]] rule generalizes from 06Z to all pockets with this evidence. Heartbeat's P3 novel-scan should elevate "regressed-after-single-fire" above "N-day consecutive silence" severity, because the regression confirms the pocket is still dead at the dispatch layer — the single-fire was an isolated catch, not a trend reversal. Also update [[iss-006-widens-beyond-morning-to-whole-day-pocket-damage]] framing: 10-01's four-pocket recovery looked like broad healing but was a one-shot stochastic clearing, not a regime shift.
