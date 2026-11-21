---
id: skill-freshness-flag-count-jumps-discontinuously-under-iss-006-silence
created: 2026-11-19
type: lesson
links: [[heartbeat-self-check-invisible-while-heartbeat-is-silent]], [[iss-006-widened-split-cohort-regime-preserves-08z-16z-drops-others]], [[monitor-monitored-coupling]], [[skill-freshness-mtime-blind-in-gha]]
---
# skill-freshness flag-count is a step function keyed on its own dispatch events — the 11-14 → 11-19 widened-split-cohort silence jumped flagged-deps 1→6 in a single recovery fire, with 4 of the 5 new flags themselves ISS-006-silent-cohort casualties

**Why:** 11-14 skill-freshness surfaced 1 flag; the skill then went silent 5 days under the widened split-cohort regime per [[iss-006-widened-split-cohort-regime-preserves-08z-16z-drops-others]] plus the 11-17 fleet-wide silent day per [[iss-006-fleet-wide-silent-day-recurs-on-11-17-at-5-day-cadence]], and the 11-19 recovery run surfaced 6 flags where 4 of 5 new flags are themselves ISS-006-silent-cohort casualties (skill-evals Sun-09Z 67d, vuln-scanner Sat-16Z 12d, workflow-security-audit Sun-16Z 11d, cost-report Mon-07Z 10d). Flag-count was already compounding during the blind period but only became operator-visible when the watchdog re-dispatched — same shape as heartbeat self-check breach appearing at magnitude 119h on 11-19 (vs 24h on 11-13) because heartbeat too was silent across the window.

**How to apply:** skill-freshness flag-count is non-monotone between dispatch events and aliases silent-staleness accumulation to its own cron cadence, so a single recovery dispatch under ISS-006 cohort silence can surface a week of accumulated flags at once — add a telemetry delta `flag_count_jump = ${today} − ${last_dispatch_count}` to distinguish accumulation-surfacing from single-regression detection. The 11-19 jump of +5 (1 → 6) is the first observation with jump-size ≥ 2 in the running series; prior fires have been Δ∈{−1, 0, +1} under clean weekly dispatch cadence.
