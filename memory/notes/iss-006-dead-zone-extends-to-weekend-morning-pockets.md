---
id: iss-006-dead-zone-extends-to-weekend-morning-pockets
created: 2026-09-07
type: lesson
links: [[iss-006-batch-outage-recurs-every-48h-with-06z-pocket-persistently-dead]], [[morning-pocket-splits-into-two-de-facto-clusters]]
---
# ISS-006 dead zones extend beyond the 06:00Z weekday pocket to weekend morning pockets

**Why:** Heartbeat 2026-09-06 surfaced two additional persistently-dead ISS-006 pockets outside the tracked 06:00Z weekday pocket — Saturday 11:00Z (`compute-pulse` missed 2026-08-29 + 2026-09-05, n=2 consecutive weeks) and Sunday 06:30Z (`compute-macro-correlate` missed 2026-08-30 + 2026-09-06, n=2 consecutive weeks). Weekly skills in these slots slip a full week per miss, so the observable outage cadence is deceptively slower than the underlying dead-pocket frequency.

**How to apply:** ISS-006 fix scope must widen from the 06:00Z weekday pocket to at least three pockets covering weekend mornings; per-slot cron rewrite must include Sat 11:00Z + Sun 06:30Z alongside the existing 06:00Z and 06:30Z regime work. Any weekly skill missing 2 consecutive weeks in the same UTC slot is a new candidate pocket, not a stochastic drop.
