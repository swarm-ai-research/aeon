---
id: iss-006-05z-single-day-regression-promotes-to-multi-day-regime
created: 2026-10-14
type: lesson
links: [[iss-006-single-day-recovery-regression-generalizes-across-slots]], [[iss-006-08z-nominal-silence-persists-past-day-n-plus-2]], [[iss-006-widens-beyond-morning-to-whole-day-pocket-damage]], [[iss-006-pocket-recovery-is-noise]]
---
# After a single-day recovery of an ISS-006 pocket, the subsequent regression can run multiple days rather than one — 05Z's 10-10 recovery was followed by three consecutive silent-at-nominal days (10-11, 10-12, 10-13)

**Why:** The 10-10 05:53Z fire of notegraph + suggest-edges was treated by the 10-11/10-12 heartbeats under the single-day regression framing of [[iss-006-single-day-recovery-regression-generalizes-across-slots]], but the 10-13 heartbeat observed day-3 silence at 05Z — 10-11, 10-12, and 10-13 05:00Z slots all silent. Together with 23:45Z's parallel sequence (10-10 00:02Z fire → 10-11, 10-12 silent → day-2+ at a second slot), this promotes the regression class from "single-day" to "multi-day" at n=2 slots simultaneously. The 05Z observation is the clearest since the slot is daily and both consumers (notegraph + suggest-edges) share a single cron slot, so each silent day is a 2-skill casualty.

**How to apply:** treat any post-recovery regression at an ISS-006 pocket as a multi-day silent-at-nominal regime by default rather than a single-day stochastic miss; only downgrade after ≥2 consecutive clean fires at nominal cadence (not just a single-day fire followed by silence). The [[iss-006-pocket-recovery-is-noise]] rule tightens from "require 3 clean days before closing" to "a lone recovery followed by day-1 silence is evidence of multi-day regime, not noise." Heartbeat's P3 novel-scan should emit a `multi-day-regression-after-recovery` signal distinct from the first-day regression flag, so operators see the regime class on day-2 rather than day-N+k.
